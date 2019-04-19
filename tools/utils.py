from math import degrees, atan2, asin, sin, cos, radians, sqrt
from random import random, randint, choice
from sklearn import preprocessing
from statistics import mean
import datetime
import os
import pandas as pd
import numpy as np

global_vals = {'movements': {'first_movement': ['step_up_right'], 'second_movement': ['random']}
            }

def get_movements():
    return global_vals['movements']


def set_movements(movements):
    global_vals['movements'] = movements

#trajectory generator's functions
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


def get_distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295  # Pi/180
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a)) * 1000  # 2*R*asin...


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


#printing functions

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
        print("\nData Extractor settings",file=file)
        for key, value in data_generation_options.items():
            print("{0}: {1}".format(key, value),file=file)
        print("\nClasses",file=file)
        for key, value in define_csvs_options.items():
            print("{0}: {1}".format(key, value),file=file)
        print("\nGenetic Options",file=file)
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

#experiments and functions for gendis

def start_experiments(n_exp=1,real_data=False):
    from tools import experiments
    from tools import gendis
    exp = experiments.Experiments()
    settings = exp.get_setting()
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
    count = 0
    while count < n_exp:
        print("************************* Loop no: {0}  *************************".format(count + 1))
        results = gendis.gendis_experiment(settings,real_data)
        n_exp = results.index(max(results))
        file = "outputs/gendis_test_output_"+datetime.datetime.today().strftime("%d_%m")+".txt"
        file_output = open(file, 'a+')
        print("max accuracy: {0} (exp no: {2}) at round :{1}".format(max(results), count, n_exp+1), file=file_output)
        print("\nThe max accuracy: {0} at: {1}".format(max(results), n_exp+1), file=file_output)
        count = count + 1
        print("************************* End of Loop no: {0} *************************\n".format(count))

#simple scale down given the sampling of fake data and the size of real dataset
def scalling_down_simple(data,n_sample):
    data_size = len(data)
    labels = data.columns
    sampling_offset = int(data_size/n_sample)
    count = 0
    new_data = []
    while count< data_size:
        new_data.append(data.iloc[count])
        count = count + sampling_offset

    return pd.DataFrame(new_data,columns=labels)

#if a neighbor sample has already being used then return false or True
def check_sampling(x,sampling,data_index):
    i = 1
    sampling_acc = True
    down_limit = (x[1]-sampling)
    up_limit = (x[1]+sampling)
    while i<=sampling:
        if 0 <=down_limit and up_limit < len(data_index):
            if (data_index[x[1]-i] == True) or (data_index[x[1]+i] == True):
                sampling_acc = False
                break
        i = i + 1
    return sampling_acc

#return the bearing differance and the distance between two samples
def dist_and_bearing_diff(data):
    all_distances = []
    bearing_diff = []
    data_size=len(data)
    i = 0
    while i<data_size:
        if i + 1 >=data_size:
            break
        bearing_1, bearing_2 = data["HEADING"].iloc[i], data["HEADING"].iloc[i+1]
        bearing_diff.append([abs(bearing_2 - bearing_1),i])
        lat_1, lon_1, lat_2, lon_2 = data["LAT"].iloc[i], data["LON"].iloc[i], data["LAT"].iloc[i+1], data["LON"].iloc[i+1]
        all_distances.append(get_distance(lat_1,lon_1,lat_2,lon_2))
        i = i +1
    return bearing_diff, all_distances

#get more samples to fit to generated data sampling size
def fitting_indexes(arr,new_size):
    i = 0
    r_arr = []
    while i <len(arr):
        if i+1 >=len(arr):
            break
        r_arr.append(arr[i+1]-arr[i])
        i = i + 1

    mean_space = mean(r_arr)
    i = 0
    while i<len(arr)<new_size:
        if i+1 >=len(arr):
            break
        diff = arr[i+1]-arr[i]
        if mean_space < diff:
            step = int(diff/2)
            new_index = arr[i] + step
            arr.insert(i+1,new_index)
            i = i + 1
        i = i + 1
    return arr

def scalling_down(data,n_sample,turn_sensitivity=35):
    if len(data) <= n_sample :
        return data
    size_correction = int(len(data) / n_sample) * n_sample
    data=data[:size_correction]
    data_size=len(data)
    data_index = [False for i in range(data_size)]
    sampling = int((int(data_size/n_sample) * 0.25))
    labels = data.columns

    temp_idx = []
    final_data = pd.DataFrame(data,columns=labels)
    final_data.reset_index(drop=True)

    #find the number of bearing differance above the turn sensitivity
    bearing_diff , all_distances = dist_and_bearing_diff(final_data)
    mean_dist = mean(all_distances)
    for idx, x in enumerate(bearing_diff):
        sampling_acc = check_sampling(x,sampling,data_index)
        if (x[0] > turn_sensitivity) and (all_distances[idx] > mean_dist/2) and sampling_acc:
            data_index[x[1]] = True
            temp_idx.append(x[1])
    for x in temp_idx:
        while n_sample > len(temp_idx):
            final_index=fitting_indexes(temp_idx,n_sample)

        for x in temp_idx:
            data_index[x]=True

    return final_data[data_index]

def angle_diff(data):
    if type(data) is np.ndarray:
        new_arr = np.array([])
        for arr in data:
            temp_arr = []
            i = 0
            while i < len(arr):
                if i+1 == len(arr):
                    break
                result = arr[i+1]-arr[i]
                if result != 0 and abs(result) >= 180:
                        result = abs(abs(result) - 360)
                temp_arr.append(result)
                i = i+1
            new_arr = np.append(new_arr, temp_arr).astype(int)
    new_arr = np.reshape(new_arr, (data.shape[0], data.shape[1]-1))
    return new_arr

def standardize_data(x_train, x_test):
    x_scaled_train = preprocessing.scale(x_train)
    x_scaled_test = preprocessing .scale(x_test)

    return x_scaled_train, x_scaled_test
