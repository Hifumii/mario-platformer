import pygame.sprite
from math import floor
from code.constants import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.width = TILE_SIZE

        # Chargement de l'image
        self.resize_factor = TILE_SIZE / image.get_width()
        self.image = pygame.transform.scale_by(image, self.resize_factor)

        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE


class AnimatedTile(Tile):
    def __init__(self, x, y, image, path):
        super().__init__(x, y, image)

        self.path = path
        self.tile_width = 16
        self.resize_factor = TILE_SIZE / self.tile_width

        self.frame_index = 0
        self.animation_speed = .1
        self.animation_sprites = list()
        self.load_sprites()

    def load_sprites(self):

        sprite_sheet = pygame.image.load(self.path).convert_alpha()
        nb_sprites = int(sprite_sheet.get_width() / self.tile_width)
        sprite_sheet = pygame.transform.scale_by(sprite_sheet, (
            self.resize_factor))

        for x in range(nb_sprites):
            surface = pygame.Surface((self.width, self.width), pygame.SRCALPHA).convert_alpha()
            surface.set_colorkey((0, 0, 0))
            surface.blit(sprite_sheet, (0, 0),
                         (x * TILE_SIZE, 0, TILE_SIZE,
                          TILE_SIZE))

            self.animation_sprites.append(surface)

    def animate(self):
        # Fonction qui gère l'image du joueur à afficher selon l'état du joueur et la progression de l'animation

        # boucle d'animation (index de progression de l'animation)
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animation_sprites):
            self.frame_index = 0

        # récupération de l'image de l'animation
        self.image = self.animation_sprites[floor(self.frame_index)]

    def update(self):
        self.animate()
