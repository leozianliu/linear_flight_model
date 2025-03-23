from scipy.constants import foot, pound, hour
import warnings
import numpy as np
import citation_data

# Constants
R = 287.05  # Specific gas constant for dry air
g = 9.80665  # Acceleration due to gravity
rho_air = 1.225  # Density of air at sea level in kg/m^3

def ft_to_meters(feet):
    meters = feet * foot  # 1 foot = 0.3048 meters
    return meters

def inch_to_meters(inch):
    meters = inch * 0.0254
    return meters

def search_time_index(time_series, find_time):
    # Search for the index of the time in the time_series
    time_index = np.argmin(np.abs(time_series - find_time))
    if find_time < time_series[0]:
        warnings.warn("The time is less than the minimum time in the time series.")
    elif find_time > time_series[-1]:
        warnings.warn("The time is greater than the maximum time in the time series.")
    return time_index

def lb_to_kg(lbs):
    return lbs * pound

def lbs_hr_to_kg_s(lbs_hr):
    return lbs_hr * pound / hour

def kt_to_meter_per_sec(kts):
    return kts * 1852 / 3600

def celsius_to_kelvin(celsius):
    return celsius + 273.15

def ISA_alt_to_static_pressure(pressure_alt_meters):
    # Convert pressure altitude to static pressure
    lambda_rate = -0.0065  # Lapse rate
    T0 = 288.15  # Sea level temperature in Kelvin
    p0 = 101325  # Sea level pressure in Pascals

    static_pressure = p0 * (1 + (lambda_rate * pressure_alt_meters) / T0) ** (-g / (lambda_rate * R))
    return static_pressure

def pressure_alt_to_ISA_temperature(pressure_alt_meters):
    # Convert pressure altitude to ISA temperature
    lambda_rate = -0.0065  # Lapse rate
    T0 = 288.15  # Sea level temperature in Kelvin
    ISA_temperature = T0 + lambda_rate * pressure_alt_meters
    return ISA_temperature

def static_pres_to_density(static_pressure, static_temperature):
    density = static_pressure / (R * static_temperature)
    return density

def pressure_alt_to_density(pressure_alt_meters, static_temperature):
    static_pressure = ISA_alt_to_static_pressure(pressure_alt_meters)
    density = static_pres_to_density(static_pressure, static_temperature)
    return density

