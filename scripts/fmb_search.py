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

list_domain_input = ['domain', 'dom', 'dmoain', 'dmo', ' domain', ' dom', ' dmoain', ' dmo']
list_format_input = ['format', 'formats', 'form', 'for', 'fromat', 'fromats', 'from', 'fro', 
                     ' format', ' formats', ' form', ' for', ' fromat', ' fromats', ' from', ' fro',]
list_features_input = ['features', 'feature', '#features', '#feature', 'number of features', 'feat',
                       'faetures', 'faeture', '#faetures', '#faeture', 'number of faetures', 'faet',
                       ' features', ' ature', ' #features', ' #feature', ' number of features', ' feat',
                       ' faetures', ' faeture', ' #faetures', ' #faeture', ' number of faetures', ' faet',]
list_ctc_input = ['ctc', 'ctcs', 'cross-tree constraints', 'cross tree constraints', 'cct', 'ccts'
                  ' ctc', ' ctcs', ' cross-tree constraints', ' cross tree constraints', ' cct', ' ccts']
allowed_input = list_domain_input + list_format_input + list_features_input + list_ctc_input

print("You can search for the categories domain, format, features, or CTC")
print("First enter one or more categories, press enter, then the search term")
print("Search for multiple categories: For intersection, separate them by comma, for union by semicolon")
isIntersection = False # comma-separated values
isUnion = False        # semicolon-separated values
search_term = input("Enter category: ").lower()
if("," in search_term):
  isIntersection = True
  search_list = search_term.split(",")
elif(";" in search_term):
  isUnion = True
  search_list = search_term.split(";")
else:
  isUnion = True
  search_list = search_term.split(",")

for term in search_list:
    if(term not in allowed_input):
        print("Please enter at least one allowed category. Possible categories are domain, format, features, and ctc")
        search_term = input("Enter category: ").lower()
        if(isIntersection):
          search_list = search_term.split(",")
        elif(isUnion):
          search_list = search_term.split(";")

# to print list only once per category
isAlreadyPrinted = False
for term in search_list:
    if(term in list_domain_input):
        # To get a list of domains currently present in the feature model benchmark
        list_of_domains = []
        for fm in feature_models:
            for key, value in fm.items():
                if(key == "Domain"):
                    list_of_domains.append(value)
        list_of_domains = list(dict.fromkeys(list_of_domains))
        if(not isAlreadyPrinted):
          print(list_of_domains)
        isAlreadyPrinted = True
    elif(term in list_format_input):
        # To get a list of formats currently present in the feature model benchmark
        list_of_formats = []
        for fm in feature_models:
            for key, value in fm.items():
                if(key == "Format"):
                    list_of_formats.append(value)
        list_of_formats = list(dict.fromkeys(list_of_formats))
        if(not isAlreadyPrinted):
          print(list_of_formats)
        isAlreadyPrinted = True

print("Search for multiple categories: For intersection, separate them by comma, for union by semicolon")
value_term = input("Enter value: ")
if(isIntersection):
  value_list = value_term.split(",")
elif(isUnion):
  value_list = value_term.split(";")
else:
  value_list = value_term.split(",")

# search terms become keys from feature model CSV-file
fmb_keys = []
for term in search_list:
  if(term in list_domain_input):
    fmb_keys.append("Domain")
  elif(term in list_format_input):
    fmb_keys.append("Format")
  elif(term in list_features_input):
    fmb_keys.append("#Features")
  elif(term in list_ctc_input):
    fmb_keys.append("#CTC")

# make list of tuples of categories and values user searches for
search_key_values = list(zip(fmb_keys, value_list))

def add_fm_to_list(fm_list, cat, val):
  temp_fm_list = []
  for fm in fm_list:
    if(fm[cat] == val):
      temp_fm_list.append(fm)
  return temp_fm_list

def find_higher(fm_list, cat, val):
  temp_fm_list = []
  act_val = val.replace(">", "")
  act_val = int(act_val)
  for fm in fm_list:
    if(fm[cat]):
      fm_value = int(fm[cat])
      if(act_val < fm_value):
        temp_fm_list.append(fm)
  return temp_fm_list

def find_lower(fm_list, cat, val):
  temp_fm_list = []
  act_val = val.replace("<", "")
  act_val = int(act_val)
  for fm in fm_list:
    if(fm[cat]):
      fm_value = int(fm[cat])
      if(act_val > fm_value):
        temp_fm_list.append(fm)
  return temp_fm_list

def find_range(fm_list, cat, val):
  temp_fm_list = []
  values = val.replace("to", " ").replace("t", " ").replace("-", " ").split()
  values = [int(val) for val in values]
  lower_bound = min(values)
  upper_bound = max(values)
  for fm in fm_list:
    if(fm[cat]):
      fm_value = int(fm[cat])
      if(lower_bound <= fm_value <= upper_bound):
        temp_fm_list.append(fm)
  return temp_fm_list

# checks if search keys are subset of an FM in our list of FMs
fm_selection = []
if(isIntersection):
  for cat,val in search_key_values:
    temp_selection = []
    if(cat == "Domain"):
      temp_selection = add_fm_to_list(feature_models, cat, val)
      if(fm_selection):
        fm_selection = [fm for fm in fm_selection if fm in temp_selection]
      else: 
        fm_selection = temp_selection
    elif (cat == "Format"):
      temp_selection = add_fm_to_list(feature_models, cat, val)
      if(fm_selection):
        fm_selection = [fm for fm in fm_selection if fm in temp_selection]
      else:
        fm_selection = temp_selection
    elif(cat == "#Features"):
      if(">" in val):
        temp_selection = find_higher(feature_models, cat, val)
      elif("<" in val):
        temp_selection = find_lower(feature_models, cat, val)
      elif(("to" in val) or ("t" in val) or ("-" in val)):
        temp_selection = find_range(feature_models, cat, val)
      else:
        temp_selection = add_fm_to_list(feature_models, cat, val)
      if(fm_selection):
        fm_selection = [fm for fm in fm_selection if fm in temp_selection]
      else:
        fm_selection = temp_selection
    elif(cat == "#CTC"):
      if(">" in val):
        temp_selection = find_higher(feature_models, cat, val)
      elif("<" in val):
        temp_selection = find_lower(feature_models, cat, val)
      elif(("to" in val) or ("t" in val) or ("-" in val)):
        temp_selection = find_range(feature_models, cat, val)
      else:
        temp_selection = add_fm_to_list(feature_models, cat, val)
      if(fm_selection):
        fm_selection = [fm for fm in fm_selection if fm in temp_selection]
      else:
        fm_selection = temp_selection
elif(isUnion):
  pre_fm_selection = []
  for cat,val in search_key_values:
    temp_selection = []
    if(cat == "Domain"):
      temp_selection = add_fm_to_list(feature_models, cat, val)
      pre_fm_selection = pre_fm_selection + temp_selection
    elif (cat == "Format"):
      temp_selection = add_fm_to_list(feature_models, cat, val)
      pre_fm_selection = pre_fm_selection + temp_selection
    elif(cat == "#Features"):
      if(">" in val):
        temp_selection = find_higher(feature_models, cat, val)
      elif("<" in val):
        temp_selection = find_lower(feature_models, cat, val)
      elif(("to" in val) or ("t" in val) or ("-" in val)):
        temp_selection = find_range(feature_models, cat, val)
      else:
        temp_selection = add_fm_to_list(feature_models, cat, val)
      pre_fm_selection = pre_fm_selection + temp_selection
    elif(cat == "#CTC"):
      if(">" in val):
        temp_selection = find_higher(feature_models, cat, val)
      elif("<" in val):
        temp_selection = find_lower(feature_models, cat, val)
      elif(("to" in val) or ("t" in val) or ("-" in val)):
        temp_selection = find_range(feature_models, cat, val)
      else:
        temp_selection = add_fm_to_list(feature_models, cat, val)
      pre_fm_selection = pre_fm_selection + temp_selection
  # remove duplicates
  for fm in pre_fm_selection:
    if(fm not in fm_selection):
      fm_selection.append(fm)

for fm in fm_selection:
  print(fm)