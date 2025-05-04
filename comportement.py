import random
import labyrinthe  

class Comportement:
    """
    classe abstraite permettant de coder les différents comportements possibles d'une fourmi 
    """
    def choisir_direction(self, fourmi, labyrinthe):
        raise NotImplementedError("Méthode à implémenter dans les sous-classes")

class ComportementExploration(Comportement):
    
    def choisir_direction(self, fourmi, labyrinthe):
        """
        La fourmi choisi le chemin avec le moins de phéromones 
        :param la fourmi, le labyrinthe
        :return: la direction choisi
        """


        chemins = fourmi.chemins_possible(labyrinthe) #liste des directions possible sous forme de str
        chemin_choisi = []
        
        if len(chemins)== 1 : # il n'ya qu'une direction possible 
            return chemins[0]
        
        else : 
            for c in chemins : 
                i,j = fourmi.conversion_str_int(c)[0], fourmi.conversion_str_int(c)[1] # stock l'indice de la case donné par la direction c
                pheromone = labyrinthe.etat_case.pheromones[i][j] #c'est un dictionnaire avec 2 clés
                val_case = pheromone["attractif"] - pheromone["repulsif"] #on regarde l'attractivité de la case 

                if val_case >= 0 : # on ne garde que les cases attractives 
                    chemin_choisi.append((c, val_case))
            
            if not chemin_choisi : #aucun chemin n'est attractif ou neutre, on créer la meme liste que précédemment sans filtrage 
                for c in chemins : 
                    i,j = fourmi.conversion_str_int(c)[0], fourmi.conversion_str_int(c)[1] 
                    pheromone = labyrinthe.etat_case.pheromones[i][j]
                    chemin_choisi.append((c, pheromone["repulsif"]))

            chemin_choisi_final = min(chemin_choisi, key=lambda x: x[1])[0]  # retourne la direction (str) (on prends le chemin le moins attractif ou le moins répulsif)
                
        return chemin_choisi_final 



         
            

      
            


class ComportementSuivi(Comportement):
    """
    La fourmi suit le chemin avec la phéromone la plus attractive
    """
    def se_deplacer(self, fourmi, labyrinthe):
        pass

class ComportementRetour(Comportement): 
    pass