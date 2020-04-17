# /usr/bin/python3.7
# @Author : RAUX Matthieu
# main.py du mini-projet MasterMind par algorithme génétique
import random
import math

NB_COLORS = 8
NB_PIONS = 4
COEFF_RIGHT_POSITION = 10
POPULATION = 100
MUTATION = 0.1
CROISEMENT = 0.5
NB_GENERATIONS = 10
# Attribution des id
# Historique des couleurs
# Noir:0, Blanc:1, Bleu:2, Vert:3, Rouge:4, Violet:5, Marron:6, Jaune:7
TOFIND = [random.randint(0, NB_COLORS-1) for _ in range(NB_PIONS)]
ATTEMPT = [random.randint(0, NB_COLORS-1) for _ in range(NB_PIONS)]
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
        exit(1)
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
    for i in range(NB_PIONS):
        if (c1[i] == c2[i]):
            pc+=1
        elif(c2[i] in c1):
            mc+=1
    return (pc, mc)

def eval(c, cj):
    """
    (int[], int[]) -> int+
    Retourne la différence entre le score virtuel de cj par rapport à c et le
    score de cj
    """
    pc_cj, mc_cj = compare(cj, TOFIND)
    pc_cj_c, mc_cj_c = compare(cj, c)
    return math.fabs(score(pc_cj_c, mc_cj_c) - score(pc_cj, mc_cj))

def fitness(c):
    """
    int[] -> float
    Retourne la moyenne des évaluations entre c et toutes les combinaisons de l'
    historique
    """
    sum_diff = 0
    for i in range(len(HISTORY)):
        sum_diff += eval(c, HISTORY[i])
    return float(sum_diff/len(HISTORY)) #len(HISTORY) != 0 (sera intialisé au début)

# Début Etape 2
def m_meilleurs(gen):
    """
    prend une liste une liste de combinaisons et en déduit simplement les meilleures
    grâce à la moyenne des diiférence donc fitness.
    int[int[]] -> int[int[]]
    """
    m_meilleurs = list()
    for i in range(POPULATION):
        print("In m_meilleurs {}".format(gen[i]))
        m_meilleurs.append((fitness(gen[i]), gen[i]))
    m_meilleurs = sorted(m_meilleurs, key=lambda a : a[0]) #- vers + sur les fitness
    all_fitness = [each_candidat[0] for each_candidat in m_meilleurs]
    #Si toutes les le fitness est nul alors cela signifie que la combinaison
    #dispose d'une eval nulle donc que son score virtuel par apport à toutes les combinaisons de l'historique est égal
    #au score de chacune de ces combinaisons par rapport à la combinaison à trouver
    if 0 not in all_fitness:
        return [m_meilleurs[0][1]] # Première combinaison avec le fitness le plus faible
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

def mutation(c):
    """
    int[] -> int[]
    Applique une mutation (de proba MUTATION) sur une combinaison un swap,
    + une couleur modifié de manière aléatoire
    """
    # Chose two element to swap
    print("In mutation c is {}".format(c))
    indexes = random.sample(range(NB_PIONS-1), 3)
    c[indexes[0]], c[indexes[1]] = c[indexes[1]], c[indexes[0]] #swap
    toChange = c[indexes[2]]
    while (c[indexes[2]] == toChange): #change la couleur choisie
        new_color = random.randint(0, NB_COLORS-1)
        c[indexes[2]] = new_color
    print("After mutation : {}".format(c))
    return c

# Etape 3
def croisement(c1, c2):
    """
    (int[], int[]) -> int[]
    Applique un croisement entre deux combinaisons on prend une moitié
    ce c1 et une seconde de c2
    On peut soit commencer de 0 ou commencer à un index aléatoire
    """
    index_to_start = random.randint(0, NB_PIONS-1)
    child = [0 for _ in range(NB_PIONS)]
    for i in range(NB_PIONS):
        if (i < NB_PIONS//2):
            child[(index_to_start+i)%NB_PIONS] = c1[i]
        else:
            child[(index_to_start+i)%NB_PIONS] = c2[i]
    return child

def create_new_population(g):
    """
    int[] -> int[int[]]
    On prend une génération et on applique les croisements + mutations en fonction des probas (var globale)
    """
    # TO DO
    new_population = list()
    for i in range(len(g)):
        #gère les croisements
        will_cross = random.random()
        if will_cross <= CROISEMENT:
            print("Croisement")
            new_population.append(croisement(g[i], g[(i+1)%len(g)]))
            new_population.append(croisement((g[(i+1)%len(g)]), g[i]))
        will_mutate = random.random()
        if will_mutate <= MUTATION:
            print("Mutation")
            new_population.append(mutation(g[i]))
        if will_mutate > MUTATION and will_cross > CROISEMENT:
            new_population.append(g[i])
        # else:
        #     new_population.append(g[i])
        # pour bien appliquer fitness il est nécessaire que len(new_population) == len(HISTORY)
        # ce qui sera tjrs le cas du aux conditions
    #La nouvelle géneraion doit faire la taille de la population.ON ajoute des nouveaux jusqu'à atteindre la taille
    while (len(new_population) < POPULATION):
        new_candidate = [random.randrange(0, NB_COLORS) for _ in range(NB_PIONS)]
        if new_candidate not in new_population:
            new_population.append(new_candidate)
    return new_population[:POPULATION]

if __name__ == "__main__":
    # La première tentative est purement aléatoire
    essai = [random.randint(0, NB_COLORS) for _ in range(NB_PIONS)]
    HISTORY.append(essai) #HISTORY ne doit jamais etre empty (utilisation de len(HISTORY) en dénominateur)
    candidats_possibles = list()
    iter_essai = 0 #suit le nombre de tentatives jusqu'à trouver le TOFIND
    print("Le résultat ...{}".format(TOFIND))
    # On vérifie que l'essai est différent du TOFIND
    while (essai != TOFIND):
        iter_essai += 1
        nombre_gen = 0
        #ON crée la population qui sera aléatoire
        gen = [[random.randint(0, NB_COLORS) for _ in range(NB_PIONS)] for _ in range(POPULATION)]
        #On va génerer plusieurs génrations (NB_GENERATIONS)
        while (nombre_gen < NB_GENERATIONS):
            print(nombre_gen)
            if nombre_gen != 0:
                gen = create_new_population(gen)
            gen = m_meilleurs(gen)
            #On doit avoir de nouveau un gen de taille POPULATION
            print("After...")
            for each_candidat in gen:
                if each_candidat not in candidats_possibles:
                    candidats_possibles.append(each_candidat)
            nombre_gen += 1
        # On obtient ici une liste avec un certain nombre de candidats possible
        # les " m meilleurs" de chacune des generation
        #On doit choisir un candidat de manière random
        index_candidat_final = random.randint(0, len(candidats_possibles)-1)
        essai = candidats_possibles[index_candidat_final]
        #vérifier que la tentative n'a pas encore éfé faite
        while (essai in HISTORY):
            index_candidat_final = random.randint(0, len(candidats_possibles)-1)
            essai = candidats_possibles[index_candidat_final]

        print("Tentative n°{} : {}".format(iter_essai, essai))
        HISTORY.append(essai)
        candidats_possibles = list()
    print("Solution trouvé après {} essais. La solution était en effet {}".format(iter_essai, TOFIND))
