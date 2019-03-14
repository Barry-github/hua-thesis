import csv
import os
import shutil
from random import shuffle, choice

import pandas as pd
from pandas.tseries.offsets import Minute

from tools.utils import bearing_noise, random_init_bearing,random_turn, speed_noise, calc_distance, destination, get_movements, print_data_generation


class TrajectoryGenerator:
    def __init__(self,
                 first_lat=37.295493,
                 first_lon=23.824322,
                 init_bearing=90,
                 init_speed=5,
                 samples=10,
                 timestamp=pd.Timestamp(2015, 2, 1, 12),
                 freq=3,
                 reset_data=False):
        self.first_lat = first_lat
        self.first_lon = first_lon
        self.init_bearing = init_bearing
        self.init_speed = init_speed
        self.samples = samples
        self.timestamp = timestamp
        self.freq = freq
        movement_types = {'first_movement': get_movements()['first_movement'],
                          'second_movement': get_movements()['second_movement']}
        self.movements = movement_types
        self.reset_data = reset_data
        if self.reset_data:
            TrajectoryGenerator.reset_data()

    def generator(self, pattern, filename):
        csv_file = filename+"_"+str(self.timestamp.date())+".csv"
        data = [{'Timestamp': self.timestamp,
                 'Lat': self.first_lat, 'Lon': self.first_lon,
                 'Bearing': self.init_bearing,
                 'Speed': self.init_speed,
                 'Distance': 0}]

        with open(csv_file, 'w', newline='') as csv_File:
            fields = ['Timestamp', 'Lat', 'Lon', 'Bearing', 'Speed', 'Distance']
            writer = csv.DictWriter(csv_File, fieldnames=fields)
            writer.writeheader()
            last_location = [self.first_lat, self.first_lon]
            last_bearing = self.init_bearing
            last_timestamp = self.timestamp
            d = 0
            while d < self.samples:
                tempdata, timestamp, lat2, lon2, bearing = self.pattern_switcher(pattern=pattern,
                                                                                 timestamp=last_timestamp,
                                                                                 lat=last_location[0],
                                                                                 lon=last_location[1],
                                                                                 speed=self.init_speed,
                                                                                 bearing=last_bearing,
                                                                                 time=self.freq)
                if lat2 == 0 and lon2 == 0 and timestamp == 0 and tempdata == 0:
                    print("Invalid Pattern")
                    break
                last_location[0] = lat2
                last_location[1] = lon2
                last_bearing = bearing
                last_timestamp = timestamp
                data.extend(tempdata)
                d = len(data)-1

            while len(data) > self.samples:
                data.pop()
            writer.writerows(data)
            csv_File.close()

    def turn_right(self, timestamp, first_lat, first_lon, speed, bearing, time, turn=90, loops=[2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6]):
        data = []
        bearing = bearing_noise((bearing + turn) % 360)
        speed = speed_noise(speed)
        last_location = [first_lat, first_lon]
        loops = choice(loops)
        count = 1
        while count <= loops:
            #time = freq_sampling_noise(time)
            timestamp = timestamp + Minute(time)
            distance = calc_distance(speed, time=time)
            lat, lon = destination(lat=last_location[0], lon=last_location[1], distance=distance, bearing=bearing)
            data.append({'Timestamp': timestamp,
                         'Lat': lat, 'Lon': lon,
                         'Bearing': bearing,
                         'Speed': speed,
                         'Distance': distance})
            last_location[0] = lat
            last_location[1] = lon
            count = count + 1
        return data, timestamp, last_location[0], last_location[1], bearing

    def turn_left(self, timestamp, first_lat, first_lon, speed, bearing, time, turn=90, loops=[2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6]):
        data = []
        bearing = bearing_noise((bearing - turn) % 360)
        speed = speed_noise(speed)
        last_location = [first_lat, first_lon]
        loops = choice(loops)
        count = 1
        while count <= loops:
            #time = freq_sampling_noise(time)
            timestamp = timestamp + Minute(time)
            distance = calc_distance(speed, time=time)
            lat, lon = destination(lat=last_location[0], lon=last_location[1], distance=distance, bearing=bearing)
            data.append({'Timestamp': timestamp,
                         'Lat': lat, 'Lon': lon,
                         'Bearing': bearing,
                         'Speed': speed,
                         'Distance': distance})
            last_location[0] = lat
            last_location[1] = lon
            count = count + 1
        return data, timestamp, last_location[0], last_location[1], bearing

    def go_straight(self, timestamp, first_lat, first_lon, speed, bearing, time, turn=0, loops=[2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6]):
        data = []
        bearing = bearing_noise((bearing - turn) % 360)
        speed = speed_noise(speed)
        last_location = [first_lat, first_lon]
        loops = choice(loops)
        count = 1
        while count <= loops:
            # time = freq_sampling_noise(time)
            timestamp = timestamp + Minute(time)
            distance = calc_distance(speed, time=time)
            lat, lon = destination(lat=last_location[0], lon=last_location[1], distance=distance, bearing=bearing)
            data.append({'Timestamp': timestamp,
                         'Lat': lat, 'Lon': lon,
                         'Bearing': bearing,
                         'Speed': speed,
                         'Distance': distance})
            last_location[0] = lat
            last_location[1] = lon
            count = count + 1
        return data, timestamp, last_location[0], last_location[1], bearing

    def go_backwards(self, timestamp, first_lat, first_lon, speed, bearing, time, turn=180, loops=[2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6]):
        data = []
        bearing = bearing_noise((bearing - turn) % 360)
        speed = speed_noise(speed)
        last_location = [first_lat, first_lon]
        loops = choice(loops)
        count = 1
        while count <= loops:
            # time = freq_sampling_noise(time)
            timestamp = timestamp + Minute(time)
            distance = calc_distance(speed, time=time)
            lat, lon = destination(lat=last_location[0], lon=last_location[1], distance=distance, bearing=bearing)
            data.append({'Timestamp': timestamp,
                         'Lat': lat, 'Lon': lon,
                         'Bearing': bearing,
                         'Speed': speed,
                         'Distance': distance})
            last_location[0] = lat
            last_location[1] = lon
            count = count + 1
        return data, timestamp, last_location[0], last_location[1], bearing

    def step_up_right(self, timestamp, first_lat, first_lon, speed, bearing, time):
        data = []
        tempdata, timestamp, lat, lon, bearing = self.turn_right(timestamp=timestamp,
                                                                 first_lat=first_lat,
                                                                 first_lon=first_lon,
                                                                 speed=speed,
                                                                 bearing=bearing,
                                                                 time=time)
        data.extend(tempdata)
        tempdata, timestamp, lat, lon, bearing = self.turn_left(timestamp=timestamp,
                                                                first_lat=lat,
                                                                first_lon=lon,
                                                                speed=speed,
                                                                bearing=bearing,
                                                                time=time)
        data.extend(tempdata)
        return data, timestamp, lat, lon, bearing

    def step_up_left(self, timestamp, first_lat, first_lon, speed, bearing, time):
        data = []
        tempdata, timestamp, lat, lon, bearing = self.turn_left(timestamp=timestamp,
                                                                first_lat=first_lat,
                                                                first_lon=first_lon,
                                                                speed=speed,
                                                                bearing=bearing,
                                                                time=time)
        data.extend(tempdata)
        tempdata, timestamp, lat, lon, bearing = self.turn_right(timestamp=timestamp,
                                                            first_lat=lat,
                                                            first_lon=lon,
                                                            speed=speed,
                                                            bearing=bearing,
                                                            time=time)
        data.extend(tempdata)
        return data, timestamp, lat, lon, bearing

    def step_down_right(self, timestamp, first_lat, first_lon, speed, bearing, time):
        data = []
        tempdata, timestamp, lat, lon, bearing = self.turn_right(timestamp=timestamp,
                                                                 first_lat=first_lat,
                                                                 first_lon=first_lon,
                                                                 speed=speed,
                                                                 bearing=bearing,
                                                                 time=time)
        data.extend(tempdata)
        tempdata, timestamp, lat, lon, bearing = self.turn_left(timestamp=timestamp,
                                                           first_lat=lat,
                                                           first_lon=lon,
                                                           speed=speed,
                                                           bearing=bearing,
                                                           time=time)
        data.extend(tempdata)
        return data, timestamp, lat, lon, bearing

    def step_down_left(self, timestamp, first_lat, first_lon, speed, bearing, time):
        data = []
        tempdata, timestamp, lat, lon, bearing = self.turn_left(timestamp=timestamp,
                                                                first_lat=first_lat,
                                                                first_lon=first_lon,
                                                                speed=speed,
                                                                bearing=bearing,
                                                                time=time)
        data.append(tempdata[0])
        tempdata, timestamp, lat, lon, bearing = self.turn_right(timestamp=timestamp,
                                                                 first_lat=lat,
                                                                 first_lon=lon,
                                                                 speed=speed,
                                                                 bearing=bearing,
                                                                 time=time)
        data.extend(tempdata)
        return data, timestamp, lat, lon, bearing

    def spiral_movement_left(self, timestamp, first_lat, first_lon, speed, bearing, time):
        data = []
        turn = random_turn(min=45, max=80)
        loops = [2,2,2,2,2,2,2,3,3,3]
        tempdata, timestamp, lat, lon, bearing = self.turn_left(timestamp=timestamp,
                                                                first_lat=first_lat,
                                                                first_lon=first_lon,
                                                                speed=speed,
                                                                bearing=bearing,
                                                                time=time,
                                                                turn=turn,
                                                                loops=loops)
        data.extend(tempdata)
        return data, timestamp, lat, lon, bearing

    def spiral_movement_right(self, timestamp, first_lat, first_lon, speed, bearing, time):
        data = []
        turn = random_turn(min=45, max=80)
        loops = [2,2,2,2,2,2,2,3,3,3]
        tempdata, timestamp, lat, lon, bearing = self.turn_right(timestamp=timestamp,
                                                                 first_lat=first_lat,
                                                                 first_lon=first_lon,
                                                                 speed=speed,
                                                                 bearing=bearing,
                                                                 time=time,
                                                                 turn=turn,
                                                                 loops=loops)
        data.extend(tempdata)
        return data, timestamp, lat, lon, bearing

    def random_movement(self, timestamp, first_lat, first_lon, speed, bearing, time):
        m = ['turn_right',
             'turn_left',
             'go_straight']
        shuffle(m)
        pattern = choice(m)
        if pattern == "turn_right" or pattern == "turn_left":
            turn = random_turn(min=80, max=90)
            data, timestamp, lat, lon, bearing = getattr(TrajectoryGenerator, pattern)(self,
                                                                                       timestamp,
                                                                                       first_lat,
                                                                                       first_lon,
                                                                                       speed,
                                                                                       bearing,
                                                                                       time,
                                                                                       turn)
        else:
            data, timestamp, lat, lon, bearing = getattr(TrajectoryGenerator, pattern)(self,
                                                                                       timestamp,
                                                                                       first_lat,
                                                                                       first_lon,
                                                                                       speed,
                                                                                       bearing,
                                                                                       time)

        return data, timestamp, lat, lon, bearing

    def pattern_switcher(self, pattern, timestamp, lat, lon, speed, bearing, time):
        switcher = {
            'turn_right': self.turn_right(timestamp, lat, lon, speed, bearing, time),
            'turn_left': self.turn_left(timestamp, lat, lon, speed, bearing, time),
            'step_up_right': self.step_up_right(timestamp, lat, lon, speed, bearing, time),
            'step_up_left': self.step_up_left(timestamp, lat, lon, speed, bearing, time),
            'step_down_left': self.step_down_left(timestamp, lat, lon, speed, bearing, time),
            'step_down_right': self.step_down_right(timestamp, lat, lon, speed, bearing, time),
            'spiral_movement_right': self.spiral_movement_right(timestamp, lat, lon, speed, bearing, time),
            'spiral_movement_left': self.spiral_movement_left(timestamp, lat, lon, speed, bearing, time),
            'random': self.random_movement(timestamp, lat, lon, speed, bearing, time)
        }
        data, timestamp, lat, lon, bearing = switcher.get(pattern, (0, 0, 0, 0))
        return data, timestamp, lat, lon, bearing

    def data_generation(self, filename="", n_test=10):
        #print_data_generation(self.__dict__)
        filename = "data/" + filename
        if not os.path.exists("data"):
            print("\nCreate directory \'data\' ")
            os.makedirs("data")
            if len(os.listdir("data")) < n_test:
                first_movement = self.movements['first_movement']
                second_movement = self.movements['second_movement']
                for idx, d in enumerate(first_movement):
                    print("now creating data for movement: {0:s}".format(d))
                    for i in range(n_test):
                        self.init_bearing = random_init_bearing(self.init_bearing)
                        self.generator(pattern=d, filename=filename+"first_movement_"+str(idx)+"_" +d + "_"+str(i))
                for idx, d in enumerate(second_movement):
                    print("now creating data for movement: {0:s}".format(d))
                    for i in range(n_test):
                        self.init_bearing = random_init_bearing(self.init_bearing)
                        self.generator(pattern=d, filename=filename+"second_movement_"+str(idx)+"_" + d + "_"+str(i))
            else:
                print("Done with generator")
                return None
        else:
            print("\nData already exists")
            if os.path.isdir("data"):
                if len(os.listdir("data")) < n_test:
                    print("Not enough files. creating more")
                    first_movement = self.movements['first_movement']
                    second_movement = self.movements['second_movement']
                    for idx, d in enumerate(first_movement):
                        print("now creating data for movement: {0:s}".format(d))
                        for i in range(n_test):
                            self.init_bearing = random_init_bearing(self.init_bearing)
                            self.generator(pattern=d,
                                           filename=filename + "first_movement_" + str(idx) + "_" + d + "_" + str(i))
                    for idx, d in enumerate(second_movement):
                        print("now creating data for movement: {0:s}".format(d))
                        for i in range(n_test):
                            self.init_bearing = random_init_bearing(self.init_bearing)
                            self.generator(pattern=d,
                                           filename=filename + "second_movement_" + str(idx) + "_" + d + "_" + str(i))
                else:
                    print("Done with generator")
                    return None
            else:
                print("Done with generator")
                return None

        print("Done with generator")

    @staticmethod
    def reset_data():
        shutil.rmtree("data") if os.path.isdir("data") else None
        for x in os.listdir(os.getcwd()):
            os.remove(os.path.basename(x)) if x.endswith(".csv") else None

