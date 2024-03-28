import pygame
from code.ui import Button
from code.constants import *
import os


class Gameover:

    def __init__(self, create_level, show_menu):

        self.display_surface = pygame.display.get_surface()
        self.current_level = 1

        self.create_level = create_level
        self.show_menu = show_menu

        self.input_cooldown = 300
        self.last_input = self.input_cooldown

        # Titre :
        font_path = 'assets/ui/Retro Gaming.ttf'
        self.font = pygame.font.Font(os.path.join(font_path), 50)
        self.title_image = None
        self.title_rect = None

        self.buttons = []
        self.button_selected = 0

    def get_inputs(self, events, joysticks):
        # Fonction qui gère les actions du joueur

        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Cliquer sur le bouton

                for button in self.buttons:
                    if button.on_mouse_clicked(event):
                        button.click(self.current_level)

            elif event.type == pygame.MOUSEMOTION:
                # Changer la couleur du bouton si l'on passe la souris par-dessus

                for button in self.buttons:
                    button.on_mouse_motion(event)

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    # Changer de bouton sélectionné avec le clavier (vers le bas)

                    self.buttons[self.button_selected].unselect()
                    self.button_selected += 1
                    if self.button_selected > len(self.buttons) - 1:
                        self.button_selected = 0
                    self.buttons[self.button_selected].select()

                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    # Changer de bouton sélectionné avec le clavier (vers le haut)

                    self.buttons[self.button_selected].unselect()
                    self.button_selected -= 1
                    if self.button_selected < 0:
                        self.button_selected = len(self.buttons) - 1
                    self.buttons[self.button_selected].select()

                elif event.key == pygame.K_SPACE:
                    # Cliquer sur le bouton si l'on appuie sur espace

                    self.buttons[self.button_selected].click(self.current_level)

            elif event.type == pygame.JOYBUTTONDOWN:

                if event.button == 0:
                    # Cliquer sur le bouton si l'on appuie sur le premier bouton de la manette

                    self.buttons[self.button_selected].click(self.current_level)

        # puis les actions de la manette
        for joystick in joysticks.values():

            # le joystick
            if joystick.get_axis(1) > DEADZONE_SENS:
                # Changer de bouton sélectionné avec le joystick (vers le bas)

                now = pygame.time.get_ticks()
                if now - self.last_input > self.input_cooldown:
                    self.buttons[self.button_selected].unselect()
                    self.button_selected += 1
                    if self.button_selected > len(self.buttons) - 1:
                        self.button_selected = 0
                    self.buttons[self.button_selected].select()

                    self.last_input = pygame.time.get_ticks()

            elif joystick.get_axis(1) < -DEADZONE_SENS:
                # Changer de bouton sélectionné avec le joystick (vers le haut)

                now = pygame.time.get_ticks()
                if now - self.last_input > self.input_cooldown:

                    self.buttons[self.button_selected].unselect()
                    self.button_selected -= 1
                    if self.button_selected < 0:
                        self.button_selected = len(self.buttons) - 1
                    self.buttons[self.button_selected].select()

                    self.last_input = pygame.time.get_ticks()

            else:
                self.last_input = 300

    def run(self, events, joysticks):

        # On récupère les actions du joueur
        self.get_inputs(events, joysticks)

        # Titre:
        self.display_surface.blit(self.title_image, self.title_rect)

        # Boutons
        for button in self.buttons:
            button.draw(self.display_surface)

        # Actualisation de la fenêtre
        pygame.display.flip()


class DefeatScreen(Gameover):

    def __init__(self, create_level, show_menu):
        super().__init__(create_level, show_menu)

        self.title = 'Game Over'
        red = (255, 0, 0)
        self.title_image = self.font.render(self.title, False, red)
        self.title_rect = self.title_image.get_rect(centerx=WINDOW_WIDTH / 2, y=50)

        # Restart Button
        button_width = 450
        button_height = 100
        button_x = (WINDOW_WIDTH - button_width) / 2
        button_y = WINDOW_HEIGHT / 2 - button_height
        self.restart_btn = Button(button_x, button_y, text='Restart', width=button_width, height=button_height,
                                  click=self.create_level)

        # Return to menu Button
        button_width = 450
        button_height = 100
        button_x = (WINDOW_WIDTH - button_width) / 2
        button_y = WINDOW_HEIGHT / 2 + button_height / 2
        self.menu_btn = Button(button_x, button_y, text='Back to menu', width=button_width, height=button_height,
                               click=self.show_menu)

        self.buttons = [self.restart_btn, self.menu_btn]
        self.button_selected = 0
        self.restart_btn.select()


class VictoryScreen(Gameover):

    def __init__(self, create_level, show_menu, next_level):
        super().__init__(create_level, show_menu)

        self.next_level = next_level

        self.title = 'You win!'
        green = (0, 255, 0)
        self.title_image = self.font.render(self.title, False, green)
        self.title_rect = self.title_image.get_rect(centerx=WINDOW_WIDTH / 2, y=50)

        # Next level Button
        button_width = 450
        button_height = 100
        button_x = (WINDOW_WIDTH - button_width) / 2
        button_y = WINDOW_HEIGHT / 2 - 2 * button_height
        self.next_level_btn = Button(button_x, button_y, text='Next level', width=button_width, height=button_height,
                                     click=self.next_level)

        # Restart Button
        button_width = 450
        button_height = 100
        button_x = (WINDOW_WIDTH - button_width) / 2
        button_y = (WINDOW_HEIGHT - button_height) / 2
        self.restart_btn = Button(button_x, button_y, text='Restart', width=button_width, height=button_height,
                                  click=self.create_level)

        # Return to menu Button
        button_width = 450
        button_height = 100
        button_x = (WINDOW_WIDTH - button_width) / 2
        button_y = WINDOW_HEIGHT / 2 + button_height
        self.menu_btn = Button(button_x, button_y, text='Back to menu', width=button_width, height=button_height,
                               click=self.show_menu)

        self.buttons = [self.next_level_btn, self.restart_btn, self.menu_btn]
        self.button_selected = 0
        self.restart_btn.select()
