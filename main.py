import hand
import partie
import joueurs
import afficher

nb_joueurs = afficher.nb_de_j ()
L_joueurs = []
for i in range (nb_joueurs):
    nom_joueur_x , solde_joueur_x = afficher.nom_solde(i)
    joueur_x= joueurs.Joueurs(nom_joueur_x,solde_joueur_x)
    L_joueurs.append(joueur_x)
partie_x = partie.partie(L_joueurs)
for joueur in L_joueurs:
    afficher.afficher_cartes_joueur(joueur)
partie_x.vote()
afficher.afficher_pots(partie_x.table_partie)
for joueur in L_joueurs:
    afficher.afficher_solde(joueur)
partie_x.table_partie.etape +=1
afficher.afficher_cartes_table(partie_x)
for joueur in L_joueurs:
    joueur.cartes_jouables = hand.hand(joueur.cartes, partie_x.table_partie)
    joueur.combo, joueur.cartes_jouee = joueur.cartes_jouables.analyse_main()
    afficher.afficher_combo(joueur)
partie_x.vote()
afficher.afficher_pots(partie_x.table_partie)
for joueur in L_joueurs:
    afficher.afficher_solde(joueur)
partie_x.table_partie.etape +=1
afficher.afficher_cartes_table(partie_x)
for joueur in L_joueurs:
    joueur.cartes_jouables = hand.hand(joueur.cartes, partie_x.table_partie)
    joueur.combo, joueur.cartes_jouee = joueur.cartes_jouables.analyse_main()
    afficher.afficher_combo(joueur)
partie_x.vote()
afficher.afficher_pots(partie_x.table_partie)
for joueur in L_joueurs:
    afficher.afficher_solde(joueur)
partie_x.table_partie.etape +=1
afficher.afficher_cartes_table(partie_x)
for joueur in L_joueurs:
    joueur.cartes_jouables = hand.hand(joueur.cartes, partie_x.table_partie)
    joueur.combo, joueur.cartes_jouee = joueur.cartes_jouables.analyse_main()
    afficher.afficher_combo(joueur)
partie_x.vote()
afficher.afficher_pots(partie_x.table_partie)
for joueur in L_joueurs:
    afficher.afficher_solde(joueur)

gain=0
while partie_x.table_partie.main_pot !=0:
    if len(partie_x.def_gagnant()) == 1:
        gagnant=partie_x.def_gagnant()[0]
        gain=partie_x.atribution_pots(gagnant)
        afficher.grand_gagnant(gagnant)
        gagnant.couche =True
        partie_x.table_partie.main_pot -= gain
    else:
            gain=partie_x.atribution_pots_execos_1()
            partie_x.table_partie.main_pot-= gain

    


