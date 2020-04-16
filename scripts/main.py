# /usr/bin/python3.7
# @Author : RAUX Matthieu
# main.py du mini-projet MasterMind par algorithme génétique
import random
import math
import sys

AMOUNT_COLORS = 8
AMOUNT_PAWNS = 4
COEFF_RIGHT_POSITION = 5
# Attribution des id
# Historique des couleurs
# Noir:0, Blanc:1, Bleu:2, Vert:3, Rouge:4, Violet:5, Marron:6, Jaune:7
TOFIND = [random.randint(0, AMOUNT_COLORS-1) for _ in range(AMOUNT_PAWNS)]
ATTEMPT = [random.randint(0, AMOUNT_COLORS-1) for _ in range(AMOUNT_PAWNS)]
HISTORY = list()

 # L'algorithme retournera deux valeurs pour chaque solution candidate (ATTEMPT)
 # pc le nombre de couleur correctement placées
 # mc le nombre de couleur présentes mais mal placées

def score(pc, mc):
    """
    (int, int) -> int+
    On quitte si l'une des deux est strictement négative
    On utilise COEFF_RIGHT_POSITION pour donner plus d'importance à un pion bien
    positionné
    """
    if (mc < 0 or mc < 0) :
        sys.exit()
    return COEFF_RIGHT_POSITION*pc + mc

def compare(c1, c2):
    """
    (int, int) -> (int, int)[(pc, mc)]
    Retourne le nombre de couleur de c2 bien placé dans c1 et le nombre de couleur
    mal placé mais existante
    On devra garder les indices des bons couleurs à la bonne position et de celle
    à la mauvaise mais quand même existance
    """
    pc, mc = 0, 0
    pc_indexes, mc_indexes = list(), list()
    for i in range(AMOUNT_PAWNS):
        if (c1[i] == c2[i]):
             pc+=1
             pc_indexes.append(i)
        elif(c2[i] in c1):
            mc+=1
            mc_indexes.append(i)
    return (pc, mc)

def eval(c, cj):
    """
    (int[], int[]) -> int+
    Retourne la différence entre le score virtuel de cj par rapport à c et le
    score de cj
    """
    pc_cj, mc_cj = compare(cj, TOFIND)
    pc_cj_c, mc_cj_c = compare(cj, c)
    return math.abs(score(pc_cj_c, mc_cj_c) - score(pc_cj, mc_cj))

def fitness(c):
    """
    int[] -> float
    Retourne la moyenne des évaluations entre c et toutes les combinaisons de l'
    historique
    """
    sum_diff = 0
    for i in range(len(HISTORY)):
        sum_diff += eval(c, HISTORY[i])
    return sum_diff/len(HISTORY)

# Début Etape 2


if __name__ == "__main__":
    print("So far nothing")
