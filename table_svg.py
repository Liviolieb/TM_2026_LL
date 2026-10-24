from nicegui import app
import math 
import html
from urllib.parse import quote
import table
from pathlib import Path

CARTES_DIR = Path(__file__).parent / 'cartes_j' # pour que peu importe où se trouve notre dossier on retrouve chaque fois cartes_j en revenant de 1 dossier depuis afficher
app.add_static_files('/cartes_j', str(CARTES_DIR)) # Sert les images de cartes (dossier cartes_j/) à l'URL /cartes_j/, pour pouvoir utiliser href



DENOMS = [(500, '#6a1b9a'), (100, '#212121'), (50, '#2e7d32'), (10, '#1565c0'), (1, '#eeeeee')]  # liste de couleur pour les jetons, ordre décroissant pour utiliser les plus gros jeton en premier pour la décomposition

def jeton_svg(cx, cy, r, couleur, valeur): # fonction de création de jetons
    texte = '#000000' if couleur == '#eeeeee' else '#ffffff'
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{couleur}" stroke="white" stroke-width="{r*0.1}"/> ' #premier cercle couleur du jetons avec un bord blanc
        f'<circle cx="{cx}" cy="{cy}" r="{r*0.7}" fill="none" stroke="white" stroke-width="{r*0.12}" stroke-dasharray="{r*0.4} {r*0.4}"/> ' # deuxième cercle vide avec une bordure traitillée 
        f'<text x="{cx}" y="{cy}" text-anchor="middle" dy="0.35em" font-size="{r*0.6}" fill="{texte}">{valeur}</text> ' # la valeur du jeton, en noir ou blanc selon la couleur du jeton
    )

def decomposer(montant):
    jetons = []
    for valeur, couleur in DENOMS:
        nb, montant = divmod(montant, valeur) # pour avoir le résultat de la division et le reste
        if nb!=0:
            jetons += [[(valeur, couleur)] *int(nb)]
    return jetons #retourne une pile(liste) de liste (valeur, couleur)

def table_jolie(partie_x,joueur_table=None):

    cx, cy, rx, ry = 200, 150, 140, 75 #centre et rayon de l'ellipse
    nb = len(partie_x.L_joueurs)
    distance_b=10
    w_r=15
    h_r=25
    distance_nom=35 
    distance_mise =25
    elements =[f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"'
                f'fill="#8B5A2B" stroke="navy" stroke-width="4"/>' 
                f'<ellipse cx="{cx}" cy="{cy}" rx="{rx-30}" ry="{ry-30}"'
                f'fill="green" />']
    rcx = rx -15
    rcy = ry -15

    th = html.escape("Texas hold'em") # pour pouvoir mettre le '
    elements.append(
        f'<text x="{cx}" y="{cy + 25}" text-anchor="middle" '
        f'dominant-baseline="middle" font-size="8" fill="gold" >{table.Table.etape_libelles[table.Table.type_etape[partie_x.table_partie.etape]]}</text> '

        f'<text x="{cx}" y="{cy - 25}" text-anchor="middle" dominant-baseline="middle"'
        f'font-family="Georgia, serif" font-weight="bold" font-size="15"'
        f'fill="gold" stroke="black" stroke-width="1">{th}</text>')

    #je voulais utiliser des angles égaux pour répartir les joueurs mais cela paraissait injuste sur la table alors j'ai du changer de methode
    def points_equidistants(cx, cy, a, b, nb, echantillons=1000): # fonction pour déterminer la positions de points equidistant sur le périmètre d'une ellipse
        ts = [(2 * math.pi * k / echantillons)+math.pi/2 for k in range(echantillons + 1)] # t décrit un tour complet de l'ellipse (période 2π), en partant de π/2 = point du bas
        pts = [(cx + a * math.cos(t), cy + b * math.sin(t)) for t in ts] # formule de l'ellipse pour trouver son x et son y à partir d'un paramètre périodique
        s=[0.0] #la liste qui va contenir pour chaque point sa distance sur l'arc d'ellipse avec le point 0 (pi/2)
        for i in range (len(pts)-1): # à chaque point on regarde la distance entre ce dernier et celui qui arrive juste après
            x0,y0=pts[i]
            x1,y1=pts[i+1]
            s.append(s[-1]+math.hypot(x1 - x0, y1 - y0))#on additionne avec le résultat qu'on a eu juste avant
        L=s[-1] #le dernier résultat est donc le périmètre de l'ellipse
        resultat=[]
        for i in range (nb) : # on cherche un élément de s qui correspond à la fraction i/nb de la longueur totale (chaque fois à la distance L/nb du précédent)
            cible=L*i/nb 
            g=0
            position=0
            for k in range(len(s)): #on parcours tout s pour trouver le premier échantillon dont la longueur cumulée atteint la cible
                if g < cible:
                    g=s[k]
                    position=k
            resultat.append((pts[position],ts[position])) #on peut donc avoir un point et un angle

        return(resultat)
    L=points_equidistants(cx,cy,rcx,rcy,nb)
    index=0
    if joueur_table: # si on a pas de joueur_table on veut un joueur 0 en bas sinon le joueur en question en bas
        index=partie_x.L_joueurs.index(joueur_table)
    for j in range(len(L)):
        (x,y),t= L[j]
        joueur = partie_x.L_joueurs[index]
        if j==0 and joueur_table is not None:  #j==0 donc on construit le joueur en bas, si on a un joueur_table il est en bas, on révele donc ses cartes

            href1=f"/cartes_j/{joueur_table.cartes[0].couleur}/{joueur_table.cartes[0].valeur}.png"
            href2=f"/cartes_j/{joueur_table.cartes[1].couleur}/{joueur_table.cartes[1].valeur}.png"
        else:
            if partie_x.revel_c is True: # si il faut réveler les cartes de tout les joueurs on le fait
                href1=f"/cartes_j/{joueur.cartes[0].couleur}/{joueur.cartes[0].valeur}.png"
                href2=f"/cartes_j/{joueur.cartes[1].couleur}/{joueur.cartes[1].valeur}.png"
            else:
                href1="/cartes_j/verso.png"
                href2=href1
            

        tx= -rcx * math.sin(t) # dérivée pour trouver les vecteurs tangents
        ty=rcy * math.cos(t)
        norme = math.hypot(tx, ty)
        ux = tx / norme #on les normalises (vecteur unitaire)
        uy= ty / norme

        x1 = x + distance_b * ux # on place les cartes à une certaine distance du siège (on peut les déplacer grace au vecteur unitaire trouvé en haut)
        y1 = y + distance_b * uy
        x2 = x - distance_b * ux
        y2 = y - distance_b * uy

        xr1= x1 - w_r/2 #placés par leur coin supérieur gauche, on décale d’une demi-taille pour les centrer sur (x1, y1)
        yr1= y1 - h_r/2
        xr2= x2 - w_r/2
        yr2= y2 - h_r/2

        unx = -uy #le vecteur unitaire normale
        uny= ux

        x_nom= x - distance_nom * unx # nom : vers l'extérieur de la table
        y_nom= y- distance_nom * uny 

        x_jeton= x +distance_mise * unx # jetons : vers l'intérieur
        y_jeton = y + distance_mise * uny

        nom = html.escape(joueur.nom)      # échappement : le nom et solde vient de l'utilisateur
        solde= html.escape(f"{joueur.solde}")
        if joueur_table == joueur: # si le joueur qu'on regarde en ce moment est celui chez qui on dessine la table on le vouvoie
            elements.append(
                f'<text x="{x_nom}" y="{y_nom}" text-anchor="middle" '
                f'dominant-baseline="middle" font-size="8" fill="gold" >Vous</text> ')
        else:
            if joueur_table is None: #sur la table de /jeu on veut pouvoir cliquer sur les noms 
                largeur = max(30, 6 + 4.4*len(nom))  #approximation de la largeur du nom par rapport à la font size et si le prénom trop petit on utilise 30
                forme = (
                    f'<rect x="{x_nom-largeur/2}" y="{y_nom-6.5}" width="{largeur}" height="13" rx="6.5" '
                    f'fill="gold" fill-opacity="0.15" stroke="gold" stroke-width="0.5"/> ' # légerement opaque sinon on le vois pas ou alors il prend trop de place
                    f'<text x="{x_nom}" y="{y_nom}" dy="0.35em" text-anchor="middle" font-size="8" fill="gold">{nom}</text> '
                    )
                elements.append(f'<a class="nom-joueur" href="/jeu/{quote(joueur.nom, safe="")}" target="_blank" rel="noopener" style="cursor:pointer">{forme}</a> ')
            else:
                elements.append(
                    f'<text x="{x_nom}" y="{y_nom}" text-anchor="middle" '
                    f'dominant-baseline="middle" font-size="8" fill="gold" >{nom}</text> ')
        pile=decomposer(joueur.mise)
        for k in range(len(pile)) : # pour chaque montant de jeton on fait une nouvelle pile
            pile_c=pile[k]
            for i in range(len(pile_c)):
                valeur,couleur= pile_c[i]
                elements.append(jeton_svg(x_jeton+4*k,y_jeton-2*i,3,couleur,valeur)) #on construit un jeton et on le rajoute à la pile en le décalant légerement, et pour chaque couleur différente on décale vers la droite)
        # on écrit la solde en dessus du nom du joueur
        elements.append(
            f'<text x="{x_nom}" y="{y_nom-10}" text-anchor="middle" '
            f'dominant-baseline="middle" font-size="8" fill="gold" >{solde}</text> ')
            

        angle = math.degrees(math.atan2(ty, tx)) # retrouver l'angle avec l'horizontale (atan2 plutôt que atan car gère x=0 et distingue les 4 quadrants)
        #on tourne sur x1 y1 car on veut tourner sur le centre de la carte et pas le coin
        if joueur in(partie_x.L_gagnants) : # on met les cartes en doré du joueur gagnants
            elements.append(f'<rect x="{xr1}" y="{yr1}" width="{w_r}" height="{h_r}"'
                            f'fill="none" stroke="gold" stroke-width="2" rx="2" transform="rotate({angle} {x1} {y1})"/>') 
            elements.append(f'<rect x="{xr2}" y="{yr2}" width="{w_r}" height="{h_r}"'
                                f'fill="none" stroke="gold" stroke-width="2" rx="2" transform="rotate({angle} {x2} {y2})"/>')
        else:
            elements.append(f'<rect x="{xr1}" y="{yr1}" width="{w_r}" height="{h_r}"'
                            f'fill="none" stroke="black" stroke-width="2" rx="2" transform="rotate({angle} {x1} {y1})"/>')
            elements.append(f'<rect x="{xr2}" y="{yr2}" width="{w_r}" height="{h_r}"'
                                f'fill="none" stroke="black" stroke-width="2" rx="2" transform="rotate({angle} {x2} {y2})"/>')
        if joueur.couche is not True: # si le joueur n'est pas couché on affiche le verso ou le recto de ses carte (voir plus haut pour href1 et href2)
            elements.append(f'<image href={href1} x="{xr1}" y="{yr1}" width="{w_r}" height="{h_r}" transform="rotate({angle} {x1} {y1})"/>')
            elements.append(f'<image href={href2} x="{xr2}" y="{yr2}" width="{w_r}" height="{h_r}" transform="rotate({angle} {x2} {y2})"/>')

        if joueur.en_vote is True: # si le joueur qu'on dessine est en train de voter on veut lui dessiner un spinner 
            ar = 5 # le rayon du spinner
            c = 2*math.pi*ar #périmètre spinner
            arc = c/4 # un quart du périmètre
            if joueur_table: #si on est chez un joueur juste en dessous du nom 
                position=10
            else: # dans /jeu le <a> prend un peu plus de place env 13 unités au lieu de 8
                position=15
            elements.append(
            f'<circle cx="{x_nom}" cy="{y_nom+position}" r="{ar}" fill="none" stroke="#DDDDDD" stroke-width="2"/> '
            f'<circle cx="{x_nom}" cy="{y_nom+position}" r="{ar}" fill="none" stroke="steelblue" stroke-width="2" '
                f'stroke-linecap="round" '
                f'stroke-dasharray="{arc} {c-arc}"> '
            f'<animateTransform attributeName="transform" type="rotate" ' # on fait tourner l'arc en rond 
                f'from="-90 {x_nom} {y_nom+position}" to="270 {x_nom} {y_nom+position}" '
                f'dur="1s" repeatCount="indefinite"/> '
                '</circle>')
            
        index = (index+1) % len(partie_x.L_joueurs) # pour passer au prochain joueur (modulo pour revenir à 0 après le dernier)


            

    """ for i in range(nb):
        t = 2 * math.pi * i / nb + math.pi / 2
        x = cx + rcx * math.cos(t)
        y = cy + rcy * math.sin(t)

        tx= -rcx * math.sin(t) 
        ty=rcy * math.cos(t)
        norme = math.hypot(tx, ty)
        ux = tx / norme
        uy= ty / norme

        x1 = x + distance_b * ux 
        y1 = y + distance_b * uy
        x2 = x - distance_b * ux
        y2 = y - distance_b * uy

        xr1= x1 - w_r/2
        yr1= y1 - h_r/2
        xr2= x2 - w_r/2
        yr2= y2 - h_r/2

        angle = math.degrees(math.atan2(ry * math.cos(t), -rx * math.sin(t)))

        elements.append(f'<rect x="{xr1}" y="{yr1}" width="{w_r}" height="{h_r}"'
                        f'fill="none" stroke="black" stroke-width="4" rx="2" transform="rotate({angle} {x1} {y1})"/>')
        elements.append(f'<rect x="{xr2}" y="{yr2}" width="{w_r}" height="{h_r}"'
                            f'fill="none" stroke="black" stroke-width="4" rx="2" transform="rotate({angle} {x2} {y2})"/>')
        elements.append(f'<image href="/cartes_j/verso.png" x="{xr1}" y="{yr1}" width="{w_r}" height="{h_r}" transform="rotate({angle} {x1} {y1})"/>')
        elements.append(f'<image href="/cartes_j/verso.png" x="{xr2}" y="{yr2}" width="{w_r}" height="{h_r}" transform="rotate({angle} {x2} {y2})"/>')
    """
        
    n=0
    for i in range (partie_x.table_partie.etape):
        for k in range (len(partie_x.table_partie.liste[i])): #on parcourt les carte de la table (à l'étape en cours)
            rect=False
            for joueur in partie_x.L_gagnants: 
                if partie_x.table_partie.liste[i][k] in (joueur.cartes_jouee) and partie_x.revel_c is True: # si elle est dans les cartes du joueur gagnant et qu'on révèle nos carte alors on les entoure de doré
                    elements.append(f'<rect x="{(cx-(2.5*w_r+2*distance_b))+n*(w_r+distance_b)}" y="{cy-(h_r/2)}" width="{w_r}" height="{h_r}" fill="none" stroke="gold" stroke-width="2" rx="2"/>')
                    rect=True
                    break
            if rect is False:
                   elements.append(f'<rect x="{(cx-(2.5*w_r+2*distance_b))+n*(w_r+distance_b)}" y="{cy-(h_r/2)}" width="{w_r}" height="{h_r}" fill="none" stroke="black" stroke-width="2" rx="2"/>')
            elements.append(f'<image href="/cartes_j/{partie_x.table_partie.liste[i][k].couleur}/{partie_x.table_partie.liste[i][k].valeur}.png" x="{(cx-(2.5*w_r+2*distance_b))+n*(w_r+distance_b)}" y="{cy-(h_r/2)}" width="{w_r}" height="{h_r}"/>')
            n+=1 #on rajoute l'image de la carte et on ajoute 1 à n pour le rapprocher de 5 (le board fait 5 cartes au poker)
    while n<5: # pour completer n jusqu'à 5 on rajoute des verso
        elements.append(f'<image href="/cartes_j/verso.png" x="{(cx-(2.5*w_r+2*distance_b))+n*(w_r+distance_b)}" y="{cy-(h_r/2)}" width="{w_r}" height="{h_r}"/>')
        elements.append(f'<rect x="{(cx-(2.5*w_r+2*distance_b))+n*(w_r+distance_b)}" y="{cy-(h_r/2)}" width="{w_r}" height="{h_r}" fill="none" stroke="black" stroke-width="2" rx="2"/>')
        n+=1

    #l'élément svg auquel on va rajouter tout nos éléments
    #il prend toute la place qui lui est accordé en préservant son ratio
    svg = f'''
    <svg viewBox="25 35 350 240" preserveAspectRatio="xMidYMid meet"
        style="width: 100%; height: auto; display: block;" xmlns="http://www.w3.org/2000/svg">
        {''.join(elements)}
    </svg>
    '''
    return(svg)

