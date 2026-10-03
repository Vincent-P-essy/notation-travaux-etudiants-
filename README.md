# TP Noteur de Fichiers C

Ce projet automatise la compilation, les tests et l’évaluation de plusieurs programmes en C. Il génère un fichier `resultats.csv` contenant, pour chaque étudiant :

- **Prénom** et **nom**  
- **Succès** de la compilation (1 = OK, 0 = KO)  
- **Nombre de warnings**  
- **Nombre de tests réussis**  
- **Nombre de lignes de documentation détectées**  
- **Note de compilation** (sur 3)  
- **Note finale** (sur 10)

---

##  Structure du dépôt

```
.
├── main.py               # Script Python principal
├── resultats.csv         # (généré) tableau des résultats
├── *.c                   # Sources C des étudiants
└── README.md             # Documentation du projet
```

---

##  Prérequis

- Python 3.x  
- GCC (avec les drapeaux `-Wall` et `-ansi`)  
- Modules Python standards (`subprocess`, `csv`, `re`, `os`)

---

##  Utilisation

1. **Cloner le dépôt**  
   ```bash
   git clone https://github.com/tonuser/tp-noteur.git
   cd tp-noteur
   ```

2. **Ajouter les fichiers `.c`**  
   Place tous les fichiers sources C (`Prenom_Nom.c`) dans le même répertoire que `main.py`.

3. **Exécuter le script**  
   ```bash
   python3 main.py
   ```
   Cela compile chaque `.c`, lance 7 jeux de tests, compte les lignes de commentaires et produit `resultats.csv`.

4. **Consulter les résultats**  
   Ouvre `resultats.csv` avec Excel, LibreOffice Calc, ou tout éditeur de texte.

---

##  Détails techniques

- **Compilation**  
  - Options : `-Wall -ansi`  
  - Chaque warning retire 0,5 pt sur la note de compilation (max 3 pts).

- **Tests**  
  - 7 paires d’arguments prédéfinies  
  - Chaque test réussi apporte `5/7` pts (max 5 pts).

- **Documentation**  
  - Chaque commentaire `/* ... */` compte pour 2/3 pt (max 2 pts).

- **Calcul de la note finale**  
  ```text
  note_finale = note_compil (0–3) + note_tests (0–5) + note_doc (0–2)  # Total sur 10 pts
  ```

---

##  Personnalisation

- Pour modifier les cas de tests, édite la liste `LISTE_TEST` en début de `main.py`.  
- Pour ajuster le barème, change la fonction `notes()`.

---

##  Licence

MIT — libre de réutiliser et d’adapter.
