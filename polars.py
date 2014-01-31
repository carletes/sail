import unittest
import csv
from math import cos, radians
from nearestkey import nearest_key

def read_polars_from_file(file):
    """
    """
    p = {}
    tbs = {}
    optimalangles = {}

    reader = csv.reader(open(file),delimiter='\t')
    for row in reader:
        if reader.line_num == 1:
            header = row
            h = {}
            for i in range(3,(len(header)-2)):
                header[i]=float(header[i])
                for i, v in enumerate(header):
                    h[v] = i
        else:
            rd = {}
            roa = {}
            wv = float(row[0])
            for i in h.keys():
                if isinstance(i,float):
                    rd[i] = float(row[h[i]])
            rd[float(row[h['TWAOU']])] = float(row[h['TBSOU']])
            rd[float(row[h['TWAOD']])] = float(row[h['TBSOD']])
            roa = {'upwind':float(row[h['TWAOU']]), 'downwind':float(row[h['TWAOD']])}
            tbs[wv] = rd
            optimalangles[wv] = roa

    p['tbs'] = tbs
    p['optimalangles'] = optimalangles
    return p

class ReadPolarsFromFileTest(unittest.TestCase):
    def test_read_polars(self):
        p = read_polars_from_file('minimal_polars.txt')
        self.assertEqual(p['tbs'][10.0][32.0], 4.81)
        self.assertEqual(p['tbs'][10.0][41.3], 5.45)
        self.assertEqual(p['tbs'][10.0][159.3], 5.26)
        self.assertEqual(p['tbs'][10.0][180], 5.05)
        self.assertEqual(p['tbs'][20.0][32], 5.07)
        self.assertEqual(p['tbs'][20.0][37.8], 5.7)
        self.assertEqual(p['tbs'][20.0][174], 7.02)
        self.assertEqual(p['tbs'][20.0][180], 6.72)
        self.assertEqual(p['optimalangles'][10.0]['upwind'], 41.3)
        self.assertEqual(p['optimalangles'][20.0]['upwind'], 37.8)
        self.assertEqual(p['optimalangles'][10.0]['downwind'], 159.3)
        self.assertEqual(p['optimalangles'][20.0]['downwind'], 174)

class Polars():

    def __init__(self, tbs = None, optimalangles = None):
        if tbs is None:
            tbs = {0: {0: 0}}
        self._tbs = tbs
        if optimalangles is None:
            optimalangles = {0: {'upwind': 0, 'downwind': 0}}
        self._optimalangles = optimalangles


    def target_boatspeed(self, windspeed, windangle):
        nearest_windspeed = nearest_key(self._tbs, windspeed)
        nearest_windangle = nearest_key(
            self._tbs[nearest_windspeed], windangle)
        return self._tbs[nearest_windspeed][nearest_windangle]

    def optimal_angle(self, windspeed, direction):
        nearest_windspeed = nearest_key(self._optimalangles, windspeed)
        return self._optimalangles[nearest_windspeed][direction]

    def vmg(self, windspeed, windangle):
        return cos(radians(windangle))* \
                   self.target_boatspeed(windspeed, windangle)

class PolarsTest(unittest.TestCase):

    def test_create_polars(self):
        polars = Polars()
        self.assertEqual(polars.target_boatspeed(0, 0), 0)

    def test_polars_methods(self):
        p = read_polars_from_file('minimal_polars.txt')
        polars = Polars(tbs=p['tbs'],optimalangles=p['optimalangles'])
        self.assertEqual(polars.target_boatspeed(10.0, 32.0), 4.81)
        self.assertEqual(polars.target_boatspeed(10.0, 41.3), 5.45)
        self.assertEqual(polars.target_boatspeed(10.0, 159.3), 5.26)
        self.assertEqual(polars.target_boatspeed(10.0, 180), 5.05)
        self.assertEqual(polars.target_boatspeed(20.0, 32), 5.07)
        self.assertEqual(polars.target_boatspeed(20.0, 37.8), 5.7)
        self.assertEqual(polars.target_boatspeed(20.0, 174), 7.02)
        self.assertEqual(polars.target_boatspeed(20.0, 180), 6.72)
        self.assertEqual(polars.optimal_angle(10.0, 'upwind'), 41.3)
        self.assertEqual(polars.optimal_angle(20.0, 'upwind'), 37.8)
        self.assertEqual(polars.optimal_angle(10.0, 'downwind'), 159.3)
        self.assertEqual(polars.optimal_angle(20.0, 'downwind'), 174)
        self.assertAlmostEqual(polars.vmg(10,41.3),4.094390, places=6)
        self.assertAlmostEqual(polars.vmg(20,180),-6.72)


def main():
    pass


if __name__ == '__main__':
    unittest.main()
