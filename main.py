import pygame
import os
import random


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Car(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.image = load_image(random.choice(('car1.png', 'car2.png', 'car3.png')))

    def update(self, dt):
        self.y += 10 * dt / 1000


class Player(Car):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image('player.png')


width, height = 480, 540
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False