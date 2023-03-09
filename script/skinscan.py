import numpy as np
import cv2
import json

def offset_frame(frame, raw=False):
    frame_adjusted = frame.copy()

    if not raw:
        # Load the channel offsets from a JSON file
        with open("./assets/offsets.json", "r") as f:
            offsets = json.load(f)

        blue_offset = offsets["blue"]
        green_offset = offsets["green"]
        red_offset = offsets["red"]

        # Subtract channel offsets
        frame_adjusted[:,:,0] = frame[:,:,0] - blue_offset
        frame_adjusted[:,:,1] = frame[:,:,1] - green_offset
        frame_adjusted[:,:,2] = frame[:,:,2] - red_offset
    else:
        # Load raw offset image and subtract it to frame
        diff = cv2.imread("./assets/raw_offset.png")
        frame_adjusted = frame - diff
    
    return frame_adjusted


def skin_detect(frame):
    # Convert the frame to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Apply Kovac's rules to detect skin regions
    r, g, b = cv2.split(frame)
    
    rule1 = (r > 38) & (g > 16) & (b > 8)
    rule2 = np.abs(np.max([r, g, b], axis=0) - np.min([r, g, b], axis=0)) > 15
    rule3 = np.abs(r - g) > 15
    rule4 = (r > g) & (r > b)
    rule5 = (r < (g + 100))

    skin_region = np.logical_and.reduce((rule1, rule2, rule3, rule4, rule5))
    
    # Ratio model
    # skin_region = ((r + g) != 0) & ((abs(r - g) / (r + g)) <= 0.5) & ((b / (r + g)) <= 0.5)

    # Convert the boolean mask to a binary image
    skin_region = skin_region.astype(np.uint8) * 255

    # Perform morphological closing to fill small holes
    se = np.ones((3, 3), dtype=np.uint8)
    skin_region = cv2.morphologyEx(skin_region, cv2.MORPH_CLOSE, se)

    # Find contours in the skin region
    contours, hierarchy = cv2.findContours(skin_region, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        # Draw the contours on the source image and get the dominant color of each contour
        areas = [(cv2.contourArea(c), c, i) for i, c in enumerate(contours)]
        max_area = max(areas, key=lambda x: x[0])

        # Get the bounding rectangle of the contour
        x, y, w, h = cv2.boundingRect(max_area[1])

        # Crop the image to the bounding rectangle
        bounded = frame[y:y+h, x:x+w]

        # Get the height and width of the image
        height, width = bounded.shape[:2]

        # Calculate the amount to be cropped
        h_crop = int(height * 0.2)
        w_crop = int(width * 0.2)

        # Create a new NumPy array representing the cropped region
        crop = bounded[h_crop:height-h_crop, w_crop:width-w_crop]
        
        # Get dominant color in crop
        n_clusters = 5
        data = cv2.resize(crop, (100, 100)).reshape(-1, 3)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        flags = cv2.KMEANS_RANDOM_CENTERS
        compactness, labels, centers = cv2.kmeans(data.astype(np.float32), n_clusters, None, criteria, 10, flags)
        cluster_sizes = np.bincount(labels.flatten())
        palette = []
        
        for cluster_idx in np.argsort(-cluster_sizes):
            # Create a palette of each color with its RGB values
            color = centers[cluster_idx].astype(int)
            color_palette = np.full((frame.shape[0], frame.shape[1], 3), fill_value=color, dtype=np.uint8)

            # Check for yellow tinge
            if color[1] - color[2] > 40:
                # Add text to indicate yellowing detected
                print("Yellowing detected")
                cv2.putText(frame, "Yellowing detected", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                cv2.circle(color_palette, (int(frame.shape[1]/2), int(frame.shape[0]/2)), 20, (255, 0, 0), -1)

            palette.append(color_palette)
            # Add text to palette indicating the RGB values for each color
            text = "R:{} G:{} B:{}".format(color[2], color[1], color[0])
            cv2.putText(color_palette, text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 4)

        palette = np.hstack(palette)
        sf = frame.shape[1] / palette.shape[1]
        frame = np.vstack([frame, cv2.resize(palette, (0, 0), fx=sf, fy=sf)])

        # Draw the contour
        cv2.drawContours(frame, contours, max_area[2], (0, 255, 0), 3)

    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    return frame


def yellow_mask(frame, yellow_opacity = 0.4):
    # Create a yellow color layer with the same dimensions as the image
    yellow_layer = frame.copy()
    yellow_layer[:] = (0, 255, 255)  # BGR value for yellow is (0, 255, 255)

    # Combine the original image and the yellow layer using addWeighted function
    frame = cv2.addWeighted(frame, 1 - yellow_opacity, yellow_layer, yellow_opacity, 0)
    return frame
