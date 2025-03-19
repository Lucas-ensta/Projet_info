"""Projet info : 
1. Périmètre du sujet : 

- Une classe Labyrinthe qui contient : 
Méthodes de la classe : 
- créer le labyrinthe (entrée : cases, mur verticaux, mur horizontaux)
- afficher le labyrinthe 
- Une classe fille nommée Case : 
- ajouter et gérer les phéromones
interagit avec les fourmis


- Une classe Simulation :
- un fonction fourmilière qui génère une fourni périodiquement 
- créer une case « puit de nourriture »
- créer une fonction qui simule 1 étape : 
-faire diminuer les phéromones,
- stocker les nouvelles phéromones déposées  
- gérer la fourmilière (faire apparaitre une nouvelle fourmi tous les n tour, -- faire déplacer chaque fourmi du labyrinthe 
- faire disparaitre si elle atteint la nourriture 
- faire fusionner les fourmis sur la même case



- Une classe Fourmi : 
Méthodes :
-	 Une fonction qui renvoie les chemins possibles en fonction des murs autour de la fourmi : nom :  … 
-	 Une fonction qui renvoie les cases autour d’elle sur lesquels il y a des phéromones, et le type de phéromone : nom : …
-	Une fonction qui renvoie les cases autour d’elle sur lesquels il y a de la nourriture autour si pas de mur, nom :  …
-	Une fonction qui dépose un des 2 types de phéromones sur sa case, 
-	Une fonction permettant de se déplacer d'une case, 
-	Une fonction cerveau permettant de se souvenir de la case qu'elle vient de visiter, 
-	Une fonction qui décide du comportement à adopter 

Une classe fille de Fourmi qui est son Comportement :
  	Méthode : 
        - mode exploration 
    	- mode suivi de chemin
        - mode retour de cul de sac 

"""

import numpy as np 

class Labyrinthe (): 
    """
    Classe qui permet de générer le labyrinthe
    """
    def __init__(self, longueur, largeur):
        self.cases = np.arange(longueur * largeur).reshape(largeur, longueur)
        self.mur_v = np.ones((largeur, longueur-1))
        self.mur_h = np.ones((largeur-1, longueur))

    def creation_lab (self) : 
        murs_retires = 0 
        while murs_retires < (self.longueur * self.largeur - 1) :
            a = np.random.randint(0,2)
            if a == 0 : #On chosit un mur horizontal
                x = np.random.randint(0,self.largeur) #prends un entier aléatoir entre 0 et largeur-1
                y = np.random.randint(0,self.longueur + 1) # ATTTENTION AUX BORNES 
                if self.murs_h[x,y] == 2 : #Si le mur est déjà défintif, on passe
                    pass
                #On compare les cases du dessu et du dessous
                elif self.cases[x,y] == self.cases[x+1,y] : #Les valeurs sont égales, le mur devient définitif
                    self.murs_h[x,y] = 2
                elif self.cases[x,y] > self.cases[x+1,y] : #La valeur du dessus est plus élevée, on la remplace
                    self.cases[x,y] = self.cases[x+1,y]
                    self.murs_h[x,y] = 0 #Le mur ne peut plus être choise
                    murs_retires += 1
                else : #La valeur du dessous est plus grande, on la remplace
                    self.cases[x,y+1] = self.cases[x,y]
                    murs_retires += 1
            else :
                x = np.random.randint(0, self.largeur)
                y = np.random.randint(0, self.longueur-1)
                if self.murs_v[x, y] == 2:  # Si le mur est déjà défintif, on passe
                    pass
                # On compare les cases de gauche et de droite
                elif self.cases[x, y] == self.cases[x,y+1]:  # Les valeurs sont égales, le mur devient définitif
                    self.murs_v[x, y] = 2
                elif self.cases[x, y] > self.cases[x,y+1]:  # La valeur de gauche est plus élevée, on la remplace
                    self.cases[x, y] = self.cases[x,y+1]
                    self.murs_v[x, y] = 0  # Le mur ne peut plus être choisi
                    murs_retires += 1
                else : #La valeur de droite est plus élevée, on la remplace
                    self.cases[x, y + 1] = self.cases[x, y]
                    murs_retires += 1
        return self.mur_h, self.mur_v
    

    
         
         
    



        


        
        



if __name__ == "__main__" : 
    
    print (np.random.randint(0,2))
    # Notre simulation 

