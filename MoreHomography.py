__author__ = 'ee364e02'

import numpy as np
from scipy import interpolate

class AdvancedTransformation():
    def __init__(self, sourceImage, v, h1, h2):
        if not isinstance(sourceImage, np.ndarray):
            raise TypeError("sourceImage must be of type numpy.ndarray")
        if sourceImage.ndim != 3:
            raise ValueError("sourceImage must be a color image (3-dimensional)")
        if sourceImage.shape[1] % 2 != 0:
            raise ValueError("sourceImage must have an even number of columns")
        self.sourceImage = sourceImage
        self.v = v
        self.h1 = h1
        self.h2 = h2

    def applyEffectV(self):
        max_y, max_x, _ = self.sourceImage.shape
        print(max_x, max_y)

    def applyEffectA(self):
        pass

if __name__ == '__main__':
    atran = AdvancedTransformation