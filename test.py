from nicegui import ui, app
import math 
import html

app.add_static_files('/cartes_j', 'cartes_j')



DENOMS = [(500, '#6a1b9a'), (100, '#212121'), (50, '#2e7d32'), (10, '#1565c0'), (1, '#eeeeee')]  # du plus grand au plus petit

def jeton_svg(cx, cy, r, couleur, valeur):
    texte = '#000000' if couleur == '#eeeeee' else '#ffffff'
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{couleur}" stroke="white" stroke-width="{r*0.1}"/> '
        f'<circle cx="{cx}" cy="{cy}" r="{r*0.7}" fill="none" stroke="white" stroke-width="{r*0.12}" stroke-dasharray="{r*0.4} {r*0.4}"/> '
        f'<text x="{cx}" y="{cy}" text-anchor="middle" dy="0.35em" font-size="{r*0.6}" fill="{texte}">{valeur}</text> '
    )

def decomposer(montant):
    jetons = []
    for valeur, couleur in DENOMS:
        nb, montant = divmod(montant, valeur)
        if nb!=0:
            jetons += [[(valeur, couleur)] *int(nb)]
    return jetons

def table_jolie(partie_x,joueur_table=None):

    cx, cy, rx, ry = 200, 150, 140, 75
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

    def points_equidistants(cx, cy, a, b, nb, echantillons=1000):
        ts = [(2 * math.pi * k / echantillons)+math.pi/2 for k in range(echantillons + 1)]
        pts = [(cx + a * math.cos(t), cy + b * math.sin(t)) for t in ts]
        s=[0.0]
        for i in range (len(pts)-1):
            x0,y0=pts[i]
            x1,y1=pts[i+1]
            s.append(s[-1]+math.hypot(x1 - x0, y1 - y0))
        L=s[-1]
        resultat=[]
        for i in range (nb) :
            cible=L*i/nb
            g=0
            position=0
            for k in range(len(s)):
                if g < cible:
                    g=s[k]
                    position=k
            resultat.append((pts[position],ts[position]))

        return(resultat)
    L=points_equidistants(cx,cy,rcx,rcy,nb)
    index=0
    if joueur_table:
        index=partie_x.L_joueurs.index(joueur_table)
    for j in range(len(L)):
        (x,y),t= L[j]
        joueur = partie_x.L_joueurs[index]
        if j==0 and joueur_table is not None:

            href1=f"/cartes_j/{joueur_table.cartes[0].couleur}/{joueur_table.cartes[0].valeur}.png"
            href2=f"/cartes_j/{joueur_table.cartes[1].couleur}/{joueur_table.cartes[1].valeur}.png"
        else:
            if partie_x.revel_c is True:
                href1=f"/cartes_j/{joueur.cartes[0].couleur}/{joueur.cartes[0].valeur}.png"
                href2=f"/cartes_j/{joueur.cartes[1].couleur}/{joueur.cartes[1].valeur}.png"
            else:
                href1="/cartes_j/verso.png"
                href2=href1
            

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

        unx = -uy
        uny= ux

        nx= x - distance_nom * unx
        ny= y- distance_nom * uny 

        mx= x +distance_mise * unx
        my = y + distance_mise * uny

        nom = html.escape(joueur.nom)
        solde= html.escape(f"{joueur.solde}")
        if joueur_table == joueur:
            elements.append(
                f'<text x="{nx}" y="{ny}" text-anchor="middle" '
                f'dominant-baseline="middle" font-size="8" fill="gold" >Vous</text> ')
        else:
            elements.append(
                f'<text x="{nx}" y="{ny}" text-anchor="middle" '
                f'dominant-baseline="middle" font-size="8" fill="gold" >{nom}</text> ')
        pile=decomposer(joueur.mise)
        for k in range(len(pile)) :
            pile_c=pile[k]
            for i in range(len(pile_c)):
                valeur,couleur= pile_c[i]
                elements.append(jeton_svg(mx+4*k,my-2*i,3,couleur,valeur))
        elements.append(
            f'<text x="{nx}" y="{ny-10}" text-anchor="middle" '
            f'dominant-baseline="middle" font-size="8" fill="gold" >{solde}</text> ')
        if joueur.couche is True :
            if joueur_table == joueur:
                elements.append(
                    f'<text x="{nx}" y="{ny+10}" text-anchor="middle" '
                    f'dominant-baseline="middle" font-size="8" fill="gold" > êtes couché(e)</text> ')
            else:
                elements.append(
                    f'<text x="{nx}" y="{ny+10}" text-anchor="middle" '
                    f'dominant-baseline="middle" font-size="8" fill="gold" > est couché(e)</text> ')
            
        index = (index+1) % len(partie_x.L_joueurs)

        angle = math.degrees(math.atan2(ty, tx))
        if joueur in(partie_x.L_gagnants): 
            elements.append(f'<rect x="{xr1}" y="{yr1}" width="{w_r}" height="{h_r}"'
                            f'fill="none" stroke="gold" stroke-width="2" rx="2" transform="rotate({angle} {x1} {y1})"/>')
            elements.append(f'<rect x="{xr2}" y="{yr2}" width="{w_r}" height="{h_r}"'
                                f'fill="none" stroke="gold" stroke-width="2" rx="2" transform="rotate({angle} {x2} {y2})"/>')
        else:
            elements.append(f'<rect x="{xr1}" y="{yr1}" width="{w_r}" height="{h_r}"'
                            f'fill="none" stroke="black" stroke-width="2" rx="2" transform="rotate({angle} {x1} {y1})"/>')
            elements.append(f'<rect x="{xr2}" y="{yr2}" width="{w_r}" height="{h_r}"'
                                f'fill="none" stroke="black" stroke-width="2" rx="2" transform="rotate({angle} {x2} {y2})"/>')
        if joueur.couche is not True:
            elements.append(f'<image href={href1} x="{xr1}" y="{yr1}" width="{w_r}" height="{h_r}" transform="rotate({angle} {x1} {y1})"/>')
            elements.append(f'<image href={href2} x="{xr2}" y="{yr2}" width="{w_r}" height="{h_r}" transform="rotate({angle} {x2} {y2})"/>')

            

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
    for i in range (5):
        elements.append(f'<rect x="{(cx-(2.5*w_r+2*distance_b))+i*(w_r+distance_b)}" y="{cy-(h_r/2)}" width="{w_r}" height="{h_r}" fill="none" stroke="black" stroke-width="2" rx="2"/>')
    n=0
    for i in range (partie_x.table_partie.etape):
        for k in range (len(partie_x.table_partie.liste[i])):
            elements.append(f'<image href="/cartes_j/{partie_x.table_partie.liste[i][k].couleur}/{partie_x.table_partie.liste[i][k].valeur}.png" x="{(cx-(2.5*w_r+2*distance_b))+n*(w_r+distance_b)}" y="{cy-(h_r/2)}" width="{w_r}" height="{h_r}"/>')
            n+=1
    while n<5:
        elements.append(f'<image href="/cartes_j/verso.png" x="{(cx-(2.5*w_r+2*distance_b))+n*(w_r+distance_b)}" y="{cy-(h_r/2)}" width="{w_r}" height="{h_r}"/>')
        n+=1

    svg = f'''
    <svg viewBox="25 35 350 240" preserveAspectRatio="xMidYMid meet"
        style="width: 100%; height: 100%;" xmlns="http://www.w3.org/2000/svg">
        {''.join(elements)}
    </svg>
    '''
    return(svg)

