from picamera import PiCamera
from gpiozero import Button

# Initialized
camera = PiCamera()
button = Button(17)
camera.rotation = 180

# Stop motion
print('The test-stop-motion starts.')
counter = 1
max = 20
print('The program will automatically exit when counter = {}.'.format(max))
while counter <= max:
    try:
        print('Counter = ' + str(counter))
        button.wait_for_press()
        camera.capture('/home/pi/Desktop/Parent_Detector/animation/frame%03d.jpg' % counter)
        print('Take the picture, ' + str(counter) + ' round.')
        counter += 1
    except KeyboardInterrupt:
        break
print('The test-stop-motion finishes.')
print('The program ends.')