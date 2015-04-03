from vector import Vector3D
import struct
import sys as sys
sys.setcheckinterval(10000)

# Globals vars
canvas = None
scene = None
lightsgrid = None
origin = None
invorigin = None
guidelines = []


# Inital scene bounds
max_x = -1
max_y = -1
max_z = -1
min_x = float('inf')
min_y = float('inf')
min_z = float('inf')

# Global constants
CANVAS_WIDTH = 280
CANVAS_HEIGHT = 280
DRAW_GUIDE_LINES = True
CAMERA_Z = 1000
LIGHTS_GRID_BG_COLOR = 'lightgray'

LIGHTS_GRID_X_MULT = 5.
LIGHTS_GRID_Y_MULT = 5.
LIGHTS_GRID_NODE_SIZE = 10

LIGHT_INTENSITY_MULTIPLIER = 1.5 / 255
INITIAL_Z_OFFSET = 600
WIREFRAME_COLORS = ('#%02x%02x%02x' % (33, 33, 33), '')
VIEW_ANGLE = Vector3D(0, 0, -0.5)


BASE_IMAGE = [struct.pack("BBB", 60, 60, 60)] * CANVAS_WIDTH * CANVAS_HEIGHT
HIRES_IMAGE = [struct.pack("BBB", 60, 60, 60)] * CANVAS_WIDTH * CANVAS_HEIGHT * 16
