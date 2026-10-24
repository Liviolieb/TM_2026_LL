import partie
import joueurs
import afficher
import hand
from nicegui import ui, background_tasks
import asyncio
import table_svg



partie_x =None
@ui.page('/')
def accueil():
    ui.query('body').classes('bg-green-900')  # fond vert foncé (Tailwind bg-green-900)
    ui.label("Configuration de la partie").style('font-size: 1.5em; color: white;')
    nb_joueurs_input =ui.number('Combien de joueurs :', value=3, min=2, max=10,precision=0).props('dark').classes('w-64') # pas de demi joueur et seulement de 2 à 10 joueurs

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
                        input_solde = ui.number(f"Solde du joueur {i + 1}", value=1000,step=10,min=1,precision=0).props('dark')# on veut pas de joueur avec des bouts de jeton, ni avec 0 ou moins de solde
                    champs.append((input_nom, input_solde))

    bouton_j=ui.button("Valider le nombre de joueurs", on_click=generer_champs, color='amber')

    resultat = ui.column()

    async def demarrer_partie(): # fonction asynchrone car on doit attendre le asyncio sleep(1)
        global partie_x # pour pouvoir l'utiliser partout
        if partie_x is not None and partie_x.table_partie.pot_princ != 0: # pour éviter de commencer une deuxième partie en parallele qui viendrait supprimer l'actuelle(si on rejoue, on veut recréer une partie par dessus l'ancienne, on utilise le pot vide pour différencier ce cas)
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
        
        if not champs: #on a pas saisi un nombre de joueur
            with resultat:
                resultat.clear()
                ui.label("Valide d'abord le nombre de joueurs.").style('color: red')
            return
        L_joueurs = []
        for i in range(len(champs)):
            input_nom, input_solde = champs[i]
            nom = input_nom.value or (f"Joueur{i+1}") # si il n'y a pas de nom spécifié on les appelle "joueur"et on ajoute un nombre
            solde = int(input_solde.value)
            L_joueurs.append(joueurs.Joueurs(nom, solde))
        partie_x = partie.partie(L_joueurs) # créée tout de suite (tire les cartes), annulée plus bas si validation échoue
        noms_invalides = [j.nom for j in L_joueurs if '/' in j.nom] #un / casserait l’adresse /jeu/{nom}
        if noms_invalides:
            with resultat:
                partie_x=None
                resultat.clear()
                ui.label("Votre nom ne doit pas contenir de /").style('color: red')
            return

        if len(L_joueurs) != len(set(s.nom.lower() for s in L_joueurs)): # on met tout les nom en minuscule et on fait un set (plus de doublons) si on a une longueur (du set et de la liste de base) différente alors on demande de resaisir pour ne pas avoir deux joueur avec le même nom
            with resultat:
                partie_x=None
                resultat.clear()
                ui.label("Vous devez avoir des noms différents").style('color: red')
                

            return

        resultat.clear()
        ui.navigate.to('/jeu')
        
        

    ui.button("Démarrer la partie", on_click=demarrer_partie, color='amber')
@ui.page('/jeu')

async def jeu(): #même raison que en haut chaque etape en son temps
    ui.query('body').classes('bg-green-900') # fond vert foncé (Tailwind bg-green-900)
    if not partie_x:
         ui.navigate.to('/')
         return

    @ui.refreshable
    def vue_table():
        svg=table_svg.table_jolie(partie_x)
        with ui.column().classes('w-full items-center'): #L'élément prend toute la largeur disponible de son parent,et centrage au milieu de la colonne
            ui.html(svg,sanitize=False).style('width: min(100%, calc((100vh - 2rem) * 350 / 240))') # sanitize=False : on injecte du SVG brut, on fait confiance à notre génération, Largeur = min(largeur écran, largeur qui fait tenir le SVG en hauteur via le ratio 350/240 du viewBox): la table tient toujours entière, centrée, quelle que soit la forme de la fenêtre.
    partie_x.vues_tables.append(vue_table)

    def retirer_vue(): # si un client se déconnecte j'enleve la vue de ma liste pour pas en avoir une infinité
        if vue_table in partie_x.vues_tables:
            partie_x.vues_tables.remove(vue_table)
    ui.context.client.on_disconnect(retirer_vue)

    vue_table()


    async def lancer_main():
        for j in partie_x.L_joueurs:
            if not j.couche:
                try:
                    await asyncio.wait_for(j.pret.wait(), timeout=afficher.TIMEOUT_VOTE) #on laisse 60 seconde par joueur pour que tout les joueurs se connectent à leur page sinon on les couche
                except asyncio.TimeoutError:
                    j.couche = True

        index_1 = (partie_x.index + 1) % len(partie_x.L_joueurs) #index est celui de la grosse blinde on commence au joueur d'après(modulo pour retourner à 0 après le dernier)
        
        await partie_x.vote(index_1) #on attend tout les vote avant de continuer
        for i in range (3): #Flop, Turn, River
            L_non_couche =[j for j in partie_x.L_joueurs if not j.couche]
            if len(L_non_couche) >1: # on révèle pas les autres cartes si il n'y a plus qu'un seul joueur non-couché
                partie_x.table_partie.etape +=1 #on incrémente l'étape, on affiche les 3 nouvelles cartes, on analyse les mains, puis nouveau tour de vote.
                afficher.afficher_cartes_table(partie_x,0)
                afficher.afficher_cartes_joueurs(partie_x)
                await partie_x.vote((partie_x.dealer + 1) % len(partie_x.L_joueurs))

        L_non_couche =[j for j in partie_x.L_joueurs if not j.couche]
        if len(L_non_couche) >1: # s'il ne reste plus qu'un seul joueur non couché, il ne montre pas ses cartes aux autres joueurs
            partie_x.revel_c=True
        partie_x.L_gagnants=partie_x.def_gagnant()
        partie_x.atribution_pots()
        partie_x.table_partie.pot_princ= 0 # fin de partie (marqueur pour l'accueil) 
        partie_x.table_partie.mise = 0
        afficher.afficher_cartes_table(partie_x,1)
        for j in partie_x.L_joueurs:
            if j.zone_jeu:
                afficher.rafraichir(j.zone_jeu,6)

        
                     
    await ui.context.client.connected() #sans ça, les rafraîchissements partiraient vers une page pas encore connectée
    if not partie_x.lancee:
        partie_x.lancee = True
        background_tasks.create(lancer_main())



@ui.page('/jeu/{j}')    #vue personnelle des joueurs
async def jeu_j(j: str):
    if partie_x is None:
        ui.label("Aucune partie en cours.").style('color: white')
        ui.navigate.to('/')
        return
    moi = next((x for x in partie_x.L_joueurs if x.nom == j), None) # le premier qui correspond à j dans la liste de joueur
    if moi is None: #si le nom n'est pas dans la liste on renvoit à la page jeu
            ui.label(f"Joueur '{j}' inconnu.").style('color: white')
            ui.navigate.to('/jeu')
            return
    
    @ui.refreshable
    def zone_table():
        svg=table_svg.table_jolie(partie_x,moi)
        ui.html(svg,sanitize=False).style('width: min(100%, calc((100vh - 2rem) * 350 / 240))') # même logique que /jeu

            
    @ui.refreshable
    def zone_infos():
        ui.label(f"{moi.nom}")
        ui.label(f"A suivre : {partie_x.table_partie.mise - moi.mise}")
        ui.label(f"Pot principal de : {partie_x.table_partie.pot_princ}")
        ui.label(f"Vous pouvez jouer : {hand.hand.noms_mains[moi.combo]}")
        if moi.couche:
            ui.badge("Couché", color="red")
        if moi.allin:
            ui.badge("Tapis", color="orange") 
        



    @ui.refreshable
    def zone_jeu (etape=5):
        if etape == 0:
            Vote_t = {}
            for v in joueurs.Joueurs.Vote:
                if moi.mise < partie_x.table_partie.mise : #si ce qu'il nous reste à payer (difference entre notre mise et celle des autre) n'est pas nul on affiche tout les boutons
                    Vote_t[v] = joueurs.Joueurs.Vote_libelles[v]
                else: 
                    if v != joueurs.Joueurs.Vote[2]: #sinon on n'affiche pas coucher car, on ne va pas se coucher si on peut suivre
                        Vote_t[v] = joueurs.Joueurs.Vote_libelles[v]
            def changer_couleur(): # pour attribuer une couleur au toggle enfoncé
                t_vote.props(f'toggle-color={joueurs.Joueurs.couleurs_vote[t_vote.value]}')
                t_vote.update()
            t_vote=ui.toggle(Vote_t,on_change=changer_couleur)
            def valider (): #un deuxième bouton car si on appuie et qu'on veut encore changer on peut
                moi.reponse_vote = t_vote.value
                moi.a_vote.set()
            ui.button('valider', on_click=valider, color = 'amber')
            ui.label().bind_text_from(moi, 'temps', lambda t: f"il vous reste {t}s pour voter") # bind_text_from : le label se met à jour tout seul quand moi.temps change (on évite de changer le label car il peut disparaitre mais pas la variable python)
        
        if etape ==1:
            x =ui.number("Quelle mise voulez vous rajouter? :",value =10,step=10,min=0,precision=0)
            def valider ():
                moi.mise_v = int(x.value) # rend un float
                moi.a_vote.set()
            ui.button('valider', on_click=valider, color='amber')
            ui.label().bind_text_from(moi, 'temps', lambda t: f"il vous reste {t}s pour miser") # même chose que en haut
            
        
        if etape ==2:
            ui.label(f"vous n'avez pas le solde nécessaire, vous pouvez miser au maximum {moi.solde}").style('color: red')

        if etape ==7:
            ui.label(f"vous ne pouvez pas miser un montant négatif").style('color: red')

        if etape ==3:
            ui.label("pas un vote autorisé").style('color: red')

        if etape ==4:
            ui.label("vous ne pouvez pas miser plus vous etes désormais en tapis").style('color: red')

        if etape == 5: #quand on attend les autres joueurs
            pass
        if etape == 6:
            ui.button('Rejouer', on_click =lambda :ui.navigate.to('/'),color ='amber')


    ui.query('body').classes('bg-green-900') # fond vert foncé (Tailwind bg-green-900)
    with ui.element('div').classes('relative w-full'): # devient cadre repère pour ses enfants (il prend aussi toute la largeur de son parent (page)), sans lui, top-2 left-2 mesurés par rapport à la fenêtre
        with ui.column().classes('w-full items-center'): #toute la largeur de son parent, elle centre horizontalement ses enfants
            zone_table() 
        with ui.card().classes('absolute top-2 left-2 z-10').style('background: rgba(255,255,255,0.50)'): #petite carte en haut à gauche (absolute par rapport au relatif), semi-transparente, z-10 pour passer devant la table
            zone_infos()
            zone_jeu()


    moi.zone_table=zone_table
    moi.zone_infos=zone_infos
    moi.zone_jeu=zone_jeu


            
    await ui.context.client.connected()
    moi.pret.set()
if __name__ in {"__main__", "__mp_main__"}: #on veut executer run seulement depuis ce fichier (__main__) et quand nicegui reload (__mp_main__)
    ui.run()

