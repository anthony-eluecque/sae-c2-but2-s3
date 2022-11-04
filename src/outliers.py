from typing_extensions import Self
from PyQt5.QtWidgets import QLabel,QLineEdit,QWidget,QPushButton,QHBoxLayout


class OutliersManager(QWidget):

    def __init__(self:Self):
        super().__init__()
        self.UI()

    def UI(self:Self):

        self.sigma = 2.85

        self.hlayout_outliers = QHBoxLayout()

        self.label_outliers = QLabel("Choisir votre Sigma (Par défault 2.85)")
        self.lineedit_outliers = QLineEdit("2.85")
        self.button_outliers = QPushButton("Détecter les valeurs aberrantes")

        self.hlayout_outliers.addWidget(self.label_outliers)
        self.hlayout_outliers.addWidget(self.lineedit_outliers)
        self.hlayout_outliers.addWidget(self.button_outliers)

        self.setLayout(self.hlayout_outliers)