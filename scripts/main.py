# /usr/bin/python3.7
# @Author : RAUX Matthieu
# main.py du mini-projet MasterMind par algorithme génétique
import random
import math
import sys

AMOUNT_COLORS = 8
AMOUNT_PAWNS = 4
COEFF_RIGHT_POSITION = 5
POPULATION = 200
MUTATION = 0.05
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
    if (mc < 0 or pc < 0) :
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
    return float(sum_diff/len(HISTORY))

# Début Etape 2
def m_meilleurs(gen):
    """
    prend une liste une liste de combinaisons et en déduit simplement les meilleures
    grâce à la moyenne des diiférence donc fitness.
    int[int[]] -> int[int[]]
    """
    m_meilleurs = list()
    for i in range(POPULATION):
        m_meilleurs.append(fitness(gen[i]), gen[i])
    m_meilleurs = sorted(m_meilleurs, key=lambda a : a[0]) #- vers + sur les fitness
    all_fitness = [each_candidat[0] for each_candidat in m_meilleurs]
    #Si toutes les le fitness est nul alors cela signifie que la combinaison
    #dispose d'une eval nulle donc que son score virtuel par apport à toutes les combinaisons de l'historique est égal
    #au score de chacune de ces combinaisons par rapport à la combinaison à trouver
    if 0 not in all_fitness:
        return m_meilleurs[1][0] # Première combinaison avec le fitness le plus faible
    else:
        index = 0
        # Dans ce cas faut prendre toutes les combinaisons jusqu'au premier non nul
        for i in range(len(all_fitness)):
            if all_fitness[i] != 0:
                index = i
                break
    return [each_candidat[1] for each_candidat in m_meilleurs[:index]]

#Opération de mutation sur une solution candidate
#La mutation est juste une altération aléatoire, on peut en swapper deux ou alors
#modifier une couleur de manière random

def mutate(c):
    """
    int[] -> int[]
    Applique une mutation (de proba MUTATION) sur une combinaison un swap,
    + une couleur modifié de manière aléatoire
    """
    # Chose two element to swap
    indexes = random.sample(range(AMOUNT_PAWNS-1), 3)
    c[indexes[0]], c[indexes[1]] = c[indexes[1]], c[indexes[0]] #swap
    toChange = c[indexes[2]]
    while (c[indexes[2] == toChange]):
        new_color = random.randint(0, AMOUNT_COLORS-1)
        c[indexes[2]] = new_color

def croisement(c1, c2):
    """
    (int[], int[]) -> int[]
    Applique un croisement entre deux combinaisons on prend une moitié
    ce c1 et une seconde de c2
    On peut soit commencer de 0 ou commencer à un index aléatoire
    """
    index_to_start = random.randint(0, AMOUNT_PAWNS-1)
    child = [0 for _ in range(AMOUNT_PAWNS)]
    for i in range(AMOUNT_PAWNS):
        if (i < AMOUNT_PAWNS//2):
            child[(index_to_start+i)%AMOUNT_PAWNS] = c1[i]
        else:
            child[(index_to_start+i)%AMOUNT_PAWNS] = c2[i]
        print(child)
    return child


if __name__ == "__main__":
    print("So far nothing")
