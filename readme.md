# Poker en ligne (NiceGUI)

Application web de Texas Hold'em multijoueur, construite avec [NiceGUI](https://nicegui.io/) (Python).

## Prérequis

- Python 3.8 ou supérieur (version minimale requise par NiceGUI)
- NiceGUI :
  ```bash
  pip install nicegui
  ```
- Un dossier `cartes_j/` à la racine du projet, contenant les images des cartes, organisé par couleur :

  ```
  cartes_j/
  ├── pique/
  │   ├── 1.png
  │   ├── 2.png
  │   ...
  │   └── 13.png
  ├── trefle/
  │   └── ...
  ├── carreau/
  │   └── ...
  └── coeur/
      └── ...
  ```

  Les valeurs vont de 1 à 13, où 1 = "2" et 13 = As.

## Lancer l'application

```bash
python poker_copie.py
```

Puis ouvrir l'adresse indiquée dans le terminal (par défaut `http://localhost:8080`) dans un navigateur.

## Comment jouer

1. Sur la page d'accueil, indiquer le nombre de joueurs puis valider.
2. Entrer le nom et le solde de départ de chaque joueur.
3. Cliquer sur **Démarrer la partie** — ça ouvre la page `/jeu`, qui sert de vue "table" commune (visible par tout le monde).
4. Chaque joueur doit ouvrir son propre onglet via le bouton portant son nom (il s'ouvre dans un nouvel onglet) : c'est là qu'il voit ses cartes et peut voter.
5. La main se déroule automatiquement : pré-flop, flop, turn, river, puis distribution des gains.

## Structure du projet

| Fichier | Rôle |
|---|---|
| `poker_copie.py` | Point d'entrée principal : pages NiceGUI (accueil, table, vue joueur) |
| `partie.py` | Logique de la partie : distribution, blinds, mises, votes, calcul du gagnant, répartition des pots |
| `joueurs.py` | Classe `Joueurs` |
| `cartes.py` | Classe `Cartes` et création du paquet |
| `table.py` | Classe `Table` (board, étape de jeu, pot) |
| `hand.py` | Évaluation des mains de poker (paire, suite, couleur, full, etc.) |
| `afficher.py` | Fonctions d'affichage côté interface |

`poker.py` et `main.py` sont d'anciennes versions (interface console / architecture antérieure), conservées pour référence mais non utilisées par le flux de jeu actuel.

## Règles implémentées

- Texas Hold'em classique (2 cartes privées + 5 cartes communes)
- Petite et grosse blind postées automatiquement, attribuées aléatoirement à deux joueurs à chaque main
- Mises, suivis, relances, couchers, tapis (all-in)
- Side pots en cas d'all-in à des montants différents entre joueurs
- Classement complet des mains, y compris la quinte et la quinte flush à l'As bas ("la roue", As-2-3-4-5)
- Départage des égalités par les cartes kicker

## Limitations connues

- Chaque lancement ne joue qu'**une seule main** : le bouton "Rejouer" repasse par l'écran de configuration, et les soldes ne sont pas conservés automatiquement d'une main à l'autre.
- Pas de détection de fin de partie (dernier joueur restant avec des jetons). Cette limitation ne se manifeste que si une boucle multi-mains est mise en place : dans le fonctionnement actuel (une seule main par lancement, soldes ressaisis à chaque fois), elle n'a pas d'effet concret.
- Une seule partie peut être active à la fois sur le serveur (`partie_x` est une variable globale partagée par tous les joueurs connectés).