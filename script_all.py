import mne
import os
import pandas as pd ## use pandas to read the csv file
import numpy as np ## use numpy to convert the data into a numpy array
import matplotlib as mpl
import matplotlib.pyplot as plt

###############################
## Authored by Catherine Head.
##
## I am using MNE Python to make this into a EEG data interactive plot. 
## 
###############################

## Constants
DEFAULT_DIRECTORY = "/Users/catcitapita/Documents/Multimodal Video Game Data/archive/Samples/118/EEG/"

for file_name in os.listdir(DEFAULT_DIRECTORY):
    if file_name.endswith(".csv"):
        DEFAULT_DIRECTORY = DEFAULT_DIRECTORY + file_name


## Load the data from the csv file at "directory + path" into a pandas DataFrame.
def load_data(directory : str = DEFAULT_DIRECTORY) -> pd.DataFrame | None:
    print("Loading data from: ", directory)
    sample_data_directory = directory

    # Edge case prevention.
    if(sample_data_directory is None):
        print("Error: Could not find the csv file")
        return None

    # Convert file into a pandas DataFrame and cull header.
    raw_data : pd.DataFrame = pd.read_csv(sample_data_directory, skiprows=1)

    # Sanity check.
    if(raw_data is None):
        print("Error: Could not read the csv file")
        return None

    return raw_data

for file_name in os.listdir(DEFAULT_DIRECTORY):
    if file_name.endswith(".csv"):

        file_path = os.path.join(DEFAULT_DIRECTORY, file_name)

        print("Found CSV file:", file_name)

        data = load_data(file_path)