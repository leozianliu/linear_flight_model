import scipy.io
import numpy as np
from helper import *
import matplotlib.pyplot as plt
import Solver
import Aircraft
import citation_data
import unittest


class Test_Mass_Centroid(unittest.TestCase):
    def test_floats(self):
        ## Testing floats
        ac = Aircraft.Aircraft(citation_data.Data()[0], citation_data.Data()[1])

        test_cases = [
            {"time1": 9.0, "time2": 500, "int_fuel_lbs": 4100, "benji_pos": 200, "msg": "time1 took float", "raises": True},
            {"time1": 9, "time2": 500.0, "int_fuel_lbs": 4100, "benji_pos": 200, "msg": "time2 took float", "raises": True},
            {"time1": 9, "time2": 500, "int_fuel_lbs": 4100.0, "benji_pos": 200, "msg": "int_fuel_lbs didn\'t take float", "raises": False},
            {"time1": 9, "time2": 500, "int_fuel_lbs": 4100, "benji_pos": 200.0, "msg": "benji_pos didn\'t take float", "raises": False},
        ]

        for case in test_cases:
            with self.subTest(msg=case["msg"]): 
                if case['raises']:
                    with self.assertRaises(TypeError):
                        ac.mass_centroid(**{k:v for k,v in case.items() if k not in ["msg","raises"]})
                else:
                    try:
                        ac.mass_centroid(**{k:v for k,v in case.items() if k not in ["msg","raises"]})
                    except TypeError:
                        self.fail(case["msg"])


    def test_output_types(self):
        ## Testing if the "outputs'" type is corret

        ac = Aircraft.Aircraft(citation_data.Data()[0], citation_data.Data()[1])
        ac.mass_centroid(time1=9,time2=500,int_fuel_lbs=4100,benji_pos=200)

        self.assertIsInstance(ac.center_mass,float,msg='center_mass is not float')
        self.assertIsInstance(ac.x_cg,float,msg='x_cg is not float')
        self.assertIsInstance(ac.x_cg_percent,float,msg='x_cg_percent is not float')
        
        
    def test_extreme_values(self):
        ## Testimg time interval
        ## Testing time1 can't be lower than 9 and time2 can't be higher than total flight time (5183.1 seconds but only till 5183 cuz integer only)
        ## Testing extreme values for int_fuel_lbs and benji_pos

        ac = Aircraft.Aircraft(citation_data.Data()[0], citation_data.Data()[1])

        test_cases = [
            {"time1": 8, "time2": 500, "int_fuel_lbs": 4100, "benji_pos": 200, "msg": "time1 was taken lower than 9"},
            {"time1": 9, "time2": 5184, "int_fuel_lbs": 4100, "benji_pos": 200, "msg": "time2 was taken above 5183"},
            {"time1": 9, "time2": 500, "int_fuel_lbs": 0, "msg": "int_fuel_lbs took 0"},
            {"time1": 9, "time2": 500, "int_fuel_lbs": -1, "msg": "int_fuel_lbs took negative weight"},
            {"time1": 9, "time2": 500, "int_fuel_lbs": 4100, "benji_pos": -1, "msg": "benji_pos is in front of plane"},
            {"time1": 9, "time2": 500, "int_fuel_lbs": 4100, "benji_pos": 575, "msg": "benji_pos is behind the plane"}
        ]
        
        for case in test_cases:
            with self.subTest(msg=case["msg"]):
                with self.assertRaises(ValueError):
                    ac.mass_centroid(**{k:v for k,v in case.items() if k!= "msg"})
        

    def test_calculation(self):
        ## Testing if the calculation is correct

        ac = Aircraft.Aircraft(citation_data.Data()[0], citation_data.Data()[1])

        test_cases = [
            {"time1": 9, "time2": 10, "int_fuel_lbs": 4100},
            {"time1": 9, "time2": 10, "int_fuel_lbs": 4100, "benji_pos": 200}
        ]


        for case in test_cases:
            ac.mass_centroid(**case)
            if "benji_pos" not in case:
                self.assertAlmostEqual(ac.center_mass,7.1368023612,msg="center_mass not almost equal for benji_pos=default, 288")
                self.assertAlmostEqual(ac.x_cg,0.4931783612,msg="x_cg not almost equal for benji_pos=default, 288")
                self.assertAlmostEqual(ac.x_cg_percent, 0.239768719602,msg="x_cg_percent not almost equal for benji_pos=default, 288")
            if "benji_pos" in case:
                self.assertAlmostEqual(ac.center_mass,7.10469476374,msg="center_mass not almost equal for benji_pos=200")
                self.assertAlmostEqual(ac.x_cg,0.46107076374,msg="x_cg not almost equal for benji_pos=200")
                self.assertAlmostEqual(ac.x_cg_percent, 0.224158956202,msg="x_cg_percent not almost equal for benji_pos=200")
