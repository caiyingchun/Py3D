import math


##
# A class to represent a vector in 3D space, with various operations that can be applied to it
##
class Vector3D:

    def __init__(self, x, y, z, cols=None):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.cn = None
        self.spec = 0
        self.col = cols
        self.mag = math.sqrt(x ** 2 + y ** 2 + z ** 2)

    # Move formatting for debugging
    def __repr__(self):
        return "<Vector3D x=%s, y=%s, z=%s, cn=%s, mag=%s>" % (self.x, self.y, self.z, self.cn, self.mag)

    ## Overrides '=='
    def  __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    ## Overrides '-'
    def __sub__(self, other):
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    ## Overrides '+'
    def __add__(self, other):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    ## Overrides '/'
    def __div__(self, num):
        return Vector3D(self.x / num, self.y / num, self.z / num)

    ## Overrides '*', we use this to represent dot product.
    def __mul__(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    ## Overrides '**', we use this to represent cross product.
    def __pow__(self, other):
        nx = self.y * other.z - self.z * other.y
        ny = self.z * other.x - self.x * other.z
        nz = self.x * other.y - self.y * other.x
        return Vector3D(nx, ny, nz)

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    ##
    # Returns the average of a collection of vectors.
    ##
    def average(self, others, num):
        x = self.x
        y = self.y
        z = self.z
        for vec in others:
            norm = vec.surfaceNormal
            x += norm.x
            y += norm.y
            z += norm.z
        x /= num
        y /= num
        z /= num
        return Vector3D(x, y, z)

    def unit_vector(self):
        if(self.mag <= 0.0):
            return Vector3D(1.0, 0.0, 0.0)
        else:
            return Vector3D(self.x / self.mag, self.y / self.mag, self.z / self.mag)

    def apply(self, transform):
        x = transform[0][0] * self.x + transform[0][1] * self.y + transform[0][2] * self.z + transform[0][3]
        y = transform[1][0] * self.x + transform[1][1] * self.y + transform[1][2] * self.z + transform[1][3]
        z = transform[2][0] * self.x + transform[2][1] * self.y + transform[2][2] * self.z + transform[2][3]
        return Vector3D(x, y, z, cols=self.col)
