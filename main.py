import unittest
from math import radians, cos, sin

class Boat():
    def __init__(self, position, compass):
        self._position = position
        self._compass = compass

    @property
    def position(self):
        return self._position

    @property
    def compass(self):
        return self._compass

    def move(self,distance):
        theta = radians(self._compass + 90)
        d_x = distance * cos(theta)
        d_y = distance * sin(theta)
        self._position = (self._position[0] + d_x, self._position[1] + d_y)

class BoatTest(unittest.TestCase):
    def test_create_boat(self):
        boat = Boat(position=(30,30), compass=75)
        self.assertEqual(boat.position,(30,30))
        self.assertEqual(boat.compass, 75)

    def test_move_boat(self):
        boat = Boat(position=(0,0), compass= 0)
        boat.move(10)
        self.assertAlmostEqual(boat.position[0],0)
        self.assertAlmostEqual(boat.position[1],10)

        boat.move(-10)
        self.assertAlmostEqual(boat.position[0],0)
        self.assertAlmostEqual(boat.position[1],0)        

        
def main():
    pass



if __name__ == '__main__':
    unittest.main()
