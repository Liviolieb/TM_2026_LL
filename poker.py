import partie
import joueurs
from nicegui import ui

partie_x =None
@ui.page('/')
def accueil():
    ui.label("Configuration de la partie").style('font-size: 1.5em')
    nb_joueurs_input = ui.number('Combien de joueurs :', value=3, min=2, max=10, format='%d')

    champ_joueurs = ui.column()
    champs = [] 

    def generer_champs():
        champ_joueurs.clear()
        champs.clear()
        nb = int(nb_joueurs_input.value)
        with champ_joueurs:
            for i in range(nb):
                with ui.row():
                    input_nom = ui.input(f"Nom du joueur {i + 1}")
                    input_solde = ui.number(f"Solde du joueur {i + 1}", value=1000)
                champs.append((input_nom, input_solde))

    ui.button("Valider le nombre de joueurs", on_click=generer_champs)

    resultat = ui.column()

    def demarrer_partie():
        global partie_x
        if not champs:
            with resultat:
                resultat.clear()
                ui.label("Valide d'abord le nombre de joueurs.")
            return
        L_joueurs = []
        for input_nom, input_solde in champs:
            nom = input_nom.value or "Joueur"
            solde = int(input_solde.value)
            L_joueurs.append(joueurs.Joueurs(nom, solde))
        partie_x = partie.partie(L_joueurs)
        resultat.clear()
        ui.navigate.to('/jeu')
        
        

    ui.button("Démarrer la partie", on_click=demarrer_partie)

@ui.page('/jeu')

async def jeu():
    if not partie_x:
         ui.navigate.to('/')
         return
    affichage=ui.column()
    with affichage:
                ui.label("Partie créée !")
                for j in partie_x.L_joueurs:
                    j.jape = ui.card()
                    with j.jape:
                        ui.label(f"{j.nom} : solde {j.solde}, cartes {[str(c) for c in j.cartes]}")
    await ui.context.client.connected()
    await partie_x.vote()


ui.run()
