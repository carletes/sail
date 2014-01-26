import unittest


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


class BoatTest(unittest.TestCase):
    def test_create_boat(self):
        boat = Boat(position=(30,30), compass=75)
        self.assertEqual(boat.position,(30,30))
        self.assertEqual(boat.compass, 75)

def main():
    pass



if __name__ == '__main__':
    unittest.main()
