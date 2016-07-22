__author__ = 'ee364e02'

import numpy as np
from scipy import interpolate
from enum import Enum
# from scipy.misc import *
import PIL

class Homography():
    def __init__(self, **kwargs):
        self.effect = None
        if 'homographyMatrix' in kwargs:
            homog_matrix = kwargs['homographyMatrix']
            if len(homog_matrix) != 3:
                raise ValueError("Matrix not of size 3x3")
            for matrix_ele in homog_matrix:
                if len(matrix_ele) != 3:
                    raise ValueError("Matrix not of size 3x3")
                for value in matrix_ele:
                    if not isinstance(value, float):
                        raise ValueError("Matrix elements must be of type 'float'")
            str_rep = ""
            for row in homog_matrix:
                for column in row:
                    str_rep += str(column) + ","
                str_rep = str_rep[:-1] + ";"
            str_rep = str_rep[:-1]
            self.homographyMatrix = np.matrix(str_rep)
        elif 'sourcePoints' in kwargs and 'targetPoints' in kwargs:
            source_points = kwargs['sourcePoints']
            target_points = kwargs['targetPoints']
            if len(source_points) != 4 or len(target_points) != 4:
                raise ValueError("Source or Target Points not of size 4.")
            if 'effect' in kwargs:
                effect_val = kwargs['effect']
                if effect_val is not None:
                    if not isinstance(effect_val, Effect):
                        raise TypeError("'effect' argument must be of type Effect")
                    self.effect = effect_val
            self.homographyMatrix = self.computeHomography(source_points, target_points, self.effect)
        else:
            raise ValueError("Missing homographyMatrix OR sourcePoints, targetPoints arguments")

    def computeHomography(self, sourcePoints, targetPoints, effect=None):
        if effect is not None:
            new_source = [0, 1, 2, 3]
            if effect == Effect.rotate90:
                new_source = [2, 0, 3, 1] # 90
            elif effect == Effect.rotate180:
                new_source = [3, 2, 1, 0] # 180
            elif effect == Effect.rotate270:
                new_source = [1, 3, 0, 2] # 270
            elif effect == Effect.flipVertically:
                new_source = [1, 0, 3, 2] # vertical
            elif effect == Effect.flipHorizontally:
                new_source = [2, 3, 0, 1] # horizontal
            elif effect == Effect.transpose:
                new_source = [0, 2, 1, 3] # transpose
            sourcePoints = [sourcePoints[i] for i in new_source]

        coef_matrix = np.matrix([[sourcePoints[0][0], sourcePoints[0][1], 1, 0, 0, 0, -1 * sourcePoints[0][0] * targetPoints[0][0], -1 * sourcePoints[0][1] * targetPoints[0][0]],
              [0, 0, 0, sourcePoints[0][0], sourcePoints[0][1], 1, -1 * sourcePoints[0][0] * targetPoints[0][1], -1 * sourcePoints[0][1] * targetPoints[0][1]],
              [sourcePoints[1][0], sourcePoints[1][1], 1, 0, 0, 0, -1 * sourcePoints[1][0] * targetPoints[1][0], -1 * sourcePoints[1][1] * targetPoints[1][0]],
              [0, 0, 0, sourcePoints[1][0], sourcePoints[1][1], 1, -1 * sourcePoints[1][0] * targetPoints[1][1], -1 * sourcePoints[1][1] * targetPoints[1][1]],
              [sourcePoints[2][0], sourcePoints[2][1], 1, 0, 0, 0, -1 * sourcePoints[2][0] * targetPoints[2][0], -1 * sourcePoints[2][1] * targetPoints[2][0]],
              [0, 0, 0, sourcePoints[2][0], sourcePoints[2][1], 1, -1 * sourcePoints[2][0] * targetPoints[2][1], -1 * sourcePoints[2][1] * targetPoints[2][1]],
              [sourcePoints[3][0], sourcePoints[3][1], 1, 0, 0, 0, -1 * sourcePoints[3][0] * targetPoints[3][0], -1 * sourcePoints[3][1] * targetPoints[3][0]],
              [0, 0, 0, sourcePoints[3][0], sourcePoints[3][1], 1, -1 * sourcePoints[3][0] * targetPoints[3][1], -1 * sourcePoints[3][1] * targetPoints[3][1]]])

        dep_matrix = np.matrix([[targetPoints[0][0]],[targetPoints[0][1]],[targetPoints[1][0]],[targetPoints[1][1]],
                                [targetPoints[2][0]],[targetPoints[2][1]],[targetPoints[3][0]],[targetPoints[3][1]]])

        h_vert = np.linalg.solve(coef_matrix, dep_matrix)
        h_rearr = np.vstack([h_vert, 1])
        h_rearr = np.reshape(h_rearr, (3,3))
        return h_rearr

    def forwardProject(self, point):
        x, y = point
        homog_matrix = self.homographyMatrix
        point_matrix = np.matrix("{0};{1};1".format(str(x), str(y)))
        x_prime_matrix = homog_matrix * point_matrix
        x_prime_matrix /= x_prime_matrix[2]
        return tuple([round(float(x_prime_matrix[0][0]),2), round(float(x_prime_matrix[1][0]),2)])

    def inverseProject(self, pointPrime):
        x_p, y_p = pointPrime
        inv_homog_matrix = self.homographyMatrix.I
        x_prime_matrix = np.matrix("{0};{1};1".format(str(x_p), str(y_p)))
        x_matrix = inv_homog_matrix * x_prime_matrix
        x_matrix /= x_matrix[2]
        return tuple([np.round(float(x_matrix[0][0]),2), np.round(float(x_matrix[1][0]),2)])

class Transformation():
    def __init__(self, sourceImage, homography=None):
        if not isinstance(sourceImage, np.ndarray):
            raise TypeError("sourceImage must be of type numpy.ndarray")
        if not isinstance(homography, Homography) and not homography is None:
            raise TypeError("homography must be of type Homography")
        self.sourceImage = sourceImage
        self.homography = homography
        self.targetPoints = None

    def setupTransformation(self, targetPoints, effect=None):
        if self.targetPoints is None:
            self.targetPoints = targetPoints
        # question: compute a new homography?
        max_y, max_x = self.sourceImage.shape[0] - 1, self.sourceImage.shape[1] - 1
        sourcePoints = [(0,0), (max_x, 0), (0, max_y), (max_x, max_y)]
        self.homography = Homography(sourcePoints=sourcePoints, targetPoints=targetPoints, effect=effect)

    def transformImage(self, containerImage):
        if not isinstance(containerImage, np.ndarray):
            raise TypeError("containerImage must be of type numpy.ndarray")
        if containerImage.ndim != 2:
            raise ValueError("containerImage may only be two dimensional")
        top_left, _, _, bottom_right = calculateBoundingBox(self.targetPoints)
        source_max_x, source_max_y = self.sourceImage.shape[1] - 1, self.sourceImage.shape[0] - 1
        min_x, min_y = top_left
        max_x, max_y = bottom_right
        rbs = interpolate.RectBivariateSpline(np.arange(0, source_max_y + 1, 1), np.arange(0, source_max_x + 1, 1), self.sourceImage, kx=1, ky=1)
        for x_coord in range(int(min_x), int(max_x) + 1):
            for y_coord in range(int(min_y), int(max_y) + 1):
                projected_x, projected_y = self.homography.inverseProject((x_coord, y_coord))
                new_z = rbs(projected_y, projected_x)
                if 0.0<= projected_x <= source_max_x and 0.0 <= projected_y <= source_max_y:
                    containerImage[y_coord][x_coord] = new_z
        return containerImage

class ColorTransformation(Transformation):
    def __init__(self, sourceImage, homography=None):
        super().__init__(sourceImage, homography)
        if len(sourceImage.shape) != 3:
            raise ValueError("sourceImage shape must be of length 3")

    def transformImage(self, containerImage):
        if not isinstance(containerImage, np.ndarray):
            raise TypeError("containerImage must be of type numpy.ndarray")
        if containerImage.ndim != 3:
            raise ValueError("containerImage may only be three dimensional")
        top_left, _, _, bottom_right = calculateBoundingBox(self.targetPoints)
        source_max_x, source_max_y = self.sourceImage.shape[1], self.sourceImage.shape[0]
        min_x, min_y = top_left
        max_x, max_y = bottom_right
        rbs_b = interpolate.RectBivariateSpline(range(0, source_max_y), range(0, source_max_x), self.sourceImage[:,:,0], kx=1, ky=1)
        rbs_g = interpolate.RectBivariateSpline(range(0, source_max_y), range(0, source_max_x), self.sourceImage[:,:,1], kx=1, ky=1)
        rbs_r = interpolate.RectBivariateSpline(range(0, source_max_y), range(0, source_max_x), self.sourceImage[:,:,2], kx=1, ky=1)
        for x_coord in range(int(min_x), int(max_x) + 1):
            for y_coord in range(int(min_y), int(max_y) + 1):
                projected_x, projected_y = self.homography.inverseProject((x_coord, y_coord))
                new_b = rbs_b(projected_y, projected_x)
                new_g = rbs_g(projected_y, projected_x)
                new_r = rbs_r(projected_y, projected_x)
                if 0.0<= projected_x <= (source_max_x - 1) and 0.0 <= projected_y <= (source_max_y - 1):
                    containerImage[y_coord][x_coord][0] = new_b
                    containerImage[y_coord][x_coord][1] = new_g
                    containerImage[y_coord][x_coord][2] = new_r
        return containerImage

class Effect(Enum):
    rotate90 = 1
    rotate180 = 2
    rotate270 = 3
    flipHorizontally = 4
    flipVertically = 5
    transpose = 6

def calculateBoundingBox(targetPoints):
    x_coords = sorted([x for x,_ in targetPoints])
    y_coords = sorted([y for _,y in targetPoints])
    min_x, max_x = x_coords[0], x_coords[-1]
    min_y, max_y = y_coords[0], y_coords[-1]
    top_left     = min_x, min_y
    top_right    = max_x, min_y
    bottom_left  = min_x, max_y
    bottom_right = max_x, max_y
    return top_left, top_right, bottom_left, bottom_right

if __name__ == '__main__':
    homog = Homography(sourcePoints= [(1.0, 2.0), (3.0, 4.0), (5.0, 6.0), (7.0, 8.0)],
                       targetPoints=[(9.0, 10.0), (11.0, 12.0), (13.0, 14.0), (15.0, 16.0)])
    transformer = Transformation([(9.0, 10.0), (11.0, 12.0), (13.0, 14.0), (15.0, 16.0)])
    pass