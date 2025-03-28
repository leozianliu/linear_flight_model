import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

class stat_ansys():
    def __init__(self, sys_data):
        self.sys_data = sys_data
        self.calc_residual()
        self.cross_corr()
        self.print_R2()
        self.plot_corr_sym()
        self.plot_corr_asym()

    def determination_coef(self, y_true, y_pred):
        mean_y_true = np.mean(y_true)
        ss_total = np.sum((y_true - mean_y_true) ** 2)
        ss_residual = np.sum((y_true - y_pred) ** 2)
        R2 = 1 - (ss_residual / ss_total)
        return R2

    def print_R2(self):
        R2_1 = self.determination_coef(self.sys_data['real_tas_si'], self.sys_data['sim_tas_si'])
        R2_2 = self.determination_coef(self.sys_data['real_aoa_deg'], self.sys_data['sim_aoa_deg'])
        R2_3 = self.determination_coef(self.sys_data['real_pitch_deg'], self.sys_data['sim_pitch_deg'])
        R2_4 = self.determination_coef(self.sys_data['real_pitch_rate_deg'], self.sys_data['sim_pitch_rate_deg'])
        R2_5 = self.determination_coef(self.sys_data['real_roll_deg'], self.sys_data['sim_roll_deg'])
        R2_6 = self.determination_coef(self.sys_data['real_roll_rate_deg'], self.sys_data['sim_roll_rate_deg'])
        R2_7 = self.determination_coef(self.sys_data['real_yaw_rate_deg'], self.sys_data['sim_yaw_rate_deg'])

        print(f'R2 for TAS: {R2_1}')
        print(f'R2 for AOA: {R2_2}')
        print(f'R2 for Pitch: {R2_3}')
        print(f'R2 for Pitch Rate: {R2_4}')
        print(f'R2 for Roll: {R2_5}')
        print(f'R2 for Roll Rate: {R2_6}')
        print(f'R2 for Yaw Rate: {R2_7}')

    def calc_residual(self):
        self.residual_tas = self.sys_data['sim_tas_si'] - self.sys_data['real_tas_si']
        self.residual_aoa = self.sys_data['sim_aoa_deg'] - self.sys_data['real_aoa_deg']
        self.residual_pitch = self.sys_data['sim_pitch_deg'] - self.sys_data['real_pitch_deg']
        self.residual_pitch_rate = self.sys_data['sim_pitch_rate_deg'] - self.sys_data['real_pitch_rate_deg']
        self.residual_roll = self.sys_data['sim_roll_deg'] - self.sys_data['real_roll_deg']
        self.residual_roll_rate = self.sys_data['sim_roll_rate_deg'] - self.sys_data['real_roll_rate_deg']
        self.residual_yaw_rate = self.sys_data['sim_yaw_rate_deg'] - self.sys_data['real_yaw_rate_deg']
        self.input_delta_e = self.sys_data['real_delta_e_deg']
        self.input_delta_a = self.sys_data['real_delta_a_deg']
        self.input_delta_r = self.sys_data['real_delta_r_deg']
        self.timeVector = self.sys_data['sim_time']

    def cross_corr(self):
        self.acf = signal.correlation_lags(len(self.timeVector), len(self.timeVector))
        corr_tas = signal.correlate(self.residual_tas - np.mean(self.residual_tas), self.residual_tas - np.mean(self.residual_tas), mode='full')
        self.corr_tas = corr_tas / np.max(corr_tas)
        corr_pitch = signal.correlate(self.residual_pitch - np.mean(self.residual_pitch), self.residual_pitch - np.mean(self.residual_pitch), mode='full')
        self.corr_pitch = corr_pitch / np.max(corr_pitch)
        corr_aoa = signal.correlate(self.residual_aoa - np.mean(self.residual_aoa), self.residual_aoa - np.mean(self.residual_aoa), mode='full')
        self.corr_aoa = corr_aoa / np.max(corr_aoa)
        corr_pitch_rate = signal.correlate(self.residual_pitch_rate - np.mean(self.residual_pitch_rate), self.residual_pitch_rate - np.mean(self.residual_pitch_rate), mode='full')
        self.corr_pitch_rate = corr_pitch_rate / np.max(corr_pitch_rate)
        corr_roll = signal.correlate(self.residual_roll - np.mean(self.residual_roll), self.residual_roll - np.mean(self.residual_roll), mode='full')
        self.corr_roll = corr_roll / np.max(corr_roll)
        corr_roll_rate = signal.correlate(self.residual_roll_rate - np.mean(self.residual_roll_rate), self.residual_roll_rate - np.mean(self.residual_roll_rate), mode='full')
        self.corr_roll_rate = corr_roll_rate / np.max(corr_roll_rate)
        corr_yaw_rate = signal.correlate(self.residual_yaw_rate - np.mean(self.residual_yaw_rate), self.residual_yaw_rate - np.mean(self.residual_yaw_rate), mode='full')
        self.corr_yaw_rate = corr_yaw_rate / np.max(corr_yaw_rate)

        corr_tas_de = signal.correlate(self.residual_tas - np.mean(self.residual_tas), self.input_delta_e - np.mean(self.input_delta_e), mode='full')
        norm_factor0 = np.sqrt(np.sum(self.residual_tas**2) * np.sum(self.input_delta_e**2))
        self.corr_tas_de = corr_tas_de / norm_factor0
        corr_pitch_de = signal.correlate(self.residual_pitch - np.mean(self.residual_pitch), self.input_delta_e - np.mean(self.input_delta_e), mode='full')
        norm_factor1 = np.sqrt(np.sum(self.residual_pitch**2) * np.sum(self.input_delta_e**2))
        self.corr_pitch_de = corr_pitch_de / norm_factor1
        corr_aoa_de = signal.correlate(self.residual_aoa - np.mean(self.residual_aoa), self.input_delta_e - np.mean(self.input_delta_e), mode='full')
        norm_factor2 = np.sqrt(np.sum(self.residual_aoa**2) * np.sum(self.input_delta_e**2))
        self.corr_aoa_de = corr_aoa_de / norm_factor2
        corr_pitch_rate_de = signal.correlate(self.residual_pitch_rate - np.mean(self.residual_pitch_rate), self.input_delta_e - np.mean(self.input_delta_e), mode='full')
        norm_factor3 = np.sqrt(np.sum(self.residual_pitch_rate**2) * np.sum(self.input_delta_e**2))
        self.corr_pitch_rate_de = corr_pitch_rate_de / norm_factor3
        corr_roll_da = signal.correlate(self.residual_roll - np.mean(self.residual_roll), self.input_delta_a - np.mean(self.input_delta_a), mode='full')
        norm_factor4 = np.sqrt(np.sum(self.residual_roll**2) * np.sum(self.input_delta_a**2))
        self.corr_roll_da = corr_roll_da / norm_factor4
        corr_roll_dr = signal.correlate(self.residual_roll - np.mean(self.residual_roll), self.input_delta_r - np.mean(self.input_delta_r), mode='full')
        norm_factor5 = np.sqrt(np.sum(self.residual_roll**2) * np.sum(self.input_delta_r**2))
        self.corr_roll_dr = corr_roll_dr / norm_factor5
        corr_roll_rate_da = signal.correlate(self.residual_roll_rate - np.mean(self.residual_roll_rate), self.input_delta_a - np.mean(self.input_delta_a), mode='full')
        norm_factor6 = np.sqrt(np.sum(self.residual_roll_rate**2) * np.sum(self.input_delta_a**2))
        self.corr_roll_rate_da = corr_roll_rate_da / norm_factor6
        corr_roll_rate_dr = signal.correlate(self.residual_roll_rate - np.mean(self.residual_roll_rate), self.input_delta_r - np.mean(self.input_delta_r), mode='full')
        norm_factor7 = np.sqrt(np.sum(self.residual_roll_rate**2) * np.sum(self.input_delta_r**2))
        self.corr_roll_rate_dr = corr_roll_rate_dr / norm_factor7
        corr_yaw_rate_da = signal.correlate(self.residual_yaw_rate - np.mean(self.residual_yaw_rate), self.input_delta_a - np.mean(self.input_delta_a), mode='full')
        norm_factor8 = np.sqrt(np.sum(self.residual_yaw_rate**2) * np.sum(self.input_delta_a**2))
        self.corr_yaw_rate_da = corr_yaw_rate_da / norm_factor8
        corr_yaw_rate_dr = signal.correlate(self.residual_yaw_rate - np.mean(self.residual_yaw_rate), self.input_delta_r - np.mean(self.input_delta_r), mode='full')
        norm_factor9 = np.sqrt(np.sum(self.residual_yaw_rate**2) * np.sum(self.input_delta_r**2))
        self.corr_yaw_rate_dr = corr_yaw_rate_dr / norm_factor9

    def plot_corr_sym(self):
        confidence_interval = 1.96 / np.sqrt(len(self.timeVector))
        #plt.figure(figsize=(15, 20))
        plt.figure()

        # Autocorrelation plots
        plt.subplot(5, 1, 1)
        plt.plot(self.acf, self.corr_tas, color='blue')
        # plt.xlabel('Lag')
        plt.ylabel('Autocorrelation')
        plt.title('Autocorrelation of TAS Residual')
        plt.grid(True)
        plt.axhspan(-confidence_interval, confidence_interval, alpha=0.2, color='gray')
        plt.axvline(x=0, color='red', linestyle='--', alpha=0.7)

        plt.subplot(5, 1, 2)
        plt.plot(self.acf, self.corr_aoa, color='blue')
        # plt.xlabel('Lag')
        plt.ylabel('Autocorrelation')
        plt.title('Autocorrelation of AOA Residual')
        plt.grid(True)
        plt.axhspan(-confidence_interval, confidence_interval, alpha=0.2, color='gray')
        plt.axvline(x=0, color='red', linestyle='--', alpha=0.7)

        plt.subplot(5, 1, 3)
        plt.plot(self.acf, self.corr_pitch, color='blue')
        # plt.xlabel('Lag')
        plt.ylabel('Autocorrelation')
        plt.title('Autocorrelation of Pitch Residual')
        plt.grid(True)
        plt.axhspan(-confidence_interval, confidence_interval, alpha=0.2, color='gray')
        plt.axvline(x=0, color='red', linestyle='--', alpha=0.7)

        plt.subplot(5, 1, 4)
        plt.plot(self.acf, self.corr_pitch_rate, color='blue')
        # plt.xlabel('Lag')
        plt.ylabel('Autocorrelation')
        plt.title('Autocorrelation of Pitch Rate Residual')
        plt.grid(True)
        plt.axhspan(-confidence_interval, confidence_interval, alpha=0.2, color='gray')
        plt.axvline(x=0, color='red', linestyle='--', alpha=0.7)

        # Cross-correlation plots for Roll, Roll Rate, and Yaw Rate
        plt.subplot(5, 1, 5)
        plt.plot(self.acf, self.corr_tas_de, color='red', label='TAS vs Delta E')
        plt.plot(self.acf, self.corr_pitch_de, color='blue', label='Pitch vs Delta E')
        plt.plot(self.acf, self.corr_aoa_de, color='green', label='AOA vs Delta E')
        plt.xlabel('Lag')
        plt.ylabel('Cross-correlation')
        plt.title('Cross-correlation with Control Inputs')
        plt.legend()
        plt.grid(True)
        plt.axhspan(-confidence_interval, confidence_interval, alpha=0.2, color='gray')
        plt.axvline(x=0, color='red', linestyle='--', alpha=0.7)

        # plt.tight_layout()
        plt.show(block=False)

    def plot_corr_asym(self):
        confidence_interval = 1.96 / np.sqrt(len(self.timeVector))
        #plt.figure(figsize=(15, 20))
        plt.figure()

        # Roll, Roll Rate, and Yaw Rate Autocorrelation
        plt.subplot(4, 1, 1)
        plt.plot(self.acf, self.corr_roll, color='blue')
        # plt.xlabel('Lag')
        plt.ylabel('Autocorrelation')
        plt.title('Autocorrelation of Roll Residual')
        plt.grid(True)
        plt.axhspan(-confidence_interval, confidence_interval, alpha=0.2, color='gray')
        plt.axvline(x=0, color='red', linestyle='--', alpha=0.7)

        plt.subplot(4, 1, 2)
        plt.plot(self.acf, self.corr_roll_rate, color='blue')
        # plt.xlabel('Lag')
        plt.ylabel('Autocorrelation')
        plt.title('Autocorrelation of Roll Rate Residual')
        plt.grid(True)
        plt.axhspan(-confidence_interval, confidence_interval, alpha=0.2, color='gray')
        plt.axvline(x=0, color='red', linestyle='--', alpha=0.7)

        plt.subplot(4, 1, 3)
        plt.plot(self.acf, self.corr_yaw_rate, color='blue')
        # plt.xlabel('Lag')
        plt.ylabel('Autocorrelation')
        plt.title('Autocorrelation of Yaw Rate Residual')
        plt.grid(True)
        plt.axhspan(-confidence_interval, confidence_interval, alpha=0.2, color='gray')
        plt.axvline(x=0, color='red', linestyle='--', alpha=0.7)

        # Cross-correlation plots for Roll, Roll Rate, and Yaw Rate
        plt.subplot(4, 1, 4)
        plt.plot(self.acf, self.corr_roll_da, color='red', label='Roll vs Aileron')
        plt.plot(self.acf, self.corr_roll_dr, color='blue', label='Roll vs Rudder')
        plt.plot(self.acf, self.corr_roll_rate_da, color='green', label='Roll Rate vs Aileron')
        plt.plot(self.acf, self.corr_roll_rate_dr, color='purple', label='Roll Rate vs Rudder')
        plt.plot(self.acf, self.corr_yaw_rate_da, color='orange', label='Yaw Rate vs Aileron')
        plt.plot(self.acf, self.corr_yaw_rate_dr, color='black', label='Yaw Rate vs Rudder')
        plt.xlabel('Lag')
        plt.ylabel('Cross-correlation')
        plt.title('Cross-correlation with Control Inputs')
        plt.legend(loc='upper left')
        plt.grid(True)
        plt.axhspan(-confidence_interval, confidence_interval, alpha=0.2, color='gray')
        plt.axvline(x=0, color='red', linestyle='--', alpha=0.7)

        # plt.tight_layout()
        plt.show()

