from hand import *
from cartes import *
from partie import *
from joueurs import *

h = hand.__new__(hand)
jeu = partie.__new__(partie)

c1 = Cartes(couleur="coeur", valeur=1)
c2 = Cartes(couleur="coeur", valeur=2)
c3 = Cartes(couleur="coeur", valeur=3)
c4 = Cartes(couleur="coeur", valeur=4)
c5 = Cartes(couleur="coeur", valeur=5)
c6 = Cartes(couleur="coeur", valeur=6)
c7 = Cartes(couleur="coeur", valeur=7)
c8 = Cartes(couleur="coeur", valeur=8)
c9 = Cartes(couleur="coeur", valeur=9)
c10 = Cartes(couleur="coeur", valeur=10)
c11 = Cartes(couleur="coeur", valeur=11)
c12 = Cartes(couleur="coeur", valeur=12)
c13 = Cartes(couleur="coeur", valeur=13)
 
k1 = Cartes(couleur="carreau", valeur=1)
k2 = Cartes(couleur="carreau", valeur=2)
k3 = Cartes(couleur="carreau", valeur=3)
k4 = Cartes(couleur="carreau", valeur=4)
k5 = Cartes(couleur="carreau", valeur=5)
k6 = Cartes(couleur="carreau", valeur=6)
k7 = Cartes(couleur="carreau", valeur=7)
k8 = Cartes(couleur="carreau", valeur=8)
k9 = Cartes(couleur="carreau", valeur=9)
k10 = Cartes(couleur="carreau", valeur=10)
k11 = Cartes(couleur="carreau", valeur=11)
k12 = Cartes(couleur="carreau", valeur=12)
k13 = Cartes(couleur="carreau", valeur=13)
 
p1 = Cartes(couleur="pique", valeur=1)
p2 = Cartes(couleur="pique", valeur=2)
p3 = Cartes(couleur="pique", valeur=3)
p4 = Cartes(couleur="pique", valeur=4)
p5 = Cartes(couleur="pique", valeur=5)
p6 = Cartes(couleur="pique", valeur=6)
p7 = Cartes(couleur="pique", valeur=7)
p8 = Cartes(couleur="pique", valeur=8)
p9 = Cartes(couleur="pique", valeur=9)
p10 = Cartes(couleur="pique", valeur=10)
p11 = Cartes(couleur="pique", valeur=11)
p12 = Cartes(couleur="pique", valeur=12)
p13 = Cartes(couleur="pique", valeur=13)
 
t1 = Cartes(couleur="trefle", valeur=1)
t2 = Cartes(couleur="trefle", valeur=2)
t3 = Cartes(couleur="trefle", valeur=3)
t4 = Cartes(couleur="trefle", valeur=4)
t5 = Cartes(couleur="trefle", valeur=5)
t6 = Cartes(couleur="trefle", valeur=6)
t7 = Cartes(couleur="trefle", valeur=7)
t8 = Cartes(couleur="trefle", valeur=8)
t9 = Cartes(couleur="trefle", valeur=9)
t10 = Cartes(couleur="trefle", valeur=10)
t11 = Cartes(couleur="trefle", valeur=11)
t12 = Cartes(couleur="trefle", valeur=12)
t13 = Cartes(couleur="trefle", valeur=13)



# 1. Carte haute : aucune paire, aucune suite, aucune couleur
sept1=[c13,k3,k5,t9,t11,p6,p1]               # attendu : combo 0, combinaison vide, kickers As Dame 10 7 6
combo_c1=[]
kicker_c1=[c13,t11,t9,p6,k5]

# 2. Paire d'as
sept2=[c13,k13,k5,t9,t11,p6,p1]              # attendu : combo 1 (paire d'as), kickers Dame 10 7
combo_c2=[c13,k13]
kicker_c2=[t11,t9,p6]

# 3. Double paire (9 et 6)
sept3=[c8,k8,k5,t5,t11,p6,p1]                # attendu : combo 2 (9 9 6 6), kicker Dame
combo_c3=[c8,k8,k5,t5]
kicker_c3=[t11]

# 4. Brelan de 9
sept4=[c8,k8,t8,t5,t11,p6,p1]                # attendu : combo 3 (9 9 9), kickers Dame 7
combo_c4=[c8,k8,t8]
kicker_c4=[t11,p6]

# 5. Suite 4-5-6-7-8, avec deux cartes en trop (Dame, As)
sept5=[k3,p4,t5,p6,c7,t11,c13]               # attendu : combo 4 (suite), combinaison 4 5 6 7 8, pas de kicker
combo_c5=[k3,p4,t5,p6,c7]
kicker_c5=[]

# 6. Couleur de carreau, avec en plus une paire d'as : la couleur doit gagner
sept6=[k3,k13,k5,k8,k9,t11,c13]             # attendu : combo 5 (couleur : As 10 9 6 4), pas de kicker
combo_c6=[k13,k9,k8,k5,k3]
kicker_c6=[]

# 7. Full : brelan de 9 + paire de 6
sept7=[c8,t8,k5,k8,t5,t11,c13]               # attendu : combo 6 (9 9 9 6 6), pas de kicker
combo_c7=[c8,t8,k8,k5,t5]
kicker_c7=[]

# 8. Carré de 9
sept8=[c8,k8,t8,p8,t11,p6,p1]                # attendu : combo 7 (9 9 9 9), kicker Dame
combo_c8=[c8,k8,t8,p8]
kicker_c8=[t11]


# 9. Sept carreaux qui se suivent (6 à Dame) : on garde les 5 plus hauts
sept9=[k5,k8,k7,k6,k9,k10,k11]               # attendu : combo 8 (quinte flush 8 9 10 Valet Dame), le 6 et le 7 écartés
combo_c9=[k7,k8,k9,k10,k11]
kicker_c9=[]


# 10. Sept carreaux qui se suivent (8 à As) : la quinte flush royale
sept10=[k11,k9,k8,k7,k12,k10,k13]             # attendu : combo 9 (quinte flush royale 10 Valet Dame Roi As), le 8 et le 9 écartés
combo_c10=[k9,k10,k11,k12,k13]
kicker_c10=[]


# 11. La roue (A-2-3-4-5)
sept11 = [c13, k1, t2, p3, c4, k12, t8]       # attendu : combo 4 (suite), As en première position
combo_c11=[c13,k1,t2,p3,c4]
kicker_c11=[]


# 12. Suite 5-9 + paire de 9 dans les mêmes sept cartes
sept12 = [c4, k5, t6, p7, c8, k8, t12]        # attendu : combo 4 (la suite bat la paire)
combo_c12=[c4,k5,t6,p7,c8]
kicker_c12=[]

# 13. Deux brelans (9-9-9 et 5-5-5)
sept13 = [c8, k8, t8, c4, k4, t4, p12]        # attendu : combo 6 (full : 9 9 9 5 5, pas de kicker)
combo_c13=[c8,k8,t8,k4,t4]
kicker_c13=[]



# 14. Trois paires (Roi, 9, 6) + un 4
sept14 = [c12, k12, c8, k8, t5, p5, t3]       # attendu : combo 2 (double paire Roi-9), kicker = un 6
combo_c14=[c12,k12,c8,k8]
kicker_c14=[t5]


# 15. Couleur à six cartes de cœur
sept15 = [c13, c10, c8, c6, c3, c1, t4]       # attendu : combo 5 (couleur : 13 10 8 6 3), le 2 de cœur écarté
combo_c15=[c13,c10,c8,c6,c3]
kicker_c15=[]


test=[sept1,sept2,sept3,sept4,sept5,sept6,sept7,sept8,sept9,sept10,sept11,sept12,sept13,sept14,sept15]
combo_attendu=[0,1,2,3,4,5,6,7,8,9,4,4,6,2,5]
combos=[combo_c1,combo_c2,combo_c3,combo_c4,combo_c5,combo_c6,combo_c7,combo_c8,combo_c9,combo_c10,combo_c11,combo_c12,combo_c13,combo_c14,combo_c15]
kickers=[kicker_c1,kicker_c2,kicker_c3,kicker_c4,kicker_c5,kicker_c6,kicker_c7,kicker_c8,kicker_c9,kicker_c10,kicker_c11,kicker_c12,kicker_c13,kicker_c14,kicker_c15]
erreurs=0
for i,sept in enumerate(test):
    print(f"{i+1}.")
    combo_c=combos[i]
    kicker_c=kickers[i]
    h.cartes_jouables=sept
    h.L_valeur=[j.valeur for j in sept]
    main_special,cartes_combo,cartes_kicker=h.analyse_main()
    if main_special!=combo_attendu[i]:
        print("combo faux")
        erreurs+=1
    if cartes_combo!=combo_c:
        print("les cartes de combo sont fausses")
        erreurs+=1
    if cartes_kicker!=kicker_c:
        print("les cartes de kicker sont fausses") 
        erreurs+=1
    print(main_special,cartes_combo,cartes_kicker)
    print("")




def joueur(nom, main, board):
    j = joueurs.Joueurs(nom, 1000)
    sept = main + board
    h.cartes_jouables = sept
    h.L_valeur = [x.valeur for x in sept]
    j.combo, j.cartes_combo, j.cartes_kicker = h.analyse_main()
    return j

def verifier(num, gagnants, attendus):
    global erreurs
    noms = sorted(g.nom for g in gagnants)
    if noms == sorted(attendus):
        print(f"{num}. ok  {noms}")
    else:
        print(f"{num}. PROBLÈME : obtenu {noms}, attendu {sorted(attendus)}")
        erreurs += 1

        


# 1. Combos différents : le brelan bat la paire
board = [k1, p6, c8, t3, k12]
A = joueur("Alice", [c13, t13], board)         # paire d'as
B = joueur("Bob",   [c8, k8],   board)          # brelan de 9
verifier(1, jeu.def_gagnant([A, B]), ["Bob"])

# 2. Même combo (paire) : la paire la plus haute gagne
board = [k1, p6, c8, t3, k5]
A = joueur("Alice", [c13, t13], board)         # paire d'as
B = joueur("Bob",   [c12, t12], board)         # paire de rois
verifier(2, jeu.def_gagnant([A, B]), ["Alice"])

# 3. Même paire d'as : le premier kicker départage (roi > dame)
board = [t13, k1, p6, c8, t10]
A = joueur("Alice", [p13, c12], board)         # paire d'as, kickers R V 9
B = joueur("Bob",   [k13, c11], board)         # paire d'as, kickers D V 9
verifier(3, jeu.def_gagnant([A, B]), ["Alice"])

# 4. Égalité parfaite : les deux jouent la quinte du board, le pot est partagé
board = [c9, k10, t11, p12, c13]               # 10 V D R A : suite sur le board
A = joueur("Alice", [k1, p2], board)
B = joueur("Bob",   [t3, c4], board)
verifier(4,jeu.def_gagnant([A, B]), ["Alice", "Bob"])

# 5. La roue perd contre une suite plus haute (l'As compte 0)
board = [c1, k2, t3, p4, k12]
A = joueur("Alice", [c13, t8], board)          # as 2 3 4 5 : la roue
B = joueur("Bob",   [p5, p8],  board)          # 2 3 4 5 6
verifier(5,jeu.def_gagnant([A, B]), ["Bob"])

# 6. Deux couleurs : la 5e carte départage
board = [c13, c12, c8, c4, t11]
A = joueur("Alice", [c1, t5], board)           # coeurs : as k 9 5 2
B = joueur("Bob",   [c2, t6], board)           # coeurs : as k 9 5 3
verifier(6,jeu.def_gagnant([A, B]), ["Bob"])

# 7. Trois joueurs, dans tous les ordres : le gagnant ne dépend pas de l'ordre de la liste
board = [k1, p6, c8, t3, k12]
A = joueur("Alice", [c13, t13], board)         # paire d'as
B = joueur("Bob",   [c8, k8],   board)          # brelan de 9  gagnant
C = joueur("Carole", [p12, t7],  board)         # paire de rois
print("ABC:")
verifier(7, jeu.def_gagnant([A,B,C]), ["Bob"])
print("ACB:")
verifier(7, jeu.def_gagnant([A,C,B]), ["Bob"])
print("BAC:")
verifier(7, jeu.def_gagnant([B,A,C]), ["Bob"])
print("BCA:")
verifier(7, jeu.def_gagnant([B,C,A]), ["Bob"])
print("CAB:")
verifier(7, jeu.def_gagnant([C,A,B]), ["Bob"])
print("CBA:")
verifier(7, jeu.def_gagnant([C,B,A]), ["Bob"])

# 8. Cas limites : un seul joueur, aucun joueur
verifier(8,jeu.def_gagnant([A]), ["Alice"])
verifier(8,jeu.def_gagnant([]), [])


if erreurs!=0:
    print(f"Vous avez {erreurs} erreurs, allez verifier")
else:
    print("Tout bon pas d'erreur")