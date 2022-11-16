from arbin import *
from filtre import *
import string
import sys
import json
import re
import os


# ----------------------------------------------------------------------------
"""
Remplace une lettre dans la chaine s à la position "index"
par la chaîne newstring.
i.e replacer("bonjour","pate",3) --> "bonpateour"
"""


def replacer(s, newstring, index):

    if index < 0:  # l'ajoute au début
        return newstring + s
    if index > len(s):  # l'ajoute à la fin
        return s + newstring
    # insère la nouvelle chaîne entre les tranches de l'originalnsert the new string between "slices" of the original
    return s[:index] + newstring + s[index + 1:]
# ----------------------------------------------------------------------------


"""
Recherche dans le mot donné les mots possible à partir de
sa forme phonétique en substituant une partie du mot
ex : model -> monel,motel,modal,modem,etc
retourne une liste de tuples des possibilitées au format :
[(mot,Anciennelettre,nouvellelettre),...]
"""


def aideSonSubs(mot_origine):

    with open('data/dicoPhoncom.json') as tmp:
        dicoPhon = json.load(tmp)

    phon_file = open("data/BD_phoneme.txt", encoding="utf-8")
    BD_phoneme = phon_file.read()
    BD_phoneme = BD_phoneme.split("\n")
    listeDeMotCop = []

    mot = Mot_to_Phon_Only(arbre_mot, mot_origine)
    if not isinstance(mot, str):
        print("Ce mot n'est pas dans notre lexique, nous ne pouvons pas trouver son phonème.\n")
        return 0
    clear()
    # mettre un test de si Mot_to_Phon renvoi False, cest une Erreur
    print(f"\nEn phonétique '{mot_origine}' se lit '{mot}'\n")

    print("Voici donc les sons que l'on peut changer :")
    compteur = 0
    for lettre1 in enumerate(mot):
        print(f"  '{lettre1[1]}'    ", end='')

        for lettre2 in BD_phoneme:
            compteur += 1
            # si on remplace à l'index la lettre1 par lettre2,
            # et que ça forme un mot dans lexique, on ajoute le nvMot à la liste.
            nvMot = replacer(mot, lettre2, lettre1[0])

            test = isInDico('phon', nvMot)

            if lettre1[1] != lettre2 and test:
                listeDeMotCop.append((nvMot, lettre1[1], lettre2, dicoPhon[nvMot][0]))
    print("\n")
    return listeDeMotCop


# ----------------------------------------------------------------------------
"""
Gènère les quadruplets de l'aide, avec l'échange d'un seul son entre les mots.
Prend en argument la sortie de aideSonSub et l'index du mot saisie par l'utilisateur

retourne une liste de tuple de format :
(son1,son2,mot1',mot2',mot2)
son1 -> son saisie, que l'on désir échanger
son2 -> son selectionné ensuite que l'on veut échanger avec son1

mot2 -> obtenu en échangeant son1 par son2 dans le mot d'origine

mot1'-> mot contenant son1
mot2'-> mot contenant son2
"""


def aideSonRechDico(index, listeDeMotCop):
    with open('data/DicoVulgaire.json') as vulgaire:
        BDvulgaire = json.load(vulgaire)

    with open('data/config.json') as diconfig_:
        diconfig = json.load(diconfig_)

    index -= 1
    NombreDeMot = len(listeDeMotCop)
    compteur = 0
    listeDeMotNONCop = []
    listeDeRacines = []
    listeAffichage = []

    tsv_file = open("data/Lexique383.tsv", encoding="utf-8")
    lignes = csv.reader(tsv_file, delimiter="\t")

    # lit ligne par ligne du DICO (près de 100k lignes)
    diconfig = changerfiltre(diconfig)
    for mot in lignes:
        mot = mot[1]

        for ChaqueLettre in range(len(listeDeMotCop)):

            test1 = listeDeMotCop[ChaqueLettre][2] in mot
            test2 = mot[:5] not in listeDeRacines
            # Racines:
            if index == ChaqueLettre and test1 and test2:
                testDansMot = replacer(mot, listeDeMotCop[ChaqueLettre][1],
                                       mot.index(listeDeMotCop[ChaqueLettre][2]))
                # la lettre est dans le mot
                if isInDico('phon', testDansMot):
                    if diconfig["FiltreGrossier"] == "Oui":
                        if (listeDeMotCop[ChaqueLettre][0] in BDvulgaire or testDansMot in BDvulgaire or mot in BDvulgaire):
                            listeAffichage.append((listeDeMotCop[ChaqueLettre][1],
                                                   listeDeMotCop[ChaqueLettre][2],
                                                   listeDeMotCop[ChaqueLettre][0],
                                                   testDansMot, mot))
                            listeDeRacines.append(mot[:5])
                    else:
                        listeDeRacines.append(mot[:5])
                        listeAffichage.append((listeDeMotCop[ChaqueLettre][1],
                                               listeDeMotCop[ChaqueLettre][2],
                                               listeDeMotCop[ChaqueLettre][0],
                                               testDansMot, mot))
                compteur += 1
    return (listeAffichage, compteur, diconfig)


# ----------------------------------------------------------------------------
"""
Affiche les quadruplets trouvés suite à la recherche de façon jolie.
et permet de voir les orthographes différents des phonèmes du quadruplets en
appelant affiOrthoPhon
"""
def affiRechSon(listeAffichage, compteur, mot_origine):
    with open('data/dicoPhoncom.json') as tmp:
        dicoPhon = json.load(tmp)

    motOriPhon = Mot_to_Phon_Only(arbre_mot, mot_origine)
    listeAffichage = (sorted(listeAffichage, key=lambda lettre: lettre[0]))
    son1,son2 = "",""
    clear()
    while(True):
        compt = 1

        for pack in listeAffichage:

            espace = 40 - len(mot_origine) - len(pack[4])
            marge = len(str(compt))+2

            print(marge*" ", "Phonèmes", " "*(30-marge), "Un exemple d'orthographe")
            print(marge*" "+f"{motOriPhon} - {pack[4]}"+espace * " "+f"|  {mot_origine} - {dicoPhon[pack[4]][0]}")
            print(compt, 35 * " ", " ex : ")

            espace = 40 - len(pack[2]) - len(pack[3])

            print(marge*" "+f"{pack[2]} - {pack[3]}"+espace*" " +
                  f"|  {dicoPhon[pack[2]][0]} - {dicoPhon[pack[3]][0]}")

            print("\n"+"-"*60+"\n")

            son1 = pack[0]
            son2 = pack[1]
            compt += 1
        print("Échange entre : ",son1,"-",son2)
        print(f"Nombre de combinaisons : {compt-1}")

        selecteur = None
        boucle = True
        while(boucle):
            try:
                selecteur = int(input(
                    "\n0 = quitter l'aide,-1 revenir au début de l'aide \nou numéro du quadruplet, pour voir toutes les orthographes des phonèmes : \n"))
            except:
                print("\nVous n'avez pas saisi un chiffre")
                continue

            if selecteur == 0:
                return 0
            elif selecteur == -1:
                clear()
                return 1
            elif selecteur <= len(listeAffichage) and selecteur > 0:
                affiOrthoPhon(listeAffichage, selecteur-1, mot_origine)
                boucle = False
            else:
                print("\nL'entrée n'est pas valide, réessayez")


# ------------------------------------------------------------------------------
"""
Affiche toutes les orthographes contenus dans le dicoPhon.json des Phonèmes du quadruplet
de listeAffichage à l'index donnée en entrée.
"""


def affiOrthoPhon(listeAffichage, index, mot_origine):
    clear()
    with open('data/dicoPhoncom.json') as tmp:
        dicoPhon = json.load(tmp)

    motOriPhon = Mot_to_Phon_Only(arbre_mot, mot_origine)
    pack = listeAffichage[index]

    tCol = 20
    print(" "*8, motOriPhon, " "*(tCol-len(motOriPhon)), end='')
    print(pack[3], " "*(tCol-len(pack[4])), end='')
    print(pack[2], " "*(tCol-len(pack[2])), end='')
    print(pack[4], " "*(tCol-len(pack[3])), "\n")

    phon2 = dicoPhon[pack[3]]
    phon3 = dicoPhon[pack[2]]
    phon4 = dicoPhon[pack[4]]

    for i in range(max((len(phon2), len(phon3), len(phon4)))):
        if i == 0:
            print(" "*7, mot_origine, " "*(tCol-len(motOriPhon)), end='')
        else:
            print(" "*8, " "*(tCol+1), end='')
        if i < len(phon2):
            print(phon2[i], " "*(tCol-len(phon2[i])), end='')
        else:
            print(" "*(tCol+1), end='')
        if i < len(phon3):
            print(phon3[i], " "*(tCol-len(phon3[i])), end='')
        else:
            print(" "*(tCol+1), end='')

        print(phon4[i]) if i < len(phon4) else print("")

    input("\nEntrez n'importe quel touche pour continuer ")


"""
# ----------------------------------------------------------------------------
# Partie sur plusieurs sons :
# ----------------------------------------------------------------------------
"""
"""
Retourne un dico dont les clefs sont toutes les tranches du mots plus grandes
que tailleMin
"""
def trancheMot2(mot, tSlice):
    """
    Retourne un dico dont les clefs sont toutes les tranches du mots plus grandes
    que tailleMin
    """
    dicoSliceCom = {}
    for i in range(len(mot)):
        for j in range(i+1, len(mot)+1):
            if mot[i:j] != mot and j-i <= tSlice:
                dicoSliceCom[mot[i:j]] = []

    return dicoSliceCom
# ----------------------------------------------------------------------------
"""
génère un itérateur de tuples contenant (debutMot,finMot) autour de toutes
les différentes tranches possible du mot.
"""

def DebFinMot(mot, tSlice):
    # génère un itérateur de tuples contenant (debutMot,finMot) autour de toutes
    # les différentes tranches possible du mot.
    for i in range(len(mot)):
        for j in range(i+1, len(mot)+1):
            if mot[i:j] != mot and j-i <= tSlice:
                yield (mot[:i], mot[j:])


# ----------------------------------------------------------------------------
"""
Prend en argument le mot dont on veut les contrepétries,
Fait la même chose que aideSonSubs()
La fonction retourne un dictionnaire avec en clefs la slice et en valeur
un ensemble contenant les mots contenant cette slice du mot d'origine
"""

def aideMultiSonSubs(mot_origine):

    tsv_file = open("data/Lexique383.tsv", encoding="utf-8")
    Lexlignes = csv.reader(tsv_file, delimiter="\t")
    tmp = mot_origine
    mot_origine = Mot_to_Phon_Only(arbre_mot, mot_origine)
    if isinstance(mot_origine, bool):
        return False

    dicoSliceCom = trancheMot2(mot_origine, 3)

# recherche dans le lexique la correspondance des slices
    for ligne in Lexlignes:
        # on ne fait pas de recherche sur les mots composés et on exclue le mot d'entrée
        if '-' not in ligne[1] and ' ' not in ligne[1] and ligne[1] != mot_origine:
            ensTmp = []
            LexMot = ligne[1]

            iterDebFin = DebFinMot(mot_origine, 3)
# pour chaque tranche on recherche les mots dans lexique qui commencent
# et finissent de la même façon que le mot_origine:
# ex. danse -> slice: "an", on cherche les mots commençant
# par "d" et finissant par "se".

            for slice in dicoSliceCom.keys():
                try:
                    deb, fin = next(iterDebFin)
                except:
                    break

                # on ne prend que les mots dont la partie qui change au centre
                # mesure 5 caractères maximums.
                test = len(LexMot) - len(deb) - len(fin) <= 3 and len(LexMot) > 1
                if LexMot.startswith(deb) and LexMot.endswith(fin) and test:
                    dicoSliceCom[slice].append(LexMot)

    # on supprime les tranches qui n'ont pas de résultats
    dicoTmp = {}
    for i in dicoSliceCom.keys():
        if dicoSliceCom[i] != []:
            dicoTmp[i] = dicoSliceCom[i]

    print(f"Écriture phonétique : {mot_origine} - {tmp}")
    return dicoTmp

#je m'excuse de la qualité des commentaires de certaines fonctions,
#il est actuellement 5h du mat pour moi pour la 4eme fois de la semaine pour rendre ce projet ^^
#bon courage pour votre projet, jespère que vous vous en sortirez, -Corentin (mort à l'intérieur)

#ps: si M.Lafourcade vous lisez ceci et désolé je voulais glisser un petit easter egg :)

# -----------------------------------------------------------------------------

"""
Affichage intermédaire avant la fin.
Affiche les différentes tranches du phonème du mot d'origine qui peuvent
êtres remplacées pour former un mot dans le lexique
Retourne les sons que souhaite échangé l'utilisateur dans le mot d'origine
"""

def affiNbCorrTranche2(dicoSliceCom):
    # affichage du nombre de correspondances par tranche
    index = 1
    for i in dicoSliceCom.keys():
        # elimination des doublons dans les listes.
        dicoSliceCom[i] = sorted(list(set(dicoSliceCom[i])))
        tailleString = 15 - len(str(i) + str(len(dicoSliceCom[i])))

        print(index, i, "-"*tailleString+">", len(dicoSliceCom[i]), "mots")
        index += 1

    print("\n0 : quitter l'aide/ -1 revenir au début de l'aide")
    selectSlice = None
    test = True
    while(test):
        try:
            selectSlice = int(
                input("Quels sons voulez-vous voulez-vous échanger ? (rentrez leur indice) :"))
        except:
            print("")
        if selectSlice in range(1, len(dicoSliceCom.keys())+1):
            test = False
        elif selectSlice == 0:
            return 0
        elif selectSlice == -1:
            return -1
        else:
            print("L'entrée n'est pas valide, réessayez\n")
    return list(dicoSliceCom.keys())[selectSlice-1]


# -----------------------------------------------------------------------------
"""
Suite de affiNbCorrTranche2,
affiche page par page de 60 phonèmes avec un exemple d'orthographe
des mot possibles en échangeant les sons rentrée par l'utilisateur dans
la fonction précédante,
Retourne le phonème selectionné par l'utilisateur qui l'intéresse pour l'echange
"""

def affiPageParPage2(listeMot, syllOrigine, mot_origine):
    nbMotPage = 60  # nombre de mots par pages
    nbPage = (len(listeMot)//nbMotPage)  # nombre total de pages.
    numPage = 0                          # numéro page en cours

    with open('data/dicoPhoncom.json') as tmp:
        dicoPhon = json.load(tmp)

    choix = {-1, -2}
    selecteur = 0
    continuer = True
    while(continuer):
        if selecteur == -2:
            numPage = numPage+1 if numPage+1 <= nbPage else numPage
        elif selecteur == -1:
            numPage = numPage-1 if numPage-1 >= 0 else numPage

        clear()
        print(f"page {numPage}/{nbPage}\n")

        for i in range(1, nbMotPage, 2):

            mot1 = listeMot[nbMotPage*numPage+i-1] if nbMotPage*numPage+i-1 < len(listeMot) else ""
            mot2 = listeMot[nbMotPage*numPage+i] if nbMotPage*numPage+i < len(listeMot) else ""

            phon1 = "ex: "+dicoPhon[mot1][0] if mot1 != "" else ""
            phon2 = "ex: "+dicoPhon[mot2][0] if mot2 != "" else ""

            # recupération de la taille des mots pour l'espace entre les deux
            # c'est un pretty print
            espace1 = 15 - len(mot1)
            espace2 = 45 - len(phon1)-len(mot1)-espace1
            espace3 = 15 - len(mot2)

            if i <= 10:
                print(f"{i}  {mot1}", espace1*" ", phon1, " " *
                      espace2, f"{i+1}  {mot2}", espace3*" ", phon2)
            else:
                print(i, mot1, espace1*" ", phon1, " "*espace2, i+1, mot2, espace3*" ", phon2)

        print(
            f"\nLes mots obtenables en remplaçant '{syllOrigine}' dans '{Mot_to_Phon_Only(arbre_mot,mot_origine)}' ('{mot_origine}')")
        test = True
        while(test):

            try:
                selecteur = int(input("""
(0 : quitter l'aide/-3: revenir à selection précèdante /-4: revenir au début de l'aide)
(-1:Gauche / -2:Droite) ou saisissez numéro du mot :\n"""))
            except:
                print("\nVous n'avez pas saisi un chiffre")
                continue

            test1 = (nbMotPage*numPage+selecteur) <= len(listeMot) and (nbMotPage*numPage+selecteur) > 0
            if selecteur == 0:
                return 0
            elif selecteur == -3:
                clear()
                print(f"{mot_origine} : {Mot_to_Phon_Only(arbre_mot,mot_origine)}\n")
                return True
            elif selecteur == -4:
                return -1
            elif selecteur in choix or test1:
                print("\nChargement en cours ...")
                test = False
            else:
                print("\nL'entrée n'est pas valide, réessayez")
        continuer = False if selecteur not in choix else True
    return listeMot[nbMotPage*numPage+selecteur-1]


# ----------------------------------------------------------------------------
"""
Fait la liste des quaduplets d'échanges possibles:
de forme exemple :

(syll1,syll2,mot1',mot2',mot2)
"""

def aideMultiSonRechDico(mot_origine, selectMot, syllOrigine):
    # ex: d'an'se      d'ar'se    'an'

    mot_origine = Mot_to_Phon_Only(arbre_mot, mot_origine)
    listeAffichage = []
    listeTmp = []

    # recup deb et fin de mot_origine:
    debFin = mot_origine.split(syllOrigine)
    # extraction de 'ar' de selectMot.
    if len(debFin[1]) > 0:
        syllNvlle = selectMot[len(debFin[0]):-len(debFin[1])]

    else:
        syllNvlle = selectMot[len(debFin[0]):]
    print(syllNvlle,"-",syllOrigine)
    tsv_file = open("data/Lexique383.tsv", encoding="utf-8")
    LexLignes = csv.reader(tsv_file, delimiter="\t")

    with open('data/DicoVulgaire.json') as vulgaire:
        BDvulgaire = json.load(vulgaire)

    with open('data/config.json') as diconfig_:
        diconfig = json.load(diconfig_)

    # lit ligne par ligne du DICO (près de 100k lignes)
    # changer filtres
    print('Maintenant il reste à gérer les filtres pour la génération')
    diconfig = changerfiltre(diconfig)

    for ligne in LexLignes:
        LexMot = ligne[1]

        # cherche occurences de la nouvelle tranche dans le lexique
        if syllNvlle in LexMot:

            # on recupère l'index de l'occurence de syllNvlle dans le mot du lexique
            indexSyllNvlle = re.finditer(syllNvlle, LexMot)
            indexSyllNvlle = [match.start() for match in indexSyllNvlle]

            for i in indexSyllNvlle:
                # À partir de celles-ci on recupère le début et la fin de ce mot
                LexDeb = LexMot[:i]
                LexFin = LexMot[i+len(syllNvlle):]

                # on teste si le la concaténation du debut et fin de ce mot avec la slice
                # d'origine forment un mot qui existe dans le lexique
                testMot = LexDeb + syllOrigine + LexFin
                if isInDico('phon', testMot) and testMot not in listeTmp:
                    if diconfig["FiltreGrossier"] == "Oui":
                        if (selectMot in BDvulgaire or testMot in BDvulgaire or LexMot in BDvulgaire):
                            listeAffichage.append([syllOrigine, syllNvlle,
                                                   selectMot, testMot,
                                                   LexMot])
                            listeTmp.append(testMot)
                    else:
                        # si oui on l'ajoute a notre liste de résultat.
                        listeAffichage.append([syllOrigine, syllNvlle,
                                               selectMot, testMot,
                                               LexMot])
                        listeTmp.append(testMot)
    return (listeAffichage, len(listeAffichage), diconfig)
