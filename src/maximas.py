from typing_extensions import Self
from PyQt5.QtWidgets import QLabel,QLineEdit,QWidget,QPushButton,QHBoxLayout



class MaximasManager(QWidget):

    def __init__(self:Self):
        super().__init__()
        self.UI()

    def UI(self:Self):
        
        self.h_maxima = 0.2

        self.hlayout_maxima = QHBoxLayout()
        
        self.label_maxima = QLabel("Choisir votre H")
        self.lineedit_maxima = QLineEdit()
        self.lineedit_maxima.setText(str(self.h_maxima))

        self.button_maxima = QPushButton("Afficher") 

        self.hlayout_maxima.addWidget(self.label_maxima)
        self.hlayout_maxima.addWidget(self.lineedit_maxima)
        self.hlayout_maxima.addWidget(self.button_maxima) 

        self.setLayout(self.hlayout_maxima)