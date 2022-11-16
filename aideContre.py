import sys
import json
import os
from filtre import *
from fonc_aide_son import *
from fonc_aide_lettre import *

sys.stdout.reconfigure(encoding='utf-8')

def aideContrepetrie():
    with open('data/config.json') as diconfig_:
        diconfig = json.load(diconfig_)

    # boucle "tant que" pour le recommencer aide avec un autre mot.
    continuer = 1

    while continuer == 1:
        Linput = input("Mot : ")
        mot = Linput
        mot = mot.lower()

        # case rech sur une lettre
        # ou   rech sur une syllabe

        listeDeMotCop = []
        choix = set(range(5))
        print("""Voulez-vous faire une recherche sur :
            1- une lettre
            2- un  son
            3- plusieurs lettres
            4- plusieurs sons
            0- quitter l'aide""")

        while True:
            try:
                selection = int(input(""))
            except:
                print("\nVous n'avez pas saisi un chiffre")
                continue
            if selection in choix:
                break
            else:
                print("\nL'entrée n'est pas valide, réessayez")

        # selection des différents mode de l'aide
        if selection == 0:
            continuer = 0
            break
    # -------------------------------------------------------------------------------
        elif selection == 1:
            clear()
            print("Recherche des contrepétries possibles ...")
            listeDeMotCop = aideLettreSubs(mot)
    # -------------------------------------------------------------------------------

        elif selection == 2:
            clear()
            print("Recherche des contrepétries possibles ...\n")
            listeDeMotCop = aideSonSubs(mot)
            # cas où le mot rentré par l'utilisateur n'est pas dans le lexique
            if listeDeMotCop == 0:
                continue
    # -------------------------------------------------------------------------------

        elif selection == 3:
            clear()
            print(f"Recherche des échanges possibles sur les différentes tranches :")
            print("\nChargement en cours...\n")

            sliceCorr = aideSyllSubs(mot)
            # si les tranches n'avait pas de correspondance:
            if isinstance(sliceCorr, bool):
                clear()
                print("Ce mot n'est pas dans notre lexique, nous ne pouvons pas trouver son phonème.\n")
                continue
            else:
                while(True):
                    syllOrigine = affiNbCorrTranche(sliceCorr)
                    if syllOrigine == 0:
                        return 0
                    elif syllOrigine == -1:
                        clear()
                        break

                    selectMot = affiPageParPage(sliceCorr[syllOrigine], syllOrigine, mot)
                    if selectMot == 0:
                        return 0
                    elif selectMot == -1:
                        clear()
                        break
                    elif isinstance(selectMot, str):
                        break
                if syllOrigine == -1 or selectMot == -1:
                    continue
    # -------------------------------------------------------------------------------

        elif selection == 4:
            clear()
            print(f"Recherche des échanges possibles sur les différentes tranches :")
            print("\nChargement en cours...\n")

            sliceCorr = aideMultiSonSubs(mot)

            # si les tranches n'avait pas de correspondance:
            if isinstance(sliceCorr, bool):
                clear()
                print("Ce mot n'est pas dans notre lexique, nous ne pouvons pas trouver son phonème.\n")
                continue
            else:

                while(True):
                    syllOrigine = affiNbCorrTranche2(sliceCorr)
                    if syllOrigine == 0:
                        return 0
                    elif syllOrigine == -1:
                        clear()
                        break

                    selectMot = affiPageParPage2(sliceCorr[syllOrigine], syllOrigine, mot)
                    if selectMot == 0:
                        return 0
                    elif selectMot == -1:
                        clear()
                        break
                    elif isinstance(selectMot, str):
                        break
                if syllOrigine == -1 or selectMot == -1:
                    continue
    # -------------------------------------------------------------------------------
        if selection == 1 or selection == 2:

            # affichage des premiers resultats
            for i in enumerate(listeDeMotCop):
                tmp = i[1][2] if i[1][2] != "" else chr(32)
                if selection == 1:
                    print(f" {i[0]+1}   {i[1][1]} - {tmp}    {i[1][0]}")
                else:
                    if (i[0]+1)<10:
                        print(f"{i[0]+1}   {i[1][1]} - {tmp}    {i[1][0]} ex : {i[1][3]}")
                    else:
                        print(f"{i[0]+1}  {i[1][1]} - {tmp}    {i[1][0]} ex : {i[1][3]}")

            selectMot = None
            boucle = True
            while(boucle):
                try:
                    selectMot = int(input(
                        "\n0 = quitter l'aide,-1 revenir au début de l'aide \nou numéro de l'échange qui vous intéresse : \n"))
                except:
                    print("\nVous n'avez pas saisi un chiffre")
                    continue

                if selectMot == 0:
                    continuer = 0
                    break
                elif selectMot == -1:
                    clear()
                    continuer = -1
                    boucle = False
                elif selectMot <= len(listeDeMotCop) and selectMot > 0:
                    boucle = False
                else:
                    print("\nL'entrée n'est pas valide, réessayez")

            if continuer == -1:
                continuer = 1
                continue
            elif continuer == 0:
                continue

        # affichage affiné sur contrepetrie choisie
        if selection == 1:

            listeAffichage, compteur, diconfig = aideLettreRechDico(selectMot, listeDeMotCop)

            # en cas de liste vide, affichant qu'aucune possibilité n'est trouvé
            if listeAffichage != []:
                # ici enlever if(filtregrammaticale) ->listeAffichage =  f('listeAffichage')
                if (diconfig["FiltreGrammatical"] == "Oui"):
                    listeAffichage = GramFiltre(listeAffichage, mot)
                continuer = affiRechLettre(listeAffichage, compteur, mot)
            else:
                print("Aucune correspondance trouvée")

        elif selection == 2:
            (listeAffichage, compteur, diconfig) = aideSonRechDico(selectMot, listeDeMotCop)

            # en cas de liste vide, affichant qu'aucune possibilité n'est trouvé
            if listeAffichage != []:
                if (diconfig["FiltreGrammatical"] == "Oui"):
                    listeAffichage = GramFiltre(listeAffichage, mot)
                # ici enlever if(filtregrammaticale) ->listeAffichage =  f('listeAffichage')

                continuer = affiRechSon(listeAffichage, compteur, mot)
            else:
                print("Aucune correspondance trouvée")

        elif selection == 3:
            (listeAffichage, compteur, diconfig) = aideSyllRechDico(mot, selectMot, syllOrigine)
            if (diconfig["FiltreGrammatical"] == "Oui"):
                listeAffichage = GramFiltre(listeAffichage, mot)
            # ici enlever if(filtregrammaticale) ->listeAffichage =  f('listeAffichage')
            continuer = affiRechLettre(listeAffichage, compteur, mot)

        elif selection == 4:

            (listeAffichage, compteur, diconfig) = aideMultiSonRechDico(mot, selectMot, syllOrigine)

            if (diconfig["FiltreGrammatical"] == "Oui"):
                listeAffichage = GramFiltre(listeAffichage, mot)
            # ici enlever if(filtregrammaticale) ->listeAffichage =  f('listeAffichage')
            continuer = affiRechSon(listeAffichage, compteur, mot)

    return 0
