import numpy as np
import matplotlib.pyplot as plt
class Plotter:

    def __init__(self, data, A):
        self.data = data    # data should be a NxM matrix, where n is the number of different responses and M is the
                            # length of each response in timesteps
        self.A = A # [A_sym, A_asym]

    def plot(self):

        # input arrays
        e_arr = np.rad2deg(self.data[4][0, :])
        a_arr = np.rad2deg(self.data[5][0, :])
        rd_arr = np.rad2deg(self.data[5][1, :])

        # sym arrays
        u_arr = self.data[1][0, :]
        aoa_arr = np.rad2deg(self.data[1][1, :])
        pitch_arr = np.rad2deg(self.data[1][2, :])
        q_arr = np.rad2deg(self.data[1][3, :])

        # asym arrays
        beta_arr = np.rad2deg(self.data[3][0, :])
        phi_arr = np.rad2deg(self.data[3][1, :])
        p_arr = np.rad2deg(self.data[3][2, :])
        r_arr = np.rad2deg(self.data[3][3, :])

        # Plot the response
        fig, plots = plt.subplots(3, 4, figsize=(10, 8))

        plots[0, 0].plot(self.data[0], e_arr, label='Elevator Input')
        plots[0, 0].set_ylabel('elevator input (deg)')

        plots[0, 1].plot(self.data[2], a_arr, label='Aileron Input')
        plots[0, 1].set_ylabel('aileron input (deg)')

        plots[0, 2].plot(self.data[2], rd_arr, label='Rudder Input')
        plots[0, 2].set_ylabel('rudder input (deg)')

        plots[1, 0].plot(self.data[0], u_arr, label='Speed Deviation')
        plots[1, 0].set_ylabel('dev')

        plots[1, 1].plot(self.data[0], aoa_arr, label='Angle Of Attack')
        plots[1, 1].set_ylabel('aoa deg')

        plots[1, 2].plot(self.data[0], pitch_arr, label='Pitch Angle')
        plots[1, 2].set_ylabel('pitch deg')

        plots[1, 3].plot(self.data[0], q_arr, label='Pitch Rate')
        plots[1, 3].set_ylabel('pitch deg/s')

        plots[2, 0].plot(self.data[2], beta_arr, label='Sideslip Angle')
        plots[2, 0].set_ylabel('slip deg')

        plots[2, 1].plot(self.data[2], phi_arr, label='Roll Angle')
        plots[2, 1].set_ylabel('roll deg')

        plots[2, 2].plot(self.data[2], p_arr, label='Roll Rate')
        plots[2, 2].set_ylabel('roll deg/s')

        plots[2, 3].plot(self.data[2], r_arr, label='Yaw Rate')
        plots[2, 3].set_ylabel('yaw deg/s')

        fig.suptitle('Simulation Data')
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.show(block=False)
    
    def plot_poles(self):
        eig_val_sym , eig_vec_sym = np.linalg.eig(self.A[0])
        eig_val_asym, eig_vec_asym = np.linalg.eig(self.A[1])

        print("-----------------------------------------")
        print("Symmetrical eigenvalues: ", eig_val_sym)
        for i in range(len(eig_val_sym)):
            print(f"Symmetrical eigenvectors {i}: ", eig_vec_sym[:, i])
        print("Asymmetrical eigenvalues: ", eig_val_asym)
        for i in range(len(eig_val_asym)):
            print(f"Asymmetrical eigenvectors {i}: ", eig_vec_asym[:, i])
        print("-----------------------------------------")
        
        plt.figure(figsize=(12, 6))

        plt.subplot(1, 2, 1)
        plt.scatter(np.real(eig_val_sym), np.imag(eig_val_sym), marker='x', color='r', label='Poles', s=100)
        plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
        plt.axvline(0, color='black', linewidth=0.5, linestyle='--')
        plt.xlabel('Real')
        plt.ylabel('Imaginary')
        plt.title('Poles of Symmetrical System')
        plt.legend()
        plt.grid(True)

        plt.subplot(1, 2, 2)
        plt.scatter(np.real(eig_val_asym), np.imag(eig_val_asym), marker='x', color='b', label='Poles', s=100)
        plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
        plt.axvline(0, color='black', linewidth=0.5, linestyle='--')
        plt.xlabel('Real')
        plt.ylabel('Imaginary')
        plt.title('Poles of Asymmetrical System')
        plt.legend()
        plt.grid(True)

        plt.suptitle('Poles of Symmetrical and Asymmetrical Systems')
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.show(block=False)
        input('Press Enter to close plots')