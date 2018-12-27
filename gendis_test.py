import numpy as np
from gendis.genetic import GeneticExtractor
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

np.random.seed(1337)  # Random seed for reproducibility

from data_extraction import DataExtractor
from trajectory_generator import TrajectoryGenerator


#create files if not created
tr_gen = TrajectoryGenerator(samples=100)
tr_gen.data_generation(n_test=10)

# Read in the datafiles
dex = DataExtractor()
train_df,test_df = dex.train_test_dataframes()
dex.define_csv(dataset=train_df, ts_class="Bearing", file="train.csv")
dex.define_csv(dataset=test_df, ts_class="Bearing", file="test.csv")

x_train, y_train, x_test, y_test = dex.load_datasets()
genetic_extractor =  GeneticExtractor(population_size=20, iterations=25, verbose=True,
                                     normed=False, add_noise_prob=0.3, add_shapelet_prob=0.3,
                                     wait=10, plot=None, remove_shapelet_prob=0.3,
                                     crossover_prob=0.66, n_jobs=4)
genetic_extractor.fit(x_train, y_train)
distances_train = genetic_extractor.transform(x_train)
distances_test = genetic_extractor.transform(x_test)

lr = LogisticRegression()
lr.fit(distances_train, y_train)

# Print the accuracy score on the test set
print('Accuracy = {}'.format(accuracy_score(y_test, lr.predict(distances_test))))