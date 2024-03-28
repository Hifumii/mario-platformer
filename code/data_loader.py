import json
import os


def get_player_data(path):
    if os.path.exists(path):
        # Si le fichier existe, on récupère les données du joueur
        with open(path, 'r') as player_data:
            data = json.load(player_data)
    else:
        # Si le fichier n'existe pas, on le crée
        data = {
            'level1': [0, 22],
            'level2': [0, 34],
            'level3': [0, 32]
        }
        with open(path, 'w') as player_data:
            json.dump(data, player_data)

    return data


def update_player_data(path, level, nb_coin):
    with open(path, 'r') as player_data:
        data = json.load(player_data)

    key = 'level' + str(level)

    best_nb_coin = data[key][0]
    if nb_coin > best_nb_coin:
        data[key][0] = nb_coin

        with open(path, 'w') as player_data:
            json.dump(data, player_data)

        return True

    else:

        return False
