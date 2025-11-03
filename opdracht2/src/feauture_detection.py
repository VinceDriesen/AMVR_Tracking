import cv2
import numpy as np
import os

SAVE_INTERVAL = 20


def _load_image(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Image not found: {path}")
    image = cv2.imread(path)
    if image is None:
        raise IOError(f"Failed to load image: {path}")
    return image


def _load_video(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Video file not found: {path}")
    video = cv2.VideoCapture(path)
    if not video.isOpened():
        raise IOError(f"Could not open video file: {path}")
    return video


def _create_orb_detector(n_features):
    return cv2.ORB_create(nfeatures=n_features)  # type: ignore


def _match_features(bf, desc1, desc2, ratio=0.75):
    matches = bf.knnMatch(desc1, desc2, k=2)
    return [m for m, n in matches if m.distance < ratio * n.distance]


def process(
    target_img_path: str,
    use_webcam: bool,
    video_path: str = "",
    overlay_video_path: str = "",
    n_features=1000,
):
    """Processes each frame of the given video, and matches its features with the given image.
        Optionally can overlay a video on the refernce image found in the video

    Args:
        target_img_path (str): Location of the reference image
        use_webcam (bool): Whether to use the webcam for processing
        video_path (str, optional): Location of the video to process if use_webcam = False
        overlay_video_path (str, optional): Location of the video to overlay
        n_features (int, optional): Maximum amount of keypoints to be detected by ORB. Defaults to 1000.
    """
    target_img = _load_image(target_img_path)
    if use_webcam:
        video = cv2.VideoCapture(0)
    else:
        video = _load_video(video_path)

    orb = _create_orb_detector(n_features)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)

    keypoints_img, descriptors_img = orb.detectAndCompute(target_img, None)

    overlay_video = None
    if overlay_video_path:
        overlay_video = _load_video(overlay_video_path)

    h_t, w_t = target_img.shape[:2]
    pts_target = np.float32([[0, 0], [w_t, 0], [w_t, h_t], [0, h_t]]).reshape(-1, 1, 2) # type: ignore

    video_writer = None
    if not use_webcam:
        os.makedirs(os.path.dirname("output/output_video.mp4"), exist_ok=True)
        fps = video.get(cv2.CAP_PROP_FPS)
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # type: ignore
        video_writer = cv2.VideoWriter(
            "output/output_video.mp4", fourcc, fps, (width, height)
        )

    while True:
        success, frame = video.read()
        if not success:
            print("End of video or failed to read frame.")
            break

        keypoints_vid, descriptors_vid = orb.detectAndCompute(frame, None)
        if descriptors_vid is None:
            continue

        good_matches = _match_features(bf, descriptors_img, descriptors_vid)
        if len(good_matches) < 10:
            if video_writer:
                video_writer.write(frame)
            else:
                cv2.imshow("Feature Matching / Overlay", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
                continue

        src_pts = np.float32(
            [keypoints_img[m.queryIdx].pt for m in good_matches]  # type: ignore
        ).reshape(-1, 1, 2)
        dst_pts = np.float32(
            [keypoints_vid[m.trainIdx].pt for m in good_matches]  # type: ignore
        ).reshape(-1, 1, 2)

        H, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 3.0)

        if H is not None:
            if overlay_video:  # Draw overlay_video at detected position
                ret, overlay_frame = overlay_video.read()
                if not ret:
                    overlay_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    ret, overlay_frame = overlay_video.read()
                    
                overlay_frame = cv2.resize(overlay_frame, (frame.shape[1], frame.shape[0]))

                warped_overlay = cv2.warpPerspective(
                    overlay_frame, H, (frame.shape[1], frame.shape[0])
                )

                mask_overlay = np.any(warped_overlay > 0, axis=2).astype(np.uint8) * 255
                mask_inv = cv2.bitwise_not(mask_overlay)

                bg = cv2.bitwise_and(frame, frame, mask=mask_inv)
                fg = cv2.bitwise_and(warped_overlay, warped_overlay, mask=mask_overlay)

                frame = cv2.add(bg, fg)
            else:  # Draw detected position
                dst = cv2.perspectiveTransform(pts_target, H)
                frame = cv2.polylines(
                    frame,
                    [np.array(dst, dtype=np.int32)],
                    True,
                    (0, 255, 0),
                    3,
                    cv2.LINE_AA,
                )

        if video_writer:
            video_writer.write(frame)
        else:
            cv2.imshow("Feature Matching / Overlay", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    video.release()
    if overlay_video:
        overlay_video.release()
    if video_writer:
        video_writer.release()
    cv2.destroyAllWindows()