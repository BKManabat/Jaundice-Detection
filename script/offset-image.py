import cv2
import numpy as np
import json

# This script computes for the offset values for detecting skin in blue light

img1 = cv2.imread('./data/jaundice/3.png') # reference image without blue light
img2 = cv2.imread('./data/jaundice/3-blue.png') # reference image with blue light

# Computer for raw difference
diff = img2 - img1

# Compute the average of the difference in each channel
blue_offset = np.mean(diff[:, :, 0])
green_offset = np.mean(diff[:, :, 1])
red_offset = np.mean(diff[:, :, 2])

offsets = {
    'blue': blue_offset,
    'green': green_offset,
    'red': red_offset,
}

# Save raw offset as image
cv2.imwrite('./assets/raw_offset.png', diff)

# Save the offsets to a JSON file
with open('./assets/offsets.json', 'w') as f:
    json.dump(offsets, f)

print(offsets)