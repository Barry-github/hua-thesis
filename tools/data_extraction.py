import pandas as pd
import numpy as np
import os
from tools.utils import get_movements


class DataExtractor:
    def __init__(self, train_samples=0.8):
        self.dataframes_steps, self.dataframes_random = self.read_datasets()
        self.train_samples = train_samples
        self.file_string = "_"+str(pd.Timestamp(2015, 2, 1, 12).date())+".csv"
        self.listdir_sz = 0
        self.listdir = []
        self.movements = []
        col_names = ['Timestamp', 'Lat', 'Lon', 'Bearing', 'Speed', 'Distance']
        self.train_df = [pd.DataFrame(columns=col_names), pd.DataFrame(columns=col_names)]
        self.test_df = [pd.DataFrame(columns=col_names), pd.DataFrame(columns=col_names)]
        self.train_range = int(len(self.dataframes_steps[0]) * self.train_samples)

    def read_datasets(self):
        print("\nReading the data files", end='')
        self.movements = get_movements()
        dataframes_steps = []
        dataframes_random = []
        if os.path.exists("data"):
            if os.path.isdir("data"):
                self.listdir = os.listdir("data")
                self.set_sz_listdir(len(self.listdir))
                for x in self.movements:
                    steps = []
                    randoms = []
                    for file in self.listdir:
                        if file.endswith(".csv"):
                            if file.__contains__(x):
                                if x.__contains__("step"):
                                    file = "data/" + file
                                    steps.append(pd.read_csv(file))
                                else:
                                    file = "data/" + file
                                    randoms.append(pd.read_csv(file))
                    if x.__contains__("step"):
                        dataframes_steps.append(steps)
                    else:
                        dataframes_random.append(randoms)
        print("....Done reading files")
        return dataframes_steps, dataframes_random

    def train_test_dataframes(self, split=10):
        for idx, mov in enumerate(self.dataframes_steps):
            for d in range(0, self.train_range):
                self.train_df[0] = self.train_df[0].append(self.dataframes_steps[idx][d], ignore_index=True)
            for d in range(self.train_range, len(self.dataframes_steps[idx])):
                self.test_df[0] = self.test_df[0].append(self.dataframes_steps[idx][d], ignore_index=True)

        for idx, mov in enumerate(self.dataframes_random):
            for d in range(0, self.train_range):
                self.train_df[1] = self.train_df[1].append(self.dataframes_random[idx][d], ignore_index=True)
            for d in range(self.train_range, len(self.dataframes_random[idx])):
                self.test_df[1] = self.test_df[1].append(self.dataframes_random[idx][d], ignore_index=True)

        n_split = int(len(self.train_df[0]) / split)
        self.train_df[0] = np.split(self.train_df[0], n_split)
        self.train_df[1] = np.split(self.train_df[1], n_split)
        n_split = int(len(self.test_df[0]) / split)
        self.test_df[0] = np.split(self.test_df[0], n_split)
        self.test_df[1] = np.split(self.test_df[1], n_split)
        return self.train_df, self.test_df

    def define_csv(self, ts_class):
        if DataExtractor.is_right_format(ts_class):
            print("Creating {0:s} and {1:s} ".format("x_train.csv--y_train.csv", "x_test.csv--y_test.csv"), end='')
            class_list = ts_class
            x_train_file = "x_train.csv"
            y_train_file = "y_train.csv"
            x_test_file = "x_test.csv"
            y_test_file = "y_test.csv"
            # for train.csv
            x_ds = []
            y_ds = []
            for idx, sl in enumerate(self.train_df[0]):
                x_ds.append(self.train_df[0][idx][class_list].values)
                x_ds.append(self.train_df[1][idx][class_list].values)
                y_ds.append(0)
                y_ds.append(1)

            x_ds = np.array(x_ds)
            y_ds = np.array(y_ds)
            x_ds = np.reshape(x_ds, (x_ds.shape[0], x_ds.shape[1])).astype(int)
            y_ds = np.reshape(y_ds, (1, y_ds.shape[0])).astype(int)
            with open(x_train_file, 'wb') as x_csv:

                np.savetxt(x_csv, x_ds, delimiter=',', newline='\n', fmt='%i')

            np.savetxt(y_train_file, y_ds, delimiter=",", fmt='%i')
            x_csv.close()
            print("...Done with train.csv", end=' ')

            # for test.csv
            x_ds = []
            y_ds = []
            for idx, sl in enumerate(self.test_df[0]):
                x_ds.append(self.test_df[0][idx][class_list].values)
                x_ds.append(self.test_df[1][idx][class_list].values)
                y_ds.append(0)
                y_ds.append(1)

            x_ds = np.array(x_ds)
            y_ds = np.array(y_ds)
            x_ds = np.reshape(x_ds, (x_ds.shape[0], x_ds.shape[1])).astype(int)
            y_ds = np.reshape(y_ds, (1, y_ds.shape[0])).astype(int)
            with open(x_test_file, 'wb') as x_csv:

                np.savetxt(x_csv, x_ds, delimiter=',', newline='\n', fmt='%i')

            np.savetxt(y_test_file, y_ds, delimiter=",", fmt='%i')
            x_csv.close()
            print("...Done with test.csv")
        else:
            print("...wrong format for requested attributes. needed a option from [Bearing,Speed,Distance]")

    @staticmethod
    def load_datasets():

        print("Loading the csv files to the appropriate train and test arrays(nparrays)", end='')
        x_train = np.loadtxt("x_train.csv", delimiter=",", dtype=int)
        y_train = np.loadtxt("y_train.csv", delimiter=",", dtype=int)
        x_test = np.loadtxt("x_test.csv", delimiter=",", dtype=int)
        y_test = np.loadtxt("y_test.csv", delimiter=",", dtype=int)
        print("...Done")
        return x_train, y_train, x_test, y_test

    def set_sz_listdir(self, listdir_sz):
        self.listdir_sz = listdir_sz

    def set_listdir(self, listdir):
        self.listdir = listdir

    @staticmethod
    def is_right_format(ts_class):
        if isinstance(ts_class, str):
            if (ts_class is "Bearing") or (ts_class is "Distance") or (ts_class is "Speed"):
                return True
        else:
            return False


