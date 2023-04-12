import pandas as pd
import hashlib
import argparse
import datetime
import os
import shutil
import json
from pathlib import Path
from utils import get_latest_version, get_first_version, get_model_json, get_latest_variant, get_first_variant


def get_file_name(path):
    return Path(path).stem
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_colwidth', None)

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
#    #Features
#    #Temp_Variables
#    #Constraints
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


df_all = pd.read_csv("statistics/complete_new.csv", sep=';')


# columns = list(df_all.columns)
# print(columns)

# init default values
# domain_values = list(df_all['Domain'].unique())
# format_values = list(df_all['Format'].unique())
# # source_values = list(df_all['Source'].unique())
# feature_range = (int(min(df_all['#Features'])), int(max(df_all['#Features'])))
# ctc_range = (int(min(df_all['#Constraints'])),
#              int(max(df_all['#Constraints'])))
# name_regex = '.*'
VARIANT_SELECTORS = ["all", "none", "first", "last"]


def init_args():
    parser = argparse.ArgumentParser(
        description='Derive feature-model subset according to filtering')
    parser.add_argument('--show_filter_options',
                        help="Show possible values for all filters")
    parser.add_argument('--domains', type=str, nargs="+", default=domain_values,
                        help="Only include feature models belonging to list of domains")
    parser.add_argument('--features', type=str, default=str(feature_range[0]) + ".." + str(
        feature_range[1]), help="Only include feature models with between X--Y features")
    parser.add_argument('--original_formats', type=str, nargs="+", default=format_values,
                        help="Only include feature models of a specific format")
    parser.add_argument('--output_format', type=str, default="uvl",
                        help="Select format of output feature models: uvl|dimacs|orignal")
    parser.add_argument('--name', type=str, default='.*',
                        help="Only include feature models whose name matches the regex")
    parser.add_argument('--evolution', type=bool, default=False,
                        help="Only provide feature models with a history")
    parser.add_argument('--constraints', type=str, default=str(ctc_range[0]) + ".." + str(
        ctc_range[1]), help="Only include feature models with between X--Y constraints")
    parser.add_argument('--save_path', type=str, default="benchmark" + str(datetime.datetime.now()),
                        help="Provide directory path for storing benchmark and meta data")
    parser.add_argument('--versions', type=str, default="all",
                        help="Which version(s) to include: " + str(VARIANT_SELECTORS))
    parser.add_argument('--variants', type=str, default="all",
                        help="Which variants of a system to include: " + str(VARIANT_SELECTORS))
    parser.add_argument('--load_config', type=str, default=None,
                        help="Path configuration file to load")

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
    # return [min, max]
    return [int(range_string.split('..')[0].strip()), int(range_string.split('..')[1].strip())]


def printFilterOptions():
    print("Name: " + name_regex)
    print("Domain: " + str(domain_values))
    print("Format: " + str(format_values))
    print("#Features: " + str(feature_range[0]) + ".." + str(feature_range[1]))
    print("#Constraints: " + str(ctc_range[0]) + ".." + str(ctc_range[1]))


def applyFilter(df, filter_dict : dict):
    df = df[df['Domain'].isin(filter_dict['Domain'])]
    df = df[df['Format'].isin(filter_dict['OriginalFormat'])]
    df = df[df['#Features'] >= filter_dict['Features'][0]]
    df = df[df['#Features'] <= filter_dict['Features'][1]]
    df = df[df['#Constraints'] >= filter_dict['Constraints'][0]]
    df = df[df['#Constraints'] <= filter_dict['Constraints'][1]]
    df = df[df['Name'].str.match(filter_dict['Name'])]
    if filter_dict['Evolution']:
        df = df[df['PartOfHistory'] == True]
    df = filter_by_version_strategy(df, filter_dict['Versions'])
    df = filter_by_variant_strategy(df, filter_dict['Variants'])
    return df

def filter_by_version_strategy(df : pd.DataFrame, strategy : str):
    if strategy == 'all':
        return df
    elif strategy == 'None':
        return df[df['PartOfHistory'] != True]
    elif strategy == 'first':
        return filter_version_first_strategy(df)
    elif strategy == 'last':
        return filter_version_latest_strategy(df)
    

def filter_version_latest_strategy(df : pd.DataFrame):
    paths = list(df['Domain'] + "/" + df['Name'] + "/" + df['Origin'] + ".json")
    full_paths = [os.path.join("feature_models", "original", model_path) for model_path in paths]
    latest_version = [get_latest_version(get_model_json(full_path)) for full_path in full_paths]
    df['LatestVersion'] = latest_version
    df = df[((df['PartOfHistory'] == False)) | (df['Version'] == df['LatestVersion'])]
    df = df.drop('LatestVersion', axis=1)
    return df

def filter_version_first_strategy(df : pd.DataFrame):
    paths = list(df['Domain'] + "/" + df['Name'] + "/" + df['Origin'] + ".json")
    full_paths = [os.path.join("feature_models", "original", model_path) for model_path in paths]
    first_version = [get_first_version(get_model_json(full_path)) for full_path in full_paths]
    df['VersionOfInterest'] = first_version
    df = df[((df['PartOfHistory'] == False)) | (df['Version'] == df['VersionOfInterest'])]
    df = df.drop('VersionOfInterest', axis=1)
    return df

def filter_by_variant_strategy(df : pd.DataFrame, strategy : str):
    if strategy == 'all':
        return df
    elif strategy == 'None':
        return df[df['PartOfHistory'] != True]
    elif strategy == 'first':
        return filter_variant_first_strategy(df)
    elif strategy == 'last':
        return filter_variant_latest_strategy(df)

def filter_variant_latest_strategy(df : pd.DataFrame):
    paths = list(df['Domain'] + "/" + df['Name'] + "/" + df['Origin'] + ".json")
    full_paths = [os.path.join("feature_models", "original", model_path) for model_path in paths]
    latest_version = [get_latest_variant(get_model_json(full_path)) for full_path in full_paths]
    df['VersionOfInterest'] = latest_version
    df = df[((df['VersionOfInterest'] == "")) | (df['Version'] == df['VersionOfInterest'])]
    df = df.drop('VersionOfInterest', axis=1)
    return df

def filter_variant_first_strategy(df : pd.DataFrame):
    paths = list(df['Domain'] + "/" + df['Name'] + "/" + df['Origin'] + ".json")
    full_paths = [os.path.join("feature_models", "original", model_path) for model_path in paths]
    first_version = [get_first_version(get_model_json(full_path)) for full_path in full_paths]
    df['VersionOfInterest'] = first_version
    df = df[((df['VersionOfInterest'] == "")) | (df['Version'] == df['VersionOfInterest'])]
    df = df.drop('VersionOfInterest', axis=1)
    return df



def filter_data_frame_by_list_of_models(data_frame, models):
    clean_file_names = [get_file_name(model) for model in models]
    return data_frame[data_frame['Name'].isin(clean_file_names)]


def create_benchmark_directory(data_frame, target_directory):
    os.makedirs(os.path.join(target_directory, "feature_models"))
    data_frame.to_csv(os.path.join(target_directory,
                      "statistics.csv"), ";", index=False)

    # Create domain directories
    for domain in list(data_frame['Domain'].unique()):
        os.makedirs(os.path.join(target_directory, "feature_models", domain))

    for model_path in list(data_frame['Path']):
        Path(os.path.join(target_directory,os.path.dirname(model_path))).mkdir(parents=True, exist_ok=True)
        shutil.copy(model_path,
                    os.path.join(target_directory, model_path))

    create_benchmark_json(data_frame, os.path.join(
        target_directory, "config.json"))


def create_benchmark_directory_from_config(config_path, data_frame, target_directory):
    with open(config_path) as config_file:
        data = json.load(config_file)
        feature_models = data['Feature Models']
        filtered_frame = filter_data_frame_by_list_of_models(
            data_frame, feature_models)
        create_benchmark_directory(filtered_frame, target_directory)


def create_properties_dict():
    return {"Title": "", "Analyses": [], "Reasoning Engines": [], "Date": str(datetime.date.today()), "DOI": "",
            "Filter": {
                "Domains": domain_values,
                "Formats": format_values,
                "#Features": str(feature_range[0]) + ".." + str(feature_range[1]),
                "#Constraints": str(ctc_range[0]) + ".." + str(ctc_range[1])
    }}


def data_frame_to_dict(data_frame):
    return data_frame.to_dict(orient="list")


def create_benchmark_json(data_frame, json_path='benchmark.json'):
    value_dict = create_properties_dict()
    data_frame["Feature Models"] = data_frame['Domain'] + \
        "/" + data_frame['Name'] + data_frame['Format']
    name_data_frame = data_frame[["Feature Models"]]
    model_dict = data_frame_to_dict(name_data_frame)
    value_dict.update(model_dict)
    with open(json_path, 'w') as outfile:
        json.dump(value_dict, outfile, indent=4)


# args = init_args()
# if args.load_config is not None:
#     create_benchmark_directory_from_config(
#         args.load_config, df_all, "configbenchmark")
# elif args.show_filter_options:
#     printFilterOptions()
# else:
#     filter_dict = parse_filter_args(args)
#     df_filtered = applyFilter(df_all, filter_dict)
#     create_benchmark_directory(df_filtered, "testbenchmark")


df = filter_by_version_strategy(df_all, "last")
create_benchmark_directory(df, "testbenchmark")
