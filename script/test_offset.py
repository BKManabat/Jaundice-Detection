import cv2
import numpy as np
import json

# Load img2
img2 = cv2.imread('./data/jaundice/3-blue.png')

# Load the channel offsets from a JSON file
with open("./assets/offsets.json", "r") as f:
    offsets = json.load(f)

blue_offset = offsets["blue"]
green_offset = offsets["green"]
red_offset = offsets["red"]

# Method 1: Adjust channels of img2 using average offsets
img2_adjusted1 = img2.copy()
img2_adjusted1[:,:,0] = img2[:,:,0] - blue_offset
img2_adjusted1[:,:,1] = img2[:,:,1] - green_offset
img2_adjusted1[:,:,2] = img2[:,:,2] - red_offset

# Method 2: Load raw offset image and add it to img2
diff = cv2.imread("./assets/raw_offset.png")
img2_adjusted2 = img2 - diff

# Show the two methods side-by-side
cv2.imshow("Method 1", img2_adjusted1)
cv2.imwrite("Method1.png", img2_adjusted1)
cv2.imshow("Method 2", img2_adjusted2)
cv2.waitKey(0)
cv2.destroyAllWindows()
