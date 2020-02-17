import pygame
import os
import random
import sys


AVAILABLE_SPAWNS = {1, 2, 3, 4}


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert()
    return image


class Car(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        global AVAILABLE_SPAWNS
        self.image = load_image('car1.png', -1)
        self.rect = self.image.get_rect()
        self.row = 0
        self.row = random.choice(list(AVAILABLE_SPAWNS))
        AVAILABLE_SPAWNS.remove(self.row)
        self.rect.y = self.y = 0 - self.rect.height
        self.on_cooldown = True
        if self.row == 1:
            self.x = self.rect.x = 95
            self.speed = 100
            self.spawn_cooldown = 2
        elif self.row == 2:
            self.x = self.rect.x = 185
            self.speed = 100
            self.spawn_cooldown = 2
        elif self.row == 3:
            self.x = self.rect.x = 290
            self.speed = 250
            self.image = pygame.transform.flip(self.image, 0, 1)
            self.spawn_cooldown = 1
        elif self.row == 4:
            self.x = self.rect.x = 380
            self.speed = 250
            self.image = pygame.transform.flip(self.image, 0, 1)
            self.spawn_cooldown = 1

    def update(self, dt):
        global AVAILABLE_SPAWNS
        if self.spawn_cooldown >= 0:
            if self.spawn_cooldown - dt <= 0 and self.on_cooldown:
                AVAILABLE_SPAWNS.add(self.row)
                self.on_cooldown = False
            else:
                self.spawn_cooldown -= dt
        self.y += self.speed * dt
        self.rect.y = int(self.y)


class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image('player.png', -1), (64, 96))
        self.rect = self.image.get_rect()
        self.rect.x = 90
        self.rect.y = 380
        self.x = 90
        self.y = 380
        self.pressed_keys = set()
        self.outofroad_timeout = 5

    def update(self, dt):
        self.rect.y = int(self.y)
        self.rect.x = int(self.x)
        for key in self.pressed_keys:
            if key == pygame.K_w and self.y > 10:
                self.y -= 10
            elif key == pygame.K_s and self.y + self.rect.height < 470:
                self.y += 10
            elif key == pygame.K_a and self.x > 40:
                self.x -= 10
            elif key == pygame.K_d and self.x + self.rect.width < 500:
                self.x += 10
        if self.x < 50 or self.x > 436:
            self.outofroad_timeout -= dt
        else:
            self.outofroad_timeout = 5


def main():
    width, height = 540, 480
    pygame.init()
    pygame.font.init()
    FONT = pygame.font.SysFont('Calibri MS', 30)
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    FPS = 30
    SCORE = 0
    background_y = -480
    stopped = False
    all_sprites = pygame.sprite.Group()
    player = Player(all_sprites)
    background_image = load_image('background_long.png')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d) and not stopped:
                    player.pressed_keys.add(event.key)
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    return int(SCORE)
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d):
                    if event.key in player.pressed_keys:
                        player.pressed_keys.remove(event.key)
        screen.blit(background_image, (0, background_y))
        if not stopped:
            background_y += 5
            if background_y == 0:
                background_y = -480
            all_sprites.update(1 / FPS)
            for sprite in all_sprites:
                if 480 <= sprite.y or 0 >= sprite.y + sprite.rect.height:
                    all_sprites.remove(sprite)
            if random.randint(0, len(all_sprites) * 10) == 0 and AVAILABLE_SPAWNS:
                Car(all_sprites)
        all_sprites.draw(screen)
        if player.outofroad_timeout == 5:
            if not stopped:
                SCORE += 10 / FPS
            for sprite in all_sprites:
                if sprite == player:
                    continue
                for x, y in ((player.x + 10, player.y + 10),
                             (player.x + 10, player.y + player.rect.height - 10), (player.x + player.rect.width - 10, player.y + 10),
                             (player.x + player.rect.width - 10, player.y + player.rect.height - 10)):
                    if sprite.x < x < sprite.x + sprite.rect.width and \
                       sprite.y < y < sprite.y + sprite.rect.height:
                        stopped = True
        else:
            if player.outofroad_timeout <= 0:
                stopped = True
            elif not stopped:
                screen.blit(FONT.render('RETURN ON ROAD IN ' + str(int(player.outofroad_timeout)), False, (255, 0, 0)), (160, 232))
        if stopped:
            screen.blit(FONT.render('YOU LOST, PRESS ESC', False, (255, 0, 0)), (160, 232))
        screen.blit(FONT.render('SCORE: ' + str(int(SCORE)), False, (255, 255, 255)), (0, 0))
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
