import pymedia
import cv2
import numpy as np
import json
import glob
import serial
import random
import tkinter
from tkinter import filedialog
from imutils.video import WebcamVideoStream

serial_port = serial.Serial(port='COM3', baudrate=115200)

# kernel for erosion and dilation
kernel = np.ones((9, 9), np.uint8)

TOTAL_FRAMES = 16


def thresholding(img):
    # convert frame image to greyscale, and then blur
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (17, 17), 0)

    # binary threshold on the frame
    re, thr = cv2.threshold(blur, 250, 255, cv2.THRESH_BINARY)

    # erosion and then dilation on the frame
    opened = cv2.morphologyEx(thr, cv2.MORPH_OPEN, kernel)

    return opened


players = []
""" List to hold the pymedia Player instances for each key object."""

audio = []
""" List to store paths to all the necessary audio files. """

print('Please select the calibration file')
tkinter.Tk().withdraw()
filename = filedialog.askopenfilename()
with open(filename, 'r') as importfile:
    calib = json.load(importfile)

obj_num = len(calib)
""" Total number of calibrated objects. """
print(obj_num)

obj_coords = []
""" List to hold the coordinates of each "action object" in each frame. """

for obj in calib:

    audio.append(calib[obj]['audio'])

    coords = [None]*TOTAL_FRAMES

    new_player = pymedia.Player()
    new_player.start()
    players.append(new_player)

    for frame in range(TOTAL_FRAMES):
        if str(frame+1) in calib[obj]['location']:
            coords[frame] = (calib[obj]['location'][str(frame+1)])

    obj_coords.append(coords)


current_frame = None
"""Variable to hold what the current frame is """

prev_frame = None
""" Variable to hold what the previous frame was"""

prev_obj = None
""" Variable to hold the index of the previously illuminated object, if any """


cap = WebcamVideoStream(src=1).start()
while True:
    current_frame = serial_port.readline().decode().strip()
    current_frame = int(current_frame)

    frame = cap.read()
    # process the frame
    thresh = thresholding(frame)

    obj_detected = False
    """ Variable to hold whether or not an "action" object is illuminated in the frame.
        Initially False, True if object detected. """

    current_obj = None
    """ Variable to hold the index of the current illuminated object, if any """

    if (current_frame is not None) and (current_frame > 0) and (current_frame != prev_frame):
        for i in range(obj_num):
            if obj_coords[i][current_frame-1] is not None:
                temp_frame = thresh[obj_coords[i][current_frame-1][0]:obj_coords[i][current_frame-1][1],
                                    obj_coords[i][current_frame-1][2]:obj_coords[i][current_frame-1][3]]

                if 255 in temp_frame:
                    obj_detected = True
                    current_obj = i
                    print('Detected object ' + str(current_obj))
                    break

        # If no key objects are illuminated and a sound is currently playing, stop the sound
        if not obj_detected:
            print("No objects of interest are illuminated.")
            if prev_obj is not None:
                players[prev_obj].stopPlayback()
                print("Stopped playback for object " + str(prev_obj) + ".")
                current_obj = None

        else:
            if current_obj != prev_obj:
                # if there was an object detected in the previous frame, and it is not the same as the current object,
                # stop the playback of sound for the previous object
                if prev_obj is not None and players[prev_obj].isPlaying():
                    players[prev_obj].stopPlayback()
                    print("Stopped playback for object " + str(prev_obj) + ".")

                if audio[current_obj]:
                    # play sound for detected object
                    players[current_obj].startPlayback(random.choice(audio[current_obj]))
                    print("Playing audio for object " + str(current_obj) + ".")

        prev_frame = current_frame
        prev_obj = current_obj

    # display frames and exit
    cv2.imshow('original frame', frame)
    #cv2.imshow('threshold frame', thresh)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
cap.stop()
