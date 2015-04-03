from vector import *
from config import *


##
# A class to represent a polygon in 3D space, with multiple methods of rendering.
##
class Polygon:

    def __init__(self, parent, coords, color):
        self.camera_z = CAMERA_Z
        self.coords = coords
        self.base_state = self.coords[:]
        self.color = color
        self.parent = parent
        self.polygon_exists = False
        self.colorNormals = None
        self.neighbors = {}
        self.calculate_surface_normal()
        self.color_tuple = (self.color.x, self.color.y, self.color.z)

    ##
    # Returns a list of x,y values for each vertex in this polygon
    ##
    def get_x_y(self, perspective):
        return sum([[v.x, v.y] for v in self.coord_tuple(perspective)], [])

    ##
    # Returns the coordinages of the polygon, if perspective is set to true,
    # it applies perspective to each coordinate based on the CAMERA_Z and
    # the midpoint of the canvas.
    ##
    def coord_tuple(self, perspective):
        if not perspective:
            return self.coords
        else:
            coords = self.coords[:]

            for coord in self.coords:
                depth = self.camera_z / coord.z if coord.z != self.camera_z else 1
                mids = CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2
                coord.x = (coord.x - mids[0]) * depth + mids[0]
                coord.y = (coord.y - mids[1]) * depth + mids[1]
            return coords

    ##
    # Draws the shape straight onto the Canvas as single-color, filled polygon shapes.
    # Fast but simplistic. See "Pixels" for the interpolated drawing
    ##
    def draw(self, wireframe, light, scene):
        rgb = self.parent.rgb()
        if self.surfaceNormal.z <= 0 or scene.wireframe or scene.perspective:
            outline, fill = WIREFRAME_COLORS if scene.wireframe else ("", '#%02x%02x%02x' % tuple(self.getRGB(rgb, self.color_tuple, light * self.surfaceNormal, 0)))

            if(self.polygon_exists):
                self.parent.coords(self.polygon_exists, *self.get_x_y(scene.perspective))
                self.parent.itemconfig(self.polygon_exists, fill=fill, outline=outline, width=1)
                self.parent.tag_raise(self.polygon_exists)
            else:
                self.polygon_exists = self.parent.create_polygon(*self.get_x_y(scene.perspective), fill=fill, outline=outline, width=1, smooth=0)
        else:
            if self.polygon_exists:
                self.parent.delete(self.polygon_exists)
                self.polygon_exists = False

    ##
    # Re-calculates the polygons surface normal.
    ##
    def calculate_surface_normal(self):
        self.surfaceNormal = ((self.coords[1] - self.coords[0]) ** (self.coords[2] - self.coords[1])).unit_vector()

    ##
    # Finds the average z-index, of a polygon (used to z-buffer entire polygons when we are not in interpolated mode)
    ##
    def get_average_z(self):
        count = 0
        total = 0
        for coord in self.coords:
            count += 1
            total += coord.z
        averageZ = -(total / count)

        if self.surfaceNormal.z > 0:
            averageZ -= 100000
        return averageZ

    ##
    # Returns a generator for all pixels in this polygon.
    # Or an empty array if the shape isn't visible (surfaceNormal >= 0)
    ##
    def pixels(self, lights, scene):
        self.calculate_costh(lights)
        if self.surfaceNormal.z < 0:
            return self.interpolate_pixels(lights, scene)
        return []

    ##
    # Calculates an average color for each of this shapes vertices,
    # depends on the vertex colors of each of its neighbors.
    ##
    def calculate_shared_colors(self):
        idof = self.base_state.index
        for vec, (polys, poly_len) in self.neighbors.items():

            idx = idof(vec)

            color = self.color
            for poly in polys:
                color = color + poly.color
            color = color / poly_len
            self.coords[idx].col = color

    ##
    # Calculates an average costh and specular lighting variables for each of this shapes vertices,
    # depends on the vertex colors of each of its neighbors.
    ##
    def calculate_costh(self, lights):
        idof = self.base_state.index
        coords = self.coords
        for vec, (polys, poly_len) in self.neighbors.items():
            tot_normal = 0
            tot_spec = 0
            idx = idof(vec)
            for indx, light in lights.items():
                halfangle = (light + VIEW_ANGLE).unit_vector()
                normal = self.surfaceNormal.average(polys, poly_len)
                blinnTerm = halfangle * normal
                if(tot_normal > 0 and blinnTerm < 0):
                    continue
                tot_normal += normal * light
                tot_spec += min(max(0.01, blinnTerm), 1) ** self.parent.shinyness
            coords[idx].cn = tot_normal
            coords[idx].spec = tot_spec

    ##
    # This function is a generator of pixel values, for this polygon.
    # Yields an x,y postion, a z-value and a color for each pixel.
    ##
    def interpolate_pixels(self,  light, scene):

        edgelist = self.compute_edge_lists(scene.perspective)

        rgb = self.parent.rgb()
        toon = scene.toon_shading

        # Step through the edgelist along our y-axis.
        for y, edge1, edge2 in edgelist:

            # Extract variables we calculated in our compute_edge_lists function.
            (x1, z1, cn1, spec1, (r1, g1, b1)) = edge1
            (x2, z2, cn2, spec2, (r2, g2, b2)) = edge2

            xDiff, xRangeIs0 = x2 - x1, x2 <= x1

            # # Calculate slopes for:
            # # Z,   Shading,   R, G, B
            slopeZ, slopeN, slopeSpec, slopeR, slopeG, slopeB = map(
                                                lambda v: (v[0] - v[1]) / xDiff if not xRangeIs0 else 0,
                                                [(z2, z1), (cn2, cn1), (spec2, spec1), (r2, r1), (g2, g1), (b2, b1)]
                                                )

            # # Step from left edge to right and interpolate
            # # Z, shading, and color for each step
            for x in xrange(int(round(x1)), int(round(x2))):

                # Interpolated values. value = value + slope (for each step)
                z1 += slopeZ
                cn1 += slopeN
                spec1 += slopeSpec
                r1 += slopeR
                g1 += slopeG
                b1 += slopeB

                # If we arent using gourad shading, we dont use the interpolated shading value
                snormal = cn1 if scene.gourad_shading else self.surfaceNormal * light.items()[0][1]

                # If we aren't using gourad colors dont use interpolated color value
                color_tup = (r1, g1, b1) if scene.gourad_color else self.color_tuple
                spec1 = spec1 if scene.specular_lighting else 0

                # set the colors in our RGB calculation array.
                rgb[0][3] = color_tup[0]
                rgb[1][3] = color_tup[1]
                rgb[2][3] = color_tup[2]

                # posterize output if toon-shading is enabled.
                if toon:
                    snormal = round(snormal / .3) * 0.3
                    spec1 = round(spec1 / .3) * 0.3

                # Yield our generated pixel.
                yield [[x, y, z1], [
                max(min(255, (diffuse_color * light_intensity * snormal) + (specular_color * light_intensity * spec1) + (diffuse_color * ambient_intensity)), 0) for light_intensity, specular_color, ambient_intensity, diffuse_color in rgb
                ]]

    ##
    # This function calculates the edge_lists, for this polygon.
    # Finds left and right values for the color normal, specular lighting constant,
    # RGB values, and X and Z coordinates.
    ##
    def compute_edge_lists(self, perspective):

        # Grad each vertex sorted by y.
        min_y, mid_y, max_y = sorted(self.coord_tuple(perspective), key=lambda coord: coord.y)
        edgeList = {}

        # Loop through our edges, from min to max.
        for va, vb in [[min_y, mid_y], [min_y, max_y], [mid_y, max_y]]:

            if vb.y > va.y:
                div = (vb.y - va.y)
                mx = (vb.x - va.x) / div
                mcn = (vb.cn - va.cn) / div
                mspec = (vb.spec - va.spec) / div
                mz = (vb.z - va.z) / div
                mr = (vb.col.x - va.col.x) / div
                mg = (vb.col.y - va.col.y) / div
                mb = (vb.col.z - va.col.z) / div
            else:
                mx = 0
                mcn = 0
                mspec = 0
                mz = 0
                mr = 0
                mg = 0
                mb = 0

            x = va.x
            z = va.z
            cn = va.cn
            spec = va.spec
            col = va.col
            r = col.x
            g = col.y
            b = col.z
            i = int(round(va.y))
            maxi = int(round(vb.y))

            for i in xrange(i, maxi):

                try:
                    # When we have two values (left, right) we can yield our calculated edges.
                    if edgeList[i][0][0] > x:
                        yield i, (x, z, cn, spec, (r, g, b)), edgeList[i][0]
                    else:
                        yield i, edgeList[i][0], (x, z, cn, spec, (r, g, b))
                except:
                    # Otherwise add to edgelist and keep going.
                    edgeList[i] = [(x, z, cn, spec, (r, g, b))]
                x += mx
                z += mz
                r += mr
                g += mg
                b += mb
                cn += mcn
                spec += mspec

    ##
    # Nice formatting for debugging purposes.
    ##
    def __repr__(self):
        return """\nPolygon:
        Coords:   %s
        color: %s""" % (self.coords, self.color)

    ##
    # Apply a transform to each vertex in the polygon.
    ##
    def apply(self, transform):
        for idx, vec in enumerate(self.base_state):
            self.coords[idx] = vec.apply(transform)
        self.surfaceNormal = self.getSurfaceNormal()

    ##
    # Calculate RGB value, given an array of ambient light, intensity and specular values, and a color.
    ##
    def getRGB(self, rgb, color, costh, spec):
        rgb[0][3] = color[0]
        rgb[1][3] = color[1]
        rgb[2][3] = color[2]

        return [
               max(0, min(255, (diffuse_color * light_intensity * costh) + (specular_color * light_intensity * spec) + (diffuse_color * ambient_intensity))) for light_intensity, specular_color, ambient_intensity, diffuse_color in rgb
                ]
