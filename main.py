from ObjectDetection import *
from Methods import *
import os

# create saved_frames folder to save captured frames
if not os.path.exists('saved_frames'):
   os.makedirs('saved_frames')

# Big Colored Balls Bouncing Video URL Link
cap = read_url("https://www.youtube.com/watch?v=c5py4O9kUn0")
frame_counter = 0

while True:
    ret, frame = cap.read()

    # if ret is False stop the loop
    if not ret:
        break

    frame_counter += 1

    # create object detection variable to use mask_creator() method
    object_detection = ObjectDetection(frame)
    height, width, mask = object_detection.mask_creator()

    # create contours variable to use it for drawing box
    # use mask only on the left side of the video
    contours, _ = cv.findContours(mask[0:int(height), 0:int(width / 2)], cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    left_side = frame[0:int(height), 0:int(width / 2)]

    # draw rectangle to show detected objects
    center_points_current = draw_rectangle(contours, left_side)

    # send error messages to the terminal and post request
    show_error(center_points_current, frame_counter, frame)

    # show the results on video
    cv.imshow("Frame", frame)

    # press 'q' to quit
    if cv.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
# cv.destroyAllWindows() gives an error, so I did not put it here

