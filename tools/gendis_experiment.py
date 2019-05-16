import time
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from gendis.genetic import GeneticExtractor
from tools.data_extraction import DataExtractor
from tools.trajectory_generator import TrajectoryGenerator
from tools.utils import print_genetic_param, standardize_data, scale_down, set_movements, angle_diff
from loguru import logger

np.random.seed(1337)  # Random seed for reproducibility


def gendis_experiment(settings, real_data=False, angle_diff_mode=False):
    accuracy_results = []
    times = []
    exp_results = {"accuracy_results": accuracy_results, "times": times}
    for idx, sc in enumerate(settings):
        logger.info("Start of setting {0}".format(sc["message"]))
        first = time.time()
        tr_gen_options = sc["tr_gen_options"]
        dt_gen_options = sc["dt_gen_options"]
        df_csv_options = sc["df_csv_options"]
        train_test_options = sc["train_test_options"]
        gen_options = sc["gen_options"]
        set_movements(sc['movements'])

        # Create files if not created
        tr_gen = TrajectoryGenerator(**tr_gen_options)
        tr_gen.data_generation(**dt_gen_options)

        # Read in the datafiles
        dex = DataExtractor()
        train_df, test_df = dex.train_test_dataframes(**train_test_options)
        logger.info("The train samples length is:{0}".format(len(train_df[0][0]) * len(train_df[0]) * len(train_df)))
        logger.info("The test samples length is:{0}\n".format(len(test_df[0][0]) * len(test_df[0]) * len(test_df)))
        dex.define_csv(**df_csv_options)

        x_train, y_train, x_test, y_test = dex.load_datasets()

        if real_data:
            logger.info("Loading real data")
            labels = ["TIMESTAMP", "LAT", "LON", "HEADING"]
            real_data = pd.read_csv("/home/kotsos/Desktop/hua/infos/data/route.csv")
            real_data = real_data[labels]
            real_data.sort_values('TIMESTAMP', inplace=True)
            real_data = real_data.reset_index(drop=True)
            data = scale_down(real_data, train_test_options["split"])

            y_test = np.array([0, 1])
            fdata=np.array(data["HEADING"].values).astype(int)
            x_test=np.array([fdata, x_test[1]])

        if angle_diff_mode:
            logger.info("Angle_Diff mode on: Computing angle(bearing) difference")
            x_train = angle_diff(x_train)
            x_test = angle_diff(x_test)

        logger.info("standardized train and test data")
        x_train, x_test = standardize_data(x_train, x_test)

        genetic_extractor = GeneticExtractor(**gen_options)
        logger.info(print_genetic_param(genetic_extractor))
        genetic_extractor.fit(x_train, y_train)
        distances_train = genetic_extractor.transform(x_train)
        distances_test = genetic_extractor.transform(x_test)

        lr = LogisticRegression()
        lr.fit(distances_train, y_train)

        # Print the accuracy score on the test set
        accuracy_result = accuracy_score(y_test, lr.predict(distances_test))
        logger.info('Accuracy = {}'.format(accuracy_result))
        time_passed = (time.time() - first)/60
        times.append(time_passed)
        accuracy_results.append(accuracy_result)
        logger.info("time passed on this experiment: {0} minutes".format(time_passed))
        logger.info("End of setting no:{0}".format(idx+1))

    return exp_results
