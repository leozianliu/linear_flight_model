import sys
from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent
sys.path.append(ROOT_DIR) # Replace with your own path so you can use .py files from other directories
sys.path.append(f'{ROOT_DIR}/tools') # Replace with your own path so you can use .py files from other directories
sys.path.append(f'{ROOT_DIR}/parameters') # Replace with your own path so you can use .py files from other directories
sys.path.append(f'{ROOT_DIR}/get_coefficients') # Replace with your own path so you can use .py files from other directories

import matplotlib
import numpy as np
import Solver
import Aircraft
import citation_data

if __name__ == '__main__':

    ac_data = citation_data.Data()[0]
    cond_data = citation_data.Data()[1]
    data_dir = citation_data.Data()[0]['data_dir']

    steady_period_sec = [2256, 2258] # Used to get parameters for the aircraft in steady flight condition
    ac = Aircraft.Aircraft(steady_period_sec, ac_data, cond_data, data_dir)
    solver = Solver.Solver(ac, cond_data)

    solver.show_solutions()
    
