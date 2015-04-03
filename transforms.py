import math


##
# Wrapper class to be used for generating appropriate transforms, or compositions thereof.
##
class Transform:

    @classmethod
    def translation(self, vec3):
        return [[1.0, 0.0, 0.0, vec3.x],
                [0.0, 1.0, 0.0, vec3.y],
                [0.0, 0.0, 1.0, vec3.z]]

    @classmethod
    def scale(self, vec3):
        return [[vec3.x, 0.0, 0.0, 0.0],
                [0.0, vec3.y, 0.0, 0.0],
                [0.0, 0.0, vec3.z, 0.0]]

    @classmethod
    def x_rotate(self, theta):
        sinth = math.sin(theta)
        costh = math.cos(theta)
        return [[1.0, 0.0,    0.0,   0.0],
                [0.0, costh, -sinth, 0.0],
                [0.0, sinth, costh, 0.0]]

    @classmethod
    def y_rotate(self, theta):
        sinth = math.sin(float(theta))
        costh = math.cos(float(theta))
        return [[costh,  0.0, sinth, 0.0],
                [0.0,    1.0, 0.0,   0.0],
                [-sinth, 0.0, costh, 0.0]]

    @classmethod
    def z_rotate(self, theta):
        sinth = math.sin(theta)
        costh = math.cos(theta)
        return [[costh, -sinth, 0.0, 0.0],
                [sinth,  costh, 0.0, 0.0],
                [0.0,    0.0,   1.0, 0.0]]

    @classmethod
    def compose(self, v1, v2):

        ans = []
        for row in range(0, 3):
            ans.append([0, 0, 0, 0])
            for col in range(0, 4):
                for i in range(0, 3):
                    ans[row][col] += v1[row][i] * v2[i][col]
            ans[row][3] += v1[row][3]
        return ans
