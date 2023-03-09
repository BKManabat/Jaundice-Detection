import numpy as np
import cv2

# Define skin tone colors
skin_tones = [
    [45, 34, 30], [60, 46, 40], [75, 57, 50], [90, 69, 60], [105, 80, 70],
    [120, 92, 80], [135, 103, 90], [150, 114, 100], [165, 126, 110], [180, 138, 120],
    [195, 149, 130], [210, 161, 140], [225, 172, 150], [240, 184, 160], [255, 195, 170],
    [255, 206, 180], [255, 218, 190], [255, 229, 200]
]

# Create empty lists to store before and after images
before_images = []
after_images = []

# Loop through each skin tone color and apply different opacities of yellow to it
for skin_tone in skin_tones:
    for opacity in range(1, 101):
        # Create a yellow layer with the same dimensions as the pixel
        yellow_layer = np.zeros((1, 1, 3), dtype=np.uint8)
        yellow_layer[:] = (255, 255, 0)  # Set the color to yellow

        # Set the pixel color to the current skin tone color
        pixel = np.zeros((1, 1, 3), np.uint8)
        pixel[0, 0] = skin_tone

        # Overlay the yellow layer onto the pixel with the current opacity
        result = cv2.addWeighted(pixel, 1 - opacity / 100, yellow_layer, opacity / 100, 0)

        # Extract the yellow opacity value as an integer
        yellow_opacity = int(opacity)

        # Add the yellow opacity value to the green channel of the result pixel
        r, g, b = result[0, 0]
        result[0, 0] = [r, g + yellow_opacity, b]

        # Check if the condition is satisfied
        if opacity == 4:
            # Add before and after images to their respective lists
            before = np.zeros((50, 50, 3), np.uint8)
            before[:] = skin_tone
            after = np.zeros((50, 50, 3), np.uint8)
            after[:] = result

            # Write the yellow opacity value on the after pixel
            # cv2.putText(after, str(yellow_opacity), (10, 30), cv2.FONT_HERSHEY_PLAIN, 0.9, (0, 0, 0), 1)

            before_images.append(before)
            after_images.append(after)
            break

# Concatenate all before and after images horizontally
before_all = np.concatenate(before_images, axis=1)
after_all = np.concatenate(after_images, axis=1)

yellow_tones = [list(pixel[0][0]) for pixel in after_images]
differences = [abs(x[1]-x[2]) for x in yellow_tones]

print(yellow_tones)
print(differences)

# Concatenate the before and after images vertically
display_img = np.concatenate((before_all, after_all), axis=0)

# Convert BGR to RGB and display the final image
display_img = cv2.cvtColor(display_img, cv2.COLOR_BGR2RGB)
cv2.imshow("Result", display_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
