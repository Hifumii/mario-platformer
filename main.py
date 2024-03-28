import pygame
import os
import sys
from code.game import Game
from code.constants import *

# Initialisation de pygame
pygame.init()

#   Création de la fenêtre du jeu
pygame.display.set_caption('Platformer')  # titre de la fenêtre
win_icon = pygame.image.load(os.path.join(WIN_ICON_PATH))  # icone de la fenêtre
pygame.display.set_icon(win_icon)
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),
                                          pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED, vsync=1)

# gestion de la vitesse de l'actualisation de l'écran
clock = pygame.time.Clock()

# on crée un dictionnaire qui va stocker les manettes connectées
joysticks = {}

game = Game()

# Boucle principale du jeu
running = True
while running:
    # on limite le jeu à un certain nombre d'images par secondes
    dt = clock.tick(FPS) / 1000

    # récupération des actions grace aux "events" de pygame
    events = pygame.event.get()
    for event in events:

        # fermeture de la fenêtre
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Gérer la connexion d'une manette pendant que le jeu tourne
        elif event.type == pygame.JOYDEVICEADDED:
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks[joy.get_instance_id()] = joy

        # Gérer la déconnexion d'une manette en jeu
        elif event.type == pygame.JOYDEVICEREMOVED:
            del joysticks[event.instance_id]

    # Fonction principale du jeu
    game.run(events, joysticks, dt)


# fermeture de pygame lorsqu'on quitte le jeu
pygame.quit()
sys.exit()
