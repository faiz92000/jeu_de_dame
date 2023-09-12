# Définition des pièces
VIDE = ' '
BLANC = 'B'
NOIR = 'N'

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

# Fonction d'affichage du plateau
def afficher_plateau(plateau):
    print("   0  1  2  3  4  5  6  7")
    print("  +-----------------------+")
    for i, ligne in enumerate(plateau):
        ligne_str = str(i) + " |"
        for case in ligne:
            ligne_str += " " + case + " |"
        print(ligne_str)
        print("  +-----------------------+")

# Afficher le plateau de jeu initial
afficher_plateau(plateau)
