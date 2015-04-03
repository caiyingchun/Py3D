

##
# A Class to reresent a line in 3D space,
# maintains two 3D points, as 3D Vectors.
##
class Line:

    def __init__(self, p1, p2):
        self.origin = (p1, p2)
        self.p1 = p1
        self.p2 = p2
        self.exists = False

    # Redraws the line (creates it first if non-existant)
    def draw(self, parent, color):
        if self.exists:
            parent.coords(self.exists, self.p1.x, self.p1.y, self.p2.x, self.p2.y)
        else:
            self.exists = parent.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=color)

    # Applies a transformation to our 3D line.
    def apply(self, transform):
        self.p1 = self.origin[0].apply(transform)
        self.p2 = self.origin[1].apply(transform)

    # Makes a permanent transform
    def set(self, transform):
        self.origin = (self.origin[0].apply(transform), self.origin[1].apply(transform))

    # Removes the line from the canvas.
    def hide(self, parent):
        if self.exists:
            parent.delete(self.exists)
            self.exists = False
