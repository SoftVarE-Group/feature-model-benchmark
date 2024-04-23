import os
import json
from pathlib import Path
import pandas as pd
# -------------------------- File Management --------------------------

def get_files_from_directory(directory_path, supported_suffixes):
    return [os.path.join(path, file) for path, directory, files in os.walk(directory_path) for file in files if file.endswith(tuple(supported_suffixes))]


def read_csv_to_dataframe(path, delimiter=';'):
    return pd.read_csv(path, delimiter=delimiter)


# -------------------------- Create Table --------------------------

def get_extension(path):
    return path.split(".", 1)[1]


def get_domain_from_relative_path(path, depth_of_root=0):
    return path.split("/")[depth_of_root + 2]


def get_system_name(path, depth_of_root=0):
    return path.split("/")[depth_of_root + 3]


def get_model_json(path):
    with open(path) as json_file:
        return json.load(json_file)


def get_file_format(model_json):
    return model_json['OriginalFormat']


def get_keywords(model_json):
    return model_json['Keywords']


def get_publication(model_json):
    return model_json['Publication']


def get_source(model_json):
    return model_json['Source']


def get_hierarchy(model_json):
    return model_json['Hierarchy']


def get_conversion_tool(model_json):
    return model_json['ConversionTool']


def get_year(model_json):
    return model_json['Year']

def get_keywords(model_json):
    if model_json.get('Keywords') is None:
        return []
    return model_json['Keywords']

def get_origin(path):
    file_name = Path(path).stem
    return file_name.split('-')[0]


def get_version(path):
    if "-" in Path(path).stem:
        fileName = Path(path).stem
        while "." in fileName:
            fileName = Path(fileName).stem
        return fileName.split('-', 1)[1]
    return ""


def get_no_versions(model_json):
    if 'History' in model_json.keys():
        return len(model_json['History'])
    return 0

def get_latest_version(model_json):
    if 'History' in model_json.keys() and len(model_json['History']) > 0:
        return model_json['History'][-1]
    return ""

def get_first_version(model_json):
    if 'History' in model_json.keys() and len(model_json['History']) > 0:
        return model_json['History'][0]
    return ""


def get_latest_variant(model_json):
    if 'Variants' in model_json.keys() and len(model_json['Variants']) > 0:
        return model_json['Variants'][-1]
    return ""

def get_first_variant(model_json):
    if 'Variants' in model_json.keys() and len(model_json['Variants']) > 0:
        return model_json['Variants'][0]
    return ""


def get_version_range(model_json):
    if 'History' in model_json.keys() and len(model_json['History']) != 0:
        return model_json['History'][0] + ".." + model_json['History'][-1]
    return ""


def get_no_variants(model_json):
    if 'Variants' in model_json.keys():
        return len(model_json['Variants'])

    return 0


def get_json_for_model(model_path):
    file_name = model_path.split("/")[-1]
    if "-" in file_name:
        adapted_file_name = file_name.split("-", 1)[0] + ".json"
    else:
        adapted_file_name = file_name.split(".", 1)[0] + ".json"
    return get_model_json(model_path.replace(file_name, adapted_file_name))

# returns path consisting of domain/system/model
def get_describing_path(original_path):
    split = original_path.split("/")
    return os.path.join(split[-3], split[-2], Path(split[-1]).stem)


def get_data_frame_subset(data_frame, filter_column=None, row_values_to_keep=[], columns_to_keep=None):
    filtered_df = data_frame
    if not columns_to_keep is None:
        filtered_df = data_frame[columns_to_keep]
    if not filter_column is None:
        filtered_df = filtered_df[filtered_df[filter_column].isin(
            row_values_to_keep)]

    return filtered_df
