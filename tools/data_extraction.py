import pandas as pd
import numpy as np
import os
from loguru import logger


class DataExtractor:
    def __init__(self, train_samples=0.8):
        self.dataframes_first_movement, self.dataframes_second_movement = self.read_datasets()
        self.train_samples = train_samples
        self.file_string = "_"+str(pd.Timestamp(2015, 2, 1, 12).date())+".csv"
        self.listdir_sz = 0
        self.listdir = []
        self.movements = []
        col_names = ['Timestamp', 'Lat', 'Lon', 'Bearing', 'Speed', 'Distance']
        self.train_df = [pd.DataFrame(columns=col_names), pd.DataFrame(columns=col_names)]
        self.test_df = [pd.DataFrame(columns=col_names), pd.DataFrame(columns=col_names)]
        self.train_range = int(len(self.dataframes_first_movement[0]) * self.train_samples)

    def read_datasets(self):
        from tools.utils import get_movements
        logger.info("Reading the data files")
        self.movements = get_movements()
        dataframes_first_movement = []
        dataframes_second_movement = []
        if os.path.exists("generator_data"):
            if os.path.isdir("generator_data"):
                self.listdir = os.listdir("generator_data")
                self.set_sz_listdir(len(self.listdir))
                for idx, d in enumerate(self.movements['first_movement']):
                    first = []
                    for file in self.listdir:
                        if file.endswith(".csv"):
                            check_file = "first_movement_" + str(idx)
                            if file.__contains__(d) and file.__contains__(check_file):
                                file = "generator_data/" + file
                                first.append(pd.read_csv(file))

                    dataframes_first_movement.append(first)
                for idx, d in enumerate(self.movements['second_movement']):
                    second = []
                    for file in self.listdir:
                        if file.endswith(".csv"):
                            check_file = "second_movement_"+str(idx)
                            if file.__contains__(d) and file.__contains__(check_file):
                                file = "generator_data/" + file
                                second.append(pd.read_csv(file))

                    dataframes_second_movement.append(second)

        logger.success("Done reading files")
        return dataframes_first_movement, dataframes_second_movement

    def train_test_dataframes(self, split=10):
        for idx, mov in enumerate(self.dataframes_first_movement):
            for d in range(0, self.train_range):
                self.train_df[0] = self.train_df[0].append(self.dataframes_first_movement[idx][d], ignore_index=True)
            for d in range(self.train_range, len(self.dataframes_first_movement[idx])):
                self.test_df[0] = self.test_df[0].append(self.dataframes_first_movement[idx][d], ignore_index=True)

        for idx, mov in enumerate(self.dataframes_second_movement):
            for d in range(0, self.train_range):
                self.train_df[1] = self.train_df[1].append(self.dataframes_second_movement[idx][d], ignore_index=True)
            for d in range(self.train_range, len(self.dataframes_second_movement[idx])):
                self.test_df[1] = self.test_df[1].append(self.dataframes_second_movement[idx][d], ignore_index=True)
        n_split = int(len(self.train_df[0]) / split)
        self.train_df[0] = np.split(self.train_df[0], n_split)
        self.train_df[1] = np.split(self.train_df[1], n_split)
        n_split = int(len(self.test_df[0]) / split)
        self.test_df[0] = np.split(self.test_df[0], n_split)
        self.test_df[1] = np.split(self.test_df[1], n_split)
        return self.train_df, self.test_df

    def define_csv(self, ts_class):
        if DataExtractor.is_right_format(ts_class):
            logger.info("Creating {0:s} and {1:s} ".format("x_train.csv--y_train.csv", "x_test.csv--y_test.csv"))
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
            logger.success("Done with train.csv")

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
            logger.info("Done with test.csv")
        else:
            logger.error("wrong format for requested attributes. needed a option from [Bearing,Speed,Distance]")

    @staticmethod
    def load_datasets():

        logger.info("Loading the csv files to the appropriate train and test arrays(nparrays)")
        x_train = np.loadtxt("x_train.csv", delimiter=",", dtype=int)
        y_train = np.loadtxt("y_train.csv", delimiter=",", dtype=int)
        x_test = np.loadtxt("x_test.csv", delimiter=",", dtype=int)
        y_test = np.loadtxt("y_test.csv", delimiter=",", dtype=int)
        logger.success("Done")
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
