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


class datacurve_calc:

    def __init__(self):

        # [10,11] is a filler to obtain static values from citation_data, this program does not use time dependent coefficients from aircraft.py
        self.ac = Aircraft.Aircraft([1000,1001] , citation_data.Data()[0], citation_data.Data()[1])

    def get_ac(self):
         return self.ac
        

    def damped_oscillation(self, characteristic_data, interval):
        data_slice = characteristic_data[interval[0]:interval[1]]
        t = np.linspace(0, interval[1] - interval[0] - 1, interval[1] - interval[0])
        global avg_zero
        avg_zero = (data_slice[0] + data_slice[-1]) / 2
        data_slice = data_slice - avg_zero
        damp_exp_regressant = sp.optimize.curve_fit(damp_model_curve, t, data_slice)

        plt.plot(t, data_slice)
        plt.plot(t, damp_model_curve(t, 
                                     damp_exp_regressant[0][0],
                                     damp_exp_regressant[0][1], 
                                     damp_exp_regressant[0][2], 
                                     damp_exp_regressant[0][3],
                                     damp_exp_regressant[0][4]))
        plt.show()
        return damp_exp_regressant[0][0], damp_exp_regressant[0][3]

    def non_oscillatory_motion(self, characteristic_data, interval):
        data_slice = characteristic_data[interval[0]:interval[1]]
        t = np.linspace(0, interval[1] - interval[0] - 1, interval[1] - interval[0])
        nondamp_exp_regressant = sp.optimize.curve_fit(expgrowth_model_curve, t, data_slice)
        print(nondamp_exp_regressant)
        plt.plot(t, data_slice)
        plt.plot(t, expgrowth_model_curve(t, 
                                          nondamp_exp_regressant[0][0], 
                                          nondamp_exp_regressant[0][1], 
                                          nondamp_exp_regressant[0][2],
                                          nondamp_exp_regressant[0][3]))
        plt.show()
        return nondamp_exp_regressant[0][0]

def damp_model_curve(inp, tc, offsetx, amp, period, offsety):  # assumes begin at peak, so pure cosine may be used
        return amp * np.exp(-inp / tc) * np.cos((inp * 2 * np.pi / (period*2)) + offsetx) + offsety # this will give the negative TC. Don't forget to multiply TC by -1

def expgrowth_model_curve(inp, tc, amp, offsetx, offsety):  # assumes begin at peak, so pure cosine may be used
        return amp * np.exp(inp / tc / 1000 - offsetx) + offsety # Don't forget to multiply TC by 1000
        
 


PLOT=True

data_dir = citation_data.Data()[0]['data_dir']

# Load the .mat file
data = sp.io.loadmat(data_dir)

# Accessing a struct field
flightdata = data['flightdata']  # This gives a numpy structured array

#Time series
time_series = np.asarray(flightdata['time'][0][0][0][0][0].flatten())

#Plotting altitude
Dadc1_bcAlt = np.asarray(flightdata['Dadc1_bcAlt'][0][0][0][0][0].flatten()) # Baro-corrected altitude (ft)

Dadc1_tas = np.asarray(flightdata['Dadc1_tas'][0][0][0][0][0].flatten()) # True airspeed in kts
Dadc1_tas_meters = kt_to_meter_per_sec(Dadc1_tas)

Ahrs1_Roll = np.asarray(flightdata['Ahrs1_Roll'][0][0][0][0][0].flatten()) # Roll angle (DEGREES)

#Define the interval of the phugoid motion
phugoid_interval = np.array([31812, 33288])

#Define the interval of the short form motion
shortpitch_interval = np.array([31168, 31239])

#Define the interval of the spiral dive
spiraldive_interval = np.array([37601, 38855])

#Define the interval of the Dutch Roll (without yaw damper)
dutchroll_interval = np.array([34233, 34492])

#Define the interval of the aperiodic roll
aperiodicroll_interval = np.array([35937, 36011])


thingy = datacurve_calc() 

Tcd, Pdamped = thingy.damped_oscillation(Dadc1_tas_meters, phugoid_interval)

Tce = thingy.non_oscillatory_motion(Ahrs1_Roll, spiraldive_interval)

Tce *= 1000
Tcd *= -1
Pdamped *= 2 #No clue why the program broke down and decided to always give 1 as the period but now it doesn't but we gotta multiply by 2

#Now we use the halftime and and period to validate the eigenvalues, not forgetting the necessary corrections

print('Time constant damped', Tcd)
print('Period damped', Pdamped)
print('Time constant exponential', Tce)

ac = thingy.get_ac()
chord = ac.c
V0 = ac.V0
V0 = kt_to_meter_per_sec(V0)
print('Chord is', chord)
print('V0 is', V0)


# e^-t/tau has to be 1/2. -t/tau = ln(0.5) t = ln0.5*-tau
Thalf = np.log(0.5)*Tcd
print('Half time is', Thalf)

Ksic = np.log(0.5)*chord/(V0*Thalf)
print('Ksi c is', Ksic)

Etac = 2 * np.pi * chord / (V0*Pdamped)
print('Eta c is', Etac)