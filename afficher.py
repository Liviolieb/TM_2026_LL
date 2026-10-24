import joueurs
import hand
import asyncio



TIMEOUT_VOTE = 60  # le temps qu'on laisse à l'utilisateur pour voter et pour miser


def rafraichir(refreshable, *args): # au lieu de tout le temps refresh, car si la page n'existe plus, erreur de refresh
    if refreshable is None:
        return
    try:
        refreshable.refresh(*args)
    except Exception: # on ignore, une nouvelle vue sera créée
        pass
#0: voter(toggle), 1 mise, 2 pas le solde, 3 pas un vote autorisé, 4 plus miser car tapis, 5 on affiche rien, 6 rejouer, 7 pas de montant negatif
async def afficher_vote (etape,joueur,a_payer=0): # a_payer est la différence entre la mise actuelle du joueur et la mise courante de la table
    if etape == 0:
        joueur.a_vote = asyncio.Event() # on veut pouvoir attendre cette variable (est-ce que le joueur a voté et on peut continuer) (c'est chaque fois un nouvel event)
        joueur.temps = TIMEOUT_VOTE # attribution au joueur pour pouvoir l'afficher
        rafraichir(joueur.zone_jeu,0)
        while joueur.temps>0: # on fait une boucle sur le temps restant au joueur et on diminue de 1 à chaque fois
            if joueur.a_vote.is_set(): # si le joueur a valider et donc set son a_vote on a pas besoin d'attendre plus longtemps(is_set() rend booleen)
                break
            await asyncio.sleep(1)
            joueur.temps-=1
        if not joueur.a_vote.is_set(): # si on est sorti de la while et que joueur n'as pas set cela signifie qu'on a attendu au delà de TIMEOUT_VOTE
            if a_payer <=0: # si il est encore possible de continuer la partie sans augmenter, on fait suivre le joueur automatiquement
                joueur.reponse_vote = joueurs.Joueurs.Vote[1]
            else: # sinon on le couche
                joueur.reponse_vote = joueurs.Joueurs.Vote[2]
        return joueur.reponse_vote
    
    if etape ==1:
        rafraichir(joueur.zone_table)
        rafraichir(joueur.zone_infos) # le joueur a suivi automatiquement on rafraichit donc les zones table et infos
        joueur.a_vote = asyncio.Event() # on veut pouvoir attendre cette variable (est-ce que le joueur a misé et on peut continuer)
        joueur.temps=TIMEOUT_VOTE # attribution au joueur pour pouvoir l'afficher
        rafraichir(joueur.zone_jeu,1)
        while joueur.temps>0: # on fait une boucle sur le temps restant au joueur et on diminue de 1 à chaque fois
            if joueur.a_vote.is_set():# si le joueur a valider et donc set son a_vote on a pas besoin d'attendre plus longtemps
                break
            await asyncio.sleep(1)
            joueur.temps-=1
        if not joueur.a_vote.is_set(): # si on est sorti de la while et que joueur n'as pas set cela signifie qu'on a attendu au delà de TIMEOUT_VOTE
            joueur.mise_v = 0 # on met tout simplement sa mise à 0 pour ne pas interférer avec le reste du jeu
        return joueur.mise_v
    
    if etape >=2:
        rafraichir(joueur.zone_jeu,etape)
        await asyncio.sleep(2) # on veut que le message reste un petit moment( pour etape==6 ça n'as pas d'influence)

def afficher_cartes_joueurs(partie):
        for joueur in partie.L_joueurs:
                joueur.hand = hand.hand(joueur.cartes, partie.table_partie) # définition de l'objet hand qu'on va pouvoir analyser
                joueur.combo, joueur.cartes_combo, joueur.cartes_kicker = joueur.hand.analyse_main() # l'analyse nous rend le combo(sous forme int), les cartes qui composent ce combo et les cartes qui complète le combo pour former une main
                joueur.cartes_jouee = joueur.cartes_combo+joueur.cartes_kicker # cartes que le joueur va jouer (meilleur combo possible) on ne l'affichera que à la fin pour le ou les joueurs gagnants
        for j in partie.L_joueurs:
            rafraichir(j.zone_table)
            rafraichir(j.zone_infos)
                

def afficher_cartes_table(partie,etape):
    for vue in partie.vues_tables[:]: # on veut gerer la vue de chaque page qui s'ouvre sur la table ([:]car on va peut-être remove une vue)
        try:
            vue.refresh()
        except Exception:
            partie.vues_tables.remove(vue) # si on arrive pas a refresh la page à été fermée on a plus besoin de s'en occuper, si elle est réouverte une nouvelle vue sera créée
    for j in partie.L_joueurs: #les zones table et infos des joueurs doit être synchronisé avec table (des éléments en commmun)
        rafraichir(j.zone_table)
        rafraichir(j.zone_infos)





#code mort il allait avec mes premier test la manière textuelle
# def nb_de_j ():
#     x= int(input("Combien de joueurs :"))
#     return(int(x))

# def nom_solde (i):
#     nom_joueur_x= input(f"nom du joueur {i+1}:")
#     solde_joueur_x= int(input("Quel est sa solde de départ :"))
#     return (nom_joueur_x,solde_joueur_x)

# def grand_gagnant (gagnant):
#     ui.label(f"le grand gagnant est {gagnant.nom}")
#     with ui.row():
#         for i in range (len(gagnant.cartes_jouee)):
#             ui.image(CARTES_DIR/str(gagnant.cartes_jouee[i].couleur)/f"{gagnant.cartes_jouee[i].valeur}.png").style('width: 120px')
#     ui.label (hand.hand.liste_main_s[int(gagnant.combo)])

# def afficher_solde (joueur):
#      print (joueur.nom,"a :")
#      print (joueur.solde,"de solde")

# def afficher_combo (joueur):
#      print (f"{joueur} a :")
#      for i in range (len(joueur.cartes_jouee)):
#         print (joueur.cartes_jouee[i])
#      print (hand.hand.liste_main_s[int(joueur.combo)])
