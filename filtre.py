import language_tool_python
import json
import os
from arbin import *
"""
Efface le terminal ou met une série de \n pour simuler un éffacement du terminal
selon fichier config.json
"""

def clear():
    with open('data/config.json','r') as diconfig_:
        diconfig = json.load(diconfig_)

        if diconfig["EffacerComplétement"] == "Oui":
            os.system('clear') if os.name == 'posix' else os.system('clear')
        else :
            print("\n"*60)
#-------------------------------------------------------------------------------
"""
Modifie le fichier de configuration des filtres.
"""
def configFiltre():
    with open('data/config.json','r') as diconfig_:
        diconfig = json.load(diconfig_)
        n = input("\nActiver filtre Grammaticale\n(1:Oui/0:Non/autre:defaut):")
        if n == '1':
            diconfig["FiltreGrammatical"] = "Oui"
        elif n == '0':
            diconfig["FiltreGrammatical"] = "Non"

        n = input("\nActiver filtre Grossier\n(1:Oui/0:Non/autre:defaut):")
        if n == '1':
            diconfig["FiltreGrossier"] = "Oui"
        elif n == '0':
            diconfig["FiltreGrossier"] = "Non"

        n = input("\nActiver effaçage définitif (empêche de voir les saisies précèdantes)\n(1:Oui/0:Non/autre:defaut):")
        if n == '1':
            diconfig["EffacerComplétement"] = "Oui"
        elif n == '0':
            diconfig["EffacerComplétement"] = "Non"
    print("\n")
    for i in diconfig.keys():
        print(f"{i}  -  {diconfig[i]}")
    with open('data/config.json','w') as diconfig_:
        json.dump(diconfig,diconfig_)

#-------------------------------------------------------------------------------

def changerfiltre(diconfig):
    n = input("\nActiver filtre Grammaticale\n(1:Oui/0:Non/n'importe quelle clef:défaut):")
    if n == '1':
        diconfig["FiltreGrammatical"] = "Oui"
    elif n == '0':
        diconfig["FiltreGrammatical"] = "Non"

    n = input("\nActiver filtre Grossier\n(1:Oui/0:Non/n'importe quelle clef:défaut):")
    if n == '1':
        diconfig["FiltreGrossier"] = "Oui"
    elif n == '0':
        diconfig["FiltreGrossier"] = "Non"

    print("\n")
    return diconfig
#-------------------------------------------------------------------------------

"""
Applique les filtres et affiche les résultats en fonctions de la config
donnée par l'utilisateur
"""
def affiRechFiltre(nvDico,mode):

    with open('data/config.json') as diconfig_:
        diconfig = json.load(diconfig_)

    print('\nTraitement en cours ...')
    diconfig = changerfiltre(diconfig)


    if mode == 'phon':
        if diconfig["FiltreGrossier"] == "Oui":
            nvDico = filtreMix(nvDico)
        count1 = 0
        count2 = 0
        for key in nvDico:
            count1 += len(nvDico[key])

        StockPourkey = ""
        compteur = -1
        dicores = []

        for key in nvDico:

            if diconfig["FiltreGrammatical"] == "Oui":

                for j in nvDico[key]:
                    j = ' '.join(j)
                    if j[0] == " ":
                        j = j[1:]
                    j = j.capitalize()
                    compteur += 1

                    if StockPourkey != key and len(language_tool_python.LanguageToolPublicAPI('fr').check(j)) == 0:
                        print(compteur, " -->", j)
                        StockPourkey = key
                        dicores.append(key)
                    else:
                        compteur -= 1

            else:
                for j in nvDico[key]:
                    j = ' '.join(j)
                    if j[0] == " ":
                        j = j[1:]
                    j = j.capitalize()
                    compteur += 1
                    if StockPourkey != key:
                        print(compteur, " -->", j)
                        StockPourkey = key
                        dicores.append(key)
                    else:
                        compteur -= 1

        choixutilisateur = 1
        while choixutilisateur in range(compteur):
            try:
                choixutilisateur = int(input(
                "\n-1 : quitter/ -2 revenir au menu principal ou \nChiffre pour ortographe\n"))
            except:
                print("\nVous n'avez pas saisi un chiffre")
                continue
            if (choixutilisateur) <= compteur and choixutilisateur > -1:
                for j in nvDico[dicores[choixutilisateur]]:
                    j = ' '.join(j)
                    if j[0] == " ":
                        j = j[1:]
                    j = j.capitalize()
                    if diconfig["FiltreGrammatical"] == "Oui":
                        matches = language_tool_python.LanguageToolPublicAPI('fr').check(j)
                        if len(matches) == 0:
                            print(j)
                    else:
                        print(j)

            elif choixutilisateur == -1:
                return 0
            elif choixutilisateur == -2:
                return 1
            else:
                print("Pas de résultat")

    if mode == 'word':
        #attention, ici nvDico est une liste de tuple, plus un dico
        #filtrage par grammaire de la phrase
        nvListe = [nvDico[0]]
        if diconfig["FiltreGrossier"] == "Non" and diconfig["FiltreGrammatical"] == "Non":
            for i in nvDico[1:]:
                nvListe.append(" ".join(i[0]))
            return nvListe

        with open('data/DicoVulgaire.json') as vulgaire:
            BDvulgaire = json.load(vulgaire)

        if diconfig["FiltreGrammatical"] == "Oui":
            for contrepet in nvDico[1:]:
                str = " ".join(contrepet[0])
                j = str.capitalize()

                if len(language_tool_python.LanguageToolPublicAPI('fr').check(j)) == 0:
                    nvListe.append(contrepet)

        tmpListe = []
        if diconfig["FiltreGrammatical"] == "Oui":
            tmpListe = nvListe[:]
            nvListe = [nvListe[0]]
        else:
            tmpListe =  nvDico[:]
        #filtrage par mot vulgaires
        for contrepet in tmpListe[1:]:
            if diconfig["FiltreGrossier"] == "Oui":
                test = False
                for i in contrepet[0]:
                    if i in BDvulgaire:
                        test = True
                        break
                if test:
                    nvListe.append(" ".join(contrepet[0]))
            else :
                nvListe.append(" ".join(contrepet[0]))
        return nvListe


# -------------------------------------------------------------------------------
"""
Filtre depuis un dictionnaire de phrase, garde toutes les phrases contenant
au moins un mot vulgaire.
"""
def filtreMix(dicoResult):

    with open('data/DicoVulgaire.json') as vulgaire:
        BDvulgaire = json.load(vulgaire)

    dicoFiltre = {}
    for key in dicoResult:
        tmpListe = []

        dicoTmp = dicoResult[key]
        for i in range(len(dicoTmp)):
            test1 = False

            for value in dicoTmp[i]:
                # test si le contrepet contient un mot vulgaire
                if value in BDvulgaire:
                    test1 = True
                    break

            if test1:
                tmpListe.append(dicoTmp[i])

        if tmpListe != []:
            dicoFiltre[key] = tmpListe

    return dicoFiltre

#-------------------------------------------------------------------------------
"""
filtre pour l'aide à la contrepétrie.
retourne une liste de quadruplets dont tous les élèments sont de la même classe Grammaticale

/!\ ne fonctionne pas correctement car Mot_to_Phon n'est pas adapté.
"""
def GramFiltre(listeOrgine, mot_origine):
    nouvelleListe = []

    for pack in listeOrgine:
        mot1 = Mot_to_Phon(arbre_mot, mot_origine)
        mot2 = Mot_to_Phon(arbre_mot, pack[4])
        mot3 = Mot_to_Phon(arbre_mot, pack[2])
        mot4 = Mot_to_Phon(arbre_mot, pack[3])
        if mot1 is not False and mot2 is not False and mot3 is not False and mot4 is not False:
            if mot1.split(",")[1] == mot2.split(",")[1] and mot3.split(",")[1] == mot4.split(",")[1]:
                nouvelleListe.append(pack)
    return nouvelleListe
