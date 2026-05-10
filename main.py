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
for joueur in L_joueurs:
    afficher.afficher_solde(joueur)
partie_x.table_partie.etape +=1
afficher.afficher_cartes_table(partie_x)
for joueur in L_joueurs:
    joueur.cartes_jouables = hand.hand(joueur.cartes, partie_x.table_partie)
    joueur.combo, joueur.cartes_jouee = joueur.cartes_jouables.analyse_main()
    afficher.afficher_combo(joueur)
partie_x.vote()
for joueur in L_joueurs:
    afficher.afficher_solde(joueur)
partie_x.table_partie.etape +=1
afficher.afficher_cartes_table(partie_x)
for joueur in L_joueurs:
    joueur.cartes_jouables = hand.hand(joueur.cartes, partie_x.table_partie)
    joueur.combo, joueur.cartes_jouee = joueur.cartes_jouables.analyse_main()
    afficher.afficher_combo(joueur)
partie_x.vote()
for joueur in L_joueurs:
    afficher.afficher_solde(joueur)
partie_x.table_partie.etape +=1
afficher.afficher_cartes_table(partie_x)
for joueur in L_joueurs:
    joueur.cartes_jouables = hand.hand(joueur.cartes, partie_x.table_partie)
    joueur.combo, joueur.cartes_jouee = joueur.cartes_jouables.analyse_main()
    afficher.afficher_combo(joueur)
gagnant=partie_x.def_gagnant()
afficher.grand_gagnant(gagnant)