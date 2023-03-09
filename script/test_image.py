import cv2
from skinscan import skin_detect, offset_frame, yellow_mask

# Load the image file
img = cv2.imread('./data/jaundice/1-blue.png')

cv2.imshow("Original", img)

# Detect skin in the image
img = offset_frame(img)
# img = yellow_mask(img, yellow_opacity=0.1)
img = skin_detect(img)

# Show the resulting image
cv2.imshow('Dominant Color Detection', img)
cv2.waitKey(0)

# Destroy the window
cv2.destroyAllWindows()
