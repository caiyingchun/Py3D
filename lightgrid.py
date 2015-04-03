from Tkinter import *
from config import *
from vector import *


###
# The master canvas is an extension of the Canvas class that maintain a ruccrent specular color,
# ambient intensity, light intensity and shinyness of its child object.
# It can be queried at any time for an RGB structure that holds values for each of these variables
###
class MasterCanvas(Canvas):

    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        self.specular_color = Vector3D(255, 255, 255)
        self.ambient_intens = Vector3D(0.8, 0.8, 0.8)
        self.light_intens = 0.5
        self.shinyness = 20

    ###
    #    Queries the master canvas for its variables of its current state in specular color,
    #    ambient intensity, light intensity and shinyness of its child object.
    ###
    def rgb(self):
        return    [
        [LIGHT_INTENSITY_MULTIPLIER * self.light_intens * self.specular_color.x, self.specular_color.x, self.ambient_intens.x, None],
        [LIGHT_INTENSITY_MULTIPLIER * self.light_intens * self.specular_color.y, self.specular_color.y, self.ambient_intens.y, None],
        [LIGHT_INTENSITY_MULTIPLIER * self.light_intens * self.specular_color.z, self.specular_color.z, self.ambient_intens.z, None]
        ]


##
# The LightsCanvas is an interacive canvas of small ovals that represent the lights in the current scene.
# They can be dragged around to reposition the lights, and right-clicked to remove.
# Clicking on the canvas anywhere creates a new light.
# Since the Canvas is 2D and the scene is 3D a empty lambda is added to this class
# which can be coupled with a slider to adjust a lights Z-value.
##
class LightsCanvas(Canvas):

    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, height=CANVAS_HEIGHT / 2, width=CANVAS_WIDTH / 2, bg="lightgray")
        self.set_dimensions()
        self.add_axis()
        self.lights = {}
        self.sum_of_lights = None
        self.scene = None
        self.changeActive = lambda x: x
        self.bind("<Button-1>", self.click)
        self.bind("<Button-2>", self.remove)
        self.bind("<B1-Motion>", self.drag)
        self.bg = LIGHTS_GRID_BG_COLOR

    # Draws x, y axis.
    def add_axis(self):
        self.create_line(0, self.mid[1], self.width, self.mid[1])
        self.create_line(self.mid[0], 0, self.mid[0], self.height)

    # Sets canvas dimensions
    def set_dimensions(self):
        self.height = CANVAS_HEIGHT / 2
        self.width = CANVAS_WIDTH / 2
        self.mid = (self.width / 2, self.height / 2)
        self.x_size = self.height / LIGHTS_GRID_Y_MULT
        self.y_size = self.width / LIGHTS_GRID_X_MULT

    # Resets canvas state.
    def clear(self):
        self.delete(ALL)
        self.create_line(0, self.mid[1], self.width, self.mid[1])
        self.create_line(self.mid[0], 0, self.mid[0], self.height)
        self.sum_of_lights = None
        self.scene = None
        self.lights = {}

    # Removes a light when clicked
    def remove(self, event):
        try:
            clicked = self.find_withtag(CURRENT)[0]
            if clicked in self.lights:
                del self.lights[clicked]
                self.delete(clicked)
                self.calculate_combined_light()
                if self.scene is not None:
                    self.scene.changed = True
        except Exception as f:
            print f
            pass

    # Selects a light, or adds one if a blank area was clicked.
    def click(self, event):
        try:
            clicked = self.find_withtag(CURRENT)[0]
            if clicked in self.lights:
                self.set_active(self.find_withtag(CURRENT)[0])
        except:
            x, y = self.convert_to_real_units(event.x, event.y)
            new_light = Vector3D(x, y, -0.75)
            self.add_light(new_light)
            self.calculate_combined_light()

    # Repositions a light in the scene
    def drag(self, event):
        global active
        self.coords(active, event.x, event.y, event.x + LIGHTS_GRID_NODE_SIZE, event.y + LIGHTS_GRID_NODE_SIZE)
        active_light = self.lights[active]
        active_light.x, active_light.y = self.convert_to_real_units(event.x, event.y)
        self.calculate_combined_light()

    # Adds a light to the scene.
    def add_light(self, light):
        global active
        coords_oval = map(int, (self.mid[0] + light.x * self.x_size, self.mid[1] + light.y * self.y_size))
        coords_oval = self.add_light_to_canvas(coords_oval)
        self.lights[coords_oval] = light
        self.set_active(coords_oval)

    # A method that can be called by an external entity to adjust a lights Z value.
    def adjust_z(self, val):
        global active
        active_light = self.lights[active]
        active_light.z = float(val)
        self.calculate_combined_light()

    # Sets a light to be the active light.
    def set_active(self, oval):
        global active
        active = oval
        for oval, light in self.lights.items():
            self.itemconfig(oval, fill="green")
        self.itemconfig(active, fill="red")
        self.changeActive(self.lights[active])

    # Adds the oval representation of the light to the canvas.
    def add_light_to_canvas(self, coords):
        return self.create_oval(coords[0], coords[1], coords[0] + LIGHTS_GRID_NODE_SIZE, coords[1] + LIGHTS_GRID_NODE_SIZE, fill="green")

    # Calculates a fake light to represent the current lights in the scene.
    # This is used for accelerated rendering in the simple polygon (Non interpolated) rendering mode.
    def calculate_combined_light(self):
        x = 0
        y = 0
        z = 0
        for oval, light in self.lights.items():
            x += light.x
            y += light.y
            z += light.z

        self.sum_of_lights.x = x
        self.sum_of_lights.y = y
        self.sum_of_lights.z = z

        if self.scene is not None:
            self.scene.changed = True

    def get_combined_light(self):
        if self.sum_of_lights == None:
            self.sum_of_lights = Vector3D(0, 0, 0)
        self.calculate_combined_light()
        return self.sum_of_lights

    # Converts canvas units to scene units.
    def convert_to_real_units(self, x, y):
        return (x - self.mid[0]) / self.x_size, (y - self.mid[0]) / self.x_size

    # Converts scene units to canvas units.
    def convert_to_canvas_units(self, x, y):
        return (self.mid[0] + x * self.x_size, self.mid[1] + y * self.y_size)
