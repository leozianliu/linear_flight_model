import sys
from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent
sys.path.append(ROOT_DIR) # Replace with your own path so you can use .py files from other directories
sys.path.append(f'{ROOT_DIR}/tools') # Replace with your own path so you can use .py files from other directories

import numpy as np

import Aircraft
import citation_data
from thrust import *
from helper import *


class curve_calc:

    def __init__(self):

        # [10,11] is a filler to obtain static values from citation_data, this program does not use time dependent coefficients from aircraft.py
        self.ac = Aircraft.Aircraft([1000,1001] , citation_data.Data()[0], citation_data.Data()[1])

    def cl_data(self, data, data_ranges):
        """Generates an alpha-cl curve from the data.

        Args:
            data (np.array(4,2)): arrays with the relevant data: 0 - aoa, 1 - weight, 2 - rho, 3 - tas
            data_ranges (np.array(:,2)): array with the ranges during which the equilibrium is measured

        Returns:
            np.array(:,2): array with the alpha-cl curve where [(alpha,cl),...]
        """

        cl_curve = []

        for i in range(0, len(data_ranges[:])):  # for every chosen interval of equilibrium flight

            start = data_ranges[i][0]  # interval start and end
            end = data_ranges[i][1]

            aoa_data = data[0][start:end]
            avg_aoa = np.mean(aoa_data)  # aoa during interval

            weight_data = data[1][start:end]
            rho_data = data[2][start:end]
            tas_data = data[3][start:end]
            height_data = data[4][start:end]
            temp_data = data[5][start:end]
            mach_data = data[6][start:end]
            left_fuelflow_data = data[7][start:end]
            right_fuelflow_data = data[8][start:end]

            avg_weight = np.mean(weight_data)
            avg_rho = np.mean(rho_data)
            avg_tas = np.mean(tas_data)
            avg_height = np.mean(height_data)
            avg_temp = np.mean(temp_data)
            avg_mach = np.mean(mach_data)
            avg_left_fuelflow = np.mean(left_fuelflow_data)
            avg_right_fuelflow = np.mean(right_fuelflow_data)

            dT = avg_temp - pressure_alt_to_ISA_temperature(avg_height)

            left_thrust = Thrust.compute(avg_height, avg_mach, dT, avg_left_fuelflow)
            right_thrust = Thrust.compute(avg_height, avg_mach, dT, avg_right_fuelflow)

            thrust = left_thrust + right_thrust

            cl = 2 * (avg_weight - np.sin(avg_aoa) * thrust) / avg_rho / avg_tas**2 / self.ac.S
            cl_curve.append([avg_aoa, cl])

        return cl_curve  # calculate

    def cd_data(self, data, data_ranges):
        """Generates an alpha-cd curve from the data.

        Args:
            data (np.array(4,2)): arrays with the relevant data: 0 - aoa, 1 - weight, 2 - rho, 3 - tas, 4 - h(time), 5 - T(time), 6 - mach, 7 - m_f_dot_left(time), 8 - m_f_dot_right(time)
            data_ranges (np.array(:,2)): array with the ranges during which the equilibrium is measured

        Returns:
            np.array(:,2): array with the alpha-cd curve where [(alpha,cd),...]
        """

        cd_curve = []

        for i in range(0, len(data_ranges)):  # for every chosen interval of equilibrium flight

            start = data_ranges[i][0]  # interval start and end
            end = data_ranges[i][1]

            aoa_data = data[0][start:end]
            avg_aoa = np.mean(aoa_data)  # aoa during interval

            weight_data = data[1][start:end]
            rho_data = data[2][start:end]
            tas_data = data[3][start:end]
            height_data = data[4][start:end]
            temp_data = data[5][start:end]
            mach_data = data[6][start:end]
            left_fuelflow_data = data[7][start:end]
            right_fuelflow_data = data[8][start:end]

            avg_weight = np.mean(weight_data)
            avg_rho = np.mean(rho_data)
            avg_tas = np.mean(tas_data)
            avg_height = np.mean(height_data)
            avg_temp = np.mean(temp_data)
            avg_mach = np.mean(mach_data)
            avg_left_fuelflow = np.mean(left_fuelflow_data)
            avg_right_fuelflow = np.mean(right_fuelflow_data)

            dT = avg_temp - pressure_alt_to_ISA_temperature(avg_height)

            left_thrust = Thrust.compute(avg_height, avg_mach, dT, avg_left_fuelflow)
            right_thrust = Thrust.compute(avg_height, avg_mach, dT, avg_right_fuelflow)

            thrust = left_thrust + right_thrust

            cd = 2 * np.cos(np.deg2rad(avg_aoa)) * thrust / avg_rho / avg_tas**2 / self.ac.S

            cd_curve += [[avg_aoa, cd]]

        return cd_curve

    def cl_cd(self, cl_curve, cd_curve):

        cl_cd_curve = []

        for i in range(0, len(cl_curve)):

            cl_cd_curve.append([[], []])
            cl_cd_curve[i][0] = cd_curve[i][1]
            cl_cd_curve[i][1] = cl_curve[i][1]

        return cl_cd_curve

    def cl2_cd(self, cl_curve, cd_curve):

        cl2_cd_curve = []

        for i in range(0, len(cl_curve)):

            cl2_cd_curve.append([[], []])
            cl2_cd_curve[i][0] = cd_curve[i][1]
            cl2_cd_curve[i][1] = cl_curve[i][1]**2

        return cl2_cd_curve


    
