from pyimagesearch.augmented_reality import find_and_warp
from imutils.video import VideoStream
from collections import deque
import argparse
import imutils
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str, required=True,
                help="path to input video file for augmented reality")
ap.add_argument("-c", "--cache", type=int, default=-1,
                help="whether or not to use reference points cache")
args = vars(ap.parse_args())

# Load the ArUCo dictionary and grab the ArUCo parameters
print("[INFO] initializing marker detector...")
arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)
arucoParams = cv2.aruco.DetectorParameters()

# Initialize the video file stream
print("[INFO] accessing video stream...")
vf = cv2.VideoCapture(args["input"])

# Initialize a queue to maintain the next frame from the video stream
Q = deque(maxlen=128)

# We need to have a frame in our queue to start our augmented reality pipeline, so read the next frame from our video file source and add it to our queue
(grabbed, source) = vf.read()
Q.appendleft(source)

# Initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

# Loop over the frames from the video file stream
while len(Q) > 0:
    # Grab the frame from our video stream and resize it
    frame = vs.read()
    frame = imutils.resize(frame, width=600)

    # Attampt to find the markers in the frame, and provided they are found, take the current source image and warp it onto the input frame using our augmented reality technique
    warped = find_and_warp(frame, source, 
                           cornerIDs=(923, 1001, 241, 1007),
                            arucoDict=arucoDict,
                            arucoParams=arucoParams,
                            useCache=args["cache"] > 0)

    # If the warepd frame is not None, then we know we successfully found the markers and warped the source image onto the input frame
    if warped is not None:
        frame = warped
        source = Q.popleft()

    # For speed/efficinecy, we can use a queue to keep the next video frame queue ready for us. The trick is to ensure the queue is always full
    if len(Q) != Q.maxlen:
        (grabbed, frame) = vf.read()

        # If we are unable to grab a frame, then we have reached the end of the video file
        if grabbed:
            Q.append(frame)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(10) & 0xFF

    if key == ord("q"):
        break

    cv2.destroyAllWindows()
    vs.stop()



