import pandas as pd
import argparse
import datetime
import os
import shutil
import json
from pathlib import Path
from utils import get_latest_version, get_first_version, get_model_json, get_latest_variant, get_first_variant, get_extension, get_describing_path

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

# load statistics file
df_all = pd.read_csv("statistics/FullCombined.csv", sep=';')

# init default values
available_domains = list(df_all['Domain'].unique())
available_formats = list(df_all['Format'].unique())
available_sources = list(df_all['Source'].unique())
available_feature_range = (
    int(min(df_all['#Features'])), int(max(df_all['#Features'])))
available_ctc_range = (int(min(df_all['#Constraints'])),
                       int(max(df_all['#Constraints'])))
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
    print("#Features: " +
          str(available_feature_range[0]) + ".." + str(available_feature_range[1]))
    print("#Constraints: " +
          str(available_ctc_range[0]) + ".." + str(available_ctc_range[1]))


def applyFilter(df, filter_dict: dict):
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


def udpate_path_according_to_output_format(path: str, output_format):
    if output_format == 'original':
        return path
    path = path.replace('original', output_format)
    return os.path.splitext(path)[0] + "." + output_format


def create_properties_dict():
    return {"Title": "", "Analyses": [], "Reasoning Engines": [], "Date": str(datetime.date.today()), "DOI": "",
            "Filter": {
                "Domains": available_domains,
                "Formats": available_formats,
                # "#Features": str(feature_range[0]) + ".." + str(feature_range[1]),
                # "#Constraints": str(ctc_range[0]) + ".." + str(ctc_range[1])
    }}


def create_properties_dict_config(config_json):
    return {"Title": "", "Dataset From": config_json['Title'], "Analyses": [], "Reasoning Engines": [], "Date": str(datetime.date.today()), "DOI": ""}


def create_benchmark_directory(data_frame, target_directory, output_format='original', value_dict=create_properties_dict()):
    os.makedirs(os.path.join(target_directory, "feature_models"))
    data_frame.to_csv(os.path.join(target_directory,
                      "statistics.csv"), ";", index=False)

    data_frame['Path'] = data_frame.apply(
        lambda row: udpate_path_according_to_output_format(row.Path, output_format), axis=1)

    for model_path in list(data_frame['Path']):
        dir_path = os.path.join(target_directory, os.path.dirname(model_path))
        dir_path = os.path.join(target_directory, os.path.dirname(model_path))
        full_path = os.path.join(target_directory, model_path)
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

    create_benchmark_json(data_frame, value_dict, os.path.join(
        target_directory, "config.json"))


def create_benchmark_directory_from_config(config_path, data_frame, target_directory, output_format='original'):
    with open(config_path) as config_file:
        data = json.load(config_file)
        feature_models = data['Feature Models']
        filtered_frame = filter_data_frame_by_list_of_models(
            data_frame, feature_models)
        create_benchmark_directory(
            filtered_frame, target_directory, output_format=output_format, value_dict=create_properties_dict_config(data))


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
        args.load_config, df_all, "configbenchmark", args.output_format)
elif args.show_filter_options:
    printFilterOptions()
else:
    filter_dict = parse_filter_args(args)
    df_filtered = applyFilter(df_all, filter_dict)
    create_benchmark_directory(
        df_filtered, "testbenchmark", filter_dict["OutputFormat"])
