from math import degrees, atan2, asin, sin, cos, radians
from random import random, randint, choice
from sklearn import preprocessing
import pandas as pd
import numpy as np


global_vals = {'movements': {'first_movement': ['step_up_right'], 'second_movement': ['random']}
               }


def random_turn(min=0, max=90):
    return randint(min, max)


def random_init_bearing(bearing):
    return random_noise(bearing, limit_up=180) % 360


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


def get_movements():
    return global_vals['movements']


def set_movements(movements):
    global_vals['movements'] = movements


def standardize_data(x_train, x_test):
    x_scaled_train = preprocessing.scale(x_train)
    x_scaled_test = preprocessing .scale(x_test)

    return x_scaled_train, x_scaled_test


def angle_diff(data):
    if type(data) is np.ndarray:
        new_arr = np.array([])
        for arr in data:
            temp_arr = []
            i = 0
            while i < len(arr):
                if i+1 == len(arr):
                    break;
                result = arr[i+1]-arr[i]
                if result !=0 and abs(result) >=180:
                        result = abs(abs(result) - 360)
                temp_arr.append(result)
                i = i+1
            new_arr=np.append(new_arr, temp_arr).astype(int)
    new_arr = np.reshape(new_arr, (data.shape[0], data.shape[1]-1))
    return new_arr


def statistics_results(results):
    print(results)


def print_genetic_param(gen_ext):
    print("Starting fit in genetic extractor with:\n"
          "population size:{0:d}\n"
          "iterations: {1:d}\n"
          "normed: {2}\n"
          "noise_prob: {3}\n"
          "add_shapelet_prob: {4}\n"
          "remove_shapelet_prob: {5}\n"
          "crossover_prob: {6}\n".format(gen_ext.population_size,
                                         gen_ext.iterations,
                                         gen_ext.normed,
                                         gen_ext.add_noise_prob,
                                         gen_ext.add_shapelet_prob,
                                         gen_ext.remove_shapelet_prob,
                                         gen_ext.crossover_prob))


def print_data_generation(dict):
    print("\nStarting the generator with attributes: \n"
          "Original latitude: {first_lat}\n"
          "Original longitude: {first_lon}\n"
          "Initial bearing: {init_bearing}\n"
          "Initial speed: {init_speed}\n"
          "Number of samples: {samples}\n"
          "Starting time of measurements: {timestamp}\n"
          "With initial frequency of collected data: {freq} min\n"
          "and hard reset of data: {reset_data}".format(**dict))


def print_settings(trajectory_generator_options,data_generation_options,define_csvs_options,genetic_options,file=None):
    if file is not None:
        for key, value in trajectory_generator_options.items():
            print("{0}: {1}".format(key, value),file=file)
        print("\nData Extractor settings")
        for key, value in data_generation_options.items():
            print("{0}: {1}".format(key, value),file=file)
        print("\nClasses")
        for key, value in define_csvs_options.items():
            print("{0}: {1}".format(key, value),file=file)
        print("\nGenetic Options")
        for key, value in genetic_options.items():
            print("{0}: {1}".format(key, value),file=file)
    else:
        for key, value in trajectory_generator_options.items():
            print("{0}: {1}".format(key, value))
        print("\nData Extractor settings")
        for key, value in data_generation_options.items():
            print("{0}: {1}".format(key, value))
        print("\nClasses")
        for key, value in define_csvs_options.items():
            print("{0}: {1}".format(key, value))
        print("\nGenetic Options")
        for key, value in genetic_options.items():
            print("{0}: {1}".format(key, value))


