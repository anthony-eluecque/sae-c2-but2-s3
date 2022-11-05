from typing_extensions import Self
import numpy as np

class StackingManager():
    """
    Classe permettant le calcul de stacking différent
    réalisé lors de la SAE C2 BUT2 par ELUECQUE Anthony et DOURNEL
    Frédéric
    """
    def __init__(self:Self,liste_images:list[list[int]]):
        self.images = liste_images

    def stacking_mediane(self:Self)->np.ndarray:
        """
        Empilement d'images par médiane (Nombres entre 1 à N)
        Utilisable pour des images monochrome
        Le temps de calcul est plus ou moins long selon la taille de l'image

        Returns:
            np.ndarray: Image empilée
        """
        image = self.initEmptyImage()
        for row in range(len(image)):
            for elem in range(len(image[row])):
                liste_pixel = []
                for data_image in self.images:
                    liste_pixel.append(data_image[row][elem])
                image[row][elem] = self.mediane(liste_pixel)
        return image

    def stacking_moyenne(self:Self)->np.ndarray:
        """
        Empilement d'images par moyenne (Nombres entre 1 à N)
        Utilisable pour des images RGB mais aussi monochrome 
        Le temps de calcul est plus ou moins long selon la taille de l'image
        
        Returns:
            np.ndarray: Image empilée
        """
        print(len(self.images[0][0]))
        if len(self.images[0].shape)==3:
            print("RGB Stacking")
            image = self.initEmptyRGBImage()
            image = image.astype(int)
            for _image in self.images:
                image= image + _image
            image= image//len(self.images)
            return image
        else:
            print("Classique Stacking")
            image = self.initEmptyImage()
            for row in range(len(image)):
                for elem in range(len(image[row])):
                    sum_pixel = 0
                    for data_image in self.images:
                        sum_pixel += data_image[row][elem]
                    image[row][elem] = sum_pixel//len(self.images)
        return image

    def initEmptyImage(self:Self)->np.ndarray:
        """
        Fonction permettant de crée une image (ndarray) monochrome utilisé pour les méthodes
        de stacking (empilement)

        Returns:
            np.ndarray: Image Monochrome "vierge"
        """
        return np.zeros(shape=self.images[0].shape)

    def initEmptyRGBImage(self:Self)->np.ndarray:
        """
        Fonction permettant de crée une image (ndarray) RGB utilisé pour les méthodes
        de stacking (empilement)

        Returns:
            np.ndarray: Image RGB "vierge"
        """
        return np.zeros((self.images[0].shape[0],
                        self.images[0].shape[1],
                        self.images[0].shape[2]))

    def mediane(self:Self,l_pixel:list)->int:
        """
        Fonction permettant de calculer la médiane d'une liste de pixel
        d'une même coordonnée de X images

        Args:
            l_pixel (list): La liste des pixels de la même coordonnée de l'image

        Returns:
            int: La médiane
        """
        mid =  len(l_pixel) // 2
        l_pixel.sort()
        return l_pixel[mid] if len(l_pixel)%2 else l_pixel[mid-1]+l_pixel[mid]//2
