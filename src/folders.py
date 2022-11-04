from PyQt5.QtWidgets import QWidget,QPushButton,QFileDialog,QHBoxLayout,QDialog
from PyQt5.QtCore import pyqtSignal
import os
from typing_extensions import Self
from astropy.io import fits

class Folders(QWidget):

    # Emit Signal à MainWindow
    signalDisplayImage = pyqtSignal(list)

    def __init__(self:Self):
        super().__init__()

        self.currentLayout = QHBoxLayout()
        self.setLayout(self.currentLayout)


        self.button_image = QPushButton("Ouvrir un Dossier")
        self.button_image.clicked.connect(self.get_folder_image)

        self.button_fichier_image = QPushButton("Ouvrir un Fichier")
        self.button_fichier_image.clicked.connect(self.get_file)

        self.currentLayout.addWidget(self.button_image)
        self.currentLayout.addWidget(self.button_fichier_image)

    def get_folder_image(self:Self):
        """
        Fonction permettant d'ouvrir la totalité des fichiers FITS de la même image à partir d'un dossier
        Attention, le dossier ne doit contenir que les images de celles-ci

        L'ouverture des fichiers est différentes selon si les images sont RGB ou Monochrome, en effet une image RGB aura ses valeurs entre 0 & 1, ici nous convertissons
        directement ses valeurs en les multipliant par 255 pour revenir à un ratio de couleur classique (simplifiant les calculs par la suite)

        Selectionner "Ouvrir un dossier" sur l'application
        """
        
        self.path = QFileDialog.getExistingDirectory(self,"Ouvrir dossiers des images",r"C:\Users\Antorak\Desktop\BUT 2\SAE C2\fits_tests")
        
        try:
            self.list_of_images = os.listdir(self.path)
            self.list_fits_images = []

            image0 = fits.open(self.path+"/"+self.list_of_images[0])
            if len(image0[0].shape)==3:
                print("RGB FITS")
                for image in self.list_of_images:
                    data_image = fits.open(self.path+"/"+image,ext=0)
                    data_image[0].data = data_image[0].data.swapaxes(0,1)
                    data_image[0].data = data_image[0].data.swapaxes(1,2)
                    data_image[0].data*= 255
                    data_image[0].data = data_image[0].data.astype(int)
                    self.list_fits_images.append(data_image)
            else:    
                print("Classique")
                for image in self.list_of_images:
                    self.list_fits_images.append(fits.open(self.path+"/"+image))

            self.signalDisplayImage.emit(self.list_fits_images)
        except:
            print("Chemin Invalide")

    def get_file(self:Self):
        """
        Fonction permettant d'ouvrir un fichier FITS
        Attention, le fichier ne doit pas être autre extension que FITS.

        Selectionner "Ouvrir un fichier" sur l'application


        """
        self.path = QFileDialog()
        self.path.setFileMode(QFileDialog.AnyFile)

        if self.path.exec_():
            filenames = []
            for file in self.path.selectedFiles():
                filenames.append(fits.open(file))
            self.signalDisplayImage.emit(filenames)