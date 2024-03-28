from math import floor, sin

import pygame

from code.constants import *
from code.tile import Tile


class Enemy(Tile):

    def __init__(self, x, y, image):
        super().__init__(x, y, image)

        self.speed = 3
        self.horizontal_movement = self.speed

        self.facing_right = True
        self.status = 'idle'
        self.animation_sprites = {'idle': [], 'run': [], 'hurt': []}
        self.frame_index = 0
        self.animation_speed = 0.15

        # SFX
        self.explosion_sfx = pygame.mixer.Sound('assets/sounds/Explosion.wav')
        self.explosion_sfx.set_volume(SFX_VOLUME)

    def animate(self):
        # Fonction qui gère l'image du joueur à afficher selon l'état du joueur et la progression de l'animation

        # état de l'ennemi :
        current_animation = self.animation_sprites[self.status]

        # boucle d'animation (index de progression de l'animation)
        self.frame_index += self.animation_speed
        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.status == 'hurt':
                self.kill()

        # récupération de l'image de l'animation
        image = current_animation[floor(self.frame_index)]

        # Inversion de l'image selon la direction dans laquelle regarde le joueur
        if not self.facing_right:
            image = pygame.transform.flip(image, True, False).convert_alpha()

        self.image = image

    def get_status(self):
        # Fonction qui change l'état du joueur pour les animations (immobile, en train de courir, de sauter...)
        if self.status != 'hurt':
            if self.horizontal_movement == 0:
                self.status = 'idle'
            elif self.horizontal_movement > 0:
                self.status = 'run'
                self.facing_right = True
            elif self.horizontal_movement < 0:
                self.status = 'run'
                self.facing_right = False

    def move(self):
        self.rect.x += self.horizontal_movement

    def die(self):
        self.horizontal_movement = 0
        self.status = 'hurt'
        self.explosion_sfx.play()
        self.frame_index = 2

    def update(self):
        self.get_status()
        self.move()
        self.animate()


class Goomba(Enemy):

    def __init__(self, x, y, image):
        super().__init__(x, y, image)

        self.status = 'idle'
        self.animation_sprites = {'idle': [], 'run': [], 'hurt': []}
        self.frame_index = 0
        self.animation_speed = 0.15
        self.load_sprites()
        self.image = self.animation_sprites[self.status][0]

    def load_sprites(self):

        sprite_sheet_path = 'assets/animations/enemy.png'
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        sprite_sheet = pygame.transform.scale_by(sprite_sheet, (
            self.resize_factor))

        for key in self.animation_sprites:

            # On récupère les coordonnées sur la sprite sheet de chaque type d'animation
            if key == 'idle':
                y = 0
                nb_sprite = 8
            elif key == 'run':
                y = 16
                nb_sprite = 6
            elif key == 'hurt':
                y = 32
                nb_sprite = 4

            for i in range(nb_sprite):
                surface = pygame.Surface((self.width, self.width)).convert_alpha()
                surface.set_colorkey((0, 0, 0))
                surface.blit(sprite_sheet, (0, 0),
                             (i * 16 * self.resize_factor, y * self.resize_factor, 16 * self.resize_factor,
                              28 * self.resize_factor))

                self.animation_sprites[key].append(surface)


class Isib(Enemy):

    def __init__(self, x, y):
        image_path = 'assets/animations/ISIB_Logo2.png'
        image = pygame.image.load(image_path).convert_alpha()
        image = pygame.transform.scale_by(image, TILE_SIZE * 3 / image.get_height())

        super().__init__(x, y, image)

        self._y = y * TILE_SIZE
        self.image = image
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()

    def update(self):
        self.rect.y = self.oscillate(pygame.time.get_ticks() / 200)

    def oscillate(self, t):
        return self._y + sin(t) * 20

    def die(self):
        self.explosion_sfx.play()
        self.kill()

    def draw(self, win):
        win.blit(self.image, self.rect)


class Bee(Enemy):

    def __init__(self, x, y, image):
        super().__init__(x, y, image)

        self.speed = 1
        self.horizontal_movement = self.speed

        self._y = y * TILE_SIZE
        self.status = 'run'
        self.animation_sprites = {'run': [], 'hurt': []}
        self.frame_index = 0
        self.animation_speed = 0.15
        self.load_sprites()
        self.image = self.animation_sprites[self.status][0]

    def load_sprites(self):

        sprite_sheet_path = 'assets/animations/bee.png'
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        sprite_sheet = pygame.transform.scale_by(sprite_sheet, (
            self.resize_factor))

        for key in self.animation_sprites:

            # On récupère les coordonnées sur la sprite sheet de chaque type d'animation
            if key == 'run':
                y = 0
                nb_sprite = 4
            elif key == 'hurt':
                y = 16
                nb_sprite = 3

            for i in range(nb_sprite):
                surface = pygame.Surface((self.width, self.width)).convert_alpha()
                surface.set_colorkey((0, 0, 0))
                surface.blit(sprite_sheet, (0, 0),
                             (i * 16 * self.resize_factor, y * self.resize_factor, 16 * self.resize_factor,
                              28 * self.resize_factor))

                self.animation_sprites[key].append(surface)
