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

# Requesting meta information
list_help_input = ['show help', 'show h', 'help']
list_domains_info_input = ['show domains', 'show domain', 'show dom']
list_formats_info_input = ['show formats', 'show format', 'show form', 'show for']
list_exit_input = ['exit', 'quit']
list_meta_input = list_help_input + list_domains_info_input + list_formats_info_input + list_exit_input
# Category searcg input
list_domain_input = ['domain', 'dom', 'dmoain', 'dmo', ' domain', ' dom', ' dmoain', ' dmo']
list_format_input = ['format', 'formats', 'form', 'for', 'fromat', 'fromats', 'from', 'fro', 
                     ' format', ' formats', ' form', ' for', ' fromat', ' fromats', ' from', ' fro',]
list_features_input = ['features', 'feature', '#features', '#feature', 'number of features', 'feat',
                       'faetures', 'faeture', '#faetures', '#faeture', 'number of faetures', 'faet',
                       ' features', ' ature', ' #features', ' #feature', ' number of features', ' feat',
                       ' faetures', ' faeture', ' #faetures', ' #faeture', ' number of faetures', ' faet',]
list_ctc_input = ['ctc', 'ctcs', 'cross-tree constraints', 'cross tree constraints', 'cct', 'ccts'
                  ' ctc', ' ctcs', ' cross-tree constraints', ' cross tree constraints', ' cct', ' ccts']
list_category_input = list_domain_input + list_format_input + list_features_input + list_ctc_input
allowed_input = list_meta_input + list_category_input

help_text = '''
Searchable categories: domain, format, features, CTC
Search procedure:
  1) Enter one or more categories
  2) Press Enter
  3) Enter one search term per category
  4) Press Enter
Multiple categories:
  1) Intersection: Separate categories and search terms by comma
  2) Union: Separate categories and search terms by semicolon
Search commands:
  1) Greater than: >
  2) Less than:    <
  3) Range:        -, to
Feature Model information:
  1) Give available domains: show domains
  2) Give available formats: show formats
Examples:
  1) FMs of domain systems software AND format DIMACS
     domain,format
     systems software,DIMACS
  2) FMs of domain systems software OR format DIMACS
     domain;format
     systems software;DIMACS
  3) FMs with more than 500 features
     features
     >500
  4) FMs with less than 500 features
     features
     <500
  5) FMs with 500 to 800 cross-tree constraints
     CTC
     500to800
'''

def give_meta_info(user_input):
  """Provide meta information to user.

  Prints either the help text, available domains, available formats or a goodby message,
  depending on what the user requests.

  Keyword argument:
  user_input -- Console input from user 
  """
  if(user_input in list_help_input):
    print(help_text)
  elif(user_input in list_domains_info_input):
    # To get a list of domains currently present in the feature model benchmark
    list_of_domains = []
    for fm in feature_models:
      for key, value in fm.items():
        if(key == "Domain"):
          list_of_domains.append(value)
    list_of_domains = list(dict.fromkeys(list_of_domains))
    print(list_of_domains)
  elif(user_input in list_formats_info_input):
    # To get a list of formats currently present in the feature model benchmark
    list_of_formats = []
    for fm in feature_models:
      for key, value in fm.items():
        if(key == "Format"):
          list_of_formats.append(value)
    list_of_formats = list(dict.fromkeys(list_of_formats))
    print(list_of_formats)
  elif(user_input in list_exit_input):
    print("Goodbye!")

def add_fm_to_list(fm_list, cat, val):
  """Add feature model to list and return list.

  If a feature model from the provided list of feature models
  contains the value for the given category key,
  the feature model is added to a list that's returned.

  Keyword argument:
  fm_list -- list of feature models
  cat     -- category (key) 
  val     -- value to key 
  """
  temp_fm_list = []
  for fm in fm_list:
    if(fm[cat] == val):
      temp_fm_list.append(fm)
  return temp_fm_list

def find_higher(fm_list, cat, val):
  """Find feature models with higher numerical values.

  If a feature model from the provided list of feature models
  contains a value for the given category key that's higher than the provided value,
  the feature model is added to a list that's returned.

  Keyword argument:
  fm_list -- list of feature models
  cat     -- category (key) 
  val     -- value to key 
  """
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
  """Find feature models with lower numerical values.

  If a feature model from the provided list of feature models
  contains a value for the given category key that's lower than the provided value,
  the feature model is added to a list that's returned.

  Keyword argument:
  fm_list -- list of feature models
  cat     -- category (key) 
  val     -- value to key 
  """
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
  """Find feature models with numerical values between a given range.

  If a feature model from the provided list of feature models
  contains a value for the given category key that's in the range of the provided values,
  the feature model is added to a list that's returned.
  The values are provided in String format and are converted to two numbers first.

  Keyword argument:
  fm_list -- list of feature models
  cat     -- category (key) 
  val     -- value to key, in String format 
  """
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

print('For help, enter "help", to quit enter "quit" or "exit"')
isSearchRunning = True  # user has not received feature models yet
isCategoryGiven = False # user has to give category before value
isValueGiven = False    # user has to give category and value to complete search
category_list = []
value_list = []
while(isSearchRunning):
  isIntersection = False  # comma-separated values
  isUnion = False         # semicolon-separated values
  search_list = []
  search_term = input("Enter: ")
  if(search_term in list_exit_input):
    break
  elif(search_term in list_meta_input):
    give_meta_info(search_term)
  else:
    if("," in search_term):
      isIntersection = True
      search_list = search_term.split(",")
    elif(";" in search_term):
      isUnion = True
      search_list = search_term.split(";")
    else:
      isUnion = True
      search_list = search_term.split(",")

  if(search_list):
    isNotCategories = True # current user input provides values, not categories
    for term in search_list:
        if(term.lower() in list_category_input):
            isCategoryGiven = True
            isNotCategories = False
            category_list = search_list
    if(isNotCategories):
      isValueGiven = True
      value_list = search_list

  if(isCategoryGiven and isValueGiven):
    # search terms become keys from feature model CSV-file
    fmb_keys = []
    for term in category_list:
      if(term.lower() in list_domain_input):
        fmb_keys.append("Domain")
      elif(term.lower() in list_format_input):
        fmb_keys.append("Format")
      elif(term.lower() in list_features_input):
        fmb_keys.append("#Features")
      elif(term.lower() in list_ctc_input):
        fmb_keys.append("#CTC")

    # make list of tuples of categories and values user searches for
    search_key_values = list(zip(fmb_keys, value_list))

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

    isSearchRunning = False