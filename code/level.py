import os

import pygame
from pytmx.util_pygame import load_pygame

from code.constants import *
from code.enemy import Goomba, Isib, Bee
from code.player import Player
from code.tile import Tile, AnimatedTile
from code.ui import LevelUI


class Level:
    # Classe qui gère le jeu lorsque le joueur est dans un niveau

    def __init__(self, current_level, show_menu, show_gameover):
        self.display_surface = pygame.display.get_surface()
        self.current_level = current_level
        self.show_menu = show_menu
        self.show_gameover = show_gameover

        # Interface utilisateur dans le niveau
        self.ui = LevelUI(self.display_surface)
        self.nb_coins = 0

        # Player setup
        self.player = Player()
        self.scroll = False
        self.nb_goomba = 0
        self.nb_bee = 0
        self.nb_isib = 0

        # Level setup
        self.sprite_groups = []
        self.setup_level()
        self.center_camera()

        # SFX
        coin_volume = 2 * SFX_VOLUME
        self.coin_sfx = pygame.mixer.Sound('assets/sounds/coin_2.mp3')
        self.coin_sfx.set_volume(coin_volume)

    def setup_level(self):
        # Fonction qui importe la carte du jeu

        # Importation du fichier tmx
        path = 'assets/levels/level' + str(self.current_level) + '.tmx'  # on récupère le fichier du niveau actuel
        level_data = load_pygame(os.path.join(path))

        # Terrain :
        layer = level_data.get_layer_by_name('Terrain')
        self.terrain = self.create_sprite_group(layer)
        self.sprite_groups.append(self.terrain)

        # Decoration :
        layer = level_data.get_layer_by_name('Decoration')
        self.decoration = self.create_sprite_group(layer)
        self.sprite_groups.append(self.decoration)

        # Background :
        layer = level_data.get_layer_by_name('Background')
        self.background = self.create_sprite_group(layer)
        self.sprite_groups.append(self.background)

        # Player
        layer = level_data.get_layer_by_name('Spawn')
        for x, y, surface in layer.tiles():
            player_spawn_x = x * TILE_SIZE
            player_spawn_y = (y + 1) * TILE_SIZE
            self.player.rect.bottomleft = (player_spawn_x, player_spawn_y)

        # Enemies
        layer = level_data.get_layer_by_name('Enemies')
        self.enemies = pygame.sprite.Group()

        for x, y, surface in layer.tiles():
            tile = Goomba(x, y, surface)  # création d'un nouvel objet "Tile" grace à sa position et son image
            self.enemies.add(tile)  # on ajoute ce carreau au groupe

        # Isib ennemi
        layer = level_data.get_layer_by_name('Isib')
        for x, y, surface in layer.tiles():
            tile = Isib(x, y)  # création d'un nouvel objet "Tile" grace à sa position et son image
            # self.enemies.add(tile)  # on ajoute ce carreau au groupe

        # Bees ennemi
        layer = level_data.get_layer_by_name('Bees')
        for x, y, surface in layer.tiles():
            tile = Bee(x, y, surface)  # création d'un nouvel objet "Tile" grace à sa position et son image
            self.enemies.add(tile)  # on ajoute ce carreau au groupe

        self.sprite_groups.append(self.enemies)

        # Enemy boundaries :
        layer = level_data.get_layer_by_name('EnemyBoundaries')
        self.enemy_boundaries = self.create_sprite_group(layer)
        self.sprite_groups.append(self.enemy_boundaries)

        # Pièces :
        layer = level_data.get_layer_by_name('Coins')
        path = 'assets/animations/coin.png'
        self.coins = self.create_sprite_group(layer, 'animated', path)
        self.sprite_groups.append(self.coins)

        # Eau profonde :
        layer = level_data.get_layer_by_name('DeepWater')
        path = 'assets/animations/deep_water.png'
        self.deep_water = self.create_sprite_group(layer, 'animated', path)
        self.sprite_groups.append(self.deep_water)

        # Eau de surface :
        layer = level_data.get_layer_by_name('SurfaceWater')
        path = 'assets/animations/surface_water.png'
        self.surface_water = self.create_sprite_group(layer, 'animated', path)
        self.sprite_groups.append(self.surface_water)

        # Premier plan:
        layer = level_data.get_layer_by_name('Foreground')
        self.foreground = self.create_sprite_group(layer)
        self.sprite_groups.append(self.foreground)

        # Portes :
        layer = level_data.get_layer_by_name('Doors')
        self.doors = self.create_sprite_group(layer)
        self.sprite_groups.append(self.doors)

        # Finish :
        layer = level_data.get_layer_by_name('Finish')
        self.finish = self.create_sprite_group(layer)
        self.sprite_groups.append(self.finish)

    @staticmethod
    def create_sprite_group(layer, tile_type='static', path=''):

        sprite_group = pygame.sprite.Group()

        for x, y, surface in layer.tiles():
            if tile_type == 'static':
                tile = Tile(x, y, surface)  # création d'un nouvel objet "Tile" grace à sa position et son image
                sprite_group.add(tile)  # on ajoute ce carreau au groupe

            elif tile_type == 'animated':
                tile = AnimatedTile(x, y, surface, path)  # création d'une nouvelle tile animée
                sprite_group.add(tile)  # on ajoute ce carreau au groupe

        return sprite_group

    def horizontal_collision(self, dt):

        # Application du mouvement horizontal du joueur :
        if not self.scroll:  # Si la caméra a déplacé tous les sprites, pas besoin de déplacer le joueur
            x_offset = self.player.horizontal_movement * dt
            self.player.rect.x += x_offset

        collidable_groups = self.terrain
        collision = pygame.sprite.spritecollide(self.player, collidable_groups.sprites(), False)

        for tile in collision:

            # Collisions sur la droite du joueur
            if self.player.horizontal_movement > 0:
                self.player.rect.right = tile.rect.left

            # Collisions sur la gauche du joueur
            elif self.player.horizontal_movement < 0:
                self.player.rect.left = tile.rect.right

    def vertical_collision(self, dt):

        # Application du mouvement vertical du joueur :
        y_offset = self.player.vertical_movement * dt
        self.player.rect.y += y_offset

        collidable_groups = self.terrain
        collision = pygame.sprite.spritecollide(self.player, collidable_groups.sprites(), False)

        for tile in collision:

            # Collisions en dessous du joueur
            if self.player.vertical_movement > 0:
                self.player.rect.bottom = tile.rect.top
                self.player.vertical_movement = 0
                self.player.on_ground = True
            # Collisions au-dessus du joueur
            elif self.player.vertical_movement < 0:
                self.player.rect.top = tile.rect.bottom
                self.player.vertical_movement = 0

        if self.player.vertical_movement > 0:
            self.player.on_ground = False

    def check_coin_collision(self):
        # Fonction qui permet de récupérer les pièces lorsque le joueur les touche

        collision = pygame.sprite.spritecollide(self.player, self.coins.sprites(), False)

        if collision:
            for coin in collision:
                self.nb_coins += 1
                coin.kill()
                self.coin_sfx.play()

    def check_enemy_collision(self):
        # Fonction qui vérifie les collisions des ennemis avec leurs barrières et le joueur

        for enemy in self.enemies.sprites():

            #  Collision avec les barrières des ennemis pour déterminer à quel moment ils tournent
            collision = pygame.sprite.spritecollide(enemy, self.enemy_boundaries.sprites(), False)

            if collision:
                for tile in collision:

                    # Collisions sur la droite de l'ennemi
                    if enemy.horizontal_movement > 0:
                        enemy.rect.right = tile.rect.left
                        enemy.horizontal_movement = -enemy.speed
                    # Collisions sur la gauche de l'ennemi
                    elif enemy.horizontal_movement < 0:
                        enemy.rect.left = tile.rect.right
                        enemy.horizontal_movement = enemy.speed

            # Collision entre l'ennemi et le joueur
            collision = enemy.rect.colliderect(self.player.rect)

            if collision and enemy.status != 'hurt':  # Collision avec un ennemi en vie

                # Si le joueur saute sur l'ennemi
                if self.player.rect.bottom < enemy.rect.centery and self.player.vertical_movement > 0:
                    self.player.vertical_movement = - self.player.jump_power / 2
                    enemy.die()
                    if enemy.__class__.__name__ == 'Goomba':
                        self.nb_goomba += 1
                    elif enemy.__class__.__name__ == 'Bee':
                        self.nb_bee += 1
                    elif enemy.__class__.__name__ == 'Isib':
                        self.nb_isib += 1
                    else:
                        pass

                elif self.player.rect.bottom < enemy.rect.centery and self.player.vertical_movement < 0:
                    pass

                # Si le joueur est touché par l'ennemi et qu'il n'est pas invincible
                elif not self.player.invincible:
                    self.player.take_damage()
                    if self.player.current_lives <= 0:
                        self.show_gameover(self.current_level)

    def check_finish(self):

        finish_collision = pygame.sprite.spritecollide(self.player, self.finish, False)

        if finish_collision:
            self.show_gameover(self.current_level, win=True, nb_coin=self.nb_coins)

    def check_player_death(self):

        if self.player.rect.top > WINDOW_HEIGHT:
            self.show_gameover(self.current_level)

    def reset_player(self):
        # Reinitialise le niveau et le joueur

        self.nb_coins = 0
        self.player.current_lives = self.player.lives

        self.player.vertical_movement = 0
        self.player.horizontal_movement = 0
        self.player.rect.x = 0
        self.player.rect.y = 0

        self.player.on_ground = False
        self.player.facing_right = True
        self.player.invincible = False
        self.player.first_run = True

        self.sprite_groups = []
        self.setup_level()
        self.center_camera()

    def center_camera(self):
        # Place le joueur au centre de l'écran

        # on calcule le décalage entre le centre de l'écran et le joueur
        offset = round(WINDOW_WIDTH / 2 - self.player.rect.centerx)

        # on déplace le joueur
        self.player.rect.centerx += offset

        # on déplace tous les autres sprites
        for sprite_group in self.sprite_groups:
            for sprite in sprite_group:
                sprite.rect.x += offset

    def camera_scroll(self, dt):
        # Fonction qui déplace la camera horizontalement

        # Indicateur qui permet de ne pas déplacer le joueur si l'on déplace tous les autres objets
        self.scroll = False

        if self.player.rect.right > WINDOW_WIDTH / 2:  # Si le joueur est du côté droit de l'écran
            if self.player.horizontal_movement > 0:  # Si le joueur se déplace vers la droite

                # On déplace tous les sprites vers la gauche
                offset = self.player.horizontal_movement * dt
                for sprite_group in self.sprite_groups:
                    for sprite in sprite_group:
                        sprite.rect.x -= offset
                        self.scroll = True

        elif self.player.rect.left < WINDOW_WIDTH / 4:  # Si le joueur est du côté gauche de l'écran
            if self.player.horizontal_movement < 0:  # Si le joueur se déplace vers la gauche

                # On déplace tous les sprites vers la gauche
                offset = self.player.horizontal_movement * dt
                for sprite_group in self.sprite_groups:
                    for sprite in sprite_group:
                        sprite.rect.x -= offset
                        self.scroll = True

    def run(self, joysticks, dt):
        # Fonction principale qui fait tourner le jeu dans les niveaux

        # Ciel
        self.display_surface.fill((51, 165, 255))

        # Arrière-plan :
        self.background.draw(self.display_surface)

        # Decoration
        self.decoration.draw(self.display_surface)

        # Terrain
        self.terrain.draw(self.display_surface)

        # Pièces
        self.coins.update()
        self.coins.draw(self.display_surface)

        # Joueur
        self.display_surface.blit(self.player.image, (self.player.rect.x, self.player.rect.y))

        # Enemies
        self.enemies.draw(self.display_surface)

        # Mer :
        self.deep_water.update()
        self.deep_water.draw(self.display_surface)
        self.surface_water.update()
        self.surface_water.draw(self.display_surface)

        # Premier-plan:
        self.foreground.draw(self.display_surface)

        # Portes
        self.doors.draw(self.display_surface)

        # Interface de l'utilisateur
        self.ui.draw(self.nb_coins, self.nb_goomba, self.nb_bee, self.nb_isib, self.player.current_lives)

        # Actualisation de l'écran
        pygame.display.flip()

        # Actualisation du joueur :
        self.player.update(joysticks, dt)
        self.check_coin_collision()
        self.check_finish()

        # Actualisation des ennemis :
        self.enemies.update()
        self.check_enemy_collision()

        # Camera scroll:
        self.camera_scroll(dt)

        # Collisions du joueur
        self.horizontal_collision(dt)
        self.vertical_collision(dt)

        self.check_player_death()  # mort
