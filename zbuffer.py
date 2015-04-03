import cStringIO
from config import *


def get_z_buffered_pixels(self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, offset=(0, 0), baseimage=BASE_IMAGE):
        lights = self.lightsources
        z_map = {}
        pixel_map = {}
        min_max_y = {}
        min_max_x = {}

        for polygon in self.polygons:
                for coords, color in polygon.pixels(lights, self):
                    x, y, z = coords
                    x += CANVAS_WIDTH * offset[0]
                    y += CANVAS_HEIGHT * offset[1]
                    ix = int(x)
                    iy = int(y)
                    pos = (x, y)

                    if not pos in z_map or z_map[pos] > z:
                        pixel_map[pos] = color
                        z_map[pos] = z

                    if self.toon_shading:
                        if not iy in min_max_y:
                            min_max_y[iy] = [ix, ix]
                        else:
                            if ix < min_max_y[iy][0]:
                                min_max_y[iy][0] = ix
                            elif x > min_max_y[y][1]:
                                min_max_y[iy][1] = ix

                        if not ix in min_max_x:
                            min_max_x[ix] = [iy, iy]
                        else:
                            if iy < min_max_x[ix][0]:
                                min_max_x[ix][0] = iy
                            elif iy > min_max_x[ix][1]:
                                min_max_x[ix][1] = iy

        out = cStringIO.StringIO()
        lst = baseimage[:]

        for pos, color in pixel_map.items():
            try:
                if 0 < pos[0] < height and 0 < pos[1] < width:
                    lst[int(pos[1] * width + pos[0])] = struct.pack("BBB", *color)
            except:
                pass

        if self.toon_shading:
            for y, min_max in min_max_y.items():
                for x in range(min_max[0] - 1, min_max[1] + 2):
                    try:
                        if (not (x, y) in z_map and (x + 1, y) in z_map) or (not (x, y) in z_map and (x - 1, y) in z_map):
                            if 0 < y < height and 0 < x < width:
                                lst[int(y * width + x)] = struct.pack("BBB", *(0.0, 0.0, 0.0))
                    except:
                        pass
            for x, min_max in min_max_x.items():
                for y in range(min_max[0] - 1, min_max[1] + 2):
                    try:
                        if (not (x, y) in z_map and (x, y + 1) in z_map) or (not (x, y) in z_map and (x, y - 1) in z_map):
                            if 0 < y < height and 0 < x < width:
                                lst[(y * width + x)] = struct.pack("BBB", *(0.0, 0.0, 0.0))
                    except:
                            pass

        out.write("".join(lst))
        return out

## UTILITY FUNCTIONS


# updates the max and min of a current collection of polygons
def update_max_min(self):
    global max_x, max_y, max_z
    global min_x, min_y, min_z
    if self.x < min_x:
        min_x = self.x
    if self.x > max_x:
        max_x = self.x
    if self.y < min_y:
        min_y = self.y
    if self.y > max_y:
        max_y = self.y
    if self.z < min_z:
        min_z = self.z
    if self.z > max_z:
        max_z = self.z


def get_min_z():
    return max_z


def get_scale():
    return max(
        CANVAS_WIDTH / (max_x - min_x) / 3,
        CANVAS_HEIGHT / (max_y - min_y) / 3,
        CANVAS_HEIGHT / (max_z - min_z) / 3)


def get_origin():
    return Vector3D(((max_x - min_x) / 2) + min_x,
            ((max_y - min_y) / 2) + min_y,
            ((max_z - min_z) / 2) + min_z)


def get_inverse_origin():
    origin = get_origin()
    return Vector3D(-origin.x, -origin.y, -origin.z)


def reset_max_min():
    global max_x, max_y, max_z
    global min_x, min_y, min_z
    max_x = -1
    max_y = -1
    max_z = -1
    min_x = float('inf')
    min_y = float('inf')
    min_z = float('inf')
