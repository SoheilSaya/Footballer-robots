from collections import deque
from imutils.video import VideoStream
import numpy
import argparse
import cv2
import pygame
import imutils
import time
import math
upperlowers = [
    [(220,10,10),(255,10,10),0,'blue'], #blue
    [(10, 220, 10),(10, 255, 10),1,'green'],
    
    [(8, 8, 220), (12, 12, 255),2,'red']
]
pts = []
for i in range(len(upperlowers)):
    pts.append(i)
    pts[i]=deque(maxlen=64)


white = (230, 230, 230)
red = (230, 10, 10)
green = (10, 230, 10)
blue = (10, 10, 230)
black = (10, 10, 10)
rect1 = pygame.Rect(60, 60, 60, 60)
rect2 = pygame.Rect(540, 300, 60, 60)
circle_pos = [200, 300]
circle_radius = 30
grid_size = 10
screen_width, screen_height = 600, 600
window_size = (600, 600)
cell_width = screen_width // grid_size
cell_height = screen_height // grid_size
def calculate_angle_and_distance(x1, y1, x2, y2):
    # Calculate the distance between the two points using the distance formula
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    # Calculate the angle between the two points using trigonometry (arctan)
    angle_rad = math.atan2(y2 - y1, x2 - x1)
    angle_deg = math.degrees(angle_rad)

    # Ensure the angle is in the range of [0, 360)
    if angle_deg < 0:
        angle_deg += 360

    print( angle_deg, distance)

def pygame_surface_to_cv2_image(surface):
    # Convert Pygame surface to OpenCV image object
    img_array = numpy.array(pygame.surfarray.pixels3d(surface))
    img_array = numpy.transpose(img_array, (1, 0, 2))
    img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    return img_array

def colorpicker(lowerband,upperband,index,pts,colorname,blurred,frame):
    mask = cv2.inRange(blurred, lowerband, upperband)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None
    radius=0
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    if radius > 10:
        cv2.circle(frame, (int(x), int(y)), int(radius),(255, 255, 255), 2)
        cv2.circle(frame, center, 5, (255, 255, 255), -1)
    pts[index].appendleft(center)




def pygame_surface_to_cv2_image(surface):
    img_array = numpy.array(pygame.surfarray.pixels3d(surface))
    img_array = numpy.transpose(img_array, (1, 0, 2))
    img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    return img_array
