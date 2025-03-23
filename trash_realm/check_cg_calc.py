import matplotlib
import numpy as np
import Solver
import Aircraft
import citation_data
from helper import *

data_dir = "data_ref_2025/FTISxprt-20250304_084412.mat"

if __name__ == '__main__':
    ac = Aircraft.Aircraft([500,510], citation_data.Data()[0], citation_data.Data()[1])
    print(ac.V0)
    print(ac.rho)

    ac.mass_centroid(10, 100)
    print(ac.center_mass)
    print(ac.x_cg)

    # 7.068208857533041
    # 0.4245848575330413