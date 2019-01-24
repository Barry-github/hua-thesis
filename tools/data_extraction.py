import pandas as pd
import numpy as np
import os
from tools.utils import timestamp_converter, movements


class DataExtractor:
    def __init__(self, train_samples=0.2):
        self.dataframes = self.read_datasets()
        self.train_samples = train_samples
        self.file_string = "_"+str(pd.Timestamp(2015, 2, 1, 12).date())+".csv"
        self.listdir_sz = 0
        self.listdir = []
        self.movements = []

    def read_datasets(self):
        print("\nReading the data files", end='')
        self.movements = movements()
        dataframes = []
        if os.path.exists("data"):
            if os.path.isdir("data"):
                self.listdir = os.listdir("data")
                self.set_sz_listdir(len(self.listdir))
                for idx, x in enumerate(self.movements):
                    new_data = []
                    for file in self.listdir:
                        if file.endswith(".csv"):
                            if file.__contains__(x):
                                file = "data/" + file
                                new_data.append(pd.read_csv(file))
                    dataframes.append(new_data)
        print("....Done reading files")
        return dataframes

    def train_test_dataframes(self, dataset=0):
        col_names = ['Timestamp', 'Lat', 'Lon', 'Bearing', 'Speed', 'Distance']
        train_df = pd.DataFrame(columns=col_names)
        train_range = int(len(self.dataframes[dataset]) * self.train_samples)
        print()
        for d in range(0, train_range):
            train_df = train_df.append(self.dataframes[dataset][d], ignore_index=True)
        n_split = int(len(train_df)/10)
        train_df = np.split(train_df, n_split)
        test_df = pd.DataFrame(columns=col_names)
        for d in range(train_range, len(self.dataframes[dataset])):
            test_df = test_df.append(self.dataframes[dataset][d], ignore_index=True)
        n_split = int(len(test_df) / 10)
        test_df = np.split(test_df, n_split)
        return train_df, test_df

    @staticmethod
    def define_csv(dataset, ts_class, file):
        if DataExtractor.is_right_format(ts_class):
            print("Creating {0:s} ".format(file), end='')
            class_list = ts_class
            x_file = "x_" + file
            y_file = "y_" + file
            x_ds = []
            y_ds = []
            for sl in dataset:
                if DataExtractor.classes_exist(ts_class,sl):
                    x_ds.append(sl[class_list[0]].values)
                    x_ds.append(sl[class_list[1]].values)
                    y_ds.append(1)
                    y_ds.append(2)
                else:
                    print("...error. not such classes in a dataframe of given dataset")
                    break

            x_ds = np.array(x_ds)
            y_ds = np.array(y_ds)
            x_ds = np.reshape(x_ds, (x_ds.shape[0], x_ds.shape[1]))
            y_ds = np.reshape(y_ds, (1, y_ds.shape[0]))
            with open(x_file, 'wb') as x_csv:
                for idx, d in enumerate(x_ds):
                    d = timestamp_converter(d)
                    x_ds[idx] = d
                np.savetxt(x_csv, x_ds, delimiter=',', newline='\n', fmt='%f')

            np.savetxt(y_file, y_ds, delimiter=",", fmt='%f')
            x_csv.close()
            print("...Done")
        else:
            print("...wrong format for requested classes. needed a list with 2 string cells")

    @staticmethod
    def load_datasets():

        print("Loading the csv files to the appropriate train and test arrays(nparrays)", end='')
        x_train = pd.read_csv("x_train.csv", header=None, skip_blank_lines=True).get_values()
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1]))
        y_train = pd.read_csv("y_train.csv", header=None, skip_blank_lines=True).get_values()
        y_train = np.reshape(y_train, (y_train.shape[1]))
        x_test = pd.read_csv("x_test.csv", header=None, skip_blank_lines=True).get_values()
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1]))
        y_test = pd.read_csv("y_test.csv", header=None, skip_blank_lines=True).get_values()
        y_test = np.reshape(y_test, (y_test.shape[1]))
        print("...Done")
        return x_train, y_train, x_test, y_test

    def set_sz_listdir(self, listdir_sz):
        self.listdir_sz = listdir_sz

    def set_listdir(self, listdir):
        self.listdir = listdir

    @staticmethod
    def is_right_format(ts_class):
        if len(ts_class) == 2:
            if isinstance(ts_class[0], str) and isinstance(ts_class[1], str):
                return True
            else:
                return False

    @staticmethod
    def classes_exist(ts_class, df):
        list_col = list(df)
        if ts_class[0] in list_col and ts_class[1] in list_col:
            return True
        else:
            return False


