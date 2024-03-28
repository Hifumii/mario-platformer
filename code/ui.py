import os

import pygame

from code.constants import *


class LevelUI:
    # Classe qui gère l'interface utilisateur dans les niveaux

    def __init__(self, display_surface):
        self.display_surface = display_surface

        # health asset
        heart_path = 'assets/ui/heart.png'
        self.heart_image = pygame.image.load(os.path.join(heart_path))
        self.heart_image = pygame.transform.scale_by(self.heart_image, TILE_SIZE / self.heart_image.get_width())

        # coin asset
        coin_path = 'assets/ui/coin_icon.png'
        self.coin_image = pygame.image.load(os.path.join(coin_path))
        self.coin_image = pygame.transform.scale_by(self.coin_image, TILE_SIZE / self.coin_image.get_width())

        # police de caractère et taille du compteur de pièce
        font_path = 'assets/ui/Retro Gaming.ttf'
        self.font = pygame.font.Font(os.path.join(font_path), 30)

        self.enemy_path = "assets/ui/enemy.png"
        self.enemy_image = pygame.image.load(self.enemy_path)
        self.enemy_image = pygame.transform.scale_by(self.enemy_image, TILE_SIZE / self.enemy_image.get_width())

        self.bee_path = "assets/ui/bee.png"
        self.bee_image = pygame.image.load(self.bee_path)
        self.bee_image = pygame.transform.scale_by(self.bee_image, TILE_SIZE / self.bee_image.get_width())

        self.isib_path = "assets/animations/ISIB_Logo2.png"
        self.isib_image = pygame.image.load(self.isib_path)
        self.isib_image = pygame.transform.scale_by(self.isib_image, TILE_SIZE / self.isib_image.get_width())

    def draw_health(self, current_health):
        # Affiche le compteur de vies

        for x in range(current_health):
            self.display_surface.blit(self.heart_image, (10 + x * (self.heart_image.get_width() + 5), 10))

    def draw_coins_counter(self, nb_coin):
        # Affiche le compteur de pièces du niveau

        self.display_surface.blit(self.coin_image, (5, 10 + TILE_SIZE))

        text = '× ' + str(nb_coin)
        text_surface = self.font.render(text, False, (255, 196, 56))
        self.display_surface.blit(text_surface, (TILE_SIZE, TILE_SIZE + 15))

    def draw_enemy_count(self, nb_goomba, nb_bee, nb_isib):
        self.draw_goomba_count(nb_goomba)
        self.draw_bee_count(nb_bee)
        # self.draw_isib_count(nb_isib)

    def draw_goomba_count(self, nb_enemy):
        self.display_surface.blit(self.enemy_image, (5, 10 + 2 * TILE_SIZE))

        text = '× ' + str(nb_enemy)
        text_surface = self.font.render(text, False, (23, 25, 27))
        self.display_surface.blit(text_surface, (TILE_SIZE + 10, 2 * TILE_SIZE + 20))

    def draw_bee_count(self, nb_enemy):
        self.display_surface.blit(self.bee_image, (5, 10 + 3 * TILE_SIZE))

        text = '× ' + str(nb_enemy)
        text_surface = self.font.render(text, False, (23, 25, 27))
        self.display_surface.blit(text_surface, (TILE_SIZE + 10, 3 * TILE_SIZE + 20))

    def draw_isib_count(self, nb_enemy):
        self.display_surface.blit(self.isib_image, (5, 10 + 4 * TILE_SIZE))

        text = '× ' + str(nb_enemy)
        text_surface = self.font.render(text, False, (23, 25, 27))
        self.display_surface.blit(text_surface, (TILE_SIZE + 10, 4 * TILE_SIZE + 20))

    def draw(self, nb_coins, nb_goomba, nb_bee, nb_isib, health):
        self.draw_enemy_count(nb_goomba, nb_bee, nb_isib)
        self.draw_health(health)
        self.draw_coins_counter(nb_coins)


class Button:

    def __init__(self, x, y, text, width=150, height=150, click=None):

        self.x = x
        self.y = y

        font_path = 'assets/ui/Retro Gaming.ttf'

        self.click = click

        self.text = text
        self.font = pygame.font.Font(os.path.join(font_path), 50)

        self.color = (105, 222, 222)
        self.outline_color = (0, 0, 0)

        self.width = width
        self.height = height

        self.rect = pygame.Rect((x, y), (self.width, self.height))
        self.outline_rect = pygame.Rect(x - 2, y - 2, self.rect.width + 4, self.rect.height + 4)

        self.text_image = self.font.render(self.text, False, (0, 0, 0))
        self.text_rect = self.text_image.get_rect(center=self.rect.center)

    def draw(self, screen):

        # contours du bouton
        pygame.draw.rect(screen, self.outline_color, self.outline_rect, 0)

        # bouton
        pygame.draw.rect(screen, self.color, self.rect)

        # texte du bouton
        screen.blit(self.text_image, self.text_rect)

    def on_mouse_clicked(self, event):
        # Fonction qui renvoie Vrai si le click est sur le bouton

        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.rect.collidepoint(event.pos)

    def on_mouse_motion(self, event):
        # Fonction qui change la couleur du bouton si on passe la souris par-dessus

        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.color = (255, 255, 255)
            else:
                self.color = (105, 222, 222)

    def select(self):
        # Change la couleur du bouton si on le sélectionne

        self.color = (255, 255, 255)

    def unselect(self):
        # Remet la couleur de base du bouton si on le désélectionne

        self.color = (105, 222, 222)
