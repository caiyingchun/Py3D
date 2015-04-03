from Tkinter import *
from config import *
from main import *
from lightgrid import *


##
# Attempt to refresh screen at 20 FPS
##
def redraw():
    draw()
    root.after(int(1000. / 20.), redraw)


##
# Reset GUI and load new 3D object.
##
def load_new():
    lights_overlay.clear()
    load()
    checkbox_perspective.deselect()
    checkbox_guidelines.select()
    checkbox_wireframe_mode.deselect()
    checkbox_interp_colors.deselect()
    checkbox_gourad_shading.select()
    checkbox_wireframe_mode.deselect()
    checkbox_toonshading.deselect()
    checkbox_specular_lighting.select()
    if label_render_mode.poly:
        label_render_mode.config(text="Current Mode : Interpolated")
        set_interpolated_state(NORMAL)
        set_poly_mode_state(DISABLED)
        label_render_mode.poly = False


##
# Sets the Z of the selected light
##
def set_selected_light_z(active):
    light_z_index.set(active.z)


##
# Toggles Render mode between interpolated mode (high quality), and polygon mode (fast)
##
def changed_render_mode():
    switch_render_mode()
    if label_render_mode.poly:
        label_render_mode.config(text="Current Mode : Interpolated")
        set_interpolated_state(NORMAL)
        set_poly_mode_state(DISABLED)
    else:
        label_render_mode.config(text="Current Mode : Polygon")
        set_interpolated_state(DISABLED)
        set_poly_mode_state(NORMAL)
    label_render_mode.poly = not label_render_mode.poly


##
# Quickly sets polygon mode checkboxes
##
def set_poly_mode_state(change):
    checkbox_guidelines.config(state=change)
    checkbox_wireframe_mode.config(state=change)


##
# Quickly sets interpolated mode checkboxes
##
def set_interpolated_state(change):
    checkbox_gourad_shading.config(state=change)
    checkbox_toonshading.config(state=change)
    checkbox_interp_colors.config(state=change)
    checkbox_specular_lighting.config(state=change)


#WINDOWS
master = Tk()

#FRAMES
root = Frame(master)
root.grid(row=0, column=0)

lights_frame = Frame(root)
lights_frame.grid(row=7, column=1)

buttonFrame = Frame(root, )
buttonFrame.grid(row=1, column=3, sticky=W)

light_grid_frame = Frame(root)
light_grid_frame.grid(row=7, column=3, sticky=NW)

canvas_block = Frame(light_grid_frame)
canvas_block.grid(row=0, column=0)

y_box = Frame(root)
y_box.grid(row=1, column=2)

z_box = Frame(root)
z_box.grid(row=1, column=0)

load_save = Frame(root)
load_save.grid(row=0, column=0, sticky=W)
colorButtons = Frame(lights_frame)
colorButtons.grid(row=7, column=0)

#SURFACES
canvas = MasterCanvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="darkgrey")
canvas.grid(row=1, column=1)
canvas.draw_guides = True
lights_overlay = LightsCanvas(canvas_block)
lights_overlay.grid(row=1, column=0, sticky=NW)

#LABELS
label_lights = Label(lights_frame, text="LIGHTS", pady=10)
label_lights.grid(row=0, column=0)
label_lights_adjustments = Label(light_grid_frame, justify=LEFT, text="Left Click to Add, Select or Move lights\nRight Click to remove lights\nUse z-slider to adjust z-value")
label_lights_adjustments.grid(row=1, column=0)
label_title = Label(root, justify=LEFT, text="Position the model using the sliders\n(Polygon mode is less detailed, but faster.)")
label_title.grid(row=0, column=1)
label_y = Label(root, text="Y (Rotate, Translate)")
label_y.grid(row=2, column=2)
label_z = Label(root, text="Z (Rotate, Translate)")
label_z.grid(row=2, column=0)
label_x_rotate = Label(root, text="X (Rotate)")
label_x_rotate.grid(row=2, column=1)
label_x_translate = Label(root, text="X (Translate)")
label_x_translate.grid(row=4, column=1)
label_render_mode = Label(root, text="Current Mode : Interpolated")
label_render_mode.grid(row=0, column=3, sticky=W)
label_render_mode.poly = False
label_toggle = Label(buttonFrame, text="EDITOR", pady=5)
label_toggle.grid(row=0, column=0, sticky=W)
label_polygon_mode = Label(buttonFrame, text="POLYGON MODE", pady=5)
label_polygon_mode.grid(row=2, column=0, sticky=W)
label_interpolated_mode = Label(buttonFrame, text="INTERPOLATED MODE", pady=5)
label_interpolated_mode.grid(row=5, column=0, sticky=W)
label_ambient = Label(lights_frame, text="Ambient Light Level")
label_ambient.grid(row=5, column=0)
label_lightstrength = Label(lights_frame, text="Light Strength")
label_lightstrength.grid(row=1, column=0)
label_shinyness = Label(lights_frame, text="Object Shinyness")
label_shinyness.grid(row=3, column=0)

#Sliders
light_z_index = Scale(canvas_block, from_=-2, to=2, command=lights_overlay.adjust_z,  resolution=0.02, length=CANVAS_HEIGHT / 2, width=13)
light_z_index.grid(row=1, column=1, sticky=NW)

y_rot_slider = Scale(y_box, from_=-10, to=10, command=rotate_y,  resolution=0.00002, length=CANVAS_HEIGHT, showvalue=False, width=13)
y_rot_slider.grid(row=0, column=0)
y_mov_slider = Scale(y_box, from_=-500, to=500, command=mov_y,  resolution=0.02, length=CANVAS_WIDTH, showvalue=False, width=13)
y_mov_slider.grid(row=0, column=1)

x_mov_slider = Scale(root, from_=-500, to=500, command=mov_x, orient=HORIZONTAL,  resolution=0.02, length=CANVAS_WIDTH, showvalue=False, width=13)
x_mov_slider.grid(row=5, column=1)
x_rot_slider = Scale(root, from_=-10, to=10, command=rotate_x, orient=HORIZONTAL,  resolution=0.00002, length=CANVAS_HEIGHT, showvalue=False, width=13)
x_rot_slider.grid(row=3, column=1)

z_rot_slider = Scale(z_box, from_=-10, to=10, command=rotate_z,  resolution=0.00002, length=CANVAS_HEIGHT, showvalue=False, width=13)
z_rot_slider.grid(row=0, column=0)
z_mov_slider = Scale(z_box, from_=0, to=5000, command=mov_z,  resolution=0.02, length=CANVAS_WIDTH, showvalue=False, width=13)
z_mov_slider.grid(row=0, column=1)

scale_ambient = Scale(lights_frame, from_=-0.7, to=0.7, command=set_ambient_light, orient=HORIZONTAL,  resolution=0.02, length=CANVAS_WIDTH, showvalue=False, width=13)
scale_ambient.grid(row=6, column=0)

scale_level = Scale(lights_frame, from_=-0.7, to=0.7, command=set_light_strength, orient=HORIZONTAL,  resolution=0.02, length=CANVAS_HEIGHT, showvalue=False, width=13)
scale_level.grid(row=2, column=0)

scale_level = Scale(lights_frame, from_=50, to=-50, command=set_shinyness, orient=HORIZONTAL,  resolution=0.02, length=CANVAS_HEIGHT, showvalue=False, width=13)
scale_level.grid(row=4, column=0)

#Buttons
button_switch_mode = Button(root, text="Switch Mode", command=changed_render_mode)
button_switch_mode.mode = False
button_switch_mode.grid(row=0, column=2, sticky=W)
button_load = Button(load_save, text="Load Model", command=load_new)
button_load.grid(row=0, column=0, sticky=W)
button_generate = Button(load_save, text="Save As Image", command=generate_image)
button_generate.grid(row=1, column=0, sticky=W)
button_choose_color = Button(colorButtons, text="Choose Light Color", command=choose_light_col)
button_choose_color.grid(row=0, column=0, sticky=W)

#Checkbuttons
checkbox_perspective = Checkbutton(buttonFrame, text="Toggle Perspective", command=switch_perspective)
checkbox_perspective.grid(row=1, column=0, sticky=W)
checkbox_guidelines = Checkbutton(buttonFrame, text="Toggle Guidelines", command=toggle_guides, state=DISABLED)
checkbox_guidelines.grid(row=3, column=0, sticky=W)
checkbox_guidelines.select()
checkbox_wireframe_mode = Checkbutton(buttonFrame, text="Toggle Wireframe", command=switch_wireframe, state=DISABLED)
checkbox_wireframe_mode.grid(row=4, column=0, sticky=W)
checkbox_gourad_shading = Checkbutton(buttonFrame, text="Gourad Shading", command=toggle_gshading)
checkbox_gourad_shading.grid(row=6, column=0, sticky=W)
checkbox_gourad_shading.select()
checkbox_interp_colors = Checkbutton(buttonFrame, text="Interpolated Colors", command=toggle_gcolor)
checkbox_interp_colors.grid(row=7, column=0, sticky=W)
checkbox_toonshading = Checkbutton(buttonFrame, text="Toon Shading", command=toggle_tshading)
checkbox_toonshading.grid(row=8, column=0, sticky=W)
checkbox_specular_lighting = Checkbutton(buttonFrame, text="Specular Lighting", command=toggle_specular)
checkbox_specular_lighting.grid(row=9, column=0, sticky=W)
checkbox_specular_lighting.select()


lights_overlay.changeActive = set_selected_light_z

main(canvas, lights_overlay)
redraw()

# Start!
root.mainloop()
