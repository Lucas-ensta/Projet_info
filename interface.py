import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QHBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPen, QFont
from PyQt5.QtCore import Qt, QTimer
from memento import Memento

class LabyrintheWidget(QWidget):
    """
    Classe permettant de générer l'affichage du labyritnhe sur la fenêtre graphique
    """
    def __init__(self, labyrinthe, simulation, cell_size=40):
        super().__init__()
        self.lab = labyrinthe
        self.sim = simulation
        self.cell_size = cell_size
        self.saved_state = None  # Memento sauvegardé
        self.margin = 20
        self.setMinimumSize(self.lab.murs_h.shape[1]*cell_size + 2*self.margin,
                            self.lab.murs_v.shape[0]*cell_size + 2*self.margin)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w_cells = self.lab.murs_h.shape[1]
        h_cells = self.lab.murs_v.shape[0]

        # Fond blanc
        painter.fillRect(self.rect(), QColor(255, 255, 255))

        #coloriage cases
        
        for i in range(h_cells):
            for j in range(w_cells):
                pheromones = self.lab.etat_case[i][j].pheromones
                color = self.pheromone_to_color(pheromones["attractif"], pheromones["repulsif"])

                x = self.margin + j * self.cell_size
                y = self.margin + i * self.cell_size
                painter.fillRect(x, y, self.cell_size, self.cell_size, color)


        # Dessiner murs verticaux
        pen_black = QPen(Qt.black, 3)
        pen_red = QPen(Qt.red, 3)
        painter.setPen(pen_black)
        for i in range(self.lab.murs_v.shape[0]):
            for j in range(self.lab.murs_v.shape[1]):
                if self.lab.murs_v[i, j] in (1, 2):
                    x = self.margin + (j+1) * self.cell_size
                    y1 = self.margin + i * self.cell_size
                    y2 = y1 + self.cell_size
                    painter.drawLine(x , y1, x , y2)

        # Dessiner murs horizontaux
        for i in range(self.lab.murs_h.shape[0]):
            for j in range(self.lab.murs_h.shape[1]):
                if self.lab.murs_h[i, j] in (1, 2):
                    x1 = self.margin + j * self.cell_size
                    x2 = x1 + self.cell_size
                    y = self.margin + (i+1) * self.cell_size
                    painter.drawLine(x1 , y, x2 , y)

        # Dessiner bordures rouges
        painter.setPen(pen_red)
        # bord supérieur
        painter.drawLine(self.margin, self.margin,
                         self.margin + w_cells * self.cell_size, self.margin)
        # bord inférieur
        painter.drawLine(self.margin, self.margin + h_cells * self.cell_size,
                         self.margin + w_cells * self.cell_size, self.margin + h_cells * self.cell_size)
        # bord gauche
        painter.drawLine(self.margin, self.margin,
                         self.margin, self.margin + h_cells * self.cell_size)
        # bord droit
        painter.drawLine(self.margin + w_cells * self.cell_size, self.margin,
                         self.margin + w_cells * self.cell_size, self.margin + h_cells * self.cell_size)

        # Afficher fourmilière (vert)
        fx, fy = self.sim.position_fourmiliere
        self.draw_cell(painter, fx, fy, QColor(0, 180, 0), label='F')

        # Afficher nourriture (rouge)
        nx, ny = self.sim.puit_nourriture
        self.draw_cell(painter, nx, ny, QColor(180, 0, 0), label='N')

        # Afficher fourmis (jaune) avec numéros
        rect_size = 40
        painter.setBrush(Qt.yellow)
        for index, fourmi in enumerate(self.sim.fourmis):
            x, y = fourmi.position
            # Calculer le centre de la cellule
            center_x = self.margin + (y + 0.5) * self.cell_size
            center_y = self.margin + (x + 0.5) * self.cell_size
            # Dessiner la fourmi centrée
            painter.drawEllipse(
                int(center_x - rect_size / 2 + rect_size * 0.15),
                int(center_y - rect_size / 2 + rect_size * 0.15),
                int(rect_size * 0.7),
                int(rect_size * 0.7)
            )
            # Afficher le numéro de la fourmi
            painter.setPen(Qt.black)
            font = QFont('Arial', 10, QFont.Bold)
            painter.setFont(font)
            painter.drawText(
                int(center_x - rect_size / 4),  # Position X du texte
                int(center_y + rect_size / 4),  # Position Y du texte
                str(index + 1)  # Numéro de la fourmi
            )

    def draw_cell(self, painter, i, j, color, label=None, font_size=14):
        x = self.margin + j * self.cell_size
        y = self.margin + i * self.cell_size
        rect_size = self.cell_size

        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(int(x + rect_size * 0.15), int(y + rect_size * 0.15),
                            int(rect_size * 0.7), int(rect_size * 0.7))

        if label:
            painter.setPen(Qt.black)
            font = QFont('Arial', font_size, QFont.Bold)
            painter.setFont(font)
            painter.drawText(x, y, rect_size, rect_size,
                             Qt.AlignCenter, label)
            
            ### Vusualisation phéromones###
            
    def pheromone_to_color(self, attractif, repulsif):
        val_diff = max(-1, min(1, attractif - repulsif))

        if val_diff <= 0:
            red = 255
            green = int(255 * (val_diff + 1))  # 0 to 255
        else:
            red = int(255 * (1 - val_diff))   # 255 to 0
            green = 255

        return QColor(red, green, 0)


class MainWindow(QWidget):
    def __init__(self, labyrinthe, simulation, cell_size=40, vitesse=500):
        super().__init__()
        self.lab = labyrinthe
        self.sim = simulation
        self.cell_size = cell_size
        self.vitesse = vitesse
        self.saved_state = None  # Memento sauvegardé

        self.setWindowTitle("Simulation Fourmis - Labyrinthe")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.lab_widget = LabyrintheWidget(self.lab, self.sim, cell_size=self.cell_size)
        self.layout.addWidget(self.lab_widget)

        # Ligne de boutons
        btn_layout = QHBoxLayout()

        # Démarrer
        self.start_btn = QPushButton("Démarrer Simulation")
        self.start_btn.clicked.connect(self.start_simulation)
        btn_layout.addWidget(self.start_btn)

        # Pause/Reprise
        self.pause_btn = QPushButton("Pause")
        self.pause_btn.setEnabled(False)
        self.pause_btn.clicked.connect(self.toggle_pause)
        btn_layout.addWidget(self.pause_btn)

        # Étape par étape
        self.step_btn = QPushButton("Étape Suivante")
        self.step_btn.clicked.connect(self.step_simulation)
        btn_layout.addWidget(self.step_btn)

        # Sauvegarde
        self.save_btn = QPushButton("Sauvegarder État")
        self.save_btn.clicked.connect(self.save_state)
        btn_layout.addWidget(self.save_btn)

        # Restauration
        self.restore_btn = QPushButton("Restaurer État")
        self.restore_btn.clicked.connect(self.restore_state)
        btn_layout.addWidget(self.restore_btn)

        self.layout.addLayout(btn_layout)

        # Statut
        self.status_label = QLabel("Appuyez sur Démarrer ou Étape Suivante")
        self.layout.addWidget(self.status_label)

        self.timer = QTimer()
        self.timer.timeout.connect(self.step_simulation)
        self.simulation_en_cours = False

    def start_simulation(self):
        self.status_label.setText("Simulation en cours...")
        self.timer.start(self.vitesse)
        self.simulation_en_cours = True
        self.pause_btn.setEnabled(True)

    def toggle_pause(self):
        if self.simulation_en_cours:
            self.timer.stop()
            self.simulation_en_cours = False
            self.pause_btn.setText("Reprendre")
            self.status_label.setText("Simulation en pause")
        else:
            self.timer.start(self.vitesse)
            self.simulation_en_cours = True
            self.pause_btn.setText("Pause")
            self.status_label.setText("Simulation en cours...")

    def step_simulation(self):
        self.sim.etape()
        self.lab_widget.update()
        if len(self.sim.fourmis) == 0:
            self.timer.stop()
            self.status_label.setText("Simulation terminée")

    def save_state(self):
        self.saved_state = self.sim.sauvegarder_etat()
        self.status_label.setText("État sauvegardé")

    def restore_state(self):
        if self.saved_state:
            self.sim.restaurer_etat(self.saved_state)
            self.lab_widget.update()
            self.status_label.setText(f"État restauré au tour {self.sim.tour}")
        else:
            self.status_label.setText("Aucune sauvegarde trouvée")


if __name__ == "__main__":
    from labyrinthe import Labyrinthe
    from simulation import Simulation

    app = QApplication(sys.argv)

    lab = Labyrinthe(15, 12)
    lab.creation_labyrinthe()

    sim = Simulation(lab, 20, 30)
    pos_fourmilliere = sim.position_fourmiliere
    pos_nourriture = sim.puit_nourriture

    window = MainWindow(lab, sim)
    window.show()

    sys.exit(app.exec_())