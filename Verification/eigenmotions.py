import scipy as sp
import numpy as np
from helper import *
import matplotlib.pyplot as plt
import calculate_aero_curves_from_data

PLOT=True

# Load the .mat file
data = sp.io.loadmat(data_dir)

# Accessing a struct field
flightdata = data['flightdata']  # This gives a numpy structured array

#Time series
time_series = np.asarray(flightdata['time'][0][0][0][0][0].flatten())

Plotting altitude
Dadc1_bcAlt = np.asarray(flightdata['Dadc1_bcAlt'][0][0][0][0][0].flatten()) # Baro-corrected altitude (ft)
#plotting to enable visual inspection
if PLOT:
    plt.plot([#Time], [Dadc1_bcAlt])
    plt.xlabel("Time")
    plt.ylabel("Altitude")
    plt.title("Altitude over time")
    plt.show()

#Define the interval of the phugoid motion
phugoid_interval = np.array([31812, 33288])

#Now we find the halftime and and period, starting with the period to ensure the halftime calculation is non-trivial
