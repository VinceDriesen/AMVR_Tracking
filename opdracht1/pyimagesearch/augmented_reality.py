import numpy as np
import cv2

# Dit is voor caching, om zo geen flickering te krijgen als je bij de ene frame wel tags vind, en bij de frame daarna niet. 
CACHED_REf_PTS = None




# frame
# : The input frame from our video stream
# source
# : The source image/frame that will be warped onto the input frame
# cornerIDs : The IDs of the ArUco tags that we need to detect arucoDict
# : OpenCV’s ArUco tag dictionary
# arucoParams
# : The ArUco marker detector parameters
# useCache
# : A boolean indicating whether or not we should use the reference point caching method
#
def find_and_warp(frame, source, cornerIDs, arucoDict, arucoParams, useCache=False):
    # Grab a reference to our cached reference points variable
    global CACHED_REf_PTS

    # Grab the width and height of the frame and source image, respectively
    (imgH, imgW) = frame.shape[:2]
    (srcH, srcW) = source.shape[:2]
    
    # Detect ArUco markers in the input frame
    (corners, ids, rejected) = cv2.aruco.detectMarkers(frame,
        arucoDict, parameters=arucoParams)

    # If we did not find our four ArUco markers, initialize an empty Ids list, ohterwise flatten the ArUco IDs list
    ids = np.array([]) if len(corners) == 0 else ids.flatten()

    # Initialize a list to store our reference points
    refPts = []

    for i in cornerIDs:
        # Grab the index of the corner with the current ID
        j = np.squeeze(np.where(ids == i))

        # If we receive an empty list instead of an integer index, then we could not find the marker with the current ID
        if j.size == 0:
            continue

        # Otherwise, append the corner (x, y)-coordinates to our reference points list
        corner = np.squeeze(corners[j])
        refPts.append(corner)

        # But what ahppens if we could not find all four reference points?
        # Check to see if we found all four reference points
    if len(refPts) != 4:
        # If we are allowed to use chached reference points, fall back on them
        if useCache and CACHED_REf_PTS is not None:
            refPts = CACHED_REf_PTS

        # Otherwise, we cannot use the cache andor or there are no cached reference points, so return None
        else:
            return None
    # If we are allowed to use chaching reference points, then update the cache with the current set.
    if useCache:
        CACHED_REf_PTS = refPts

    # Unpack our ArUco reference points and use the reference points to define the *destination* transform matrix, making sure the points are specified in top-left, top-right, bottom-right, and bottom-left order
    (refPtTL, refPtTR, refPtBR, refPtBL) = refPts
    dstMat = [refPtTL[0], refPtTR[1], refPtBR[2], refPtBL[3]]
    dstMat = np.array(dstMat)
    # Define the transform matrix for the *source* image in top-left, top-right, bottom-right, and bottom-left order
    srcMat = np.array([[0, 0], [srcW, 0], [srcW, srcH], [0, srcH]])
    # compute the homography matrix and then warp the source image to the destination based on the homography
    (H, _) = cv2.findHomography(srcMat, dstMat)
    warped = cv2.warpPerspective(source, H, (imgW, imgH))

    # Construct a mask for the source image now that the prespctive warp has take place
    mask = np.zeros((imgH, imgW), dtype="uint8")
    cv2.fillConvexPoly(mask, dstMat.astype("int32"), (255, 255, 255), cv2.LINE_AA)

    # Black border around the warped source image
    rect = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask = cv2.dilate(mask, rect, iterations=2)

    # Create a three channel version of the mask by stacking it depth-wise, such that we can copy the warped source image into the input image
    maskScaled = mask.copy() / 255.0
    maskScaled = np.dstack([maskScaled] * 3)

    # Copy the warped source image into the input input by 1, multiplying the warped image and masked together, 2, then multiplying the orgriginal input img with the mask and 3, adding the resulting multiplications together
    warpedMultiplied = cv2.multiply(warped.astype("float"), maskScaled)
    frameMultiplied = cv2.multiply(frame.astype(float), 1.0 - maskScaled)
    output = cv2.add(warpedMultiplied.astype("uint8"), frameMultiplied.astype("uint8"))
    # Return the output frame
    return output




