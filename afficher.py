import joueurs
import table
import hand
import asyncio
from nicegui import ui
from pathlib import Path











async def afficher_vote (etape,joueur):
    if etape == 0:
        joueur.a_vote = asyncio.Event()
        if joueur.zone_jeu:
            joueur.zone_jeu.refresh(0)
        await joueur.a_vote.wait()
        return joueur.reponse_vote
    
    if etape ==1:
        joueur.a_vote = asyncio.Event()
        if joueur.zone_jeu:
            joueur.zone_jeu.refresh(1)
        await joueur.a_vote.wait()
        return joueur.mise_v
    
    if etape ==2:
        joueur.zone_jeu.refresh(2)
    if etape ==3:
        joueur.zone_jeu.refresh(3)
    if etape ==4:
        joueur.zone_jeu.refresh(4)

def afficher_cartes_joueur(partie):
        for joueur in partie.L_joueurs:
                joueur.cartes_jouables = hand.hand(joueur.cartes, partie.table_partie)
                joueur.combo, joueur.cartes_combo, joueur.cartes_kicker = joueur.cartes_jouables.analyse_main()
                joueur.cartes_jouee = joueur.cartes_combo+joueur.cartes_kicker
        for j in partie.L_joueurs:
            if j.zone_entete:
                j.zone_entete.refresh()
                

def afficher_cartes_table(partie,etape):
        partie.table_partie.jape.clear()
        with partie.table_partie.jape:
            if etape==0:
                ui.label(f"le main pot est : {partie.table_partie.main_pot}")
                ui.label(table.Table.type_etape[partie.table_partie.etape])
                with ui.row():
                    for i in range (partie.table_partie.etape):
                        for j in range (len(partie.table_partie.liste[i])):
                                ui.image(Path('cartes_j')/str(partie.table_partie.liste[i][j].couleur)/f"{partie.table_partie.liste[i][j].valeur}.png").style('width: 120px')
            elif etape==1:
                if len(partie.L_gagnants)== 1 :
                    ui.label(f"le grand gagnant est {partie.L_gagnants[0].nom}")
                    with ui.row():
                        for i in range (len(partie.L_gagnants[0].cartes_jouee)):
                            ui.image(Path('cartes_j')/str(partie.L_gagnants[0].cartes_jouee[i].couleur)/f"{partie.L_gagnants[0].cartes_jouee[i].valeur}.png").style('width: 120px')
                    ui.label (hand.hand.liste_main_s[int(partie.L_gagnants[0].combo)])
                else:
                    ui.label("Les gagnants sont : " )
                    for j in partie.L_gagnants:
                        with ui.row():
                            ui.label(j.nom)
                    for j in partie.L_gagnants:
                        ui.label(f"{j.nom} avait :")
                        with ui.row():
                            for i in range (len(j.cartes_jouee)):
                                ui.image(Path('cartes_j')/str(j.cartes_jouee[i].couleur)/f"{j.cartes_jouee[i].valeur}.png").style('width: 120px')
                        ui.label (hand.hand.liste_main_s[int(j.combo)])

        for j in partie.L_joueurs:
            if j.zone_entete is not None:
                j.zone_entete.refresh()
        

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
