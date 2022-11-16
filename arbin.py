import os
import sys
import csv
sys.stdout.reconfigure(encoding='utf-8')

# ----------------------------------------------------------------------------
"""
fonctions de navigations et création de la classe d'arbre binaire 
"""
class Tree:
    def __init__(self, value, left, right):
        self.value = value  # kystiques,kis tik -> kis tik,kystiques
        self.left = left
        self.right = right
        self.hauteurG = 0
        self.hauteurD = 0

    def __str__(self):
        return "Tree(%s (%d, %d), %s , %s)" % (self.value, self.hauteurG, self.hauteurD, self.left.value, self.right.value)
# ----------------------------------------------------------------------------


def insert(tree, value):
    if value < tree.value:
        if tree.left is None:
            tree.left = Tree(value, None, None)
            tree.hauteurG = 1
        else:
            insert(tree.left, value)
            tree.hauteurG = 1 + max(tree.left.hauteurG,
                                    tree.left.hauteurD)
    else:
        if tree.right is None:
            tree.right = Tree(value, None, None)
            tree.hauteurD = 1
        else:
            insert(tree.right, value)
            tree.hauteurD = 1 + max(tree.right.hauteurG,
                                    tree.right.hauteurD)

    eq = equilibre(tree)
    if eq > 1:
        if equilibre(tree.left) < 0:
            rotate_left(tree.left)

        rotate_right(tree)

    elif eq < -1:
        if equilibre(tree.right) > 0:
            rotate_right(tree.right)

        rotate_left(tree)
# ----------------------------------------------------------------------------


def insertbis(tree, value):
    if value < tree.value:
        if tree.left is None:
            tree.left = Tree(value, None, None)
            tree.hauteurG = 1
        else:
            insert(tree.left, value)
            tree.hauteurG = 1 + max(tree.left.hauteurG,
                                    tree.left.hauteurD)
    else:
        if tree.right is None:
            tree.right = Tree(value, None, None)
            tree.hauteurD = 1
        else:
            insert(tree.right, value)
            tree.hauteurD = 1 + max(tree.right.hauteurG,
                                    tree.right.hauteurD)

    eq = equilibre(tree)
    if eq > 1:
        if equilibre(tree.left) < 0:
            rotate_left(tree.left)

        rotate_right(tree)

    elif eq < -1:
        if equilibre(tree.right) > 0:
            rotate_right(tree.right)

        rotate_left(tree)
# ----------------------------------------------------------------------------


def hauteur(tree):
    if tree is None:
        return 0
    else:
        return max(hauteur(tree.left), hauteur(tree.right)) + 1
# ----------------------------------------------------------------------------


def equilibre(tree):
    return tree.hauteurG - tree.hauteurD
# ----------------------------------------------------------------------------


def rotate_right(tree):
    tf = tree.left
    (tree.value, tree.left, tree.right,
     tf.value, tf.left, tf.right,
     ) = \
        (tf.value, tf.left, tf,
         tree.value, tf.right, tree.right)

    tr = tree.right
    tr.hauteurD = hauteurF(tr.right)
    tr.hauteurG = hauteurF(tr.left)

    tree.hauteurD = hauteurF(tree.right)
    tree.hauteurG = hauteurF(tree.left)

    return tree
# ----------------------------------------------------------------------------


def hauteurF(t):
    if t is None:
        return 0
    return max(t.hauteurG, t.hauteurD) + 1
# ----------------------------------------------------------------------------


def rotate_left(tree):
    tf = tree.right
    (tree.value, tree.right, tree.left, tf.value, tf.right, tf.left,) = \
        (tf.value, tf.right, tf, tree.value, tf.left, tree.left)

    tr = tree.left
    tr.hauteurG = hauteurF(tr.left)
    tr.hauteurD = hauteurF(tr.right)

    tree.hauteurG = hauteurF(tree.left)
    tree.hauteurD = hauteurF(tree.right)

    return tree
# ----------------------------------------------------------------------------
"""
retourne une écriture orthographique
de 'value' si le mot est dans le lexique, false sinon
mais cette a peu d'intêret à leur où l'on rend le projet
Cet arbre ne nous sers qu'à la fonction isInDico
"""

def Phon_to_Mot(tree, value):
    if tree is None:
        return False
    if (tree.value.split(",")[0]) == value:
        return (tree.value.split(",")[1] + "," + tree.value.split(",")[2])
    if (tree.value.split(",")[0]) is not None and value < (tree.value.split(",")[0]):
        return Mot_to_Phon(tree.left, value)
    elif (tree.value.split(",")[0]) is not None:
        return Mot_to_Phon(tree.right, value)

# ----------------------------------------------------------------------------
"""
retourne le phonème et la classe grammaticale de 'value' si le mot est dans
le lexique, false sinon

retour de forme:
'phoneme,classGramm'
"""

def Mot_to_Phon(tree, value):
    if tree is None:
        return False
    if (tree.value.split(",")[0]) == value:
        return (tree.value.split(",")[1] + "," + tree.value.split(",")[2])
    if (tree.value.split(",")[0]) is not None and value < (tree.value.split(",")[0]):
        return Mot_to_Phon(tree.left, value)
    elif (tree.value.split(",")[0]) is not None:
        return Mot_to_Phon(tree.right, value)
# ----------------------------------------------------------------------------
"""
retourne le phonème de 'value' si le mot est dans le lexique, false sinon
"""

def Mot_to_Phon_Only(tree, value):
    if tree is None:
        return False
    if (tree.value.split(",")[0]) == value:
        return tree.value.split(",")[1]
    elif (tree.value.split(",")[0]) is not None and value < (tree.value.split(",")[0]):
        return Mot_to_Phon_Only(tree.left, value)
    elif (tree.value.split(",")[0]) is not None:
        return Mot_to_Phon_Only(tree.right, value)
# ----------------------------------------------------------------------------

"""
Vérifie si le mot ou phonéme en entrée est dans le lexique
en nLog(n) compléxité
"""
def isInDico(mode, mot):

    if mode == 'word':
        return isinstance(Mot_to_Phon(arbre_mot, mot), str)

    if mode == 'phon':
        return isinstance(Phon_to_Mot(arbre_phon, mot), str)
    else:
        return False
# ----------------------------------------------------------------------------


def empty():
    return Tree(0, None, None)
# ----------------------------------------------------------------------------

"""
Construit une structure d'arbre de recherche binaire, trié par ordre alphabétique
Contient les mots du lexique sous forme orthographique et leur correspondance en phonétique

chaque feuille contient une string de forme :
'mot,sonphoneme,sa classe gramticale,genre,nombre'
"""
def Constructeur_Arbre_Mot():
    a = Tree("aaa", None, None)
    tsv_file = open("data/Lexique383.tsv", encoding="utf-8")
    read_tsv = csv.reader(tsv_file, delimiter="\t")
    for lignes in read_tsv:
        if " " not in lignes[0]:
            mot = lignes[0] + "," + lignes[1] + "," + \
                lignes[3][:3] + "," + lignes[4] + "," + lignes[5]
            insert(a, mot)
    tsv_file.close()
    return a
# ----------------------------------------------------------------------------
"""
verso de la fonction ci-dessus, mais cet arbre a peu d'intêret à celle-ci
à leur où l'on rend le projet
Cet arbre ne nous sers qu'à la fonction isInDico
chaque feuille contient une string de forme :
'phoneme,mot,sa classe gramticale,genre,nombre'
"""

def Constructeur_Arbre_Phon():
    a = Tree("aaa", None, None)
    tsv_file = open("data/Lexique383.tsv", encoding="utf-8")
    read_tsv = csv.reader(tsv_file, delimiter="\t")
    for lignes in read_tsv:
        if " " not in lignes[0]:
            mot = lignes[1] + "," + lignes[0] + "," + lignes[3] + lignes[4] + lignes[5]
            insert(a, mot)
    tsv_file.close()
    return a


# ----------------------------------------------------------------------------
arbre_mot = Constructeur_Arbre_Mot()
arbre_phon = Constructeur_Arbre_Phon()
