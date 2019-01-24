import numpy as np
from gendis.genetic import GeneticExtractor
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from tools.data_extraction import DataExtractor
from tools.trajectory_generator import TrajectoryGenerator
from tools.utils import standardize_data, print_genetic_param
from tools.experiments import Experiments

np.random.seed(1337)  # Random seed for reproducibility


def gendis_experiment(testing=False):
    accuracy_results = []
    for sc in settings:
        print("####################### start of an experiment #######################\n")
        if testing:
            tr_gen_options = sc["trajectory_generator_options"]
            dt_gen_options = sc["data_generation_options"]
            df_csvs_options = sc["define_csvs_option"]
            genetic_options = sc["genetic_options"]

            # Create files if not created
            tr_gen = TrajectoryGenerator(**tr_gen_options)
            tr_gen.data_generation(**dt_gen_options)

            # Read in the datafiles
            dex = DataExtractor()
            train_df, test_df = dex.train_test_dataframes()
            print("The train samples length is:{0}".format(len(train_df*10)))
            print("The test samples length is:{0}\n".format(len(test_df*10)))
            train_options, test_options = Experiments.fix_df_csvs_options(df_csvs_options)
            train_options["dataset"] = train_df
            test_options["dataset"] = test_df
            dex.define_csv(**train_options)
            dex.define_csv(**test_options)

            x_train, y_train, x_test, y_test = dex.load_datasets()

            print("standardized train and test data\n")
            x_train, x_test = standardize_data(x_train, x_test)

            genetic_extractor = GeneticExtractor(**genetic_options)
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
            break
        else:
            tr_gen_options = sc["trajectory_generator_options"]
            dt_gen_options = sc["data_generation_options"]
            df_csvs_options = sc["define_csvs_option"]
            genetic_options = sc["genetic_options"]

            # Create files if not created
            tr_gen = TrajectoryGenerator(**tr_gen_options)
            tr_gen.data_generation(**dt_gen_options)

            # Read in the datafiles
            dex = DataExtractor()
            train_df, test_df = dex.train_test_dataframes()
            print("The train samples length is:{0}".format(len(train_df)))
            print("The test samples length is:{0}\n".format(len(test_df)))
            train_options, test_options = Experiments.fix_df_csvs_options(df_csvs_options)
            train_options["dataset"] = train_df
            test_options["dataset"] = test_df
            dex.define_csv(**train_options)
            dex.define_csv(**test_options)

            x_train, y_train, x_test, y_test = dex.load_datasets()

            print("standardized train and test data\n")
            x_train, x_test = standardize_data(x_train, x_test)

            genetic_extractor = GeneticExtractor(**genetic_options)
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
        print("####################### end of an experiment #######################\n")
    return accuracy_results


exp = Experiments()
settings = exp.get_setting()
testing = True
results = gendis_experiment(testing)
print("\nThe max accuracy is: {0} from the settings occurred in experiment no:{1}".format(max(results), results.index(max(results))))

