import pandas as pd
from utils import *

USER_COLUMNS = ["Publication", "Keywords",
                "Source", "ConvertedFrom", "Conversion_Tool"]
SUPPORTED_SUFFIXES = ["uvl", "xml", "dimacs", "afm", "zip", "cfr", "fm"]
JSON_SUFFIX_ARRAY = ["json"]





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

    data_frame = pd.DataFrame({'Name': model_names, 'Origin': model_origins, 'PartOfHistory' : partOfHistory, 'Version': model_versions, 'Domain': domains,
                              'Format': formats, 'Extension' : model_extensions, 'Year': years, 'Hierarchy': hasHierarchyFlags, 'Source': sources, 'Publication': publications, 'Path' : model_paths})
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

    data_frame = pd.DataFrame({'Name': model_names, 'Origin': model_origins, 'Domain': domains, 'Format': formats, 'Extension' : model_extensions, 'Year': years, 'Hierarchy': hasHierarchyFlags,
                              'Versions': no_versions, 'VersionRange': version_ranges, 'Variants': no_variants, 'Source': sources, 'Publication': publications, 'Path' : model_paths})
    data_frame = data_frame.sort_values(["Domain", "Name"])
    return data_frame


def append_analysis_results(models_data_frame, analysis_data_frame, output_path="statistics/complete.csv"):
    models_data_frame = models_data_frame.sort_values(
        ["Name"]).reset_index(drop=True)
    print(models_data_frame)
    analysis_data_frame = analysis_data_frame.sort_values(
        ["Name"]).reset_index(drop=True)
    print(analysis_data_frame)
    analysis_data_frame = analysis_data_frame.drop(columns='Name')
    combined_data_frame = pd.concat(
        [models_data_frame, analysis_data_frame], axis=1)
    combined_data_frame = combined_data_frame.sort_values(["Domain", "Name"])

    combined_data_frame.to_csv(output_path, ";", index=False)


# -------------------------- Update Table --------------------------


def add_new_feature_models(directory_path, old_csv_path):
    existing_data_frame = read_csv_to_dataframe(old_csv_path)

    model_paths = get_files_from_directory(directory_path, SUPPORTED_SUFFIXES)
    new_model_paths = [
        model_path for model_path in model_paths if not get_system_name(model_path) in existing_data_frame['Name'].values]
    new_data_frame = data_frame_from_json_list(new_model_paths)
    combined_data_frame = pd.concat([existing_data_frame, new_data_frame])
    combined_data_frame = combined_data_frame.sort_values(["Domain", "Name"])
    combined_data_frame.to_csv(old_csv_path, ";", index=False)


# -------------------------- Filter Table --------------------------

def get_data_frame_subset(data_frame, filter_column=None, row_values_to_keep=[], columns_to_keep=None):
    filtered_df = data_frame
    if not columns_to_keep is None:
        filtered_df = data_frame[columns_to_keep]
    if not filter_column is None:
        filtered_df = filtered_df[filtered_df[filter_column].isin(
            row_values_to_keep)]

    return filtered_df


# load_feature_models("feature_models/original", "statistics/models_temp.csv")
load_feature_models_complete("feature_models/original")
# add_new_feature_models("feature_models", "statistics/complete.csv")
# get_data_frame_subset(read_csv_to_dataframe("statistics/complete.csv"), filter_column="Name", row_values_to_keep=["Automotive1", "ERP-System"],columns_to_keep=["Name", "Domain"])
