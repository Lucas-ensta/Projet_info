import numpy as np
import matplotlib.pyplot as plt
from case import Case
from simulation import *

class Labyrinthe :
    """
    Classe permettant de générer et d'afficher le labyrinthe
    """

    def __init__(self,longueur,largeur):
        """
        :param longueur: nombre de colonnes des matrices
        :param largeur: nombre de lignes des matrices
        """
        self.longueur = longueur #Longueur du labyrinthe
        self.largeur = largeur #Hauteur du labyrinthe
        self.cases = np.arange(longueur*largeur).reshape(largeur,longueur)
        self.murs_v = np.ones((largeur,longueur-1),dtype=int) #Matrice initiale des murs verticuax
        self.murs_h = np.ones((largeur-1,longueur),dtype=int)  #Matrice initiale des murs horizontaux
        self.etat_case = np.array([[Case((i, j)) for i in range(self.longueur)] for j in range(self.largeur)]) #Tableau d'instance de case permettant de renseigner la fourmi sur ce qu'il y a sur la case
        self.figure = None
        self.ax = None

    def creation_labyrinthe(self):
        """
        Méthode permettant de générer le labyrinthe
        :return: Les murs horizontaux, les murs verticaux et les cases dans notre labyrinthe
        """
        murs_retires = 0
        while murs_retires < (self.longueur * self.largeur - 1) :
            a = np.random.choice(['vertical', 'horizontal'])
            if a == 'horizontal' : #On chosit un mur horizontal
                x = np.random.randint(0,self.murs_h.shape[0])
                y = np.random.randint(0,self.murs_h.shape[1])
                if self.murs_h[x,y] == 2 or self.murs_h[x,y] == 0 : #Si le mur est déjà défintif ou bien supprimé, on passe
                    continue
                #On compare les cases du dessus et du dessous
                if self.cases[x,y] == self.cases[x+1,y] : #Les valeurs sont égales, le mur devient définitif
                    self.murs_h[x,y] = 2
                else : #On fusionne des cases
                    old_value = max(self.cases[x,y],self.cases[x+1,y])
                    new_value = min(self.cases[x,y],self.cases[x+1,y])
                    self.cases[self.cases == old_value] = new_value
                    self.murs_h[x, y] = 0  # Le mur ne peut plus être choisi
                    murs_retires += 1

            else :
                x = np.random.randint(0, self.murs_v.shape[0])
                y = np.random.randint(0, self.murs_v.shape[1])
                if self.murs_v[x, y] == 2 or self.murs_v[x,y] == 0:  # Si le mur est déjà défintif, on passe
                    continue
                # On compare les cases de gauche et de droite
                if self.cases[x, y] == self.cases[x,y+1]:  # Les valeurs sont égales, le mur devient définitif
                    self.murs_v[x, y] = 2
                else:  # On fusionne des cases
                    old_value = max(self.cases[x,y], self.cases[x,y+1])
                    new_value = min(self.cases[x,y], self.cases[x,y+1])
                    self.cases[self.cases == old_value] = new_value
                    self.murs_v[x, y] = 0  # Le mur ne peut plus être choisi
                    murs_retires += 1

        return self.murs_v, self.murs_h, self.cases


    def afficher_labyrinthe(self):
        """
        Méthode permettant d'afficher le labyrinthe
        :return: Nothing
        """
        fig, ax = plt.subplots()
        #Tracer les murs verticaux
        for i in range(self.murs_v.shape[0]):
            for j in range(self.murs_v.shape[1]):
                if self.murs_v[i, j] == 2 or self.murs_v[i, j] == 1 :
                    ax.plot([j+1,j+1], [self.murs_v.shape[0]-i,self.murs_v.shape[0]-i-1], color='black')
                elif self.murs_v[i, j] == 0 :
                    ax.plot([j+1,j+1], [self.murs_v.shape[0]-i,self.murs_v.shape[0]-i-1], color='white')
        #Tracer les murs horizontaux
        for i in range(self.murs_h.shape[0]):
            for j in range(self.murs_h.shape[1]):
                if self.murs_h[i, j] == 2 or self.murs_h[i, j] == 1 :
                    ax.plot([j,j+1], [self.murs_h.shape[0]-i,self.murs_h.shape[0]-i], color='black')
                elif self.murs_h[i, j] == 0 :
                    ax.plot([j,j+1], [self.murs_h.shape[0]-i,self.murs_h.shape[0]-i], color='white')

        # Tracer le carré autour du labyrinthe
        ax.plot([0, self.murs_h.shape[1]], [self.murs_v.shape[0],self.murs_v.shape[0] ], color='red')  # Bord supérieur
        ax.plot([0, self.murs_h.shape[1]], [0, 0],color='red')  # Bord inférieur
        ax.plot([0, 0], [0, self.murs_v.shape[0]], color='red')  # Bord gauche
        ax.plot([self.murs_h.shape[1], self.murs_h.shape[1]], [0, self.murs_v.shape[0]],color='red')  # Bord droit

        ax.set_aspect('equal')
        ax.axis('off')
        self.figure = fig
        self.ax = ax

    def placer_fourmiliere_aleatoire(self):
        """
        Méthode permettant de placer la fourmillière sur une case du labyrinthe
        :return: La position de la fourmillière
        """
        while True:
            x = np.random.randint(0, self.murs_h.shape[0])  #Choix d'un x au hasard
            y = np.random.randint(0, self.murs_h.shape[1])  #choix d'un y au hasard
            if (self.etat_case[x][y].nourriture == False) :  # Vérifie que ce n'est pas le puit de nourriture
                self.etat_case[x][y].est_fourmilliere()  #Définit la case comme fourmillière
                position = (x,y)
                return position

    def placer_nourriture_aleatoire(self):
        """
        Méthode permettant de placer la nourriture sur une case du labyrinthe
        :return: La position du puit de nourriture
        """
        while True:
            x = np.random.randint(0, self.murs_h.shape[0]) #Choix d'un x au hasard
            y = np.random.randint(0, self.murs_h.shape[1])  #Choix d'un y au hasard
            if (self.etat_case[x][y].fourmilliere == False) :  # Vérifie que ce n'est pas le puit de nourriture
                self.etat_case[x][y].est_nourriture()
                position = (x,y)
                return position

    def afficher_fourmilliere(self,position):
        """
        Méthode permettant l'affichage de la fourmillière
        :param position: La position de la fourmillière
        :return: Nothing
        """
        ax = self.figure.gca()
        x, y = position
        ax.plot(y + 0.5, self.largeur - x - 0.5, 'go', markersize=15)  # cercle vert
        ax.text(y + 0.5, self.largeur - x - 0.5, "F", color="white", ha="center", va="center", fontsize=10, weight="bold")  # lettre F

    def afficher_nourriture(self,position):
        """
        Méthode permettant l'affichage du puit de nourriture
        :param position: La position du puit de nourriture
        :return: Nothing
        """
        ax = self.figure.gca()
        x, y = position
        ax.plot(y + 0.5, self.largeur - x - 0.5, 'ro', markersize=15)  # cercle vert
        ax.text(y + 0.5, self.largeur - x - 0.5, "N", color="white", ha="center", va="center", fontsize=10, weight="bold")  # lettre N

    def afficher_fourmi(self, position):
        x, y = position
        self.ax.plot(y + 0.5, self.largeur - x - 0.5, 'ko', markersize=8)  # 'ko' pour un cercle noir
        self.ax.text(y + 0.5, self.largeur - x - 0.5, "🐜", ha='center', va='center', fontsize=8) #Fourmi

    def afficher_fourmis(self, fourmis):
        for fourmi in fourmis:
            x, y = fourmi.position
            self.ax.plot(y + 0.5, self.largeur - x - 0.5, 'ko', markersize=8)  # 'ko' pour un cercle noir
            self.ax.text(y + 0.5, self.largeur - x - 0.5, "🐜", ha='center', va='center', fontsize=8)  # Fourmi

    def mise_a_jour(frame):
        # Effacer la figure précédente
        labyrinthe.ax.clear()

        # Redessiner le labyrinthe
        labyrinthe.afficher_labyrinthe()

        # Afficher la fourmilière et la nourriture
        labyrinthe.afficher_fourmilliere(sim.position_fourmiliere)
        labyrinthe.afficher_nourriture(sim.puit_nourriture)

        # Mettre à jour les fourmis à chaque tour
        sim.etape()  # Avance d'un tour dans la simulation
        labyrinthe.afficher_fourmis(sim.fourmis)

        plt.title(f"Tour {sim.tour}")  # Affiche le tour en cours
        return labyrinthe.ax


if __name__ == '__main__':
    labyrinthe = Labyrinthe(10, 5)
    labyrinthe.creation_labyrinthe()
    labyrinthe.afficher_labyrinthe()

    sim = Simulation(labyrinthe, 4, 2)

    for i in range (6) : 
        sim.etape()
    
    position_f = sim.position_fourmiliere
    labyrinthe.afficher_fourmilliere(position_f)

    x, y = position_f
    print("Fourmilière à :", position_f)
    print("Est une fourmilière ?", labyrinthe.etat_case[x][y].fourmilliere)

    position_n = sim.puit_nourriture
    labyrinthe.afficher_nourriture(position_n)

    x_n, y_n = position_n
    print("Puit de nourriture à :", position_n)
    print("Est un puit de nourriture ?", labyrinthe.etat_case[x_n][y_n].nourriture)

    x_f,y_f = (3,5)
    labyrinthe.afficher_fourmi((x_f,y_f))

    plt.show()