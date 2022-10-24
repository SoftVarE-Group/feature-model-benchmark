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
print("If you search for multiple categories, separate them by a comma")
search_term = input("Enter category: ").lower()
search_list = search_term.split(",")

for term in search_list:
    if (term not in allowed_input):
        print("Please enter at least one allowed category. Possible categories are domain, format, features, and ctc")
        search_term = input("Enter category: ").lower()
        search_list = search_term.split(",")

for term in search_list:
    if (term in list_domain_input):
        # To get a list of domains currently present in the feature model benchmark
        list_of_domains = []
        for fm in feature_models:
            for key, value in fm.items():
                if (key == "Domain"):
                    list_of_domains.append(value)
        list_of_domains = list(dict.fromkeys(list_of_domains))
        print(list_of_domains)
    elif(term in list_format_input):
        # To get a list of formats currently present in the feature model benchmark
        list_of_formats = []
        for fm in feature_models:
            for key, value in fm.items():
                if (key == "Format"):
                    list_of_formats.append(value)
        list_of_formats = list(dict.fromkeys(list_of_formats))
        print(list_of_formats)

print("If you search for multiple categories, separate the values by a comma")
value_term = input("Enter value: ")
value_list = value_term.split(",")

# search terms become keys from feature model CSV-file
fmb_keys = []
for term in search_list:
  if (term in list_domain_input):
    fmb_keys.append("Domain")
  elif (term in list_format_input):
    fmb_keys.append("Format")
  elif (term in list_features_input):
    fmb_keys.append("#Features")
  elif (term in list_ctc_input):
    fmb_keys.append("#CTC")

# make dictionary of categories and values user searches for
search_key_values = dict(zip(fmb_keys, value_list))

# user is looking for FMs with number of features or CTCs higher or lower than given value
looking_for_higher_lower = False
for key,value in search_key_values.items():
  if (((key == "#Features") or (key == "#CTC")) and (">" in value) or ("<" in value)):
    looking_for_higher_lower = True

list_of_pre_fms = []
list_of_post_fms = []

# checks if search keys are subset of an FM in our list of FMs
if (not looking_for_higher_lower):
  for fm in feature_models:
      if search_key_values.items() <= fm.items():
        print(fm)
else:
  for fm in feature_models:
    for key,value in search_key_values.items():
      if(((key == "Domain") or (key == "Format")) and (fm[key] == value)):
        list_of_pre_fms.append(fm)
  if (list_of_pre_fms):
    for pre_fm in list_of_pre_fms:
      for key,value in search_key_values.items():
        if((key == "#Features") or (key == "#CTC")):
          if (">" in value):
            act_value = value.replace(">", "")
            act_value = int(act_value)
            fm_value = int(pre_fm[key])
            if (act_value < fm_value):
              list_of_post_fms.append(pre_fm)
          elif ("<" in value):
            act_value = value.replace("<", "")
            act_value = int(act_value)
            fm_value = int(pre_fm[key])
            if (act_value > fm_value):
              list_of_post_fms.append(pre_fm)
          else:
            if (value == pre_fm[key]):
              list_of_post_fms.append(pre_fm)
  else:
    for fm in feature_models:
      for key,value in search_key_values.items():
        if((key == "#Features") or (key == "#CTC")):
          if (">" in value):
            act_value = value.replace(">", "")
            act_value = int(act_value)
            fm_value = int(fm[key])
            if (act_value < fm_value):
              list_of_post_fms.append(fm)
          elif ("<" in value):
            act_value = value.replace("<", "")
            act_value = int(act_value)
            fm_value = int(fm[key])
            if (act_value > fm_value):
              list_of_post_fms.append(fm)
          else:
            if (value == fm[key]):
              list_of_post_fms.append(fm) 
  for post_fm in list_of_post_fms:
    print(post_fm)