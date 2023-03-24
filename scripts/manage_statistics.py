import numpy as np
import pandas as pd
import os
from pathlib import Path
import json

USER_COLUMNS = ["Publication", "Keywords",
                "Source", "ConvertedFrom", "Conversion_Tool"]
SUPPORTED_SUFFIXES = ["uvl", "xml", "dimacs", "afm", "zip", "cfr", "fm"]


# -------------------------- File Management --------------------------

def get_files_from_directory(directory_path, supported_suffixes):
    suffices_regex = '(*.' + '|*.'.join(supported_suffixes) + ')'
    print(suffices_regex)
    return [os.path.join(path, file) for path, directory, files in os.walk(directory_path) for file in files]


def read_csv_to_dataframe(path):
    return pd.read_csv(path, delimiter=";")


# -------------------------- Create Table --------------------------

def add_user_input_columns(data_frame):
    for header in USER_COLUMNS:
        data_frame[header] = ""
    return data_frame


def get_domain_from_relative_path(path, depth_of_root=0):
    return path.split("/")[depth_of_root + 1]


def get_file_name(path):
    return Path(path).stem

def get_file_format(path):
    _, extension = os.path.splitext(path)
    return extension 


def load_feature_models(directory_path, output_path="statistics/models.csv"):
    model_paths = get_files_from_directory(directory_path, SUPPORTED_SUFFIXES)
    data_frame = data_frame_from_models_list(model_paths)
    data_frame.to_csv(output_path, ";", index=False)


def data_frame_from_models_list(model_paths):
    domains = [get_domain_from_relative_path(model) for model in model_paths]
    model_names = [get_file_name(model) for model in model_paths]
    formats = [get_file_format(model) for model in model_paths]

    data_frame = pd.DataFrame({'Name': model_names, 'Domain': domains, 'Format' : formats})
    data_frame = add_user_input_columns(data_frame)
    data_frame = data_frame.sort_values(["Domain", "Name"])
    return data_frame

def append_analysis_results(models_data_frame, analysis_data_frame, output_path="statistics/complete.csv"):
    models_data_frame = models_data_frame.sort_values(["Name"]).reset_index(drop=True)
    print(models_data_frame)
    analysis_data_frame = analysis_data_frame.sort_values(["Name"]).reset_index(drop=True)
    print(analysis_data_frame)
    analysis_data_frame = analysis_data_frame.drop(columns='Name')
    combined_data_frame = pd.concat([models_data_frame, analysis_data_frame], axis=1)
    combined_data_frame = combined_data_frame.sort_values(["Domain", "Name"])

    combined_data_frame.to_csv(output_path, ";", index=False)



# -------------------------- Update Table --------------------------


def add_new_feature_models(directory_path, old_csv_path):
    existing_data_frame = read_csv_to_dataframe(old_csv_path)

    model_paths = get_files_from_directory(directory_path, SUPPORTED_SUFFIXES)
    new_model_paths = [
        model_path for model_path in model_paths if not get_file_name(model_path) in existing_data_frame['Name'].values]
    new_data_frame = data_frame_from_models_list(new_model_paths)
    combined_data_frame = pd.concat([existing_data_frame,new_data_frame])
    combined_data_frame = combined_data_frame.sort_values(["Domain", "Name"])
    combined_data_frame.to_csv(old_csv_path, ";", index=False)



# -------------------------- Filter Table --------------------------

def get_data_frame_subset(data_frame, filter_column=None, row_values_to_keep=[], columns_to_keep=None):
    filtered_df = data_frame
    if not columns_to_keep is None:
        filtered_df = data_frame[columns_to_keep]
    if not filter_column is None:
        filtered_df = filtered_df[filtered_df[filter_column].isin(row_values_to_keep)]

    return filtered_df
        





# load_feature_models("feature_models")
# add_new_feature_models("feature_models", "statistics/complete.csv")
# get_data_frame_subset(read_csv_to_dataframe("statistics/complete.csv"), filter_column="Name", row_values_to_keep=["Automotive1", "ERP-System"],columns_to_keep=["Name", "Domain"])

# create_benchmark_json({'Publication Title' : 'Fun Fun', 'Filter' : [ {'Domain': 'Automotive'}, {'#Features' : '100-1000'} ], 'DOI' : 'doi.org/hehe'}, read_csv_to_dataframe("statistics/complete.csv"))

append_analysis_results(read_csv_to_dataframe("statistics/models.csv"), read_csv_to_dataframe("/home/chico/git/software/Feature-Model-Structure-Analysis/result.csv"))