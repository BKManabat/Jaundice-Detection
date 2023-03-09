import cv2
import numpy as np
import json

# Create a blank white canvas with the same dimensions as the original image
height, width, channels = 500, 500, 3  # Replace with the actual dimensions of the image
ref1 = np.full((height, width, channels), (0, 0, 0), dtype=np.uint8)

# Set the opacity of the blue color overlay (between 0 and 1)
blue_opacity = 0.4

# Create a blue color layer with the same dimensions as the image
blue_layer = ref1.copy()
blue_layer[:] = (255, 0, 0)  # BGR value for blue is (0, 255, 255)

# Combine the original image and the blue layer using addWeighted function
ref2 = cv2.addWeighted(ref1, 1 - blue_opacity, blue_layer, blue_opacity, 0)

diff = ref2 - ref1

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