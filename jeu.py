# Définition des pièces
VIDE = ' '
BLANC = 'B'
NOIR = 'N'
DAME_BLANC = 'DB'
DAME_NOIR = 'DN'

# Création d'un plateau de jeu 8x8 avec des pièces aux positions de départ
plateau = [
    [VIDE, BLANC, VIDE, BLANC, VIDE, BLANC, VIDE, BLANC],
    [BLANC, VIDE, BLANC, VIDE, BLANC, VIDE, BLANC, VIDE],
    [VIDE, BLANC, VIDE, BLANC, VIDE, BLANC, VIDE, BLANC],
    [VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE],
    [VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE],
    [NOIR, VIDE, NOIR, VIDE, NOIR, VIDE, NOIR, VIDE],
    [VIDE, NOIR, VIDE, NOIR, VIDE, NOIR, VIDE, NOIR],
    [NOIR, VIDE, NOIR, VIDE, NOIR, VIDE, NOIR, VIDE]
]

# Fonction pour effectuer un mouvement
def effectuer_mouvement(plateau, depart, arrivee):
    x_dep, y_dep = depart
    x_arr, y_arr = arrivee

    piece = plateau[x_dep][y_dep]

    # Vérifier si la case de départ est occupée par une pièce du joueur actif
    if (piece == BLANC or piece == DAME_BLANC) and x_dep > x_arr:
        return False  # Les pièces blanches se déplacent vers le haut
    elif (piece == NOIR or piece == DAME_NOIR) and x_dep < x_arr:
        return False  # Les pièces noires se déplacent vers le bas

    # Calculer la distance de déplacement en lignes et en colonnes
    delta_x = abs(x_arr - x_dep)
    delta_y = abs(y_arr - y_dep)

    # Vérifier si le mouvement est diagonal d'une case
    if delta_x != 1 or delta_y != 1:
        return False

    # Vérifier si la case d'arrivée est vide
    if plateau[x_arr][y_arr] != VIDE:
        return False

    # Déplacer la pièce
    plateau[x_arr][y_arr] = piece
    plateau[x_dep][y_dep] = VIDE

    # Gérer la promotion en dame
    if (piece == BLANC and x_arr == 0) or (piece == NOIR and x_arr == 7):
        plateau[x_arr][y_arr] = DAMES_BLANC if piece == BLANC else DAMES_NOIR

    return True

# Fonction pour effectuer une prise multiple
def prise_multiple(plateau, depart):
    x_dep, y_dep = depart
    piece = plateau[x_dep][y_dep]

    prises_possibles = []

    # Déplacement possible pour les prises en série
    deplacements = [(2, 2), (2, -2), (-2, 2), (-2, -2)]

    for dx, dy in deplacements:
        x_mid, y_mid = x_dep + dx // 2, y_dep + dy // 2
        x_arr, y_arr = x_dep + dx, y_dep + dy

        if 0 <= x_arr < 8 and 0 <= y_arr < 8 and plateau[x_arr][y_arr] == VIDE and \
                plateau[x_mid][y_mid] != VIDE and plateau[x_mid][y_mid] != piece:
            prises_possibles.append((x_arr, y_arr))

    return prises_possibles

# Afficher le plateau de jeu initial
def afficher_plateau(plateau):
    print("   0  1  2  3  4  5  6  7")
    print("  +-----------------------+")
    for i, ligne in enumerate(plateau):
        ligne_str = str(i) + " |"
        for case in ligne:
            ligne_str += " " + case + " |"
        print(ligne_str)
        print("  +-----------------------+")

# Exemple de mouvement
depart = (5, 0)
arrivee = (3, 2)

if effectuer_mouvement(plateau, depart, arrivee):
    print("Mouvement valide.")
    afficher_plateau(plateau)
else:
    print("Mouvement invalide.")

# Exemple de prise multiple (saut en série)
depart = (3, 2)
prises_possibles = prise_multiple(plateau, depart)

if prises_possibles:
    print("Prises multiples possibles depuis la position (3, 2):", prises_possibles)
else:
    print("Aucune prise multiple possible depuis la position (3, 2).")

