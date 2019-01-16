import numpy as np
from gendis.genetic import GeneticExtractor
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from tools.data_extraction import DataExtractor
from tools.trajectory_generator import TrajectoryGenerator
from tools.utils import standardize_data
from tools.experiments import Experiments

np.random.seed(1337)  # Random seed for reproducibility


exp = Experiments()
scenarios = exp.scenarios

for sc in scenarios:
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

    train_options, test_options = Experiments.fix_df_csvs_options(df_csvs_options)
    train_options["dataset"] = train_df
    test_options["dataset"] = test_df
    dex.define_csv(**train_options)
    dex.define_csv(**test_options)

    x_train, y_train, x_test, y_test = dex.load_datasets()

    print("standardized train and test data\n")
    x_train, x_test = standardize_data(x_train, x_test)

    genetic_extractor = GeneticExtractor(**genetic_options)
    print("Starting fit in genetic extractor with:\n"
          "population size:{0:d}\n"
          "iterations: {1:d}\n"
          "normed: {2}\n".format(genetic_extractor.population_size,
                                 genetic_extractor.iterations,
                                 genetic_extractor.normed))

    genetic_extractor.fit(x_train, y_train)
    distances_train = genetic_extractor.transform(x_train)
    distances_test = genetic_extractor.transform(x_test)

    lr = LogisticRegression()
    lr.fit(distances_train, y_train)

    # Print the accuracy score on the test set
    print('Accuracy = {}'.format(accuracy_score(y_test, lr.predict(distances_test))))
