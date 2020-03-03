from gpiozero import MotionSensor
from picamera import PiCamera
from time import sleep

camera = PiCamera()
pir = MotionSensor(4)
camera.rotation = 180
filename = "../intruder-record/test-intruder.h264"

while True:
    pir.wait_for_motion()
    print("Motion Detected")
    camera.start_recording(filename)
    sleep(3)
    pir.wait_for_no_motion()
    camera.stop_recording()
    question = input("Do you wanna continue monitoring? (Y)es or (N)o: ")
    if question == 'n':
        break
    
