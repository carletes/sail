import unittest
from math import degrees, fmod, radians, cos, sin, sqrt, pi

from nearestkey import nearest_key


class Boat():

    def __init__(self, position, compass, polars=None):
        self._position = position
        # want 0 <= compass < 360
        compass = fmod(compass, 360)
        if compass < 0:
            compass = 360 + compass
        self._theta = radians(compass)
        if polars is None:
            polars = {0: {0: 0}}
        self._polars = polars

    @property
    def position(self):
        return self._position

    @property
    def compass(self):
        return degrees(self._theta)

    def polars(self, windspeed, windangle):
        nearest_windspeed = nearest_key(self._polars, windspeed)
        nearest_windangle = nearest_key(self._polars[nearest_windspeed],
                                        windangle)
        return self._polars[nearest_windspeed][nearest_windangle]

    def move(self, distance):
        # TODO: check distance is positive, don't allow if not
        d_x = distance * sin(self._theta)
        d_y = distance * cos(self._theta)
        self._position = (self._position[0] + d_x, self._position[1] + d_y)

    def steer(self, degrees):
        # positive values for starboard, negative to port
        # no spinning allowed, let's limit turns to less than 360
        degrees = fmod(degrees, 360)
        # set new theta...
        # and make sure it is always positive and less than 2 * pi
        self._theta += radians(degrees)
        if self._theta >= 2 * pi:
            self._theta = fmod(self._theta, 2 * pi)
        if self._theta < 0:
            self._theta = 2 * pi + self._theta


class Environment():
    def __init__(self, wind):
        self._wind = wind

    @property
    def wind(self):
        return self._wind

    def get_wind(self, time, position):
        """
        given a time and position, return the windspeed and winddirection at
         at that location and time
        """
        # to start we're assuming constant windspeed 15 from the north
        # everywhere and all the time
        return (15, 0)


class BoatTest(unittest.TestCase):

    def test_create_boat(self):
        boat = Boat(position=(30, 30), compass=75)
        self.assertEqual(boat.position, (30, 30))
        self.assertEqual(boat.compass, 75)
        self.assertEqual(boat.polars(0, 0), 0)

    def test_move_boat(self):
        boat = Boat(position=(0, 0), compass=0)
        boat.move(10)
        self.assertAlmostEqual(boat.position[0], 0)
        self.assertAlmostEqual(boat.position[1], 10)

        boat.move(-10)
        self.assertAlmostEqual(boat.position[0], 0)
        self.assertAlmostEqual(boat.position[1], 0)

    def test_steer_boat(self):
        boat = Boat(position=(0, 0), compass=0)
        boat.steer(90)
        self.assertEqual(boat.compass, 90)
        boat.steer(-10)
        self.assertEqual(boat.compass, 80)
        boat.steer(20)
        self.assertEqual(boat.compass, 100)
        boat.steer(-180)
        self.assertEqual(boat.compass, 280)
        boat.steer(730)
        self.assertEqual(boat.compass, 290)

    def test_move_and_steer_boat(self):
        boat = Boat(position=(0, 0), compass=0)
        boat.steer(45)
        boat.move(sqrt(200))
        self.assertAlmostEqual(boat.position[0], 10)
        self.assertAlmostEqual(boat.position[1], 10)
        self.assertEqual(boat.compass, 45)

    def test_get_polars(self):
        boat = Boat(position=(0, 0), compass=0, polars={0: {0: 0, 15: 0,
                                                            30: 0, 180: 0},
                                                        5: {0: 0, 15: 0.8,
                                                            30: 1, 45: 1.5,
                                                            180: 3},
                                                        10: {0: 0, 15: 1.3,
                                                             30: 1.7, 180: 5},
                                                        15: {0: 0, 15: 2,
                                                             30: 3,
                                                             180: 10}})
        self.assertEqual(boat.polars(0, 0), 0)
        self.assertEqual(boat.polars(0, 180), 0)
        self.assertEqual(boat.polars(5, 180), 3)
        self.assertEqual(boat.polars(6, 30), 1)
        self.assertEqual(boat.polars(6, 170), 3)
        self.assertEqual(boat.polars(10, 180), 5)
        self.assertEqual(boat.polars(5, 170), 3)


class EnvironmentTest(unittest.TestCase):
    def test_create_Environment(self):
        environment = Environment(wind={})
        self.assertEqual(environment.wind, {})

    def test_get_wind(self):
        environment = Environment(wind={})
        self.assertEqual(environment.get_wind(time=0,
                                              position=(45, 67)), (15, 0))


def main():
    pass


if __name__ == '__main__':
    unittest.main()
