import labyrinthe
import case 
import comportement 
import random

class Fourmi :
    """
    Cette classe gère les fourmis, leurs propriétés et tout ce qu'il est possible de faire
    """

    def __init__(self,position):
        self.position = position
        self.memoire = None
        self.comportement = None

    def chemins_possible(self,labyrinthe):
        """
        Cette méthode permet de percevoir les murs adjacents et de retourner les chemins possibles
        :return: Les chemins possibles
        """
        (i,j) = self.position
        directions_possibles = []
        #Si on n'est pas sur une case adjacente à un bord
        if labyrinthe.murs_v[i,j-1] == 0 and j != 0: #Si on a pas de mur à gauche, on ajoute la direction
            directions_possibles.append("gauche")
        if labyrinthe.murs_v[i,j] == 0 and j != labyrinthe.murs_v.shape[1]: #Si on a pas de mur à droite, on ajoute la direction
            directions_possibles.append("droite")
        if labyrinthe.murs_h[i-1,j] == 0 and i != 0: #Si on a pas de mur au dessus, on ajoute la direction
            directions_possibles.append("haut")
        if labyrinthe.murs_h[i,j] == 0 and i != labyrinthe.murs_h.shape[0]: #Si on a pas de mur à gauche, on ajoute la direction
            directions_possibles.append("bas")

        #Si on est sur une case adjacente à un bord
        if i == 0 :  #Bord supérieur
            if j == 0 : #Coin en haut à gauche
                if labyrinthe.murs_v[i,j] == 0 : #Si on a pas de mur à droite, on ajoute la direction
                    directions_possibles.append("droite")
                if labyrinthe.murs_h[i,j] == 0 : #Si on a pas de mur à gauche, on ajoute la direction
                    directions_possibles.append("bas")
            elif j == labyrinthe.murs_h.shape[1]: #Coin en haut à droite
                if labyrinthe.murs_v[i, j - 1] == 0 :  # Si on a pas de mur à gauche, on ajoute la direction
                    directions_possibles.append("gauche")
                if labyrinthe.murs_h[i,j] == 0 : #Si on a pas de mur à gauche, on ajoute la direction
                    directions_possibles.append("bas")
            else:
                if labyrinthe.murs_v[i, j - 1] == 0:  # Si on a pas de mur à gauche, on ajoute la direction
                    directions_possibles.append("gauche")
                if labyrinthe.murs_v[i, j] == 0: # Si on a pas de mur à droite, on ajoute la direction
                    directions_possibles.append("droite")
                if labyrinthe.murs_h[i, j] == 0: # Si on a pas de mur à gauche, on ajoute la direction
                    directions_possibles.append("bas")

        if i == labyrinthe.murs_h.shape[0] :  #Bord inférieur
            if j == 0 : #Coin en bas à gauche
                if labyrinthe.murs_v[i,j] == 0 : #Si on a pas de mur à droite, on ajoute la direction
                    directions_possibles.append("droite")
                if labyrinthe.murs_h[i - 1, j] == 0 :  # Si on a pas de mur au dessus, on ajoute la direction
                    directions_possibles.append("haut")
            elif j == labyrinthe.murs_h.shape[1]: #Coin en bas à droite
                if labyrinthe.murs_v[i, j - 1] == 0 :  # Si on a pas de mur à gauche, on ajoute la direction
                    directions_possibles.append("gauche")
                if labyrinthe.murs_h[i - 1, j] == 0 :  # Si on a pas de mur au dessus, on ajoute la direction
                    directions_possibles.append("haut")
            else:
                if labyrinthe.murs_v[i, j - 1] == 0:  # Si on a pas de mur à gauche, on ajoute la direction
                    directions_possibles.append("gauche")
                if labyrinthe.murs_v[i, j] == 0: # Si on a pas de mur à droite, on ajoute la direction
                    directions_possibles.append("droite")
                if labyrinthe.murs_h[i - 1, j] == 0 :  # Si on a pas de mur au dessus, on ajoute la direction
                    directions_possibles.append("haut")

        #Si on est sur le bord gauche ou droit
        if i != 0 and i != labyrinthe.murs_h.shape[0] :
            if j == 0 :
                if labyrinthe.murs_v[i, j] == 0 and j != labyrinthe.murs_v.shape[1]:  # Si on a pas de mur à droite, on ajoute la direction
                    directions_possibles.append("droite")
                if labyrinthe.murs_h[i - 1, j] == 0 and i != 0:  # Si on a pas de mur au dessus, on ajoute la direction
                    directions_possibles.append("haut")
                if labyrinthe.murs_h[i, j] == 0 and i != labyrinthe.murs_h.shape[0]:  # Si on a pas de mur à gauche, on ajoute la direction
                    directions_possibles.append("bas")
            elif j == labyrinthe.murs_v.shape[1] :
                if labyrinthe.murs_h[i - 1, j] == 0 and i != 0:  # Si on a pas de mur au dessus, on ajoute la direction
                    directions_possibles.append("haut")
                if labyrinthe.murs_h[i, j] == 0 and i != labyrinthe.murs_h.shape[0]:  # Si on a pas de mur à gauche, on ajoute la direction
                    directions_possibles.append("bas")
                if labyrinthe.murs_v[i, j - 1] == 0:  # Si on a pas de mur à gauche, on ajoute la direction
                    directions_possibles.append("gauche")

        return(directions_possibles)

    def percevoir_pheromone(self,labyrinthe):
        """
        Cette méthode permet de percevoir les phéromones qui se trouvent sur les cases adjacentes accessibles
        :param chemins_possibles:
        :param cases: Cases adjacentes
        :return: Dictionnaire des positions avec phéromones
        """
        i,j = self.position
        


        pass 






            
    def percevoir_nourriture(self,labyrinthe,position_case):
        """
        Cette méthode permet de vérifier si il y a de la nourriture sur les cases voisines
        :param labyrinthe:
        :param position de la case:
        :return: Booléen vrai s'il y a de la nourriture sur la case 
        """
        i,j = position_case[0], position_case[1]
        return labyrinthe.etat_case.nourriture[i][j]

    def deposer_pheromone (self):
        pass

    def se_deplacer(self, lab):
        """
        permet a la fourmer de changer de case en fonction de son comportement 
        """
        direction = self.comportement.choisir_direction(self, labyrinthe)
        if direction:
            self._move_in_direction(direction)
    
    def conversion_str_int(self, str_direction): 
        """
        Cette méthode permet de connaitre les coordonées des cases adjacentes à la fourmi, utiles pour s'y déplacer si on sait dans quelle direction aller
        :param direction sous forme de string:
        :return: coordonée (couple d'entier) de la case de la direction donnée 
        """
        i, j = self.position[0], self.position[1]
        if str_direction == "haut":
            return (i-1, j)
        if str_direction == "bas":
            return (i+1, j)
        if str_direction == "gauche": 
            return (i, j-1)
        if str_direction == "droite":
            return (i, j+1)


    def _move_in_direction(self, direction):
        """
        Permet d'afffecter la nouvelle position à une fourmi lorsqu'elle sait dans quelle direction elle veut se déplcaer 
        """
        i, j = self.position[0], self.postion[1]
        if direction == "gauche":
            self.position = (i, j - 1)
        elif direction == "droite":
            self.position = (i, j + 1)
        elif direction == "haut":
            self.position = (i - 1, j)
        elif direction == "bas":
            self.position = (i + 1, j)

    def cerveau(self):
        pass
    def decider_comportement (self):
        """

        """ 







