from gpiozero import Button

button = Button(17)

print('Start the test-button program.')

print('Wait for button pressing.')

button.wait_for_press()

print('The button is pressed!')

print('The program ends.')