import numpy as np
from comportement import Super, Exploration, Retour, Suivi


class Fourmi :
    """
    Cette classe gère les fourmis, leurs propriétés et tout ce qu'il est possible de faire
    """

    def __init__(self,position,comportement):
        self.position = position
        self.memoire = []
        self.comportement = comportement if comportement else Exploration() #Instance des classes comportement
        self.distance = 0

    def chemins_possible(self, labyrinthe):
        i, j = self.position
        directions_possibles = []

        # Vérifier à gauche
        if j >= 0 and labyrinthe.murs_v[i, j - 1] == 0:
            directions_possibles.append("gauche")
        # Vérifier à droite
        if j <= (labyrinthe.murs_v.shape[1] - 1) and labyrinthe.murs_v[i, j] == 0:
            directions_possibles.append("droite")
        # Vérifier en haut
        if i >= 0 and labyrinthe.murs_h[i - 1, j] == 0:
            directions_possibles.append("haut")
        # Vérifier en bas
        if i <= (labyrinthe.murs_h.shape[0] - 1) and labyrinthe.murs_h[i, j] == 0:
            directions_possibles.append("bas")

        if j==0 and "gauche" in directions_possibles:
            directions_possibles.remove("gauche")

        if i==0 and "haut" in directions_possibles:
            directions_possibles.remove("haut")

        if j == (labyrinthe.murs_v.shape[1]) and "droite" in directions_possibles:
            directions_possibles.remove("droite")

        if i == (labyrinthe.murs_h.shape[0]) and "bas" in directions_possibles:
            directions_possibles.remove("bas")

        return directions_possibles

    def percevoir_pheromone(self,labyrinthe):
        """
        Cette méthode permet de percevoir les phéromones qui se trouvent sur les cases adjacentes accessibles
        :param labyrinthe : Le labyrinthe créé avec les cases
        :return: Dictionnaire des positions adjacentes avec la quantité de phéromones attractives
        """
        L = {"haut": 0, "bas": 0, "gauche": 0, "droite": 0}
        chemins = self.chemins_possible(labyrinthe)  # liste des directions possible sous forme de str
        for c in chemins:
            i, j = self.conversion_str_int(c)
            pheromone = labyrinthe.etat_case[i][j].pheromones
            val_case = pheromone["attractif"] - pheromone["repulsif"]
            L[c] = val_case
        return L

    def percevoir_nourriture(self,labyrinthe):
        """
        Cette méthode permet de vérifier si il y a de la nourriture sur les cases voisines
        :param labyrinthe : Le labyrinthe créée avec les cases
        :return : Dictionnaire des positions adjacentes avec la quantité de nourriture qui s'y trouve
        """
        L = {"haut": None, "bas": None, "gauche": None, "droite": None}
        chemins = self.chemins_possible(labyrinthe)  # liste des directions possible sous forme de str
        for c in chemins:
            i, j = self.conversion_str_int(c)
            val_case = labyrinthe.etat_case[i][j].nourriture
            L[c] = val_case
        return L

    def deposer_pheromone (self,labyrinthe,quantite = 1):
        """
        Méthode permettant à la fourmi d'ajouter une certaine quantité d'un certain type de phéromones sur la case où elle se trouve
        :param type_pheromones: Le type de phéromones
        :param quantite: La quantité de phéromones
        :return: Nothing
        """
        if self.position is None:
            raise ValueError ("Position inconnue")
        else :
            (i, j) = self.position
        if self.comportement.choisir_pheromone(self, labyrinthe):
            type = self.comportement.choisir_pheromone(self, labyrinthe)
        else :
            type = 0
        if type != 0:
            labyrinthe.etat_case[i][j].pheromones[type] += quantite
            print(f"J'ai déposé des phero {type} en position {(i,j)}")

    def se_deplacer(self,labyrinthe):
        """
        Méthode permettant à la fourmi d'avancer d'une case dans la direction qu'elle souhaite
        :param labyrinthe : le labyrinthe créé
        :return: Nothing
        """
        self.distance+= 1
        new_position = self.comportement.choisir_direction(self,labyrinthe) #Nouvelle position qui dépend du comportement choisi
        if len(self.memoire) == 0: #Si elle n'a rien dans sa mémoire
            self.memoire.append(self.position) #On stocke dans sa mémoire sa position, avant qu'elle ne se déplace
        elif len(self.memoire) == 1: #Si elle a déja une position
            self.memoire.pop() #On supprime la position
            self.memoire.append(self.position) #On stocke dans sa mémoire sa position, avant qu'elle ne se déplace
        if new_position in self.chemins_possible(labyrinthe):
            nouv_position = self.conversion_str_int(new_position) #La position est actualisée à sa nouvelle position
            if nouv_position[0] < 0 or nouv_position[1] < 0:
                raise ValueError ("La fourmi est sorti du labyrinthe, c'est interdit")
            self.position = nouv_position

    def conversion_str_int(self, str_direction):
        """
        Cette méthode permet de connaitre les coordonées des cases adjacentes à la fourmi, utiles pour s'y déplacer si on sait dans quelle direction aller
        :param str_direction : La direction sous forme de string:
        :return: Les coordonées (couple d'entier) de la case de la direction donnée
        """
        i, j = self.position
        if str_direction == "haut":
            return (i - 1, j)
        if str_direction == "bas":
            return (i + 1, j)
        if str_direction == "gauche":
            return (i, j - 1)
        if str_direction == "droite":
            return (i, j + 1)

    def decider_comportement(self, labyrinthe):
        """
        Methode permettant à la fourmi de changer de comportement en fonction des situations qu'elle renctre dans le labyrinthe
        :param labyrinthe
        """
        if isinstance(self.comportement, Super): #on reste en mode super jusqu'a la nourriture 
            return 
        chemins = self.chemins_possible(labyrinthe)
        #Si la fourmi est dans un cul de sac
        if len(chemins) == 1:
            self.comportement = Retour()
            print(f"fourmi {self.position} : passage en mode Retour")
        #Si la fourmi explore et qu'elle ne trouve rien, elle passe en mode suivi
        if isinstance(self.comportement, Exploration):
            if self.distance > 30:
                self.comportement = Suivi()
                print(f"fourmi {self.position} : passage en mode Suivi")
        #Si elle était dans cul de sac
        if isinstance(self.comportement, Retour):
            chemins = self.chemins_possible(labyrinthe)
            i, j = self.memoire[0]
            for c in chemins:
                n, m = self.conversion_str_int(c)
                if (i, j) == (n, m) and len(chemins) > 1 :
                    chemins.remove(c) #on retire la direction qui est le cul de sac
            if len(chemins) > 1:  # la fourmi est sorti du cul de sac
                self.comportement = Exploration()
                print(f"fourmi {self.position} : passage en mode Exploration")

        if isinstance(self.comportement, Exploration) or isinstance(self.comportement, Suivi) : 
            if self.distance >= 70 : 
                self.comportement = Super()
                print(f"fourmi {self.position} : passage en mode Super")



if __name__ == "__main__":
    pass





