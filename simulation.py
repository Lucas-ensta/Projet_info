from labyrinthe import *
from fourmi import Fourmi
from case import *
from comportement import Exploration, Retour, Suivi 
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
            # print(f"déplacement fourmi : {fourmi.position} -> ")
            fourmi.se_deplacer(self.labyrinthe)
            # print(f"nouvelle position : {fourmi.position}")

        # 4. Suppression des fourmis sur la nourriture
        fourmis_sur_nourriture = []
        for fourmi in self.fourmis:
            (i, j) = fourmi.position
            if self.labyrinthe.etat_case[i][j].nourriture > 0:
                fourmis_sur_nourriture.append(fourmi)
        for fourmi in fourmis_sur_nourriture:
            self.fourmis.remove(fourmi)
            print(f"Fourmi supprimée (mange) à la position {fourmi.position}")

        # 5. Fusion des fourmis sur une même case
        nouvelles_fourmis = []
        positions_vues = set() #ensemble ne pouvant pas contenir de doublons

        for fourmi in self.fourmis:
            if fourmi.position not in positions_vues:
                nouvelles_fourmis.append(fourmi)
                positions_vues.add(fourmi.position)
            else:
                print(f"Fourmi supprimée pour éviter doublon à la position {fourmi.position}")

        self.fourmis = nouvelles_fourmis

        # 6. Dépôt de phéromones
        for fourmi in self.fourmis:
            fourmi.deposer_pheromone(self.labyrinthe, quantite=1)
        # 7. choix comportement 
        for fourmi in self.fourmis : 
            fourmi.decider_comportement(self.labyrinthe)
        # 7. Incrément du compteur de tours
        self.tour += 1

        print(f"{self.fourmis}")

