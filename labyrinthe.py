import numpy as np 
import matplotlib.pyplot as plt 

class Labyrinthe :
    """
    Classe permettant de générer et d'afficher le labyrinthe
    """

    def __init__(self,longueur,largeur):
        """
        :param longueur: nombre de colonnes des matrices
        :param largeur: nombre de lignes des matrices
        """
        self.longueur = longueur
        self.largeur = largeur
        self.cases = np.arange(longueur*largeur).reshape(largeur,longueur)
        self.murs_v = np.ones((largeur,longueur-1),dtype=int)
        self.murs_h = np.ones((largeur-1,longueur),dtype=int)

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
                    print(self.cases)

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
                    print(self.cases)
        print("La grille des murs verticaux est", self.murs_v,self.murs_v.shape[0],self.murs_v.shape[1])
        print("La grille des murs horizontaux est", self.murs_h,self.murs_h.shape[0],self.murs_h.shape[1])

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
        plt.show()

if __name__ == "__main__":
    pass
    # lab = Labyrinthe(10, 15)
    # lab.creation_labyrinthe()
    # lab.afficher_labyrinthe()
