import cv2 as cv
import numpy as np


class ObjectDetection:

    """
        With the help of ObjectDetection class, we will extract
        the objects we would like to detect from the background
        and other objects.
    """

    def __init__(self, frame):
        self.frame = frame

    def mask_creator(self):

        """
            This function creates lower and upper boundaries to
            extract the red color. It returns the mask variable
            to detect the objects with color red.
        """

        # changing the color space into HSV from BGR
        hsv_frame = cv.cvtColor(self.frame, cv.COLOR_BGR2HSV)

        # creating mask to detect red objects
        lower_boundary = np.array([0, 50, 20])
        upper_boundary = np.array([10, 255, 255])

        height, width, _ = self.frame.shape

        # creating mask
        mask = cv.inRange(hsv_frame, lower_boundary, upper_boundary)

        return height, width, mask
