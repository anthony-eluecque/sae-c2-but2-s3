from typing_extensions import Self

from PyQt5.QtWidgets import QLabel,QLineEdit,QVBoxLayout, QWidget,QPushButton,QHBoxLayout
import numpy as np
from canvasImage import CanvasImage

class StatistiquesManager(QWidget):


    def __init__(self:Self,image):
        super().__init__()
        self.UI(image)


    def UI(self:Self,image):

        self.statistiques = CanvasImage()
        self.statistiques.drawHistogram(image)
    
        self.layout_stats = QHBoxLayout()
        self.display_stats = QVBoxLayout()

        self.label_taille_image = QLabel("Taille de l'image :"+str(image.shape))

        self.label_vmin = QLabel("Vmin :")
        self.lineedit_vmin = QLineEdit()
        self.lineedit_vmin.setText(str(np.amin(image)))
        
        self.label_vmax = QLabel("Vmax :")
        self.lineedit_vmax = QLineEdit()
        self.lineedit_vmax.setText(str(np.amax(image)))

        self.new_vm = QPushButton("Afficher")     

        self.layout_stats.addWidget(self.label_taille_image)

        self.layout_stats.addWidget(self.label_vmin)
        self.layout_stats.addWidget(self.lineedit_vmin)

        self.layout_stats.addWidget(self.label_vmax)
        self.layout_stats.addWidget(self.lineedit_vmax)

        self.layout_stats.addWidget(self.new_vm)

        self.display_stats.addLayout(self.layout_stats)
        self.display_stats.addWidget(self.statistiques)


        self.setLayout(self.display_stats)
    