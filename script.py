import mne
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
DEFAULT_DIRECTORY = "/Users/catcitapita/Documents/Multimodal Video Game Data/archive/Samples/118/EEG"

## Load the data from the csv file at "directory + path" into a pandas DataFrame.
def load_data(directory : str = DEFAULT_DIRECTORY, path : str = "/118_4_4_1_3_EEG.csv") -> pd.DataFrame:
    print("Loading data from: ", directory + path)
    # Get file.
    sample_data_directory = directory
    sample_data_raw_file = sample_data_directory + path

    # Edge case prevention.
    if(sample_data_raw_file is None):
        print("Error: Could not find the csv file")
        return None

    # Convert file into a pandas DataFrame and cull header.
    raw_data : pd.DataFrame = pd.read_csv(sample_data_raw_file, skiprows=1)

    # Sanity check.
    if(raw_data is None):
        print("Error: Could not read the csv file")
        return None

    return raw_data


def convert_to_numpy_array(raw_data : pd.DataFrame) -> np.ndarray:
    print("Converting data into numpy array format")
    return raw_data.to_numpy().T


def convert_to_mne_raw_array(raw_data : pd.DataFrame) -> mne.io.RawArray:
    print("Converting data into MNE RawArray format")

    # Define input data.
    channel_names = raw_data.columns[4:18].tolist()
    data_values = raw_data.values[:, 4:18].T * 1e-6

    sfreq = 128  # Sampling frequency in Hz
    info = mne.create_info(ch_names=channel_names,sfreq=sfreq,ch_types='eeg')

    return mne.io.RawArray(data_values, info)


loaded_data = load_data()
numpy_data = convert_to_numpy_array(loaded_data)
mne_data = convert_to_mne_raw_array(loaded_data)


def preprocess_data(mne_data):

    # Filter the data to remove noise and artifacts
    mne_data.filter(l_freq=1.0, h_freq=50.0)

    # Remove EEG prefix from channel names and set montage
    mne_data.rename_channels(lambda x: x.replace("EEG.", ""))
    montage = mne.channels.make_standard_montage("standard_1020") 
    mne_data.set_montage(montage)

    # Compute and plot the power spectral density (PSD) for each channel
    spect = mne_data.compute_psd(picks="eeg", fmin=0, fmax=64)
    spect_data = mne_data.info['ch_names']

    custom_colors = [
    "red", "blue", "green", "orange",
    "purple", "pink", "brown", "cyan",
    "magenta", "yellow", "black", "gray",
    "olive", "navy"
    ]
  
    spect.plot(picks=spect_data, color=custom_colors)
    
    mne_data.plot(scalings={"eeg": 200e-6},block=True, color="purple")


data_plot_filtered = preprocess_data(mne_data)

