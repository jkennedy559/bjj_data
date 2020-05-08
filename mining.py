from offset_enum import OffsetValues as oe
import matplotlib.pyplot as plt
import os
import cv2

# Load scraped screenshots
images = os.listdir('screenshots')
image = cv2.imread('screenshots/' + images[5], cv2.IMREAD_COLOR)

# Extract images from original screenshot
score_box = image[oe.scoreboard_upper_y:oe.scoreboard_lower_y,
                  oe.scoreboard_left_x:oe.scoreboard_right_x]

header = image[oe.header_upper_y:oe.header_lower_y,
               oe.header_left_x:oe.header_right_x]

competitor_1_points = image[oe.competitor_1_points_upper_y:oe.competitor_1_points_lower_y,
                            oe.competitor_1_points_left_x:oe.competitor_1_points_right_x]

competitor_2_points = image[oe.competitor_2_points_upper_y:oe.competitor_2_points_lower_y,
                            oe.competitor_2_points_left_x:oe.competitor_2_points_right_x]


def sanitise_image(img, inversion=True):
    """Process image extractions for optical character recognition"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening
    return invert if inversion is True else opening


sanitise_list = [(header, False),
                 (competitor_1_points, True),
                 (competitor_2_points, False)]


cleaned_extractions = [sanitise_image(*sanitise) for sanitise in sanitise_list]
cleaned_extractions.insert(0, score_box)


def visualise(vis):
    """Plot single image"""
    visual = cv2.cvtColor(vis, cv2.COLOR_RGB2BGR)
    plt.imshow(visual, cmap='gray', interpolation='bicubic')
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    return plt


def visualise_grid(vis_list):
    """Plot all extracted images from single match"""
    fig = plt.figure()
    fig.suptitle('Extracted Images', fontsize=16)
    ax1 = fig.add_subplot(2, 2, 1)
    ax1 = visualise(vis_list[0])
    ax2 = fig.add_subplot(2, 2, 2)
    ax2 = visualise(vis_list[1])
    ax3 = fig.add_subplot(2, 2, 3)
    ax3 = visualise(vis_list[2])
    ax4 = fig.add_subplot(2, 2, 4)
    ax4 = visualise(vis_list[3])
    return plt


fig_cleaned = visualise_grid(cleaned_extractions)


