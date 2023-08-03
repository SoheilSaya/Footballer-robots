from collections import deque
from imutils.video import VideoStream
import numpy
import argparse
import cv2
import pygame
import imutils
import time
import math
import toolbox

pygame.init()
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())


# Set screen size
screen_width, screen_height = 600, 600
window_size = (600, 600)
screen = pygame.display.set_mode((screen_width, screen_height))
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
cell_width = screen_width // grid_size
cell_height = screen_height // grid_size
print(cell_width,cell_height)
cv2_image = toolbox.pygame_surface_to_cv2_image(screen)
frame=cv2_image
frame_height = frame.shape[0]
frame_width = frame.shape[1]
print(frame_height)
print(frame_width)
counter=0
running = True
text_color = (0, 0, 0)
font_size = 32
font = pygame.font.Font(None, font_size)
text_surface = font.render("", True, text_color)
position = (window_size[0] // 2 - text_surface.get_width() // 2, window_size[1] // 2 - text_surface.get_height() // 2)
cellpos=[[] for _ in range(3)]

while running:
    
    circle_pos[0]+=60
    circle_pos[1]-=60
    rect1.x+=60
    rect2.y-=60
    time.sleep(0.9)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(white)
    pygame.draw.rect(screen, red, rect1)
    pygame.draw.rect(screen, green, rect2)
    pygame.draw.circle(screen, blue, circle_pos, circle_radius)
    
    for i in range(grid_size + 1):
        pygame.draw.line(screen, black, (i * cell_width, 0), (i * cell_width, screen_height))
        pygame.draw.line(screen, black, (0, i * cell_height), (screen_width, i * cell_height))
    
    pygame.display.flip()
    
    cv2_image = toolbox.pygame_surface_to_cv2_image(screen)
    frame=cv2_image
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    for i in range(len(upperlowers)):
        #print(i)
        toolbox.colorpicker(upperlowers[i][0],upperlowers[i][1],upperlowers[i][2],pts,upperlowers[i][3],blurred,frame)

    for j,jtem in enumerate(pts):
        for i in range(1, len(pts[j])):
            counter+=1
            if jtem[i - 1] is None or jtem[i] is None:
                continue
            try:
                if jtem[0][0]==jtem[1][0] and jtem[0][1]==jtem[1][1] and counter>3:
                    continue
            except:
                print(Exception)
                pass
            thickness = int(numpy.sqrt(args["buffer"] / float(i + 1)) * 2.5)
            cv2.line(frame, jtem[i - 1], jtem[i], (255, 255, 255), thickness)
            if jtem[0] is not None:
                print(pts[j][i],f"set {j} {upperlowers[j][3]}")
                xcell=int((pts[j][0][0]/(frame_width/10))+1)
                ycell=int((pts[j][0][1]/(frame_height/10))+1)
                print(xcell,'x')
                print(ycell,'y')
                cellpos[j].append([xcell,ycell])
                text_surface = font.render(f"({xcell},{ycell}) {upperlowers[j][3]}      ", True, text_color,(255,255,255))
                screen.blit(text_surface, (300,300+30*j))
                try:
                    toolbox.calculate_angle_and_distance(pts[0][-1][0],pts[0][-1][1],pts[1][-1][0],pts[1][-1][1])
                    toolbox.calculate_angle_and_distance(pts[0][-1][0],pts[0][-1][1],pts[2][-1][0],pts[2][-1][1])
                except:
                    print(Exception)
                    pass
                #print(cellpos[1][-1][i]-cellpos[0][-1][i])
                #print(cellpos[0][-1][i]-cellpos[1][-1][i])


                pygame.display.flip()
            else:
                print("none")
        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1) & 0xFF

        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break

# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
    vs.stop()

# otherwise, release the camera
else:
    vs.release()

# close all windows
cv2.destroyAllWindows()
# Quit Pygame
pygame.quit()
