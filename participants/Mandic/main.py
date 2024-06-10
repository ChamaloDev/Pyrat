from typing import List, Tuple

# Tests à effectuer : Haut, Bas, Droite, Gauche
MOVE = {
    "H": (0, -1),
    "B": (0, 1),
    "D": (1, 0),
    "G": (-1, 0)
}
# Version alternative
DIRECTION = (
    ("H", (0, -1)),
    ("B", (0, 1)),
    ("D", (1, 0)),
    ("G", (-1, 0))
)

# Itinéraire à suivre
path = []

def main(maze: List[List[str]], pos_self: Tuple[int, int], pos_enemy: Tuple[int, int]) -> str:

    # Si un itinéraire à déjà été trouvé
    if path != []:
        # Iténéraire sous forme de PILE
        return path.pop()

    # Liste des positions à tester (Dijktra)
    list_pos = (pos_self,)
    # Rien ne sert de trouver un itinéraire pour revenir au point de départ
    maze[pos_self[1]][pos_self[0]] = "."

    # La condition du while permet d'arrèter le calcul si aucune solution n'est trouvée
    while True:
        next_list_pos = []

        # Pour chaque position avec un test actif
        for pos in list_pos:

            # Tous les tests sont effectuées
            for move, delta in DIRECTION:
                new_pos = (pos[0] + delta[0], pos[1] + delta[1])

                # Détection du contenu de la tuile
                match maze[new_pos[1]][new_pos[0]]:

                    # Si la tuile est un espace vide
                    case " ":
                        # On répertorie sur cette tuile d'où l'on vient (Dijktra)
                        maze[new_pos[1]][new_pos[0]] = move
                        # On ajoute cette tuile à la liste de position active
                        next_list_pos.append(new_pos)

                    # Si la tuile est une fromage (Yay !)
                    case "$":
                        # On répertorie sur cette tuile d'où l'on vient (Dijktra)
                        path.append(move)
                        # On backtrack jusqu'au point de départ
                        pos = (new_pos[0] - MOVE[move][0], new_pos[1] - MOVE[move][1])
                        while pos != pos_self:
                            # Là d'où on vient
                            move = maze[pos[1]][pos[0]]
                            # Ajout de cette provenance à l'itinéraire
                            path.append(move)
                            # On se déplace (en marche arrière)
                            pos = (pos[0] - MOVE[move][0], pos[1] - MOVE[move][1])

                        # Return de la première (dernière ajouté) étape de l'itinéraire et on la retire
                        return path.pop()

        # Nouvelles positions
        list_pos = tuple(next_list_pos)
