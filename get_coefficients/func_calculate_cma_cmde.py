import sys
from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent
sys.path.append(ROOT_DIR) # Replace with your own path so you can use .py files from other directories
sys.path.append(f'{ROOT_DIR}/tools') # Replace with your own path so you can use .py files from other directories

import warnings
import numpy as np
import citation_data
from scipy import stats
from thrust import Thrust
from helper import *

# Constants
R = 287.05  # Specific gas constant for dry air
g = 9.80665  # Acceleration due to gravity
rho_air = 1.225  # Density of air at sea level in kg/m^3

# Standard values S
W_s = 60500 # standard aircraft mass in N
mass_flow_si = 0.048 # standard mass flow in kg/s

def tas_to_eas(tas, true_rho): # True Airspeed in kts to Equivalent Airspeed in m/s
    return tas * np.sqrt(true_rho / rho_air)

def eas_to_ras(eas_si, weight_N): # Equivalent Airspeed to Reduced Airspeed in m/s
    return eas_si * np.sqrt(W_s / weight_N)

def T_to_Tc(T, h, sat, tas): # converts thrust to thrust coefficient;
    rho = pressure_alt_to_density(h,sat)
    q = 1/2*rho*tas**2
    S_eng = inch_to_meters(27)**2 # 27in is the engine diameter
    return T/(q*S_eng)

# def total_thrust(pressure_alt, mach, left_ff, right_ff, tat):
#     dT = tat - pressure_alt_to_ISA_temperature(pressure_alt)

#     map_to_thrust_fnc = np.vectorize(Thrust.compute)
#     left_thrust = map_to_thrust_fnc(pressure_alt, mach, dT, left_ff)
#     right_thrust = map_to_thrust_fnc(pressure_alt, mach, dT, right_ff)
#     thrust = left_thrust + right_thrust
#     return thrust

def total_thrust(pressure_alt, mach, left_ff, right_ff, tat):
    dT = tat - pressure_alt_to_ISA_temperature(pressure_alt)
    dT = np.mean(dT)
    pressure_alt = np.mean(pressure_alt)
    mach = np.mean(mach)
    left_ff = np.mean(left_ff)
    right_ff = np.mean(right_ff)

    left_thrust = Thrust.compute(pressure_alt, mach, dT, left_ff)
    right_thrust = Thrust.compute(pressure_alt, mach, dT, right_ff)
    thrust = left_thrust + right_thrust
    return thrust

def reduced_elev_angle_deg(pressure_alt, mach, left_ff, right_ff, tat, sat, tas, delta_e_deg, cmde, Tcs, CmTc):
    Tc = T_to_Tc(total_thrust(pressure_alt, mach, left_ff, right_ff, tat), pressure_alt, sat, tas)
    red_delta_e_rad = np.deg2rad(delta_e_deg) - CmTc / cmde * (Tcs - Tc)
    return np.rad2deg(red_delta_e_rad)

def reduced_elev_force(meas_elev_force, weight_N):
    return meas_elev_force * W_s / weight_N

def cn_calc(weight_N, eas, S):
    return weight_N / (0.5 * rho_air * eas ** 2 * S)

def cmde_calc(weight_N, elev_ang_prev_deg, elev_ang_after_deg, cg_pos_prev, cg_pos_after, eas, c, S):
    cn = cn_calc(weight_N, eas, S)
    cmde = - (1 / (np.deg2rad(elev_ang_after_deg) - np.deg2rad(elev_ang_prev_deg))) * cn * (cg_pos_after - cg_pos_prev) / c
    return cmde

def linear_reg(x, y):
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    return slope, intercept, r_value, p_value, std_err

def de_vs_daoa_calc(de_deg_arr, aoa_deg_arr):
    de_rad_arr = np.deg2rad(de_deg_arr)
    aoa_rad_arr = np.deg2rad(aoa_deg_arr)
    slope, intercept, r_value, p_value, std_err = linear_reg(aoa_rad_arr, de_rad_arr)
    return slope

def cma_calc(de_deg_arr, aoa_deg_arr, cmde):
    de_rad_arr = np.deg2rad(de_deg_arr)
    aoa_rad_arr = np.deg2rad(aoa_deg_arr)
    cma = - cmde * de_vs_daoa_calc(de_deg_arr, aoa_deg_arr)
    return cma