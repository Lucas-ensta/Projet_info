import numpy as np
import matplotlib.pyplot as plt

class Case :
    """
    Classe permettant de gérer les phéromones qui se trouvent sur les cases
    """

    def __init__(self,position):
        self.position = position
        self.pheromones = {"attractif" : 0, "répulsif" : 0} #Il existe seulement deux types de phéromones
        self.nourriture = False

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

    def poser_nourriture(self):
        """
        Méthode permettant de dire qu'il y a de la nourriture sur une case
        :return: Nothing
        """
        self.nourriture = True

    def retirer_nourriture(self):
        """
        Méthode permettant de dire qu'il n'y a pas de nourriture sur une case
        :return:
        """
        self.nourriture = False



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

