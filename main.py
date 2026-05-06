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
for i in range (nb_joueurs-1):
    L_joueurs[i].cartes_jouables = hand.hand(L_joueurs[i].cartes, partie_x.table_partie)
    L_joueurs[i].combo, L_joueurs[i].cartes_jouee = L_joueurs[i].cartes_jouables.analyse_main()
    afficher.afficher_combo(L_joueurs[i])
partie_x.vote()
for joueur in L_joueurs:
    afficher.afficher_solde(joueur)
partie_x.table_partie.etape +=1
afficher.afficher_cartes_table(partie_x)
for i in range (nb_joueurs-1):
    L_joueurs[i].cartes_jouables = hand.hand(L_joueurs[i].cartes, partie_x.table_partie)
    L_joueurs[i].combo, L_joueurs[i].cartes_jouee = L_joueurs[i].cartes_jouables.analyse_main()
    afficher.afficher_combo(L_joueurs[i])
partie_x.vote()
for joueur in L_joueurs:
    afficher.afficher_solde(joueur)
partie_x.table_partie.etape +=1
afficher.afficher_cartes_table(partie_x)
for i in range (nb_joueurs-1):
    L_joueurs[i].cartes_jouables = hand.hand(L_joueurs[i].cartes, partie_x.table_partie)
    L_joueurs[i].combo, L_joueurs[i].cartes_jouee = L_joueurs[i].cartes_jouables.analyse_main()
    afficher.afficher_combo(L_joueurs[i])
gagnant=partie_x.def_gagnant()
afficher.grand_gagnant(gagnant)