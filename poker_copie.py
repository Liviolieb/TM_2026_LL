import partie
import joueurs
import afficher
import hand
import table
from nicegui import ui
from pathlib import Path

partie_x =None
@ui.page('/')
def accueil():
    ui.label("Configuration de la partie").style('font-size: 1.5em')
    nb_joueurs_input = ui.number('Combien de joueurs :', value=3, min=2, max=10)

    champ_joueurs = ui.column()
    champs = [] 

    def generer_champs():
        bouton_j.delete()
        champ_joueurs.clear()
        champs.clear()
        nb = int(nb_joueurs_input.value)
        nb_joueurs_input.delete()
        with champ_joueurs:
            for i in range(nb):
                with ui.row():
                    input_nom = ui.input(f"Nom du joueur {i + 1}")
                    input_solde = ui.number(f"Solde du joueur {i + 1}", value=1000,step=10)
                champs.append((input_nom, input_solde))

    bouton_j=ui.button("Valider le nombre de joueurs", on_click=generer_champs)

    resultat = ui.column()

    def demarrer_partie():
        global partie_x
        if partie_x is not None and partie_x.table_partie.main_pot != 0:
            with resultat:
                resultat.clear()
                ui.label("Une partie est déjà en cours. Rejoins-la plutôt que d'en créer une nouvelle.")
            return
        if not champs:
            with resultat:
                resultat.clear()
                ui.label("Valide d'abord le nombre de joueurs.")
            return
        L_joueurs = []
        for input_nom, input_solde in champs:
            nom = input_nom.value or "Joueur"
            solde = int(input_solde.value)
            L_joueurs.append(joueurs.Joueurs(nom, solde))
        partie_x = partie.partie(L_joueurs)
        resultat.clear()
        ui.navigate.to('/jeu')
        
        

    ui.button("Démarrer la partie", on_click=demarrer_partie)
@ui.page('/jeu')

async def jeu():
    if not partie_x:
         ui.navigate.to('/')
         return
    affichage=ui.column()
    with affichage:
        ui.label("Partie créée !")
        partie_x.table_partie.jape = ui.card()
        afficher.afficher_cartes_table(partie_x,0)
        for j in partie_x.L_joueurs:
            ui.button(j.nom, on_click=lambda j=j:ui.navigate.to(f'/jeu/{j.nom}', new_tab=True))
                     
    await ui.context.client.connected()
    for j in partie_x.L_joueurs:
        if not j.couche:
            await j.pret.wait() 
    await partie_x.vote()

    partie_x.table_partie.etape +=1
    afficher.afficher_cartes_table(partie_x,0)
    afficher.afficher_cartes_joueur(partie_x)
    await partie_x.vote()

    partie_x.table_partie.etape +=1
    afficher.afficher_cartes_table(partie_x,0)
    afficher.afficher_cartes_joueur(partie_x)
    await partie_x.vote()

    partie_x.table_partie.etape +=1
    afficher.afficher_cartes_table(partie_x,0)
    afficher.afficher_cartes_joueur(partie_x)
    await partie_x.vote()

    gain=0
    gagnant=None
    
    while partie_x.table_partie.main_pot !=0:
        if len(partie_x.def_gagnant()) == 1:
            gagnant=partie_x.def_gagnant()[0]
            gain=partie_x.atribution_pots(gagnant)
            gagnant.compte =True
            partie_x.table_partie.main_pot -= gain
            partie_x.L_gagnants=[gagnant]
        else:
            partie_x.L_gagnants=partie_x.def_gagnant()
            gain=partie_x.atribution_pots_execos_1()
            partie_x.table_partie.main_pot-= gain
    afficher.afficher_cartes_table(partie_x,1)
    for j in partie_x.L_joueurs:
        if j.zone_jeu:
            j.zone_jeu.refresh(6)

@ui.page('/jeu/{j}')
async def jeu_j(j: str):
    if partie_x is None:
        ui.label("Aucune partie en cours.")
        ui.navigate.to('/')
        return
    moi = next((x for x in partie_x.L_joueurs if x.nom == j), None)
    if moi is None:
            ui.label(f"Joueur '{j}' inconnu.")
            ui.navigate.to('/jeu')
            return
    
    @ui.refreshable
    def zone_entete():
        moi.jape=ui.card()
        with moi.jape:
            ui.label(f"{moi.nom} : solde {moi.solde}" )
            ui.label(f"mise : {moi.mise}")
            if moi.allin is True:
                ui.label("Vous êtes en tapis")
            if moi.couche is True:
                ui.label("Vous êtes couché")
            row= ui.row()
            with row:
                for i in range (len(moi.cartes)):
                    ui.image(Path('cartes_j')/str(moi.cartes[i].couleur)/f"{moi.cartes[i].valeur}.png").style('width: 120px')
            ui.label (hand.hand.liste_main_s[int(moi.combo)])
            ui.label(f"le main pot est : {partie_x.table_partie.main_pot}")
            ui.label(f"les autres personnes ont misé : {partie_x.table_partie.mise}")
            ui.label(table.Table.type_etape[partie_x.table_partie.etape])
            with ui.row():
                for i in range (partie_x.table_partie.etape):
                    for j in range (len(partie_x.table_partie.liste[i])):
                        ui.image(Path('cartes_j')/str(partie_x.table_partie.liste[i][j].couleur)/f"{partie_x.table_partie.liste[i][j].valeur}.png").style('width: 120px')



    @ui.refreshable
    def zone_jeu (etape=5):

        if etape == 0:
            ui.label(f"{moi.nom}, que voulez vous faire")
            t_vote=ui.toggle(joueurs.Joueurs.Vote)
            def valider ():
                moi.reponse_vote = t_vote.value
                moi.a_vote.set()
            ui.button('valider', on_click=valider )
        
        if etape ==1:
            x =ui.number("Quelle mise voulez vous rajouter? :",value =10,step=10)
            def valider ():
                moi.mise_v = x.value
                moi.a_vote.set()
            ui.button('valider', on_click=valider)
            
        
        if etape ==2:
            ui.label(f"vous n'avez pas le solde nécessaire, vous pouvez miser au maximum {moi.solde}")

        if etape ==3:
            ui.label("pas un vote autorisé")

        if etape ==4:
            ui.label("vous ne pouvez pas miser plus vous etes désormais en tapis")

        if etape == 5:
            ui.label(" En attente des autres joueurs...")
            ui.spinner()
        if etape == 6:
            if len(partie_x.L_gagnants)== 1 :
                if moi.nom == partie_x.L_gagnants[0].nom:
                   ui.label(f"Vous etes le grand gagnant, felicitations") 
                else:
                    ui.label(f"le grand gagnant est {partie_x.L_gagnants[0].nom}")
                with ui.row():
                    for i in range (len(partie_x.L_gagnants[0].cartes_jouee)):
                        ui.image(Path('cartes_j')/str(partie_x.L_gagnants[0].cartes_jouee[i].couleur)/f"{partie_x.L_gagnants[0].cartes_jouee[i].valeur}.png").style('width: 120px')
                ui.label (hand.hand.liste_main_s[int(partie_x.L_gagnants[0].combo)])
            else:
                ui.label("Les gagnants sont : " )
                for j in partie_x.L_gagnants:
                    with ui.row():
                        ui.label(j.nom)
                for j in partie_x.L_gagnants:
                    ui.label(f"{j.nom} avait :")
                    with ui.row():
                        for i in range (len(j.cartes_jouee)):
                            ui.image(Path('cartes_j')/str(j.cartes_jouee[i].couleur)/f"{j.cartes_jouee[i].valeur}.png").style('width: 120px')
                    ui.label (hand.hand.liste_main_s[int(j.combo)])
            ui.button('Rejouer', on_click =lambda :ui.navigate.to('/'))



    moi.zone_entete=zone_entete
    moi.zone_jeu=zone_jeu

    zone_entete()
    zone_jeu()
            
    await ui.context.client.connected()
    moi.pret.set()

ui.run()
