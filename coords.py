import unittest
from math import fmod

def math_to_nav(degrees):
    if abs(degrees) >= 360:
        degrees = fmod(degrees, 360)
    if degrees < 0:
        degrees = 360 + degrees
    if degrees >= 0 and degrees <= 90:
        result = 90 - degrees
    elif degrees > 90 and degrees < 360:
        result = 450 - degrees
    return result

def nav_to_math(degrees):
    return math_to_nav(degrees)
    
class FunctionTest(unittest.TestCase):
    def test_math_to_nav(self):
        self.assertEqual(math_to_nav(0),90)
        self.assertEqual(math_to_nav(45),45)
        self.assertEqual(math_to_nav(90),0)
        self.assertEqual(math_to_nav(135),315)
        self.assertEqual(math_to_nav(180),270)
        self.assertEqual(math_to_nav(225),225)
        self.assertEqual(math_to_nav(270),180)
        self.assertEqual(math_to_nav(315),135)
        self.assertEqual(math_to_nav(360),90)
        self.assertEqual(math_to_nav(370),80)
        self.assertEqual(math_to_nav(-370),100)

    def test_nav_to_math(self):
        self.assertEqual(nav_to_math(0),90)
        self.assertEqual(nav_to_math(45),45)
        self.assertEqual(nav_to_math(90),0)
        self.assertEqual(nav_to_math(135),315)
        self.assertEqual(nav_to_math(180),270)
        self.assertEqual(nav_to_math(225),225)
        self.assertEqual(nav_to_math(270),180)
        self.assertEqual(nav_to_math(315),135)
        self.assertEqual(nav_to_math(360),90)
        self.assertEqual(nav_to_math(370),80)
        self.assertEqual(nav_to_math(-370),100)



def main():
    pass

if __name__ == '__main__':
    unittest.main()
