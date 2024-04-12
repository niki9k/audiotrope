import cv2
import numpy as np
import glob
import os
import json
import tkinter
from tkinter import filedialog


def match(template_img, whole_frame):
    temp = cv2.imread(template_img, cv2.IMREAD_GRAYSCALE)

    assert temp is not None, "file could not be read, check with os.path.exists()"
    w, h = temp.shape[::-1]

    img = cv2.imread(whole_frame, cv2.IMREAD_GRAYSCALE)
    assert img is not None, "file could not be read, check with os.path.exists()"

    method = eval('cv2.TM_CCOEFF_NORMED')
    res = cv2.matchTemplate(img, temp, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    return [max_loc[1], max_loc[1] + h, max_loc[0], max_loc[0] + w]


print("Please select the root directory: ")
tkinter.Tk().withdraw()  # prevents an empty tkinter window from appearing
root_dir = filedialog.askdirectory(mustexist=True)
frame_dir = glob.glob(root_dir + '/images/whole_scene' + '/*.png')

total_frames = len(frame_dir)

frame_images = []

for i in range(total_frames):
    frame_images.append(root_dir + '/images/whole_scene/frame' + str(i + 1) + '.png')

key_objects = []
isObjDone = 0
key_object_frame_dirs = []

while not isObjDone:
    print("Select the image directory of a key object (cancel if done): ")
    tkinter.Tk().withdraw()  # prevents an empty tkinter window from appearing
    obj_dir = filedialog.askdirectory(mustexist=True)
    if obj_dir == '':
        isObjDone = 1
    else:
        key_obj = obj_dir.split('/')
        key_obj = str(key_obj[-1])
        key_objects.append(key_obj)

audio_files = []
obj_audio_dirs = []

for obj in key_objects:
    key_object_frame_dirs.append(root_dir + '/images/' + obj)
    obj_audio_dirs.append(root_dir + '/audio/' + obj)

    obj_audio = []

    for sound in glob.glob(root_dir + '/audio/' + obj + '/*.wav'):
        obj_audio.append(sound)

    audio_files.append(obj_audio)


calib = {}

obj_count = 0
for obj in key_objects:

    obj_values = {}
    for i in range(total_frames):

        if os.path.exists(key_object_frame_dirs[obj_count] + '/frame' + str(i+1) + '.png'):

            coords = match(key_object_frame_dirs[obj_count] + '/frame' +
                           str(i+1) + '.png', frame_images[i])
            obj_values[str(i + 1)] = coords

    calib[obj] = {"audio": audio_files[obj_count],
                  "location": obj_values}
    obj_count += 1

filename = raw_input("Save settings as: ") + ".json"
with open(filename, 'w') as export_file:
    json.dump(calib, export_file)
