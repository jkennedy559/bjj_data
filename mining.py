from offset_enum import OffsetValues as oe
from tensorflow import keras
import matplotlib.pyplot as plt
import os
import cv2
import numpy as np
import pandas as pd


def visualise(images, main_title=''):
    for i, image in enumerate(images):
        plt.suptitle(f'{main_title}', fontsize=14)
        plt.subplot(10, 10, i + 1)
        plt.imshow(image, 'gray')
        plt.xticks([]), plt.yticks([])
    return plt


# Read screenshot
screenshots = os.listdir('screenshots/')
images = list()
for screenshot in screenshots[0:50]:
    image = cv2.imread('screenshots/' + screenshot, cv2.IMREAD_GRAYSCALE)
    raw_1 = image[oe.competitor_1_points_upper_y:oe.competitor_1_points_lower_y,
            oe.competitor_1_points_left_x:oe.competitor_1_points_right_x]
    raw_2 = image[oe.competitor_2_points_upper_y:oe.competitor_2_points_lower_y,
            oe.competitor_2_points_left_x:oe.competitor_2_points_right_x]
    raw_1 = cv2.threshold(raw_1, 170, 255, cv2.THRESH_BINARY_INV)[1]
    raw_2 = cv2.threshold(raw_2, 170, 255, cv2.THRESH_BINARY)[1]
    images.extend([raw_1, raw_2])

# Resize to 28/28
images_resized = [cv2.resize(image, (28, 28), interpolation=cv2.INTER_LINEAR) for image in images]

# Erosion for better focus
#kernel = np.ones((3, 3), np.uint8)
#images_erosion = [cv2.erode(image, kernel, iterations=1) for image in images_resized]

# Format for modelling
df = pd.read_csv('test_target.csv', index_col=0, na_values='None')

features = np.dstack(images_resized)
features = np.rollaxis(features, -1)
features = np.expand_dims(features, -1)
features = features.astype("float32") / 255
features = features[(df.target.notna()) & (df.target <= 10)]

target = df.target[(df.target.notna()) & (df.target <= 10)]
target = target.to_numpy()
target = keras.utils.to_categorical(target, 10)

# Visualise features
features_vis = np.split(features[:, :, :, 0], 87, axis=0)
features_vis = [i[0, :, :] for i in features_vis]

# TODO - Amend pictures to improve performance on 6 & 9
# Model pipeline
score = model.evaluate(features, target, verbose=0)
predictions = np.argmax(model.predict(features), axis=1)
print("Test loss:", score[0])
print("Test accuracy:", score[1])


# Visualise errors
visualise(features_vis)

for (i, image), prediction in zip(enumerate(features_vis), predictions):
    plt.suptitle(f'', fontsize=14)
    plt.subplot(10, 10, i + 1)
    plt.imshow(image, 'gray')
    plt.text(6, 21, f'{prediction}', fontsize=20, color='red')
    plt.xticks([]), plt.yticks([])