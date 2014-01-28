import logging
import unittest

from math import degrees, fmod, radians, cos, sin, pi, sqrt
from nearestkey import nearest_key


class Boat():

    log = logging.getLogger("Boat")

    def __init__(self, position, compass, polars):
        self._position = position
        # want 0 <= compass < 360
        compass = fmod(compass, 360)
        if compass < 0:
            compass = 360 + compass
        self._theta = radians(compass)
        self._polars = polars

    @property
    def position(self):
        return self._position

    @property
    def compass(self):
        return degrees(self._theta)

    @property
    def theta(self):
        return self._theta

    def polars(self, windspeed, windangle):
        nearest_windspeed = nearest_key(self._polars,windspeed)
        nearest_windangle = nearest_key(self._polars[nearest_windspeed],windangle)
        return self._polars[nearest_windspeed][nearest_windangle]

    def move(self, d_x, d_y):
        new_position = (self._position[0] + d_x, self._position[1] + d_y)
        self.log.debug("move(): Moving from %s to %s",
                       self._position, new_position)
        self._position = new_position

    def steer(self,degrees):
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

class BoatTest(unittest.TestCase):
    def test_create_boat(self):
        boat = Boat(position=(30,30), compass=75, polars={0:{0:0}})
        self.assertEqual(boat.position,(30,30))
        self.assertEqual(boat.compass, 75)
        self.assertEqual(boat.polars(0,0),0)

    def test_steer_boat(self):
        boat = Boat(position=(0,0), compass=0, polars={0:{0:0}})
        boat.steer(90)
        self.assertEqual(boat.compass, 90)
        boat.steer(-10)
        self.assertEqual(boat.compass,80)
        boat.steer(20)
        self.assertEqual(boat.compass,100)
        boat.steer(-180)
        self.assertEqual(boat.compass,280)
        boat.steer(730)
        self.assertEqual(boat.compass,290)

    def test_get_polars(self):
        boat = Boat(position=(0,0), compass=0, polars={0:{0:0,15:0,30:0,180:0},5:{0:0,15:0.8,30:1,45:1.5,180:3},10:{0:0,15:1.3,30:1.7,180:5},15:{0:0,15:2,30:3,180:10}})
        self.assertEqual(boat.polars(0,0),0)
        self.assertEqual(boat.polars(0,180),0)
        self.assertEqual(boat.polars(5,180),3)
        self.assertEqual(boat.polars(6,30),1)
        self.assertEqual(boat.polars(6,170),3)
        self.assertEqual(boat.polars(10,180),5)
        self.assertEqual(boat.polars(5,170),3)


class Force(object):

    """Base class of things that make a boat move."""

    def effect(self, boat, t):
        """Applies this force to a boat at a given point in time.

        Returns the effect, expressed as a vector ``(x, y)``, of applying this
        force. Each component of the return value represents the number of
        units to move in each axis.

        """
        raise NotImplementedError()


class Engine(Force):

    log = logging.getLogger("Engine")

    def __init__(self, k):
        """Initialise an engine with an arbitrary constant, representing the
        magnitude of its effect vector.

        """
        # TODO: Pass an initial amount of fuel to the constructor.
        self.k = k

    def effect(self, boat, t):
        theta = boat.theta
        self.log.debug("effect(%g): Theta: %g", self.k, theta)
        # TODO: Use a non-arbitrary speed, take into account remaining
        # fuel, ...
        ret = (self.k * sin(theta), self.k * cos(theta))
        self.log.debug("effect(%g): Moving to (%s, %s)", self.k, ret[0], ret[1])
        return ret


class Wind(Force):

    def __init__(self):
        # TODO: Pass the path to a GRIB file with the values for the ``u`` and
        # ``v`` components of the wind.
        pass

    def effect(self, boat, t):
        x, y = boat.position
        u, v = self.wind_at(x, y, t)
        # TODO: Take into account the polars of the boat, and perhaps also the
        # boat's compass. For now we just return an arbitrary multiple of the
        # wind components.
        #
        # Also take in to account any other factor (polars?) that you might
        # think of!
        return (0.42 * u, 0.42 * v)

    def wind_at(self, x, y, t):
        """Returns the ``u`` and ``v`` components of the wind at coordinates
        ``(x, y)``.

        """
        # TODO: Use data from a GRIB file instead.
        return (10, 10)


def move(boat, forces, t):
    """Move a boat at a given point in time, taking into account all the
    forces acting upon it.

    """
    new_x, new_y = 0, 0
    for (d_x, d_y) in (f.effect(boat, t) for f in forces):
        new_x += d_x
        new_y += d_y
    boat.move(new_x, new_y)


class MoveTest(unittest.TestCase):

    def test_engine(self):
        boat = Boat(position=(0,0), compass=0, polars={0:{0:0}})
        engine = Engine(10)
        move(boat, [engine], 0)
        self.assertAlmostEqual(boat.position[0],0)
        self.assertAlmostEqual(boat.position[1],10)

        engine = Engine(-10)
        move(boat, [engine], 0)
        self.assertAlmostEqual(boat.position[0],0)
        self.assertAlmostEqual(boat.position[1],0)

        engine = Engine(sqrt(200))
        boat = Boat(position=(0,0), compass=0, polars={0:{0:0}})
        boat.steer(45)
        move(boat, [engine], 0)
        self.assertAlmostEqual(boat.position[0],10)
        self.assertAlmostEqual(boat.position[1],10)
        self.assertEqual(boat.compass,45)

    def test_wind(self):
        # TODO: Implement!
        pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s %(name)s %(message)s")
    unittest.main()
