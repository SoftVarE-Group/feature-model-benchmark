import pandas as pd
from utils import *
import argparse
import sys

USER_COLUMNS = ["Publication", "Keywords",
                "Source", "ConvertedFrom", "Conversion_Tool"]
SUPPORTED_SUFFIXES = ["uvl", "xml", "dimacs", "afm", "zip", "cfr", "fm"]
JSON_SUFFIX_ARRAY = ["json"]

# Args handling


def init_args():
    parser = argparse.ArgumentParser(
        description='Derive feature-model subset according to filtering')
    parser.add_argument('--createfull', type=str,
                        help="Create csv containing information on origin of every feature model in feature_models/original and save it in value")
    parser.add_argument('--createaggregate', type=str,
                        help="Create csv containing information on origin for every system (i.e., with variants of the same feature models being aggregated) in feature_models/original")
    parser.add_argument('--originfile', type=str, required= '--mergeanalysis' in sys.argv, help="Path to statistics csv containing information on the origin")
    parser.add_argument('--analysisfile', type=str, required= '--mergeanalysis' in sys.argv, help="Path to statistics csv containing results of analysis")
    parser.add_argument('--mergeanalysis', type=str, help="Create merged statistics csv from an origin and analysis csv")
    parser.add_argument('--printmeta', type=str, help="Prints some meta information about the current collection based on specified csv")

    return parser.parse_args()


def load_feature_models(directory_path, output_path="statistics/models_new.csv"):
    model_paths = get_files_from_directory(directory_path, JSON_SUFFIX_ARRAY)
    data_frame = data_frame_from_json_list(model_paths)
    data_frame.to_csv(output_path, ";", index=False)


def load_feature_models_complete(directory_path, output_path="statistics/complete_new.csv"):
    model_paths = get_files_from_directory(directory_path, SUPPORTED_SUFFIXES)
    data_frame = data_frame_from_models_list(model_paths)
    data_frame.to_csv(output_path, ";", index=False)


def data_frame_from_models_list(model_paths):
    domains = [get_domain_from_relative_path(model) for model in model_paths]
    model_names = [get_system_name(model) for model in model_paths]
    model_origins = [get_origin(model) for model in model_paths]
    model_versions = [get_version(model) for model in model_paths]
    model_extensions = [get_extension(model) for model in model_paths]

    model_jsons = [get_json_for_model(path) for path in model_paths]

    formats = [get_file_format(model) for model in model_jsons]
    years = [get_year(model) for model in model_jsons]
    hasHierarchyFlags = [get_hierarchy(model) for model in model_jsons]
    sources = [get_source(model) for model in model_jsons]
    publications = [get_publication(model) for model in model_jsons]
    partOfHistory = [get_no_versions(model) > 1 for model in model_jsons]
    model_keywords = [get_keywords(model) for model in model_jsons]

    data_frame = pd.DataFrame({'Name': model_names, 'Origin': model_origins, 'PartOfHistory': partOfHistory, 'Version': model_versions, 'Domain': domains,
                              'Format': formats, 'Extension': model_extensions, 'Year': years, "Keywords": model_keywords, 'Hierarchy': hasHierarchyFlags, 'Source': sources, 'Publication': publications, 'Path': model_paths})
    data_frame = data_frame.sort_values(
        ["Domain", "Name", "Origin", "Version"])
    return data_frame


def data_frame_from_json_list(model_paths):
    domains = [get_domain_from_relative_path(model) for model in model_paths]
    model_names = [get_system_name(model) for model in model_paths]
    model_origins = [get_origin(model) for model in model_paths]
    model_jsons = [get_model_json(model) for model in model_paths]
    model_extensions = [get_extension(model) for model in model_paths]

    # Json data
    formats = [get_file_format(model) for model in model_jsons]
    years = [get_year(model) for model in model_jsons]
    hasHierarchyFlags = [get_hierarchy(model) for model in model_jsons]
    sources = [get_source(model) for model in model_jsons]
    publications = [get_publication(model) for model in model_jsons]
    no_versions = [get_no_versions(model) for model in model_jsons]
    version_ranges = [get_version_range(model) for model in model_jsons]
    no_variants = [get_no_variants(model) for model in model_jsons]
    model_keywords = [get_keywords(model) for model in model_jsons]

    data_frame = pd.DataFrame({'Name': model_names, 'Origin': model_origins, 'Domain': domains, 'Format': formats, 'Extension': model_extensions, 'Year': years, "Keywords": model_keywords, 'Hierarchy': hasHierarchyFlags,
                              'Versions': no_versions, 'VersionRange': version_ranges, 'Variants': no_variants, 'Source': sources, 'Publication': publications, 'Path': model_paths})
    data_frame = data_frame.sort_values(["Domain", "Name"])
    return data_frame


def append_analysis_results(origin_file, analysis_file, output_path="statistics/complete.csv"):
    models_data_frame = read_csv_to_dataframe(origin_file)
    analysis_data_frame = read_csv_to_dataframe(analysis_file)
    models_data_frame['DescribingPath'] = models_data_frame.apply(
        lambda row: get_describing_path(row.Path), axis=1)
    analysis_data_frame['DescribingPath'] = analysis_data_frame.apply(
        lambda row: get_describing_path(row.model), axis=1)

    complete_data_frame = pd.merge(
        models_data_frame, analysis_data_frame, on="DescribingPath", how="left")
    comeplete_data_frame = complete_data_frame.drop(columns='model')
    comeplete_data_frame = comeplete_data_frame.sort_values(["Domain", "Name"])

    comeplete_data_frame.to_csv(output_path, ";", index=False)

def get_number_of_evolutions(df):
    df['id'] = df['Name'] + df['Origin']
    evo_df = df[df['PartOfHistory'] == True].reset_index(drop=True)
    return evo_df['id'].nunique()

def print_meta(complete_file):
    df = read_csv_to_dataframe(complete_file)
    print(f'Number of feature models: {len(df.index)}')
    print(f'Number of systems: {df["Name"].nunique()}')
    print(f'Number of histories: {get_number_of_evolutions(df)}')
    print(f'Models per domain:\n{df["Domain"].value_counts()}')



args = init_args()
if args.createfull:
    load_feature_models_complete("feature_models/original", args.createfull)
elif args.createaggregate:
    load_feature_models("feature_models/original", args.createaggregate)
elif args.mergeanalysis:
    append_analysis_results(args.originfile, args.analysisfile, args.mergeanalysis)
elif args.printmeta:
    print_meta(args.printmeta)

