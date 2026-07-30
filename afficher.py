import joueurs
import table
import hand
import asyncio
import poker
from nicegui import ui











async def afficher_vote (etape,joueur):
    if etape == 0:
        with joueur.jape :
            ui.label(f"{joueur}, que voulez vous faire")
            t_vote=ui.toggle(joueurs.Joueurs.Vote)
            valide= asyncio.Event()
            ui.button('valider', on_click=valide.set )
            await valide.wait()

        return (t_vote.value)
    if etape ==1:
        with joueur.jape:
            x =ui.number("Quelle mise voulez vous rajouter? :")
            valide = asyncio.Event()
            ui.button('valider', on_click=valide.set)
        await valide.wait()

        return x.value
    if etape ==2:
        ui.label("vous n'avez pas le solde nécessaire",f"vous pouvez miser au maximum {joueur.solde}")
    if etape ==3:
        ui.label("pas un vote autorisé")
    if etape ==4:
        ui.label("vous ne pouvez pas miser plus vous etes désormais en tapis")

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