import cv2
import numpy as np
import json

# This script computes for the offset values for detecting skin in blue light

img1 = cv2.imread('./data/jaundice/3.png') # reference image without blue light
img2 = cv2.imread('./data/jaundice/3-blue.png') # reference image with blue light

# Find difference between images
diff = img2 - img1

# Adjust channels of img2 to match diff
img2_adjusted = img2 - diff

# Compute the average of the difference in each channel
blue_offset = np.mean(diff[:, :, 0])
green_offset = np.mean(diff[:, :, 1])
red_offset = np.mean(diff[:, :, 2])

offsets = {
    'blue': blue_offset,
    'green': green_offset,
    'red': red_offset,
}
print(offsets)

# Save raw offset as image
cv2.imwrite('./assets/raw_offset.png', diff)

# Save the offsets to a JSON file
with open('./assets/offsets.json', 'w') as f:
    json.dump(offsets, f)

# Show result
cv2.imshow('Result', img2_adjusted)
cv2.waitKey(0)
cv2.destroyAllWindows()
