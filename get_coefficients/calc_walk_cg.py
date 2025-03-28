import sys
from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent
sys.path.append(ROOT_DIR) # Replace with your own path so you can use .py files from other directories
sys.path.append(f'{ROOT_DIR}/tools') # Replace with your own path so you can use .py files from other directories
sys.path.append(f'{ROOT_DIR}/parameters') # Replace with your own path so you can use .py files from other directories
sys.path.append(f'{ROOT_DIR}/EoM')
sys.path.append(f'{ROOT_DIR}/get_coefficients') # Replace with your own path so you can use .py files from other directories

import numpy as np
import Solver
import Aircraft
import citation_data

if __name__ == '__main__':

    ac_data = citation_data.Data()[0]
    cond_data = citation_data.Data()[1]
    data_dir = citation_data.Data()[0]['data_dir']

    steady_period_sec_before_walk = [2256, 2257] # Used to get parameters for the aircraft in steady flight condition
    ac_before_walk = Aircraft.Aircraft(steady_period_sec_before_walk, ac_data, cond_data, data_dir, benji_pos=288)
    print(f'CoM before: {ac_before_walk.xcom}')
    steady_period_sec_after_walk = [2377, 2378] # Used to get parameters for the aircraft in steady flight condition
    ac_after_walk = Aircraft.Aircraft(steady_period_sec_after_walk, ac_data, cond_data, data_dir, benji_pos=288-175) # moved 175 inches to the front
    print(f'CoM after: {ac_after_walk.xcom}')

