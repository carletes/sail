import unittest
from math import degrees, fmod, radians, cos, sin, sqrt
from coords import nav_to_math, math_to_nav

class Boat():
    def __init__(self, position, compass):
        self._position = position
        compass = fmod(compass, 360)
        self._theta = radians(nav_to_math(compass))

    @property
    def theta(self):
        return self._theta

    @property
    def position(self):
        return self._position

    @property
    def compass(self):
        return math_to_nav(degrees(self._theta))

    def move(self,distance):
        # TODO: check distance is positive, don't allow if not
        d_x = distance * cos(self._theta)
        d_y = distance * sin(self._theta)
        self._position = (self._position[0] + d_x, self._position[1] + d_y)

    def steer(self,degrees):
        # positive values for starboard, negative to port
        # no spinning allowed, let's limit turns to less than 360
        degrees = fmod(degrees, 360)
        # set new theta...
        self._theta -= radians(degrees)

class BoatTest(unittest.TestCase):
    def test_create_boat(self):
        boat = Boat(position=(30,30), compass=75)
        self.assertEqual(boat.position,(30,30))
        self.assertEqual(boat.compass, 75)

    def test_move_boat(self):
        boat = Boat(position=(0,0), compass=0)
        boat.move(10)
        self.assertAlmostEqual(boat.position[0],0)
        self.assertAlmostEqual(boat.position[1],10)

        boat.move(-10)
        self.assertAlmostEqual(boat.position[0],0)
        self.assertAlmostEqual(boat.position[1],0)        

    def test_steer_boat(self):
        boat = Boat(position=(0,0), compass=0)
        boat.steer(90)
        self.assertEqual(boat.compass, 90)
        self.assertEqual(degrees(boat.theta), 0)
        boat.steer(-10)
        self.assertEqual(boat.compass,80)
        self.assertEqual(degrees(boat.theta), 10)
        boat.steer(20)
        self.assertEqual(boat.compass,100)
        self.assertEqual(fmod(degrees(boat.theta),360), -10)
        boat.steer(-180)
        self.assertEqual(boat.compass,280)
        self.assertEqual(fmod(degrees(boat.theta),360), 170)
        boat.steer(730)
        self.assertEqual(boat.compass,290)
        # next one off by .00000000000003 for some reason
        self.assertAlmostEqual(fmod(degrees(boat.theta),360), 160)

    def test_move_and_steer_boat(self):
        boat = Boat(position=(0,0), compass=0)
        boat.steer(45)
        boat.move(sqrt(200))
        self.assertAlmostEqual(boat.position[0],10)        
        self.assertAlmostEqual(boat.position[1],10)        
        self.assertEqual(boat.compass,45)

    

def main():
    pass



if __name__ == '__main__':
    unittest.main()
