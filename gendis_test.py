import numpy as np
import datetime
import sys
from gendis.genetic import GeneticExtractor
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from tools.data_extraction import DataExtractor
from tools.trajectory_generator import TrajectoryGenerator
from tools.utils import standardize_data, print_genetic_param, print_settings, set_movements, angle_diff
from tools.experiments import Experiments

now = datetime.datetime.now()

np.random.seed(1337)  # Random seed for reproducibility


def gendis_experiment():
    accuracy_results = []
    for idx, sc in enumerate(settings):
        print("####################### Experiment no: {0}  #######################".format(idx+1))
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
        print("####################### End of Experiment no: {0} #######################\n".format(idx+1))
    return accuracy_results


# output_file = "gendis_test_ouput_" + now.strftime('%m_%d_%H:%M') + ".txt"
# sys.stdout = open(output_file, 'w')
exp = Experiments()
settings = exp.get_setting()
results = gendis_experiment()
n_exp = results.index(max(results))
print("\nThe max accuracy is: {0} from the settings occurred in experiment no:{1}".format(max(results), n_exp))
best_result = settings[n_exp]
print_settings(best_result["tr_gen_options"],
               best_result["dt_gen_options"],
               best_result["define_csvs_option"],
               best_result["gen_options"])
print("\nAll experiments results")
for idx, x in results:
    print("Experiment#: {0}".format(str(idx)))
    temp_settings = settings[idx]
    print_settings(temp_settings["tr_gen_options"],
                   temp_settings["dt_gen_options"],
                   temp_settings["df_csv_options"],
                   temp_settings["gen_options"])
    print("Accuracy: {0}".format(results[idx]))
