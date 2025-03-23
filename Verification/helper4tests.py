import unittest
import numpy as np


def get_test_data():
    '''
    n=1000
    cl = np.linspace(-1.2,1.5,n)
    aoa = np.linspace(-10,10,n)
    h = np.linspace(2000,3000,n)
    w=np.linspace(1000,950,n)
    rho = np.linspace(1.225,1.1,n)
    S=25
    example_data = [
        aoa, # aoa
        w, # weight
        rho, # rho
        np.sqrt(2*w/(rho*cl*S)), # TAS
        h, # h
        np.ones(n)*10, # T
        np.sqrt(np.ones(n)*1.4*287*(273.15+10)), # M
        [],
        [],
    ]
    '''
    n=1000
    cl = np.linspace(0.2,1.5,n)
    aoa = np.linspace(0,10,n)
    h = np.zeros(n)
    w=np.linspace(1000,950,n)*9.81
    rho = np.ones(n)*1.225
    S=25
    example_data = [
        aoa, # aoa
        w, # weight
        rho, # rho
        np.sqrt(2*w/(rho*cl*S)), # TAS
        h, # h
        np.ones(n)*10, # T
        np.sqrt(np.ones(n)*1.4*287*(273.15+10)), # M
        0.453592*(np.ones(n)*1000)/3600,
        0.453592*(np.ones(n)*1000)/3600
    ]
    #make Mach correcct
    example_data[6]=example_data[3]/example_data[6]
    return example_data