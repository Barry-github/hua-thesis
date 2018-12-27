from math import degrees, atan2, asin, sin, cos, radians
from random import random, randint, choice
import pandas as pd
import numpy as np



def bearing_noise(bearing):
    return random_noise(bearing, limit_up=10)


def speed_noise(speed):
    noises = [2,2,2,2,2,3,3,3,3,3,5,5,5,5,5,5,7,7,7,7,10,10,10,10,10,30,50,60]
    limit = choice(noises)
    return random_noise(speed, limit_up=limit)


def freq_sampling_noise(freq):

    return random_noise(x=freq, limit_down=3, limit_up=15)


def calc_distance(speed, time):
    time = time/60
    return round(speed * time, 3)


def random_noise(x, limit_up, limit_down=0):
        choice = random()
        if choice <= 0.5:
            return x + randint(limit_down, limit_up)
        else:
            return abs(x - randint(limit_down, limit_up))


def destination(lat, lon, distance, bearing):
    R = 6378.1  # Radius of the Earth
    bearing = radians(bearing)
    lat1 = radians(lat)  # Current lat point converted to radians
    lon1 = radians(lon)  # Current long point converted to radians

    lat2 = asin(sin(lat1) * cos(distance / R) + cos(lat1) * sin(distance / R) * cos(bearing))
    lon2 = lon1 + atan2(sin(bearing) * sin(distance / R) * cos(lat1), cos(distance / R) - sin(lat1) * sin(lat2))

    lat2 = degrees(lat2)
    lon2 = degrees(lon2)
    return lat2, lon2


def timestamp_converter(data):
    new_array = np.empty(shape=data.shape)
    for idx, d in enumerate(data):
        if isinstance(d, str):
            new_array[idx] = int(pd.Timestamp(d).timestamp())
        else:
            return data
    return new_array


def movements():
    movements = ['step_up_right',
                 'step_up_left',
                 'step_down_left',
                 'step_down_right',
                 'random']
    return movements
