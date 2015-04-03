<link href="http://fonts.googleapis.com/css?family=Pontano+Sans" rel="stylesheet" type="text/css">
<link href="http://fonts.googleapis.com/css?family=Ropa+Sans" rel="stylesheet" type="text/css">
<link href="file:///Volumes/Storage/Study/COMP%20261/3D/data/markdown.css" rel="stylesheet"></link>
### Assignment 3 ###

### How To Run:
Cd to the directory that contains the source files, and launch main.py with python

    cd /path/to/3D
    python main.py

### Prerequisites

The GUI automatically loads the monkey.txt model upon start from ./data/monkey.txt. Ensure this model stays present and in that directory

### Implementation

The 3D image generator was implemented with a GUI that allows maximum customization of the scene before the image is generated.
##### Key GUI Features
* Allows you to load models
* Allows you to export images
* Has two visual modes (Fast polygon mode, and high-quality interpolated mode.)
* Provides extensive controls to manipulate the scene, including:
    * X,Y and Z Rotation and Translation
    * Allows you to create, remove and adjust of lights, light color, intensity and ambient light levels.
    * Allows you to adjust the reflectivity of the models surface.
    * Allows you to toggle Specular lighting, Gourad Shading, Interpolated Colors and Toon Shading
    * Provides you with x,y,z guidelines and a wireframe mode in the Polygon view mode.
    * Allows you to toggle rendering the scene with/without perspective.


#### Limitations
* The Viewer distance used in the Perspective calculation is not adjustable (Allowing this made it too easy to loose the model)
* Wireframe and guidelines are only available in Polygon mode
* Rendering is quite wasteful and not managed terribly efficiently. All possible lighting, shading and coloring values are interpolated on every
scene update, regardless of whether they are enabled. 

<br/>
<br/>
<br/>

### How to use:
<div style="float: left;" style="width: 206px;"><img src="file:///Volumes/Storage/Study/COMP%20261/3D/data/tk.jpg" style="width: 620px;"></img>
<p style="text-align: center; font-style:italic; width: 206px;">Key UI Elements</p></div>
<div style="clear: both;"></div>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>

# Extensions and Results
## Diffuse and Specular Lighting
First I implemented Gourad shading and specular lighting, the gourad shading allowed the lighting to appear much smoother, the specular lighting
makes the image appear more real.
<div style="float: left;" style="width: 206px;"><img src="file:///Volumes/Storage/Study/COMP%20261/3D/data/ball-rough.jpg" style="width: 206px;"></img>
<p style="text-align: center; font-style:italic; width: 206px;">Base Case</p></div>
<div style="float: left;" style="width: 206px;"><img src="file:///Volumes/Storage/Study/COMP%20261/3D/data/ball-smooth.jpg" style="width: 206px;"></img>
<p style="text-align: center; font-style:italic; width: 206px;">Base Case with Gourad Shading</p></div>
<div style="float: left;" style="width: 206px;"><img src="file:///Volumes/Storage/Study/COMP%20261/3D/data/shiny-textured-ball.jpg" style="width: 206px;"></img>
<p style="text-align: center; font-style:italic; width: 206px;">Base Case with Gourad Shading and Specular Lighting</p></div>
<div style="clear: both;"></div>
To make the ball seem even smoother I added an option to also interpolate colors, which makes the different colored polygons of the ball less apparent.

Multiple lights, and coloring of the light source are also added options.
<div style="float: left;" style="width: 206px;"><img src="file:///Volumes/Storage/Study/COMP%20261/3D/data/shiny-ball.jpg" style="width: 206px;"></img>
<p style="text-align: center; font-style:italic; width: 206px;">+Interpolated Coloring</p></div>
<div style="float: left;" style="width: 206px;"><img src="file:///Volumes/Storage/Study/COMP%20261/3D/data/red-light-ball.jpg" style="width: 206px;"></img>
<p style="text-align: center; font-style:italic; width: 206px;">+Alternate Lighting Colors</p></div>
<div style="float: left;" style="width: 206px;"><img src="file:///Volumes/Storage/Study/COMP%20261/3D/data/double-shiny.jpg" style="width: 206px;"></img>
<p style="text-align: center; font-style:italic; width: 206px;">+Multiple Lights</p></div>
<div style="clear: both;"></div>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
### Perspective
I added an option to render with perspective. This gives a much better sense of depth and distance of an object and means that translating
along the z-axis when both the y and x axis are perfectly aligned still provides meaningful differences to the resulting image.

<div style="float: left;" style="width: 206px;"><img src="file:///Volumes/Storage/Study/COMP%20261/3D/data/monkey.jpg" style="width: 206px;"></img>
<p style="text-align: center; font-style:italic; width: 206px;">No Perspective</p></div>
<div style="float: left;" style="width: 206px;"><img src="file:///Volumes/Storage/Study/COMP%20261/3D/data/monkeypers.jpg" style="width: 206px;"></img>
<p style="text-align: center; font-style:italic; width: 206px;">With Perspective</p></div>
<div style="clear: both;"></div>
<div style="float: left;" style="width: 206px;"><img src="file:///Volumes/Storage/Study/COMP%20261/3D/data/ogre.jpg" style="width: 206px;"></img>
<p style="text-align: center; font-style:italic; width: 206px;">No Perspective</p></div>
<div style="float: left;" style="width: 206px;"><img src="file:///Volumes/Storage/Study/COMP%20261/3D/data/ogrepers.jpg" style="width: 206px;"></img>
<p style="text-align: center; font-style:italic; width: 206px;">With Perspective</p></div>
<div style="clear: both;"></div>


### Real Time Lighting + Multiple Lights:
The lights in the scene update in real-time as you drag them around, or adjust the z-slider. 
<div style="float: left;" style="width: 103px;"><img src="file:///Volumes/Storage/Study/COMP%20261/3D/data/1.png" style="width: 103px;"></img>
<p style="text-align: center; font-style:italic; width: 103px;"></p></div>
<div style="float: left;" style="width: 103px;"><img src="file:///Volumes/Storage/Study/COMP%20261/3D/data/2.png" style="width: 103px;"></img>
<p style="text-align: center; font-style:italic; width: 103px;"></p></div>
<div style="float: left;" style="width: 103px;"><img src="file:///Volumes/Storage/Study/COMP%20261/3D/data/3.png" style="width: 103px;"></img>
<p style="text-align: center; font-style:italic; width: 103px;"></p></div>
<div style="float: left;" style="width: 103px;"><img src="file:///Volumes/Storage/Study/COMP%20261/3D/data/4.png" style="width: 103px;"></img>
<p style="text-align: center; font-style:italic; width: 103px;"></p></div>
<div style="float: left;" style="width: 103px;"><img src="file:///Volumes/Storage/Study/COMP%20261/3D/data/5.png" style="width: 103px;"></img>
<p style="text-align: center; font-style:italic; width: 103px;"></p></div>
<div style="float: left;" style="width: 103px;"><img src="file:///Volumes/Storage/Study/COMP%20261/3D/data/6.png" style="width: 103px;"></img>
<p style="text-align: center; font-style:italic; width: 103px;"></p></div>
<br/>


### Toon Shading and Light Colors
Just for fun I also added "Toon shading", which I implemented by:

* forcing the shading to be posterized by rounding all shading values to within 0.3
* Upon rendering calculating all the edges of the resultant image and rendering a black-outline around it.

Aswell as the intensity of the light, color can also be adjusted. This affects both the reflected specular light aswell as the tone
of any light vectors. Ambient light is not affected.

The magnitude of how much specular light affects the model is determined by both the light-intensity and the shinyness of the model.
Both of these values can be adjusted in the GUI.
<div style="float: left;" style="width: 206px;"><img src="file:///Volumes/Storage/Study/COMP%20261/3D/data/toonmonkey.jpg" style="width: 206px;"></img>
<p style="text-align: center; font-style:italic; width: 206px;">Toon Shading</p></div>
<div style="float: left;" style="width: 206px;"><img src="file:///Volumes/Storage/Study/COMP%20261/3D/data/toon2ogre.jpg" style="width: 206px;"></img>
<p style="text-align: center; font-style:italic; width: 206px;">Toon Shading</p></div>
<div style="float: left;" style="width: 206px;"><img src="file:///Volumes/Storage/Study/COMP%20261/3D/data/scaryogre.jpg" style="width: 206px;"></img>
<p style="text-align: center; font-style:italic; width: 206px;">Toon Shading &amp; Colored Lighting</p></div>
<div style="clear: both;"></div>
<div style="float: left;" style="width: 206px;"><img src="file:///Volumes/Storage/Study/COMP%20261/3D/data/sad-monkey.jpg" style="width: 206px;"></img>
<p style="text-align: center; font-style:italic; width: 206px;">Toon Shading &amp; Colored Lighting</p></div>
<div style="float: left;" style="width: 206px;"><img src="file:///Volumes/Storage/Study/COMP%20261/3D/data/nightogre.jpg" style="width: 206px;"></img>
<p style="text-align: center; font-style:italic; width: 206px;">Colored Lighting</p></div>
<div style="float: left;" style="width: 206px;"><img src="file:///Volumes/Storage/Study/COMP%20261/3D/data/bright-lights.jpg" style="width: 206px;"></img>
<p style="text-align: center; font-style:italic; width: 206px;">High Intensity Lighting</p></div>
<div style="clear: both;"></div>
<div style="float: left;" style="width: 206px;"><img src="file:///Volumes/Storage/Study/COMP%20261/3D/data/plaincolor.jpg" style="width: 206px;"></img>
<p style="text-align: center; font-style:italic; width: 206px;">Plain Coloring</p></div>
<div style="float: left;" style="width: 206px;"><img src="file:///Volumes/Storage/Study/COMP%20261/3D/data/gouradcoloring.jpg" style="width: 206px;"></img>
<p style="text-align: center; font-style:italic; width: 206px;">Interpolated Coloring</p></div>
<div style="float: left;" style="width: 206px;"><img src="file:///Volumes/Storage/Study/COMP%20261/3D/data/aaon.png" style="width: 206px;  height:206px;"></img>
<p style="text-align: center; font-style:italic; width: 206px;">Saved images are Anti Aliased</p></div>
<div style="float: left;" style="width: 206px;"><img src="file:///Volumes/Storage/Study/COMP%20261/3D/data/ogre-hires.jpg" style="width: 206px;  height:206px;"></img>
<p style="text-align: center; font-style:italic; width: 206px;">Saved images are of Higher Resolution</p></div>
<div style="float: left;" style="width: 206px;"><img src="file:///Volumes/Storage/Study/COMP%20261/3D/data/pmode1.png" style="width: 206px;  height:206px;"></img>
<p style="text-align: center; font-style:italic; width: 206px;">Polygon mode shows guidelines and wireframe</p></div>
<div style="float: left;" style="width: 206px;"><img src="file:///Volumes/Storage/Study/COMP%20261/3D/data/pmode2.png" style="width: 206px;  height:206px;"></img>
<p style="text-align: center; font-style:italic; width: 206px;">Sacrifices nice shading for simple shadows and speed</p></div>

<div style="clear: both;"></div>