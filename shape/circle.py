from math import dist


class Circle:
    def __init__(self, centre, radius):
        self.centre = centre
        self.radius = radius

    def __contains__(self, arg):
        if max(0, self.radius-dist(self.centre, arg)):
            return True
        else:
            return False
