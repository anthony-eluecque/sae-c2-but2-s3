from typing_extensions import Self
from PyQt5.QtWidgets import QLabel,QLineEdit, QWidget,QPushButton,QHBoxLayout


class IntensityManager(QWidget):


    def __init__(self:Self):
        super().__init__()
        self.UI()

    def UI(self:Self):

        self.hlayout_intensity = QHBoxLayout()

        self.label_imin = QLabel("Intensité Minimale :")
        self.lineedit_imin = QLineEdit()
        
        self.label_imax = QLabel("Intensité Maximale :")
        self.lineedit_imax = QLineEdit()

        self.new_intensity = QPushButton("Afficher") 

        self.hlayout_intensity.addWidget(self.label_imin)
        self.hlayout_intensity.addWidget(self.lineedit_imin)
        self.hlayout_intensity.addWidget(self.label_imax)
        self.hlayout_intensity.addWidget(self.lineedit_imax)
        self.hlayout_intensity.addWidget(self.new_intensity)

        self.setLayout(self.hlayout_intensity)