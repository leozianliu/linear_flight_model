import sys
from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent
sys.path.append(ROOT_DIR) # Replace with your own path so you can use .py files from other directories
sys.path.append(f'{ROOT_DIR}/tools') # Replace with your own path so you can use .py files from other directories
sys.path.append(f'{ROOT_DIR}/parameters') # Replace with your own path so you can use .py files from other directories
sys.path.append(f'{ROOT_DIR}/EoM')
sys.path.append(f'{ROOT_DIR}/get_coefficients') # Replace with your own path so you can use .py files from other directories

import scipy.io
import numpy as np
from helper import *
import matplotlib.pyplot as plt
import math


class Aircraft:

    def __init__(self, time_of_interest:list[int,int], aircraft_data, conditions_data, data_dir, benji_pos=288):
        self.data_dir = data_dir
        idx_of_interest = np.array(time_of_interest) * 10# First measurement, second measurement in seconds
        self.int_fuel_lbs = aircraft_data["int_fuel_lbs"]
        self.person_masses = aircraft_data["person_masses"]
        
        self.read_flight_data(time_of_interest, self.int_fuel_lbs, self.data_dir)
        total_mass_arr = []
        x_com_arr = [] # metric
        x_cg_arr = [] # %MAC
        for i in np.arange(time_of_interest[0], time_of_interest[1]+1, 1):
            self.mass_centroid(time_of_interest[1], benji_pos)
            total_mass_arr.append(self.total_current_mass_kg)
            x_com_arr.append(self.center_mass)
            x_cg_arr.append(self.x_cg)

        #identifier
        self.name = aircraft_data["name"]

        #point mass parameters
        self.mass = np.mean(total_mass_arr) #aircraft_data["mass"]
        self.W = self.mass * 9.80665 # [N]       (aircraft weight)
        self.xcom = np.mean(x_com_arr) # [m]       (x position of the center of mass)
        self.xcg =  np.mean(x_cg_arr)

        #stationary flight conditions
        self.hp0 = np.mean(self.Dadc1_bcAlt_meters[idx_of_interest[0]:idx_of_interest[1]])
        self.V0 = np.mean(self.Dadc1_tas_si[idx_of_interest[0]:idx_of_interest[1]])
        self.rho = np.mean(pressure_alt_to_density(self.Dadc1_bcAlt_meters[idx_of_interest[0]:idx_of_interest[1]], self.Dadc1_sat_si[idx_of_interest[0]:idx_of_interest[1]]))
        self.alpha0 = np.deg2rad(np.mean(self.vane_AOA[idx_of_interest[0]:idx_of_interest[1]])) # Must be in radians
        self.th0 = np.deg2rad(np.mean(self.Ahrs1_Pitch[idx_of_interest[0]:idx_of_interest[1]])) # Must be in radians
        self.delta_e0 = np.deg2rad(np.mean(self.delta_e[idx_of_interest[0]:idx_of_interest[1]])) # Must be in radians
        self.delta_a0 = np.deg2rad(np.mean(self.delta_a[idx_of_interest[0]:idx_of_interest[1]])) # Must be in radians
        self.delta_r0 = np.deg2rad(np.mean(self.delta_r[idx_of_interest[0]:idx_of_interest[1]])) # Must be in radians
        self.phi0 = np.deg2rad(np.mean(self.Ahrs1_Roll[idx_of_interest[0]:idx_of_interest[1]])) # Must be in radians
        self.p0 = np.deg2rad(np.mean(self.Ahrs1_bRollRate[idx_of_interest[0]:idx_of_interest[1]])) # Must be in radians
        self.q0 = np.deg2rad(np.mean(self.Ahrs1_bPitchRate[idx_of_interest[0]:idx_of_interest[1]])) # Must be in radians
        self.r0 = np.deg2rad(np.mean(self.Ahrs1_bYawRate[idx_of_interest[0]:idx_of_interest[1]])) # Must be in radians
    
        #aircraft geometry
        self.S = aircraft_data["S"]
        self.Sh = aircraft_data["Sh"]
        self.Sh_S = aircraft_data["Sh_S"]
        self.lh = aircraft_data["lh"]
        self.c = aircraft_data["c"]
        self.lh_c = aircraft_data["lh_c"]
        self.b = aircraft_data["b"]
        self.bh = aircraft_data["bh"]
        self.A = aircraft_data["A"]
        self.Ah = aircraft_data["Ah"]
        self.Vh_V = aircraft_data["Vh_V"]
        self.ih = aircraft_data["ih"]

        #aircraft steady parameters
        CX0 = self.W * math.sin(self.th0) / (0.5 * self.rho * self.V0 ** 2 * self.S)
        self.CX0 = CX0
        CZ0 = -self.W * math.cos(self.th0) / (0.5 * self.rho * self.V0 ** 2 * self.S)
        self.CZ0 = CZ0
        self.CL = 2 * self.W / (self.rho * self.V0 ** 2 * self.S)  # Lift coefficient [ ]
        # self.CD = aircraft_data["CD"]

        #updatable parameters
        muc = self.mass / (self.rho * self.S * self.c)
        self.muc = muc
        mub = self.mass / (self.rho * self.S * self.b)
        self.mub = mub

        #stuff
        self.KX2 = aircraft_data["KX2"]
        self.KZ2 = aircraft_data["KZ2"]
        self.KXZ = aircraft_data["KXZ"]
        self.KY2 = aircraft_data["KY2"]

        #aerodynamic coefficients
        self.Cmac = aircraft_data["Cmac"]
        self.CNwa = aircraft_data["CNwa"]
        self.CNha = aircraft_data["CNha"]
        self.depsda = aircraft_data["depsda"]

        self.CXu = aircraft_data["CXu"]
        self.CXa = aircraft_data["CXa"]
        self.CXadot = aircraft_data["CXadot"]
        self.CXq = aircraft_data["CXq"]
        self.CXde = aircraft_data["CXde"]

        self.CZu = aircraft_data["CZu"]
        self.CZa = aircraft_data["CZa"]
        self.CZadot = aircraft_data["CZadot"]
        self.CZq = aircraft_data["CZq"]
        self.CZde = aircraft_data["CZde"]

        self.Cm0 = aircraft_data["Cm0"]
        self.Cma = aircraft_data["Cma"]
        self.Cmu = aircraft_data["Cmu"]
        self.Cmadot = aircraft_data["Cmadot"]
        self.Cmq = aircraft_data["Cmq"]
        self.CmTc = aircraft_data["CmTc"]
        self.Cmde = aircraft_data["Cmde"]  # needs to be calculated from elevator curve (i think) >.<

        self.CYb = aircraft_data["CYb"]
        self.CYbdot = aircraft_data["CYbdot"]
        self.CYp = aircraft_data["CYp"]
        self.CYr = aircraft_data["CYr"]
        self.CYda = aircraft_data["CYda"]
        self.CYdr = aircraft_data["CYdr"]

        self.Clb = aircraft_data["Clb"]
        self.Clp = aircraft_data["Clp"]
        self.Clr = aircraft_data["Clr"]
        self.Clda = aircraft_data["Clda"]
        self.Cldr = aircraft_data["Cldr"]

        self.Cnb = aircraft_data["Cnb"]
        self.Cnbdot = aircraft_data["Cnbdot"]
        self.Cnp = aircraft_data["Cnp"]
        self.Cnr = aircraft_data["Cnr"]
        self.Cnda = aircraft_data["Cnda"]
        self.Cndr = aircraft_data["Cndr"]

    def read_flight_data(self, time_of_interest:list[int,int], int_fuel_lbs, data_dir:str):

        # Load the .mat file
        data = scipy.io.loadmat(data_dir)

        # Accessing a struct field
        flightdata = data['flightdata']  # This gives a numpy structured array

        # AOA in DEGREES!!!
        vane_AOA = np.asarray(flightdata['vane_AOA'][0][0][0][0][0].flatten())

        # Roll, Pitch in DEGREES!!!
        Ahrs1_Roll = np.asarray(flightdata['Ahrs1_Roll'][0][0][0][0][0].flatten())
        Ahrs1_Pitch = np.asarray(flightdata['Ahrs1_Pitch'][0][0][0][0][0].flatten())
        Ahrs1_bRollRate = np.asarray(flightdata['Ahrs1_bRollRate'][0][0][0][0][0].flatten())
        Ahrs1_bPitchRate = np.asarray(flightdata['Ahrs1_bPitchRate'][0][0][0][0][0].flatten())
        Ahrs1_bYawRate = np.asarray(flightdata['Ahrs1_bYawRate'][0][0][0][0][0].flatten())

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

        # Surface deflection in degrees
        delta_e = np.asarray(flightdata['delta_e'][0][0][0][0][0].flatten())
        delta_a = np.asarray(flightdata['delta_a'][0][0][0][0][0].flatten())
        delta_r = np.asarray(flightdata['delta_r'][0][0][0][0][0].flatten())

        # Fuel use
        lh_engine_FU = np.asarray(flightdata['lh_engine_FU'][0][0][0][0][0].flatten())
        rh_engine_FU = np.asarray(flightdata['rh_engine_FU'][0][0][0][0][0].flatten())

        # Fuel flow
        lh_engine_FMF = np.asarray(flightdata['lh_engine_FMF'][0][0][0][0][0].flatten())
        lh_engine_FMF_si = lbs_hr_to_kg_s(lh_engine_FMF)
        rh_engine_FMF = np.asarray(flightdata['rh_engine_FMF'][0][0][0][0][0].flatten())
        rh_engine_FMF_si = lbs_hr_to_kg_s(rh_engine_FMF)

        # Total fuel left
        total_FL_lb = int_fuel_lbs - (lh_engine_FU + rh_engine_FU)
        total_FL_kg = lb_to_kg(total_FL_lb)

        # Time series
        time_series = np.asarray(flightdata['time'][0][0][0][0][0].flatten())

        self.vane_AOA = vane_AOA
        self.Dadc1_bcAlt_meters = Dadc1_bcAlt_meters
        self.Ahrs1_Roll = Ahrs1_Roll
        self.Ahrs1_Pitch = Ahrs1_Pitch
        self.Ahrs1_bRollRate = Ahrs1_bRollRate
        self.Ahrs1_bPitchRate = Ahrs1_bPitchRate
        self.Ahrs1_bYawRate = Ahrs1_bYawRate
        self.total_FL_kg = total_FL_kg
        self.total_FL_lb = total_FL_lb
        self.Dadc1_tas_si = Dadc1_tas_si
        self.Dadc1_sat_si = Dadc1_sat_si
        self.Dadc1_tat_si = Dadc1_tat_si
        self.Dadc1_mach = Dadc1_mach
        self.column_fe = column_fe
        self.delta_e = delta_e
        self.delta_a = delta_a
        self.delta_r = delta_r
        self.lh_engine_FMF_si = lh_engine_FMF_si
        self.rh_engine_FMF_si = rh_engine_FMF_si
        self.time_series = time_series

        # Use these two indices to dissect the data later
        if time_of_interest != []:
            time_index_1 = search_time_index(time_series, time_of_interest[0])
            time_index_2 = search_time_index(time_series, time_of_interest[1])
        else:
            time_index_1 = 0
            time_index_2 = len(time_series)

        # Slice the data into the time frame of interest
        self.vane_AOA_1 = vane_AOA[time_index_1:time_index_2]
        self.Dadc1_bcAlt_meters_1 = Dadc1_bcAlt_meters[time_index_1:time_index_2]
        self.Ahrs1_Roll_1 = Ahrs1_Roll[time_index_1:time_index_2]
        self.Ahrs1_Pitch_1 = Ahrs1_Pitch[time_index_1:time_index_2]
        self.Ahrs1_bRollRate_1 = Ahrs1_bRollRate[time_index_1:time_index_2]
        self.Ahrs1_bPitchRate_1 = Ahrs1_bPitchRate[time_index_1:time_index_2]
        self.Ahrs1_bYawRate_1 = Ahrs1_bYawRate[time_index_1:time_index_2]
        self.total_FL_kg_1 = total_FL_kg[time_index_1:time_index_2]
        self.total_FL_lb_1 = total_FL_lb[time_index_1:time_index_2]
        self.Dadc1_tas_si_1 = Dadc1_tas_si[time_index_1:time_index_2]
        self.Dadc1_sat_si_1 = Dadc1_sat_si[time_index_1:time_index_2]
        self.Dadc1_tat_si_1 = Dadc1_tat_si[time_index_1:time_index_2]
        self.Dadc1_mach_1 = Dadc1_mach[time_index_1:time_index_2]
        self.column_fe_1 = column_fe[time_index_1:time_index_2]
        self.delta_e_1 = delta_e[time_index_1:time_index_2]
        self.delta_a_1 = delta_a[time_index_1:time_index_2]
        self.delta_r_1 = delta_r[time_index_1:time_index_2]
        self.lh_engine_FMF_si_1 = lh_engine_FMF_si[time_index_1:time_index_2]
        self.rh_engine_FMF_si_1 = rh_engine_FMF_si[time_index_1:time_index_2]
        self.time_series_1 = time_series[time_index_1:time_index_2]

    def mass_centroid(self, time:int, benji_pos=288):
        ## gives mass_centroid at time of interest
        ## time is the interval for time iof interest, minimum is 9, maximum is 5183
        ## benji_pos is in inches
        ## benji_pos has reference datum at nose cone, 0 is at the nose cone and 288 is at benji chair

        if not isinstance(time,int):
            raise Exception('time2 is not type integer')
        if not time >= 9:
            raise Exception('time1 must be at least 9')
        if not time <= 5183:
            raise Exception('time2 must be at most the duration of the flight, 5183 seconds')
        if not 0 < benji_pos < 575:
            raise Exception('benji_pos is outside of plane')

        lbs_kg = 0.453592
        inch_m = 0.0254

        # Payload - People, Baggage
        seat_positions = np.array([131,131,214,214,251,251,288,benji_pos,170])*inch_m
        person_masses = self.person_masses #np.array([91,96,79,71,90,93,90,98,83])
        person_moments = seat_positions*person_masses
        baggage = 0 #220*lbs_kg
        baggage_moment = 0 #baggage*moment_arm*lbs_kg*inch_kg

        # Fuel
        self.read_flight_data([time,time+1], self.int_fuel_lbs, self.data_dir)
        self.current_fuel_lbs = self.total_FL_lb_1[-1]
        fuel_moment = (2.853 * self.current_fuel_lbs + 9.896)*lbs_kg*inch_m*100  ## moment to fuel mass equation from data

        # Basic Empty Weight
        self.BEM_kg = 9197.0*lbs_kg
        BEM_moment = 2678893.5*inch_m*lbs_kg

        # mass centroid
        total_moment = np.sum(person_moments) + baggage_moment + fuel_moment + BEM_moment
        self.total_current_mass_kg = np.sum(person_masses) + baggage + self.current_fuel_lbs*lbs_kg + self.BEM_kg
        self.center_mass = total_moment/self.total_current_mass_kg

        # finding coordinate of MAC
        x_LEMAC = 261.56*inch_m
        self.x_cg = self.center_mass - x_LEMAC
        self.x_cg_percent = self.x_cg / (80.98*inch_m)


