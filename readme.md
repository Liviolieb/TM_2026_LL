# Poker Texas Hold'em en ligne (NiceGUI)

Application web de Texas Hold'em pour 2 à 10 joueurs, construite avec [NiceGUI](https://nicegui.io/) (Python). Chaque joueur joue depuis son propre onglet, et une vue commune affiche la table.

## Prérequis

- **Python** récent (le projet a été développé avec Python 3.14). La version minimale dépend de celle de NiceGUI : `pip` refusera l'installation si votre Python est trop ancien.
- **NiceGUI**, dans une version récente (le projet utilise `ui.html(..., sanitize=False)`) :
  ```bash
  pip install nicegui
  ```
- Un dossier `cartes_j/`, placé dans le même dossier que les fichiers `.py`, contenant les images des cartes et le dos des cartes :

  ```
  cartes_j/
  ├── verso.png          # dos des cartes
  ├── pique/
  │   ├── 1.png
  │   ├── 2.png
  │   ...
  │   └── 13.png
  ├── trefle/
  ├── carreau/
  └── coeur/
  ```

  Les valeurs vont de 1 à 13, où **1 = « 2 »** et **13 = As**.

## Lancer l'application

Depuis le dossier du projet :

```bash
python pokerv3.py
```

Puis ouvrir `http://localhost:8080` dans un navigateur.

## Comment jouer

1. Sur la page d'accueil, indiquer le nombre de joueurs (2 à 10) puis valider.
2. Saisir le nom et le solde de départ de chaque joueur. Les noms doivent être **différents** (sans tenir compte des majuscules) et **ne pas contenir de `/`**.
3. Cliquer sur **Démarrer la partie**. Ça ouvre `/jeu`, la vue commune de la table.
4. Chaque joueur ouvre **sa propre page** en cliquant sur son nom, dessiné sur la table (la page s'ouvre dans un nouvel onglet). C'est là qu'il voit ses cartes et qu'il vote.
5. La main démarre quand tous les joueurs ont ouvert leur page. Le serveur attend chaque joueur 60 secondes, l'un après l'autre ; celui qui n'a toujours pas ouvert sa page est couché d'office.
6. La main se déroule : pré-flop, flop, turn, river, puis showdown et distribution des gains.

### Les actions

| Action | Effet |
|---|---|
| **Relancer** | Suit la mise, puis demande un montant supplémentaire. |
| **Suivre** | Paie ce qu'il manque pour égaler la mise. Si le solde ne suffit pas, le joueur met tout ce qu'il lui reste (tapis). |
| **Coucher** | Abandonne la main. Cette option n'est pas proposée quand il n'y a rien à payer. |
| **Tapis** | Mise tout le solde. |

Chaque décision doit être prise en **60 secondes**. Sans réponse, le joueur suit automatiquement s'il n'a rien à payer, sinon il est couché. Un montant de relance non saisi à temps compte pour 0.

### Lire la table

- Votre siège est toujours **en bas** ; les autres joueurs sont placés autour dans l'ordre de jeu.
- Le nombre au-dessus d'un nom est son **solde**. Les jetons posés devant lui représentent sa **mise** du tour (1 blanc, 10 bleu, 50 vert, 100 noir, 500 violet).
- Un cercle bleu qui tourne indique le joueur dont c'est le tour.
- Un disque blanc marqué **D** indique le donneur.
- Un joueur couché n'a plus de cartes affichées (il reste les deux cadres vides).
- Au showdown, les cartes des joueurs encore en jeu sont révélées. Les cartes du ou des gagnants, et celles du board qui composent leur main, sont entourées en doré. Si tous les autres joueurs se sont couchés, les cartes du gagnant restent cachées.
- À la fin de la main, le texte sous le board (là où s'affichait l'étape) annonce le ou les gagnants et leur combinaison, ou « remporte le pot » quand tous les autres joueurs se sont couchés.

### Sur votre page

Un panneau semi-transparent en haut à gauche regroupe :

- votre nom ;
- **A suivre** : ce qu'il vous faut payer pour égaler la mise de la table ;
- le **pot principal** ;
- **Vous pouvez jouer** : la meilleure combinaison que vous pouvez former avec vos cartes et celles déjà visibles sur le board ;
- les badges **Couché** et **Tapis** quand ils s'appliquent ;
- quand c'est votre tour, les commandes de vote (choix de l'action, bouton **valider**) et le décompte du temps restant.

## Règles implémentées

- Texas Hold'em classique : 2 cartes privées et 5 cartes communes (flop de 3, turn, river).
- Petite blinde de 10 et grosse blinde de 20, postées automatiquement : la petite blinde est tirée au hasard parmi les joueurs, la grosse blinde est le joueur suivant. Le pré-flop commence après la grosse blinde. Le donneur est le joueur juste avant la petite blinde (à deux joueurs, la petite blinde elle-même) : après le flop, le turn et la river, la parole commence au premier joueur encore en jeu après lui.
- Mises, suivis, relances, couchers et tapis.
- Si tous les joueurs sauf un se couchent avant la fin, la main s'arrête : le joueur restant gagne le pot et les cartes du board qui n'avaient pas encore été dévoilées restent cachées.
- **Side pots** quand des joueurs sont au tapis pour des montants différents. Un palier auquel plus aucun joueur encore en jeu n'a contribué est remboursé.
- Classement complet des mains : carte haute, paire, double paire, brelan, suite, couleur, full, carré, quinte flush et quinte flush royale. La suite et la quinte flush à l'As bas (As-2-3-4-5, « la roue ») sont gérées.
- Départage des égalités par les valeurs des cartes de la combinaison, puis par les kickers. En cas d'égalité parfaite, le pot est partagé, et les jetons restants sont donnés un par un aux premiers gagnants.

## Structure du projet

| Fichier | Rôle |
|---|---|
| `pokerv3.py` | Point d'entrée : pages NiceGUI (accueil `/`, vue commune `/jeu`, vue joueur `/jeu/{nom}`) |
| `partie.py` | Logique de la partie : distribution, blindes, tours de vote, gagnant, répartition des pots |
| `joueurs.py` | Classe `Joueurs` |
| `cartes.py` | Classe `Cartes` et création du paquet |
| `table.py` | Classe `Table` (board, étape de jeu, pot, mise courante) |
| `hand.py` | Évaluation des mains (paire, suite, couleur, full, etc.) |
| `afficher.py` | Rafraîchissement de l'interface et attente des votes (avec décompte) |
| `table_svg.py` | Dessin de la table en SVG (sièges, cartes, jetons, noms) |

Le dossier `archive/` contient d'anciennes versions (`pokerv1.py`, `pokerv2.py`, `main.py` : première page de test, interface sans SVG, mode console). Elles ne fonctionnent plus avec le code actuel et sont conservées uniquement pour référence.

## Réglages

| Valeur | Où la modifier |
|---|---|
| Blindes (10 / 20) | `Petite_blind` et `Grosse_blind` dans `partie.py` |
| Durée d'un vote (60 s) | `TIMEOUT_VOTE` dans `afficher.py` |
| Valeurs et couleurs des jetons | `DENOMS` dans `table_svg.py` |

## Limitations connues

- Chaque lancement ne joue qu'**une seule main** : le bouton « Rejouer » ramène à la page de configuration, et les soldes ne sont pas conservés d'une main à l'autre.
- Il n'y a **pas de détection de fin de partie** (dernier joueur ayant encore des jetons). Elle n'aurait de sens qu'avec plusieurs mains à la suite.
- Le donneur est fixé une fois pour la main (déduit de la petite blinde) : comme il n'y a qu'une main par lancement, il n'y a pas de rotation du bouton d'une main à l'autre.
- Une seule partie peut être active à la fois (`partie_x` est une variable globale du serveur). Démarrer une partie pendant qu'une main est en cours redirige vers la partie existante.