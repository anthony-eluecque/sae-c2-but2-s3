from typing_extensions import Self
from PyQt5.QtWidgets import QHBoxLayout,QWidget
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from skimage import io
from skimage import exposure
from skimage.morphology import extrema

from astropy.stats import SigmaClip
from skimage.feature import blob_log
from skimage.color import rgb2gray,label2rgb
from skimage.measure import label

class CanvasImage(QWidget):

    def __init__(self:Self):

        super().__init__()
        layout = QHBoxLayout()
        self.figure : Figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.figure.clear()
        self.canvas.draw()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def drawImage(self:Self,new_img:np.ndarray,amin:np.float64,amax:np.float64):
        """
        Fonction permettant de dessiner une Image sur un Canvas à partir
        d'un numpy.ndarray (image)
        Args:
            new_img (np.ndarray): L'image à montrer dans le Canvas
            amin (np.float64): Le minimun du Color Scaling de l'image
            amax (np.float64): Le maximun du Color Scaling de l'image
        """
        self.canvas.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.ax.imshow(new_img,vmin=amin,vmax=amax,cmap='gray')
        self.ax.set_axis_off()
        self.figure.tight_layout()
        self.canvas.draw()

    def drawStarsImages(self:Self,file):
        """
        Fonction permettant de trouver quels sont les corps célestes (Tout ce qui est lumineux dans une image)
        On utile pour cela un gaussien de laplace, utilisé afin de trouver sur une image noir et blanc les éléments lumineux (blobs)

        Le gaussien aura pour effet de lisser l'image puisque le laplacien est très sensible au bruit

        Attention : si l'image est uniforme, le LoG donnera une image noir.

        Args:
            self (Self): _description_
            file (_type_): _description_
        """
        self.canvas.figure.clear()
        read_image = io.imread(file)[:,:,:3]
        image_gray = rgb2gray(read_image)
        blobs_log = blob_log(image_gray, max_sigma=35, num_sigma=10, threshold=.1)
        self.ax = self.figure.add_subplot()
        self.ax.imshow(read_image)

        print("Running Stars Finder")
        for blob in blobs_log:
            y, x, r = blob
            c = plt.Circle((x, y), r, color='red', linewidth=1.5, fill=False)
            self.ax.add_artist(c)
        self.figure.tight_layout()
        self.ax.set_axis_off()
        print("Stars Finder Done")
        self.canvas.draw()

    def drawHistogram(self:Self,data_images:list[list[int]]):
        """Fonction permettant de dessiner le color Scaling d'une image ou plusieurs
        Args:
            data_images (list[list[int]]): Les images utilisées
        """
        self.canvas.figure.clear()
        self.ax = self.figure.add_subplot()

        self.ax.hist(data_images.flatten(),facecolor="green",bins="auto",alpha=0.75)
        self.ax.set_title("Color Scaling de l'image (en haut à gauche)")
        self.canvas.draw()

    def drawSigmaClipImage(self:Self,image:np.ndarray,sig:float):
        """Fonction permettant de dessiner une image en remplaçant les valeurs abérrantes
        par des carrées blancs à partir d'un sigma et d'une méthode de stacking (image)

        Par défault, nous avons réglé le Sigma à 2.85, valeur la plus cohérente après test
        Args:
            image (np.ndarray): Image correspondant au stacking utilisé
            sig (float): Sigma correspondant à l'isolement souhaité des valeurs abérrantes
        """
        self.canvas.figure.clear()
        sig_clip = SigmaClip(sigma=sig, maxiters=1)
        self.canvasDisplay(sig_clip(image))

    def drawIntensity(self:Self,image:np.ndarray,min:float,max:float):
        """Fonction permettant de filtrer une image à partir d'un stacking avec des intensités de couleurs
        différentes selon l'input de l'utilisateur
        Par défault, l'intensité de l'image correspondant au maximun pris par le type de l'image

        Args:
            image (np.ndarray): Image correspondant au stacking utilisé
            min (float): Le Minimun de l'intensité (couleur) voulu
            max (float): Le Maximun de l'intensité (couleur) voulu
        """
        self.canvas.figure.clear()
        log = exposure.rescale_intensity(image,(min,max))
        self.canvasDisplay(log)

    def drawMaximas(self:Self,file,h):
        
        self.canvas.figure.clear()
        read_image = io.imread(file)[:,:,:3]
        image_gray = rgb2gray(read_image)
        maxima = extrema.h_maxima(image_gray,h)
        overlay_h = label2rgb(label(maxima), image_gray, alpha=0.7, bg_label=0,
                            bg_color=None, colors=[(1, 0, 0)])
        self.canvasDisplay(overlay_h)

    def canvasDisplay(self:Self,image):
        """
        Fonction permettant d'afficher le canvas sur le widget

        Args:
            image : L'image à afficher
        """
        self.ax = self.figure.add_subplot()
        self.ax.imshow(image,cmap='gray')
        self.ax.set_axis_off()
        self.figure.tight_layout()
        self.canvas.draw()