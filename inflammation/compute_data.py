"""Module containing mechanism for calculating standard deviation between datasets.
"""

import glob
import os
import numpy as np

from inflammation import models, views

class CSVDataSource:
    def __init__(self, data_dir):
        self.data_dir = data_dir # where to look for CSV files

    def load_inflammation_data(self):
        self.data_file_paths = glob.glob(os.path.join(self.data_dir, 'inflammation*.csv'))
        if len(self.data_file_paths) == 0:
            raise ValueError(f"No inflammation data CSV files found in path {self.data_dir}")
        self.data = map(models.load_csv, self.data_file_paths) # load in all CSVs found in the given directory
        return list(self.data)  # returns a list where each entry is a 2D numpy array of the data from one CSV file. 


def analyse_data(data_source):
    """Calculates the standard deviation by day between datasets.

    Works out the mean inflammation value for each day across all datasets,
    then plots the graphs of standard deviation of these means."""
    
    data = data_source.load_inflammation_data() # load in the data from the directory as a list of 2D numpy arrays

    means_by_day = map(models.daily_mean, data)
    means_by_day_matrix = np.stack(list(means_by_day))

    daily_standard_deviation = np.std(means_by_day_matrix, axis=0)

    graph_data = {
        'standard deviation by day': daily_standard_deviation,
    }
    views.visualize(graph_data)