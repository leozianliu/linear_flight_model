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

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

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

data_dir = "data_ref_2025/FTISxprt-20250304_084412.mat"

if __name__ == '__main__':

    ac_data = citation_data.Data()[0]
    cond_data = citation_data.Data()[1]

    #steady_period_sec = [3410, 3420] # Used to get parameters for the aircraft in steady flight condition
    compare_period_sec = [3173.2, 3310.8] # Used to compare the simulation with the real data
    steady_period_sec = [int(compare_period_sec[0] - 2), int(compare_period_sec[0])] # Used to get parameters for the aircraft in steady flight condition
    ac = Aircraft.Aircraft(steady_period_sec, ac_data, cond_data)
    solver = Solver.Solver(ac, cond_data)
    compare_valid = compare.compare_validation(ac, compare_period_sec, solver.sym_ss, solver.asym_ss)

    sys_data = compare_valid.sys_data
    residual_tas = compare_valid.sys_data['sim_tas_si'] - compare_valid.sys_data['real_tas_si']
    residual_aoa = compare_valid.sys_data['sim_aoa_deg'] - compare_valid.sys_data['real_aoa_deg']
    residual_pitch = compare_valid.sys_data['sim_pitch_deg'] - compare_valid.sys_data['real_pitch_deg']
    residual_pitch_rate = compare_valid.sys_data['sim_pitch_rate_deg'] - compare_valid.sys_data['real_pitch_rate_deg']
    input_delta_e = compare_valid.sys_data['real_delta_e_deg']
    timeVector = compare_valid.sys_data['sim_time']

    acf = signal.correlation_lags(len(timeVector), len(timeVector))
    corr_pitch = signal.correlate(residual_pitch - np.mean(residual_pitch), 
                        residual_pitch - np.mean(residual_pitch), 
                        mode='full')
    corr_pitch = corr_pitch / np.max(corr_pitch)  # Normalize

    plt.figure(figsize=(12, 6))
    plt.plot(acf, corr_pitch, color='blue')
    plt.xlabel('Lag')
    plt.ylabel('Autocorrelation')
    plt.title('Autocorrelation Function (All Lags)')
    plt.grid(True)

    # Add confidence intervals (95%)
    confidence_interval = 1.96 / np.sqrt(len(timeVector))
    plt.axhspan(-confidence_interval, confidence_interval, alpha=0.2, color='green')

    # Add a vertical line at lag 0 for reference
    plt.axvline(x=0, color='red', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show(block=False)

    corr_pitch_de = signal.correlate(residual_pitch - np.mean(residual_pitch), 
                        input_delta_e - np.mean(input_delta_e), 
                        mode='full')
    corr_pitch_de = corr_pitch_de / np.max(corr_pitch_de)  # Normalize

    plt.figure(figsize=(12, 6))
    plt.plot(acf, corr_pitch_de, color='red')
    plt.xlabel('Lag')
    plt.ylabel('Cross-correlation')
    plt.title('Residual Correlation with Input')
    plt.grid(True)

    # Add a vertical line at lag 0 for reference
    plt.axvline(x=0, color='red', linestyle='--', alpha=0.7)

    # Add confidence intervals (95%)
    confidence_interval = 1.96 / np.sqrt(len(timeVector))
    plt.axhspan(-confidence_interval, confidence_interval, alpha=0.2, color='green')

    # Add a vertical line at lag 0 for reference
    plt.axvline(x=0, color='red', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show(block=True)
