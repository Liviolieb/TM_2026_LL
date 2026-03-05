import hand
import partie
import joueurs

nb_joueurs = int(input("Combien de joueurs :"))
L_joueurs = []
for i in range (nb_joueurs):
    nom_joueur_x= input(f"nom du joueur {i+1}:")
    solde_joueur_x= int(input("Quel est sa solde de départ :"))
    joueur_x= joueurs.Joueurs(nom_joueur_x,solde_joueur_x)
    L_joueurs.append(joueur_x)
partie_x = partie.partie(L_joueurs)
for joueur in L_joueurs:
    joueur.afficher_cartes()
partie_x.vote()
partie_x.table_partie.etape +=1
partie_x.afficher_cartes_table()
for i in range (nb_joueurs):
    L_joueurs[i].cartes_jouables = hand.hand(L_joueurs[i].cartes, partie_x.table_partie)
    L_joueurs[i].cartes_jouables.analyse_main()
partie_x.vote()