# 67‑FlappyBird — Gesture‑Controlled Flappy Bird (Python + Mediapipe)
This is a modified version of flappy bird that can be controlled using the 67 gesture. It is built with pygame, mediapipe and opencv.

In this version of flappy bird, players have the choice to use real-time hands tracking and perform the "67 movement" to flap the bird instead of using the space bar.

It doesn't work the best with the hand detection, but the concept is there though.

# How it works
Mediapipe detects the location of your wrists and sends back info on how much it moved. Depending on the amount it moved from the previous location, it tells the bird to flap or not flap.

# How to play the game
1. Download the release here: https://github.com/laisammy/67-FlappyBird/releases/tag/v1.0 (It takes a while to download)
2. Unzip dist.zip
3. Run game.exe

# Requirements
- Python 3.13.7
- Pygame
- Mediapipe tasks
- OpenCV

# Why?
I was on my bed about to fall asleep when I had this amazing idea (literal eureka moment) and I thought it was a great opportunity for me to pick up pygame and computer vision

# Note
This project is for educational and portfolio use.
Sprites and sounds are adapted from open Flappy Bird resources.
