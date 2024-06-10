Crédits :

Script réalisé par DE SAINT LEGER Térence en classe de Tle 7 Hélios durant l'année scolaire 2022 - 2023 à Pétrelle (Rocroy St Vincent de Paul).
Merci à BLANDIN Anatole en classe de Tle 7 Hélios d'avoir créé plusieurs cartes officileles et plusieurs sets de tuiles.



Infos :

Bienvenu sur PYRAT - Edition Deluxe (v1.4.8).
L'objectif est de récupérer le plus de fromages avant l'autre souris.

La carte se présente sous une forme de liste de liste de string.

Chaque charactère représente un élément différent :
    " " = un espace vide
    "#" = un mur
    "$" = un fromage, avec un espace vide en dessous

La carte est générée procéduralement, elle est donc aléatoire.
Pour autant, quelques cartes invariables seront utilisées lors de la compétition.
Les textures utilisée sont également aléatoires, mais n'ont aucun impact sur la carte.

Le fichier "update_log.txt" vous donnera toutes les informations sur les dernières mises à jour.



Le IA :

Votre IA doit être contenu dans un fichier python nommé main.
Votre fichier doit contnir une fonction nommée main.
Celle-ci sera exécutée par le script principal.

Chaque IA reçoit (et doit obligatoirment accepter) :
    - le labyrinthe sous forme de liste de liste de string
    - sa position (en tuiles) sous forme de tuple
    - la position de son adversaire (en tuiles) sous forme de tuple

Elles doivent retourner l'un des 5 élément suivant :
    - "H" pour avancer vers le HAUT (si possible)
    - "B" pour avancer vers le BAS (si possible)
    - "D" pour avancer vers la DROITE (si possible)
    - "G" pour avancer vers la GAUCHE (si possible)
    - None ou autre pour ne rien faire (None vivement conseillé)

Tout autre output ne sera pas accepté.

Vos IA seront bridées et verront leur vitesse d'exécution divisée par 1000, soit une vitesse de 0.1% par rapport à la vitesse originale.
Cette valeur sera modifiée le jour de la compétion en fonction des envies des participants.
La vitesse maximale de votre IA est limité par les performances de votre ordinateur.
Pour autant, cela ne devrait pas vous gèner, même avec un script très rapide.

VOTRE IA NE DOIT PAS CRASHER !
Dans le cas échéant, elle cessera de fonctionner (incroyable n'est-ce pas).



Fichiers équipe :

Votre nom de fichier ne peut contenir que des charactères alpha-décimaux, des accents et le symbole "_" qui sera afficher comme un " " durant le match.
Définissez votre fichier "main.py", puis un dossier "custom" dans lequel vous mettrez un sprite "souris.png" (1:1) représentant votre souris, puis un fichier "banniere.png" (8:9) qui représente la banière de votre équipe.
Dans ce fichier "main.py", définissez une fonction "main" prenant 3 arguments :
    - le labyrinthe sous forme list[list[str]]
    - la position de votre IA sous forme tuple[int, int]
    - la position de l'IA ennemie sous forme tuple[int, int]
Elle devra retourner :
    - "H" pour avancer vers le HAUT (si possible)
    - "B" pour avancer vers le BAS (si possible)
    - "D" pour avancer vers la DROITE (si possible)
    - "G" pour avancer vers la GAUCHE (si possible)
    - None ou autre pour ne rien faire (None vivement conseillé)



Racourcis claviers :

ECHAP -----> Quitter
ASTERISK --> Regénérer aléatoirement le labyrinthe (recharge également les IA)



Conseilles pratiques :

Pour désactiver l'une des IA, mettez un nom de fichier participant n'existant pas.
Les dossiers d'équipe doivent-être valides pour que le code puisse fonctionner.
Sauvegardez vos map sous aux moins 2 noms au cas où.



Règlement du tournoi :

INTERDICTION D'IMPORTER DES LIBRAIRIES OU DES MODULE !
Seules exceptions sont les fichiers fait par vous même en python (.py) ou format textuel (.txt, .csv) ainsi que les modules "random" et "time".
Interdiction pûre et dure de saboter l'IA adverse en affectant sa vitesse ou son code source.
Interdiction d'essayer de modifier les valeurs du code principal (vous pouvez les modifiers localement, mais c'est tout).
LE PLAGIAT INTERNET C'EST EXCLUSION DE LA COMPETITION !
Gentleman rule : On ne hack pas le PC faisant tourner la compétition, merci.



Contribution et suggestions :

N'hésitez pas à contribuer au projet PYRAT !
Vous pouvez créer votre propre système de génération de carte.
Vous pouvez créer vos propres textures.
Envoyez-les moi si vous voulez que je les ajoutes.
Je prends également toutes les suggestions.
Avec le nouvel éditeur de carte, je vous propose de créer des maps officielles pour le tournoi.



Réclamations et questions :

Vous n'êtes pas satisfait de l'une des règles définies ?
Vous haïssez profondément une carte ou jeu de texture ?
Une question sur le tournois et ses règles/fonctionnement ?
Contactez moi pour en parler.



BONNE CHANCE A TOUS !