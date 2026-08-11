import joueurs
import table
import hand
import asyncio
import poker
from nicegui import ui
from pathlib import Path











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
            x =ui.number("Quelle mise voulez vous rajouter? :",value =10,step=10)
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

def afficher_cartes_joueur(partie):
        for joueur in partie.L_joueurs:
                joueur.cartes_jouables = hand.hand(joueur.cartes, partie.table_partie)
                joueur.combo, joueur.cartes_jouee = joueur.cartes_jouables.analyse_main()
        for j in partie.L_joueurs:
            j.jape.clear()
            with j.jape:
                ui.label(f"{j.nom} : solde {j.solde}" )
                ui.label(f"mise : {j.mise}")
                row= ui.row()
                with row:
                    for i in range (len(j.cartes)):
                        ui.image(Path('cartes_j')/str(j.cartes[i].couleur)/f"{j.cartes[i].valeur}.png").style('width: 120px')
                ui.label (hand.hand.liste_main_s[int(j.combo)])
                

def afficher_cartes_table(partie):
        partie.table_partie.jape.clear()
        with partie.table_partie.jape:
            ui.label(f"le main pot est : {partie.table_partie.main_pot}")
            ui.label(table.Table.type_etape[partie.table_partie.etape])
            for i in range (partie.table_partie.etape):
                for j in range (len(partie.table_partie.liste[i])):
                    ui.image(Path('cartes_j')/str(partie.table_partie.liste[i][j].couleur)/f"{partie.table_partie.liste[i][j].valeur}.png").style('width: 120px')

def nb_de_j ():
    x= int(input("Combien de joueurs :"))
    return(int(x))

def nom_solde (i):
    nom_joueur_x= input(f"nom du joueur {i+1}:")
    solde_joueur_x= int(input("Quel est sa solde de départ :"))
    return (nom_joueur_x,solde_joueur_x)

def grand_gagnant (gagnant):
    ui.label(f"le grand gagnant est {gagnant.nom}")
    with ui.row():
        for i in range (len(gagnant.cartes_jouee)):
            ui.image(Path('cartes_j')/str(gagnant.cartes_jouee[i].couleur)/f"{gagnant.cartes_jouee[i].valeur}.png").style('width: 120px')
    ui.label (hand.hand.liste_main_s[int(gagnant.combo)])

def afficher_solde (joueur):
     print (joueur.nom,"a :")
     print (joueur.solde,"de solde")

def afficher_combo (joueur):
     print (f"{joueur} a :")
     for i in range (len(joueur.cartes_jouee)):
        print (joueur.cartes_jouee[i])
     print (hand.hand.liste_main_s[int(joueur.combo)])
