print("Chargement des dictionnaires")
from filtre import *
import sys

boucle = True
memoireImport = set()
# boucle pour recommencer le programme
while boucle:
    clear()
    valide = True
    test = True
    n = 0
    # selecteur type de programme:
    while test:

        print(
"""\nSelectionnez le mode que vous souhaitez : \n
1. Aide à la contrepéterie
2. Recherche de contrepéterie
3. Configuration des filtres
0. Quitter\n""")
        try:
            n = int(input())
        except ValueError:
            print("Vous n'avez pas saisie un nombre.\n")

        if n == 0:
            sys.exit()
        elif n in range(1,4):
            test = False
        else:
            print("Votre saisie n'est pas valide\n")
# ------------------------------------------------------------------------------
    if n == 3:
        configFiltre()
# ------------------------------------------------------------------------------
    # aide à contrepeterie
    elif n == 1:
        if 'aide' not in memoireImport:
            from aideContre import *
        memoireImport.add('aide')
        clear()
        aideContrepetrie()

# ------------------------------------------------------------------------------
    # recherche de contrepeterie
    elif n == 2:
        if 'rech' not in memoireImport:
            from echSyllabe import *
        memoireImport.add('rech')

        test = True
        mode = {1: 'word', 2: 'phon'}
        n = 0
        while test:
            print("""\nVoulez-vous échanger \n
        1. Les lettres
        2. Les sons\n""")
            try:
                n = int(input())
            except ValueError:
                print("Vous n'avez pas saisie un nombre.\n")
            if n in range(1,3):
                test = False
            else:
                print("Votre saisie n'est pas valide\n")
# ------------------------------------------------------------------------------
        clear()
        if mode[n] == 'word':

            while(True):
                print("0 :quitter / 1 revenir au menu précédant")
                phraseOrigine = input("Phrase à sonder :\n")
                test = False
                try :
                    phraseOrigine = int(phraseOrigine)
                    test = True
                except:
                    break

                if test:
                    if  phraseOrigine == 0 :
                        sys.exit()

                    elif phraseOrigine == 1:
                        break

                    else:
                        print("\nLa saisie n'est pas valide")
            if phraseOrigine == 1:
                continue

            liste = mainMixSyllables(phraseOrigine, mode[n])
            liste = affiRechFiltre(liste,'word')
            count = 0
            print("\nLes contrepétries possibles sont :\n")
            for contrepet in liste[1:]:
                print(f" {contrepet}\n")
                count += 1
            print('\nNombre de résultats : ', count)
# ------------------------------------------------------------------------------
        #recherche sur les sons:
        else:
            while(True):
                print("0 :quitter / 1 revenir au menu précédant")
                phraseOrigine = input("Phrase à sonder: \n")
                test = False
                try :
                    phraseOrigine = int(phraseOrigine)
                    test = True
                except:
                    break

                if test:
                    if  phraseOrigine == 0 :
                        sys.exit()

                    elif phraseOrigine == 1:
                        break

                    else:
                        print("\nLa saisie n'est pas valide")
            if phraseOrigine == 1:
                continue
            phraseOrigine = phraseOrigine.lower()
            phrasePhon = Phrase_to_Phon(phraseOrigine)

            #si un mot n'a pas pu être traduire
            if phrasePhon == False:
                input()
                continue
            # retourne tout les combinaisons de phonemes qui marchent
            liste = mainMixSyllables(phrasePhon, "phon")

            nvListe = {}

            for i in liste[1:]:
                tmp = " ".join(i[0])
                pos1 = i[1][0]
                pos2 = i[2][0]
                # Phon_to_Phrase ("phrase phon" + phrase origine(l))
                nvListe[tmp] = Phon_to_Phrase(tmp, phraseOrigine.split(" "), pos1, pos2)

            test = affiRechFiltre(nvListe,'phon')
            if test == 0:
                sys.exit()
            elif test == 1:
                continue
# ------------------------------------------------------------------------------

    # boucle demande de fin de programme
    tmp = None
    test2 = True
    passeur = 1
    while passeur != 0:
        try:

            tmp = int(input("0 : Quitter / 1 : Retour au début "))
            passeur = 0
        except ValueError:
            print("Entrée invalid veuillez réessayer (Vous devez utiliser des nombres).\n")
        if tmp == 0:
            test2 = False
            boucle = False

        elif tmp == 1:
            test2 = False
            clear()
