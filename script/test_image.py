import cv2
from skinscan import skin_detect, offset_frame

# Load the image file
img = cv2.imread('./data/jaundice/1-blue.png')
cv2.imshow("Original", img)

# cv2.namedWindow('Dominant Color Detection', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('Dominant Color Detection', 800, 600)

# Detect skin in the image
img = offset_frame(img)
img = skin_detect(img)

# Save the resulting image as a PNG file
cv2.imwrite('result.png', img)

# Show the resulting image
cv2.imshow('Dominant Color Detection', img)
cv2.waitKey(0)

# Destroy the window
cv2.destroyAllWindows()
