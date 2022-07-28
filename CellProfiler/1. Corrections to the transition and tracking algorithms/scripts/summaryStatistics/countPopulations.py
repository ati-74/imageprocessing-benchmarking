"""
This script reads in .pickle files containing cellStates dictionaries and outputs
a spreadsheet containing the total population of each cellType at each time step.
The script can be used for an arbitrary number of populations

Ensure that the data files have cellType starting from 0.

Instructions:
    1. Optional: input the user_max_cell_type if you don't want extra empty headings in the csv output
        e.g., for monoculture, the max_cell_type is 0
    2. Run this script and select the directory containing the .pickle files 
"""

import sys
import os
import math
import numpy as np
import pickle
from tkinter import Tk
from tkinter.filedialog import askdirectory
from helperFunctions import create_pickle_list
import csv
import re
import pandas as pd


use_max_cell_type_custom = False #True if you want data to look nice 
max_cell_type_custom = 2 #change the RHS to the largest cellType in your data set
max_cell_type_default = 3 


def count_cell_types(file_dir_path, pickle_file_name, max_cell_type = max_cell_type_default):   
    """
    Counts the total number of each cellType at a given time step.
    @param  file_dir_path       String containing the full path to the directory containing the .pickle files 
    @param  pickle_file_name    String containing the name of the a specific .pickle file
    @param  max_cell_type       int specifying the largest cellType index in the experiment
    
    @return populations         nparray with the total population for each cellType
    """
    
    # Read in file
    pickle_full_path = os.path.join(file_dir_path, pickle_file_name)
    data = pickle.load(open(pickle_full_path, 'rb'))
    
    # Initializations
    cs = data['cellStates']
    populations = np.zeros((max_cell_type + 1,), dtype = int)
    
    # Iterate through cellStates DataFrame and add to the populations array based on cellType
    for i, row in cs.iterrows():
        cell_type = row['cellType']
        for cell_type_idx in range(0, max_cell_type + 1):
            if cell_type_idx == cell_type:
                populations[cell_type] += 1

    return populations
  

def run_population_counts_and_write_to_csv(pickle_list, output_file_path, max_cell_type = max_cell_type_default): 
    """
    Run count_cell_types at each time step, then output to csv file.
    
    @param pickle_list      list of .pickle files to process
    @param output_file_path str for path of the output csv file
    @param max_cell_type    int specifying the largest cellType index in the experiment
    """
    # Write column headers
    header = ['Time step']
    for i in range(0, max_cell_type + 1):
        cell_type_string = f"cellType {i}"
        header.append(cell_type_string) 

    # Write to csv file
    with open (output_file_path, 'w', newline = '') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
    
        #Write row of data for each time step
        for file in pickle_list:
            print('Writing : ', file)
            match = re.search('step-(\d+)', file, re.IGNORECASE)
            step = int(match.group(1))
            populations = count_cell_types(file_dir_path, file, max_cell_type)
            writer.writerow(np.concatenate((step,populations),axis = None))


# Reading files and paths
file_dir_path = askdirectory(title = 'Select directory containing .pickle files')    
output_file_path = os.path.join(file_dir_path, 'cell_type_populations.csv')

# Process data
pickle_list = create_pickle_list(file_dir_path)
if use_max_cell_type_custom == False:
    run_population_counts_and_write_to_csv(pickle_list, output_file_path)
else:
    run_population_counts_and_write_to_csv(pickle_list, output_file_path, user_max_type)
