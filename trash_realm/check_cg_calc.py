import matplotlib
import numpy as np
import Solver
import Aircraft
import citation_data
from helper import *

if __name__ == '__main__':
    ac = Aircraft.Aircraft([500,510], citation_data.Data()[0], citation_data.Data()[1], citation_data.Data()[0]['data_dir'])
    print(ac.V0)
    print(ac.rho)

    ac.mass_centroid(10, 100)
    print(ac.center_mass)
    print(ac.x_cg)

    # 7.068208857533041
    # 0.4245848575330413