import unittest
from math import degrees, fmod, radians, cos, sin, sqrt

class Boat():
    def __init__(self, position, compass):
        self._position = position
        self._theta = -radians(270 + compass)

    @property
    def position(self):
        return self._position

    @property
    def compass(self):
        return abs(fmod(degrees(self._theta) + 270, 360))

    def move(self,distance):
        d_x = distance * cos(self._theta)
        d_y = distance * sin(self._theta)
        self._position = (self._position[0] + d_x, self._position[1] + d_y)

    def steer(self,degrees):
        # positive values for starboard, negative to port
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
        boat.steer(10)
        self.assertEqual(boat.compass,100)
        boat.steer(-20)
        self.assertEqual(boat.compass,80)

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
