import numpy as np
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt

class KochFractal(ABC):
    def __init__(self, base):
        self.base = np.array(base)

    @staticmethod
    def gen_reg_polygon_base(sides):
        angles = -2 * np.pi * np.arange(sides) / sides
        steps = np.stack((np.cos(angles), np.sin(angles)), axis=1)
        points = np.concatenate(([np.array([0, 0])], np.cumsum(steps, axis=0)))
        points = np.vstack((points, [0, 0]))
        return points
        
    @abstractmethod
    def segment_transformation(self, a, b):
        """
        Given an edge from point a to point b, return a list of new points
        that replaces the segment according to the fractal's rule.
        The list should start with the first point (not including a)
        and end with b.
        """
        pass

    def new_gen(self):
        # Start with the first point.
        new_points = [self.base[0]]
        # Process each segment.
        for i in range(len(self.base) - 1):
            a = self.base[i]
            b = self.base[i + 1]
            # Apply the transformation defined in the subclass.
            new_segment = self.segment_transformation(a, b)
            new_points.extend(new_segment)
        self.base = np.array(new_points)
        return self.base

    def generate(self, generations):
        for _ in range(generations):
            self.new_gen()
        return self.base

class KochTriangle(KochFractal):
    def segment_transformation(self, a, b):
        
        point_b = a + (b - a) / 3
        point_d = b - (b - a) / 3
        # 60° rotation matrix (counterclockwise)
        R60 = np.array([
            [1/2, -np.sqrt(3)/2],
            [np.sqrt(3)/2, 1/2]
        ])
        point_c = point_b + np.dot(R60, (point_b - a))
       
        return [point_b, point_c, point_d, b]

class KochSquare(KochFractal):
    def segment_transformation(self, a, b):
        """
        For the square fractal, the rule is a bit more elaborate:
        Divide the segment into quarters (points B and H).
        Compute intermediate point E (midpoint of B and H).
        Construct two "bumps" on the segment.
        """
        
        R = np.array([[0, -1], [1, 0]])   # 90° counterclockwise
        R1 = np.array([[0, 1], [-1, 0]])   # 90° clockwise

        point_b = (3 * a + b) / 4
        point_h = (a + 3 * b) / 4
        point_e = (point_b + point_h) / 2
        point_c = point_b + np.dot(R, (point_e - point_b))
        point_d = point_c + np.dot(R1, (point_c - point_b))
        point_f = point_e + np.dot(R1, (point_h - point_e))
        point_g = point_h + np.dot(R1, (point_h - point_e))

      
        return [point_b, point_c, point_d, point_e, point_f, point_g, point_h, b]
    
class KochPentagon(KochFractal):
    def segment_transformation(self, a, g):
        """
        For a segment from point a to g, this transformation does the following:
          - point_b: one-third of the way from a to g.
          - point_f: two-thirds of the way from a to g.
          - point_c: computed from point_b and point_f using rotation matrix R1.
          - point_e: computed from point_b and point_f using rotation matrix R.
          - point_imaginary: computed from point_b and point_c using rotation matrix R3.
          - point_d: computed from point_c and point_imaginary using rotation matrix R4.
        
        The new points replacing the original segment are:
          [point_b, point_c, point_d, point_e, point_f, g]
        """
        # Define rotation matrices as given:
        R  = np.array([[-0.309016994375, -0.951056516295],
                       [ 0.951056516295, -0.309016994375]])
        R1 = np.array([[-0.309016994375,  0.951056516295],
                       [-0.951056516295, -0.309016994375]])
        R3 = np.array([[ 0.809016994375, -0.587785252292],
                       [ 0.587785252292,  0.809016994375]])
        R4 = np.array([[-0.809016994375,  0.587785252292],
                       [-0.587785252292, -0.809016994375]])
        
        # Compute intermediate points:
        point_b = (2 * a + g) / 3         # One-third point along segment a->g.
        point_f = (a + 2 * g) / 3         # Two-thirds point along segment a->g.
        point_c = point_b + np.matmul(R1, (point_f - point_b))
        point_e = point_f + np.matmul(R, (point_b - point_f))
        point_imaginary = point_c + np.matmul(R3, (point_c - point_b))
        point_d = point_c + np.matmul(R4, (point_c - point_imaginary))
        
        return [point_b, point_c, point_d, point_e, point_f, g]
    
class KochTrapezoid(KochFractal):
    def segment_transformation(self, a, b):
        """
        For the segment from a to b, we do the following:
          - point_b: one-third of the way from a to b.
          - point_g: two-thirds of the way from a to b (or, b minus one-third).
          - point_c: from point_b, add a rotated vector (using R2).
          - point_d: from point_c, add the rotated vector (using R3).
          - point_f: from point_g, add a rotated vector (using R).
        The new points will be: [point_b, point_c, point_d, point_f, point_g, b]
        """
        # Define the rotation matrices as given:
        R2 = np.array([
            [np.cos(2*np.pi/3), -np.sin(2*np.pi/3)],
            [np.sin(2*np.pi/3),  np.cos(2*np.pi/3)]
        ])
        R3 = np.array([
            [np.cos(-2*np.pi/3), -np.sin(-2*np.pi/3)],
            [np.sin(-2*np.pi/3),  np.cos(-2*np.pi/3)]
        ])
        R = np.array([
            [1/2, -np.sqrt(3)/2],
            [np.sqrt(3)/2, 1/2]
        ])

        # Compute the new points using your functions
        point_b = a + (b - a) / 3
        point_g = b - (b - a) / 3
        point_c = point_b + np.matmul(R2, (point_b - a))
        point_d = point_c + np.matmul(R3, (point_c - point_b))
        point_f = point_g + np.matmul(R, (b - point_g))

        return [point_b, point_c, point_d, point_f, point_g, b]
    
class KochOctagon(KochFractal):
    def segment_transformation(self, a, j):
        """
        For a segment from point a to j:
          - point_b is one-third of the way from a to j.
          - point_i is two-thirds of the way from a to j.
          - point_c is computed from a and point_b using a rotation by 225° (R225).
          - Then, a series of points (point_d, point_e, point_f, point_g, point_h) 
            are computed by successively rotating the previous segment by 45° (using R45).
        The new points replacing the segment (a, j) are:
          [point_b, point_c, point_d, point_e, point_f, point_g, point_h, point_i, j]
        """
        # Define the rotation matrices used in this variant:
        R45 = np.array([[(2**0.5)/2, -(2**0.5)/2],
                        [(2**0.5)/2,  (2**0.5)/2]])
        R225 = np.array([[-(2**0.5)/2, (2**0.5)/2],
                         [-(2**0.5)/2, -(2**0.5)/2]])
        
        # Compute the intermediate points:
        point_b = a + (j - a) / 3
        point_i = (a + 2 * j) / 3
        point_c = point_b + np.matmul(R225, (point_b - a))
        point_d = point_c + np.matmul(R45, (point_c - point_b))
        point_e = point_d + np.matmul(R45, (point_d - point_c))
        point_f = point_e + np.matmul(R45, (point_e - point_d))
        point_g = point_f + np.matmul(R45, (point_f - point_e))
        point_h = point_g + np.matmul(R45, (point_g - point_f))
        
        return [point_b, point_c, point_d, point_e, point_f, point_g, point_h, point_i, j]


def plot_fractal(points):
    plt.axis("equal")
    plt.plot(*points.transpose())
    plt.show()

def main():
    base_fractal = KochFractal.gen_reg_polygon_base(3)
    points = KochTriangle(base_fractal).generate(1)
    plot_fractal(points)

if __name__ == "__main__":
    main()