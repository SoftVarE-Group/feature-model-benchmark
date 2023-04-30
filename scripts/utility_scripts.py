import json
import shutil
import os
import zipfile
import pandas as pd
import re
from utils import get_files_from_directory, get_system_name, read_csv_to_dataframe

# -------------------------- JSON Generation --------------------------


def get_evolution_steps(dir_path, supported_suffixes):
    files = get_files_from_directory(dir_path, supported_suffixes)
    versions = [get_system_name(file).split('-', 1)[1] for file in files]
    versions.sort()
    print(json.dumps(versions))

# -------------------------- Get Meta Data --------------------------


def get_number_of_systems(data_frame):
    return data_frame.Name.nunique()


def get_number_of_domains(data_frame):
    return data_frame.Domain.nunique()


def get_no_feature_models_per_domain(data_frame: pd.DataFrame):
    return data_frame['Domain'].value_counts()


def get_no_unique_publications(data_frame: pd.DataFrame):
    return data_frame.Publication.nunique()


def get_number_of_feature_models(data_frame: pd.DataFrame):
    return data_frame[data_frame.columns[0]].count()


def get_no_systems_per_domain(data_frame: pd.DataFrame):
    return data_frame.groupby('Domain')['Name'].nunique()


def get_minmax_for_subset(data_frame: pd.DataFrame, column_of_interest, filter_column, filter_value):
    filtered_data_frame = data_frame[data_frame[filter_column] == filter_value]
    return filtered_data_frame[column_of_interest].min(), filtered_data_frame[column_of_interest].max()


def print_meta_data(data_frame):
    print("Number of feature models: " +
          str(get_number_of_feature_models(data_frame)))
    print("Number of unique systems: " + str(get_number_of_systems(data_frame)))
    print("Number of domains: " + str(get_number_of_domains(data_frame)))
    print("Number of unique Publications: " +
          str(get_no_unique_publications(data_frame)))
    print("Number of feature models: \n" +
          get_no_feature_models_per_domain(data_frame))
    print("Number of different systems: \n" +
          get_no_systems_per_domain(data_frame))


# -------------------------- CDL structure --------------------------

def create_cdl_dir(new_path="cdl"):
    cfr_files = get_files_from_directory(
        "feature_models/original/systems_software/eCos-benchmark-clafer", [".cfr"])
    for file_path in cfr_files:
        dir = os.path.join(new_path, get_system_name(file_path))
        os.makedirs(dir)
        shutil.copyfile(file_path, os.path.join(dir, "Passos2011.cfr"))
        value_dict = {
            "Name": get_system_name(file_path),
            "Year": 2011,
            "Hierarchy": True,
            "OriginalFormat": "Clafer",
            "Versions": [],
            "Publication": "https://doi.org/10.1145/2019136.2019139",
            "Source": "https://gsd.uwaterloo.ca/FOSD11",
            "Variants": [],
            "Keywords": [
                "CDL",
                "Automatic"
            ],
            "ConversionTool": ""
        }
        with open(os.path.join(dir, "Passos2011.json"), "w") as outfile:
            json.dump(value_dict, outfile)

    dimacs_files = get_files_from_directory(
        "feature_models/original/systems_software/eCos-benchmark-clafer", [".dimacs"])
    for file_path in dimacs_files:
        dir = os.path.join(new_path, get_system_name(file_path))
        shutil.copyfile(file_path, os.path.join(dir, "Berger2013.dimacs"))
        value_dict = {
            "Name": get_system_name(file_path),
            "Year": 2013,
            "Hierarchy": False,
            "OriginalFormat": "DIMACS",
            "Versions": [],
            "Publication": "https://doi.org/10.1109/TSE.2013.34",
            "Source": "https://gsd.uwaterloo.ca/industrial-variability-modeling",
            "Keywords": [
                "CDL",
                "Automatic"
            ],
            "ConversionTool": ""
        }
        with open(os.path.join(dir, "Berger2013.json"), "w") as outfile:
            json.dump(value_dict, outfile)

    xml_files = get_files_from_directory(
        "../is-there-a-mismatch/Data/LargeFeatureModels/CDL", [".xml"])
    for file_path in xml_files:
        dir = os.path.join(new_path, get_system_name(file_path))
        shutil.copyfile(file_path, os.path.join(dir, "Knüppel2017.xml"))
        value_dict = {
            "Name": get_system_name(file_path),
            "Year": 2017,
            "Hierarchy": True,
            "OriginalFormat": "FeatureIDE",
            "Versions": [],
            "Publication": "https://doi.org/10.1145/3106237.3106252",
            "Source": "https://github.com/AlexanderKnueppel/is-there-a-mismatch",
            "Keywords": [
                "CDL",
                "Automatic"
            ],
            "ConversionTool": ""
        }
        with open(os.path.join(dir, "Knüppel2017.json"), "w") as outfile:
            json.dump(value_dict, outfile)


def extract_pett_linux_history(new_dir="pett_linux"):
    os.makedirs(new_dir)
    input_path = "../data/Feature-Model-History-of-Linux/monthly"
    dimacs_zips = get_files_from_directory(input_path, ["dimacs.zip"])
    for dimacs_zip in dimacs_zips:
        shutil.unpack_archive(dimacs_zip, "temp")
        dimacs_path = get_files_from_directory("temp", ["dimacs"])[0]
        timestamp = dimacs_path.split("/")[-2]
        new_path = os.path.join(new_dir, "Pett2019-" +
                                timestamp + ".dimacs.zip")
        with zipfile.ZipFile(new_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.write(dimacs_path, os.path.basename(dimacs_path))
        shutil.rmtree("temp")


# ---------- DIMACS Analysis ----------

def get_no_features_and_clauses_for_dimacs(dimacs_path):
    with open(dimacs_path, 'r') as dimacs_file:
        info_line = re.search('p cnf [0-9]+ [0-9]+', dimacs_file.read()).group()
        return info_line.split(' ')[2], info_line.split(' ')[3]


def build_dimacs_rows(dimacs_paths):
    header_string = "model;NumberOfFeatures;NumberOfLeafFeatures;NumberOfTopFeatures;#Constraints;AverageConstraintSize;CtcDensity;FeaturesInConstraintsDensity;TreeDepth;AverageNumberOfChildren;NumberOfClauses;NumberOfLiterals;ClauseDensity;RatioOptionalFeatures;ConnectivityDensity;Void;#CORE;#Dead;NumberOfValidConfigurations;SimpleCyclomaticComplexity;IndependentCyclomaticComplexity"
    headers = header_string.split(';')
    model_index = headers.index("model")
    no_features_index = headers.index("NumberOfFeatures")
    no_leaves_index = headers.index("NumberOfLeafFeatures")
    no_tops_index = headers.index("NumberOfTopFeatures")
    no_constraints_index = headers.index("#Constraints")
    treedepth_index = headers.index("TreeDepth")
    no_clauses_index = headers.index("NumberOfClauses")

    result_csv = header_string + "\n"

    for path in dimacs_paths:
        original_path = path
        if path.endswith('zip'):
            shutil.unpack_archive(path, "temp")
            path = get_files_from_directory("temp", ["dimacs"])[0]
        row = ["" for x in range(len(headers))]
        features, clauses = get_no_features_and_clauses_for_dimacs(path)
        row[model_index] = original_path
        row[no_features_index] = str(features)
        row[no_leaves_index] = str(features)
        row[no_tops_index] = str(features)
        row[no_constraints_index] = str(clauses)
        row[treedepth_index] = "1"
        row[no_clauses_index] = str(clauses)

        result_csv += ';'.join(row) + "\n"
    
    print(result_csv)

# build_dimacs_rows(get_files_from_directory("feature_models/original/systems_software/Linux", ["dimacs", "dimacs.zip"]) + get_files_from_directory("feature_models/dimacs/systems_software/Linux", ["dimacs","dimacs.zip"]) + get_files_from_directory("feature_models/original/systems_software/Fiasco", ["dimacs","dimacs.zip"]))
        
print_meta_data(read_csv_to_dataframe("statistics/FullCombined.csv"))
# create_benchmark_json({'Publication Title' : 'Fun Fun', 'Filter' : [ {'Domain': 'Automotive'}, {'#Features' : '100-1000'} ], 'DOI' : 'doi.org/hehe'}, read_csv_to_dataframe("statistics/complete.csv"))

# get_evolution_steps("pett_linux")
# create_cdl_dir()
# extract_pett_linux_history()
