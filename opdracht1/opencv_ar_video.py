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
arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
arucoParams = cv2.aruco.DetectorParameters()

# Initialize the video file stream
print("[INFO] accessing video stream...")
vf = cv2.VideoCapture(args["input"])

# Initialize a queue to maintain the next frame from the video stream
Q = deque(maxlen=128)

# We need to have a frame in our queue to start our augmented reality pipeline, 
# so read the next frame from our video file source and add it to our queue
(grabbed, source) = vf.read()
if grabbed:
    Q.appendleft(source)
else:
    print("[ERROR] Could not read first frame from video file. Exiting.")
    exit()

# Initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

# Loop over the frames from the video file stream
while len(Q) > 0:
    # Grab the frame from our video stream and resize it
    frame = vs.read()
    if frame is None:
        print("[ERROR] Failed to grab frame from webcam.")
        break
    frame = imutils.resize(frame, width=600)

    # Attempt to find the markers in the frame, and provided they are found, 
    # take the current source image and warp it onto the input frame
    warped = find_and_warp(frame, source,
                           cornerIDs=(0, 1, 3, 2),
                           arucoDict=arucoDict,
                           arucoParams=arucoParams,
                           useCache=args["cache"] > 0)

    # If the warped frame is not None, we successfully found the markers
    if warped is not None:
        frame = warped  # Update the frame to be the warped one
        if len(Q) > 0:  # Only pop if queue is not empty
            source = Q.popleft()

    # Refill the queue if it's not full
    if len(Q) != Q.maxlen:
        (grabbed, next_source_frame) = vf.read() # <-- VARIABELE HERNOEMD

        # If we are unable to grab a frame, we've reached the end
        if grabbed:
            Q.append(next_source_frame) # <-- GEBRUIK NIEUWE VARIABELE
        else:
            # If video ends but we still have frames in queue, 
            # we might want to break or let it empty out.
            # For now, we just stop adding.
            pass

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(10) & 0xFF

    if key == ord("q"):
        break

# --- OPKUISEN NA DE LOOP ---
# Deze stonden verkeerd (binnen de loop)
cv2.destroyAllWindows()
vs.stop()
vf.release() # Goede praktijk om ook de videofile-reader te sluiten
