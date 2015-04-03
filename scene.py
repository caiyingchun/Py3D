from vector import Vector3D
from transforms import *
from config import *
from line import *
from Tkinter import *
import Image
import ImageTk
from tkFileDialog import asksaveasfilename
import numpy
from zbuffer import *


##
# The scene class is a very basic way of representing a 3D scenario,
# with a single 3D object, it manages a single transform that
# is applied to all its child polygons.
# It also manages a set of options that determine the look of each image rendered.
##
class Scene():

    def __init__(self, lightsources, polygons, canvas):
        self.canvas = canvas
        self.lightsources = lightsources
        self.combined_light = None
        self.polygons = polygons
        self.changed = True
        self.polymode = False
        self.wireframe = False
        self.draw_guides = True
        self.perspective = False
        self.gourad_shading = True
        self.gourad_color = False
        self.toon_shading = False
        self.specular_lighting = True
        self.set_to_base_state()
        self.calculate_scene_boundaries()
        self.init_guide_lines()
        self.get_pixel_list = get_z_buffered_pixels

    ##
    # Resets the scene orientation and base state back to its base state.
    ##
    def set_to_base_state(self):
        self.guidelines = set()
        self.allvertices = {}
        self.vertshading = {}
        self.x_rot = 0
        self.y_rot = 0
        self.z_rot = 0
        self.x_mov = 0
        self.y_mov = 0
        self.z_mov = 0
        self.transform = [[1.0, 0.0, 0.0, 0.0],
                          [0.0, 1.0, 0.0, 0.0],
                          [0.0, 0.0, 1.0, 0.0]]

    ##
    # Calculates the bounadries of a newly created scene.
    ##
    def calculate_scene_boundaries(self):
        reset_max_min()
        self.calculate_max_min()
        self.origin = get_origin()
        self.invorigin = get_inverse_origin()

    ##
    # Calculates the min, max combos of x, y and z for a set of polygons.
    ##
    def calculate_max_min(self):
        for idx, poly in numpy.ndenumerate(self.polygons):
            for v3d in poly.coords:
                update_max_min(v3d)

    ##
    # Draws the entire scene in the appropriate mode.
    ##
    def draw(self):
        if self.polymode:
            self.draw_polys()
        else:
            self.draw_pixels()

    ##
    # Initializes a set of 3D lines, for use in the polygon mode as X, Y and Z axis.
    ##
    def init_guide_lines(self):
        LINELENGTH = CANVAS_WIDTH ** 2
        self.guidelines.add((
            Line(Vector3D(-LINELENGTH, 0, 0), Vector3D(LINELENGTH, 0, 0)), "green"
            ))
        self.guidelines.add((
            Line(Vector3D(0, -LINELENGTH, 0), Vector3D(0, LINELENGTH, 0)), "red"
            ))

        self.guidelines.add((
            Line(Vector3D(0, 0, -LINELENGTH), Vector3D(0, 0, LINELENGTH)), "blue"
            ))

    ##
    # Calculates all vectors that share a space, and informs their parent polygons
    # of their neighbors
    ##
    def calculate_vector_neighbors(self):
        for vert, polygons in self.allvertices.items():
            for poly in polygons:
                poly.neighbors[vert] = ([item for item in polygons if not item is poly], len(polygons))

        for poly in self.polygons:
            # Precalculates shared color values.
            poly.calculate_shared_colors()

    ##
    # Forces hard change to guideline positions. (Not part of scene.transform)
    ##
    def set_lines(self, transform):
        for line, color in self.guidelines:
            line.set(transform)

    ##
    # Applies the current transform to the guidelines in the scene.
    ##
    def move_lines(self, transform):
        for line, color in self.guidelines:
            line.apply(transform)

    ##
    # Draws the guidelines if they are enabled
    ##
    def draw_lines(self):
        self.move_lines(self.transform)
        if self.draw_guides:
            for line, color in self.guidelines:
                line.draw(self.canvas, color)
        else:
            for line, color in self.guidelines:
                line.hide(self.canvas)

    ##
    # Toggles render mode, resets canvas and forces a redraw.
    ##
    def switch_render_mode(self):
        self.changed = True
        self.polymode = not self.polymode
        if self.polymode:
            self.canvas.delete(ALL)
            for polygon in self.polygons:
                polygon.exists = False
            for line, color in self.guidelines:
                line.exists = False

    ##
    # Recalculates all polygon positions based on current transform.
    # recalculates all surface normals.
    ##
    def update_scene_contents(self):
        transform = self.transform
        for polygon in self.polygons:
            polygon.coords = [vec.apply(transform) for vec in polygon.base_state]
            polygon.calculate_surface_normal()

    ##
    #   Draws all pixels to the canvas in interpolated mode.
    ##
    def draw_pixels(self):
        if self.changed:
            self.update_scene_contents()
            pixel_list = self.get_pixel_list(self)
            piximg = Image.fromstring("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), pixel_list.getvalue())
            self.cimg = ImageTk.PhotoImage(piximg)
            self.canvas.img = self.canvas.create_image(0, 0, image=self.cimg, anchor=NW)
            self.changed = False

    ##
    #   Creates a high-resolution image of the current scene, and saves a slightly smaller antialiased
    #   version of the scene to a file chosen by the user.
    ##
    def save_image(self):
        w, h = self.scale_by(4)
        self.update_scene_contents()
        pixels = self.get_pixel_list(self, offset=(1.5, 1.5), baseimage=HIRES_IMAGE, width=w, height=h)
        piximg = Image.fromstring("RGB", (w, h), pixels.getvalue())
        self.scale_by(0.25)
        filename = asksaveasfilename()
        piximg = piximg.resize((CANVAS_WIDTH * 2, CANVAS_HEIGHT * 2), Image.ANTIALIAS)
        if filename is not None:
            piximg.save(filename, "JPEG", quality=95)

    ##
    # Scales all items in a scene by a multiple
    ##
    def scale_by(self, amount):
        w = int(CANVAS_WIDTH * amount)
        h = int(CANVAS_HEIGHT * amount)
        self.snap_to_position()
        self.update_transform(Transform.scale(Vector3D(amount, amount, amount)))
        self.snap_to_origin()
        return w, h

    ##
    # Draws entire scene as a collection of single-color polygons (faster than interpolated mode)
    ##
    def draw_polys(self):
        if self.changed:
            self.draw_lines()
            trans = self.transform
            wireframe = self.wireframe
            combinedLight = self.combined_light
            for polygon in self.polygons:
                polygon.coords = [vec.apply(trans) for vec in polygon.base_state]
                polygon.calculate_surface_normal()
                polygon.draw(wireframe, combinedLight, self)

            self.changed = False

    ##
    # Updates the current transform applied to the scene
    # with the input transform.
    ##
    def update_transform(self, transform):
        self.transform = Transform.compose(self.transform, transform)
        self.changed = True
        self.polygons.sort(key=sort_by_z)

    ## OPTION TOGGLES:
    def switch_perspective_mode(self):
        self.perspective = not self.perspective
        self.changed = True

    def switch_wireframe_mode(self):
        self.wireframe = not self.wireframe
        self.changed = True

    def switch_shading_mode(self):
        self.gourad_shading = not self.gourad_shading
        self.changed = True

    def switch_toon_shading(self):
        self.toon_shading = not self.toon_shading
        self.changed = True

    def switch_color_mode(self):
        self.gourad_color = not self.gourad_color
        self.changed = True

    def switch_specular(self):
        self.specular_lighting = not self.specular_lighting
        self.changed = True

    def snap_to_position(self):
        self.update_transform(Transform.translation(self.origin))

    def snap_to_origin(self):
        self.update_transform(Transform.translation(self.invorigin))


def sort_by_z(polygon):
    return polygon.get_average_z()
