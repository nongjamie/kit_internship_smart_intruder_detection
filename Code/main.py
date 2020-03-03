# Import the necessary module
from gpiozero import MotionSensor
from google.cloud import storage
from firebase import firebase
from picamera import PiCamera
from gpiozero import Button
import Manual as manualObj
import Auto as autoObj
import threading
import datetime
import pyrebase
import time
import sys
import os

# Global variables
camera = None
button = Button(17)
pir = MotionSensor(4)
raspi_status = None
is_connect_db = False

# Global variables for firebase storage
bucket_name = 'fir-realtimeweb-69681.appspot.com'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'GOOGLE_APPLICATION_CREDENTIALS.json'
storage_client = storage.Client()
bucket = storage_client.get_bucket(bucket_name)
        
# Implement the feature in raspberry pi
def implement_in_raspi(receiveData):
    global button, camera, pir, bucket
    modeSplit = receiveData['mode'].split('-')
    commandType = modeSplit[0]
    commandFunc = modeSplit[1]
    commandName = modeSplit[2]
    commandParam = receiveData['parameter']
    modeName = commandType + '-' + commandFunc + '-' + commandName
    if commandType == 'auto':
        camera = PiCamera()
        if commandFunc == 'capture':
            if commandName == 'countdown':
                # auto-capture-countdown
                # user_delay = int(commandParam)
                user_delay = 5
                autoObj.captureCountdownObj.capture_countdown(camera, datetime, time, user_delay, bucket, os)
            elif commandName == 'detectIntruder':
                # auto-capture-detectIntruder
                autoObj.captureDetectIntruderObj.capture_detect_intruder(pir, datetime, camera, time, bucket, os)
            else:
                print("Don't have " + modeName + " command.")
        elif commandFunc == 'record':
            if commandName == 'countdown':
                # auto-record-countdown
                paramBox = commandParam.split(',')
                # user_delay = int(paramBox[0])
                # user_duration = int(paramBox[1])
                user_delay = 5
                user_duration = int(paramBox[0])
                autoObj.recordCountdownObj.record_countdown(camera, datetime, time, user_delay, user_duration, bucket, os)
            elif commandName == 'detectIntruder':
                # auto-record-detectIntruder
                user_duration = int(commandParam)
                autoObj.recordDetectIntruderObj.record_detect_intruder(pir, datetime, camera, time, user_duration, bucket, os)
            else:
                print("Don't have " + modeName + " command.")
        else:
            print("Don't have " + modeName + " function.")
    elif commandType == 'manual':
        camera = PiCamera()
        if commandFunc == 'record':
            # manual-capture-record
            manualObj.recordButtonObj.record_button(camera, button, datetime, time, bucket, os)
        elif commandFunc == 'capture':
            # manual-capture-button
            manualObj.captureButtonObj.capture_button(camera, button, time, datetime, bucket, os)
        else:
            print("Don't have " + modeName + " function.")
    elif commandType == 'video':
        if commandFunc == 'live':
            if commandName == 'start':
                start_live_video()
            else:
                stop_live_video()
        else:
            print("Don't have " + modeName + " function.")
    else:
        print("Don't have " + modeName + " feature.")        

def start_live_video():
    os.system('python3 LIVE_video/start_video_live.py')
    
def stop_live_video():
    os.system('python3 LIVE_video/stop_video_live.py')

# Restart the program
def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

# Function for checking the status with the database
def connect_with_database():
    global raspi_status, first_time, firebase, is_connect_db
    firebase = firebase.FirebaseApplication('https://fir-realtimeweb-69681.firebaseio.com/', None)
#    firebase = firebase.FirebaseApplication('https://vuejs-http-9ad70.firebaseio.com/', None)
    result = firebase.get('/status', None)
    command_list = list(result.values())
    last_index = len(command_list) - 1
    raspi_status = command_list[last_index]
    is_connect_db = True
    while True:
        result_2 = firebase.get('/status', None)
        command_list_2 = list(result_2.values())
        last_index_2 = len(command_list_2) - 1
        raspi_status_2 = command_list_2[last_index_2]
        if raspi_status == raspi_status_2:
            time.sleep(3)
            continue
        else:
            if not camera == None:
                camera.close()
            print('\n==================')
            print('The current feature has changed. Restart the program.')
            print('==================\n')
            restart_program()

def run_storage_checking():
    os.system('python3 Storage/storage.py')

# Running the program
db_thread = threading.Thread(target = connect_with_database)
db_thread.start()
#run_storage_checking()
while True:
    if is_connect_db:
        print('Selected feature: ' + raspi_status['mode'])
        implement_in_raspi(raspi_status)
        print('... <Raspi Thread> stops ...')
        print('... <Connect with DB Thread> is still running ...')
        break
    else:
        time.sleep(1)
        continue
#implement_in_raspi({'mode': 'manual-capture-button', 'parameter': ''})
#camera = PiCamera()
#camera.close()