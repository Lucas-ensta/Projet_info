from abc import ABC, abstractmethod
import fourmi 

class Comportement(ABC):
    """
    classe abstraite permettant de coder les différents comportements possibles d'une fourmi 
    """
    @abstractmethod
    def choisir_direction(self, fourmi, labyrinthe):
        pass

class Exploration(Comportement):
    
    def choisir_direction(self, fourmi, labyrinthe):
        """
        La fourmi choisi le chemin avec le moins de phéromones 
        :param la fourmi, le labyrinthe
        :return: la direction choisi sous forme de str 
        """


        chemins = fourmi.chemins_possible(labyrinthe) #liste des directions possible sous forme de str
        chemin_choisi = []
        
        if len(chemins)== 1 : # il n'ya qu'une direction possible 
            return chemins[0]
        
        else : 
            for c in chemins : 
                i,j = fourmi.conversion_str_int(c) # stock l'indice de la case donné par la direction c
                pheromone = labyrinthe.etat_case.pheromones[i][j] #c'est un dictionnaire avec 2 clés
                val_case = pheromone["attractif"] - pheromone["repulsif"] #on regarde l'attractivité de la case 

                if val_case >= 0 : # on ne garde que les cases attractives 
                    chemin_choisi.append((c, val_case))
            
            if not chemin_choisi : #aucun chemin n'est attractif ou neutre, on créer la meme liste que précédemment sans filtrage 
                for c in chemins : 
                    i,j = fourmi.conversion_str_int(c) 
                    pheromone = labyrinthe.etat_case.pheromones[i][j]
                    chemin_choisi.append((c, pheromone["repulsif"]))

            chemin_choisi_final = min(chemin_choisi, key=lambda x: x[1])[0]  # retourne la direction (str) (on prends le chemin le moins attractif ou le moins répulsif)
                
        return chemin_choisi_final 




class Suivi(Comportement):
    
    def choisir_direction(self, fourmi, labyrinthe):
        """
        La fourmi suit le chemin avec les phéromones la plus attractive pour arriver plus vite à la nourriture 
        :param la fourmi, le labyrinthe 
        :return: la direction choisi sous forme de str
        """
        chemins = fourmi.chemins_possible(labyrinthe) #liste des directions possible sous forme de str
        chemin_choisi = []
        if len(chemins)== 1 : # il n'ya qu'une direction possible 
            return chemins[0]
        else : 
            for c in chemins : 
                i,j = fourmi.conversion_str_int(c)
                pheromone = labyrinthe.etat_case.pheromones[i][j] #c'est un dictionnaire avec 2 clés
                val_case = pheromone["attractif"] - pheromone["repulsif"] #on regarde l'attractivité de la case 

                chemin_choisi.append((c, val_case))
            chemin_final = max(chemin_choisi, key=lambda x: x[1])[0]  # retourne la direction (str) du le chemin le plus attractif)
        return chemin_final 


class Retour(Comportement): 
    pass