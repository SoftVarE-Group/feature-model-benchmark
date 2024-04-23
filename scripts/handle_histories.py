import pandas as pd
from pathlib import Path
import shutil
import os
import hashlib
from utils import get_files_from_directory


def hash_hex(filepath):    
    with open(filepath, "rb") as f:
        h = hashlib.md5()
        while chunk := f.read(8192):
            h.update(chunk)

    return h.hexdigest()

def get_time_string(path, prefix):
    file_name = Path(path).stem
    time_string = file_name.replace(prefix, '')
    return time_string

def get_time_stamp(path, prefix):
    file_name = Path(path).stem
    time_string = file_name.replace(prefix, '').replace('_', '').replace('-', '')
    return int(time_string)

def copy_file(path : str):
    new_path = path.replace('feature_models/original/systems_software/', '')
    Path(new_path).parent.resolve().mkdir(parents=True, exist_ok=True)
    shutil.copyfile(path, new_path)


def build_frame(path, prefix):
    original = pd.read_csv(path, delimiter=',')
    original['timestring'] = original['File'].apply(lambda file : get_time_string(file, prefix))
    original['timestamp'] = original['File'].apply(lambda file : get_time_stamp(file, prefix))
    df = original.groupby(['Hash']).min(numeric_only=True)
    result = original[original['timestamp'].isin(df['timestamp'])]
    return result

def build_full_Frame(files, prefix):
    df = pd.DataFrame()
    df['File'] = files
    df['timestring'] = df['File'].apply(lambda file : get_time_string(file, prefix))
    df['timestamp'] = df['File'].apply(lambda file : get_time_stamp(file, prefix))
    df['hash'] = df['File'].apply(hash_hex)
    df = df.sort_values('timestamp', ignore_index=True)
    return df

def create_cleaned_histories(path):
    to_keep_frame = build_frame(path)
    to_keep_frame.to_csv('keptFiles.csv', index=False)
    to_keep_frame['File'].apply(copy_file)

# def create_version_json(path):
#     df = build_frame(path)
#     result = ''
#     for value in sorted(df['timestring']):
#         result += f'"{value}",\n'
#     print(result)

def create_clean_copy(path, extensions = ['.xml', '.dimacs', '.uvl']):
    files = get_files_from_directory(path, extensions)
    files = [file for file in files if 'Pett2021' in file]
    df = build_full_Frame(files)
    copied = set()
    os.makedirs('cleaned', exist_ok=True)
    for index, row in df.iterrows():
        file_name = os.path.split(row['File'])[1]
        if row['hash'] not in copied:
            shutil.copy(row['File'], os.path.join('cleaned', file_name))
        else:
            print(f'Removed {file_name}')
        copied.add(row['hash'])

def create_versions_json(path, prefix, extensions = ['.xml', '.dimacs', '.uvl']):
    files = get_files_from_directory(path, extensions)
    files = [file for file in files if prefix in file]
    df = build_full_Frame(files, prefix)
    result = ''
    for value in (df['timestring']):
        result += f'"{value}",\n'
    print(f'{path} history')
    print(result)

create_versions_json('feature_models/original/systems_software/BusyBox', 'Pett2021-')
create_versions_json('feature_models/original/systems_software/Fiasco', 'Pett2023-')
create_versions_json('feature_models/original/systems_software/soletta', 'Pett2023-')
create_versions_json('feature_models/original/systems_software/uClibc', 'Pett2023-')



# Information on feature models that have been removed
# Soletta
# Removed Pett2023-2015-06-29_15-01-39.xml
# Removed Pett2023-2015-06-30_19-23-17.xml
# Removed Pett2023-2015-07-02_18-48-59.xml
# Removed Pett2023-2015-07-06_10-50-32.xml
# Removed Pett2023-2015-07-07_19-50-10.xml
# Removed Pett2023-2015-07-13_17-55-29.xml
# Removed Pett2023-2015-07-14_13-31-24.xml
# Removed Pett2023-2015-07-14_15-43-36.xml
# Removed Pett2023-2015-07-21_15-38-17.xml
# Removed Pett2023-2015-07-21_15-38-21.xml
# Removed Pett2023-2015-07-22_14-21-15.xml
# Removed Pett2023-2015-07-28_11-20-02.xml
# Removed Pett2023-2015-07-28_11-23-51.xml
# Removed Pett2023-2015-07-29_17-38-14.xml
# Removed Pett2023-2015-07-29_17-38-15.xml
# Removed Pett2023-2015-08-03_13-48-28.xml
# Removed Pett2023-2015-08-03_14-22-40.xml
# Removed Pett2023-2015-08-04_12-06-34.xml
# Removed Pett2023-2015-08-05_14-43-08.xml
# Removed Pett2023-2015-08-05_16-59-52.xml
# Removed Pett2023-2015-08-05_21-33-11.xml
# Removed Pett2023-2015-08-06_11-13-11.xml
# Removed Pett2023-2015-08-06_17-37-04.xml
# Removed Pett2023-2015-08-07_13-59-36.xml
# Removed Pett2023-2015-08-07_14-49-18.xml
# Removed Pett2023-2015-08-07_18-08-42.xml
# Removed Pett2023-2015-08-10_15-21-37.xml
# Removed Pett2023-2015-08-10_16-05-55.xml
# Removed Pett2023-2015-08-11_10-24-30.xml
# Removed Pett2023-2015-08-11_16-47-22.xml
# Removed Pett2023-2015-08-11_16-47-23.xml
# Removed Pett2023-2015-08-12_15-17-58.xml
# Removed Pett2023-2015-08-12_15-17-59.xml
# Removed Pett2023-2015-08-13_10-55-00.xml
# Removed Pett2023-2015-08-13_10-55-10.xml
# Removed Pett2023-2015-08-13_18-28-58.xml
# Removed Pett2023-2015-08-17_13-06-17.xml
# Removed Pett2023-2015-08-17_13-23-00.xml
# Removed Pett2023-2015-08-17_15-10-33.xml
# Removed Pett2023-2015-08-17_18-58-50.xml
# Removed Pett2023-2015-08-18_18-33-11.xml
# Removed Pett2023-2015-09-10_11-19-39.xml
# Removed Pett2023-2015-09-24_11-18-47.xml
# Removed Pett2023-2015-09-28_17-45-11.xml
# Removed Pett2023-2015-09-30_20-13-26.xml
# Removed Pett2023-2015-10-20_16-33-58.xml
# Removed Pett2023-2015-10-20_16-47-45.xml
# Removed Pett2023-2015-10-30_11-17-13.xml
# Removed Pett2023-2015-11-09_19-00-12.xml
# Removed Pett2023-2015-11-23_13-53-49.xml
# Removed Pett2023-2016-02-19_20-56-47.xml
# Removed Pett2023-2016-02-24_15-26-54.xml
# Removed Pett2023-2016-05-13_17-01-39.xml
# Removed Pett2023-2016-06-02_14-58-43.xml
# Removed Pett2023-2016-06-06_14-30-24.xml
# Removed Pett2023-2016-06-13_17-39-38.xml
# Removed Pett2023-2016-06-28_15-45-15.xml


# Fiasco
# Removed Pett2023-2018-04-20_15-56-20.xml
# Removed Pett2023-2019-05-24_11-07-51.xml

# UClibc
# Removed Pett2023-2015-06-29_15-01-39.xml
# Removed Pett2023-2015-06-30_19-23-17.xml
# Removed Pett2023-2015-07-02_18-48-59.xml
# Removed Pett2023-2015-07-06_10-50-32.xml
# Removed Pett2023-2015-07-07_19-50-10.xml
# Removed Pett2023-2015-07-13_17-55-29.xml
# Removed Pett2023-2015-07-14_13-31-24.xml
# Removed Pett2023-2015-07-14_15-43-36.xml
# Removed Pett2023-2015-07-21_15-38-17.xml
# Removed Pett2023-2015-07-21_15-38-21.xml
# Removed Pett2023-2015-07-22_14-21-15.xml
# Removed Pett2023-2015-07-28_11-20-02.xml
# Removed Pett2023-2015-07-28_11-23-51.xml
# Removed Pett2023-2015-07-29_17-38-14.xml
# Removed Pett2023-2015-07-29_17-38-15.xml
# Removed Pett2023-2015-08-03_13-48-28.xml
# Removed Pett2023-2015-08-03_14-22-40.xml
# Removed Pett2023-2015-08-04_12-06-34.xml
# Removed Pett2023-2015-08-05_14-43-08.xml
# Removed Pett2023-2015-08-05_16-59-52.xml
# Removed Pett2023-2015-08-05_21-33-11.xml
# Removed Pett2023-2015-08-06_11-13-11.xml
# Removed Pett2023-2015-08-06_17-37-04.xml
# Removed Pett2023-2015-08-07_13-59-36.xml
# Removed Pett2023-2015-08-07_14-49-18.xml
# Removed Pett2023-2015-08-07_18-08-42.xml
# Removed Pett2023-2015-08-10_15-21-37.xml
# Removed Pett2023-2015-08-10_16-05-55.xml
# Removed Pett2023-2015-08-11_10-24-30.xml
# Removed Pett2023-2015-08-11_16-47-22.xml
# Removed Pett2023-2015-08-11_16-47-23.xml
# Removed Pett2023-2015-08-12_15-17-58.xml
# Removed Pett2023-2015-08-12_15-17-59.xml
# Removed Pett2023-2015-08-13_10-55-00.xml
# Removed Pett2023-2015-08-13_10-55-10.xml
# Removed Pett2023-2015-08-13_18-28-58.xml
# Removed Pett2023-2015-08-17_13-06-17.xml
# Removed Pett2023-2015-08-17_13-23-00.xml
# Removed Pett2023-2015-08-17_15-10-33.xml
# Removed Pett2023-2015-08-17_18-58-50.xml
# Removed Pett2023-2015-08-18_18-33-11.xml
# Removed Pett2023-2015-09-10_11-19-39.xml
# Removed Pett2023-2015-09-24_11-18-47.xml
# Removed Pett2023-2015-09-28_17-45-11.xml
# Removed Pett2023-2015-09-30_20-13-26.xml
# Removed Pett2023-2015-10-20_16-33-58.xml
# Removed Pett2023-2015-10-20_16-47-45.xml
# Removed Pett2023-2015-10-30_11-17-13.xml
# Removed Pett2023-2015-11-09_19-00-12.xml
# Removed Pett2023-2015-11-23_13-53-49.xml
# Removed Pett2023-2016-02-19_20-56-47.xml
# Removed Pett2023-2016-02-24_15-26-54.xml
# Removed Pett2023-2016-05-13_17-01-39.xml
# Removed Pett2023-2016-06-02_14-58-43.xml
# Removed Pett2023-2016-06-06_14-30-24.xml
# Removed Pett2023-2016-06-13_17-39-38.xml
# Removed Pett2023-2016-06-28_15-45-15.xml