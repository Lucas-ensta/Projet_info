from abc import ABC, abstractmethod

import random

from labyrinthe import *

class Comportement(ABC):
    """
    Classe abstraiite permettant de gérer les différents comportements possibles de la fourmi
    """
    @abstractmethod
    def choisir_direction(self,fourmi,labyrinthe):
        pass
    
    @abstractmethod 
    def choisir_pheromone(self, fourmi, labyrinthe):
        pass

class Exploration(Comportement):
    """
    Classe fille de comportement modélisant le comportement d'exploration
    """

    def choisir_direction(self,fourmi,labyrinthe):
        """
        Méthode permettant à la fourmi de choisir le chemin avec le moins de phéromones afin d'explorer le labyrinthe
        :param fourmi : La fourmi
        :param labyrinthe: Le labyrinthe
        :return: La direction choisie sous forme de str
        """
        
        nourriture = fourmi.percevoir_nourriture(labyrinthe) #aller à la nourriture si il y en a 
        for x in nourriture.keys() :
            if nourriture[x] is True :
                
                return x

        chemins = fourmi.chemins_possible(labyrinthe)  # liste des directions possible sous forme de str
        
        
        chemin_choisi = []

        if len(chemins) == 1: # Attention cul-de-sac, passer en mode Retour et déposer une phéromnes repulsive  
            print("cul de sac")
            return chemins[0]


        else:
            for c in chemins:
                i, j = fourmi.conversion_str_int(c)  # stock l'indice de la case donné par la direction c
                pheromone = labyrinthe.etat_case[i][j].pheromones  # c'est un dictionnaire avec 2 clés
                 
                val_case =  pheromone["attractif"] - pheromone["repulsif"]  # on regarde l'attractivité de la case

                if val_case >= 0:  # on ne garde que les cases attractives
                    chemin_choisi.append((c, val_case))

            if not chemin_choisi:  # aucun chemin n'est attractif ou neutre, on créer la meme liste que précédemment sans filtrage
                for c in chemins:
                    i, j = fourmi.conversion_str_int(c)
                    pheromone = labyrinthe.etat_case[i][j].pheromones
                    chemin_choisi.append((c, pheromone["repulsif"]))

            # On récupère la valeur de case minimale 
            min_val = min(chemin_choisi, key=lambda x: x[1])[1]
            # On garde toutes les directions ayant cette valeur
            meilleurs_chemins = [c for c, val in chemin_choisi if val == min_val]
            # On en choisit un au hasard
            chemin_choisi_final = random.choice(meilleurs_chemins)
            
            
        return  chemin_choisi_final
    
    def choisir_pheromone(self, fourmi, labyrinthe):
        """
        Methode permettant à la fourmi de déposer au non des phéromones. Dans le cas Exploration, la fourmi dépose des pheromones attractive +
        ssi elle est sur une case adjacente à la nourriture 
        :param fourmi: La fourmi
        :param labyrinthe: Le labyrinthe
        :return: le type de pherome à déposer 
        """
        chemins = fourmi.chemins_possible(labyrinthe)
        if len(chemins) == 1 : # C'est un cul de sac 
            return "repulsif"
        nourriture = fourmi.percevoir_nourriture(labyrinthe)
        for x in nourriture.keys() :
            if nourriture[x] is not None :
                return "attractif" 



class Suivi(Comportement):
    """
    Classe abstraite permettant de modéliser le comportement de suivi de phéromones attractives
    """

    def choisir_direction(self,fourmi,labyrinthe):
        """
        La fourmi suit le chemin avec les phéromones les plus attractives pour arriver plus vite à la nourriture
        :param fourmi : La fourmi
        :param labyrinthe: Le labyrinthe
        :return: la direction choisie sous forme de str
        """

        nourriture = fourmi.percevoir_nourriture(labyrinthe) #aller à la nourriture si il y en a 
        for x in nourriture.keys() :
            if nourriture[x] is True :
                return x
            
        chemins = fourmi.chemins_possible(labyrinthe)  # liste des directions possible sous forme de str
        chemin_choisi = []
        if len(chemins) == 1:  # il n'ya qu'une direction possible
            return chemins[0]
        else:
            for c in chemins:
                i, j = fourmi.conversion_str_int(c)
                pheromone = labyrinthe.etat_case[i][j].pheromones  # c'est un dictionnaire avec 2 clés
                
                val_case =  pheromone["attractif"] - pheromone["repulsif"]  # on regarde l'attractivité de la case
                chemin_choisi.append((c, val_case))

            # Choix aléatoire parmi les meilleurs chemins (évite l'oscillation)
            max_val = max(chemin_choisi, key=lambda x: x[1])[1]
            meilleurs_chemins = [c for c, val in chemin_choisi if val == max_val]
            choix = random.choice(meilleurs_chemins)
        return choix


    def choisir_pheromone(self, fourmi, labyrinthe):
            """
            Methode permettant à la fourmi de déposer au non des phéromones. Dans le cas Suivi, la fourmi dépose des pheromones attractive +
            ssi elle est sur une case adjacente à la une phéromone attractive 
            :param fourmi: La fourmi
            :param labyrinthe: Le labyrinthe
            :return: le type de pherome à déposer 
            """
            chemins = fourmi.chemins_possible(labyrinthe)
            if len(chemins) == 1 : # C'est un cul de sac 
                return "repulsif"
            pheromone = fourmi.percevoir_pheromones(labyrinthe)
            for x in pheromone.keys() :
                if pheromone[x] > 0 :
                    return "attractif" 

class Retour(Comportement):

    def choisir_direction(self, fourmi, labyrinthe):
        """
        Permet à la fourmi de sortir d'un cul de sac 
        :param fourmi : La fourmi
        :param labyrinthe: Le labyrinthe
        :return: la direction choisie sous forme de str
        """
        chemins = fourmi.chemins_possible(labyrinthe) 
        i, j = fourmi.memoire[0]
        for c in chemins : 
            n, m = fourmi.conversion_str_int(c)
            if (i, j) == (n, m) :
                chemins.remove(c)
        
        if len(chemins) == 1 : #on est toujours dans le cul de sac, on reste en mode retour 
            return chemins[0]
        
        elif len(chemins) > 1 : #On est sorti du cul de sac, repasse en mode exploration 
            return chemins[random.randint(0, len(chemins)-1)]

    def choisir_pheromone(self, fourmi, labyrinthe):
            """
            Methode permettant à la fourmi de déposer au non des phéromones. Dans le cas Retour, la fourmi dépose des pheromones repulsive 
            toutjours
            :param fourmi: La fourmi
            :param labyrinthe: Le labyrinthe
            :return: le type de pherome à déposer 
            """

            return "repulsif"


if __name__ == "__main__":
    lab = Labyrinthe(10, 10)
    lab.creation_labyrinthe()
    lab.afficher_labyrinthe()
    sim = Simulation(lab, 4, 2)

    for _ in range (12):
        sim.etape()
    
    lab.afficher_fourmilliere(sim.position_fourmiliere)
    lab.afficher_nourriture(sim.puit_nourriture)
    print(sim.fourmis)
    lab.afficher_fourmis(sim.fourmis)
    plt.show()




