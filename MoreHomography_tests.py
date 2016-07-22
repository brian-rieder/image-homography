import os
from glob import glob
import unittest
from random import uniform
from inspect import isclass
from enum import Enum
from scipy.misc import *
import numpy as np

from MoreHomography import *


class MoreHomographyTestSuite(unittest.TestCase):

    # This flag will delete all mismatched images at the end of any full run.
    # Set to False if you want to investigate the images.
    deleteMismatched = True
    imagesFolder = "MoreTestImages"
    parameterList = [(0, 0, 50), (0, 50, 0), (100, 0, 0), (0, 50, 50),
                     (100, 50, 0), (100, 0, 50), (100, 50, 50)]

    def test_advancedTransformationInitializer(self):
        """
        Test the behavior of the AdvancedTransformation initializer.
        """
        with self.subTest(key="Good Image"):
            img = np.ones([10, 10, 3], dtype=np.uint8)
            trans = AdvancedTransformation(img, 0, 0, 0)

            self.assertIsInstance(trans, AdvancedTransformation)

        with self.subTest(key="Bad Image 1"):
            img = [[0, 0], [1, 1]]

            self.assertRaises(TypeError, AdvancedTransformation, img, 0, 0, 0)

        with self.subTest(key="Bad Image 2"):
            img = np.ones([10, 10], dtype=np.uint8)

            self.assertRaises(ValueError, AdvancedTransformation, img, 0, 0, 0)

        with self.subTest(key="Bad Image 3"):
            img = np.ones([10, 11, 3], dtype=np.uint8)

            self.assertRaises(ValueError, AdvancedTransformation, img, 0, 0, 0)

    def test_applyEffectV(self):
        """
        Test the Effect V application.
        """
        sourceImagePath = self.imagesFolder + "/Ring.png"
        sourceImage = imread(sourceImagePath)

        for v, h1, h2 in self.parameterList:
            parameters = v, h1, h2

            with self.subTest(key=(v, h1, h2)):
                areEqual = self.checkTransformation(sourceImage, AdvancedTransformation.applyEffectV, "EffectV", parameters)
                self.assertTrue(areEqual)

    def test_applyEffectA(self):
        """
        Test the Effect A application.
        """
        sourceImagePath = self.imagesFolder + "/Ring3.png"
        sourceImage = imread(sourceImagePath)

        for v, h1, h2 in self.parameterList:
            parameters = v, h1, h2

            with self.subTest(key=(v, h1, h2)):
                areEqual = self.checkTransformation(sourceImage, AdvancedTransformation.applyEffectA, "EffectA", parameters)
                self.assertTrue(areEqual)

    def checkTransformation(self, sourceImage, EffectFunction, effectString, parameters):
        """
        This is a support method to simplify transformation code.
        """

        v, h1, h2 = parameters

        transformer = AdvancedTransformation(sourceImage, v, h1, h2)
        actualImage = EffectFunction(transformer)

        resultImagePath = self.imagesFolder + "/Ring_{0}_{1:03d}_{2:03d}_{3:03d}.png".format(effectString, v, h1, h2)
        differenceFilePath = resultImagePath.replace(".png", "_Mismatch.png")

        expectedImage = imread(resultImagePath)
        areEqual = self.areImagesAlmostEqual(expectedImage, actualImage, differenceFilePath)

        return areEqual

    def areImagesAlmostEqual(self, firstImage, secondImage, differenceFilePath):
        """
        Check if the two images are equal up to a difference of 2 per pixel, and return True if they are, otherwise
        return False. Also, this method saves the difference image for later comparison.
        """
        maxAllowableDifference = 2
        difference = np.absolute(firstImage - secondImage)

        if not np.any(difference > maxAllowableDifference):
            return True

        if firstImage.ndim == 3:
            differenceMap = np.any(difference, 2)
        else:
            differenceMap = difference

        differenceImage = 255 * np.array(differenceMap, np.uint8)

        print("Non zero = {0} in {1}".format(np.count_nonzero(differenceImage), differenceFilePath))
        imsave(differenceFilePath, differenceImage)

        # # Output file: Enable if you want to save the actual file.
        # outputFilePath = differenceFilePath.replace("Mismatch", "Output")
        # imsave(outputFilePath, secondImage)

        return False

    @classmethod
    def tearDownClass(cls):
        """
        Clean up the created files, as unit tests are not supposed to change the environment.
        """
        if not cls.deleteMismatched:
            return

        mismatchedFiles = glob(cls.imagesFolder + "/*Mismatch*")
        for filePath in mismatchedFiles:

            if os.path.exists(filePath):
                os.remove(filePath)


if __name__ == "__main__":
    unittest.main()
