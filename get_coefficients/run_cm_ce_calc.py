import sys
from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent
sys.path.append(ROOT_DIR) # Replace with your own path so you can use .py files from other directories
sys.path.append(f'{ROOT_DIR}/tools') # Replace with your own path so you can use .py files from other directories
sys.path.append(f'{ROOT_DIR}/parameters') # Replace with your own path so you can use .py files from other directories


import scipy as sp
import numpy as np

import citation_data
from helper import *
from func_calculate_cma_cmde import *
import matplotlib.pyplot as plt
import Aircraft

time_of_interest = [1000,1001] # Time doesn't matter in this file because we are only getting c, S, and CmTc which are constant in citation.py
ac = Aircraft.Aircraft(time_of_interest, citation_data.Data()[0], citation_data.Data()[1])

# Parameters
int_fuel_lbs = 4100
data_dir = "data_ref_2025/FTISxprt-20250304_084412.mat"

# Load the .mat file
data = sp.io.loadmat(data_dir)

# Accessing a struct field
flightdata = data['flightdata']  # This gives a numpy structured array

# AOA
vane_AOA = np.asarray(flightdata['vane_AOA'][0][0][0][0][0].flatten())

# Baro-corrected altitude
Dadc1_bcAlt = np.asarray(flightdata['Dadc1_bcAlt'][0][0][0][0][0].flatten()) # Baro-corrected altitude (ft)
Dadc1_bcAlt_meters = ft_to_meters(Dadc1_bcAlt)  # Convert to meters

# TAS
Dadc1_tas = np.asarray(flightdata['Dadc1_tas'][0][0][0][0][0].flatten())
Dadc1_tas_si = kt_to_meter_per_sec(Dadc1_tas)

# SAT
Dadc1_sat = np.asarray(flightdata['Dadc1_sat'][0][0][0][0][0].flatten())
Dadc1_sat_si = celsius_to_kelvin(Dadc1_sat)

# TAT
Dadc1_tat = np.asarray(flightdata['Dadc1_tat'][0][0][0][0][0].flatten())
Dadc1_tat_si = celsius_to_kelvin(Dadc1_tat)

# Mach number
Dadc1_mach = np.asarray(flightdata['Dadc1_mach'][0][0][0][0][0].flatten())

# Elevator force
column_fe = np.asarray(flightdata['column_fe'][0][0][0][0][0].flatten())

# Elevator deflection in degrees
delta_e = np.asarray(flightdata['delta_e'][0][0][0][0][0].flatten())

# Fuel use
lh_engine_FU = np.asarray(flightdata['lh_engine_FU'][0][0][0][0][0].flatten())
rh_engine_FU = np.asarray(flightdata['rh_engine_FU'][0][0][0][0][0].flatten())

# Fuel flow
lh_engine_FMF = np.asarray(flightdata['lh_engine_FMF'][0][0][0][0][0].flatten())
lh_engine_FMF_si = lbs_hr_to_kg_s(lh_engine_FMF)
rh_engine_FMF = np.asarray(flightdata['rh_engine_FMF'][0][0][0][0][0].flatten())
rh_engine_FMF_si = lbs_hr_to_kg_s(rh_engine_FMF)

# Total fuel left
total_FL = int_fuel_lbs - (lh_engine_FU + rh_engine_FU)
total_FL_kg = lb_to_kg(total_FL)

# Total weight
person_masses = np.array([91,96,79,71,90,93,90,98,83])
bem_kg = lb_to_kg(9197.0) # Basic empty mass
total_mass = np.sum(person_masses) + total_FL_kg + bem_kg
total_weight_N = total_mass * g

# Time series
time_series = np.asarray(flightdata['time'][0][0][0][0][0].flatten())

# Thrust and thrust coefficient at standard condition (t=2140s)
t_std = 2140
thrust_std = total_thrust(Dadc1_bcAlt_meters[t_std*10], Dadc1_mach[t_std*10], lh_engine_FMF_si[t_std*10], rh_engine_FMF_si[t_std*10], Dadc1_tat_si[t_std*10])
Tcs = T_to_Tc(thrust_std, Dadc1_bcAlt_meters[t_std*10], Dadc1_sat_si[t_std*10], Dadc1_tas_si[t_std*10])

# Change in elevator deflection when Benji walks to the cockpit
t_benji_walk = np.array([2865, 3000]) # First measurement, second measurement in seconds
benji_interval = t_benji_walk * 10
real_density_benji = pressure_alt_to_density(Dadc1_bcAlt_meters[benji_interval[0]:benji_interval[1]], Dadc1_sat_si[benji_interval[0]:benji_interval[1]])
avg_eas_benji = np.mean(tas_to_eas(Dadc1_tas_si[benji_interval[0]:benji_interval[1]], real_density_benji))

total_weight_N_benji = total_weight_N[benji_interval[0]:benji_interval[1]]
avg_weight_N_benji = np.mean(total_weight_N_benji)
ave_delta_e_benji_prev = np.mean(delta_e[benji_interval[0]-10:benji_interval[0]])
ave_delta_e_benji_after = np.mean(delta_e[benji_interval[1]-10:benji_interval[1]])
cg_benji_prev = 7.13025 # in meters
cg_benji_after = 7.06214 # in meters

# cmde in 1/rad!!!
cmde = cmde_calc(avg_weight_N_benji, ave_delta_e_benji_prev, ave_delta_e_benji_after, cg_benji_prev, cg_benji_after, avg_eas_benji, ac.c, ac.S)
print('cmde (1/rad): ', cmde)

# Equilibrium elevator deflection intervals in trim tests in idx or seconds*10
equilibrium_elevator_intervals = np.array([[21069, 21352],
                                            [21825, 22220],
                                            [22787, 23088],
                                            [23528, 23863],
                                            [24739, 25071],
                                            [25765, 26237],
                                            [26732, 27064]
                                            ])

# Calculate average values of ras_arr and delta_e for each interval
average_ras_arr = []
average_red_delta_e_deg = []
average_red_elev_force = []
average_aoa_deg = []

for interval in equilibrium_elevator_intervals:
    real_density = pressure_alt_to_density(Dadc1_bcAlt_meters[interval[0]:interval[1]], Dadc1_sat_si[interval[0]:interval[1]])
    eas_arr = tas_to_eas(Dadc1_tas_si[interval[0]:interval[1]], real_density)
    ras_arr = eas_to_ras(eas_arr, total_weight_N[interval[0]:interval[1]])
    red_elev_force_arr = reduced_elev_force(column_fe[interval[0]:interval[1]], total_weight_N[interval[0]:interval[1]])
    red_elev_angle_arr = reduced_elev_angle_deg(Dadc1_bcAlt_meters[interval[0]:interval[1]], Dadc1_mach[interval[0]:interval[1]],\
         lh_engine_FMF_si[interval[0]:interval[1]], rh_engine_FMF_si[interval[0]:interval[1]], Dadc1_tat_si[interval[0]:interval[1]], \
            Dadc1_sat_si[interval[0]:interval[1]], Dadc1_tat_si[interval[0]:interval[1]], delta_e[interval[0]:interval[1]], cmde, Tcs, ac.CmTc)
    
    avg_ras = np.mean(ras_arr)
    #avg_delta_e = np.mean(delta_e[interval[0]:interval[1]])
    avg_red_delta_e = np.mean(red_elev_angle_arr)
    avg_red_elev_force = np.mean(red_elev_force_arr)
    avg_aoa_deg = np.mean(vane_AOA[interval[0]:interval[1]])
    
    average_ras_arr.append(avg_ras)
    average_red_delta_e_deg.append(avg_red_delta_e)
    average_red_elev_force.append(avg_red_elev_force)
    average_aoa_deg.append(avg_aoa_deg)

# Sort the values for plotting only, don't use them for anything else as the orders might be mixed up
average_ras_arr_plot = np.sort(np.array(average_ras_arr))
average_red_delta_e_deg_plot = np.sort(np.array(average_red_delta_e_deg))
average_red_elev_force_plot = np.sort(np.array(average_red_elev_force))

# cma in 1/rad!!!
cma = cma_calc(average_red_delta_e_deg, average_aoa_deg, cmde) # Not sure if I should use reduced delta_e here, but the difference in cma is <1%
print('cma (1/rad): ', cma)
# --------------------------------------------------------------------------------------------

# Create subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

ax1.plot(average_ras_arr_plot, average_red_delta_e_deg_plot, linestyle='-', color='blue', marker='o', markersize=5, markerfacecolor='red')
ax1.set_xlabel('Reduced speed (m/s)')
ax1.set_ylabel('Reduced elevator angle (deg)')
ax2.plot(average_ras_arr_plot, average_red_elev_force_plot, linestyle='-', color='blue', marker='o', markersize=5, markerfacecolor='red')
ax2.set_xlabel('Reduced speed (m/s)')
ax2.set_ylabel('Reduced elevator force (N)')
ax1.grid()
ax2.grid()

#fig1.suptitle('Flight Data 1')
#fig2.suptitle('Flight Data 1')

plt.tight_layout(rect=[0, 0, 1, 0.96])

plt.show()


