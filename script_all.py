import mne
import os
import pandas as pd ## use pandas to read the csv file
import numpy as np ## use numpy to convert the data into a numpy array
import matplotlib as mpl
import matplotlib.pyplot as plt
from pathlib import Path

###############################
## Authored by Catherine Head.
##
## I am using MNE Python to make this into a EEG data interactive plot. 
## 
###############################

## Constants
DEFAULT_DIRECTORY = "/Users/catcitapita/Documents/Multimodal Video Game Data/archive/Samples/"
OUTPUT_DIR = ".vscode/output/"
PARTICIPANT_COUNT = -1

eeg_channels = [
    "EEG.AF3", "EEG.F7", "EEG.F3", "EEG.FC5", "EEG.T7", "EEG.P7", "EEG.O1", 
    "EEG.O2", "EEG.P8", "EEG.T8", "EEG.FC6", "EEG.F4", "EEG.F8", "EEG.AF4"
] 

# Load each participant CSV into DataFrame and combine into single DataFrame.
def load_data(directory : Path) -> pd.DataFrame:
    # print("Loading data from: ", directory)

    # Edge case prevention.
    if(directory is None):
        print("Error: Could not find the csv file")
        return pd.DataFrame()

    eeg_directory = directory / "EEG"
    
    if not eeg_directory.is_dir():
        return pd.DataFrame()

    csv_paths = [path for path in eeg_directory.rglob('*.csv') if path.is_file()]

    csv_df_list = []
    
    for csv in csv_paths:
        df = pd.read_csv(csv)
        csv_df_list.append(process_dataframe(df))
    return pd.concat(csv_df_list, axis=0)

# Filter DataFrame to specified global channels.
def process_dataframe(df : pd.DataFrame) -> pd.DataFrame:
    return df[eeg_channels] * 1e-6

# Convert DataFrame to RawArray.
def convert_to_mne_raw_array(eeg_data : pd.DataFrame) -> mne.io.RawArray:
    if(eeg_data is None):
        return
    print("Converting data into MNE RawArray format")

    # Define input data.
    channel_names = list(eeg_data.columns)
    print(channel_names)
    data_values = eeg_data.to_numpy().T
    #* 1e-6

    sfreq = 128  # Sampling frequency in Hz
    info = mne.create_info(ch_names=channel_names,sfreq=sfreq,ch_types='eeg')
    print(f"Info: {info}")

    return mne.io.RawArray(data_values, info)

def plot_psd_and_raw(mne_data : mne.io.RawArray): 
    mne_data.compute_psd(fmin=0, fmax=64).plot(picks="data", amplitude=False)
    mne_data.plot(duration=5, n_channels=14, block=True)

def preprocess_data(mne_data : mne.io.RawArray):
    # mne_data.filter(l_freq=1.0, h_freq=50.0)
    mne_data.compute_psd(fmin=0, fmax=64)
    mne_data.plot(scalings={"eeg": 200e-6},block=True)

def main():
    dir_path = Path(DEFAULT_DIRECTORY)
    df_list : list[pd.DataFrame] = []

    print("Collecting")
    # Get a complete DataFrame for each individual and add to list.
    pt_idx = 0
    for participant in dir_path.iterdir():
        if not participant.is_dir():
            print(f"Missing Directory: {participant}")
            continue
        
        _p_df = load_data(participant)

        if(_p_df.empty):
            print(f"Empty DataFrame for Participant: {participant}")
            continue

        df_list.append(_p_df)

        if(PARTICIPANT_COUNT > 0):
            pt_idx += 1
            if(pt_idx >= PARTICIPANT_COUNT):
                break
        
    print(f"{len(df_list)} frames found")

    # Create total concated DataFrame of all participants files.
    print("Processing")
    combined_df = pd.concat(df_list, axis=0)
    
    # Convert averaged DataFrame to MNE RawArray and plot.
    print("Plotting")
    convert_processed = convert_to_mne_raw_array(combined_df)
    plot_psd_and_raw(convert_processed)
    
main()



