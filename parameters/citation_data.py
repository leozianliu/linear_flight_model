# Citation 550 - Linear simulation
import math
import numpy as np

def power(a, b):
    return a ** b

def Data():

    aircraft_data_int = {}
    conditions_data_int = {}

    name = "TU Delft Flying Research Lab PH-LAB"
    aircraft_data_int["name"] = name

    # ==========Change me!!!==========
    data_dir = "data_our_2025/FTISxprt-20250304_084412.mat"
    #data_dir = "Reference_Data_2023/FTISxprt-20230808_083623.mat"
    #data_dir = "data_other_2025/FTISxprt-20250304_125412.mat"
    aircraft_data_int["data_dir"] = data_dir

    # Initial fuel mass in lbs
    aircraft_data_int["int_fuel_lbs"] = 4100 # lbs, our 2025
    #aircraft_data_int["int_fuel_lbs"] = 2800 # lbs, ref 2023

    # Passenger weights in kg
    person_masses = np.array([91,96,79,71,90,93,90,98,83]) # our 2025
    #person_masses = np.array([91,96,85,58,70,75,87,77,125]) # other 2025
    #person_masses = np.array([101, 90, 67, 70, 79, 69, 75, 82, 82]) # ref 2023
    aircraft_data_int["person_masses"] = person_masses

    # Aerodynamic properties
    e = 0.8113830949469385  # Oswald factor [ ]
    aircraft_data_int["e"] = e
    CD0 = 0.02027336226684088  # Zero lift drag coefficient [ ]
    aircraft_data_int["CD0"] = CD0
    CLa = 4.455693334372708  # Slope of CL-alpha curve [ 1/rad ]
    aircraft_data_int["CLa"] = CLa

    # Longitudinal stability
    Cma = -0.7617783603698869  # longitudinal stability [ ]
    aircraft_data_int["Cma"] = Cma
    Cmde = -1.5861151999545298  # elevator effectiveness [ ] 
    aircraft_data_int["Cmde"] = Cmde



    # ----------------------------------------------------------------------------------------------------------------------
    # ABOVE THIS ARE EXAMPLE VALUES - NEED TO BE CALCULATED
    # ----------------------------------------------------------------------------------------------------------------------

    # slop
    pi = math.pi

    # Aircraft geometry
    S = 30.00  # wing area [m^2]
    aircraft_data_int["S"] = S
    Sh = 0.2 * S  # stabiliser area [m^2]
    aircraft_data_int["Sh"] = Sh
    Sh_S = Sh / S  # [ ]
    aircraft_data_int["Sh_S"] = Sh_S
    lh = 0.71 * 5.968  # tail length [m]
    aircraft_data_int["lh"] = lh
    c = 2.0569  # mean aerodynamic chord [m]
    aircraft_data_int["c"] = c
    lh_c = lh / c  # [ ]
    aircraft_data_int["lh_c"] = lh_c
    b = 15.911  # wing span [m]
    aircraft_data_int["b"] = b
    bh = 5.791  # stabiliser span [m]
    aircraft_data_int["bh"] = bh
    A = b ** 2 / S  # wing aspect ratio [ ]
    aircraft_data_int["A"] = A
    Ah = bh ** 2 / Sh  # stabiliser aspect ratio [ ]
    aircraft_data_int["Ah"] = Ah
    Vh_V = 1  # [ ]
    aircraft_data_int["Vh_V"] = Vh_V
    ih = -2 * pi / 180  # stabiliser angle of incidence [rad]
    aircraft_data_int["ih"] = ih

    # Constant values concerning atmosphere and gravity

    rho0 = 1.2250  # air density at sea level [kg/m^3]
    conditions_data_int["rho0"] = rho0
    lbda = -0.0065  # temperature gradient in ISA [K/m]
    conditions_data_int["lbda"] = lbda
    Temp0 = 288.15  # temperature at sea level in ISA [K]
    conditions_data_int["Temp0"] = Temp0
    R = 287.05  # specific gas constant [m^2/sec^2K]
    conditions_data_int["R"] = R
    g = 9.81  # [m/sec^2] (gravity constant)
    conditions_data_int["g"] = g

    # # air density [kg/m^3]
    # rho = rho0 * power(((1 + (lbda * hp0 / Temp0))), (-((g / (lbda * R)) + 1)))
    # conditions_data_int["rho"] = rho
    # W = m * g  # [N]       (aircraft weight)
    # aircraft_data_int["W"] = W

    # Constant values concerning aircraft inertia

    # muc = m / (rho * S * c)
    # aircraft_data_int["muc"] = muc
    # mub = m / (rho * S * b)
    # aircraft_data_int["mub"] = mub
    KX2 = 0.019  # K_x_squared
    aircraft_data_int["KX2"] = KX2
    KZ2 = 0.042  # K_z_squared
    aircraft_data_int["KZ2"] = KZ2
    KXZ = 0.002
    aircraft_data_int["KXZ"] = KXZ
    KY2 = 1.25 * 1.114  # K_y_squared
    aircraft_data_int["KY2"] = KY2

    # Aerodynamic constants

    Cmac = 0  # Moment coefficient about the aerodynamic centre [ ]
    aircraft_data_int["Cmac"] = Cmac
    CNwa = CLa  # Wing normal force slope [ ]
    aircraft_data_int["CNwa"] = CNwa
    CNha = 2 * pi * Ah / (Ah + 2)  # Stabiliser normal force slope [ ]
    aircraft_data_int["CNha"] = CNha
    depsda = 4 / (A + 2)  # Downwash gradient [ ]
    aircraft_data_int["depsda"] = depsda

    # Lift and drag coefficient

    # CL = 2 * W / (rho * V0 ** 2 * S)  # Lift coefficient [ ]
    # aircraft_data_int["CL"] = CL
    # CD = CD0 + (CLa * alpha0) ** 2 / (pi * A * e)  # Drag coefficient [ ]
    # aircraft_data_int["CD"] = CD

    # Stability derivatives

    # CX0 = W * math.sin(th0) / (0.5 * rho * V0 ** 2 * S)
    # aircraft_data_int["CX0"] = CX0
    CXu = -0.09500
    aircraft_data_int["CXu"] = CXu
    CXa = +0.47966  # Positive, see FD lecture notes)
    aircraft_data_int["CXa"] = CXa
    CXadot = +0.08330
    aircraft_data_int["CXadot"] = CXadot
    CXq = -0.28170
    aircraft_data_int["CXq"] = CXq
    CXde = -0.03728
    aircraft_data_int["CXde"] = CXde

    # CZ0 = -W * math.cos(th0) / (0.5 * rho * V0 ** 2 * S)
    # aircraft_data_int["CZ0"] = CZ0
    CZu = -0.37616
    aircraft_data_int["CZu"] = CZu
    CZa = -5.74340
    aircraft_data_int["CZa"] = CZa
    CZadot = -0.00350
    aircraft_data_int["CZadot"] = CZadot
    CZq = -5.66290
    aircraft_data_int["CZq"] = CZq
    CZde = -0.69612
    aircraft_data_int["CZde"] = CZde

    Cm0 = +0.0297
    aircraft_data_int["Cm0"] = Cm0
    Cmu = +0.06990
    aircraft_data_int["Cmu"] = Cmu
    Cmadot = +0.17800
    aircraft_data_int["Cmadot"] = Cmadot
    Cmq = -8.79415
    aircraft_data_int["Cmq"] = Cmq
    CmTc = -0.0064
    aircraft_data_int["CmTc"] = CmTc

    CYb = -0.7500
    aircraft_data_int["CYb"] = CYb
    CYbdot = 0
    aircraft_data_int["CYbdot"] = CYbdot
    CYp = -0.0304
    aircraft_data_int["CYp"] = CYp
    CYr = +0.8495
    aircraft_data_int["CYr"] = CYr
    CYda = -0.0400
    aircraft_data_int["CYda"] = CYda
    CYdr = +0.2300
    aircraft_data_int["CYdr"] = CYdr

    Clb = -0.10260
    aircraft_data_int["Clb"] = Clb
    Clp = -0.71085
    aircraft_data_int["Clp"] = Clp
    Clr = +0.23760
    aircraft_data_int["Clr"] = Clr
    Clda = -0.23088
    aircraft_data_int["Clda"] = Clda
    Cldr = +0.03440
    aircraft_data_int["Cldr"] = Cldr

    Cnb = +0.1348
    aircraft_data_int["Cnb"] = Cnb
    Cnbdot = 0
    aircraft_data_int["Cnbdot"] = Cnbdot
    Cnp = -0.0602
    aircraft_data_int["Cnp"] = Cnp
    Cnr = -0.2061
    aircraft_data_int["Cnr"] = Cnr
    Cnda = -0.0120
    aircraft_data_int["Cnda"] = Cnda
    Cndr = -0.0939
    aircraft_data_int["Cndr"] = Cndr

    return aircraft_data_int, conditions_data_int
