import csv
import os

'''
Always same directory structure and file names:
  In some directory, e. g. let's call it "x", two subfolders are present
    x/scripts/fmb_search.py
    x/statistics/fmb.csv
'''
path_from_here = os.path.join(os.path.dirname(__file__), '..', 'statistics', 'fmb.csv')
path_to_csv = os.path.realpath(path_from_here)

# Storing dictionaries containing feature model data
feature_models = []

'''
The following steps happen:
  1) Open fmb.csv
  2) turn rows into dictionaries (the very first line of fmb.csv contains the keys)
  3) append each dictionary to feature_models list
''' 
with open(path_to_csv, newline='') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        feature_models.append(row)

list_domain_input = ['domain', 'dom']
list_format_input = ['format', 'formats']
list_features_input = ['features', 'feature', '#features', '#feature', 'number of features']
list_ctc_input = ['ctc', 'ctcs', 'cross-tree constraints', 'cross tree constraints']
allowed_input = list_domain_input + list_format_input + list_features_input + list_ctc_input

print("You can search for the categories domain, format, features, or CTC")
print("First enter the category, press enter, then the search term")
search_term = input("Enter category: ").lower()

if (search_term not in allowed_input):
  print("Please enter an allowed category. Possible categories are domain, format, features, and ctc")
  search_term = input("Enter category: ").lower()

if (search_term in list_domain_input):
    # To get a list of domains currently present in the feature model benchmark
    list_of_domains = []
    for fm in feature_models:
        for key, value in fm.items():
            if (key == "Domain"):
                list_of_domains.append(value)
    list_of_domains = list(dict.fromkeys(list_of_domains))
    print(list_of_domains)

if (search_term in list_format_input):
    # To get a list of formats currently present in the feature model benchmark
    list_of_formats = []
    for fm in feature_models:
        for key, value in fm.items():
            if (key == "Format"):
                list_of_formats.append(value)
    list_of_formats = list(dict.fromkeys(list_of_formats))
    print(list_of_formats)

value_term = input("Enter value: ")

fmb_key = ""
if (search_term in list_domain_input):
  fmb_key = "Domain"
if (search_term in list_format_input):
  fmb_key = "Format"
if (search_term in list_features_input):
  fmb_key = "#Features"
if (search_term in list_ctc_input):
  fmb_key = "#CTC"

for fm in feature_models:
  if (fm[fmb_key] == value_term):
    print(fm)