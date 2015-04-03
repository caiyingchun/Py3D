from polygon import Polygon
from scene import *
from vector import *
from config import *
from tkFileDialog import askopenfilename
from Tkinter import ALL
import controller as controller
from vectorlist import VectorList
from controller import *


##
# Parses a line of text into a polygon(triangle), with a color,
# appends the polygon to a dictionairy that maps vertices to polygons
# for gourad-shading.
##
def parse_triangle(line, vectors):
    polygon_data = line.split()

    coords = map(float, polygon_data[0:-3])
    coords = [Vector3D(*coords[i:i + 3]) for i in range(0, len(coords), 3)]

    pos = Vector3D(*map(float, polygon_data[-3:]))
    poly = Polygon(controller.canvas, coords, pos)

    # Keep track of polygons that share common vectors (for gourad-shading.)
    for idx, item in numpy.ndenumerate(poly.coords):
            vectors[Vector3D(item.x, item.y, item.z)].append(poly)

    return poly


##
# Loads a new 3D raw file for presentation in the program.
##
def load(filename=None):

    # Reset the canvas.
    controller.canvas.delete(ALL)

    if(filename is None):
        filename = askopenfilename()

    f = open(filename)

    # List of polygons in shape
    polys = []

    # Keep track of vertices and which polygons they share.
    all_vertices = VectorList()

    # Parse initial lighting for the scene.
    light_vec3 = map(float, f.readline().split())

    # Parse all polyons in the file
    for line in f:
        polys.append(parse_triangle(line, all_vertices))

    # Create scene and lights grid object.
    controller.lightsgrid.add_light(Vector3D(*light_vec3))
    controller.scene = Scene(controller.lightsgrid.lights, polys, controller.canvas)
    controller.lightsgrid.scene = controller.scene

    #Discover scene bounds, position object in front of view screen.
    scale = get_scale()
    mov_z(get_min_z() + INITIAL_Z_OFFSET)

    # Initialize scene.
    controller.scene.combined_light = controller.lightsgrid.get_combined_light()
    controller.scene.allvertices = all_vertices
    controller.scene.z_mov = 0
    controller.scene.update_transform(Transform.scale(Vector3D(scale, scale, scale)))
    controller.scene.update_transform(Transform.translation(Vector3D((CANVAS_WIDTH / 2) / scale, (CANVAS_HEIGHT / 2) / scale, 0) + controller.scene.invorigin))
    controller.scene.set_lines(Transform.translation(controller.scene.origin))
    controller.scene.calculate_vector_neighbors()


##
# First launch, load monkey!
##
def main(cnv, lightscnv):
    controller.lightsgrid = lightscnv
    controller.canvas = cnv
    load("data/monkey.txt")


##
# Redraw.
##
def draw():
    controller.scene.draw()


if __name__ == "__main__":
    from gui import *
