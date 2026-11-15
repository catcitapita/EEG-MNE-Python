import pandas
from pathlib import Path

# 1. Loop through subfolders of Samples directory
# 2. For each subfolder, check if it contains an EEG folder
# 3. If it does, loop through each CSV in the EEG folder

MAIN_DIRECTORY = "/Users/catcitapita/Documents/Multimodal Video Game Data/archive/Samples/"

EEG_CHANNELS = [
    "EEG.AF3", "EEG.F7", "EEG.F3", "EEG.FC5", "EEG.T7", "EEG.P7", "EEG.O1", 
    "EEG.O2", "EEG.P8", "EEG.T8", "EEG.FC6", "EEG.F4", "EEG.F8", "EEG.AF4"
]

# Searches for EEG subfolder in Participant path.
# If EEG folder exists, loops through each CSV.
# For each CSV, create a data map of specified Columns and their values.
# Return a list of each CSV map.
def get_eeg_data(participant : Path, columns : list[str] = []) -> list[dict[str, list]]: 
    if len(columns) == 0:
        return []
    
    EEG_FOLDER_DIR = "EEG" 
    eeg_directory = participant / EEG_FOLDER_DIR

    if not eeg_directory.is_dir():
        return []
    
    csv_paths = [path for path in eeg_directory.rglob('*.csv') if path.is_file()]
    
    for csv in csv_paths:
        _channels_to_elements = {} # next step is to map out the data
        df = pandas.read_csv(csv)
        for _channel in columns:
            _elements = df[_channel].tolist()
            _channels_to_elements[_channel] = _elements

    return []

def load_data(directory : str):
    participant_to_eeg_data : dict
    dir_path = Path(directory)
    for participant in dir_path.iterdir():
        if participant.is_dir():
            participant_data = get_eeg_data(participant, EEG_CHANNELS)
            return participant_data

load_data(MAIN_DIRECTORY)