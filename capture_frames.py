import cv2
import serial

serial_port = serial.Serial(port='COM3', baudrate=115200)     # TODO: add timeout??????????


cap = cv2.VideoCapture(1)  # video capture source camera (Here webcam of laptop)

current_frame = None
prev_frame = None

while cap.isOpened():

    ret, img = cap.read()  # return a single frame in variable `frame`

    current_frame = serial_port.readline().decode().strip()

    if current_frame is not None:
        if current_frame != '0' and current_frame != prev_frame:
            print current_frame
            cv2.imwrite('frame' + current_frame + '.png', img)
            prev_frame = current_frame

    if cv2.waitKey(1) == ord('q'):  # quit on pressing q
        serial_port.close()
        cap.release()
        cv2.destroyAllWindows()
        break
