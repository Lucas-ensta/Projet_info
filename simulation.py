from labyrinthe import *
from fourmi import *
from case import *
from comportement import *
from matplotlib.animation import FuncAnimation

class Simulation:
    """
    Classe permettant de simuler les différentes étapes lors de la simulation
    """

    def __init__(self,labyrinthe,nb_iterations,freq_apparition=1):
        self.labyrinthe = labyrinthe
        self.nb_iterations = nb_iterations
        self.freq_apparition = freq_apparition
        self.fourmis = [] #Liste des fourmis sur le labyrinthe
        self.tour = 0 #Nombre de tour de simulation
        self.position_fourmiliere = self.labyrinthe.placer_fourmiliere_aleatoire() #Initialisation de la fourmilière
        self.puit_nourriture = self.labyrinthe.placer_nourriture_aleatoire() #Initialisation du puit de nourriture

    def generer_fourmi(self):
        """
        Méthode permettant de simuler de façon périodique l'apparitioon d'une fourmi sur la fourmillière
        :return: Nothing
        """
        if self.tour % self.freq_apparition == 0:
            # Créer une nouvelle fourmi à la position de la fourmilière
            nouvelle_fourmi = Fourmi(position=self.position_fourmiliere,comportement=Exploration())
            self.fourmis.append(nouvelle_fourmi)
            print(f"Fourmi générée au tour {self.tour} à la position {self.position_fourmiliere}")

    def etape(self):
        """
        Simule un tour de la simulation.
        """
        # 1. Atténuation des phéromones
        for element in self.labyrinthe.etat_case:
            for i in range(len(element)):
                    element[i].attenuer_pheromone(0.3)
        # 2. Apparition d'une nouvelle fourmi
        self.generer_fourmi()
        # 3. Déplacement de toutes les fourmis
        for fourmi in self.fourmis:
            fourmi.se_deplacer(self.labyrinthe)
        # 4. Suppression des fourmis sur la nourriture
        fourmis_sur_nourriture = []
        for fourmi in self.fourmis:
            i, j = fourmi.position
            if self.labyrinthe.etat_case[i][j].nourriture > 0:
                fourmis_sur_nourriture.append(fourmi)
        for fourmi in fourmis_sur_nourriture:
            self.fourmis.remove(fourmi)
            print(f"Fourmi supprimée (mange) à la position {fourmi.position}")
        # 5. Fusion des fourmis sur une même case
        position_map = {}
        for fourmi in self.fourmis:
            pos = fourmi.position
            if pos in position_map:
                position_map[pos].append(fourmi)
            else:
                position_map[pos] = [fourmi]
        nouvelles_fourmis = []
        for pos, fourmis_group in position_map.items():
            if len(fourmis_group) > 1:
                # Fusion : ici on choisit le premier comportement (à adapter)
                comportement_commun = fourmis_group[0].comportement
                nouvelle_fourmi = Fourmi(position=pos, comportement=comportement_commun)
                nouvelles_fourmis.append(nouvelle_fourmi)
            else:
                nouvelles_fourmis.append(fourmis_group[0])
        self.fourmis = nouvelles_fourmis
        # 6. Dépôt de phéromones
        for fourmi in self.fourmis:
            fourmi.deposer_pheromone(self.labyrinthe, type_pheromones="attractif", quantite=1)
        # 7. Incrément du compteur de tours
        self.tour += 1

    


"""
    def etape(self):
        for i in range(self.nb_iterations):
            self.generer_fourmi()
            for fourmi in self.fourmis:
                self.labyrinthe.afficher_fourmi(fourmi.position)
                fourmi.se_deplacer(self.labyrinthe)
            plt.pause(1)
        plt.show()

    def etape_test(self):
        fig, ax = plt.subplots()
        self.labyrinthe.afficher_labyrinthe()  # Affichage du labyrinthe
        self.labyrinthe.afficher_fourmilliere(self.position_fourmiliere)
        self.labyrinthe.afficher_nourriture(self.puit_nourriture)

        # Préparation du nuage de points pour les fourmis
        scatter_fourmis = ax.scatter([], [], c='red', s=200,marker='o')  # s = taille

        for i in range(self.nb_iterations):
            self.tour = i
            self.generer_fourmi()

            # Déplacement de chaque fourmi
            for fourmi in self.fourmis:
                fourmi.se_deplacer(self.labyrinthe)

            # Mise à jour graphique des positions
            positions = [f.position for f in self.fourmis]
            if positions:
                # matplotlib attend (x, y), soit (colonne, ligne)
                x = [pos[1] + 0.5 for pos in positions]  # +0.5 pour centrer le point
                y = [self.labyrinthe.largeur - pos[0] - 0.5 for pos in positions]
                ax.scatter.set_offsets(np.c_[x, y])  # combine x et y
            else:
                ax.scatter.set_offsets([])

            scatter_fourmis.set_offsets(list(zip(x, y)))
            plt.pause(0.5)  # Pause entre les frames

        plt.show()
"""