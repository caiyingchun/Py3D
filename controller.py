from transforms import *
from vector import *
from tkColorChooser import *


##
# Rotate object in center of screen by offset amount along x axis.
# Translates to origin and back to ensure object looks as if it rotates around its own origin
##
def rotate_x(val):
    global scene, origin, invorigin
    val = float(val)
    offset = val - scene.x_rot
    scene.x_rot = val
    snap_to_origin()
    scene.update_transform(Transform.x_rotate(offset))
    snap_to_position()


##
# Rotate object in center of screen by offset amount along y axis.
# Translates to origin and back to ensure object looks as if it rotates around its own origin
##
def rotate_y(val):
    global scene, origin, invorigin
    val = float(val)
    offset = val - scene.y_rot
    scene.y_rot = val
    snap_to_origin()
    scene.update_transform(Transform.y_rotate(offset))
    snap_to_position()


##
# Rotate object in center of screen by offset amount along z axis.
# Translates to origin and back to ensure object looks as if it rotates around its own origin
##
def rotate_z(val):
    global scene, origin, invorigin
    val = float(val)
    offset = val - scene.z_rot
    scene.z_rot = val
    snap_to_origin()
    scene.update_transform(Transform.z_rotate(offset))
    snap_to_position()


##
# Tell scene to toggle between polygon and interpolated mode
##
def switch_render_mode():
    global scene
    scene.switch_render_mode()


##
# Sets the current ambient light level
##
def set_ambient_light(value):
    global canvas, scene
    value = float(value) + 0.29
    canvas.ambient_intens = Vector3D(value, value, value)
    scene.changed = True


##
# Sets the current directed light strength
##
def set_light_strength(value):
    global canvas, scene
    value = float(value) + 0.69
    canvas.light_intens = value
    scene.changed = True


##
# Adjusts the directed light color
##
def choose_light_col():
    global canvas
    col = Vector3D(*askcolor()[0])
    canvas.specular_color = col
    scene.changed = True


##
#  Adjusts the ambient light color.
##
def choose_amb_col():
    global canvas
    col = Vector3D(*askcolor()[0])
    canvas.ambient_intens = col / 255
    scene.changed = True


##
# Adjusts object shinyness
##
def set_shinyness(value):
    global canvas, scene
    value = float(value) + 52
    canvas.shinyness = value
    scene.changed = True


##
# Toggles wireframe mode.
##
def switch_wireframe():
    global scene
    scene.switch_wireframe_mode()


##
# Toggles perspective mode
##
def switch_perspective():
    global scene
    scene.switch_perspective_mode()


##
# Toggles gourad shading
##
def toggle_gshading():
    global scene
    scene.switch_shading_mode()


##
# toggles toon shading
##
def toggle_tshading():
    global scene
    scene.switch_toon_shading()


##
# Toggles specular shading
##
def toggle_specular():
    global scene
    scene.switch_specular()


##
# Toggles interpolated coloring
##
def toggle_gcolor():
    global scene
    scene.switch_color_mode()


##
# toggles guidelines
##
def toggle_guides():
    global scene
    scene.draw_guides = not scene.draw_guides
    scene.changed = True


##
# Generates hi-res image of current scene
##
def generate_image():
    global scene
    scene.save_image()


##
# Snaps scene to origin (0, 0)
##
def snap_to_origin():
    scene.update_transform(Transform.translation(scene.origin))


##
# Returns object to its original offset position.
##
def snap_to_position():
    scene.update_transform(Transform.translation(scene.invorigin))


##
# Moves scene along the x-axis
##
def mov_x(val):
    global scene, origin, invorigin
    val = float(val)
    offset = float(val - scene.x_mov)
    scene.x_mov = val
    scene.update_transform(
        Transform.translation(Vector3D(offset, 0, 0))
    )


##
# Moves scene along the y-axis
##
def mov_y(val):
    global scene, origin, invorigin
    val = float(val)
    offset = float(val - scene.y_mov)
    scene.y_mov = val
    scene.update_transform(
        Transform.translation(Vector3D(0, offset, 0))
    )


##
# Moves scene along the z-axis
##
def mov_z(val):
    global scene, origin, invorigin
    val = float(val)
    offset = float(val - scene.z_mov)
    scene.z_mov = val
    scene.update_transform(
        Transform.translation(Vector3D(0, 0, offset))
        )
