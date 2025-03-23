import numpy as np
import matplotlib.pyplot as plt
import control
import warnings
class compare_validation:

    def __init__(self, aircraft, compare_interval_sec, sym_ss, asym_ss):
        self.real_data = aircraft
        self.sym_ss = sym_ss
        self.asym_ss = asym_ss
        self.fs = 10 # Hz
        self.compare_interval_idx = [int(compare_interval_sec[0]*10), int(compare_interval_sec[1]*10)]
        self.compare_interval_sec = compare_interval_sec

        self.sys_data = {}

        self.compare_sym()
        self.compare_asym()
        self.plot_compare_sym()
        self.plot_compare_asym()

    def compare_sym(self):

        # output time domain
        self.real_time = self.real_data.time_series[self.compare_interval_idx[0]:self.compare_interval_idx[1]]
        self.timeVector = self.real_time - self.real_time[0]
        sim_points = len(self.timeVector)
        if len(self.timeVector) != len(self.real_time):
            print(len(self.timeVector))
            print(len(self.real_time))
            raise ValueError('Time vector length mismatch')

        Ae = self.real_data.delta_e[self.compare_interval_idx[0]:self.compare_interval_idx[1]] # elevator input time series
        self.Us = np.zeros(sim_points)
        self.Us[0:sim_points] = np.deg2rad(Ae) - self.real_data.delta_e0  # elevator input reshape

        # Compute response
        self.ts, self.ys = control.forced_response(self.sym_ss, T=self.timeVector, U=self.Us)
        self.ys[0] *= self.real_data.V0
        self.ys[3] *= self.real_data.V0/self.real_data.c

        self.sys_data['sim_tas_si'] = self.ys[0] + self.real_data.V0
        self.sys_data['sim_aoa_deg'] = np.rad2deg(self.ys[1]) + np.rad2deg(self.real_data.alpha0)
        self.sys_data['sim_pitch_deg'] = np.rad2deg(self.ys[2]) + np.rad2deg(self.real_data.th0)
        self.sys_data['sim_pitch_rate_deg'] = np.rad2deg(self.ys[3]) + np.rad2deg(self.real_data.q0)
        self.sys_data['sim_delta_e_deg'] = self.real_data.delta_e[self.compare_interval_idx[0]:self.compare_interval_idx[1]] - np.rad2deg(self.real_data.delta_e0)
        self.sys_data['real_delta_e_deg'] = self.real_data.delta_e[self.compare_interval_idx[0]:self.compare_interval_idx[1]]
        self.sys_data['real_tas_si'] = self.real_data.Dadc1_tas_si[self.compare_interval_idx[0]:self.compare_interval_idx[1]]
        self.sys_data['real_aoa_deg'] = self.real_data.vane_AOA[self.compare_interval_idx[0]:self.compare_interval_idx[1]]
        self.sys_data['real_pitch_deg'] = self.real_data.Ahrs1_Pitch[self.compare_interval_idx[0]:self.compare_interval_idx[1]]
        self.sys_data['real_pitch_rate_deg'] = self.real_data.Ahrs1_bPitchRate[self.compare_interval_idx[0]:self.compare_interval_idx[1]]
        self.sys_data['real_time'] = self.real_time
        self.sys_data['sim_time'] = self.timeVector


    def compare_asym(self):

        sim_points = len(self.timeVector)

        Aa = self.real_data.delta_a[self.compare_interval_idx[0]:self.compare_interval_idx[1]] # aileron input time series
        Ar = self.real_data.delta_r[self.compare_interval_idx[0]:self.compare_interval_idx[1]] # rudder input time series
        self.Ua = np.zeros((2, sim_points))
        self.Ua[0, 0:sim_points] = - (np.deg2rad(Aa) - self.real_data.delta_a0) # aileron input
        self.Ua[1, 0:sim_points] = - (np.deg2rad(Ar) - self.real_data.delta_r0) # rudder input

        # Compute response
        self.ta, self.ya = control.forced_response(self.asym_ss, T=self.timeVector, U=self.Ua)
        self.ya[2] *= (2 * self.real_data.V0 / self.real_data.b)
        self.ya[3] *= (2 * self.real_data.V0 / self.real_data.b)

        self.sys_data['sim_delta_a_deg'] = self.real_data.delta_a[self.compare_interval_idx[0]:self.compare_interval_idx[1]] - np.rad2deg(self.real_data.delta_a0)
        self.sys_data['sim_delta_r_deg'] = self.real_data.delta_r[self.compare_interval_idx[0]:self.compare_interval_idx[1]] - np.rad2deg(self.real_data.delta_r0)
        self.sys_data['sim_sideslip_deg'] = np.rad2deg(self.ya[0])
        self.sys_data['sim_roll_deg'] = np.rad2deg(self.ya[1]) + np.rad2deg(self.real_data.phi0)
        self.sys_data['sim_roll_rate_deg'] = np.rad2deg(self.ya[2]) + np.rad2deg(self.real_data.p0)
        self.sys_data['sim_yaw_rate_deg'] = np.rad2deg(self.ya[3]) + np.rad2deg(self.real_data.r0)
        self.sys_data['real_roll_deg'] = self.real_data.Ahrs1_Roll[self.compare_interval_idx[0]:self.compare_interval_idx[1]]
        self.sys_data['real_roll_rate_deg'] = self.real_data.Ahrs1_bRollRate[self.compare_interval_idx[0]:self.compare_interval_idx[1]]
        self.sys_data['real_yaw_rate_deg'] = self.real_data.Ahrs1_bYawRate[self.compare_interval_idx[0]:self.compare_interval_idx[1]]
        self.sys_data['real_delta_a_deg'] = self.real_data.delta_a[self.compare_interval_idx[0]:self.compare_interval_idx[1]]
        self.sys_data['real_delta_r_deg'] = self.real_data.delta_r[self.compare_interval_idx[0]:self.compare_interval_idx[1]]

    # Symmetrical motion
    def plot_compare_sym(self):
        # Plot the response
        fig, plots = plt.subplots(5, 1, figsize=(10, 8))

        # Elevator Input
        plots[0].plot(self.sys_data['sim_time'], self.sys_data['sim_delta_e_deg'], label='Bias Removed')
        plots[0].plot(self.sys_data['sim_time'], self.sys_data['real_delta_e_deg'], label='Real Input')
        plots[0].set_ylabel('Elevator Input (deg)')
        plots[0].legend()

        # True Airspeed
        plots[1].plot(self.sys_data['sim_time'], self.sys_data['sim_tas_si'], label='Sim')
        plots[1].plot(self.sys_data['sim_time'], self.sys_data['real_tas_si'], label='Real')
        plots[1].set_ylabel('True Airspeed (m/s)')
        plots[1].legend()

        # Angle of Attack (AOA)
        plots[2].plot(self.sys_data['sim_time'], self.sys_data['sim_aoa_deg'], label='Sim')
        plots[2].plot(self.sys_data['sim_time'], self.sys_data['real_aoa_deg'], label='Real')
        plots[2].set_ylabel('AOA (deg)')
        plots[2].legend()

        # Pitch Angle
        plots[3].plot(self.sys_data['sim_time'], self.sys_data['sim_pitch_deg'], label='Sim')
        plots[3].plot(self.sys_data['sim_time'], self.sys_data['real_pitch_deg'], label='Real')
        plots[3].set_ylabel('Pitch angle (deg)')
        plots[3].legend()

        # Pitch Rate
        plots[4].plot(self.sys_data['sim_time'], self.sys_data['sim_pitch_rate_deg'], label='Sim')
        plots[4].plot(self.sys_data['sim_time'], self.sys_data['real_pitch_rate_deg'], label='Real')
        plots[4].set_ylabel('Pitch rate (deg/s)')
        plots[4].legend()

        fig.suptitle(f'Simulation vs Real Flight (Symmetrical Motion) t={self.compare_interval_sec[0]} to t={self.compare_interval_sec[1]} sec')
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.show(block=False)
        # input('Press Enter to close plots')


    # Asymmetrical motion
    def plot_compare_asym(self):
        # Plot the response
        fig, plots = plt.subplots(6, 1, figsize=(10, 8))

        plots[0].plot(self.sys_data['sim_time'], self.sys_data['sim_delta_a_deg'], label='Sim')
        plots[0].plot(self.sys_data['sim_time'], self.sys_data['real_delta_a_deg'], label='Real')
        plots[0].set_ylabel('Aileron Input (deg)')
        plots[0].legend()

        plots[1].plot(self.sys_data['sim_time'], self.sys_data['sim_delta_r_deg'], label='Sim')
        plots[1].plot(self.sys_data['sim_time'], self.sys_data['real_delta_r_deg'], label='Real')
        plots[1].set_ylabel('Rudder Input (deg)')
        plots[1].legend()

        plots[2].plot(self.sys_data['sim_time'], self.sys_data['sim_sideslip_deg'], label='Sim')
        plots[2].set_ylabel('Sideslip angle (deg)')
        plots[2].legend()

        plots[3].plot(self.sys_data['sim_time'], self.sys_data['sim_roll_deg'], label='Sim')
        plots[3].plot(self.sys_data['sim_time'], self.sys_data['real_roll_deg'], label='Real')
        plots[3].set_ylabel('Roll angle (deg)')
        plots[3].legend()

        plots[4].plot(self.sys_data['sim_time'], self.sys_data['sim_roll_rate_deg'], label='Sim')
        plots[4].plot(self.sys_data['sim_time'], self.sys_data['real_roll_rate_deg'], label='Real')
        plots[4].set_ylabel('Roll rate (deg/s)')
        plots[4].legend()

        plots[5].plot(self.sys_data['sim_time'], self.sys_data['sim_yaw_rate_deg'], label='Sim')
        plots[5].plot(self.sys_data['sim_time'], self.sys_data['real_yaw_rate_deg'], label='Real')
        plots[5].set_ylabel('Yaw rate (deg/s)')
        plots[5].legend()

        fig.suptitle(f'Simulation vs Real Flight (Asymmetrical Motion) t={self.compare_interval_sec[0]} to t={self.compare_interval_sec[1]} sec')
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.show(block=False)
        input('Press Enter to close plots')
    