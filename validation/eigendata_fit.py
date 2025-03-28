import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize
import scipy.signal
import scipy.fftpack


class eigendata:
    def __init__(self, time, data, state, fit_type, sym_or_asym, aircraft): # fit_type = 0 for damped oscillation, 1 for damped
        self.time = time
        self.data = data[state]
        self.state = state
        self.fit_type = fit_type
        self.sym_or_asym = sym_or_asym
        self.aircraft = aircraft
        if sym_or_asym == 'sym':
            self.char_len = aircraft.c
        elif sym_or_asym == 'asym':
            self.char_len = aircraft.b

        self.t = self.shift_time()
        if fit_type == 0:
            self.guess_damped_oscil()
            self.fit_damped_oscil()
            self.determination_coef(self.data, self.y)
            self.nondim_coeff(self.paras)
            self.print_paras(self.paras)
            self.plot()
        elif fit_type == 1:
            self.guess_damped()
            self.fit_damped()
            self.determination_coef(self.data, self.y)
            self.nondim_coeff(self.paras)
            self.print_paras(self.paras)
            self.plot()

    def shift_time(self):
        t = self.time - self.time[0]
        return t

    def func_exp_cos(self, t, a, b, c, d, e):
        return a * np.exp(b * t) * np.cos(c * t + d) + e

    def func_exp(self, t, a, b, c):
        return a * np.exp(b * t) + c

    def est_freq_fft(self, t, y):
        Y = np.fft.fft(y)
        frequencies = np.fft.fftfreq(len(t), d=(t[1] - t[0]))  # Compute frequency bins
        positive_frequencies = frequencies[:len(frequencies)//2]
        positive_Y = np.abs(Y[:len(Y)//2])
        plt.plot(positive_frequencies, positive_Y)
        plt.show()
        return positive_frequencies[np.argmax(positive_Y)]

    def guess_damped_oscil(self):
        a_guess = (max(self.data) - min(self.data))/2
        b_guess = -0.01
        c_guess =  2 * np.pi / (self.t[scipy.signal.find_peaks(self.data)[0][1]] - self.t[scipy.signal.find_peaks(self.data)[0][0]])
        #c_guess = 2 * np.pi / self.est_freq_fft(self.t, self.data)
        #c_guess = 1
        d_guess = 0
        e_guess = (max(self.data) + min(self.data))/2
        self.guess = [a_guess, b_guess, c_guess, d_guess, e_guess]

    def guess_damped(self):
        a_guess = -(max(self.data) - min(self.data))/2
        b_guess = -0.01
        c_guess = (max(self.data) + min(self.data))/2
        self.guess = [a_guess, b_guess, c_guess]

    def fit_damped_oscil(self):
        self.paras, _ = scipy.optimize.curve_fit(self.func_exp_cos, self.t, self.data, p0=self.guess, maxfev=20000)
        self.y = self.func_exp_cos(self.t, *self.paras)

    def fit_damped(self):
        self.paras, _ = scipy.optimize.curve_fit(self.func_exp, self.t, self.data, p0=self.guess, maxfev=20000)
        self.y = self.func_exp(self.t, *self.paras)

    def determination_coef(self, y_true, y_pred):
        mean_y_true = np.mean(y_true)
        ss_total = np.sum((y_true - mean_y_true) ** 2)  # Total sum of squares
        ss_residual = np.sum((y_true - y_pred) ** 2)    # Residual sum of squares
        self.R2 = 1 - (ss_residual / ss_total)

    def nondim_coeff(self, paras):
        if self.fit_type == 0:
            self.nd_decay_rate = paras[1] #* self.char_len / self.aircraft.V0
            self.nd_ang_freq = paras[2] #* self.char_len / self.aircraft.V0
        else:
            self.nd_decay_rate = paras[1] #* self.char_len / self.aircraft.V0

    def print_paras(self, paras):
        if self.fit_type == 0:
            print('=====Damped Oscillation=====')
            print('Coefficient of determination: ' + str(self.R2))
            print(self.paras)
            print('Non-dimensional Parameters:')
            print('Decay rate (zeta, real):' + str(self.nd_decay_rate))
            print('Angular frequency (omega, imag):' + str(self.nd_ang_freq))
            print('Time constant (tau):' + str(1/self.nd_decay_rate))
            print('Natural period:' + str((2*np.pi)/self.nd_ang_freq))
        else:
            print('=====Damped Curve=====')
            print('Coefficient of determination: ' + str(self.R2))
            print(self.paras)
            print('Non-dimensional Parameters:')
            print('Decay rate (zeta, real):' + str(self.nd_decay_rate))
            print('Time constant (tau):' + str(1/self.nd_decay_rate))

    def plot(self):
        plt.figure(figsize=(10,6))
        plt.plot(self.t, self.data, label='Real')
        plt.plot(self.t, self.y, label="Fitted")
        plt.xlabel('Time [s]')
        plt.ylabel('State')
        plt.title(self.state + ', R^2: ' + str(self.R2))
        plt.legend()
        plt.show()


    
