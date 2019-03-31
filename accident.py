# Import necessary packages
from functools import reduce
import numpy as np
import cv2
import math
import operator
import time
# Function to find difference in frames

flag = 0
count = 0


def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)


j = 1
# Import video from webcam
cam = cv2.VideoCapture(0)

# Creating window to display
winName = "Accident Detector"
cv2.namedWindow(winName, cv2.WINDOW_AUTOSIZE)

# Reading frames at multiple instances from webcam to different variables
t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
time.sleep(3)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
time.sleep(3)
t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

k = 1
while k < 400:
    # Display video out through the window we created
    cv2.imshow(winName, t_minus)
    cv2.waitKey(1)

    k = k+1
    # Calling function diffImg() and assign the return value to 'p'
    p = diffImg(t_minus, t, t_plus)

    # Writing 'p' to a directory
    cv2.imwrite("./photos/shot.jpg", p)

    # From Python Image Library(PIL) import Image class
    from PIL import Image

    # Open image from the directories and returns it's histogram'
    for i in range(1, 5):
        h1 = Image.open("./motion/shot"+str(112+i)+".jpg").histogram()
        h2 = Image.open("./photos/shot.jpg").histogram()
        j = j+1

    # Finding rms value of the two images opened before
        rms = math.sqrt(reduce(operator.add, map(
            lambda a, b: (a-b)**2, h1, h2))/len(h1))
        # print(int(rms))
    # If the RMS value of the images are under our limit
        if (rms < 300):
            count += 1

        # Updates the frames
    t_minus = t
    t = t_plus
    t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

    # Destroys the window after key press

cv2.destroyWindow(winName)
if(count > 5):
    flag = 1
print(flag)
