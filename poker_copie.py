import partie
import joueurs
import afficher
import hand
import table
from nicegui import ui, background_tasks
import asyncio
from urllib.parse import quote

partie_x =None
@ui.page('/')
def accueil():
    ui.query('body').classes('bg-green-900')
    ui.label("Configuration de la partie").style('font-size: 1.5em; color: white;')
    nb_joueurs_input =ui.number('Combien de joueurs :', value=3, min=2, max=10,precision=0).props('dark').classes('w-64')

    champ_joueurs = ui.column()
    champs = [] 

    def generer_champs():
        if nb_joueurs_input.value:
            bouton_j.delete()
            champ_joueurs.clear()
            champs.clear()
            nb = int(nb_joueurs_input.value)
            nb_joueurs_input.delete()
            with champ_joueurs:
                for i in range(nb):
                    with ui.row():
                        input_nom = ui.input(f"Nom du joueur {i + 1}").props('dark')
                        input_solde = ui.number(f"Solde du joueur {i + 1}", value=1000,step=10,min=1,precision=0).props('dark')
                    champs.append((input_nom, input_solde))

    bouton_j=ui.button("Valider le nombre de joueurs", on_click=generer_champs, color='amber')

    resultat = ui.column()

    async def demarrer_partie():
        global partie_x
        if partie_x is not None and partie_x.table_partie.pot_princ != 0:
            with resultat:
                resultat.clear()
                ui.label("Une partie est déjà en cours. Rejoins-la plutôt que d'en créer une nouvelle.").style('color: white')
                ui.spinner().props('dark')
                for i in range (3):
                    x=ui.label(f"connexion dans {3-i}").style('color: white')
                    await asyncio.sleep(1)
                    x.delete()
                ui.navigate.to('/jeu')
                
            return
        if not champs:
            with resultat:
                resultat.clear()
                ui.label("Valide d'abord le nombre de joueurs.").style('color: red')
            return
        L_joueurs = []
        for i in range(len(champs)):
            input_nom, input_solde = champs[i]
            nom = input_nom.value or (f"Joueur {i+1}")
            solde = int(input_solde.value)
            L_joueurs.append(joueurs.Joueurs(nom, solde))
        partie_x = partie.partie(L_joueurs)
        noms_invalides = [j.nom for j in L_joueurs if '/' in j.nom]
        if noms_invalides:
            with resultat:
                partie_x=None
                resultat.clear()
                ui.label("Votre nom ne doit pas contenir de /").style('color: red')
            return

        if len(L_joueurs) != len(set(s.nom.lower() for s in L_joueurs)):
            with resultat:
                partie_x=None
                resultat.clear()
                ui.label("Vous devez avoir des noms différents").style('color: red')
                

            return

        resultat.clear()
        ui.navigate.to('/jeu')
        
        

    ui.button("Démarrer la partie", on_click=demarrer_partie, color='amber')
@ui.page('/jeu')

async def jeu():
    ui.query('body').classes('bg-green-900')
    if not partie_x:
         ui.navigate.to('/')
         return
    affichage=ui.column()
    @ui.refreshable

    def vue_table(etape=0):
        with ui.card():
            if etape==0:
                ui.label(f"le main pot est : {partie_x.table_partie.pot_princ}")
                ui.label(f"les gens ont misé: {partie_x.table_partie.mise}")
                ui.label(table.Table.etape_libelles[table.Table.type_etape[partie_x.table_partie.etape]])
                with ui.row():
                    for i in range (partie_x.table_partie.etape):
                        for j in range (len(partie_x.table_partie.liste[i])):
                                ui.image(afficher.CARTES_DIR/str(partie_x.table_partie.liste[i][j].couleur)/f"{partie_x.table_partie.liste[i][j].valeur}.png").style('width: 120px')
            elif etape==1:
                if len(partie_x.L_gagnants)== 1 :
                    ui.label(f"le grand gagnant est {partie_x.L_gagnants[0].nom}")
                    with ui.row():
                        for i in range (len(partie_x.L_gagnants[0].cartes_jouee)):
                            ui.image(afficher.CARTES_DIR/str(partie_x.L_gagnants[0].cartes_jouee[i].couleur)/f"{partie_x.L_gagnants[0].cartes_jouee[i].valeur}.png").style('width: 120px')
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
                                ui.image(afficher.CARTES_DIR/str(j.cartes_jouee[i].couleur)/f"{j.cartes_jouee[i].valeur}.png").style('width: 120px')
                        ui.label (hand.hand.liste_main_s[int(j.combo)])
    partie_x.vues_tables.append(vue_table)

    def retirer_vue():
        if vue_table in partie_x.vues_tables:
            partie_x.vues_tables.remove(vue_table)
    ui.context.client.on_disconnect(retirer_vue)

    with affichage:
        ui.label("Partie créée !").style('color: white')
        vue_table()
        for j in partie_x.L_joueurs:
            ui.button(j.nom, on_click=lambda j=j:ui.navigate.to(f'/jeu/{quote(j.nom, safe="")}', new_tab=True), color='amber')

    async def lancer_main():
        for j in partie_x.L_joueurs:
            if not j.couche:
                try:
                    await asyncio.wait_for(j.pret.wait(), timeout=afficher.TIMEOUT_VOTE)
                except asyncio.TimeoutError:
                    j.couche = True
        index_1 = (partie_x.index + 1) % len(partie_x.L_joueurs)
        
        await partie_x.vote(index_1)

        partie_x.table_partie.etape +=1
        afficher.afficher_cartes_table(partie_x,0)
        afficher.afficher_cartes_joueurs(partie_x)
        await partie_x.vote()

        partie_x.table_partie.etape +=1
        afficher.afficher_cartes_table(partie_x,0)
        afficher.afficher_cartes_joueurs(partie_x)
        await partie_x.vote()

        partie_x.table_partie.etape +=1
        afficher.afficher_cartes_table(partie_x,0)
        afficher.afficher_cartes_joueurs(partie_x)
        await partie_x.vote()

        gain=0
        partie_x.L_gagnants=partie_x.def_gagnant()
        partie_x.atribution_pots()
        partie_x.table_partie.pot_princ= 0
        afficher.afficher_cartes_table(partie_x,1)
        for j in partie_x.L_joueurs:
            if j.zone_jeu:
                afficher.rafraichir(j.zone_jeu,6)

        
                     
    await ui.context.client.connected()
    if not partie_x.lancee:
        partie_x.lancee = True
        background_tasks.create(lancer_main())



@ui.page('/jeu/{j}')
async def jeu_j(j: str):
    if partie_x is None:
        ui.label("Aucune partie en cours.").style('color: white')
        ui.navigate.to('/')
        return
    moi = next((x for x in partie_x.L_joueurs if x.nom == j), None)
    if moi is None:
            ui.label(f"Joueur '{j}' inconnu.").style('color: white')
            ui.navigate.to('/jeu')
            return
    
    @ui.refreshable
    def zone_entete():
        ui.query('body').classes('bg-green-900')
        moi.jape=ui.card()
        with moi.jape:
            ui.label(f"{moi.nom} : solde {moi.solde}" )
            ui.label(f"mise : {moi.mise}")
        if moi.couche:
            ui.badge("Couché", color="red")
        if moi.allin:
            ui.badge("Tapis", color="orange")
        row= ui.row()
        
        with row:
            for i in range (len(moi.cartes)):
                ui.image(afficher.CARTES_DIR/str(moi.cartes[i].couleur)/f"{moi.cartes[i].valeur}.png").style('width: 120px')
        ui.label (hand.hand.liste_main_s[int(moi.combo)]).style('color: white')
        ui.label(f"le main pot est : {partie_x.table_partie.pot_princ}").style('color: white')
        ui.label(f"les autres personnes ont misé : {partie_x.table_partie.mise}").style('color: white')
        ui.label(table.Table.etape_libelles[table.Table.type_etape[partie_x.table_partie.etape]]).style('color: white')
        with ui.row():
            for i in range (partie_x.table_partie.etape):
                for k in range (len(partie_x.table_partie.liste[i])):
                    ui.image(afficher.CARTES_DIR/str(partie_x.table_partie.liste[i][k].couleur)/f"{partie_x.table_partie.liste[i][k].valeur}.png").style('width: 120px')



    @ui.refreshable
    def zone_jeu (etape=5):

        if etape == 0:
            ui.label(f"{moi.nom}, que voulez vous faire").style('color: white')
            Vote_t = {}
            for v in joueurs.Joueurs.Vote:
                if moi.mise < partie_x.table_partie.mise :
                    Vote_t[v] = joueurs.Joueurs.Vote_libelles[v]
                else: 
                    if v != joueurs.Joueurs.Vote[2]:
                        Vote_t[v] = joueurs.Joueurs.Vote_libelles[v]
            def changer_couleur():
                t_vote.props(f'toggle-color={joueurs.Joueurs.couleurs_vote[t_vote.value]}')
                t_vote.update()
            t_vote=ui.toggle(Vote_t,on_change=changer_couleur).style('color: white')
            def valider ():
                moi.reponse_vote = t_vote.value
                moi.a_vote.set()
            ui.button('valider', on_click=valider, color = 'amber')
            moi.label_temps=ui.label(f"il vous reste {moi.temps}s pour voter").style('color: white')
        
        if etape ==1:
            x =ui.number("Quelle mise voulez vous rajouter? :",value =10,step=10,min=0,precision=0).props('dark')
            def valider ():
                moi.mise_v = x.value
                moi.a_vote.set()
            ui.button('valider', on_click=valider, color='amber')
            moi.label_temps=ui.label(f"il vous reste {moi.temps}s pour miser").style('color: white')
            
        
        if etape ==2:
            ui.label(f"vous n'avez pas le solde nécessaire, vous pouvez miser au maximum {moi.solde}").style('color: red')

        if etape ==7:
            ui.label(f"vous ne pouvez pas miser un montant négatif").style('color: red')

        if etape ==3:
            ui.label("pas un vote autorisé").style('color: red')

        if etape ==4:
            ui.label("vous ne pouvez pas miser plus vous etes désormais en tapis").style('color: red')

        if etape == 5:
            ui.label(" En attente des autres joueurs...").style('color: white')
            ui.spinner()
        if etape == 6:
            if len(partie_x.L_gagnants)== 1 :
                if moi.nom == partie_x.L_gagnants[0].nom:
                   ui.label(f"Vous etes le grand gagnant, felicitations").style('color: white')
                else:
                    ui.label(f"le grand gagnant est {partie_x.L_gagnants[0].nom}").style('color: white')
                with ui.row():
                    for i in range (len(partie_x.L_gagnants[0].cartes_jouee)):
                        ui.image(afficher.CARTES_DIR/str(partie_x.L_gagnants[0].cartes_jouee[i].couleur)/f"{partie_x.L_gagnants[0].cartes_jouee[i].valeur}.png").style('width: 120px')
                ui.label (hand.hand.liste_main_s[int(partie_x.L_gagnants[0].combo)]).style('color: white')
            else:
                ui.label("Les gagnants sont : " ).style('color: white')
                for g in partie_x.L_gagnants:
                    with ui.row():
                        ui.label(g.nom).style('color: white')
                for g in partie_x.L_gagnants:
                    ui.label(f"{g.nom} avait :").style('color: white')
                    with ui.row():
                        for i in range (len(g.cartes_jouee)):
                            ui.image(afficher.CARTES_DIR/str(g.cartes_jouee[i].couleur)/f"{g.cartes_jouee[i].valeur}.png").style('width: 120px')
                    ui.label (hand.hand.liste_main_s[int(g.combo)]).style('color: white')
            ui.button('Rejouer', on_click =lambda :ui.navigate.to('/'))



    moi.zone_entete=zone_entete
    moi.zone_jeu=zone_jeu

    zone_entete()
    zone_jeu()
            
    await ui.context.client.connected()
    moi.pret.set()
if __name__ in {"__main__", "__mp_main__"}:
    ui.run()

