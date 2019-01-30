import csv
import os
import shutil
from random import shuffle, choice

import pandas as pd
from pandas.tseries.offsets import Minute

from tools.utils import bearing_noise, speed_noise, calc_distance, destination, movements, print_data_generation


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
        self.movements = movements()
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

    def up(self, timestamp, first_lat, first_lon, speed, bearing, time):
        data = []
        bearing = bearing_noise((bearing - 90) % 360)
        speed = speed_noise(speed)
        last_location = [first_lat, first_lon]
        loops = choice([2,2,2,2,2,2,3,3,3,3,3,3,4,4,4,4,5,5,5,6,6])
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

    def down(self, timestamp, first_lat, first_lon, speed, bearing, time):
        data = []
        bearing = bearing_noise((bearing + 90) % 360)
        speed = speed_noise(speed)
        last_location = [first_lat, first_lon]
        loops = choice([2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6])
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

    def straight_right(self, timestamp, first_lat, first_lon, speed, bearing, time):
        data = []
        bearing = bearing_noise((bearing + 90) % 360)
        speed = speed_noise(speed)
        last_location = [first_lat, first_lon]
        loops = choice([2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6])
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

    def straight_left(self, timestamp, first_lat, first_lon, speed, bearing, time):
        data = []
        bearing = bearing_noise((bearing - 90) % 360)
        speed = speed_noise(speed)
        last_location = [first_lat, first_lon]
        loops = choice([2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6])
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

    def step_up_right(self, timestamp, first_lat, first_lon, speed, bearing, time):
        data = []
        tempdata, timestamp, lat, lon, bearing = self.straight_right(timestamp=timestamp,
                                                                     first_lat=first_lat,
                                                                     first_lon=first_lon,
                                                                     speed=speed,
                                                                     bearing=bearing,
                                                                     time=time)
        data.extend(tempdata)
        tempdata, timestamp, lat, lon, bearing = self.up(timestamp=timestamp,
                                                         first_lat=lat,
                                                         first_lon=lon,
                                                         speed=speed,
                                                         bearing=bearing,
                                                         time=time)
        data.extend(tempdata)
        return data, timestamp, lat, lon, bearing

    def step_up_left(self, timestamp, first_lat, first_lon, speed, bearing, time):
        data = []
        tempdata, timestamp, lat, lon, bearing = self.straight_left(timestamp=timestamp,
                                                                    first_lat=first_lat,
                                                                    first_lon=first_lon,
                                                                    speed=speed,
                                                                    bearing=bearing,
                                                                    time=time)
        data.extend(tempdata)
        tempdata, timestamp, lat, lon, bearing = self.up(timestamp=timestamp,
                                                         first_lat=lat,
                                                         first_lon=lon,
                                                         speed=speed,
                                                         bearing=bearing,
                                                         time=time)
        data.extend(tempdata)
        return data, timestamp, lat, lon, bearing

    def step_down_right(self, timestamp, first_lat, first_lon, speed, bearing, time):
        data = []
        tempdata, timestamp, lat, lon, bearing = self.straight_right(timestamp=timestamp,
                                                                     first_lat=first_lat,
                                                                     first_lon=first_lon,
                                                                     speed=speed,
                                                                     bearing=bearing,
                                                                     time=time)
        data.extend(tempdata)
        tempdata, timestamp, lat, lon, bearing = self.down(timestamp=timestamp,
                                                           first_lat=lat,
                                                           first_lon=lon,
                                                           speed=speed,
                                                           bearing=bearing,
                                                           time=time)
        data.extend(tempdata)
        return data, timestamp, lat, lon, bearing

    def step_down_left(self, timestamp, first_lat, first_lon, speed, bearing, time):
        data = []
        tempdata, timestamp, lat, lon, bearing = self.straight_left(timestamp=timestamp,
                                                                    first_lat=first_lat,
                                                                    first_lon=first_lon,
                                                                    speed=speed,
                                                                    bearing=bearing,
                                                                    time=time)
        data.append(tempdata[0])
        tempdata, timestamp, lat, lon, bearing = self.down(timestamp=timestamp,
                                                           first_lat=lat,
                                                           first_lon=lon,
                                                           speed=speed,
                                                           bearing=bearing,
                                                           time=time)
        data.extend(tempdata)
        return data, timestamp, lat, lon, bearing

    def random_movement(self, timestamp, first_lat, first_lon, speed, bearing, time):

        m = ['straight_right',
             'straight_left',
             'up',
             'down',
             'step_up_right',
             'step_up_left',
             'step_down_left',
             'step_down_right']

        shuffle(m)
        pattern = choice(m)
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
            'straight_right': self.straight_right(timestamp, lat, lon, speed, bearing, time),
            'straight_left': self.straight_left(timestamp, lat, lon, speed, bearing, time),
            'up': self.up(timestamp, lat, lon, speed, bearing, time),
            'down': self.down(timestamp, lat, lon, speed, bearing, time),
            'step_up_right': self.step_up_right(timestamp, lat, lon, speed, bearing, time),
            'step_up_left': self.step_up_left(timestamp, lat, lon, speed, bearing, time),
            'step_down_left': self.step_down_left(timestamp, lat, lon, speed, bearing, time),
            'step_down_right': self.step_down_right(timestamp, lat, lon, speed, bearing, time),
            'random': self.random_movement(timestamp, lat, lon, speed, bearing, time)
        }
        data, timestamp, lat, lon, bearing = switcher.get(pattern, (0, 0, 0, 0))
        return data, timestamp, lat, lon, bearing

    def data_generation(self, filename="testing_", n_test=5):
        print_data_generation(self.__dict__)
        filename = "data/" + filename
        if not os.path.exists("data"):
            print("\nCreate directory \'data\' ")
            os.makedirs("data")
            if len(os.listdir("data")) < 5:
                for d in self.movements:
                    print("now creating data for movement: {0:s}".format(d))
                    for i in range(n_test):
                        self.generator(pattern=d, filename=filename + d + "_"+str(i))
            else:
                print("Done with generator")
                return None
        else:
            print("\nData already exist")
            if os.path.isdir("data"):
                if len(os.listdir("data")) < 5:
                    print("Not enought files. creating more")
                    for d in self.movements:
                        for i in range(n_test):
                            self.generator(pattern=d, filename=filename + d + "_" + str(i))
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

