import matplotlib.pyplot as plt
import numpy as np
import control
import Plotter


class Solver:

    def __init__(self, aircraft, conditions):
        self.aircraft = aircraft
        self.conditions = conditions
        #symmetrical state space system
        self.A_sym, self.B_sym, self.C_sym, self.D_sym = Solver.calculate_sym_matrices(self, self.aircraft)
        self.sym_ss = control.ss(self.A_sym, self.B_sym, self.C_sym, self.D_sym)
        # print(self.sym_ss)

        #assymetrical state space system
        self.A_asym, self.B_asym, self.C_asym, self.D_asym = Solver.calculate_asym_matrices(self, self.aircraft)
        self.asym_ss = control.ss(self.A_asym, self.B_asym, self.C_asym, self.D_asym)
        # print(self.asym_ss)

        # output time domain
        timeVector = np.linspace(0, 10, 500)

        Ae = np.deg2rad(-5)  # elevator input magnitude
        Aa = np.deg2rad(0)  # aileron input magnitude
        Ar = np.deg2rad(5)  # rudder input magnitude

        self.Us = np.zeros((1, len(timeVector)))  # input matrix for sym
        self.Ua = np.zeros((2, len(timeVector)))  # input matrix for asym

        self.Us[0, 0:500] = Ae  # elevator input: also specify shape here, can add more lines
        self.Ua[0, 0:50] = Aa  # aileron input
        self.Ua[1, 0:25] = -Ar  # rudder input
        self.Ua[1, 25:50] = Ar  # rudder input

        # Compute response

        self.ts, self.ys = control.forced_response(self.sym_ss, T=timeVector, U=self.Us)
        self.ys[0] *= aircraft.V0
        self.ys[3] *= aircraft.V0/aircraft.c
        self.ta, self.ya = control.forced_response(self.asym_ss, T=timeVector, U=self.Ua)
        self.ya[2] *= (2 * aircraft.V0 / aircraft.b)
        self.ya[3] *= (2 * aircraft.V0 / aircraft.b)

    def show_solutions(self):

        plotter = Plotter.Plotter([self.ts, self.ys, self.ta, self.ya, self.Us, self.Ua], [self.A_sym, self.A_asym])
        plotter.plot()
        plotter.plot_poles()


    def calculate_sym_matrices(self, ac):
        C1 = np.array([[-2*ac.muc*ac.c/ac.V0, 0, 0, 0],
                       [0, (ac.CZadot-2*ac.muc)*ac.c/ac.V0, 0, 0],
                       [0, 0, -ac.c/ac.V0, 0],
                       [0, ac.Cmadot*ac.c/ac.V0, 0, -2*ac.muc*ac.KY2*ac.c/ac.V0]])
        C2 = np.array([[ac.CXu, ac.CXa, ac.CZ0, ac.CXq],
                       [ac.CZu, ac.CZa, -ac.CX0, (ac.CZq+2*ac.muc)],
                       [0, 0, 0, 1],
                       [ac.Cmu, ac.Cma, 0, ac.Cmq]])
        C3 = np.array([[ac.CXde],
                       [ac.CZde],
                       [0],
                       [ac.Cmde]])
        A = -np.linalg.inv(C1)@C2
        B = -np.linalg.inv(C1)@C3
        C = np.identity(4)
        D = np.zeros([4, 1])
        return A, B, C, D

    def calculate_asym_matrices(self, ac):
        C1 = np.array([[(ac.CYbdot-2*ac.mub)*ac.b/ac.V0, 0, 0, 0],
                       [0, -0.5*ac.b/ac.V0, 0, 0],
                       [0, 0, -4*ac.mub*ac.KX2*ac.b/ac.V0, 4*ac.mub*ac.KXZ*ac.b/ac.V0],
                       [ac.Cnbdot*ac.b/ac.V0, 0, 4*ac.mub*ac.KXZ*ac.b/ac.V0, -4*ac.mub*ac.KZ2*ac.b/ac.V0]])
        C2 = np.array([[ac.CYb, ac.CL, ac.CYp, (ac.CYr-4*ac.mub)],
                       [0, 0, 1, 0],
                       [ac.Clb, 0, ac.Clp, ac.Clr],
                       [ac.Cnb, 0, ac.Cnp, ac.Cnr]])
        C3 = np.array([[ac.CYda, ac.CYdr],
                       [0, 0],
                       [ac.Clda, ac.Cldr],
                       [ac.Cnda, ac.Cndr]])
        A = -np.linalg.inv(C1)@C2
        B = -np.linalg.inv(C1)@C3
        C = np.identity(4)
        D = np.zeros([4, 2])
        return A, B, C, D


