import csv
import os
import shutil
import time

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
list_exit_input = ['exit', 'quit', 'q']
list_get_fms_input = ['create benchmark', 'create bench', 'create b', 'benchmark', 'bench', 'fmb']
list_meta_input = list_help_input + list_domains_info_input + list_formats_info_input + list_exit_input + list_get_fms_input
# Category searcg input
list_domain_input = ['domain', 'dom', 'dmoain', 'dmo']
list_format_input = ['format', 'formats', 'form', 'for', 'fromat', 'fromats', 'from', 'fro']
list_features_input = ['features', 'feature', '#features', '#feature', 'number of features', 'feat',
                       'faetures', 'faeture', '#faetures', '#faeture', 'number of faetures', 'faet']
list_ctc_input = ['ctc', 'ctcs', 'cross-tree constraints', 'cross tree constraints', 'cct', 'ccts']
list_category_input = list_domain_input + list_format_input + list_features_input + list_ctc_input
allowed_input = list_meta_input + list_category_input

list_separators_AND = [',', '&']
list_separators_OR = [';', '|']

help_text = '''
Searchable categories: domain, format, features, CTC
Save found feature models in subdirectory of "benchmarks": fmb
Search procedure:
  1) Enter one or more categories
  2) Press Enter
  3) Enter one search term per category
  4) Press Enter
Multiple categories:
  1) Intersection: Separate categories and search terms either by comma "," or ampersand "&"
  2) Union: Separate categories and search terms either by semicolon ";" or pipe "|"
Search commands:
  1) Greater than: >
  2) Less than:    <
  3) Range:        -, to
Feature Model information:
  1) Give available domains: show domains
  2) Give available formats: show formats
Examples:
  1) FMs of domain systems software AND format DIMACS
     Solution 1.1:
      domain,format
      systems software,DIMACS
     Solution 1.2:
      domain&format
      systems software&DIMACS
  2) FMs of domain systems software OR format DIMACS
     Solution 2.1:
      domain;format
      systems software;DIMACS
     Solution 2.2:
      domain|format
      systems software|DIMACS
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

def create_benchmark(fm_list):
  """Create FM benchmark from FMs found through search.

  Creates new benchmark directory if none exists.
  Then goes through list of found FMs and looks for the respective FMs in feature_models directory,
  copying them to the benchmark directory.

  Keyword argument:
  fm_list -- List of FMs (dictionaries) found by user
  """
  fmb_directory = os.path.join(os.path.dirname(__file__), '..', 'benchmarks')
  fm_directory = os.path.join(os.path.dirname(__file__), '..', 'feature_models')
  # feature-model benchmark-directory may not yet exist
  if (not os.path.isdir(fmb_directory)):
    os.makedirs(fmb_directory)

  # create a new subdirectory in benchmarks for every benchmark
  fmb_sub_name = "fmb" + str(time.time())
  fmb_sub_directory = os.path.join(fmb_directory, fmb_sub_name)
  os.makedirs(fmb_sub_directory)

  # go through list of dictionaries (i.e. FMs found by user)
  for fm in fm_list:
    fm_name = fm['Name']
    for root, dirs, files in os.walk(fm_directory):
      # FM file names need to be unique
      for fm_file in files:
        # filename is "name.extension" and we want to get the "name" only
        if(fm_name == fm_file.split('.')[0]):
          fm_file_path = os.path.join(root, fm_file)
          shutil.copy2(fm_file_path, fmb_sub_directory)
      # in cases like eCos-benchmark-clafer, the FM name is the name of the directory, not of single FMs
      for fm_dir in dirs:
        # in case of eCos-benchmark-clafer, the FM name is eCos-benchmark-clafer (116 feature models)
        fm_part_name = fm_name.split(" ")[0]
        if(fm_part_name == fm_dir):
          fm_files_path = os.path.join(root, fm_dir)
          fm_files = os.listdir(fm_files_path)
          # copy all files in directory to feature-model benchmark
          for fm_file in fm_files:
            fm_file_path = os.path.join(fm_files_path, fm_file)
            shutil.copy2(fm_file_path, fmb_sub_directory)

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
    list_of_domains = get_category_sublist("Domain")
    print(list_of_domains)
  elif(user_input in list_formats_info_input):
    # To get a list of formats currently present in the feature model benchmark
    list_of_formats = get_category_sublist("Format")
    print(list_of_formats)
  elif(user_input in list_get_fms_input):
    global isBenchmarkWanted
    isBenchmarkWanted = True
    print('FM Benchmark will be created in a subdirectory of "benchmarks"')
  elif(user_input in list_exit_input):
    print("Goodbye!")

def get_category_sublist(cat):
    """Creates a list of values for the given category (currently for categories domain, format)

    Keyword argument:
    cat -- String (category name, currently either "Domain" or "Format) 
    """
    category_sublist = []
    for fm in feature_models:
      for key, value in fm.items():
        if(key == cat):
          category_sublist.append(value)
    category_sublist = list(dict.fromkeys(category_sublist))
    return category_sublist

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
  # turns numbers separated by "to", "t" or "-" into list of numbers
  values = val.replace("to", " ").replace("t", " ").replace("-", " ").split()
  # cover cases with invalid input as range, i.e. not two numbers separated by "to", "t" or "-""
  if(all(val.isnumeric() for val in values)):
    values = [int(val) for val in values]
    lower_bound = min(values)
    upper_bound = max(values)
    for fm in fm_list:
      if(fm[cat]):
        fm_value = int(fm[cat])
        if(lower_bound <= fm_value <= upper_bound):
          temp_fm_list.append(fm)
    return temp_fm_list

def split_with_separators(str_to_split, list_of_separators):
  """List as input for str.split()

  Keyword argument:
  str_to_split        -- String (user input specifying what FM search)
  list_of_separators  -- list of separators 
  """
  str_to_list = []
  for sep in list_of_separators:
    if(sep in str_to_split):
      str_to_list = str_to_split.split(sep)
  return str_to_list

print('For help, enter "help", to quit enter "quit" or "exit"')
isSearchRunning = True    # user has not received feature models yet
isCategoryGiven = False   # user has to give category before value
isValueGiven = False      # user has to give category and value to complete search
isBenchmarkWanted = False # user wants the FMs from the found FM benchmark
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
    if(any(x in list_separators_AND for x in search_term)):
      isIntersection = True
      search_list = split_with_separators(search_term, list_separators_AND)
    elif(any(x in list_separators_OR for x in search_term)):
      isUnion = True
      search_list = split_with_separators(search_term, list_separators_OR)
    else:
      isUnion = True
      search_list = search_term.split(",")

  # remove leading and trailing whitespaces of categories or values
  if(search_list):
    for index, item in enumerate(search_list):
      item = item.strip()
      search_list[index] = item

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
    else:
      if(any(x in list_domain_input for x in category_list)):
        list_of_domains = get_category_sublist("Domain")
        print("List of domains: ", list_of_domains)
      if(any(x in list_format_input for x in category_list)):
        list_of_formats = get_category_sublist("Format")
        print("List of formats: ", list_of_formats)

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

    if(fm_selection):
      for fm in fm_selection:
        print(fm)

    if(isBenchmarkWanted):
      create_benchmark(fm_selection)

    isSearchRunning = False