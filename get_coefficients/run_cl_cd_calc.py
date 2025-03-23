import sys
from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent
sys.path.append(ROOT_DIR) # Replace with your own path so you can use .py files from other directories
sys.path.append(f'{ROOT_DIR}/tools') # Replace with your own path so you can use .py files from other directories
sys.path.append(f'{ROOT_DIR}/parameters') # Replace with your own path so you can use .py files from other directories


import scipy as sp
import numpy as np
from helper import *
import matplotlib.pyplot as plt
import func_calculate_cla_cd

PLOT=True

#region temp data reading:

# Parameters
int_fuel_lbs = 4100
data_dir = "data_ref_2025/FTISxprt-20250304_084412.mat"

# Load the .mat file
data = sp.io.loadmat(data_dir)

# Accessing a struct field
flightdata = data['flightdata']  # This gives a numpy structured array

# AOAs
vane_AOA = np.asarray(flightdata['vane_AOA'][0][0][0][0][0].flatten())

# Mach
dadc1_mach = np.asarray(flightdata['Dadc1_mach'][0][0][0][0][0].flatten())

# Baro-corrected altitude
Dadc1_bcAlt = np.asarray(flightdata['Dadc1_bcAlt'][0][0][0][0][0].flatten()) # Baro-corrected altitude (ft)
Dadc1_bcAlt_meters = ft_to_meters(Dadc1_bcAlt)  # Convert to meters

# TAS
Dadc1_tas = np.asarray(flightdata['Dadc1_tas'][0][0][0][0][0].flatten())


# temp
Dadc1_sat = np.asarray(flightdata['Dadc1_sat'][0][0][0][0][0].flatten())

#total temp
Dadc1_tat = np.asarray(flightdata['Dadc1_tat'][0][0][0][0][0].flatten())


# Roll, Pitch in DEGREES!!!
Ahrs1_Roll = np.asarray(flightdata['Ahrs1_Roll'][0][0][0][0][0].flatten())
Ahrs1_Pitch = np.asarray(flightdata['Ahrs1_Pitch'][0][0][0][0][0].flatten())

# Fuel use
lh_engine_FU = np.asarray(flightdata['lh_engine_FU'][0][0][0][0][0].flatten())
rh_engine_FU = np.asarray(flightdata['rh_engine_FU'][0][0][0][0][0].flatten())

# Fuel mass flow
lh_engine_FMF = np.asarray(flightdata['lh_engine_FMF'][0][0][0][0][0].flatten())
rh_engine_FMF = np.asarray(flightdata['rh_engine_FMF'][0][0][0][0][0].flatten())

# Total fuel left
total_FL = int_fuel_lbs - (lh_engine_FU + rh_engine_FU)
total_FL_kg = lb_to_kg(total_FL)

# Time series
time_series = np.asarray(flightdata['time'][0][0][0][0][0].flatten())


equilibrium_cl_intervals = np.array([[11253, 12343],
                                     [12630, 13378],
                                     [13766, 14549],
                                     [15499, 16633],
                                     [17126, 18072],
                                     [18438, 19143]])
#endregion

#region calcs

#arrays with the relevant data: 0 - aoa, 1 - weight, 2 - rho, 3 - tas, 4 - h(time), 5 - T(time), 6 - mach, 7 - m_f_dot_left(time), 8 - m_f_dot_right(time) 
rhos = pressure_alt_to_density(Dadc1_bcAlt_meters, celsius_to_kelvin(Dadc1_sat))
print("Mean density = : " + str(np.mean(rhos)))

input_for_curves = [vane_AOA,
                    (total_FL_kg + 4080)*9.81,
                    rhos,
                    kt_to_meter_per_sec(Dadc1_tas),
                    Dadc1_bcAlt_meters,
                    celsius_to_kelvin(Dadc1_tat),
                    dadc1_mach,
                    lb_to_kg(lh_engine_FMF)/3600,
                    lb_to_kg(rh_engine_FMF)/3600]

calc = func_calculate_cla_cd.curve_calc()

cl_curve = calc.cl_data(input_for_curves, equilibrium_cl_intervals)
cd_curve = calc.cd_data(input_for_curves, equilibrium_cl_intervals)
clcd_curve = calc.cl_cd(cl_curve, cd_curve)
cl2cd_curve = calc.cl2_cd(cl_curve, cd_curve)

cl_regressant = sp.stats.linregress(np.asarray(cl_curve).T[0], np.asarray(cl_curve).T[1])
cl2cd_regressant = sp.stats.linregress(np.asarray(cl2cd_curve).T[1], np.asarray(cl2cd_curve).T[0])

print("Cla = : " + str(cl_regressant.slope))
print("Cd0 = " + str(cl2cd_regressant.intercept))
print("ClCd_slope = " + str(cl2cd_regressant.slope))
print("e = " + str(1 / (cl2cd_regressant.slope * 15.911/2.0569 * np.pi)))  # TODO slightly less sus value for e

# endregion

#region plotting
if PLOT:
    plt.plot([x[0] for x in cd_curve if True], [x[1] for x in cd_curve if True], 'ro')
    plt.xlabel("AoA [deg]")
    plt.ylabel("CD")
    plt.title("AoA vs CD")
    plt.show()
    plt.clf()
    plt.plot([x[0] for x in cl_curve if True], [x[1] for x in cl_curve if True], 'ro')
    plt.xlabel("AoA [deg]")
    plt.ylabel("CL")
    plt.title("AoA vs CL")
    plt.show()
    plt.clf()
    plt.plot([x[1] for x in clcd_curve if True], [x[0] for x in clcd_curve if True], 'ro')
    plt.xlabel("Cl")
    plt.ylabel("Cd")
    plt.title("Cd vs Cl")
    plt.show()
    plt.clf()
    plt.plot([x[1] for x in cl2cd_curve if True], [x[0] for x in cl2cd_curve if True], 'ro')
    plt.xlabel("Cl^2")
    plt.ylabel("Cd")
    plt.title("Cd vs Cl^2")
    plt.show()
# endregion