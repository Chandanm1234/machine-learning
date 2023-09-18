import cv2
import pyautogui
import numpy as np

# Initialize the camera
cap = cv2.VideoCapture(0)

# Set the screen width and height (you can adjust these values)
screen_width, screen_height = pyautogui.size()

while True:
    ret, frame = cap.read()

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert the frame to grayscale for hand detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise and improve accuracy
    gray = cv2.GaussianBlur(gray, (7, 7), 0)

    # Threshold the image to extract the hand region
    _, thresholded = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Find the largest contour, which should be the hand
        hand_contour = max(contours, key=cv2.contourArea)

        # Get the center of the hand
        M = cv2.moments(hand_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # Map the hand position to the screen resolution
            mapped_x = np.interp(cx, [0, frame.shape[1]], [0, screen_width])
            mapped_y = np.interp(cy, [0, frame.shape[0]], [0, screen_height])

            # Move the mouse to the mapped position
            pyautogui.moveTo(mapped_x, mapped_y)

    cv2.imshow("Hand Gesture Mouse Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
