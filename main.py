import hand
import partie
import joueurs
import afficher

nb_joueurs = afficher.nb_de_j
L_joueurs = []
for i in range (nb_joueurs):
    nom_joueur_x , solde_joueur_x = afficher.nom_solde(i)
    joueur_x= joueurs.Joueurs(nom_joueur_x,solde_joueur_x)
    L_joueurs.append(joueur_x)
partie_x = partie.partie(L_joueurs)
for joueur in L_joueurs:
    joueur.afficher_cartes()
partie_x.vote()
partie_x.table_partie.etape +=1
afficher.afficher_cartes_table(partie_x)
for i in range (nb_joueurs):
    print(L_joueurs[i].cartes)
    L_joueurs[i].cartes_jouables = hand.hand(L_joueurs[i].cartes, partie_x.table_partie)
    L_joueurs[i].combo = L_joueurs[i].cartes_jouables.analyse_main()
    print (hand.hand.liste_main_s[int(L_joueurs[i].combo)])
partie_x.vote()
partie_x.table_partie.etape +=1
afficher.afficher_cartes_table(partie_x)
for i in range (nb_joueurs):
    L_joueurs[i].cartes_jouables = hand.hand(L_joueurs[i].cartes, partie_x.table_partie)
    L_joueurs[i].combo = L_joueurs[i].cartes_jouables.analyse_main()
    print (hand.hand.liste_main_s[int(L_joueurs[i].combo)])
partie_x.vote()
partie_x.table_partie.etape +=1
afficher.afficher_cartes_table(partie_x)
for i in range (nb_joueurs):
    L_joueurs[i].cartes_jouables = hand.hand(L_joueurs[i].cartes, partie_x.table_partie)
    L_joueurs[i].combo = L_joueurs[i].cartes_jouables.analyse_main()
    print (hand.hand.liste_main_s[int(L_joueurs[i].combo)])
gagnant=partie_x.def_gagnant()
afficher.grand_gagnant(gagnant)