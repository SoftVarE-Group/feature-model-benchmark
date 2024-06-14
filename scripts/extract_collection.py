import pandas as pd
import argparse
import datetime
import os
import shutil
import json
from pathlib import Path
from utils import get_latest_version, get_first_version, get_model_json, get_latest_variant, get_first_variant, get_extension, get_describing_path
import numpy as np

# name filter default

# Regex
#    Name
#    Version
# Enum
#    Domain
#    Source
#    Format
#    ConvertedFrom
#    Conversion_Tool
# Range
#    NumberOfFeatures
#    #Temp_Variables
#    Number_Constraints
#    #Clauses
#    #Configs
#    #Core
#    #Atomic
#    <Metric>
# Boolean
#    Void
#    Hierarchy
#    Implementation
#    BooleanFeatures
#    IntegerFeatures
#    FloatFeatures
#    StringFeatures
#    BooleanAttributes
#    IntegerAttributes
#    FloatAttributes
#    StringAttributes

# load statistics file
df_all = pd.read_csv("statistics/Complete.csv", sep=';')

# Filter cfr models
df_all = df_all[df_all['Format'] != 'Clafer']

# replace ? with nan in relevant numeric columns
NUMERIC_COLUMNS = ['NumberOfFeatures', 'Number_Constraints']
df_all[NUMERIC_COLUMNS] = df_all[NUMERIC_COLUMNS].apply(pd.to_numeric, errors = 'coerce')


# init default values
available_domains = list(df_all['Domain'].unique())
available_formats = list(df_all['Format'].unique())
available_sources = list(df_all['Source'].unique())
available_feature_range = (
    int(min(df_all['NumberOfFeatures'])), int(max(df_all['NumberOfFeatures'])))
available_ctc_range = (int(min(df_all['Number_Constraints'])),
                       int(max(df_all['Number_Constraints'])))
default_name_regex = '.*'
VARIANT_SELECTORS = ["all", "none", "first", "last"]


def init_args():
    parser = argparse.ArgumentParser(
        description='Derive feature-model subset according to filtering')
    parser.add_argument('--show_filter_options',
                        help="Show possible values for all filters")
    parser.add_argument('--domains', type=str, nargs="+", default=available_domains,
                        help="Only include feature models belonging to list of domains")
    parser.add_argument('--features', type=str, default=str(available_feature_range[0]) + ".." + str(
        available_feature_range[1]), help="Only include feature models with between X..Y features")
    parser.add_argument('--original_formats', type=str, nargs="+", default=available_formats,
                        help="Only include feature models of a specific format")
    parser.add_argument('--output_format', type=str, default="uvl",
                        help="Select format of output feature models: uvl|dimacs|orignal")
    parser.add_argument('--name', type=str, default='.*',
                        help="Only include feature models whose name matches the regex")
    parser.add_argument('--evolution', action='store_true', default=False,
                        help="Only provide feature models with a history")
    parser.add_argument('--constraints', type=str, default=str(available_ctc_range[0]) + ".." + str(
        available_ctc_range[1]), help="Only include feature models with between X--Y constraints")
    parser.add_argument('--save_path', type=str, default="benchmark" + str(datetime.datetime.now()),
                        help="Provide directory path for storing benchmark and meta data")
    parser.add_argument('--versions', type=str, default="all",
                        help="Which version(s) to include: " + str(VARIANT_SELECTORS))
    parser.add_argument('--variants', type=str, default="all",
                        help="Which variants of a system to include: " + str(VARIANT_SELECTORS))
    parser.add_argument('--load_config', type=str, default=None,
                        help="Path configuration file to load")
    parser.add_argument('--flat', action='store_true', help="Provides the feature models as a flat hierarchy instead of nested directories")

    return parser.parse_args()


def parse_filter_args(args):
    return {
        'Domain': args.domains,
        'OriginalFormat': args.original_formats,
        'Features': evaluate_range_string(args.features),
        'Constraints': evaluate_range_string(args.constraints),
        'OutputFormat': args.output_format,
        'Name': args.name,
        'Evolution': args.evolution,
        'SavePath': args.save_path,
        'Versions': args.versions,
        'Variants': args.variants
    }


def evaluate_range_string(range_string):
    range_split = range_string.split('..')
    min = int(range_split[0].strip()) if range_split[0] != "" else 0
    max = int(range_split[1].strip()) if range_split[1] != "" else float('inf')
    return [min, max]


def printFilterOptions():
    print("Name: " + default_name_regex)
    print("Domain: " + str(available_domains))
    print("Format: " + str(available_formats))
    print("NumberOfFeatures: " +
          str(available_feature_range[0]) + ".." + str(available_feature_range[1]))
    print("Number_Constraints: " +
          str(available_ctc_range[0]) + ".." + str(available_ctc_range[1]))


def applyFilter(df, filter_dict: dict):
    df = df[df['Domain'].isin(filter_dict['Domain'])]
    df = df[df['Format'].isin(filter_dict['OriginalFormat'])]
    df = df[df['NumberOfFeatures'] >= filter_dict['Features'][0]]
    df = df[df['NumberOfFeatures'] <= filter_dict['Features'][1]]
    df = df[df['Number_Constraints'] >= filter_dict['Constraints'][0]]
    df = df[df['Number_Constraints'] <= filter_dict['Constraints'][1]]
    df = df[df['Name'].str.match(filter_dict['Name'])]
    if filter_dict['Evolution']:
        df = df[df['PartOfHistory'] == True]
    df = filter_by_version_strategy(df, filter_dict['Versions'])
    df = filter_by_variant_strategy(df, filter_dict['Variants'])
    return df


def filter_by_version_strategy(df: pd.DataFrame, strategy: str):
    if strategy == 'all':
        return df
    elif strategy == 'None':
        return df[df['PartOfHistory'] != True]
    elif strategy == 'first':
        return filter_version_first_strategy(df)
    elif strategy == 'last':
        return filter_version_latest_strategy(df)


def filter_version_latest_strategy(df: pd.DataFrame):
    paths = list(df['Domain'] + "/" + df['Name'] +
                 "/" + df['Origin'] + ".json")
    full_paths = [os.path.join(
        "feature_models", "original", model_path) for model_path in paths]
    latest_version = [get_latest_version(
        get_model_json(full_path)) for full_path in full_paths]
    df['LatestVersion'] = latest_version
    df = df[((df['PartOfHistory'] == False)) | (
        df['Version'] == df['LatestVersion'])]
    df = df.drop('LatestVersion', axis=1)
    return df


def filter_version_first_strategy(df: pd.DataFrame):
    paths = list(df['Domain'] + "/" + df['Name'] +
                 "/" + df['Origin'] + ".json")
    full_paths = [os.path.join(
        "feature_models", "original", model_path) for model_path in paths]
    first_version = [get_first_version(
        get_model_json(full_path)) for full_path in full_paths]
    df['VersionOfInterest'] = first_version
    df = df[((df['PartOfHistory'] == False)) | (
        df['Version'] == df['VersionOfInterest'])]
    df = df.drop('VersionOfInterest', axis=1)
    return df


def filter_by_variant_strategy(df: pd.DataFrame, strategy: str):
    if strategy == 'all':
        return df
    elif strategy == 'None':
        return df[df['PartOfHistory'] != True]
    elif strategy == 'first':
        return filter_variant_first_strategy(df)
    elif strategy == 'last':
        return filter_variant_latest_strategy(df)


def filter_variant_latest_strategy(df: pd.DataFrame):
    paths = list(df['Domain'] + "/" + df['Name'] +
                 "/" + df['Origin'] + ".json")
    full_paths = [os.path.join(
        "feature_models", "original", model_path) for model_path in paths]
    latest_version = [get_latest_variant(
        get_model_json(full_path)) for full_path in full_paths]
    df['VersionOfInterest'] = latest_version
    df = df[((df['VersionOfInterest'] == "")) | (
        df['Version'] == df['VersionOfInterest'])]
    df = df.drop('VersionOfInterest', axis=1)
    return df


def filter_variant_first_strategy(df: pd.DataFrame):
    paths = list(df['Domain'] + "/" + df['Name'] +
                 "/" + df['Origin'] + ".json")
    full_paths = [os.path.join(
        "feature_models", "original", model_path) for model_path in paths]
    first_version = [get_first_version(
        get_model_json(full_path)) for full_path in full_paths]
    df['VersionOfInterest'] = first_version
    df = df[((df['VersionOfInterest'] == "")) | (
        df['Version'] == df['VersionOfInterest'])]
    df = df.drop('VersionOfInterest', axis=1)
    return df


def filter_data_frame_by_list_of_models(data_frame, models):
    return data_frame[data_frame['Path'].isin(models)]


def update_source_path_according_to_output_format(path: str, output_format):
    if output_format == 'original':
        return path
    if path.split('.')[-1] == output_format:
        return path
    if path.split('.')[-1] == 'zip':
        without_zip = os.path.splitext(path)[0]
        if without_zip.split('.')[-1] == output_format:
            return path
        else:
           without_zip = without_zip.replace('original', output_format)
           return os.path.splitext(without_zip)[0] + "." + output_format
    path = path.replace('original', output_format)
    return os.path.splitext(path)[0] + "." + output_format

def update_target_path_according_to_output_format(path: str, output_format):
    if output_format == 'original':
        return path
    return path.replace('/original/', f'/{output_format}/')

def get_flat_target_path(directory, original_path : str):
    path_split = original_path.split('/')
    return os.path.join(directory, f'{path_split[2]}-{path_split[3]}-{path_split[4]}')
    
def create_properties_dict_from_filter(filter_dict):
    if 'SavePath' in filter_dict: del filter_dict['SavePath']
    return {"Title": "", "Analyses": [], "Reasoning Engines": [], "Date": str(datetime.date.today()), "DOI": "",
            "Filter": filter_dict
    }


def create_properties_dict_config(config_json):
    return {"Title": "", "Dataset From": config_json['Title'], "Analyses": [], "Reasoning Engines": [], "Date": str(datetime.date.today()), "DOI": ""}

def create_benchmark_directory(data_frame, target_directory, output_format='original', value_dict=None, flat=False):
    os.makedirs(os.path.join(target_directory, "feature_models"))
    data_frame.to_csv(os.path.join(target_directory,
                      "statistics.csv"), ";", index=False)
    
    data_frame['Path'] = data_frame.apply(
        lambda row: update_source_path_according_to_output_format(row.Path, output_format), axis=1)

    for model_path in list(data_frame['Path']):
        if flat:
            dir_path = os.path.join(target_directory, 'feature_models', output_format)
            full_path = get_flat_target_path(dir_path, model_path)
        else:
            dir_path = update_target_path_according_to_output_format(os.path.join(target_directory, os.path.dirname(model_path)), output_format)
            full_path = update_target_path_according_to_output_format(os.path.join(target_directory, model_path), output_format)
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        if Path(dir_path).exists():
            shutil.copy(model_path, full_path)
            if ".zip" in model_path:
                temp_extract_dir = os.path.join(dir_path, "temp/")
                shutil.unpack_archive(full_path, temp_extract_dir)
                shutil.copyfile(os.path.join(temp_extract_dir, os.listdir(temp_extract_dir)[0]), full_path.replace(
                    get_extension(full_path), get_extension(os.listdir(temp_extract_dir)[0])))
                shutil.rmtree(temp_extract_dir)
                os.remove(full_path)               

        else:
            print("Warning: " + output_format +
                  " file for " + model_path + " is missing.")

    create_benchmark_json(data_frame, create_properties_dict_from_filter(value_dict), os.path.join(
        target_directory, "config.json"))
    print(f'Partial benchmark stored in {target_directory}')


def create_benchmark_directory_from_config(config_path, data_frame, target_directory, output_format='original', flat=False):
    with open(config_path) as config_file:
        data = json.load(config_file)
        feature_models = data['Feature Models']
        filtered_frame = filter_data_frame_by_list_of_models(
            data_frame, feature_models)
        create_benchmark_directory(
            filtered_frame, target_directory, output_format=output_format, value_dict=create_properties_dict_config(data), flat=flat)


def data_frame_to_dict(data_frame):
    return data_frame.to_dict(orient="list")


def create_benchmark_json(data_frame: pd.DataFrame, value_dict, json_path='benchmark.json'):
    name_data_frame = data_frame[["Path"]]
    name_data_frame = name_data_frame.rename(columns={'Path': 'FeatureModels'})
    model_dict = data_frame_to_dict(name_data_frame)
    value_dict.update(model_dict)
    with open(json_path, 'w') as outfile:
        json.dump(value_dict, outfile, indent=4, ensure_ascii=False)


args = init_args()
if args.load_config is not None:
    create_benchmark_directory_from_config(
        args.load_config, df_all, "configbenchmark", args.output_format, flat=args.flat)
elif args.show_filter_options:
    printFilterOptions()
else:
    filter_dict = parse_filter_args(args)
    df_filtered = applyFilter(df_all, filter_dict)
    create_benchmark_directory(
        df_filtered, "testbenchmark", filter_dict["OutputFormat"], filter_dict, flat=args.flat)
