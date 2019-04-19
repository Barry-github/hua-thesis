from pandas import Timestamp as Ts

class Experiments:
    def __init__(self):
        self.settings = []
        self.tr_gen_options = []
        self.dt_gen_options = []
        self.df_csv_options = []
        self.train_test_options = []
        self.gen_options = []
        self.movements = []
        self.init_settings()

    def init_settings(self):
        tr_gen_options, dt_gen_options, df_csv_options, train_test_options, gen_options, movements = self.options_data()
        self.tr_gen_options = tr_gen_options
        self.dt_gen_options = dt_gen_options
        self.df_csv_options = df_csv_options
        self.train_test_options = train_test_options
        self.gen_options = gen_options
        self.movements = movements
        '''#test_experiment
        self.add_setting(self.tr_gen_options[0],
                         self.dt_gen_options[0],
                         self.df_csv_options[0],
                         self.train_test_options[0],
                         self.gen_options[0],
                         self.movements[0])
                         '''
        # first setting  100 samples 5 iterations
        '''self.add_setting(self.tr_gen_options[0],
                         self.dt_gen_options[0],
                         self.df_csv_options[0],
                         self.train_test_options[0],
                         self.gen_options[0],
                         self.movements[0])
        # second setting 150 samples 5 iterations
        self.add_setting(self.tr_gen_options[0],
                         self.dt_gen_options[1],
                         self.df_csv_options[0],
                         self.train_test_options[0],
                         self.gen_options[0],
                         self.movements[0])
        # third setting 100 samples 10 iterations
        self.add_setting(self.tr_gen_options[0],
                         self.dt_gen_options[0],
                         self.df_csv_options[0],
                         self.train_test_options[0],
                         self.gen_options[1],
                         self.movements[0])
        # fourth setting 100 samples 15 iterations
        self.add_setting(self.tr_gen_options[0],
                         self.dt_gen_options[0],
                         self.df_csv_options[0],
                         self.train_test_options[0],
                         self.gen_options[2],
                         self.movements[0])
        # fifth setting 150 samples 15 iterations
        self.add_setting(self.tr_gen_options[0],
                         self.dt_gen_options[1],
                         self.df_csv_options[0],
                         self.train_test_options[0],
                         self.gen_options[2],
                         self.movements[0])
        # sixth setting  150 samples 20 iterations
        self.add_setting(self.tr_gen_options[0],
                         self.dt_gen_options[1],
                         self.df_csv_options[0],
                         self.train_test_options[0],
                         self.gen_options[3],
                         self.movements[0])
        # seventh setting 150 samples 20 iterations two step classes for movements
        self.add_setting(self.tr_gen_options[0],
                         self.dt_gen_options[1],
                         self.df_csv_options[0],
                         self.train_test_options[0],
                         self.gen_options[3],
                         self.movements[1])
        # eighth setting 150 samples 20 iterations spiral
        self.add_setting(self.tr_gen_options[0],
                         self.dt_gen_options[1],
                         self.df_csv_options[0],
                         self.train_test_options[0],
                         self.gen_options[3],
                         self.movements[2])
        # ninth setting 150 samples 20 iterations two spiral classes for movements
        self.add_setting(self.tr_gen_options[0],
                         self.dt_gen_options[1],
                         self.df_csv_options[0],
                         self.train_test_options[0],
                         self.gen_options[3],
                         self.movements[3])
        # tenth setting 150 samples 20 iterations spiral - steps
        self.add_setting(self.tr_gen_options[0],
                         self.dt_gen_options[1],
                         self.df_csv_options[0],
                         self.train_test_options[0],
                         self.gen_options[3],
                         self.movements[4])
        # eleventh setting 150 samples 20 iterations two spiral - steps
        self.add_setting(self.tr_gen_options[0],
                         self.dt_gen_options[1],
                         self.df_csv_options[0],
                         self.train_test_options[0],
                         self.gen_options[3],
                         self.movements[5])


        # twelfth setting 150 samples 20 iterations expanding square - random
        self.add_setting(self.tr_gen_options[0],
                         self.dt_gen_options[1],
                         self.df_csv_options[0],
                         self.train_test_options[0],
                         self.gen_options[3],
                         self.movements[6])
        # thirteenth  setting 150 samples 20 iterations expanding square -steps
        self.add_setting(self.tr_gen_options[0],
                         self.dt_gen_options[1],
                         self.df_csv_options[0],
                         self.train_test_options[0],
                         self.gen_options[3],
                         self.movements[8])
        '''# fourteenth  setting 150 samples 20 iterations creeping line - random
        self.add_setting(self.tr_gen_options[0],
                         self.dt_gen_options[1],
                         self.df_csv_options[0],
                         self.train_test_options[0],
                         self.gen_options[3],
                         self.movements[10])
        '''# fifteenth setting 150 samples 20 iterations creeping line - steps
        self.add_setting(self.tr_gen_options[0],
                         self.dt_gen_options[1],
                         self.df_csv_options[0],
                         self.train_test_options[0],
                         self.gen_options[3],
                         self.movements[12])
        # sixteenth setting 150 samples 20 iterations sector - random
        self.add_setting(self.tr_gen_options[0],
                         self.dt_gen_options[1],
                         self.df_csv_options[0],
                         self.train_test_options[0],
                         self.gen_options[3],
                         self.movements[14])
        # seventeenth setting 150 samples 20 iterations sector - random
        self.add_setting(self.tr_gen_options[0],
                         self.dt_gen_options[1],
                         self.df_csv_options[0],
                         self.train_test_options[0],
                         self.gen_options[3],
                         self.movements[16])
                             '''

    def get_setting(self):
        return self.settings

    def add_setting(self, tr_gen_options, dt_gen_options, df_csv_options, train_test_options, gen_options, movements):
        setting = {"tr_gen_options": tr_gen_options,
                   "dt_gen_options": dt_gen_options,
                   "df_csv_options": df_csv_options,
                   "train_test_options": train_test_options,
                   "gen_options": gen_options,
                   "movements": movements}
        self.settings.append(setting)

    def remove_setting(self, setting):
        self.settings.remove(setting)

    def empty_setting(self):
        self.settings.clear()

    @staticmethod
    def options_data():
        #test options_data
        '''tr_gen_options = [{"samples": 25, "freq": 3, "reset_data": True}]
        dt_gen_options = [{"n_test": 10}]
        df_csv_options = [{"ts_class": "Bearing"}]
        train_test_options = [{"split": 25}]
        gen_options = [{"population_size": 25,
                        "iterations": 5,
                        "verbose": True,
                        "normed": True,
                        "add_noise_prob": 0.0,
                        "add_shapelet_prob": 0.3,
                        "wait": 10,
                        "plot": None,
                        "remove_shapelet_prob": 0.3,
                        "crossover_prob": 0.66,
                        "n_jobs": 4}
                       ]
        movements = [{'first_movement': ['creeping_line_left'],  # 10 creeping_line-random
                    'second_movement': ['random']}
                     ]
        '''
        tr_gen_options = [{"samples": 25, "freq": 3, "reset_data": True}]

        dt_gen_options = [{"n_test": 100},
                          {"n_test": 150}]

        df_csv_options = [{"ts_class": "Bearing"}]

        train_test_options = [{"split": 25}]

        gen_options = [{"population_size": 20,
                        "iterations": 5,
                        "verbose": True,
                        "normed": True,
                        "add_noise_prob": 0.3,
                        "add_shapelet_prob": 0.3,
                        "wait": 10,
                        "plot": None,
                        "remove_shapelet_prob": 0.3,
                        "crossover_prob": 0.66,
                        "n_jobs": 4},
                       {"population_size": 20,
                        "iterations": 10,
                        "verbose": True,
                        "normed": True,
                        "add_noise_prob": 0.3,
                        "add_shapelet_prob": 0.3,
                        "wait": 10,
                        "plot": None,
                        "remove_shapelet_prob": 0.3,
                        "crossover_prob": 0.66,
                        "n_jobs": 4},
                       {"population_size": 20,
                        "iterations": 15,
                        "verbose": True,
                        "normed": True,
                        "add_noise_prob": 0.3,
                        "add_shapelet_prob": 0.3,
                        "wait": 10,
                        "plot": None,
                        "remove_shapelet_prob": 0.3,
                        "crossover_prob": 0.66,
                        "n_jobs": 4},
                       {"population_size": 20,
                        "iterations": 20,
                        "verbose": True,
                        "normed": True,
                        "add_noise_prob": 0.0,
                        "add_shapelet_prob": 0.3,
                        "wait": 10,
                        "plot": None,
                        "remove_shapelet_prob": 0.3,
                        "crossover_prob": 0.66,
                        "n_jobs": 4}
                       ]

        movements = [{'first_movement': ['step_up_right'],  # 0 classic step-random classes
                      'second_movement': ['random']},
                     {'first_movement': ['step_up_right', 'step_down_right'],  # 1 two step-random classes
                      'second_movement': ['random', 'random']},
                     {'first_movement': ['spiral_movement_left'],  # 2 spiral_momvement-random
                      'second_movement': ['random']},
                     {'first_movement': ['spiral_movement_left', 'spiral_movement_right'],  # 3 two spiral-random classes
                      'second_movement': ['random', 'random']},
                     {'first_movement': ['spiral_movement_left'],  # 4 spiral-step classes
                      'second_movement': ['step_up_right']},
                     {'first_movement': ['spiral_movement_left', 'spiral_movement_right'],  # 5 two spiral-step classes
                      'second_movement': ['step_up_right', 'step_down_right']},
                     {'first_movement': ['expanding_square_right'],  # 6 expanding_square-random
                      'second_movement': ['random']},
                     {'first_movement': ['expanding_square_right', 'expanding_square_left'],  # 7 two expanding_square-random
                      'second_movement': ['random', 'random']},
                     {'first_movement': ['expanding_square_right'],  # 8 expanding_square_-step classes
                      'second_movement': ['step_up_right']},
                     {'first_movement': ['expanding_square_right', 'expanding_square_left'],  # 9 two expanding_square_-step classes
                      'second_movement': ['step_up_right', 'step_down_right']},
                     {'first_movement': ['creeping_line_left'],  # 10 creeping_line-random
                      'second_movement': ['random']},
                     {'first_movement': ['creeping_line_right', 'creeping_line_left'], # 11 two creeping_line_left-random
                      'second_movement': ['random', 'random']},
                     {'first_movement': ['creeping_line_left'],  # 12 creeping_line_left-step classes
                      'second_movement': ['step_up_right']},
                     {'first_movement': ['creeping_line_right', 'creeping_line_left'], # 13 two sector_pattern-step classes
                      'second_movement': ['step_up_right', 'step_down_right']},
                     {'first_movement': ['sector_pattern_left'],  # 14 creeping_line-random
                      'second_movement': ['random']},
                     {'first_movement': ['sector_pattern_right', 'creeping_line_left'], # 15 two sector_pattern-random
                      'second_movement': ['random', 'random']},
                     {'first_movement': ['sector_pattern_left'],  # 16 sector_pattern-step classes
                      'second_movement': ['step_up_right']},
                     {'first_movement': ['sector_pattern_right', 'creeping_line_left'], # 17 two sector_pattern-step classes
                      'second_movement': ['step_up_right', 'step_down_right']},
                     ]
        return tr_gen_options, dt_gen_options, df_csv_options, train_test_options, gen_options, movements
