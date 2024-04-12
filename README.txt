Outlined below are the necessary steps for running the audiotrope software:

1. Upload the frame_detection.ino file to the arduino which will be tracking frames 
	via magnetic proximity sensor.

2. With a computer connected to both the arduino and the USB camera, run capture_frames.py
	to get images of all frames.

3. Create a folder to act as a "root" and store everything required for calibration.

4. Create two subfolders within, "images" and "audio".

5. Within "images" create a subfolder named "whole_scene" and place all frames from step 2
	in here.

6. Within "images" create subfolders for each desired action object. In each folder copy the
	images of the frames within which the action object exists. Crop these images such
	that they only show the action object.

7. Within "audio" create subfolders for each desired action object, name the same as the
	respective subfolders in "images". Within these folders place any WAV files
	corresponding to the action object.

8. Run calibration.py, save the produced JSON file.

9. With a computer connected to both the arduino and USB camera, and the zoetrope running
	in a dark room, run audiotrope.py. Import JSON file from step 8 and enjoy!