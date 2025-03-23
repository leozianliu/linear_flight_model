import sys
sys.path.append(r'C:\Users\pauli\FlightDynamicsGit\B01') # Replace with your own path so you can use .py files from other directories
sys.path.append(r'C:\Users\pauli\FlightDynamicsGit\B01\tools') # Replace with your own path so you can use .py files from other directories
sys.path.append(r'C:\Users\pauli\FlightDynamicsGit\B01\parameters') # Replace with your own path so you can use .py files from other directories


import Aircraft
import math
import citation_data
from thrust import *
import scipy as sp
import numpy as np
from helper import *
import matplotlib.pyplot as plt


data_dir = "data_ref_2025/FTISxprt-20250304_084412.mat"
amp = 0
period = 0

class datacurve_calc:

    def __init__(self):

        # [10,11] is a filler to obtain static values from citation_data, this program does not use time dependent coefficients from aircraft.py
        self.ac = Aircraft.Aircraft([1000,1001] , citation_data.Data()[0], citation_data.Data()[1])

    def damped_oscillation(self, characteristic_data, interval):
        data_slice = characteristic_data[interval[0]:interval[1]]
        t = np.linspace(0, interval[1] - interval[0], 1476)
        peaks = sp.signal.find_peaks(data_slice)
        avg_zero = (characteristic_data[interval[0]] + characteristic_data[interval[1]]) / 2
        print(peaks)
        avg_period = (peaks[0][-1]-peaks[0][0])/(len(peaks[0])-1)
        global amp
        amp = characteristic_data[interval[0]+peaks[0][0]] - avg_zero
        global period 
        period = avg_period

        damp_exp_regressant = sp.optimize.curve_fit(damp_model_curve_wrapper, t, data_slice)
        print(damp_exp_regressant)

def damp_model_curve_wrapper(inp, tc):  # assumes begin at peak, so pure cosine may be used
    return damp_model_curve(inp, tc, amp, period)

def damp_model_curve(inp, tc, amp, period):  # assumes begin at peak, so pure cosine may be used
    return amp * np.exp(inp / tc) * np.cos(inp / (period * 2 * np.pi)) 

        
 


PLOT=True

# Load the .mat file
data = sp.io.loadmat(data_dir)

# Accessing a struct field
flightdata = data['flightdata']  # This gives a numpy structured array

#Time series
time_series = np.asarray(flightdata['time'][0][0][0][0][0].flatten())

#Plotting altitude
Dadc1_bcAlt = np.asarray(flightdata['Dadc1_bcAlt'][0][0][0][0][0].flatten()) # Baro-corrected altitude (ft)



#Define the interval of the phugoid motion
phugoid_interval = np.array([31812, 33288])

#Define the interval of the short form motion
shortpitch_interval = np.array([31168, 31239])

#Define the interval of the spiral dive
spiraldive_interval = np.array([37601, 39365])

#Define the interval of the Dutch Roll (without yaw damper)
dutchroll_interval = np.array([34233, 34492])

#Define the interval of the aperiodic roll
aperiodicroll_interval = np.array([35937, 36011])


thingy = datacurve_calc() 

thingy.damped_oscillation(Dadc1_bcAlt, phugoid_interval)


#Now we find the halftime and and period, starting with the period to ensure the halftime calculation is non-trivial

                            
