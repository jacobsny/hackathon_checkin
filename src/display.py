from PIL import Image
import pygame.camera
from pygame.locals import *
from src import main
import time


pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera('/dev/video0', (1280, 720))
cam.start()
image = cam.get_image()
pil_string_image = pygame.image.tostring(image, "RGB")
im = Image.frombytes("RGB", (1280, 720), pil_string_image)
im.save("image.png", "PNG")
print(main.detect_faces())

