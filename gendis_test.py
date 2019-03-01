import numpy as np
import datetime
import time
from gendis.genetic import GeneticExtractor
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from tools.data_extraction import DataExtractor
from tools.trajectory_generator import TrajectoryGenerator
from tools.utils import standardize_data, print_genetic_param, print_settings, set_movements, angle_diff
from tools.experiments import Experiments

np.random.seed(1337)  # Random seed for reproducibility


def gendis_experiment():
    accuracy_results = []
    for idx, sc in enumerate(settings):
        print("####################### Experiment no: {0}  #######################".format(idx+1))
        first = time.time()
        tr_gen_options = sc["tr_gen_options"]
        dt_gen_options = sc["dt_gen_options"]
        df_csv_options = sc["df_csv_options"]
        train_test_options = sc["train_test_options"]
        gen_options = sc["gen_options"]

        movements = ['step_up_right',
                     'random'
                     ]
        set_movements(movements)

        # Create files if not created
        tr_gen = TrajectoryGenerator(**tr_gen_options)
        tr_gen.data_generation(**dt_gen_options)

        # Read in the datafiles
        dex = DataExtractor()
        train_df, test_df = dex.train_test_dataframes(**train_test_options)
        print("The train samples length is:{0}".format(len(train_df[0][0]) * len(train_df[0]) * len(train_df)))
        print("The test samples length is:{0}\n".format(len(test_df[0][0]) * len(test_df[0]) * len(test_df)))
        dex.define_csv(**df_csv_options)

        x_train, y_train, x_test, y_test = dex.load_datasets()

        print("standardized train and test data\n")
        x_train, x_test = standardize_data(x_train, x_test)

        #x_train = angle_diff(x_train)
        #x_test = angle_diff(x_test)

        genetic_extractor = GeneticExtractor(**gen_options)
        print_genetic_param(genetic_extractor)

        genetic_extractor.fit(x_train, y_train)
        distances_train = genetic_extractor.transform(x_train)
        distances_test = genetic_extractor.transform(x_test)

        lr = LogisticRegression()
        lr.fit(distances_train, y_train)

        # Print the accuracy score on the test set
        accuracy_result = accuracy_score(y_test, lr.predict(distances_test))
        print('Accuracy = {}'.format(accuracy_result))
        accuracy_results.append(accuracy_result)
        delta = time.time() - first
        print("time passed on this experiment: {0}".format(delta))
        print("####################### End of Experiment no: {0} #######################\n".format(idx+1))
    return accuracy_results


exp = Experiments()
settings = exp.get_setting()

count = 0
while count < 50:
    results = gendis_experiment()
    #n_exp = results.index(max(results))

    file = "gendis_test_output_"+datetime.datetime.today().strftime("%d_%m")+".txt"
    file_output = open(file, 'a+')
    print("max accuracy: {0} at round :{1}".format(max(results),count),file=file_output)
    '''print("\nThe max accuracy: {0} at: {1}".format(max(results), n_exp+1), file=file_output)

    print("\nAll experiments results", file=file_output)
    for idx, x in results:
        print("Experiment#: {0}".format(str(idx+1)))
        temp_settings = settings[idx]
        print("Accuracy: {0}".format(results[idx]), file=file_output)'''
    file_output.close()
    count = count + 1
