# Jaundice-Detection

This repository contains code for monitoring jaundice in newborn infants using image processing algorithms. Detection of yellow pigmentation in skin is done in four steps: color correction, skin region identification, color palette extraction, and color thresholding. The code libraries used are NumPy and OpenCV respectively.

## Color Correction

Color correction is the process of adjusting the colors of an image to remove any unwanted color casts and make the colors appear natural. In the case of jaundice monitoring, color correction is necessary due to the presence of phototherapy light; making it difficult for the subsequent skin region identification algorithm to accurately pinpoint the skin area. As such, the presence of phototherapy light in an image must be filtered out to get the most accurate result.

## Skin Region Identification

A modified version of Kovac's rules is used to identify pixels as skin. The original model has four rules that define a pixel as skin based on its RGB values. However, Tomaz et al. noted issues with the original rules, which did not account for certain conditions such as high R-value and low G and B values, yellow-like colors, and darker skin tones. Therefore, the modified rules are designed to account for these conditions and increase the accuracy of skin identification.

## Color Palette Extraction

Once the skin region has been identified, K-means clustering is used to determine the dominant colors within that region. K-means clustering is a popular unsupervised machine learning algorithm used for clustering similar data points together. The algorithm works by partitioning a dataset into k clusters based on the similarity of the data points. In this case, the data points are the pixel values within the identified skin region, and the resulting clusters are the dominant colors within that region.

## Color Thresholding

Upon having extracted the dominant colors within the identified skin region, the next step is to check whether a color exhibits yellow pigmentation. Tomaz et al. noted that when G is greater than 150 and B is less than 90 or when R + G is greater than 400, the pixel displays a yellow-like color. This could be handled by adding another rule that excludes pixel values that satisfy those conditions. However, within the context of the problem, we can leverage this limitation by using the provided values as the threshold for determining if a dominant color demonstrates yellowness.

## Usage

The code is written in Python and requires NumPy and OpenCV libraries to run. The code for each step is contained in separate files in the ```script``` folder and can be run independently or as a complete pipeline.

```offset.py``` generates the offset values based on the loaded reference images
```skinscan.py``` contains two functions, ```offset_frame``` and ```skin_detect```

```
import cv2
from skinscan import skin_detect, offset_frame

# Load the image file
img = cv2.imread('./data/jaundice/1-blue.png')

# Detect skin in the image
img = offset_frame(img)
img = skin_detect(img)

# Show the resulting image
cv2.imshow('Dominant Color Detection', img)
cv2.waitKey(0)

# Destroy the window
cv2.destroyAllWindows()
```

## Credits

This code references the work of Kovac et al. and Tomaz et al. in their respective papers on skin pixel identification using image processing techniques.
