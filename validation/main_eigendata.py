import sys
from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent
sys.path.append(ROOT_DIR) # Replace with your own path so you can use .py files from other directories
sys.path.append(f'{ROOT_DIR}/tools') # Replace with your own path so you can use .py files from other directories
sys.path.append(f'{ROOT_DIR}/parameters') # Replace with your own path so you can use .py files from other directories
sys.path.append(f'{ROOT_DIR}/EoM')
sys.path.append(f'{ROOT_DIR}/get_coefficients') # Replace with your own path so you can use .py files from other directories

import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize
import scipy.signal
import Solver
import Aircraft
import citation_data
import compare
import eigendata_fit

# Standard intervals
#Define the interval of the phugoid motion
phugoid_interval = np.array([28206, 29938])

#Define the interval of the short form motion
shortpitch_interval = np.array([30362, 30429])

#Define the interval of the spiral dive
spiraldive_interval = np.array([34560, 35379])

#Define the interval of the Dutch Roll (without yaw damper)
dutchroll_interval = np.array([32095, 32292])

#Define the interval of the aperiodic roll
aperiodicroll_interval = np.array([31132, 31228])

# Intervals chosen for curve fitting
# Short pitch motion
[3037.0, 3040.0]
# Phugoid motion
[2840.0, 2993.8] 
# Dutch roll
[3212.5, 3222.5]
# Aperiodic roll
[3113.2, 3119.2]
# Spiral motion
[3456.0, 3476.0]

if __name__ == '__main__':

    ac_data = citation_data.Data()[0]
    cond_data = citation_data.Data()[1]
    data_dir = citation_data.Data()[0]['data_dir']

    motion_period_sec = [3456.0, 3476.0] # Used to compare the simulation with the real data
    motion_idx = [int(motion_period_sec[0] * 10), int(motion_period_sec[1] * 10)]
    steady_period_sec = [int(motion_period_sec[0] - 1), int(motion_period_sec[0] - 0)] # Used to get parameters for the aircraft in steady flight condition
    ac = Aircraft.Aircraft(steady_period_sec, ac_data, cond_data, data_dir)
    solver = Solver.Solver(ac, cond_data)

    data = {}
    data['TAS'] = ac.Dadc1_tas_si[motion_idx[0]:motion_idx[1]]
    data['AOA'] = ac.vane_AOA[motion_idx[0]:motion_idx[1]]
    data['Pitch'] = ac.Ahrs1_Pitch[motion_idx[0]:motion_idx[1]]
    data['PitchRate'] = ac.Ahrs1_bPitchRate[motion_idx[0]:motion_idx[1]]
    data['Elevator'] = ac.delta_e[motion_idx[0]:motion_idx[1]]
    data['Roll'] = ac.Ahrs1_Roll[motion_idx[0]:motion_idx[1]]
    data['RollRate'] = ac.Ahrs1_bRollRate[motion_idx[0]:motion_idx[1]]
    data['YawRate'] = ac.Ahrs1_bYawRate[motion_idx[0]:motion_idx[1]]
    data['Aileron'] = ac.delta_a[motion_idx[0]:motion_idx[1]]
    data['Rudder'] = ac.delta_r[motion_idx[0]:motion_idx[1]]
    data['RealTime'] = ac.time_series[motion_idx[0]:motion_idx[1]]

    # state1 = 'TAS'
    # state2 = 'AOA'
    # state3 = 'Pitch'
    # state4 = 'PitchRate'
    # eigendata_fit.eigendata(data['RealTime'], data, state1, 0, 'sym', ac)  # fit_type = 0 for damped oscillation, 1 for damped
    # eigendata_fit.eigendata(data['RealTime'], data, state2, 0, 'sym', ac)  # fit_type = 0 for damped oscillation, 1 for damped
    # eigendata_fit.eigendata(data['RealTime'], data, state3, 0, 'sym', ac)  # fit_type = 0 for damped oscillation, 1 for damped
    # eigendata_fit.eigendata(data['RealTime'], data, state4, 0, 'sym', ac)  # fit_type = 0 for damped oscillation, 1 for damped

    # plt.plot(data['RealTime'], data['Elevator'])
    # plt.show()

    state2 = 'Roll'
    state3 = 'RollRate'
    state4 = 'YawRate'
    eigendata_fit.eigendata(data['RealTime'], data, state2, 1, 'asym', ac)  # fit_type = 0 for damped oscillation, 1 for damped
    eigendata_fit.eigendata(data['RealTime'], data, state3, 1, 'asym', ac)  # fit_type = 0 for damped oscillation, 1 for damped
    eigendata_fit.eigendata(data['RealTime'], data, state4, 1, 'asym', ac)  # fit_type = 0 for damped oscillation, 1 for damped

    plt.plot(data['RealTime'], data['Rudder'])
    plt.plot(data['RealTime'], data['Aileron'])
    plt.show()