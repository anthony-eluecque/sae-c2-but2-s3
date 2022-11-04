import sys
from typing_extensions import Self

from PyQt5.QtWidgets import QFileDialog,QMainWindow,QVBoxLayout, QGridLayout,QWidget,QPushButton,QHBoxLayout,QComboBox,QApplication

import numpy as np
from PIL import Image

from folders import Folders
from canvasImage import CanvasImage
from intensity import IntensityManager
from statistiques import StatistiquesManager
from maximas import MaximasManager
from outliers import OutliersManager
from stacking import StackingManager


# ---------------------------------------------------------------------------- #
#                      ELUECQUE Anthony | Dournel Fréderic                     #
#                               SAE C2 S3 BUT2                                 #
#                            Octobre-Novembre 2022                             #
# ---------------------------------------------------------------------------- #


class MainWindow(QMainWindow):

    def __init__(self:Self):

        super(MainWindow, self).__init__()
        self.main = QWidget()
        self.grid = QGridLayout(self.main)
        self.setCentralWidget(self.main)
        self.main.setMinimumWidth(1200)
        self.main.setMinimumHeight(650)
        self.UI()
        self.show()

    def UI(self:Self):
        
        self.folders = Folders()
        self.folders.signalDisplayImage.connect(self.displayData)
        self.grid.addWidget(self.folders,0,0)

    def displayData(self:Self,liste_image:list[list[int]]):

        self.save_button = QPushButton("Enregistrer en PNG")
        self.save_button.clicked.connect(self.saveImageAsPng)

        self.liste_images = [] # numpy array only
        self.data_images = liste_image # All data from images
        for i in range(len(liste_image)):
            self.liste_images.append(liste_image[i][0].data)

        self.vlayout_right = QVBoxLayout()
        self.hlayout_right = QHBoxLayout()

        # -------------------------------------- #
        #           Stacking Manager             #
        # -------------------------------------- #

        self.stacking = StackingManager(self.liste_images)
        

        # ------------------------------------------------ #
        #  Image de Gauche ("Basique") => Par défault la 0 #
        # ------------------------------------------------ #
        self.left_image = CanvasImage()
        self.left_image.drawImage(self.liste_images[0],
                                np.amin(self.liste_images[0]),
                                np.amax(self.liste_images[0])
                                )
        
        # -------------------------------------- #
        #   Image de Droite (Traitement dessus)  #
        # -------------------------------------- #
        self.right_image = CanvasImage()

        # -------------------------------------- #
        #           Image Statistique            #
        # -------------------------------------- #

        self.stats = StatistiquesManager(self.liste_images[0])
        self.stats.new_vm.clicked.connect(self.coloration_image)

        # -------------------------------------- #
        #               Box Stacking             #
        # -------------------------------------- #

        self.box : QComboBox = QComboBox()
        self.box.addItems(["Méthode Stacking","Moyenne","Mediane"])
        self.box.setCurrentText("Méthode Stacking")
        self.box.currentIndexChanged.connect(self.onChanged)  

        # -------------------------------------- #
        #               Box Filtre               #
        # -------------------------------------- #

        self.filtre : QComboBox = QComboBox()
        self.filtre.addItems(["Choisir Filtre","Montrer les étoiles","Detection Outliers","Modifier l'intensité","Détection Maximas Locaux"])
        self.filtre.setCurrentText("Choisir Filtre")
        self.filtre.currentIndexChanged.connect(self.onChangedFilter)
        
        # -------------------------------------- #
        #       Maxima Detection Layout :        #
        # -------------------------------------- #

        self.maximas = MaximasManager()
        self.maximas.button_maxima.clicked.connect(self.emitMaxima)

        # -------------------------------------- #
        #           Intensity Layout :           #
        # -------------------------------------- #
        
        self.intensity_manager = IntensityManager()
        self.intensity_manager.new_intensity.clicked.connect(self.emitIntensity)

        # -------------------------------------- #
        # Button with Outliers Detection & Label #
        # -------------------------------------- #

        self.outliers_manager = OutliersManager()
        self.outliers_manager.button_outliers.clicked.connect(self.emitSigma)

        self.image_display = None

        self.grid.addWidget(self.save_button,0,1)
        self.grid.addLayout(self.vlayout_right,1,1,3,1)
        self.grid.addWidget(self.left_image,1,0)
        self.grid.addWidget(self.stats,3,0)

        self.temp_layout = QHBoxLayout()
        

        self.hlayout_right.addWidget(self.box)
        self.vlayout_right.addLayout(self.hlayout_right)
        self.vlayout_right.addLayout(self.temp_layout)
        self.vlayout_right.addWidget(self.right_image)
        

    def emitSigma(self:Self):

        if self.outliers_manager.lineedit_outliers.text().strip().replace('.','').isdigit():
            self.outliers_manager.sigma = float(self.outliers_manager.lineedit_outliers.text())
            self.right_image.drawSigmaClipImage(self.image_display,self.outliers_manager.sigma)

    def emitMaxima(self:Self):
        
        if self.maximas.lineedit_maxima.text().strip().replace('.','').isdigit():
            self.maximas.h_maxima = float(self.maximas.lineedit_maxima.text())
            self.saveImage()
            self.right_image.drawMaximas('./calcul.png',self.maximas.h_maxima)


    def emitIntensity(self:Self):
        if self.intensity_manager.lineedit_imin.text().strip().replace('.','').isdigit():
            if self.intensity_manager.lineedit_imax.text().strip().replace('.','').isdigit():
                self.right_image.drawIntensity(
                                            self.image_display,
                                            float(self.intensity_manager.lineedit_imin.text()),
                                            float(self.intensity_manager.lineedit_imax.text())
                                            )
                                            
    def onChanged(self:Self):
        if self.box.currentText().lower()=="mediane":
            self.image_display = self.stacking.stacking_mediane()
        
        if self.box.currentText().lower()=="moyenne":
            self.image_display = self.stacking.stacking_moyenne()
        
        self.hlayout_right.addWidget(self.filtre)
        self.right_image.drawImage(self.image_display,
                                np.amin(self.image_display),
                                np.amax(self.image_display))
        print(type(np.amin(self.image_display)))
        

    def onChangedFilter(self:Self):
        
        if self.temp_layout is not None:
            while self.temp_layout.count():
                item = self.temp_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)

        if self.filtre.currentText().lower()=="montrer les étoiles":
            self.saveImage()
            self.right_image.drawStarsImages('./calcul.png')

        if self.filtre.currentText().lower()=="detection outliers":
            self.temp_layout.addWidget(self.outliers_manager)
        
        if self.filtre.currentText().lower()=="modifier l'intensité":
            self.temp_layout.addWidget(self.intensity_manager)

        if self.filtre.currentText().lower() == "détection maximas locaux":
            self.temp_layout.addWidget(self.maximas)
        
    def saveImage(self:Self):
        im = Image.fromarray(self.image_display[::3,::3])
        im = im.convert('RGB')
        im.save('calcul.png')
        print("Saved")

    def saveImageAsPng(self:Self):

        self.save = QFileDialog.getSaveFileName(self,"Enregistrer le fichier","",".png")
        try:
            im = Image.fromarray(self.image_display)
            im = im.convert('RGB')
            im.save(self.save[0]+".png")
        except:
            print("Chemin Invalide")

    def coloration_image(self:Self):
        print("Coloration Image...")
        self.left_image.drawImage(self.liste_images[0],
                                int(self.stats.lineedit_vmin.text()),
                                int(self.stats.lineedit_vmax.text()))
        print("Done")


# ---- Main
if __name__ == "__main__":

    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec_()