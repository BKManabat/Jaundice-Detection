import cv2

# Load the image
img = cv2.imread('./data/normal/2.png')

# Set the opacity of the yellow color overlay (between 0 and 1)
yellow_opacity = 0.4

# Create a yellow color layer with the same dimensions as the image
yellow_layer = img.copy()
yellow_layer[:] = (0, 255, 255)  # BGR value for yellow is (0, 255, 255)

# Combine the original image and the yellow layer using addWeighted function
result = cv2.addWeighted(img, 1 - yellow_opacity, yellow_layer, yellow_opacity, 0)

# Display the result
cv2.imshow('Result', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
