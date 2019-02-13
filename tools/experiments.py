from pandas import Timestamp as Ts


class Experiments:
    def __init__(self):
        self.settings = []
        self.tr_gen_options = []
        self.dt_gen_options = []
        self.df_csv_options = []
        self.train_test_options = []
        self.gen_options = []
        self.init_settings()

    def init_settings(self):
        tr_gen_options, dt_gen_options, df_csv_options, train_test_options, gen_options = self.options_data()
        self.tr_gen_options = tr_gen_options
        self.dt_gen_options = dt_gen_options
        self.df_csv_options = df_csv_options
        self.train_test_options = train_test_options
        self.gen_options = gen_options
        # first setting
        self.add_setting(self.tr_gen_options[0],
                         self.dt_gen_options[0],
                         self.df_csv_options[0],
                         self.train_test_options[0],
                         self.gen_options[0])
        # second setting
        self.add_setting(self.tr_gen_options[0],
                         self.dt_gen_options[1],
                         self.df_csv_options[0],
                         self.train_test_options[0],
                         self.gen_options[0])
        # third setting
        self.add_setting(self.tr_gen_options[0],
                         self.dt_gen_options[0],
                         self.df_csv_options[0],
                         self.train_test_options[0],
                         self.gen_options[1])
        # fourth setting
        self.add_setting(self.tr_gen_options[0],
                         self.dt_gen_options[0],
                         self.df_csv_options[0],
                         self.train_test_options[0],
                         self.gen_options[2])
        # fifth setting
        self.add_setting(self.tr_gen_options[0],
                         self.dt_gen_options[1],
                         self.df_csv_options[0],
                         self.train_test_options[0],
                         self.gen_options[2])
        # sixth setting
        self.add_setting(self.tr_gen_options[2],
                         self.dt_gen_options[2],
                         self.df_csv_options[0],
                         self.train_test_options[2],
                         self.gen_options[2])

    def get_setting(self):
        return self.settings

    def add_setting(self, tr_gen_options, dt_gen_options, df_csv_options, train_test_options, gen_options):
        setting = {"tr_gen_options": tr_gen_options,
                   "dt_gen_options": dt_gen_options,
                   "df_csv_options": df_csv_options,
                   "train_test_options": train_test_options,
                   "gen_options": gen_options}
        self.settings.append(setting)

    def remove_setting(self, setting):
        self.settings.remove(setting)

    def empty_setting(self):
        self.settings.clear()

    @staticmethod
    def options_data():
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
                        "plot": True,
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
                        "plot": True,
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
                        "plot": True,
                        "remove_shapelet_prob": 0.3,
                        "crossover_prob": 0.66,
                        "n_jobs": 4},
                       {"population_size": 20,
                        "iterations": 20,
                        "verbose": True,
                        "normed": True,
                        "add_noise_prob": 0.3,
                        "add_shapelet_prob": 0.3,
                        "wait": 10,
                        "plot": True,
                        "remove_shapelet_prob": 0.3,
                        "crossover_prob": 0.66,
                        "n_jobs": 4}
                       ]

        return tr_gen_options, dt_gen_options, df_csv_options, train_test_options, gen_options

