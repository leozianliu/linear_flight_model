import sys
from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent
sys.path.append(ROOT_DIR) # Replace with your own path so you can use .py files from other directories
sys.path.append(f'{ROOT_DIR}/tools') # Replace with your own path so you can use .py files from other directories
sys.path.append(f'{ROOT_DIR}/parameters') # Replace with your own path so you can use .py files from other directories
sys.path.append(f'{ROOT_DIR}/EoM')
sys.path.append(f'{ROOT_DIR}/get_coefficients') # Replace with your own path so you can use .py files from other directories

import matplotlib
import numpy as np
import Solver
import Aircraft
import citation_data
import compare

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

if __name__ == '__main__':

    ac_data = citation_data.Data()[0]
    cond_data = citation_data.Data()[1]
    data_dir = citation_data.Data()[0]['data_dir']

    #steady_period_sec = [3410, 3420] # Used to get parameters for the aircraft in steady flight condition
    compare_period_sec = [3175.2, 3320.0] # Used to compare the simulation with the real data
    steady_period_sec = [int(compare_period_sec[0] - 1), int(compare_period_sec[0])] # Used to get parameters for the aircraft in steady flight condition
    ac = Aircraft.Aircraft(steady_period_sec, ac_data, cond_data, data_dir)
    solver = Solver.Solver(ac, cond_data)
    compare_valid = compare.compare_validation(ac, compare_period_sec, solver.sym_ss, solver.asym_ss)

