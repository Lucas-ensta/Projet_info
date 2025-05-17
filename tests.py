import unittest
import numpy as np
from unittest.mock import MagicMock

from comportement import Exploration, Suivi, Retour
from labyrinthe import Labyrinthe
from simulation import Simulation
from case import Case
from fourmi import Fourmi


# class TestLabyrinthe(unittest.TestCase):
#     """
#     Classe permettant de tester certaines méthodes de la classe Labyrinthe
#     """

#     def test_dimensions_labyrinthe(self):
#         """
#         Méthode permettant de tester les dimensions du labyrinthe généré ainsi que la taille des matrices murs
#         :return: Nothing
#         """
#         tailles = [(5, 5), (10, 15), (1, 20), (20, 1)]
#         for longueur_attendue, largeur_attendue in tailles:
#             with self.subTest(longueur=longueur_attendue, largeur=largeur_attendue):  #pouvoir tester différents cas, même si l'un échoue
#                 lab = Labyrinthe(longueur_attendue, largeur_attendue)

#                 # Vérifie les attributs de dimensions du labyrinthe
#                 self.assertEqual(lab.longueur, longueur_attendue)
#                 self.assertEqual(lab.largeur, largeur_attendue)

#                 # Vérifie la taille des matrices de murs
#                 self.assertEqual(lab.murs_h.shape, (largeur_attendue - 1, longueur_attendue))
#                 self.assertEqual(lab.murs_v.shape, (largeur_attendue, longueur_attendue - 1))

#     def test_etat_case_instances(self):
#         """
#         Méthode permettant de vérifier que les objets instanciées sont bien des instances de Cases
#         :return: Nothing
#         """
#         lab1 = Labyrinthe(10, 5)
#         lab2 = Labyrinthe(2, 7)
#         for element in lab1.etat_case:
#             for case in element:
#                 self.assertIsInstance(case, Case)
#         for element in lab2.etat_case:
#             for case in element:
#                 self.assertIsInstance(case, Case)



# class TestSimulation(unittest.TestCase):
#     """
#     Classe permettant de tester certaines méthodes de la classe Labyrinthe
#     """

#     def test_fourmiliere_et_puit_positions_differentes(self):
#         """
#         Méthode permettant de s'assurer que le puit de nourriture et la fourmillière ne sont pas sur la même case
#         :return: Nothing
#         """
#         tailles = [(5, 5), (10, 15), (20, 10), (3, 4)]
#         for longueur, largeur in tailles:
#             with self.subTest(longueur=longueur, largeur=largeur):
#                 sim = Simulation(Labyrinthe(longueur,largeur),1)
#                 self.assertNotEqual(sim.position_fourmiliere,sim.puit_nourriture,"La fourmilière et le puits de nourriture doivent être à des positions différentes.")

#     def test_generer_fourmi_au_tour_multiple(self):
#         """
#         méthode permettant de tester la bonne apparition de fourmi lorsque le tour est un multiple de la fréquence d'apparition
#         :return: Nothing
#         """
#         # Initialisation d'une instance de Simulation avec un labyrinthe simulé
#         self.simulation = Simulation(Labyrinthe(10, 7), nb_iterations=10, freq_apparition=3)
#         self.simulation.fourmis = []
#         self.simulation.tour = 6  # 6 est un multiple de 3
#         self.simulation.generer_fourmi() #On appelle la fonction à tester
#         self.assertEqual(len(self.simulation.fourmis), 1) #Vérifier qu'il y a une fourmi
#         fourmi = self.simulation.fourmis[0]
#         self.assertEqual(fourmi.position, self.simulation.position_fourmiliere) #Vérifier qu'elle est à la même position que la fourmillière
#         self.assertIsInstance(fourmi.comportement, Exploration) #vérifier son bon comportement par défaut exploration

#     def test_generer_fourmi_hors_multiple(self):
#         # Initialisation d'une instance de Simulation avec un labyrinthe simulé
#         self.simulation = Simulation(Labyrinthe(10, 7), nb_iterations=10, freq_apparition=3)
#         self.simulation.fourmis = []
#         self.simulation.tour = 5  # 5 n'est pas un multiple de 3
#         self.simulation.generer_fourmi()  # On appelle la fonction à tester
#         self.assertEqual(len(self.simulation.fourmis), 0) #On vérifie qu'aucune fourmi n'est apparu


# class Test_Case(unittest.TestCase):
#     """
#     Classe permettant de tester certaines méthodes de la classe Case
#     """

#     def setUp(self):
#         """
#         instanciation de 2 classes avant chaque test
#         :return: Nothing
#         """
#         self.case1 = Case((2, 3))
#         self.case2 = Case((5,7))

#     def test_ajouter_pheromone(self):
#         """
#         Méthode permettant de tester la bonne augmentation des phéromones
#         :return: Nothing
#         """
#         self.case1.ajouter_pheromone("attractif", 5)
#         self.case2.ajouter_pheromone("attractif", 7)
#         self.assertEqual(self.case1.pheromones["attractif"], 5)
#         self.assertEqual(self.case2.pheromones["attractif"], 7)

#     def test_ajouter_nouvelle_pheromone(self):
#         """
#         Méthode permettant de tester que de nouvelles variétés de phéromones ne puevnt pas être ajouter
#         :return: Nothing
#         """
#         with self.assertRaises(ValueError):
#             self.case1.ajouter_pheromone("neutre", 3)
#             self.case2.ajouter_pheromone("neutre", 6)

#     def test_attenuer_pheromone(self):
#         """
#         Méthode vérifiant la bonne aténuation des phéromones
#         :return: Nothing
#         """
#         self.case1.ajouter_pheromone("attractif", 10)
#         self.case1.attenuer_pheromone(0.3)
#         self.case2.ajouter_pheromone("attractif", 15)
#         self.case2.attenuer_pheromone(0.3)
#         self.assertAlmostEqual(self.case1.pheromones["attractif"], 7.0)
#         self.assertAlmostEqual(self.case2.pheromones["attractif"], 10.5)

#     def test_contient_nourriture(self):
#         self.assertFalse(self.case1.contient_nourriture())
#         self.assertFalse(self.case2.contient_nourriture())
#         self.case1.est_nourriture()
#         self.case2.est_nourriture()
#         self.assertTrue(self.case1.contient_nourriture())
#         self.assertTrue(self.case2.contient_nourriture())


# class TestFourmi(unittest.TestCase):
#     """
#     Classe permettant de tester certaines méthodes de la classe Fourmi
#     """
#     def setUp(self):
#         # Initialisation d'un labyrinthe 3x3
#         self.labyrinthe1 = Labyrinthe(3, 3)
#         self.labyrinthe1.murs_h = np.zeros((3-1, 3), dtype=int)
#         self.labyrinthe1.murs_v = np.zeros((3, 3-1), dtype=int)
#         # Initialisation d'un labyrinthe 6x4
#         self.labyrinthe2 = Labyrinthe(6,4)
#         self.labyrinthe2.murs_h = np.zeros((6-1, 4), dtype=int)
#         self.labyrinthe2.murs_v = np.zeros((4, 6-1), dtype=int)
#         self.fourmi = Fourmi(position=(1, 1), comportement=Exploration())
#         self.fourmi_bis = Fourmi(position=(5, 5), comportement=Exploration())


#     def test_chemins_possible_avec_murs(self):
#         # Ajout de murs
#         self.labyrinthe1.murs_h[0,1] = 1  # Mur au-dessus de la case (1, 1)
#         self.labyrinthe1.murs_v[1, 1] = 1  # Mur à droite de la case (1, 1)
#         self.fourmi = Fourmi(position=(1, 1), comportement=Exploration())
#         # Appel de la méthode
#         result1 = self.fourmi.chemins_possible(self.labyrinthe1)
#         # Vérification que certaines directions ne sont plus possibles
#         self.assertNotIn("haut", result1)
#         self.assertIn("gauche", result1)
#         self.assertIn("bas", result1)
#         self.assertNotIn("droite", result1)

#         # Ajout de murs
#         self.labyrinthe2.murs_h[2, 2] = 1  # Mur en-dessous de la case
#         self.labyrinthe2.murs_v[2, 1] = 1  # Mur à gauche de la case
#         self.fourmi = Fourmi(position=(2, 2), comportement=Exploration())
#         # Appel de la méthode
#         result2 = self.fourmi.chemins_possible(self.labyrinthe2)
#         # Vérification que certaines directions ne sont plus possibles
#         self.assertIn("haut", result2)
#         self.assertNotIn("gauche", result2)
#         self.assertNotIn("bas", result2)
#         self.assertIn("droite", result2)

#     def test_haut(self):
#         """
#         Méthode pour tester la direction haute
#         :return: Nothing
#         """
#         self.assertEqual(self.fourmi_bis.conversion_str_int("haut"), (4, 5))
#         self.assertEqual(self.fourmi.conversion_str_int("haut"),(0,1))

#     def test_bas(self):
#         """
#         Méthode pour tester la direction bas
#         :return: Nothing
#         """
#         self.assertEqual(self.fourmi_bis.conversion_str_int("bas"), (6, 5))
#         self.assertEqual(self.fourmi.conversion_str_int("bas"),(2,1))

#     def test_gauche(self):
#         """
#         Méthode pour tester la direction gauche
#         :return: Nothing
#         """
#         self.assertEqual(self.fourmi_bis.conversion_str_int("gauche"), (5, 4))
#         self.assertEqual(self.fourmi.conversion_str_int("gauche"),(1,0))

#     def test_droite(self):
#         """
#         Méthode pour tester la direction droite
#         :return: Nothing
#         """
#         self.assertEqual(self.fourmi_bis.conversion_str_int("droite"), (5, 6))
#         self.assertEqual(self.fourmi.conversion_str_int("droite"),(1,2))

    


class TestComportement(unittest.TestCase):

    def setUp(self):
        """
        Méthode appelée avant chaque test.
        On crée des objets MagicMock pour simuler la fourmi et le labyrinthe,
        sans dépendre de l'implémentation réelle du labyrinthe.
        """
        self.labyrinthe = MagicMock()  # Mock du labyrinthe (instance fictive du labyrinthe juste pour le test)
        self.fourmi = MagicMock()      # Mock de la fourmi (idem)
        self.fourmi.position = (1, 1)  # Position de la fourmi au centre d'une grille 3x3
        
        # On simule la méthode conversion_str_int de la fourmi,
        # qui convertit une direction en coordonnées dans la grille.
        # Exemple: "haut" correspond à la case (0, 1), "bas" à (2, 1)
        self.fourmi.conversion_str_int.side_effect = lambda d: {
            "haut": (0, 1),
            "bas": (2, 1),
        }[d]

# ============= classe Exploration ================ #

    def test_exploration_choisir_direction(self):
        """
        Test de la méthode choisir_direction de la classe Exploration.
        On vérifie que la fourmi choisit le chemin avec le moins de phéromones attractives.
        """
        # Simulation : la fourmi ne perçoit pas de nourriture autour
        self.fourmi.percevoir_nourriture.return_value = {"haut": None, "bas": None}
        
        # Simulation : la fourmi peut aller soit en "haut", soit en "bas"
        self.fourmi.chemins_possible.return_value = ["haut", "bas"]
        
        # On simule les phéromones sur les cases adjacentes dans le labyrinthe
        # La case (0,1) a 1 phéromone attractive, (2,1) en a 4
        self.labyrinthe.etat_case = {
            0: {
                1: MagicMock(pheromones={"attractif": 1, "repulsif": 0})
            },
            2: {
                1: MagicMock(pheromones={"attractif": 4, "repulsif": 0})
            }
        }
        
        comportement = Exploration()
        direction = comportement.choisir_direction(self.fourmi, self.labyrinthe)
        
        # On attend que la fourmi choisisse "haut" (case avec moins de phéromones attractives)
        self.assertEqual(direction, "haut")

    def test_exploration_choisir_pheromone(self):
        """
        Test de la méthode choisir_pheromone de la classe Exploration.
        La fourmi doit déposer une phéromone attractive si elle est proche de la nourriture.
        """
        # Simulation : chemins possibles
        self.fourmi.chemins_possible.return_value = ["haut", "bas"]
        
        # Simulation : la fourmi perçoit de la nourriture en "haut"
        self.fourmi.percevoir_nourriture.return_value = {"haut": True, "bas": None}
        
        comportement = Exploration()
        pheromone = comportement.choisir_pheromone(self.fourmi, self.labyrinthe)
        
        # La fourmi doit déposer une phéromone attractive
        self.assertEqual(pheromone, "attractif")


# ============= classe Suivi ================ #

    def test_suivi_choisir_direction(self):
        """
        Test de la méthode choisir_direction de la classe Suivi.
        La fourmi doit suivre la case avec le plus de phéromones attractives
        ou vers la nourriture si elle est détectée.
        """
        # Pas de nourriture perçue autour
        self.fourmi.percevoir_nourriture.return_value = {"haut": None, "bas": None}
        
        # Chemins possibles
        self.fourmi.chemins_possible.return_value = ["haut", "bas"]
        
        # Conversion direction -> coordonnées
        self.fourmi.conversion_str_int.side_effect = lambda d: {
            "haut": (0, 1),
            "bas": (2, 1),
        }[d]
        
        # On simule les cases dans le labyrinthe avec phéromones et nourriture
        self.labyrinthe.etat_case = {
            0: {
                1: MagicMock(pheromones={"attractif": 2, "repulsif": 0}, nourriture=False)
            },
            2: {
                1: MagicMock(pheromones={"attractif": 5, "repulsif": 0}, nourriture=True)
            }
        }
        
        comportement = Suivi()
        direction = comportement.choisir_direction(self.fourmi, self.labyrinthe)
        
        # La fourmi doit choisir "bas" car il y a de la nourriture à cet endroit
        self.assertEqual(direction, "bas")

# ============= classe Retour ================ #

    def test_retour_choisir_pheromone(self):
        """
        Test de la méthode choisir_pheromone de la classe Retour.
        La fourmi doit toujours déposer une phéromone répulsive en mode Retour.
        """
        # On force le comportement actuel de la fourmi à Retour
        self.fourmi.comportement = Retour()
        
        comportement = Retour()
        pheromone = comportement.choisir_pheromone(self.fourmi, self.labyrinthe)
        
        # La fourmi doit déposer une phéromone répulsive en mode Retour
        self.assertEqual(pheromone, "repulsif")

if __name__ == '__main__':
    unittest.main()