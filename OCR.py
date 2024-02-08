import RPi.GPIO as GPIO
import cv2
import pytesseract
import pyttsx3
import threading

# Set up GPIO for the button
GPIO.setmode(GPIO.BOARD)
button_pin = 10  # Change this to the GPIO pin connected to the button
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize the OCR engine (Tesseract)
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Flag to check if the button was pressed
button_pressed = False

# Function to handle button press event
def button_callback(channel):
    global button_pressed
    button_pressed = True

# Event listener for button press
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_callback, bouncetime=300)

# Function to capture image and perform OCR
def capture_image():
    global button_pressed
    while True:
        if button_pressed:
            # Capture image using OpenCV
            camera = cv2.VideoCapture(0)
            return_value, image = camera.read()
            cv2.imwrite('captured_image.jpg', image)
            camera.release()

            # Perform OCR on the captured image
            extracted_text = pytesseract.image_to_string('captured_image.jpg')

            # Read the extracted text aloud
            engine.say(extracted_text)
            engine.runAndWait()

            button_pressed = False  # Reset the button state
            

# Start the image capture thread
image_thread = threading.Thread(target=capture_image)
image_thread.daemon = True
image_thread.start()

# Start continuous video feed
camera = cv2.VideoCapture(0)

while True:
    return_value, frame = camera.read()
    cv2.imshow('Video Feed', frame)

    # Check for 'q' key to exit
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cv2.destroyAllWindows()
camera.release()
GPIO.cleanup()