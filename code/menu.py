import pygame
import os
from code.ui import Button
from code.constants import *


class Menu:
    # Classe qui gère le fonctionnement du jeu dans le menu principal

    def __init__(self, max_level, current_level, create_level, data):

        self.display_surface = pygame.display.get_surface()

        self.input_cooldown = 300
        self.last_input = 301

        self.max_level = max_level
        self.current_level = current_level
        self.create_level = create_level

        # Arrière-plan:
        background_path = 'assets/ui/background.png'
        self.background = pygame.image.load(os.path.join(background_path))
        self.background = pygame.transform.scale_by(self.background, 1200 / 1056)
        self.background.set_alpha(100)

        # coin asset
        font_path = 'assets/ui/Retro Gaming.ttf'
        self.coin_font = pygame.font.Font(os.path.join(font_path), 25)
        coin_path = 'assets/ui/coin_icon.png'
        self.coin_image = pygame.image.load(os.path.join(coin_path))
        self.coin_image = pygame.transform.scale_by(self.coin_image, TILE_SIZE / self.coin_image.get_width())

        # Titre:
        font_path = 'assets/ui/Retro Gaming.ttf'
        self.font = pygame.font.Font(os.path.join(font_path), 50)
        title = 'Select a level:'
        self.title_image = self.font.render(title, False, (0, 0, 0))
        self.title_rect = self.title_image.get_rect(centerx=WINDOW_WIDTH / 2, y=50)

        self.data = data

        # Boutons des niveaux
        self.buttons = []
        self.coins_info = []
        for index, level_data in enumerate(data.values()):
            button = Button(100 + index * 200, 200, text=str(index + 1))
            self.buttons.append(button)

            # Compteur de pièce :
            coin_surface = self.create_coin_ui(level_data[0], level_data[1])
            self.coins_info.append(coin_surface)

        self.buttons[self.current_level - 1].select()

    def update_nb_coins(self, level, new_value):
        key = 'level' + str(level)
        total_coin = self.data[key][1]
        new_coin_surface = self.create_coin_ui(new_value, total_coin)
        self.coins_info[level - 1] = new_coin_surface

    def create_coin_ui(self, nb_coin, total_coin):
        # Affiche le compteur de pièces du niveau

        text = str(nb_coin) + '/' + str(total_coin)
        black = (0, 0, 0)
        text_surface = self.coin_font.render(text, False, black)

        width = text_surface.get_width() + self.coin_image.get_width()
        height = self.coin_image.get_height()

        surface = pygame.Surface((width, height)).convert()
        surface.fill((255, 255, 255))
        surface.set_colorkey((255, 255, 255))
        surface.set_alpha(200)

        surface.blit(self.coin_image, (0, 0))

        text_pos_y = (height - text_surface.get_height()) / 2
        surface.blit(text_surface, (self.coin_image.get_width() - 5, text_pos_y))

        return surface

    def get_inputs(self, events, joysticks):
        # Fonction qui gère les actions du joueur

        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Lancer le niveau si l'on clique sur un bouton

                for button in self.buttons:
                    if button.on_mouse_clicked(event):
                        self.create_level(int(button.text))

            elif event.type == pygame.MOUSEMOTION:
                # Changer la couleur du bouton si l'on passe la souris par-dessus

                for button in self.buttons:
                    button.on_mouse_motion(event)

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RIGHT or event.key == pygame.K_a:
                    # Changer de niveau sélectionné avec le clavier (vers la droite)

                    self.buttons[self.current_level - 1].unselect()
                    self.current_level += 1
                    if self.current_level > self.max_level:
                        self.current_level = 1
                    self.buttons[self.current_level - 1].select()

                elif event.key == pygame.K_LEFT or event.key == pygame.K_d:
                    # Changer de niveau sélectionné avec le clavier (vers la gauche)

                    self.buttons[self.current_level - 1].unselect()
                    self.current_level -= 1
                    if self.current_level < 1:
                        self.current_level = self.max_level
                    self.buttons[self.current_level - 1].select()

                elif event.key == pygame.K_SPACE:
                    # Lancer le niveau sélectionné si l'on appuie sur espace

                    self.create_level(self.current_level)

            elif event.type == pygame.JOYBUTTONDOWN:

                if event.button == 0:
                    # Lancer le niveau sélectionné si l'on appuie sur le premier bouton de la manette

                    self.create_level(self.current_level)

        # puis les actions de la manette
        for joystick in joysticks.values():

            # le joystick
            if joystick.get_axis(0) > DEADZONE_SENS:
                # Changer de niveau sélectionné avec le joystick (vers la droite)

                now = pygame.time.get_ticks()
                if now - self.last_input > self.input_cooldown:
                    self.buttons[self.current_level - 1].unselect()
                    self.current_level += 1
                    if self.current_level > self.max_level:
                        self.current_level = 1
                    self.buttons[self.current_level - 1].select()

                    self.last_input = pygame.time.get_ticks()

            elif joystick.get_axis(0) < -DEADZONE_SENS:
                # Changer de niveau sélectionné avec le joystick (vers la gauche)

                now = pygame.time.get_ticks()
                if now - self.last_input > self.input_cooldown:

                    self.buttons[self.current_level - 1].unselect()
                    self.current_level -= 1
                    if self.current_level < 1:
                        self.current_level = self.max_level
                    self.buttons[self.current_level - 1].select()

                    self.last_input = pygame.time.get_ticks()

            else:
                self.last_input = 300

    def run(self, events, joysticks):

        # On récupère les actions du joueur
        self.get_inputs(events, joysticks)

        # Arrière-plan
        blue = (51, 165, 255)
        self.display_surface.fill(blue)
        self.display_surface.blit(self.background, (0, 0))

        # Titre
        self.display_surface.blit(self.title_image, self.title_rect)

        # Boutons des niveaux
        for index, button in enumerate(self.buttons):
            button.draw(self.display_surface)

            coin_surface = self.coins_info[index]
            pos = (button.x, button.y)
            self.display_surface.blit(coin_surface, pos)

        # Actualisation de la fenêtre
        pygame.display.flip()
