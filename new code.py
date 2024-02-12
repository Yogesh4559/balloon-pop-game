# Import
import pygame
import cv2
import numpy as np
import random
from cvzone.HandTrackingModule import HandDetector
import time

# Initialize
pygame.init()

# Create Window /Display
width, height = 1230, 660
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Balloon Pop")

# Initial Clock for FPS
fps = 40
clock = pygame.time.Clock()

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1230)  # width
cap.set(4, 660)   # height

# Initialize Sound Mixer
pygame.mixer.init()

# Load Sound File
pop_sound = pygame.mixer.Sound(r"C:\Users\sange\OneDrive\Desktop\virtual balloon Buster\BalloonPopGame-main\popping tone.mp3") 

# Load Balloon Images
balloon_image1 = pygame.image.load(r"C:\\Users\\sange\\OneDrive\\Desktop\\virtual balloon Buster\\BalloonPopGame-main\\Images\\belun.png").convert_alpha()
balloon_image2 = pygame.image.load(r"C:\Users\sange\OneDrive\Desktop\virtual balloon Buster\BalloonPopGame-main\Images\purple.png").convert_alpha()
balloon_image3 = pygame.image.load(r"C:\Users\sange\OneDrive\Desktop\virtual balloon Buster\BalloonPopGame-main\Images\Yellow balloon.png").convert_alpha()

# Create a List of Balloon Images
balloon_images = [balloon_image1, balloon_image2, balloon_image3]

# Initialize the Index of the Current Balloon Image
current_balloon_index = 0

# Choose the Initial Balloon Image
current_balloon_image = balloon_images[current_balloon_index]

# Merge balloons
rectBalloon = current_balloon_image.get_rect()
rectBalloon.x, rectBalloon.y = 500, 300

# Variables
speed = 5
score = 0
scoreb = 0
startTime = time.time()
totalTime = 100

# Detector
detector = HandDetector(detectionCon=0.4, maxHands=5)

def resetBalloon():
    rectBalloon.x = random.randint(100, int(cap.get(3)) - 100)
    rectBalloon.y = int(cap.get(4)) + 50

# Main Loop
start = True
while start:
    # Get events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()

    # Apply Logic
    timeRemain = int(totalTime - (time.time()-startTime))
    if timeRemain < 0:
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB = np.rot90(imgRGB)
        frame = pygame.surfarray.make_surface(imgRGB).convert()
        frame = pygame.transform.flip(frame, True, False)
        window.blit(frame, (0, 0))

        font = pygame.font.Font(None, 50)
        textScore = font.render(f'Your Score: {score}', True, (255, 50, 50))
        textScoreb = font.render(f'Total Crash: {scoreb}', True, (255, 50, 50))
        textTime = font.render(f'Time Up', True, (255, 50, 50))
        window.blit(textScore, (450, 400))
        window.blit(textScoreb, (450, 350))
        window.blit(textTime, (490, 300))
    else:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, flipType=False)

        rectBalloon.y -= speed
        if rectBalloon.y < 0:
            resetBalloon()
            speed += 1

        if hands:
            hand = hands[0]
            x, y, z = hand['lmList'][8]
            if rectBalloon.collidepoint(x, y):
                resetBalloon()
                score += 5
                speed += 1
                scoreb += 1

                pop_sound.play()

                # Move to the Next Balloon Image
                current_balloon_index = (current_balloon_index + 1) % len(balloon_images)
                current_balloon_image = balloon_images[current_balloon_index]

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB = np.rot90(imgRGB)
        frame = pygame.surfarray.make_surface(imgRGB).convert()
        frame = pygame.transform.flip(frame, True, False)
        window.blit(frame, (0, 0))
        window.blit(current_balloon_image, (rectBalloon))

        font = pygame.font.Font(None, 50)
        textScore = font.render(f'Total Score: {score}', True, (255, 50, 50))
        textScoreb = font.render(f'Total Crash: {scoreb}', True, (255, 50, 50))
        textTime = font.render(f'Remain Time: {timeRemain}', True, (255, 50, 50))
        window.blit(textScore, (35, 35))
        window.blit(textScoreb, (35, 80))
        window.blit(textTime, (915, 35))

    # Update Display
    pygame.display.update()

    # Set FPS
    clock.tick(fps)
