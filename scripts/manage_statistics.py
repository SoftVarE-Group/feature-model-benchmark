import numpy as np
import pandas as pd
import os
from pathlib import Path
import json
import shutil

USER_COLUMNS = ["Publication", "Keywords",
                "Source", "ConvertedFrom", "Conversion_Tool"]
SUPPORTED_SUFFIXES = ["uvl", "xml", "dimacs", "afm", "zip", "cfr", "fm"]


# -------------------------- File Management --------------------------

def get_files_from_directory(directory_path, supported_suffixes):
    return [os.path.join(path, file) for path, directory, files in os.walk(directory_path) for file in files if file.endswith(tuple(supported_suffixes))]


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
        


# -------------------------- JSON Generation --------------------------
def get_evolution_steps(dir_path):
    files = get_files_from_directory(dir_path, SUPPORTED_SUFFIXES)
    versions = [get_file_name(file).split('-', 1)[1] for file in files]
    versions.sort()
    print(json.dumps(versions))


# -------------------------- CDL structure --------------------------

def create_cdl_dir(new_path="cdl"):
    cfr_files = get_files_from_directory("feature_models/original/systems_software/eCos-benchmark-clafer", [".cfr"])
    for file_path in cfr_files:
        dir = os.path.join(new_path,get_file_name(file_path))
        os.makedirs(dir)
        shutil.copyfile(file_path, os.path.join(dir,"Passos2011.cfr"))
        value_dict = {
            "Name" : get_file_name(file_path),
            "Year" : 2011,
            "Hierarchy" : True,
            "OriginalFormat" : "Clafer",
            "Versions" : [],
            "Publication" : "https://doi.org/10.1145/2019136.2019139",
            "Source" : "https://gsd.uwaterloo.ca/FOSD11",
            "Variants": [],
            "Keywords" : [
                "CDL",
                "Automatic"
            ],
            "ConversionTool" : ""
        }
        with open(os.path.join(dir,"Passos2011.json"), "w") as outfile:
            json.dump(value_dict, outfile)
    
    dimacs_files = get_files_from_directory("feature_models/original/systems_software/eCos-benchmark-clafer", [".dimacs"])
    for file_path in dimacs_files:
        dir = os.path.join(new_path,get_file_name(file_path))
        shutil.copyfile(file_path, os.path.join(dir, "Berger2013.dimacs"))
        value_dict = {
            "Name" : get_file_name(file_path),
            "Year" : 2013,
            "Hierarchy" : False,
            "OriginalFormat" : "DIMACS",
            "Versions" : [],
            "Publication" : "https://doi.org/10.1109/TSE.2013.34",
            "Source" : "https://gsd.uwaterloo.ca/industrial-variability-modeling",
            "Keywords" : [
                "CDL",
                "Automatic"
            ],
            "ConversionTool" : ""
        }
        with open(os.path.join(dir,"Berger2013.json"), "w") as outfile:
            json.dump(value_dict, outfile)

    xml_files = get_files_from_directory("/home/chico/git/data/is-there-a-mismatch/Data/LargeFeatureModels/CDL", [".xml"])
    for file_path in xml_files:
        dir = os.path.join(new_path,get_file_name(file_path))
        shutil.copyfile(file_path, os.path.join(dir, "Knüppel2017.xml"))
        value_dict = {
            "Name" : get_file_name(file_path),
            "Year" : 2017,
            "Hierarchy" : True,
            "OriginalFormat" : "FeatureIDE",
            "Versions" : [],
            "Publication" : "https://doi.org/10.1145/3106237.3106252",
            "Source" : "https://github.com/AlexanderKnueppel/is-there-a-mismatch",
            "Keywords" : [
                "CDL",
                "Automatic"
            ],
            "ConversionTool" : ""
        }
        with open(os.path.join(dir,"Knüppel2017.json"), "w") as outfile:
            json.dump(value_dict, outfile)



# load_feature_models("feature_models")
# add_new_feature_models("feature_models", "statistics/complete.csv")
# get_data_frame_subset(read_csv_to_dataframe("statistics/complete.csv"), filter_column="Name", row_values_to_keep=["Automotive1", "ERP-System"],columns_to_keep=["Name", "Domain"])

# create_benchmark_json({'Publication Title' : 'Fun Fun', 'Filter' : [ {'Domain': 'Automotive'}, {'#Features' : '100-1000'} ], 'DOI' : 'doi.org/hehe'}, read_csv_to_dataframe("statistics/complete.csv"))

# append_analysis_results(read_csv_to_dataframe("statistics/models.csv"), read_csv_to_dataframe("/home/chico/git/software/Feature-Model-Structure-Analysis/result.csv"))

get_evolution_steps("feature_models/original/systems_software/Linux-Commits-Nieke")
# create_cdl_dir()