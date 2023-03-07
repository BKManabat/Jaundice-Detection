import cv2
from skinscan import skin_detect

# Start capturing video from default webcam
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video stream
    ret, frame = cap.read()

    frame = skin_detect(frame)
    cv2.imshow('Dominant Color Detection', frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and destroy the window
cap.release()
cv2.destroyAllWindows()