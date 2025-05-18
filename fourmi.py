from labyrinthe import *
from comportement import Exploration, Suivi, Retour


class Fourmi :
    """
    Cette classe gère les fourmis, leurs propriétés et tout ce qu'il est possible de faire
    """

    def __init__(self,position,comportement):
        self.position = position
        self.memoire = []
        self.comportement = comportement if comportement else Exploration() #Instance des classes comportement
        self.distance = 0

    def chemins_possible(self,labyrinthe):
        """
        Cette méthode permet de percevoir les murs adjacents et de retourner les chemins possibles
        :return: Les chemins possibles
        """
        (i,j) = self.position
        directions_possibles = []
        #Si on n'est pas en haut et qu'il y a pas de mur au dessus 
        if i != 0 and labyrinthe.murs_h[i-1, j] == 0:
            directions_possibles.append("haut")
        if i != labyrinthe.largeur-1 and labyrinthe.murs_h[i,j] == 0 :
            directions_possibles.append("bas")
        if j != 0 and labyrinthe.murs_v[i,j-1] == 0 :
            directions_possibles.append("gauche")
        if j != labyrinthe.longueur-1 and labyrinthe.murs_v[i,j] == 0 :
            directions_possibles.append("droite")
    
        return(directions_possibles)

    def percevoir_pheromone(self,labyrinthe):
        """
        Cette méthode permet de percevoir les phéromones qui se trouvent sur les cases adjacentes accessibles
        :param labyrinthe : Le labyrinthe créé avec les cases
        :return: Dictionnaire des positions adjacentes avec la quantité de phéromones attractives
        """
        L = {"haut": None, "bas": None, "gauche": None, "droite": None}
        chemins = self.chemins_possible(labyrinthe)  # liste des directions possible sous forme de str
        for c in chemins:
            i, j = self.conversion_str_int(c)
            pheromone = labyrinthe.etat_case.pheromones[i][j]
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

    def deposer_pheromone (self,labyrinthe, quantite = 1):
        """
        Méthode permettant à la fourmi d'ajouter une certaine quantité d'un certain type de phéromones sur la case où elle se trouve
        :param type_pheromones: Le type de phéromones
        :param quantite: La quantité de phéromones
        :return: Nothing
        """
        (i, j) = self.position
        type = self.comportement.choisir_pheromone(self, labyrinthe) if self.comportement.choisir_pheromone(self, labyrinthe) else 0
        if type != 0 : 
            labyrinthe.etat_case[i][j].pheromones[type] += quantite

    def se_deplacer(self,labyrinthe):
        """
        Méthode permettant à la fourmi d'avancer d'une case dans la direction qu'elle souhaite
        :param labyrinthe : le labyrinthe créé
        :return: Nothing
        """
        self.distance += 1
        new_position = self.comportement.choisir_direction(self, labyrinthe) #Nouvelle position qui dépend du comportement choisi
        if len(self.memoire) == 0: #Si elle n'a rien dans sa mémoire
            self.memoire.append(self.position) #On stocke dans sa mémoire sa position, avant qu'elle ne se déplace
        elif len(self.memoire) == 1: #Si elle a déja une position
            self.memoire.pop() #On supprime la position
            self.memoire.append(self.position) #On stocke dans sa mémoire sa position, avant qu'elle ne se déplace
        self.position = self.conversion_str_int(new_position) #La position est actualisée à sa nouvelle position

    def conversion_str_int(self, str_direction):
        """
        Cette méthode permet de connaitre les coordonées des cases adjacentes à la fourmi, utiles pour s'y déplacer si on sait dans quelle direction aller
        :param str_direction : La, ou les, direction sous forme de string:
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

    def decider_comportement (self, labyrinthe):
        """
        Methode permettant à la fourmi de changer de comportement en fonction des situations qu'elle renctre dans le labyrinthe 
        """
        chemins = self.chemins_possible(labyrinthe)
        if len(chemins) == 1: 
            self.comportement = Retour()
            print(f"fourmi {self.position} : passage en mode Retour")

        if self.comportement == Exploration():
            if self.distance > 20 : 
                self.comprtement = Suivi()
                print(f"fourmi {self.position} : passage en mode Suivi")
        
        if self.comportement == Retour():
            chemins = self.chemins_possible(labyrinthe) 
            i, j = self.memoire[0]
            for c in chemins : 
                n, m = self.convertion_str_int(c)
                if (i, j) == (n, m) :
                    chemins.remove(c)
            
            if len(chemins) > 1 :  #la fourmi est sorti du cul de sac 
                self.comportement == Exploration() 
                print(f"fourmi {self.position} : passage en mode Exploration")




if __name__ == "__main__": 
    lab = Labyrinthe(10, 10)
    lab.creation_labyrinthe()
    lab.afficher_labyrinthe()
    f1 = Fourmi((0,0), Exploration())
    for _ in range (5):
        f1.se_deplacer(lab)
        print(f1.position, f1.chemins_possible(lab))

    plt.show()
   
 















            
    
        

    

    



    

   







