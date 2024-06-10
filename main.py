################################################################################
#########|                                                            |#########
#########|   Fichier principal à exécuter se faire affronter les IA   |#########
#########|____________________________________________________________|#########
################################################################################





"""
Crédits :
Script réalisé par DE SAINT LEGER Térence
Remerciments à BLANDIN Anatole pour sa participation au développement

Prière de vous référer à READ_ME.txt pour plus d'informations

Pour modifier les équipes participant, merci de modifier les variables "team_1" et "team_2" ci_dessous

Pour augmenter ou diminuer la vitesse générale des IA, merci de modifier les constante "AI_SLOW_FACTOR" et "MIN_WAIT" situées à la toute fin de ce script
"""


if __name__ == "__main__":
    # Participants (entrer le nom du fichier)
    team_1 = "Nerd"
    team_2 = "Mandic"





################################################################################
#>-----------------< Eléments communs à tous les processus >------------------<#
################################################################################




#---------------------------< Imports des modules >----------------------------#


import multiprocessing as mp # Permet de faire tourner plusieurs fils de code
import pygame as pg # Moteur du jeu
from typing import List, Tuple



#>-------------------------< Fonctions principales >--------------------------<#


def AI_controler(q_in: mp.Queue, q_out: mp.Queue, AI_brain, AI_nb: int=1) -> None:
    """Gestion des IA"""

    # Initialisation des variables (non-nécessaire, met permet au participant de voir la nature de ces variables)
    maze: List[List[str]] = None
    pos_self: Tuple[int, int] = None
    pos_enemy: Tuple[int, int] = None

    # Indique au fil principal que l'IA est prète
    q_in[7 if AI_nb == 1 else 8] = True

    # L'IA tourne jusqu'à ce que l'épreuve soit finie
    while True:

        # Doit attendre jusqu'à avoir reçu les dernières informations
        if not q_in[3 if AI_nb == 1 else 4]:
            continue

        # Récupération des informations
        maze = list(q_in[0])
        pos_self = tuple(q_in[1 if AI_nb == 1 else 2])
        pos_enemy = tuple(q_in[2 if AI_nb == 1 else 1])

        # L'IA indique à quelle position elle pense être (débugging)
        q_in[5 if AI_nb == 1 else 6] = pos_self

        # Chronomètre : Début de l'exécution
        start = timer()

        # Exécution du cerveau de l'IA et obtention d'une output
        action = AI_brain(maze, pos_self, pos_enemy)

        # Chronomètre : Fin de l'exécution
        end = timer()

        # Délai d'attente entre chaque exécution (avec pour délai minimum MIN_WAIT)
        pg.time.wait(max(int((end - start) * 1e3 * AI_SLOW_FACTOR), MIN_WAIT))

        # Si l'output est valide
        if action in ("H", "B", "D", "G"):

            # Doit attendre pour recevoir les dernières données
            q_in[3 if AI_nb == 1 else 4] = False

            # Ajout de l'output au fil de communication
            q_out.put((action, round((end - start)*1e6, 1)))
            action = None





################################################################################
#>-----------------< Eléments propre au processus principal >-----------------<#
################################################################################




# Partie exécuté seulement si ce processus est le principal
if __name__ == "__main__":



#>--------------------------< Imports des modules >---------------------------<#


    import random as rd # Permet une génération aléatoire
    import math # Utilisé 1 ou 2 fois pour des calculs
    from os import listdir # Chargement automatique des images
    from ressources.scripts.police import zoneTexte, POLICE # Police faite maison :)
    from ast import literal_eval # Utilisé pour une évaluation sécurisé des expressions



#>---------------------< Fonctions et objets principaux >---------------------<#


    # Partie chargement des images


    def load_img(path: str, size: Tuple[int, int]|None=None) -> pg.Surface:
        """Charge une image et ajuste sa taille"""

        # Chargement de l'image
        img = pg.image.load(path)

        # Si l'image ne doit pas être redimmensionnée, alors retourne l'image
        if size is None:
            return img

        # smoothscale() nécessite une image en 24-bits ou 32-bits
        if img.get_bitsize() in (24, 32):
            return pg.transform.smoothscale(img, size)
        return pg.transform.scale(img, size)


    # Partie IA


    def update_AI(run_AI: bool=True) -> None:
        """Met à jour les données qu'ont les IA et gère leurs output"""

        # Variables globales
        global AI1_pos, AI2_pos, AI1_true_pos, AI2_true_pos, t1_score, t2_score

        AI1_outputed = AI2_outputed = False

        # Réception et gestion des données (+ log des output)

        # Utilisé pour l'affichage du momment d'output
        time_txt = str(int(game_time%6e4)).zfill(5)

        # Depuis l'IA n°1
        while not com_out_AI1.empty():
            output_AI1, t_delta = com_out_AI1.get()

            AI1_outputed = True

            # Exécution de l'output
            if output_AI1 in MOVE and carte[AI1_pos[1] + MOVE[output_AI1][1]][AI1_pos[0] + MOVE[output_AI1][0]] != "#":
                AI1_pos = (AI1_pos[0] + MOVE[output_AI1][0], AI1_pos[1] + MOVE[output_AI1][1])

                # Si l'IA a atteint un fromage
                if carte[AI1_pos[1]][AI1_pos[0]] == "$":
                    carte[AI1_pos[1]][AI1_pos[0]] = " "
                    t1_score += 1

            # Log de l'output
            if debug:
                print(f"Temps d'exécution de l'IA n°1 : {t_delta} micro-secondes\n({int(game_time//6e4)}:{time_txt[-5:-3]}:{time_txt[-3:]})  IA n°1  ->  {output_AI1}\nPosition de l'IA n°1  :  x = {AI1_pos[0]} ; y = {AI1_pos[1]}\n")

        # Depuis l'IA n°2
        while not com_out_AI2.empty():
            output_AI2, t_delta = com_out_AI2.get()

            AI2_outputed = True

            # Exécution de l'output
            if output_AI2 in MOVE and carte[AI2_pos[1] + MOVE[output_AI2][1]][AI2_pos[0] + MOVE[output_AI2][0]] != "#":
                AI2_pos = (AI2_pos[0] + MOVE[output_AI2][0], AI2_pos[1] + MOVE[output_AI2][1])

                # Si l'IA a atteint un fromage
                if carte[AI2_pos[1]][AI2_pos[0]] == "$":
                    carte[AI2_pos[1]][AI2_pos[0]] = " "
                    t2_score += 1

            # Log de l'output
            if debug:
                print(f"Temps d'exécution de l'IA n°2 : {t_delta} micro-secondes\n({int(game_time//6e4)}:{time_txt[-5:-3]}:{time_txt[-3:]})  IA n°2  ->  {output_AI2}\nPosition de l'IA n°2  :  x = {AI2_pos[0]} ; y = {AI2_pos[1]}\n")

        # Envoi des données aux IA (champ d'input commun)

        # La carte
        com_in_AIs[0] = list(carte)
        # Position de l'IA n°1
        com_in_AIs[1] = tuple(AI1_pos)
        # Position de l'IA n°2
        com_in_AIs[2] = tuple(AI2_pos)

        if AI1_outputed:
            # Autorisation à l'IA n°1 de continuer
            com_in_AIs[3] = run_AI

        if AI2_outputed:
            # Autorisation à l'IA n°2 de continuer
            com_in_AIs[4] = run_AI

        # Actualisation des variables de debug
        AI1_true_pos = com_in_AIs[5] if run_AI else (-1, -1)
        AI2_true_pos = com_in_AIs[6] if run_AI else (-1, -1)


    def kill_AI() -> None:
        """Tue les processus des IA si ils sont vivant"""

        # Variables globales
        global AI1_process, AI2_process

        # Suppression des processus d'IA (de manière violente, car on a pas le temps)
        if AI1_process.is_alive():
            AI1_process.terminate()
        if AI2_process.is_alive():
            AI2_process.terminate()


    def reboot_AI() -> None:
        """Relance les IA et affiche l'écran "Versus" si nécessaire"""

        # Affichage de l'écran "Versus"
        if do_vs_screen:
            vs_screen()

        # Variables globales
        global com_in_AIs, AI1_process, AI2_process, AI1_pos, AI2_pos

        # Suppression des processus d'IA (de manière violente, car on a pas le temps)
        if AI1_process.is_alive():
            AI1_process.terminate()
        if AI2_process.is_alive():
            AI2_process.terminate()

        # Réset les données dans "com_in_AIs"
        for nb, value in enumerate([[[[" "]]], (0, 0), (0, 0), False, False, (-1, -1), (-1, -1), False, False]):
            com_in_AIs[nb] = value

        # Réset de la position des IA
        AI1_pos = AI2_pos = spawnpoint

        # Recréation des fils de code séparés pour les IA
        AI1_process = mp.Process(target=AI_controler, args=(com_in_AIs, com_out_AI1, AI1_brain, 1))
        AI2_process = mp.Process(target=AI_controler, args=(com_in_AIs, com_out_AI2, AI2_brain, 2))

        # Lancement des IA (posibilité de mettre ces lignes en commentaire pour ne pas lancer 1 des IA ou les 2)
        AI1_process.start()
        AI2_process.start()


    # Partie génération de la carte


    def re_init(map_size: Tuple[int, int]|None=None) -> None:
        """(Re)Initialise toutes les variables afin de générer une nouvelle carte"""

        # Variables globales
        global dim_carte, size_carte, carte, used_tiles_set, screen, screen_zoom_size, screen_pos, gen_signature

        # Partie carte
        if map_size is None:
            # Si la carte doit être générée aléatoirement
            dim_carte = (rd.randint(24, 34), rd.randint(19, 29))
            # On veux toujours que la carte soie plus large que haute
            if dim_carte[0] < dim_carte[1]:
                dim_carte = (dim_carte[1], dim_carte[0])
        else:
            # Si la carte est pré-générée
            dim_carte = (max(5, map_size[0]), max(5, map_size[1]))
            gen_signature = r_gui.elements["txt_file"].get_input()
        # Taille de la carte en pixels
        size_carte = (dim_carte[0]*SIZE, dim_carte[1]*SIZE)
        # Matrice de la carte
        carte = [[" " if x not in [0, 1, dim_carte[0] - 1, dim_carte[0] - 2] and y not in [0, 1, dim_carte[1] - 1, dim_carte[1] - 2] else "#" for x in range(dim_carte[0])] for y in range(dim_carte[1])]
        used_tiles_set = rd.choice(list(tiles_set.keys()))

        # Partie écran de simulation
        # Surface sur laquelle est dessinée la carte
        screen = pg.surface.Surface(size_carte)
        # Dimensions de cette surface lorsqu'elle est en plein écran
        screen_zoom_size = (fs_width, int(size_carte[1]*fs_width/size_carte[0])) if fs_width/size_carte[0] < fs_height/size_carte[1] else (int(size_carte[0]*fs_height/size_carte[1]), fs_height)
        # Position d'affichage de la surface (pour la centrer à l'écran)
        screen_pos = ((fs_width - screen_zoom_size[0])//2, (fs_height - screen_zoom_size[1])//2)


    def reset_cheese_count() -> int:
        """Recompte le nombre de fromage sur la carte et réinitialise les scores"""

        # Variables globales
        global nb_cheese, t1_score, t2_score

        # On compte le nombre de fromage présents sur la carte
        nb_cheese = 0
        for y in range(2, dim_carte[1] - 2):
            for x in range(2, dim_carte[0] - 2):
                if carte[y][x] == "$":
                    nb_cheese += 1

        # On réinitialise les scores
        t1_score = t2_score = 0


    def find_AI_spawnpoint() -> Tuple[int, int]:
        """Trouve le point de spawn le plus adapté pour les IA"""

        # Le but est d'apparaitre le plus loin possible des fromages

        # Trouve la localisation de tous les fromages
        l_cheese = []
        for y in range(2, dim_carte[1] - 2):
            for x in range(2, dim_carte[0] - 2):
                if carte[y][x] == "$":
                    l_cheese.append((x, y))

        # Trouve le point d'apparition le plus éloigné des fromages
        spawn_pos = (0, 0)
        spawn_dist = 10**10

        # On parcourt toute la carte sauf ses bordures
        for y in range(2, dim_carte[1] - 2):
            for x in range(2, dim_carte[0] - 2):

                # Le point d'apparition doit être un espace vide
                if carte[y][x] == " ":
                    # Calcul de la proximité aux fromages
                    dist = 0

                    # Ajout de la proximité (distance ** -1)
                    for cheese_x, cheese_y in l_cheese:
                        dist += ((x - cheese_x)**2 + (y - cheese_y)**2)**(-0.5)

                    # Moyenne
                    dist /= len(l_cheese)

                    # Si la proximité est plus faible, alors on prend cette position
                    if dist < spawn_dist:
                        spawn_pos = (x, y)
                        spawn_dist = dist

        # On retourne la position de spawn la plus adaptée
        return spawn_pos


    def generate_block(size: Tuple[int, int]=(1, 1), invert: bool=False) -> None:
        """Génération de block de mur ou en vide"""

        # Position du curseur (centre du bloc)
        pos = [rd.randint(size[0]//2 + 2, dim_carte[0] - math.ceil(size[0]/2) - 2), rd.randint(size[1]//2 + 2, dim_carte[1] - math.ceil(size[1]/2) - 2)]

        # Methode de flemmard pour faire les contours du bloc en espaces vides
        if not invert:
            # Remplissage d'une zone 2x2 tuilles plus large que l'originale
            for dy in range(- (size[1]//2) - 1, math.ceil(size[1]/2) + 1):
                for dx in range(- (size[0]//2) - 1, math.ceil(size[0]/2) + 1):
                    # On ne touche pas aux bordures de la map
                    if 1 < pos[0] + dx < dim_carte[0] - 2 and 1 < pos[1] + dy < dim_carte[1] - 2:
                        carte[pos[1] + dy][pos[0] + dx] = " "

        # Remplissage de la zone où le block est situé
        for dy in range(- (size[1]//2), math.ceil(size[1]/2)):
            for dx in range(- (size[0]//2), math.ceil(size[0]/2)):
                carte[pos[1] + dy][pos[0] + dx] = " " if invert else "#"


    def generate_wall(max_lenght: int=1000, from_sides: bool=False, expend_wall: bool=False) -> None:
        """Génération de mur sur la carte"""

        # Liste de mouvement possible (Haut, Bas, Droite, Gauche)
        moves = [(0, -1), (0, 1), (1, 0), (-1, 0)]

        # Position de départ du curseur (aléatoire)
        pos = [rd.randint(2, dim_carte[0] - 3), rd.randint(2, dim_carte[1] - 3)]

        # Déplacement vers une bordure
        if from_sides:
            # Choix de la bordure
            where = rd.choice(("N", "S", "E", "W"))

            # Bordure du haut
            if where == "N":
                pos[1] = 2
            # Bordure du bas
            elif where == "S":
                pos[1] = dim_carte[1] - 3
            # Bordure à droite
            elif where == "E":
                pos[0] = 2
            # Bordure à gauche
            else:
                pos[0] = dim_carte[0] - 3

        # Si True, alors le nouveau mur partira forcément d'un mur déjà existant
        elif expend_wall:
            for _ in range(100):
                if carte[pos[1]][pos[0]] != "#":
                    pos = [rd.randint(2, dim_carte[0] - 3), rd.randint(2, dim_carte[1] - 3)]
                else:
                    break

        # Si False, alors le nouveau mur ne partira pas d'un mur déjà existant
        else:
            # Limite de test, car il est fort probable d'obtenir une boucle infinie
            for _ in range(100):
                # Test des tuilles adjacentes
                for delta in ((0, 0), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)):
                    if carte[pos[1] + delta[1]][pos[0] + delta[0]] == "#":
                        # Nouvelle position
                        pos = [rd.randint(3, dim_carte[0] - 4), rd.randint(3, dim_carte[1] - 4)]
                        break # Nouveau test
                else: # Test réussi
                    carte[pos[1]][pos[0]] = "#"
                    break # Fin des tests

        # Placement du premier mur si le curseur est situé sur le bord de la carte

        # Bordure à gauche
        if pos[0] == 2:
            for delta in ((2, -1), (2, 0), (2, 1), (1, -1), (1, 0), (1, 1)):
                if carte[pos[1] + delta[1]][pos[0] + delta[0]] == "#":
                    break # Echec du test
            else: # Si le nouveau mur peut être placé
                carte[pos[1]][pos[0]] = "#"

        # Bordure à droite
        elif pos[0] == dim_carte[0] - 3:
            for delta in ((-2, -1), (-2, 0), (-2, 1), (-1, -1), (-1, 0), (-1, 1)):
                if carte[pos[1] + delta[1]][pos[0] + delta[0]] == "#":
                    break # Echec du test
            else: # Si le nouveau mur peut être placé
                carte[pos[1]][pos[0]] = "#"

        # Bordure en haut
        elif pos[1] == 2:
            for delta in ((-1, 2), (0, 2), (1, 2), (-1, 1), (0, 1), (1, 1)):
                if carte[pos[1] + delta[1]][pos[0] + delta[0]] == "#":
                    break # Echec du test
            else: # Si le nouveau mur peut être placé
                carte[pos[1]][pos[0]] = "#"

        # Bordure en bas
        elif pos[1] == dim_carte[1] - 3:
            for delta in ((-1, -2), (0, -2), (1, -2), (-1, -1), (0, -1), (1, -1)):
                if carte[pos[1] + delta[1]][pos[0] + delta[0]] == "#":
                    break # Echec du test
            else: # Si le nouveau mur peut être placé
                carte[pos[1]][pos[0]] = "#"

        # Partie principale
        for _ in range(max_lenght):

            # Déplacement dans une direction aléatoire
            rd.shuffle(moves)
            for move in moves:
                # Le nouveau mur ne devra pas toucher d'autre mur (sauf celui dont il provient)

                # Test déplacement vers le haut
                if move == (0, -1):

                    for delta in ((-1, -2), (0, -2), (1, -2), (-1, -1), (0, -1), (1, -1)):
                        if carte[pos[1] + delta[1]][pos[0] + delta[0]] == "#":
                            break # Echec du test

                    else: # Si le nouveau mur peut être placé
                        break # Fin des tests

                # Test déplacement vers le bas
                if move == (0, 1):

                    for delta in ((-1, 2), (0, 2), (1, 2), (-1, 1), (0, 1), (1, 1)):
                        if carte[pos[1] + delta[1]][pos[0] + delta[0]] == "#":
                            break # Echec du test

                    else: # Si le nouveau mur peut être placé
                        break # Fin des tests

                # Test déplacement vers la droite
                if move == (1, 0):

                    for delta in ((2, -1), (2, 0), (2, 1), (1, -1), (1, 0), (1, 1)):
                        if carte[pos[1] + delta[1]][pos[0] + delta[0]] == "#":
                            break # Echec du test

                    else: # Si le nouveau mur peut être placé
                        break # Fin des tests

                # Test déplacement vers la gauche
                if move == (-1, 0):

                    for delta in ((-2, -1), (-2, 0), (-2, 1), (-1, -1), (-1, 0), (-1, 1)):
                        if carte[pos[1] + delta[1]][pos[0] + delta[0]] == "#":
                            break # Echec du test

                    else: # Si le nouveau mur peut être placé
                        break # Fin des tests

            else: # Si aucun mouvement n'est possible
                break # Arret des déplacements

            # Déplacement du curseur
            pos[0] += move[0]
            pos[1] += move[1]
            # Placement du mur
            carte[pos[1]][pos[0]] = "#"


    def place_cheese() -> None:
        """Place un fromage sur la carte"""

        # Tant que le fromage n'a pas été placé
        while True:

            # Position aléatoire (avec les bordures en mur exclues)
            pos = [rd.randint(2, dim_carte[0] - 3), rd.randint(2, dim_carte[1] - 3)]

            # Test pour placer le fromage
            if carte[pos[1]][pos[0]] == " ":
                carte[pos[1]][pos[0]] = "$"
                break # Fin


    def generate_carte() -> None:
        """Permet de générer un nouveau labyrinthe"""

        # Variables globales
        global gen_signature, nb_cheese, spawnpoint, AI1_pos, AI2_pos

        # Réinitialisation de la carte
        for y in range(2, dim_carte[1] - 2):
            for x in range(2, dim_carte[0] - 2):
                carte[y][x] = " "

        gen_signature = rd.choice(list(GEN_SIGNATURES.keys()))

        # Génération de la carte de manière très random (c'est comme une soupe)

        # Génération par défaut (simple et efficace)
        if gen_signature == "Defaut":
            for _ in range(100):
                generate_wall(rd.randint(5, 10), rd.randint(0, 1), rd.randint(0, 1))

        # Génération de blocs (originale à sa manière)
        elif gen_signature == "Blocks":
            for _ in range(100):
                generate_block((rd.randint(3, 8), rd.randint(3, 8)))

        # Génération officielle
        elif gen_signature == "PYRAT":
            for _ in range(10):
                generate_wall(0)
            for _ in range(rd.randint(1, 5)):
                generate_block((rd.randint(1, 5), rd.randint(1, 5)))
            for _ in range(100):
                generate_wall(rd.randint(5, 10), rd.randint(0, 1))

        # Génération n°1 de Térence
        elif gen_signature == "Ter1":
            for _ in range(100):
                r = rd.random()
                if r < 0.01:
                    generate_block((rd.randint(1, 6), rd.randint(1, 6)), rd.randint(0, 1))
                elif r < 0.08:
                    generate_block((rd.randint(1, 4), rd.randint(1, 4)), rd.randint(0, 1))
                elif r < 0.22:
                    generate_wall(rd.randint(0, 1))
                elif r < 0.45:
                    generate_wall(rd.randint(0, 20), r < 0.26, r < 0.35)
                else:
                    generate_wall(rd.randint(5, 15), r < 0.6, r < 0.8)

        # Génération n°2 de Térence
        elif gen_signature == "Ter2":
            for _ in range(10):
                generate_wall(0)
                generate_wall(from_sides=True)
            for _ in range(rd.randint(1, 5)):
                generate_block((rd.randint(1, 5), rd.randint(1, 5)), True)
            for _ in range(100):
                generate_wall(rd.randint(0, 20), rd.randint(0, 1), rd.randint(0, 1))

        # Génération n°3 de Térence
        elif gen_signature == "Ter3":
            for _ in range(100):
                generate_block((1, 10))
            for _ in range(100):
                generate_wall(from_sides=rd.randint(0, 1), expend_wall=rd.randint(0, 1))

        # Des petits points
        elif gen_signature == "Points":
            for _ in range(400):
                generate_block((1, 1))
                generate_wall(1, rd.randint(0, 1), False)

        # Placement des fromages (universel à tous les systèmes de génération)
        nb_cheese = (dim_carte[0] * dim_carte[1])//100 * 2 + 1
        for _ in range(nb_cheese):
            place_cheese()

        # Point d'apparition des IA
        spawnpoint = find_AI_spawnpoint()
        AI1_pos = tuple(spawnpoint)
        AI2_pos = tuple(spawnpoint)


    # Partie interface et éléments cliquables


    class Cursor:
        """Classe gérant toutes les interactions du curseur de la souris (pas celle dans le labyrinthe)"""

        def __init__(self) -> None:

            # Position du curseur
            self.pos = pg.mouse.get_pos()

            # Postion de la souris sur la carte
            self.tile_pos = (int((self.pos[0] - screen_pos[0])//(screen_zoom_size[0] / dim_carte[0])), int((self.pos[1] - screen_pos[1])//(screen_zoom_size[1] / dim_carte[1])))

            # Boutons de la souris pressées
            self.m_pressed = pg.mouse.get_pressed(5)
            self.old_m_pressed = list(self.m_pressed)

            # Si il faut afficher la case sélectionnée
            self.do_show_tile = bool(edit and 1 < self.tile_pos[0] < dim_carte[0] - 2 and 1 < self.tile_pos[1] < dim_carte[1] - 2)

        def update(self) -> None:
            """Met à jour les données de la souris"""

            # Position du curseur
            self.pos = pg.mouse.get_pos()

            # Postion de la souris sur la carte
            self.tile_pos = (int((self.pos[0] - screen_pos[0])//(screen_zoom_size[0] / dim_carte[0])), int((self.pos[1] - screen_pos[1])//(screen_zoom_size[1] / dim_carte[1])))

            # Boutons de la souris pressées
            self.old_m_pressed = list(self.m_pressed)
            self.m_pressed = pg.mouse.get_pressed(5)

            # Si il faut afficher la case sélectionnée
            self.do_show_tile = bool(edit and 1 < self.tile_pos[0] < dim_carte[0] - 2 and 1 < self.tile_pos[1] < dim_carte[1] - 2)

        def pressed(self, mouse_nb: int=0, reverse: bool=False) -> bool:
            """Retourne un booléan indiquant si le bouton testé vient d'être pressé ou relaché"""

            return (self.old_m_pressed[mouse_nb] and not self.m_pressed[mouse_nb]) if reverse else (self.m_pressed[mouse_nb] and not self.old_m_pressed[mouse_nb])


    class Text_input:
        """Barre d'input textuel"""

        # Ce qui est considéré comme une valeur numérique
        int_input = "0123456789"
        # Ce qui est accèpté pour les inputs textuels plus générals
        str_input = "".join([char for char in POLICE if char not in '\\/:*?"<>|'])

        def __init__(self, pos: Tuple[int, int], lenght: int, text: str="", default_text: str="", text_size: int=1, is_int: bool=False) -> None:

            # Position de la barre d'input textuel
            self.pos = pos

            # Taille de la barre d'input textuel
            self.lenght = lenght
            # Taille de la police
            self.text_size = text_size
            # Si les inputs ne peuvent que être des valeurs numériques
            self.is_int = is_int

            # Taille de la zone de texte
            self.tz_size = (lenght, text_size*11 + 20)

            # Texte affiché lorsque la barre d'input textuel est vide
            self.default_text = default_text
            # Texte contenu dans la barre d'input textuel
            self.text = text

            # Si la barre d'input textuel est sélectionnée
            self.selected = False

        def display(self) -> None:
            """Affichage de la barre d'input textuel sur l'écran d'affichage"""

            pg.draw.rect(focus_screen, (225, 225, 225) if self.selected else (175, 175, 175), (self.pos, self.tz_size))
            focus_screen.blit(zoneTexte(f"(0,0,0)${self.text}" if self.text != "" else f"(100,100,100)${self.default_text}", self.text_size), (self.pos[0] + 10, self.pos[1] + 10), ((0, 0), (self.tz_size[0] - 20, self.tz_size[1] - 20)))
            pg.draw.rect(focus_screen, (0, 0, 0), (self.pos, self.tz_size), 5)

        def update(self) -> None:
            """Récupère les touches pressés par l'utilisateur et met à jour l'input"""

            # Lorsque la souris est pressée
            if mouse.pressed(0):
                # Si la barre d'input textuel est cliquée
                if self.pos[0] <= mouse.pos[0] <= self.pos[0] + self.tz_size[0] and self.pos[1] <= mouse.pos[1] <= self.pos[1] + self.tz_size[1]:
                    # Alors elle devient sélectionnée/désélectionnée
                    self.selected = not self.selected
                    # Empêche l'utilisateur de cliquer sur plusieurs choses à la fois
                    mouse.old_m_pressed[0] = True
                else:
                    # Sinon elle n'est plus sélectionnée
                    self.selected = False

            elif mouse.old_m_pressed[0]:
                if not(self.pos[0] <= mouse.pos[0] <= self.pos[0] + self.tz_size[0] and self.pos[1] <= mouse.pos[1] <= self.pos[1] + self.tz_size[1]):
                    self.selected = False

            # Si la barre d'input textuel est sélectionnée
            if self.selected:

                # On regarde toutes les touches pressées
                for char in keys_pressed:

                    # Ajout du charactère si il est valide
                    if char in (self.int_input if self.is_int else self.str_input):
                        self.text += char

                    # Supression d'un charactère si la touche RETOUR est pressée
                    elif char == "BACKSPACE":
                        if len(self.text) != 0:
                            self.text = self.text[:-1]

                    # Fin de sélection si la touche ENTRER est pressée
                    elif char == "RETURN":
                        self.selected = False

        def get_input(self) -> str:
            """Récupère l'input contenu dans la barre d'input textuel"""

            return (int(self.text) if self.text != "" else 0) if self.is_int else str(self.text)


    class Button:
        """Bouton pressable stockant son état"""

        # Chargement de toutes les bases de bouton (commun à tous les objet Button)
        base_img = {name[:-4]: load_img(f"ressources/images/boutons/bases/{name}", (64, 64)) for name in listdir("ressources/images/boutons/bases") if name.endswith(".png")}

        def __init__(self, pos: Tuple[int, int], default_state: bool|int=0, icon_name: str|None=None, description: str|None=None, color: Tuple[int, int, int]=(255, 255, 255)) -> None:

            # Position du bouton
            self.pos = pos
            # Etat du bouton ("True" : activé ; "False" : désactivé ; "One" : activé 1 fois ; "Zero" : désactivé indéfiniment)
            # bool = interchangeable à tout momment, int = seulement changeable 1 fois
            self.state = default_state
            # Icone affichée sur le bouton
            self.icon = load_img(f"ressources/images/boutons/icones/{icon_name}.png", (64, 64)) if icon_name is not None else None

            # Description affichée lorsque le curseur touche le bouton
            if description is not None:
                description = zoneTexte(f"{color}${description}")
                desc_dim = description.get_size()

                # Taille de la description
                self.desc_dim = (desc_dim[0] + 20, desc_dim[1] + 20)
                # Description
                self.description = pg.surface.Surface(self.desc_dim)

                pg.draw.rect(self.description, (100, 100, 100), ((5, 5), (desc_dim[0] + 10, desc_dim[1] + 10)))
                self.description.blit(description, (10, 10))
            else:
                self.description = self.desc_dim = None

            # Si l'on doit afficher la description
            self.do_display_desc = False

            # Stoque la dernière fois où le bouton a été pressé
            self.last_pressed = -1

        def display(self) -> None:
            """Affichage du bouton sur l'écran d'affichage"""

            # Affichage du la base du bouton
            focus_screen.blit(self.base_img[("on" if self.state else "off") if type(self.state) == bool else ("one" if self.state else "zero")], self.pos)

            # Affichage de l'icone du bouton
            if self.icon is not None:
                focus_screen.blit(self.icon, self.pos)

        def display_desc(self) -> None:
            """Affiche la description du boutton si le curseur est sur le bouton"""

            if self.do_display_desc and self.description is not None:
                focus_screen.blit(self.description, (mouse.pos[0] - self.desc_dim[0]//2, mouse.pos[1] - 10 - self.desc_dim[1]))

        def update(self) -> None:
            """Détecte les cliques et met à jour le bouton en conséquence"""

            # Le curseur doit toucher le bouton
            if self.pos[0] <= mouse.pos[0] <= self.pos[0] + 64 and self.pos[1] <= mouse.pos[1] <= self.pos[1] + 64:
                # Alors, on affiche la description
                self.do_display_desc = True
                # Si la souris est pressée
                if mouse.pressed(0):
                    # On modifie l'état du bouton en fonction de son état actuel

                    if type(self.state) == bool:
                        # On modifie l'état du bouton
                        self.state = not self.state
                        # On note également le momment auquel à eu lieu ce changement
                        self.last_pressed = game_time + game_start
                        # Empêche l'utilisateur de cliquer sur plusieurs choses à la fois
                        mouse.old_m_pressed[0] = True

                    elif self.state:
                        # On modifie l'état du bouton
                        self.state = 0
                        # On note également le momment auquel à eu lieu ce changement
                        self.last_pressed = game_time + game_start
                        # Empêche l'utilisateur de cliquer sur plusieurs choses à la fois
                        mouse.old_m_pressed[0] = True

            else:
                #  n'affiche pas la description
                self.do_display_desc = False

        def get_state(self) -> bool:
            """Retourne l'état du bouton"""

            return bool(self.state)


    class Icon:
        """Icone ou texte affiché à l'écran"""

        def __init__(self, pos: Tuple[int, int], value: str, text_size: Tuple[int, int]|int=(64, 64)) -> None:

            # Position à laquelle l'icone sera affichée
            self.pos = pos

            # Si "text_size" est une tuple alors on charge une image
            if isinstance(text_size, tuple):
                self.icon = load_img(f"ressources/images/boutons/icones/{value}.png", text_size)

            # Sinon sela signifie que l'on doit créer une zone de texte
            else:
                self.icon = zoneTexte(f"(255,255,255)${value}", text_size)
        
        def display(self) -> None:
            """Affiche l'icone sur l'écran d'affichage"""

            focus_screen.blit(self.icon, self.pos)


    class Interface:
        """Classe principale de l'interface, barre d'interface"""

        def __init__(self, on_right_side: bool=False) -> None:

            # Coté sur lequel l'interface est affichée
            self.fliped = on_right_side

            # Si l'interface est ouverte et affichée ou non
            self.is_opened = False

            # Création du sprite pour la barre d'interface
            self.dim = (250, fs_height - 200)
            self.cz_dim = (40, 100)
            self.sprite = pg.surface.Surface(self.dim)
            self.sprite.fill((1, 1, 1))
            self.sprite.set_colorkey((1, 1, 1))

            # Outline (partie barre principale)
            pg.draw.rect(self.sprite, (0, 0, 0), ((-60, 0), (self.dim[0] + 30, self.dim[1])), border_radius=30)
            # Outline (partie zone cliquable)
            pg.draw.rect(self.sprite, (0, 0, 0), (((self.dim[0] - self.cz_dim[0] - 15), (self.dim[1] - self.cz_dim[1])//2 - 5), (self.cz_dim[0] + 10, self.cz_dim[1] + 10)), border_radius=15)

            # Petite barre cliquable pour cacher/montrer la barre d'interface
            pg.draw.rect(self.sprite, (50, 50, 50), (((self.dim[0] - self.cz_dim[0] - 10), (self.dim[1] - self.cz_dim[1])//2), self.cz_dim), border_radius=10)
            # Partie principale de la barre
            pg.draw.rect(self.sprite, (65, 65, 65), ((-50, 10), (self.dim[0] + 10, self.dim[1] - 20)), border_radius=20)

            # On flip le sprite si il doit être à droite de l'écran (au lieu d'à gauche)
            if self.fliped:
                self.sprite = pg.transform.rotate(self.sprite, 180)

                # Définition des éléments de droite
                self.elements = {
                    "icon_edit": Icon((fs_width - self.dim[0] + 75, (fs_height - self.dim[1])//2 + 25), "Menu d'édition\n  de carte", 2),
                    "edit": Button((fs_width - self.dim[0] + 115, (fs_height - self.dim[1])//2 + 85), edit, "editeur", "Mode éditeur\nKill automatiquement les IA"),
                    "e_mur": Button((fs_width - self.dim[0] + 70, (fs_height - self.dim[1])//2 + 175), 0, "t_mur", "Placer un mur"),
                    "e_sol": Button((fs_width - self.dim[0] + 160, (fs_height - self.dim[1])//2 + 175), 0, "t_sol", "Placer une case vide"),
                    "e_spawn": Button((fs_width - self.dim[0] + 70, (fs_height - self.dim[1])//2 + 265), 0, "t_spawn", "Placer le départ"),
                    "e_fromage": Button((fs_width - self.dim[0] + 160, (fs_height - self.dim[1])//2 + 265), 0, "t_fromage", "Placer un fromage"),
                    "save": Button((fs_width - self.dim[0] + 70, (fs_height - self.dim[1])//2 + 355), 1, "save", "Sauvegarde la carte"),
                    "load": Button((fs_width - self.dim[0] + 160, (fs_height - self.dim[1])//2 + 355), 1, "load", "Charge une carte"),
                    "txt_file": Text_input((fs_width - self.dim[0] + 70, (fs_height - self.dim[1])//2 + 445), 154, default_text="Nom du fichier texte"),
                    "size_x": Text_input((fs_width - self.dim[0] + 95, (fs_height - self.dim[1])//2 + 500), 42, "10", "X", 2, True),
                    "size_y": Text_input((fs_width - self.dim[0] + 95, (fs_height - self.dim[1])//2 + 550), 42, "10", "Y", 2, True),
                    "icon_x": Icon((fs_width - self.dim[0] + 60, (fs_height - self.dim[1])//2 + 505), "largeur", (32, 32)),
                    "icon_y": Icon((fs_width - self.dim[0] + 60, (fs_height - self.dim[1])//2 + 555), "hauteur", (32, 32)),
                    "reset": Button((fs_width - self.dim[0] + 160, (fs_height - self.dim[1])//2 + 513), 1, "reset", "Recréer une carte vierge\naux dimmensions choisies")
                }

            if not self.fliped:
                # Définition des éléments de gauche
                self.elements = {
                    "menu_p": Icon((30, (fs_height - self.dim[1])//2 + 25), "Menu principal", 2),
                    "quit": Button((25, (fs_height - self.dim[1])//2 + 65), 1, "quit", "Quitter le programme\nRaccourci : \"Echap\""),
                    "reload": Button((115, (fs_height - self.dim[1])//2 + 65), 1, "reload", "Générer une nouvelle carte\nRaccourci : \"Astérisk\""),
                    "icon_IA": Icon((61, (fs_height - self.dim[1])//2 + 155), "Gestion des IA", 1),
                    "run": Button((25, (fs_height - self.dim[1])//2 + 175), int(not run_AI), "run", "Lancer les IA"),
                    "stop": Button((115, (fs_height - self.dim[1])//2 + 175), int(run_AI), "stop", "Kill les IA"),
                    "icon_other": Icon((51, (fs_height - self.dim[1])//2 + 265), "Options graphiques", 1),
                    "hd": Button((25, (fs_height - self.dim[1])//2 + 285), HD_display, "hd", "Affichage HD"),
                    "debug": Button((115, (fs_height - self.dim[1])//2 + 285), bool(debug), "debug", "Eléments de débug"),
                    "vs": Button((25, (fs_height - self.dim[1])//2 + 375), bool(do_vs_screen), "vs", "Affichage de l'écran\n\"Versus\" en début\nde match"),
                    "compte_rebour": Button((115, (fs_height - self.dim[1])//2 + 375), bool(do_count_down), "compte_a_rebour", "Compte à rebour\nde 3 secondes en\ndébut de match")
                }

        def display(self) -> None:
            """
            Affichage de la barre d'interface et de son contenu\n
            Update également l'état de l'interface
            """

            # Affichage de la partie principale de l'interface
            focus_screen.blit(self.sprite, (((fs_width - self.dim[0]) if self.fliped else 0) if self.is_opened else ((fs_width - self.cz_dim[0]) if self.fliped else (self.cz_dim[0] - self.dim[0])), (fs_height - self.dim[1])//2))

            # Triangle affiché sur la zone cliquable
            if self.fliped:
                if self.is_opened:
                    pg.draw.polygon(focus_screen, (255, 255, 255), ((fs_width - self.dim[0] + 20, fs_height//2 + 25), (fs_width - self.dim[0] + 20, fs_height//2 - 25), (fs_width - self.dim[0] + 30, fs_height//2)))
                else:
                    pg.draw.polygon(focus_screen, (255, 255, 255), ((fs_width - 10, fs_height//2 + 25), (fs_width - 10, fs_height//2 - 25), (fs_width - 20, fs_height//2)))
            elif self.is_opened:
                pg.draw.polygon(focus_screen, (255, 255, 255), ((self.dim[0] - 20, fs_height//2 + 25), (self.dim[0] - 20, fs_height//2 - 25), (self.dim[0] - 30, fs_height//2)))
            else:
                pg.draw.polygon(focus_screen, (255, 255, 255), ((10, fs_height//2 + 25), (10, fs_height//2 - 25), (20, fs_height//2)))

            # Affiche les boutons
            if self.is_opened:
                # On affiche d'abord les boutons et barres d'input textuelles
                for element in self.elements.values():
                    element.display()
                # On affiche seulement ensuite la description des boutons
                for element in self.elements.values():
                    if element.__class__ == Button:
                        element.display_desc()

        def update(self) -> None:
            """Met à jour l'interface en fonction des inputs"""

            # Variables globales
            global edit, running, debug, HD_display, selected_tile, carte, spawnpoint, run_AI, t1_score, t2_score, game_time, game_start, do_vs_screen, do_count_down

            # Ouverture/fermeture de l'interface
            # Lorsque LMB est pressé et est située dans cet intervale de hauteur
            if mouse.pressed(0) and (fs_height - self.cz_dim[1])//2 <= mouse.pos[1] <= (fs_height + self.cz_dim[1])//2:
                # Si l'interface se situe à droite de l'écran
                if self.fliped:
                    # Si l'interface est ouverte
                    if self.is_opened:
                        # Si la souris est située dans cet intervale de largeur
                        if fs_width - self.dim[0] <= mouse.pos[0] <= fs_width - self.dim[0] + self.cz_dim[0]:
                            # Ferme l'interface
                            self.is_opened = False
                            # Empêche l'utilisateur de cliquer sur plusieurs choses à la fois
                            mouse.old_m_pressed[0] = True
                    # Si l'interface est fermée
                    # Si la souris est située dans cet intervale de largeur
                    elif fs_width - self.cz_dim[0] <= mouse.pos[0]:
                        # Ouvre l'interface
                        self.is_opened = True
                        # Empêche l'utilisateur de cliquer sur plusieurs choses à la fois
                        mouse.old_m_pressed[0] = True
                # Si l'interface se situe à gauche de l'écran
                # Si l'interface est ouverte
                elif self.is_opened:
                    # Si la souris est située dans cet intervale de largeur
                    if self.dim[0] - self.cz_dim[0] <= mouse.pos[0] <= self.dim[0]:
                        # Ferme l'interface
                        self.is_opened = False
                        # Empêche l'utilisateur de cliquer sur plusieurs choses à la fois
                        mouse.old_m_pressed[0] = True
                # Si l'interface est fermée
                # Si la souris est située dans cet intervale de largeur
                elif mouse.pos[0] <= self.cz_dim[0]:
                    # Ouvre l'interface
                    self.is_opened = True
                    # Empêche l'utilisateur de cliquer sur plusieurs choses à la fois
                    mouse.old_m_pressed[0] = True

            # L'interface doit être ouverte !
            if not self.is_opened:
                # Evite les piles de condition
                return None

            # Met à jour les éléments de l'interface
            for element in self.elements.values():
                # Les objets "Icon n'ont pas de méthode "update"
                if element.__class__ != Icon:
                    element.update()

            # Met à jour le programme en fonction de l'état des boutons

            # Boutons contenus dans l'interface de droite
            if self.fliped:
                # Bouton pour le mode éditeur
                sb_edit = self.elements["edit"].get_state()
                if edit and not sb_edit:
                    edit = False
                    # Réset du compte de fromage
                    reset_cheese_count()
                    # Relance les IA si nécessaire
                    if run_AI:
                        reboot_AI()
                elif sb_edit and not edit:
                    edit = True
                    # Arrète les IA
                    kill_AI()
                    # Réset du compte de fromage
                    reset_cheese_count()
                    # On réactive les boutons pour éditer la carte
                    self.elements["reset"].state = 1
                    for button in ("mur", "sol", "spawn", "fromage"):
                        self.elements[f"e_{button}"].state = int(button != selected_tile)

                # Boutons pour éditer la carte
                # Désactivés si le mode éditeur est désactivé
                if edit:
                    # Il y a 4 éléments pour éditer la carte
                    for button in ("mur", "sol", "spawn", "fromage"):
                        # Si le bouton est cliqué et n'est pas celui actuellement sélectionnée
                        if not self.elements[f"e_{button}"].get_state() and selected_tile != button:
                            # Alors on le sélectionne
                            selected_tile = button
                            # On désactive ce bouton et on réactive les autres boutons
                            for button in ("mur", "sol", "spawn", "fromage"):
                                self.elements[f"e_{button}"].state = int(button != selected_tile)
                            break
                # Si le mode éditeur n'est pas actif, alors les boutons pour éditer la carte ne le sont pas non plus
                else:
                    for button in ("mur", "sol", "spawn", "fromage"):
                        self.elements[f"e_{button}"].state = 0

                # Barre d'input textuel pour les noms de fichier
                txt_file = self.elements["txt_file"].get_input()
                # Il faut obligatoirement que le nom du fichier fasse au moins 1 charactère
                if len(txt_file) != 0 and edit:
                    # Alors on peut sauvegarder la carte à ce nom
                    self.elements["save"].state = int(self.elements["save"].last_pressed + 100 < game_time + game_start)
                    # Si un fichier .txt de ce nom existe
                    if txt_file in [file[:-4] for file in listdir("ressources/sauvegardes") if file.endswith(".txt")]:
                        # Alors on peut le charger
                        self.elements["load"].state = int(self.elements["load"].last_pressed + 100 < game_time + game_start)
                    else:
                        # Sinon on ne peut pas le charger
                        self.elements["load"].state = 0
                else:
                    # Si le nom de fichier n'est pas valide
                    self.elements["save"].state = 0
                    self.elements["load"].state = 0

                # Bouton de sauvegarde
                if not self.elements["save"].get_state() and edit and self.elements["save"].last_pressed == game_time + game_start:
                    # Création ou écrasement d'un fichier texte
                    with open(f"ressources/sauvegardes/{txt_file}.txt", "w") as file:
                        # On y met la matrice de la carte + le point d'apparition
                        file.writelines("\n".join(["".join(line) for line in carte] + [str(spawnpoint)]))
                    if debug:
                        print(f'\nCarte sauvegardé sous le nom de "{txt_file}.txt"\n')

                # Bouton pour charger une sauvegarde
                if not self.elements["load"].get_state() and edit and self.elements["load"].last_pressed == game_time + game_start:
                    # On charge le fichier texte de sauvegarde
                    with open(f"ressources/sauvegardes/{txt_file}.txt", "r") as file:
                        file_data = []
                        # On stoque toutes ses données dans une liste
                        for line in file:
                            # On ne garde pas les retours à la ligne
                            file_data.append(line.replace("\n", ""))
                        # On modifie les données de la carte pour qu'elles correspondent à celle de la sauvegarde
                        spawnpoint = literal_eval(file_data[-1])
                        relauch((len(file_data[0]), len(file_data) - 1))
                        carte = [list(line) for line in file_data[:-1]]

                # Bouton pour créer une carte vierge
                if edit:
                    if not self.elements["reset"].get_state():
                        re_init((self.elements["size_x"].get_input() + 4, self.elements["size_y"].get_input() + 4))
                        spawnpoint = (2, 2)
                    self.elements["reset"].state = 1
                else:
                    self.elements["reset"].state = 0

            # Boutons contenus dans l'interface de gauche
            else:
                # Bouton pour quitter
                if not self.elements["quit"].get_state():
                    running = False

                # Bouton de reload de la carte
                if not self.elements["reload"].get_state():
                    relauch()
                    self.elements["reload"].state = 1

                # Bouton pour lancer les IA
                if not(run_AI or self.elements["run"].get_state()):
                    run_AI = True
                    if not edit:
                        reboot_AI()
                    # Réactive le bouton "stop"
                    self.elements["stop"].state = 1

                # Bouton pour tuer les IA
                if run_AI and not self.elements["stop"].get_state():
                    run_AI = False
                    kill_AI()
                    # Réset également les scores
                    reset_cheese_count()
                    # Réactive le bouton "run"
                    self.elements["run"].state = 1

                # Bouton pour l'affichage en HD
                sb_hd = self.elements["hd"].get_state()
                if HD_display and not sb_hd:
                    HD_display = False
                elif sb_hd and not HD_display:
                    HD_display = True

                # Bouton de debug
                sb_debug = self.elements["debug"].get_state()
                if debug and not sb_debug:
                    debug = False
                elif sb_debug and not debug:
                    debug = True

                # Bouton pour l'affichage de l'écran "Versus"
                sb_vs = self.elements["vs"].get_state()
                if do_vs_screen and not sb_vs:
                    do_vs_screen = False
                elif sb_vs and not do_vs_screen:
                    do_vs_screen = True

                # Bouton pour activation du compte à rebour
                sb_count_down = self.elements["compte_rebour"].get_state()
                if do_count_down and not sb_count_down:
                    do_count_down = False
                elif sb_count_down and not do_count_down:
                    do_count_down = True


    def update_carte() -> None:
        """Update la map si l'utilisateur clique dessus"""

        # Variable globale
        global is_drawing, spawnpoint

        # Si le mode éditeur est activé et que le cureur est dans la carte
        if mouse.do_show_tile:

            # Si l'utilisateur est en train de dessiner sur la carte
            if is_drawing:

                # Si l'utilisateur arrète de cliquer, alors il ne dessine plus
                if mouse.pressed(0, True):
                    is_drawing = False

                # Si la pinceau sélectionnée est la tuile mur
                elif selected_tile == "mur":
                    carte[mouse.tile_pos[1]][mouse.tile_pos[0]] = "#"
                # Si la pinceau sélectionnée est la tuile sol
                elif selected_tile == "sol":
                    carte[mouse.tile_pos[1]][mouse.tile_pos[0]] = " "
                # Si la pinceau sélectionnée est le point d'apparition
                elif selected_tile == "spawn":
                    spawnpoint = mouse.tile_pos
                # Si la pinceau sélectionnée est la tuile fromage
                elif selected_tile == "fromage":
                    carte[mouse.tile_pos[1]][mouse.tile_pos[0]] = "$"

            # Sinon, si l'utilisateur clique sur l'écran alors il commence à dessiner
            elif mouse.pressed(0):
                is_drawing = True
                # Empêche l'utilisateur de cliquer sur plusieurs choses à la fois
                mouse.old_m_pressed[0] = True

        else:
            is_drawing = False


    # Partie affichage


    def display_carte() -> None:
        """Affichage de la carte"""

        # Affichage de toutes les tuiles
        for y in range(dim_carte[1]):
            for x in range(dim_carte[0]):

                # Affichage d'une case vide
                if carte[y][x] == " ":
                    if "sol" in tiles_set[used_tiles_set]:
                        screen.blit(tiles_set[used_tiles_set]["sol"], (x*SIZE, y*SIZE))
                    else:
                        pg.draw.rect(screen, (150, 150, 150), ((x*SIZE, y*SIZE), (SIZE, SIZE)))

                # Affichage d'une case avec un mur
                elif carte[y][x] == "#":
                    if "mur" in tiles_set[used_tiles_set]:
                        screen.blit(tiles_set[used_tiles_set]["mur"], (x*SIZE, y*SIZE))
                    else:
                        pg.draw.rect(screen, (50, 50, 50), ((x*SIZE, y*SIZE), (SIZE, SIZE)))

                # Affichage d'une case avec un fromage
                elif carte[y][x] == "$":
                    if "sol" in tiles_set[used_tiles_set]:
                        screen.blit(tiles_set[used_tiles_set]["sol"], (x*SIZE, y*SIZE))
                    else:
                        pg.draw.rect(screen, (150, 150, 150), ((x*SIZE, y*SIZE), (SIZE, SIZE)))
                    if "fromage" in tiles_set[used_tiles_set]:
                        screen.blit(tiles_set[used_tiles_set]["fromage"], (x*SIZE, y*SIZE))
                    else:
                        pg.draw.circle(screen, (200, 200, 50), (int(SIZE*(x + 0.5)), int(SIZE*(y + 0.5))), SIZE//4)

        # Affichage du point d'apparition
        if "spawn" in tiles_set[used_tiles_set]:
            screen.blit(tiles_set[used_tiles_set]["spawn"], (spawnpoint[0]*SIZE, spawnpoint[1]*SIZE))
        else:
            pg.draw.polygon(screen, (255, 0, 0), ((int((spawnpoint[0] + 0.5)*SIZE), int((spawnpoint[1] + 0.25)*SIZE)), (int((spawnpoint[0] + 0.75)*SIZE), int((spawnpoint[1] + 0.5)*SIZE)), (int((spawnpoint[0] + 0.5)*SIZE), int((spawnpoint[1] + 0.75)*SIZE)), (int((spawnpoint[0] + 0.25)*SIZE), int((spawnpoint[1] + 0.5)*SIZE))))


    def display_AIs() -> None:
        """Affiche les IA (les souris)"""

        # IA n°1
        if AI1_process.is_alive():
            screen.blit(AI1_sprite, (AI1_pos[0]*SIZE, AI1_pos[1]*SIZE))
        # IA n°2
        if AI2_process.is_alive():
            screen.blit(AI2_sprite, (AI2_pos[0]*SIZE, AI2_pos[1]*SIZE))


    def display_count_down(nb: int, progress: int) -> None:
        """Compte à rebour allant de 3 à 1"""

        size = int(progress ** 0.3 * 50)
        focus_screen.blit(pg.transform.smoothscale(count_down[str(nb)].copy(), (size, size)), ((fs_width - size)//2, (fs_height - size)//2))


    def display_GUI() -> None:
        """Affichage du GUI directement sur l'écran d'affichage"""

        # Récupération du temps (avec technique de flemmard pour l'affichage)
        time_txt = "00000" + str(game_time%60000)

        # Affichage du GUI

        # Timer
        surf_time = zoneTexte(f"(255,255,255)${game_time//60000}:{time_txt[-5:-3]}:{time_txt[-3:]}", 3)
        focus_screen.blit(surf_time, ((fs_width - surf_time.get_size()[0])//2, 10))

        # Rajoute le nom à la liste de nom de générateur si il n'est pas déjà entré (donc c'est une carte pré-faite)
        if gen_signature not in GEN_SIGNATURES:
            GEN_SIGNATURES[gen_signature] = zoneTexte(f"(235,185,25)$Carte officielle : $(255,255,255)${gen_signature[11:]}" if gen_signature.startswith("OFFICIEL - ") else f"(180,180,180)$Carte non-officielle : $(255,255,255)${gen_signature}", 2)
        # Signatures de carte (pauvres fous !)
        focus_screen.blit(GEN_SIGNATURES[gen_signature], ((fs_width - GEN_SIGNATURES[gen_signature].get_size()[0])//2, fs_height - GEN_SIGNATURES[gen_signature].get_size()[1] - 10))

        # Nom des équipes
        focus_screen.blit(t1_name, (50, 15))
        focus_screen.blit(t2_name, (fs_width - t2_name.get_size()[0] - 50, 15))
        # Mascote de chaque équipe (en version miniature)
        focus_screen.blit(s_AI1_sprite, (5, 5))
        focus_screen.blit(s_AI2_sprite, (fs_width - 45, 5))

        # Score de chaque équipe
        scores = zoneTexte(f"(255,255,255)$Score : $(255,100,0)${t1_score}$(255,255,255)$ point" + ("s" if t1_score > 1 else "") + " "*20 + f"$(255,255,255)$Score : $(0,150,255)${t2_score} $(255,255,255)$point" + ("s" if t2_score > 1 else ""), 2)
        focus_screen.blit(scores, ((fs_width - scores.get_size()[0])//2, 15))

        # Message de victoire
        # Lorsque tous les fromages ont été récupérés
        if t1_score + t2_score == nb_cheese and not edit and run_AI:
            # Arrière plan du message de victoire
            focus_screen.blit(fs_border, (0, fs_height//2 - fs_border_size[1] - 5))
            focus_screen.blit(fs_border, (0, fs_height//2 - 5))

            # En cas de victoire de l'équipe n°1
            if t1_score > t2_score:
                size = t1_victory.get_size()
                # Message de victoire
                focus_screen.blit(t1_victory, ((fs_width - size[0])//2, (fs_height - size[1])//2))
                # Affichage de l'IA gagante
                focus_screen.blit(AI1_sprite, ((fs_width - size[0])//2 - 96, fs_height//2 - 37))
                focus_screen.blit(AI1_sprite, ((fs_width + size[0])//2 + 32, fs_height//2 - 37))
            # En cas de match nul
            elif t1_score == t2_score:
                size = no_victory.get_size()
                # Message de victoire
                focus_screen.blit(no_victory, ((fs_width - size[0])//2, (fs_height - size[1])//2))
            # En cas de victoire de l'équipe n°2
            else:
                size = t2_victory.get_size()
                # Message de victoire
                focus_screen.blit(t2_victory, ((fs_width - size[0])//2, (fs_height - size[1])//2))
                # Affichage de l'IA gagante
                focus_screen.blit(AI2_sprite, ((fs_width - size[0])//2 - 96, fs_height//2 - 37))
                focus_screen.blit(AI2_sprite, ((fs_width + size[0])//2 + 32, fs_height//2 - 37))

        # Affichage de l'objet gui
        l_gui.display()
        r_gui.display()


    def display() -> None:
        """Affichage de tous les éléments"""

        screen.fill((0, 0, 0))
        focus_screen.fill((0, 0, 0))

        # Affichage de la carte
        display_carte()

        # Affichage des éléments de débugging
        if debug:
            if AI1_process.is_alive():
                pg.draw.rect(screen, (255, 100, 0), ((AI1_true_pos[0]*SIZE, AI1_true_pos[1]*SIZE), (SIZE, SIZE)), 5)
            if AI2_process.is_alive():
                pg.draw.rect(screen, (0, 150, 255), ((AI2_true_pos[0]*SIZE, AI2_true_pos[1]*SIZE), (SIZE, SIZE)), 5)

        # Affichage des IA
        display_AIs()

        # Montre la tuile sélectionnée lorsque le mode éditeur est activé
        if mouse.do_show_tile:
            pg.draw.rect(screen, (255, 255, 255), ((mouse.tile_pos[0]*SIZE, mouse.tile_pos[1]*SIZE), (SIZE, SIZE)), 5)

        # Affichage de l'écran de simulation sur l'écran d'affichage
        focus_screen.blit(pg.transform.smoothscale(screen, screen_zoom_size) if HD_display else pg.transform.scale(screen, screen_zoom_size), screen_pos)

        # Affichage du compte à rebours si nécessaire
        if do_count_down:
            time_since_start = game_start - game_true_start
            if 0 < time_since_start < 3000 and not nb_cheese == t1_score + t2_score:
                display_count_down(3 - time_since_start//1000, time_since_start%1000)

        # Bandes semi-transparantes affichées en haut et en bas de l'écran
        focus_screen.blit(fs_border, (0, 0))
        focus_screen.blit(fs_border, (0, fs_height - fs_border_size[1]))

        # Affichage des informations directement sur l'écran d'affichage
        display_GUI()

        # Affichage à l'écran
        pg.display.flip()


    def vs_screen() -> None:
        """Affiche jusqu'à ce qu'une touche soit pressée l'écran "Versus" (bloque les autres processus)"""

        # Variable globale
        global running

        # Affichage de l'arrière plan
        focus_screen.blit(vs_background, (0, 0))
        # Affichage de la bannière de l'équipe n°1
        focus_screen.blit(t1_banner, ((fs_width//2 - t1_banner_size[0])//2, (fs_height - t1_banner_size[1])//2))
        # Affichage de la bannière de l'équipe n°2
        focus_screen.blit(t2_banner, ((3*fs_width//2 - t2_banner_size[0])//2, (fs_height - t2_banner_size[1])//2))
        # Affichage du premier plan
        focus_screen.blit(vs_foreground, (0, 0))

        # Texte indiquant qu'il faut appuyer sur une touche pour continuer
        text = zoneTexte("(255,255,255)$Appuyez sur n'importe quelle touche pour continuer...", 3)
        focus_screen.blit(text, ((fs_width - text.get_size()[0])//2, fs_height - 50))

        # Actualisation unique de l'écran (l'image affichée ne change pas)
        pg.display.flip()

        # Boucle secondaire
        while running:

            # Récupération de tous les évènements pygame
            for event in pg.event.get():

                # Quitter le script
                if event.type == pg.QUIT:
                    running = False

                # Touche pressée
                elif event.type == pg.KEYDOWN:

                    # Quitter le script
                    if event.key == pg.K_ESCAPE:
                        running = False

                    # Si n'importe quelle touche est pressée, ferme l'écran "Versus"
                    return None


    # Partie relancement


    def relauch(map_size: tuple|None=None) -> None:
        """Relance le programme rapidement et recréer la carte"""

        # Variables globales
        global t1_score, t2_score, game_time, game_start, game_true_start

        # Recharge la carte
        re_init(map_size)
        if map_size is None:
            generate_carte()
        # Réset les scores
        t1_score = 0
        t2_score = 0
        # Réset du chronomètre
        game_true_start = game_start = pg.time.get_ticks()
        game_time = 0
        # Relance les IA si le mode édition n'est pas activé
        if not edit and run_AI:
            reboot_AI()


    # Partie boucle principale


    def main() -> None:
        """Boucle principale"""

        # Variables globales utilisées
        global running, keys_pressed, game_time, game_start, game_true_start, dt

        # Dictionnaire permettant de convertir les touches qui ne sont pas des charactères en chaine de charactères
        special_keys = {
            pg.K_RETURN: "RETURN",
            pg.K_BACKSPACE: "BACKSPACE"
        }

        # Génartion initiale de la carte
        relauch()

        # Impulse pour run les IA
        AI_run_impulse_needed = True

        # Boucle principale
        while running:

            # Actualisation du delta-temps
            dt = clock.tick()

            # # Si le match n'a pas encore commencé
            # if game_time == 0:
            #      pg.time.get_ticks()

            # Reset du timer si les 2 IA ne sont pas prêtes
            if not(com_in_AIs[7] and com_in_AIs[8] and (AI1_process.is_alive() or AI2_process.is_alive())) or edit:
                game_true_start = game_start = pg.time.get_ticks()
                game_time = 0
                AI_run_impulse_needed = True

            # Pause du timer si le match est fini
            elif nb_cheese == t1_score + t2_score:
                game_start += dt

            # Attente de 3 secondes au début du match pour le compte à rebours
            elif game_start < game_true_start + 3000 and do_count_down:
                game_start = pg.time.get_ticks()

            # Lancement des IA
            elif AI_run_impulse_needed:
                AI_run_impulse_needed = False
                com_in_AIs[3] = com_in_AIs[4] = True
                game_time = pg.time.get_ticks() - game_start

            # Actualisation du temps par défaut
            else:
                game_time = pg.time.get_ticks() - game_start

            # Actualisation des données de la souris (du curseur)
            mouse.update()

            # Réset de la liste des touches pressées
            keys_pressed = []

            # Récupération de tous les évènements pygame
            for event in pg.event.get():

                # Quitter le script
                if event.type == pg.QUIT:
                    running = False

                # Touche pressée
                elif event.type == pg.KEYDOWN:

                    # Quitter le script
                    if event.key == pg.K_ESCAPE:
                        running = False

                    # Touche pour recréer une map
                    elif event.key == pg.K_ASTERISK:
                        relauch()

                    # Ajout des touches pressées dans une liste globale
                    if event.key in special_keys:
                        keys_pressed.append(special_keys[event.key])
                    elif str(event.unicode) in POLICE:
                        keys_pressed.append(event.unicode)

            # Mise à jour de l'interface
            l_gui.update()
            r_gui.update()

            update_carte()

            # Gestion des IA (input/output)
            update_AI(com_in_AIs[7] and com_in_AIs[8] and (AI1_process.is_alive() or AI2_process.is_alive()) and (game_start >= game_true_start + 3000 or not do_count_down) and nb_cheese != t1_score + t2_score)

            # Affichage de tous les éléments
            display()



#>-----------------------------< Mise en place >------------------------------<#


    pg.init() # Initialisation de pygame


    """
    Explications rapides :

    La surface "focus_screen" est l'écran d'affichage. A chaque frame, "screen" est dessinée, centrée et redimmensionnée sur "focus_screen". "focus_screen" est adaptée automatiquement à la taille de l'écran (plein écran).

    La surface "screen" est la surface sur laquelle la simulation tourne. Sa taille ne varie que en fonction de la taille de la map.

    Toutes les variables définies ci-dessous (sauf les constantes, la partie "focus_screen" et "gen_signature") sont définies temporairement, et voient leurs valeurs remplacées par la fonction "re_init()".

    Si vous voullez créer votre propre génération de map, entrez clé et surface dans "GEN_SIGNATURES", allez dans "generate_carte" et créez votre propre générateur d'enfer sur Terre !
    """


    # Affichage d'éléments de débug et log d'informations dans la console (ralenti légèrement la vitesse d'exécution des IA)
    debug = False

    # Mode éditeur
    edit = False

    # Indique si il faut lancer les IA ou non
    run_AI = False

    # Si vous souhaitez signer vos attrocitées ($ = séparateur couleur-texte)
    GEN_SIGNATURES = {
        # Générations dites "Classiques"
        "Defaut": zoneTexte("(255,255,255)$Nom : $(180,180,180)$Labyrinthe classique  $(255,255,255)$-  Auteur : $(180,180,180)$Classique", 2),
        "Blocks": zoneTexte("(255,255,255)$Nom : $(255,255,0)$Block-Land  $(255,255,255)$-  Auteur : $(180,180,180)$Classique", 2),
        # Générations par "Térence"
        "PYRAT": zoneTexte("(255,255,255)$Nom : $(235,185,25)$Génération officielle de PYRAT édition Deluxe  $(255,255,255)$-  Auteur : $(235,185,25)$Térence", 2),
        "Points": zoneTexte("(255,255,255)$Nom : $(180,255,180)$Les petits points  $(255,255,255)$-  Auteur : $(235,185,25)$Térence", 2),
        "Ter1": zoneTexte("(255,255,255)$Nom : $(180,255,180)$Simplicité  $(255,255,255)$-  Auteur : $(235,185,25)$Térence", 2),
        "Ter2": zoneTexte("(255,255,255)$Nom : $(255,100,255)$Murs sans fins  $(255,255,255)$-  Auteur : $(235,185,25)$Térence", 2),
        "Ter3": zoneTexte("(255,255,255)$Nom : $(255,0,0)$Les couloirs de la douleur  $(255,255,255)$-  Auteur : $(235,185,25)$Térence", 2),
        # Génération sugérée par le grand MANDIC
        "Vide": zoneTexte("(255,255,255)$Nom : $(255,120,0)$L'arène  $(255,255,255)$-  Auteur : $(170,15,0)$L'héritier de Saitama", 2)
    }

    SIZE = 64 # Taille d'une tuile avant zoom/dézoom

    # Dictionnaire des mouvement (et donc outputs) possibles (utilisé par "generate_wall")
    MOVE = {
        "H": (0, -1),
        "B": (0, 1),
        "D": (1, 0),
        "G": (-1, 0)
    }

    keys_pressed = []

    # Surfaces représentants le nom des équipes (nom de fichier)
    t1_name = zoneTexte(f"(155,66,0)$Equipe n°1 : $(255,100,0)${team_1.replace('_', ' ')}", 2)
    t2_name = zoneTexte(f"(0,100,155)$Equipe n°2 : $(0,150,255)${team_2.replace('_', ' ')}", 2)

    t1_victory = zoneTexte(f"(235,185,25)$L'équipe n°1 $(255,100,0)${team_1.replace('_', ' ')} $(235,185,25)$remporte la victoire !", 3)
    t2_victory = zoneTexte(f"(235,185,25)$L'équipe n°2 $(0,150,255)${team_2.replace('_', ' ')} $(235,185,25)$remporte la victoire !", 3)
    no_victory = zoneTexte(f"(235,185,25)$Match nul !", 3)

    # Permet de timer de delta-temps entre chaque frame (en ms)
    clock = pg.time.Clock()
    dt = 0

    # Dimmensions de la carte (en tuiles) par défaut
    dim_carte = (24, 24)
    # Taille de la carte (en pixels)
    size_carte = (dim_carte[0]*SIZE, dim_carte[1]*SIZE)
    # Carte par défaut (sans les murs centraux) avec 2 de largeur en mur extérieurs
    carte = [[" " if x not in [0, 1, dim_carte[0] - 1, dim_carte[0] - 2] and y not in [0, 1, dim_carte[1] - 1, dim_carte[1] - 2] else "#" for x in range(dim_carte[0])] for y in range(dim_carte[1])]
    # Nombre total de fromage à rammasser
    nb_cheese = 0
    # Point d'apparition
    spawnpoint = (2, 2)

    # Nom du générateur + auteur :)
    gen_signature = "Defaut"

    # Nom et icone de la fenêtre
    pg.display.set_caption("PYRAT Deluxe - v1.4.8")
    pg.display.set_icon(load_img(f"ressources/images/icone.png", (256, 256)))

    # Taille de l'écran d'affichage
    fs_width, fs_height = pg.display.Info().current_w, pg.display.Info().current_h
    # fs_width, fs_height = 500, 500 # Si l'on veux déactiver le full-screen
    # Ecran d'affichage
    focus_screen = pg.display.set_mode((fs_width, fs_height))

    # Ecran de simulation
    screen = pg.surface.Surface(size_carte)
    # Taille de l'écran de simulation lorsque redimmentionné
    screen_zoom_size = (fs_width, int(size_carte[1]*fs_width/size_carte[0])) if fs_width/size_carte[0] < fs_width/size_carte[1] else (int(size_carte[0]*fs_height/size_carte[1]), fs_height)
    # Position de l'écran de simulation lorsqu'affiché
    screen_pos = ((fs_width - screen_zoom_size[0])//2, (fs_height - screen_zoom_size[1])//2)

    # Bordure semi-transparante de l'écran s'affichage
    fs_border_size = (fs_width, 51)
    fs_border = pg.surface.Surface(fs_border_size)
    fs_border.fill((255, 255, 255))
    for y in range(fs_border_size[1]):
        for x in range(fs_border_size[0]):
            if (x + y)%3 != 0:
                pg.draw.rect(fs_border, (0, 0, 0), ((x, y), (1, 1)))
    fs_border.set_colorkey((255, 255, 255))

    # Affichage en HD (consomme BEAUCOUP de ressources)
    HD_display = False

    # Affichage de l'écran "Versus" en début de match
    do_vs_screen = True
    # Arrière plan de l'écran "Versus"
    vs_background = load_img("ressources/images/combat/ecran_vs/background.png", (fs_width, fs_height))
    # Premier plan de l'écran "Versus"
    vs_foreground = load_img("ressources/images/combat/ecran_vs/foreground.png", (fs_width, fs_height))

    # Chronomètre du temps de jeu (utilisé dans le calcul du temps total)
    game_time = 0
    # Momment auquel la partie a commencé (utilisé dans le calcul du temps total)
    game_start = 0
    # Momment auquel la partie a commencé (pour de vrai)
    game_true_start = 0

    # Condition pour que le compte à rebour avant le début du match soit fait
    do_count_down = True

    # Set de tuile [<nom_set_tuiles>][<nom_tuile>] (seulement des png)
    tiles_set = {folder: {file[:-4]: load_img(f"ressources/images/set_tuiles/{folder}/{file}", (SIZE, SIZE)) for file in listdir(f"ressources/images/set_tuiles/{folder}") if file.endswith(".png")} for folder in listdir("ressources/images/set_tuiles")}
    # Set de tuile utilisé ("none" = pas de textures)
    used_tiles_set = "defaut"

    # Type de tuile sélectionnée dans l'éditeur
    selected_tile = "mur"

    # Si l'utilisateur est en train de dessiner sur la carte
    is_drawing = False

    # Chargement des sprites pour le compte à rebours
    count_down = {file[:-4]: load_img(f"ressources/images/combat/compte/{file}", (192, 192)) for file in listdir("ressources/images/combat/compte") if file.endswith(".png")}

    # Sprites des IA (souris) + contours
    # Taille des contours (proportionnels)
    outline_size = 1.1
    # Sprite de l'IA n°1
    AI1_sprite_path = f"participants/{team_1}/custom/souris.png"
    try:
        # Si le sprite "souris.png" existe et est placé au bon endroit
        AI1_sprite = load_img(AI1_sprite_path, (SIZE, SIZE)).convert_alpha()
    except FileNotFoundError:
        # Sinon, on met le sprite par défaut
        AI1_sprite_path = "ressources/participant_par_defaut/custom/souris.png"
        AI1_sprite = load_img(AI1_sprite_path, (SIZE, SIZE)).convert_alpha()
    # Mise en place des contours du sprite de l'IA n°1
    for y in range(SIZE):
        for x in range(SIZE):
            pixel = AI1_sprite.get_at((x, y))
            if pixel[3] != 0:
                AI1_sprite.set_at((x, y), (255, 100, 0, pixel[3]))
    AI1_sprite.blit(pg.transform.smoothscale(AI1_sprite, (int(SIZE / outline_size ** 2), int(SIZE / outline_size ** 2))), (int(SIZE * (outline_size - 1)), int(SIZE * (outline_size - 1))))
    AI1_sprite.blit(load_img(AI1_sprite_path, (int(SIZE / outline_size ** 1), int(SIZE / outline_size ** 1))), ((SIZE * (outline_size - 1))//2, (SIZE * (outline_size - 1))//2))
    # Sprite de l'IA n°2
    AI2_sprite_path = f"participants/{team_2}/custom/souris.png"
    try:
        # Si le sprite "souris.png" existe et est placé au bon endroit
        AI2_sprite = load_img(AI2_sprite_path, (SIZE, SIZE)).convert_alpha()
    except FileNotFoundError:
        # Sinon, on met le sprite par défaut
        AI2_sprite_path = "ressources/participant_par_defaut/custom/souris.png"
        AI2_sprite = load_img(AI2_sprite_path, (SIZE, SIZE)).convert_alpha()
    # Mise en place des contours du sprite de l'IA n°2
    for y in range(SIZE):
        for x in range(SIZE):
            pixel = AI2_sprite.get_at((x, y))
            if pixel[3] != 0:
                AI2_sprite.set_at((x, y), (0, 150, 255, pixel[3]))
    AI2_sprite.blit(pg.transform.smoothscale(AI2_sprite, (int(SIZE / outline_size ** 2), int(SIZE / outline_size ** 2))), (int(SIZE * (outline_size - 1)), int(SIZE * (outline_size - 1))))
    AI2_sprite.blit(load_img(AI2_sprite_path, (int(SIZE / outline_size ** 1), int(SIZE / outline_size ** 1))), ((SIZE * (outline_size - 1))//2, (SIZE * (outline_size - 1))//2))

    # Sprite miniature de l'IA n°1
    s_AI1_sprite = pg.transform.smoothscale(AI1_sprite.copy(), (40, 40))
    # Sprite miniature de l'IA n°2
    s_AI2_sprite = pg.transform.smoothscale(AI2_sprite.copy(), (40, 40))

    # Bannière d'équipe
    # De l'équipe n°1
    t1_banner_path = f"participants/{team_1}/custom/banniere.png"
    try:
        # Si le sprite "banniere.png" existe et est placée au bon endroit
        t1_banner_size = load_img(t1_banner_path).get_size()
    except FileNotFoundError:
        # Sinon, on met la bannière par défaut
        t1_banner_path = "ressources/participant_par_defaut/custom/banniere.png"
        t1_banner_size = load_img(t1_banner_path).get_size()
    t1_banner = load_img(t1_banner_path, (fs_width//2, int(t1_banner_size[1] / t1_banner_size[0] * (fs_width//2))) if t1_banner_size[0] / (fs_width//2) > t1_banner_size[1] / fs_height else (int(t1_banner_size[0] / t1_banner_size[1] * fs_height), fs_height))
    t1_banner_size = t1_banner.get_size()
    # De l'équipe n°2
    t2_banner_path = f"participants/{team_2}/custom/banniere.png"
    try:
        # Si le sprite "banniere.png" existe et est placée au bon endroit
        t2_banner_size = load_img(t2_banner_path).get_size()
    except FileNotFoundError:
        # Sinon, on met la bannière par défaut
        t2_banner_path = "ressources/participant_par_defaut/custom/banniere.png"
        t2_banner_size = load_img(t2_banner_path).get_size()
    t2_banner = load_img(t2_banner_path, (fs_width//2, int(t2_banner_size[1] / t2_banner_size[0] * (fs_width//2))) if t2_banner_size[0] / (fs_width//2) > t2_banner_size[1] / fs_height else (int(t2_banner_size[0] / t2_banner_size[1] * fs_height), fs_height))
    t2_banner_size = t2_banner.get_size()

    # Cerveau des IA
    # IA n°1
    try:
        # Si le fichier "main.py" existe et est placé au bon endroit
        exec(f"from participants.{team_1}.main import main as AI1_brain")
    except (ModuleNotFoundError, SyntaxError):
        # IA par défaut (ne fait rien)
        from ressources.participant_par_defaut.main import main as AI1_brain
    # IA n°2
    try:
        # Si le fichier "main.py" existe et est placé au bon endroit
        exec(f"from participants.{team_2}.main import main as AI2_brain")
    except (ModuleNotFoundError, SyntaxError):
        # IA par défaut (ne fait rien)
        from ressources.participant_par_defaut.main import main as AI2_brain

    # Position des IA
    AI1_pos = (0, 0)
    AI2_pos = (0, 0)
    # Score des IA
    t1_score = 0
    t2_score = 0

    # Variables de debug
    AI1_true_pos = (0, 0) # Position à laquelle l'IA n°1 pense être
    AI2_true_pos = (0, 0) # Position à laquelle l'IA n°2 pense être

    # Définition du type de méthode utilisé pour le multi-processing
    mp.set_start_method('spawn')

    # Fils de communications avec les intéligences artificielles
    # Que représente chaque élément de "com_in_AIs" ?
    # N°0 -> list  : la carte
    # N°1 -> tuple : la position de l'IA n°1
    # N°2 -> tuple : la position de l'IA n°2
    # N°3 -> bool  : si l'IA n°1 à l'autorisation de s'exécuter
    # N°4 -> bool  : si l'IA n°2 à l'autorisation de s'exécuter
    # N°5 -> tuple : là où pense être l'IA n°1 (débug)
    # N°6 -> tuple : là où pense être l'IA n°2 (débug)
    # N°7 -> bool  : si l'IA n°1 est prête
    # N°8 -> bool  : si l'IA n°1 est prête
    com_in_AIs = mp.Manager().list([[[[" "]]], (0, 0), (0, 0), False, False, (-1, -1), (-1, -1), False, False])
    com_out_AI1 = mp.Queue()
    com_out_AI2 = mp.Queue()

    # Création des fils de code séparés pour les IA
    AI1_process = mp.Process(target=AI_controler, args=(com_in_AIs, com_out_AI1, AI1_brain, 1))
    AI2_process = mp.Process(target=AI_controler, args=(com_in_AIs, com_out_AI2, AI2_brain, 2))

    # Création d'une instance de l'objet Curseur
    mouse = Cursor()

    # Création d'un objet Interface
    l_gui = Interface()
    r_gui = Interface(True)

    running = True
    main() # Fonction principale

    # Arret de force des processus d'IA
    kill_AI()


    pg.quit() # Arret de pygame





################################################################################
#>---------------< Eléments propres aux processus secondaires >---------------<#
################################################################################




# Partie exécuté seulement si ce processus n'est pas le principal (et donc une IA)
else:


#---------------------------< Imports des modules >----------------------------#


    from timeit import default_timer as timer # Utilisé pour brider la vitesse des IA



#>------------------------< Définition de variables >-------------------------<#

    # Valeur par laquelle est divisée la vitesse d'exécution des IA
    AI_SLOW_FACTOR = 1e3 # Vitesse actuellement divisée par 1000, soit 0.1% de la vitesse originale
    # Temps (en ms) d'attente minimal entre chaque exécution des IA (peut être égal à 0)
    MIN_WAIT = 0