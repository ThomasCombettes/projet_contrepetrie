from arbin import *
import json
import itertools
import sys

sys.stdout.reconfigure(encoding='utf-8')

###############################################################################


def mixSyllablesWord1(Word1, Word2, phrase, mode):
    listeWord = []
    tmp = []
    i = 0
    j = 1
    while(i < len(Word1)):

        tmp = mixSyllablesWord2(Word1[i:j], Word2, phrase, mode)

        for k in tmp:
            # test si retour de Word_to_Phon est une chaîne de caractère,
            # Si oui, alors le mélange est un mot existant
            if isInDico(mode, Word1[:i] + k[1] + Word1[j:]):
                listeWord.append([Word1[:i]+k[1]+Word1[j:], k[0], [i, j], k[2]])

        j += 1
        if (j > len(Word1)):
            i += 1
            j = i+1
    return listeWord

###############################################################################


def mixSyllablesWord2(sy, Word2, phrase, mode):
    i = 0
    j = 1
    liste = []

    while(i < len(Word2)):
        # test si retour de Word_to_Phon est une chaîne de caractère
        # et si le Word trouvé n'est pas déjà dans la phrase d'origine.
        if isInDico(mode, Word2[:i]+sy+Word2[j:]) and Word2[:i]+sy+Word2[j:] not in phrase:
            liste.append([Word2[:i]+sy+Word2[j:], Word2[i:j], [i, j]])
        # gestion de l'intervalle [i:j] section du Word2
        j += 1
        if j > len(Word2):
            i += 1
            j = i+1

    return liste
###############################################################################
"""
prend en entrée la phrase de l'utilisateur,et le mode
soit 'phon' ou 'word' (même mode que pour isInDico)

retourne une liste de tuples de la forme :
(nvllePhrase,index1,index2)
index1 est un tuple contenant les coordonées dans la phrase
du premier mot que l'on échange
index2 est un tuple contenant les coordonées dans la phrase
du deuxième mot que l'on échange
"""

def mainMixSyllables(phrase, mode):

    phrase = phrase.split()
    Lphrases = [[phrase]]
    i = 0

    # Pour chaque mot dans la phrase
    for i in range(len(phrase)):
        # Pour chaque autre mot que tmp dans la phrase on permutra
        for j in range(i+1, len(phrase)):

            WordsContreP = mixSyllablesWord1(phrase[i], phrase[j], phrase, mode)
            # remplace les contreP trouvees dans la phrase
            for k in WordsContreP:
                tmp = phrase[:]
                tmp[i] = k[0]
                tmp[j] = k[1]

                # pour chaque nouvelles combinaisons trouvées,
                # on vérifie que la nouvelles n'a pas déjà été trouvée
                taille = len(Lphrases)
                test = True
                for l in range(taille):
                    if Lphrases[l][0] == tmp:
                        test = False

                if test:
                    L1 = (i, k[2][0], k[2][1])
                    L2 = (j, k[3][0], k[3][1])
                    Lphrases.append((tmp, L1, L2))
    return Lphrases
###############################################################################
"""
Retourne liste de phonème de la phrase :
'la poule qui mu' -> 'la pul ki my
"""
def Phrase_to_Phon(phrase):
    string = ''
    for mot in phrase.split():
        if Mot_to_Phon_Only(arbre_mot, mot) != False:
            string += Mot_to_Phon_Only(arbre_mot, mot) + ' '
        else:
            print('\nLe mot', mot, '''de la phrase n\'est pas dans notre dictonnaire.
            Veuillez essayer avec une autre orthographe.''')
            return False
            break
    return string

################################################################################
'''
Prend en argument une phrase en phonétique en string
retourne les combinaisons possibles de phrases en orthographe
classique en string
phraseOrigine est la liste des mots de la phrase d'origine,
on l'utilise pour filtrer les resultats des combinaisons
selon un % de mots recurrent entre la nvlle et l'ancienne phrase
'''

def Phon_to_Phrase(PhrasePhoneme, phraseOrigine, pos1, pos2):

    listeretour = []
    listePhon = PhrasePhoneme.split()
    # PhrasePhoneme(str)
    with open('data/dicoPhoncom.json') as tmp:
        dicoPhon = json.load(tmp)

# Extraction du dico de phonème les mots possible a partir des phonèmes en entrée
    for i in range(len(listePhon)):
        listePhon[i] = dicoPhon[listePhon[i]]

    for i in range(len(listePhon[pos1])):
        for j in range(len(listePhon[pos2])):
            string = phraseOrigine[:]
            string[pos1] = listePhon[pos1][i]
            string[pos2] = listePhon[pos2][j]

            listeretour.append(string)


# Produit de toutes les combinaisons possibles des mots
# qui ont changer par rapport à la phrase d'origine
    return listeretour
