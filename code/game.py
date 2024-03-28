import pygame
from code.menu import Menu
from code.level import Level
from code.gameover import VictoryScreen, DefeatScreen
from code.constants import *
from code.data_loader import update_player_data, get_player_data


class Game:

    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        # Attributs principaux du jeu :
        self.game_state = 'menu'
        self.data_path = 'data/data.json'
        data = get_player_data(self.data_path)
        self.max_level = len(data)

        # Musique :
        self.level_music = pygame.mixer.Sound('assets/sounds/level_music.wav')
        self.level_music.set_volume(MUSIC_VOLUME)

        self.menu_music = pygame.mixer.Sound('assets/sounds/menu_music.wav')
        self.menu_music.set_volume(MUSIC_VOLUME)

        win_volume = 4 * MUSIC_VOLUME
        self.win_music = pygame.mixer.Sound('assets/sounds/victory_music.mp3')
        self.win_music.set_volume(win_volume)

        death_volume = 4 * MUSIC_VOLUME
        self.death_music = pygame.mixer.Sound('assets/sounds/death_music.mp3')
        self.death_music.set_volume(death_volume)

        # Menu setup
        self.menu = Menu(self.max_level, 1, self.create_level, data)
        self.menu_music.play(loops=-1)

        self.level = None

        # Gameover
        self.win_screen = VictoryScreen(self.create_level, self.show_menu, self.next_level)
        self.lose_screen = DefeatScreen(self.create_level, self.show_menu)

    def next_level(self, current_level):
        # Passage au niveau suivant

        if current_level < self.max_level:
            self.menu.current_level = current_level + 1
            self.win_screen.current_level = current_level + 1
            self.lose_screen.current_level = current_level + 1
            self.create_level(current_level + 1)

    def create_level(self, current_level):
        # Création du niveau lorsque le joueur le lance

        self.death_music.stop()
        self.win_music.stop()
        self.menu_music.stop()
        self.level_music.play(loops=-1)

        self.level = Level(current_level, self.show_menu, self.show_gameover)
        self.game_state = 'level'

    def show_gameover(self, current_level, win=False, nb_coin=0):

        black_filter = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        black_filter.fill((0, 0, 0))
        black_filter.set_alpha(200)

        self.display_surface.blit(black_filter, (0, 0))

        pygame.display.flip()

        self.menu_music.stop()
        self.level_music.stop()

        if win:
            self.game_state = 'win'
            self.win_music.play()
            if update_player_data(self.data_path, current_level, nb_coin):
                self.menu.update_nb_coins(current_level, nb_coin)
            for button in self.win_screen.buttons:
                button.unselect()
            self.win_screen.buttons[0].select()
            self.win_screen.button_selected = 0
            self.win_screen.current_level = current_level
        else:
            self.game_state = 'lose'
            self.death_music.play()
            for button in self.lose_screen.buttons:
                button.unselect()
            self.lose_screen.buttons[0].select()
            self.lose_screen.button_selected = 0
            self.lose_screen.current_level = current_level

    def show_menu(self, current_level):

        self.death_music.stop()
        self.win_music.stop()
        self.menu.max_level = self.max_level
        self.menu.current_level = current_level
        for button in self.menu.buttons:
            button.unselect()
        self.menu.buttons[current_level - 1].select()
        self.level_music.stop()
        self.menu_music.play(loops=-1)
        self.game_state = 'menu'

    def run(self, events, joysticks, dt):
        # Fonction appelée à chaque tour de boucle, renvoie aux fonctions principales du menu ou du niveau

        if self.game_state == 'menu':
            self.menu.run(events, joysticks)
        elif self.game_state == 'level':
            self.level.run(joysticks, dt)
        elif self.game_state == 'win':
            self.win_screen.run(events, joysticks)
        elif self.game_state == 'lose':
            self.lose_screen.run(events, joysticks)
