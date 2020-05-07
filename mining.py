import cv2
import os
import matplotlib.pyplot as plt
import pytesseract

# List of match images
images = os.listdir('screenshots')
image = cv2.imread('screenshots/' + images[100], cv2.IMREAD_COLOR)


def visualise(vis):
    visual = cv2.cvtColor(vis, cv2.COLOR_RGB2BGR)
    plt.imshow(visual, cmap='gray', interpolation='bicubic')
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    return plt


for i, image in enumerate(images[100:120]):
    img = cv2.imread('screenshots/' + image, cv2.IMREAD_COLOR)
    plot = visualise(img[1260:1450, 110:760])
    plot.savefig(f'Match {i}.png')



image[1328:1440, 130:750]

# TODO Function: Extract cleaned scores
# Clean image
gray = cv2.cvtColor(score, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3, 3), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
invert = 255 - opening

# Perform text extraction
print(pytesseract.image_to_string(invert, lang='eng', config='--psm 6 --oem 3 '))

# TODO Function to piece together the brackets from the podium