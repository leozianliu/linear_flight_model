#unit test for curve_calc
import unittest
import numpy as np
from helper4tests import *
from calculate_aero_curves_from_data import curve_calc
from thrust import Thrust

class TestCurve_calc(unittest.TestCase):
   
    
    def test_cl_data_type(self):
        data = get_test_data()
        n=11
        t=np.linspace(0,1000,n,dtype=int)
        intervals= np.array([[int(t[i]),int(t[i+1])] for i in range(n-1)])
        calc = curve_calc()
        calc.ac.S=25
        print(f'alt = {data[4][t[0]]},\n mach = {data[6]},\n T = {data[5]},\n mfleft = {data[7][t[0]]})')
        cl_curve = calc.cl_data(data, intervals)
        shape = np.shape(cl_curve)
        #print the data driving the Thrust calculations
        

        #checl if the output is a numpy array of shape (n-1,2)
        self.assertEqual(shape,(n-1,2),msg=f'shape = {shape} != {(n-1,2)} = {(n-1,2)}')
'''
    def test_cl_data_out_correctness(self):
        data = get_test_data()
        #real Cl values
        n=11
        cl = np.linspace(-1.2,1.5,n)
        aoa = np.linspace(-10,10,n)
        t=np.linspace(0,1000,n,dtype=int)
        intervals= np.array([[int(t[i]),int(t[i+1])] for i in range(n-1)])
        calc = curve_calc()

        cl_curve = calc.cl_data(data, intervals)
        for i in range(len( intervals)):
            self.assertAlmostEqual(cl_curve[i][1],cl[i], msg=f'cl_curve[{i}][1] = {cl_curve[i][1]} != {cl[i]} = cl[{i}]')
            self.assertAlmostEqual(cl_curve[i][0],aoa[i], msg=f'cl_curve[{i}][0] = {cl_curve[i][0]} != {aoa[i]} = aoa[{i}]')

        
    def test_cd_data_type(self):
        data = get_test_data()
        n=10
        t=np.linspace(0,1000,n,dtype=int)
        intervals= np.array([[int(t[i]),int(t[i+1])] for i in range(n-1)])
        calc = curve_calc()
        
        cl_curve = calc.cl_data(data, intervals)
        shape = np.shape(cl_curve)
        #checl if the output is a numpy array of shape (n-1,2)
        self.assertEqual(shape,(n-1,2),msg=f'shape = {shape} != {(n-1,2)} = {(n-1,2)}')
    def test_cd_output_correctness(self):
        #Assume thrust.py is correct 
        data = get_test_data()
        #real Cd values
        n=11

        S=25
        aoa = np.linspace(-10,10,n)
        aoa = 1 + aoa[:-1]
        rho = data[2]
        tas = data[3]
        t=np.linspace(0,1000,n,dtype=int)
        intervals= np.array([[int(t[i]),int(t[i+1])] for i in range(n-1)])
        t1 = (t[:-1]+int((1000/(n-1))/2))

        input1 = lambda i: {'pressure_altitude':data[4][t1[i]],'M':np.mean(data[6][intervals[i,0]:intervals[i,1]]),'DT':data[5][t1[i]]-273.15,'m_f_dot':data[7][t1[i]]} 
        input2 = lambda i: {'pressure_altitude':data[4][t1[i]],'M':np.mean(data[6][intervals[i,0]:intervals[i,1]]),'DT':data[5][t1[i]]-273.15,'m_f_dot':data[7][t1[i]]}
        thrust = np.array([Thrust.compute(**input1(i)) + Thrust.compute(**input2(i)) for i in range(n)])
        cd = 2 * np.cos(np.deg2rad(aoa)) * thrust / (rho[0]* np.array([np.mean(tas[i[0]:i[1]]) for i in intervals])**2 * S)
        calc = curve_calc()

        cd_curve = calc.cd_data(data, intervals)
        for i in range(len( intervals)):
            self.assertAlmostEqual(cd_curve[i][1],cd[i], msg=f'cd_curve[{i}][1] = {cd_curve[i][1]} != {cd[i]} = cd[{i}]')
            self.assertAlmostEqual(cd_curve[i][0],aoa[i], msg=f'cd_curve[{i}][0] = {cd_curve[i][0]} != {aoa[i]} = aoa[{i}]')




    
    def test_cm_data(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)
    def test_cl_cd(self):
        pass
    def test_cl2_cd(self):
        pass
     '''   
if __name__ == '__main__':
    unittest.main()