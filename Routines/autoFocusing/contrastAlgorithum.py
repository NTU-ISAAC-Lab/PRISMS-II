"""
NAME: contrastAlgorithum.py
AUTHOR: John Archibald Page
DATE CREATED: 24/05/2023
DATE LAST UPDATED: 24/05/2023

PURPOSE:
a range of contrast algorithumns that can be sued to assess an image.

1) https://github.com/vismantic-ohtuprojekti/qualipy/blob/master/qualipy/utils/focus_measure.py
2) https://stackoverflow.com/questions/33679738/measure-edge-strength-in-opencv-magnitude-of-gradient
"""
import cv2
import numpy as np 

class contrastAlgorithums_class():
    """Functionality to autofocus the camera"""
    #1)
    def LAPV(img):
        """Implements the Variance of Laplacian (LAP4) focus measure
        operator. Measures the amount of edges present in the image.
        :param img: the image the measure is applied to
        :type img: np.ndarray
        :returns: np.float32 -- the degree of focus
        """
        return(np.std(cv2.Laplacian(img, cv2.CV_64F)) ** 2)


    def LAPM(img):
        """Implements the Modified Laplacian (LAP2) focus measure
        operator. Measures the amount of edges present in the image.
        :param img: the image the measure is applied to
        :type img: np.ndarray
        :returns: np.float32 -- the degree of focus
        """
        kernel = np.array([-1, 2, -1])
        laplacianX = np.abs(cv2.filter2D(img, -1, kernel))
        laplacianY = np.abs(cv2.filter2D(img, -1, kernel.T))
        return(np.mean(laplacianX + laplacianY))


    def TENG(img):
        """Implements the Tenengrad (TENG) focus measure operator.
        Based on the gradient of the image.
        :param img: the image the measure is applied to
        :type img: np.ndarray
        :returns: np.float32 -- the degree of focus
        """
        gaussianX = cv2.Sobel(img, cv2.CV_64F, 1, 0)
        gaussianY = cv2.Sobel(img, cv2.CV_64F, 1, 0)
        return(np.mean(gaussianX * gaussianX + gaussianY * gaussianY))


    #def MLOG(img):
        """Implements the MLOG focus measure algorithm.
        :param img: the image the measure is applied to
        :type img: np.ndarray
        :returns: np.float32 -- the degree of focus
        """
    #    return(np.max(cv2.convertScaleAbs(cv2.Laplacian(img, 3))))
"""
#2)
    def getGradientMagnitude(im):
        "Get magnitude of gradient for given image"
        ddepth = cv2.CV_32F
        dx = cv2.Sobel(im, ddepth, 1, 0)
        dy = cv2.Sobel(im, ddepth, 0, 1)
        dxabs = cv2.convertScaleAbs(dx)
        dyabs = cv2.convertScaleAbs(dy)
        mag = cv2.addWeighted(dxabs, 0.5, dyabs, 0.5, 0)
        return(mag)
"""