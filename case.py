import numpy as np
import matplotlib.pyplot as plt

class Case :
    """
    Classe permettant de gérer les phéromones qui se trouvent sur les cases
    """

    def __init__(self,position):
        self.position = position
        self.pheromones = {"attractif" : 0, "repulsif" : 0} #Il existe seulement deux types de phéromones
        self.nourriture = False #Si True, renseigne le lieu du puit de nourriture
        self.fourmilliere = False #Si True, renseigne le lieu de la fourmillière

    def ajouter_pheromone(self, type_pheromones, quantity):
        """
        Méthode permettant de déposer des phéromones sur une case
        :param type_pheromones: Le type des phéromones
        :param quantity: La quantité a déposer
        :return: Nothing
        """
        if type_pheromones in self.pheromones:
            self.pheromones[type_pheromones] += quantity
        else :
            self.pheromones[type_pheromones] = quantity

    def attenuer_pheromone(self, rate):
        """
        Méthode permettant d'atténuer la quantité de phéromones sur une case
        :param rate: Le taux d'atténuation
        :return: Nothing
        """
        for type_pheromone in self.pheromones:
            self.pheromones[type_pheromone] = max(0, self.pheromones[type_pheromone] * (1 - rate))

    def est_nourriture(self):
        """
        Méthode permettant de dire qu'il y a de la nourriture sur une case : c'est le puit de nourriture
        :return: Nothing
        """
        self.nourriture = True


    def est_fourmilliere(self):
        """
        Méthode permettant de positionner la fourmillière sur une case
        :return: Nothing
        """
        self.fourmilliere = True


    def contient_nourriture(self):
        """
        Méthode permettant de renvoyer l'état de la nourriture sur une case ( Oui ou Non )
        :return: Oui de la nourriture, ou Non pas de nourriture
        """
        return self.nourriture

    def lire_pheromone(self,position):
        """
        Méthode permettant au fourmi de lire les phéromones, et la quantité associée, sur les cases
        :return: Une copie du dictionnaire des phéromones
        """
        return(self.pheromones.copy())
