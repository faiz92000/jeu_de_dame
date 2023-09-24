import tkinter as tk
from tkinter import messagebox

# Définition des pièces
VIDE = ' '
BLANC = 'B'
NOIR = 'N'
DAME_BLANC = 'DB'
DAME_NOIR = 'DN'

# Déclaration et initialisation des variables
depart = None
arrivee = None
joueur_actif = BLANC  # Vous pouvez commencer par les blancs


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
        plateau[x_arr][y_arr] = DAME_BLANC if piece == BLANC else DAME_NOIR

    return True
# Fonction pour effectuer une prise multiple
def prise_multiple(plateau, depart):
    x_dep, y_dep = depart
    piece = plateau[x_dep][y_dep]
    prises_possibles = []

    # Déplacements possibles pour les prises en série
    deplacements = [(2, 2), (2, -2), (-2, 2), (-2, -2)]

    for dx, dy in deplacements:
        x_mid, y_mid = x_dep + dx // 2, y_dep + dy // 2
        x_arr, y_arr = x_dep + dx, y_dep + dy

        if 0 <= x_arr < 8 and 0 <= y_arr < 8 and plateau[x_arr][y_arr] == VIDE and \
           plateau[x_mid][y_mid] != VIDE and plateau[x_mid][y_mid] != piece:
            prises_possibles.append((x_arr, y_arr))

    return prises_possibles

# Fonction pour afficher le plateau de jeu dans la GUI
def afficher_plateau_gui():
    for i in range(8):
        for j in range(8):
            piece = plateau[i][j]
            case = tk.Label(root, text=piece, width=3, height=1)
            case.grid(row=i, column=j)

# Fonction pour gérer le clic sur une case du plateau
# Fonction pour gérer le clic sur une case du plateau
def gestion_clic(i, j):
    global depart
    global arrivee
    global joueur_actif

    # Si le joueur a déjà sélectionné la case de départ, c'est maintenant la case d'arrivée
    if depart is not None:
        arrivee = (i, j)
        # Vérifier si le mouvement est valide
        if effectuer_mouvement(plateau, depart, arrivee):
            # Réinitialiser les cases de départ et d'arrivée
            depart = None
            arrivee = None
            # Actualiser l'affichage du plateau
            afficher_plateau_gui()
            # Vérifier si la partie est terminée
            resultat = fin_de_partie(plateau)
            if resultat:
                messagebox.showinfo("Fin de la partie", f"Le joueur {resultat} gagne la partie!")
                root.quit()  # Fermer la GUI après la fin de la partie
            elif impasse(plateau, joueur_actif):
                messagebox.showinfo("Impasse", "La partie se termine par une impasse!")
                root.quit()  # Fermer la GUI en cas d'impasse
            # Changer de joueur actif
            joueur_actif = NOIR if joueur_actif == BLANC else BLANC
        else:
            messagebox.showerror("Mouvement invalide", "Mouvement invalide. Réessayez.")
            depart = None
            arrivee = None
    else:
        # Si le joueur n'a pas encore sélectionné la case de départ, c'est la case de départ
        depart = (i, j)


# Fonction pour vérifier la fin de la partie
def fin_de_partie(plateau):
    blancs_restants = 0
    noirs_restants = 0

    for ligne in plateau:
        for case in ligne:
            if case == BLANC or case == DAME_BLANC:
                blancs_restants += 1
            elif case == NOIR or case == DAME_NOIR:
                noirs_restants += 1

    if blancs_restants == 0:
        return "Noir"  # Les blancs ont été éliminés, les noirs gagnent
    elif noirs_restants == 0:
        return "Blanc"  # Les noirs ont été éliminés, les blancs gagnent

    return None  # La partie n'est pas encore terminée

# Fonction pour vérifier s'il y a une impasse (stalemate)
def impasse(plateau, joueur_actif):
    # Vérifier si le joueur actif a des mouvements légaux
    for i in range(8):
        for j in range(8):
            if plateau[i][j] == joueur_actif or plateau[i][j] == joueur_actif.upper():
                # Vérifier si des mouvements légaux sont possibles pour cette pièce
                if mouvements_legaux_disponibles(plateau, (i, j)):
                    return False  # Il y a au moins un mouvement légal, pas d'impasse

    # Vérifier si le joueur actif peut effectuer une prise légale (prise multiple)
    for i in range(8):
        for j in range(8):
            if plateau[i][j] == joueur_actif or plateau[i][j] == joueur_actif.upper():
                prises_possibles = prise_multiple(plateau, (i, j))
                if prises_possibles:
                    return False  # Il y a au moins une prise légale, pas d'impasse

    return True  # Aucun mouvement légal ni prise légale n'est disponible, impasse

# Fonction pour vérifier si des mouvements légaux sont disponibles pour une pièce
def mouvements_legaux_disponibles(plateau, position):
    x, y = position
    piece = plateau[x][y]

    mouvements_legaux = []

    # Vérification des mouvements simples
    if piece == BLANC or piece == DAME_BLANC:
        # Vérifier les mouvements simples pour les pièces blanches
        # (vers le haut de la grille)
        if x - 1 >= 0:
            if y - 1 >= 0 and plateau[x - 1][y - 1] == VIDE:
                mouvements_legaux.append((x - 1, y - 1))
            if y + 1 < 8 and plateau[x - 1][y + 1] == VIDE:
                mouvements_legaux.append((x - 1, y + 1))

    elif piece == NOIR or piece == DAME_NOIR:
        # Vérifier les mouvements simples pour les pièces noires
        # (vers le bas de la grille)
        if x + 1 < 8:
            if y - 1 >= 0 and plateau[x + 1][y - 1] == VIDE:
                mouvements_legaux.append((x + 1, y - 1))
            if y + 1 < 8 and plateau[x + 1][y + 1] == VIDE:
                mouvements_legaux.append((x + 1, y + 1))

    # Vérification des prises multiples
    # Vous devez parcourir toutes les pièces du plateau pour voir si des prises multiples sont possibles
    for i in range(8):
        for j in range(8):
            if plateau[i][j] == piece or plateau[i][j] == piece.upper():
                # Vérifier si des prises multiples sont possibles depuis cette pièce
                prises_possibles = prise_multiple(plateau, (i, j))
                if prises_possibles:
                    mouvements_legaux.extend(prises_possibles)

    return mouvements_legaux

# Fonction pour initialiser la GUI
def initialiser_gui():
    global root
    root = tk.Tk()
    root.title("Jeu de Dames")

    # Création du plateau de jeu initial
    afficher_plateau_gui()

    # Associer la fonction de gestion du clic à chaque case
    for i in range(8):
        for j in range(8):
            case = plateau[i][j]
            if case != VIDE:
                label = tk.Label(root, text=case, width=3, height=1)
                label.grid(row=i, column=j)
                label.bind("<Button-1>", lambda event, i=i, j=j: gestion_clic(i, j))

    root.mainloop()

# Lancer la GUI
initialiser_gui()
