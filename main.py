import os
import subprocess
import csv
import re

# On definit une liste de listes globale
#chaque sous listes represente les deux arguments donnés e demandés par l'enonce
#ex: ["12", "-43"] veut dire quo'n va faire ./prog 12 -43
LISTE_TEST = [["0", "0"],["1", "0"],["0", "1"],["1", "1"],["12", "12"],["12", "-43"],["-1", "-52"]]

def sortie_correct(x, y):
    """
    Entree: on prend 2 entiers
    Sortie:un f-string

    Retourne la sortie attendue pour les deux entiers x et y."""
    return f"La somme de {x} et {y} vaut {int(x) + int(y)}\n" #x et y sont traités comme des entiers pour faire le somme

def test_compilation(nom_fichier):
    """
    Ntree: nom du fichier
    Sortie : etat de compilation , warning etc
    fonction pour compiler le fichier C avec gcc, capture les warnings,
    et renvoie (compile, warnings, stderr).
    """
    resultat= subprocess.run(["gcc", "-Wall", "-ansi", "-o", "prog", nom_fichier],capture_output=True,text=True)#capture output et text permet de recuperer la sortie standard sous forme de chaine
    #subprocess.run permet d'executer la commande gcc -Wall -ansi etc avec le nom_fichier le nom du fichier
    # On compte les warnings en recherchant 'warning:' dans stderr
    warnings = len(re.findall(r"warning:", resultat.stderr))#re.findall cree une liste dans lequel ca compte le nombre de fois ou la chaine "warnings" apparait dans stderr
    compile = (resultat.returncode == 0) and os.path.exists("prog")#renvoie True si la compilation a réussi

    return compile, warnings, resultat.stderr

def test_execution(args):
    """
    Entree:arguments 
    Exécute le binaire 'prog' avec la liste d'arguments args et renvoie stdout.
    On lance la commande ./prog suivi des arguments args
    """
    #subprocess.run va nous permetrre d'executer ./prog avec le nom de l'éxecutable du travail de l'etudiant 
    resultat= subprocess.run(["./prog"] + args, capture_output=True, text=True)
    return resultat.stdout#on renvoie la sortie standard

def nb_ligne_fichier(nom_fichier):
    """
    Entree:fichier
    Sortie:compteur de commentaires
    Compte le nombre de lignes contenant un commentaire
    sur une seule ligne de la forme /* ... */.
    ce sera utilise pour evaluer la documentation
    """
    cmp = 0
    with open(nom_fichier, 'r', encoding='utf-8') as f:#on ouvre le fichier nom_fichier en mode r 
        for line in f:
            if re.search(r"/\*.*\*/", line):#a chaque fois qu'une ligne comprend au moins un de /\*.*\*/
                                            #on incremente cmp
                cmp += 1
    return cmp

def notes(compile, warnings, test_valide, lignes_doc):
    """
    On calcule la note de compilation, la note des tests,
    la note de qualité et la note finale, si la compilation ne passe pas compile vaut 0.
    """
    # Note de compilation (sur 3)
    if not compile:
        note_compil = 0
    else:
        note_compil = 3 - 0.5 * warnings #chaque warning enleve 0.5 points a la note de compil qui vaut 3 à la base
        if note_compil<0:
            note_compil=0 #on veille à ce que la note ne soit pas negative 

    # le nombre de tests corrects multiplié par 5/7) SSI ca a bien compile sinon on fait rien
    note_test = test_valide * (5 / 7) if compile else 0

    # Note de qualité (sur 2), max 2 points
    qualite_code = min(lignes_doc * (2/3),2)#chaque commentaire rapporte 2/3 de points
    #si on a plus de  3 commentaires alors on a une note de 2, DONC SI L'ELEVE A FAIT TROP DE COMMENTAIRE ALORS IL A QUAND MEME 2!
    note_final = note_compil + note_test + qualite_code
    return note_compil, note_final

def transforme_fichier(nom_fichier):
    """
    Entree:nom_fichier
    Sortie: une liste sous la forme[prenom, nom, temoin_exec, warnings, test_valide,
    lignes_doc, note_compil, note_final]

    Traite un fichier source .c :
    -On extrait prénom et nom
    - Compilation
    - Exécution des tests si compilé
    - Comptage des commentaires
    - Calcul et formatage des notes
    """
    base = os.path.splitext(nom_fichier)[0]#commande pour retirer l'extension .c
    prenom, nom = base.split("_") #on split le _ pour avoir un joli {prenom nom}

    
    compile, warnings, gcc_out = test_compilation(nom_fichier)#on compile le fichier reçu , si tout va bien
                                                          #on le recupere avec le nb de warnings et le stderr  
    
    temoin_exec = 1 if compile else 0#egale a 1 si ca a bien compile sinon on fait rien

    #tests
    test_valide = 0
    if compile:#si la compilation a reussi alors on peut lui accorder notre temps et lui faire une batterie de tests d'executions ,on parcout tests_cases et on lui fait un test
        for args in LISTE_TEST:
            output = test_execution(args)
            # Compare la sortie obtenue à la sortie attendue
            if output == sortie_correct(args[0], args[1]):#si la sortie correspond à la sortir censé etre correct on incrmeente test_valide
                test_valide += 1

    # on compte les lignes 
    lignes_doc = nb_ligne_fichier(nom_fichier)

    
    note_compil, note_final = notes(compile, warnings, test_valide, lignes_doc)#on calucle la note de compilation de test et qualite puis la somme finale
    
    note_final = f"{note_final:.2f}".replace('.', ',')#on met la note en 2f(2 decimales) et on remplace le point par une virgule

    return [prenom, nom, temoin_exec, warnings, test_valide, lignes_doc, note_compil, note_final]
    #ce sera affiche dans le excel dans cet ordre ci-dessus

def main():
    """
    Parcourt le répertoire courant pour trouver tous les fichiers .c,
    traite chacun d'eux et génère le fichier resultats.csv
    """
    fichiers = []
    for f in os.listdir("."):
        if f.endswith(".c"):
            fichiers.append(f)
    #on liste tous les fichiers du repertoire courant SI il se termine par .c
    

    with open("resultats.csv", "w", newline='', encoding="utf-8") as csvfile:# On ouvre le fichier "resultats.csv" en mode écriture ("w"). L'argument newline='' empêche Python d'ajouter automatiquement des retours à la ligne supplémentaires,
# ce qui est très important pour le format CSV.
        writer = csv.writer(csvfile, delimiter=",", quoting=csv.QUOTE_MINIMAL)#on cree un writer csv
        for nom_fichier in fichiers:#on parcourt les fichiers dans notre liste de fichiers
            resultat = transforme_fichier(nom_fichier)#on transforme le fichier prenom.nom.c en prenom nom note .....
            writer.writerow(resultat)#commande pour ecrire le resultat dans le CSV

    print("Fichier CSV généré : resultats.csv")

if __name__ == "__main__":
    main()
