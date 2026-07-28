import joueurs
import table
import hand

def afficher_vote (etape,joueur):
    if etape == 0:
        print(f"{joueur}, que voulez vous faire")
        print(joueurs.Joueurs.Vote)
        vote_x = input(":")
        return (vote_x)
    if etape ==1:
        x = int(input("Quelle mise voulez vous rajouter? :"))
        return x
    if etape ==2:
        print ("vous n'avez pas le solde nécessaire")
        print(f"vous pouvez miser au maximum {joueur.solde}")
    if etape ==3:
        print("pas un vote autorisé")

def afficher_cartes_joueur(joueur):
        print (joueur.nom,"a :")
        for carte in joueur.cartes:
            print (carte)

def afficher_cartes_table(partie):
        print(table.Table.type_etape[partie.table_partie.etape])
        for i in range (partie.table_partie.etape):
            for j in range (len(partie.table_partie.liste[i])):
                print (partie.table_partie.liste[i][j])

def nb_de_j ():
    x= int(input("Combien de joueurs :"))
    return(int(x))

def nom_solde (i):
    nom_joueur_x= input(f"nom du joueur {i+1}:")
    solde_joueur_x= int(input("Quel est sa solde de départ :"))
    return (nom_joueur_x,solde_joueur_x)

def grand_gagnant (gagnant):
     print(f"le grand gagnant est {gagnant.nom}")
     print(f"il a desormais{gagnant.solde}")

def afficher_solde (joueur):
     print (joueur.nom,"a :")
     print (joueur.solde,"de solde")

def afficher_combo (joueur):
     print (f"{joueur} a :")
     for i in range (len(joueur.cartes_jouee)):
        print (joueur.cartes_jouee[i])
     print (hand.hand.liste_main_s[int(joueur.combo)])

def afficher_pots(table):
    print("le main pot est de",table.main_pot) 