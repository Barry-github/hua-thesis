import numpy as np
from gendis.genetic import GeneticExtractor
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from tools.data_extraction import DataExtractor
from tools.trajectory_generator import TrajectoryGenerator
from tools.utils import standardize_data
#from tools.experiments import Experiments
np.random.seed(1337)  # Random seed for reproducibility

# Create files if not created
#exp = Experiments
#scenarios = experiment_scenarios()

tr_gen = TrajectoryGenerator(samples=100, reset_data=True)
tr_gen.data_generation(n_test=50)

# Read in the datafiles
dex = DataExtractor()
train_df, test_df = dex.train_test_dataframes()
dex.define_csv(dataset=train_df, ts_class=["Bearing", "Speed"], file="train.csv")
dex.define_csv(dataset=test_df, ts_class=["Bearing", "Speed"], file="test.csv")

x_train, y_train, x_test, y_test = dex.load_datasets()

print("standardized train and test data\n")
x_train, x_test = standardize_data(x_train, x_test)

genetic_options = {"population_size": 25,
                   "iterations": 25,
                   "verbose": True,
                   "normed": True,
                   "add_noise_prob": 0.1,
                   "add_shapelet_prob": 0.1,
                   "wait": 10,
                   "plot": None,
                   "remove_shapelet_prob": 0.1,
                   "crossover_prob": 0.8,
                   "n_jobs": 4
                   }

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
