import csv
import os
import shutil
import time
import ast
import statistics

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

# Requesting meta information or data
list_help_input = ['show help', 'show h', 'help']
list_domains_info_input = ['show domains', 'show domain', 'show dom']
list_formats_info_input = ['show formats', 'show format', 'show form', 'show for']
list_features_info_input = ['show features', 'show feat', 'show faetures', 'show faet']
list_ctc_info_input = ['show ctc', 'show ctcs', 'show cct', 'show ccts']
list_numbers_stats = list_features_info_input + list_ctc_info_input
list_meta_info_input = list_help_input + list_domains_info_input + list_formats_info_input + list_numbers_stats 
list_get_fms_input = ['create benchmark', 'create bench', 'create b', 'benchmark', 'bench', 'fmb']
list_get_log_input = ['log', 'config', 'conf', 'create log', 'create config', 'create conf', 'create c']
list_get_data_input = list_get_fms_input + list_get_log_input
list_exit_input = ['exit', 'quit', 'x', 'q']
list_meta_input = list_meta_info_input + list_get_data_input + list_exit_input
# Category search input
list_domain_input = ['domain', 'dom', 'dmoain', 'dmo']
list_format_input = ['format', 'formats', 'form', 'for', 'fromat', 'fromats', 'from', 'fro']
list_features_input = ['features', 'feature', '#features', '#feature', 'number of features', 'feat',
                       'faetures', 'faeture', '#faetures', '#faeture', 'number of faetures', 'faet']
list_ctc_input = ['ctc', 'ctcs', 'cross-tree constraints', 'cross tree constraints', 'cct', 'ccts']
list_category_input = list_domain_input + list_format_input + list_features_input + list_ctc_input
# User wants all available FMs input
list_give_all_input = ['', 'all']
# User wants to create benchmark from existing config-file (name to be entered after command)
list_read_conf_input = ['read config', 'read conf', 'r config', 'r conf', 'rc']
allowed_input = list_meta_input + list_category_input + list_give_all_input + list_read_conf_input

list_separators_AND = [',', '&']
list_separators_OR = [';', '|']

list_range_operators = ['to', 't', '-', '..']

help_text = '''
Searchable categories: domain, format, features, CTC
Save found feature models in subdirectory of "benchmarks": fmb
Get all available feature models: Nothing (just press "Enter"), all
  (to save them in a new subdirectory of "benchmarks", enter "fmb" first, then press Enter in the next dialogue)
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
  3) Range:        -, to, ..
  4) NOT:          - (first char of value, in contrast to "Range")
Feature Model information:
  1) Give available domains:    show domains
  2) Give available formats:    show formats
  3) Statistics about features: show features
  4) Statistics about CTCs:     show ctc
Create config txt-file of FMs used for experiments in directory "configs":
  - without additional information: log
  - with additional information:    log(name;analysis;ARE;publication)
  - not all information has to be provided but 3 semicolons are necessary
Create FMB and config txt-file:
  - Creates new subdirectory in configs with
    - config txt-file
    - subdirectory: FMB with FM files
  - Command: fmb+log
  - Command has to start with "fmb" followed by "+" and then a command to create configs
    Possible are config-commands with and without additional information
    e.g.; both "fmb+log" or "fmb+log(name;analysis;ARE;publication)
Create FMB from config txt-file:
  - Command: rc config.txt (extension is optional, filename is enough)
  - Config-file needs to be txt-file in configs-directory
  - FMs have to be String-representations of dictionaries, starting with "{'"
    no other entry than FMs should start with "{'" (open curly brace followed by single quotation mark)
  - Benchmark is created in benchmarks-directory
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
  6) FMs of domain automotive but not in format XML
     domain,format
     automotive,-XML
  7) FMs of domain business or not with less than 70000 features
     domain;features
     business;-<70000
'''

def create_benchmark(fm_list, fmb_dir_path = ""):
  """Create FM benchmark from FMs found through search.

  Creates new benchmark directory if none exists.
  Then goes through list of found FMs and looks for the respective FMs in feature_models directory,
  copying them to the benchmark directory.

  Keyword argument:
  fm_list      -- List of FMs (dictionaries) found by user
  fmb_dir_path -- optional os.path in case directory is to be created somewhere else than "benchmarks"
  """
  fmb_directory = ""
  if(not fmb_dir_path):
    fmb_directory = os.path.join(os.path.dirname(__file__), '..', 'benchmarks')
  else:
    fmb_directory = fmb_dir_path
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

def create_config(search_term, fm_list):
  """Create FM config from FMs found through search and experiment parameters if provided.

  Creates new configs directory if none exists.
  Additional information user wants to store in the config-file is 
    - provided in parentheses right after the command (e.g., "log(...)")
    - in the following 4 categories: 
      - name of benchmark
      - type of analysis
      - automated reasoning engine used
      - accompanying publication
    - categories are separated by semicolon (e.g., "log(...;...;...;...)")
      - no or partial information can be provided, in the latter case add nothing between respective semicolons
      - if a category has multiple values, separate them by comma (e.g., 2 solvers: "log(...;...;Sat4j,Choco;...)")
    - example with no type of analysis or publication but 2 solvers: log(first solver test;;sharpSAT,Z3;)
  For each config, a new txt-file is created and stored in configs with
    - additional information by user if provided
    - all FMs used in benchmarks (info from fmb.csv-file)

  Keyword argument:
  search_term -- user input (String) with possibly additional experimental parameters in parentheses
  fm_list     -- List of FMs (dictionaries) found by user
  """
  config_directory = os.path.join(os.path.dirname(__file__), '..', 'configs')
  # configs-directory may not yet exist
  if (not os.path.isdir(config_directory)):
    os.makedirs(config_directory)

  config_time = time.gmtime()
  time_for_names = time.strftime("%Y%m%d_%H%M%S", config_time)

  isFmbWanted = False
  if((search_term.startswith("fmb")) and ("+" in search_term)):
    isFmbWanted = True
    search_term = search_term.partition("+")[2]

  if(isFmbWanted):
    # create a new subdirectory in configs for every config
    config_sub_name = "config" + time_for_names
    config_sub_directory = os.path.join(config_directory, config_sub_name)
    os.makedirs(config_sub_directory)
    if(fm_list):
      create_benchmark(fm_list, config_sub_directory)

  # normally, config txt-file is created in configs-directory, but with FMB it's created in sub-directory of configs
  config_filename = "config_" + time_for_names + ".txt"
  conf_filepath = os.path.join(config_directory, config_filename)
  if(isFmbWanted):
    conf_filepath = os.path.join(config_sub_directory, config_filename)

  # recovering the user's additional info about their experiment
  add_info = ""
  if(("(" in search_term) and (")" in search_term)):
    # 1. partition: part after "(", 2. partition: part bevore ")"
    add_info = search_term.partition("(")[2].partition(")")[0]
  
  add_info_list = []
  printable_info = []
  if(add_info):
    if(";" in add_info):
      add_info_list = add_info.split(";")
      # so user info will show up in file as something like "ARE Sat4J"
      conf_keys = ["Name", "Analysis", "ARE", "Publication"]
      printable_info = list(zip(conf_keys, add_info_list))

  # first writing experiment info into file, then feature models
  with open(conf_filepath, "a") as conf_file:
    if(add_info_list):
      for added_info in printable_info:
        user_info = str(added_info[0]) + ": " + str(added_info[1]) + "\n"
        conf_file.write(user_info)
    conf_file.write("Time: " + time.strftime("%a, %d %b %Y %H:%M:%S +0000", config_time) + "\n")
    if(fm_list):
      for fm in fm_list:
        fm_entry = str(fm) + "\n"
        conf_file.write(fm_entry)
  conf_file.close()

def create_benchmark_from_config(search_term):
  """Create FM benchmark from FMs in a given config-file.

  User input is "read config"-command and name of file ("txt"-file extension optional) in one line.
  Config-filename is extracted and configs-directory is searched for config file.
  Config-files contain FMs as String-representations of dictionaries,
  all lines starting with "{'" (open curly brace followed by single quotation mark) are converted to dicts,
  FM dictionaries are saved in FM-list and benchmark created in benchmarks-directory.

  Keyword argument:
  search_term -- String (complete search term)
  """
  conf_filename = ""
  read_config_file_path = ""
  fm_list = []

  # first step: retrieve config-filename from user input
  for pref in list_read_conf_input:
    if(search_term.startswith(pref)):
      conf_filename = search_term.removeprefix(pref).strip()
  
  # config-file has to be in configs-directory
  config_directory = os.path.join(os.path.dirname(__file__), '..', 'configs')

  # find config-file matching user input
  if(conf_filename):
    for root, dirs, files in os.walk(config_directory):
      for conf_file in files:
        # find filename with or without extenstion "txt"
        if((conf_filename == conf_file) or (conf_filename + ".txt" == conf_file)):
          read_config_file_path = os.path.join(root, conf_file)
  else:
    print("No config-filename given")

  # find strings representing FMs in file (strings with "{'" as first characters)
  if(read_config_file_path):
    with open(read_config_file_path, "r") as read_conf:
      for line in read_conf:
        if(line.startswith("{'")):
          fm = ast.literal_eval(line)
          fm_list.append(fm)
    read_conf.close()
  else:
    print("No config-file found")

  # create benchmark in benchmarks-directory with feature models
  if(fm_list):
    create_benchmark(fm_list)

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
    string_of_domains = ', '.join(list_of_domains)
    print(string_of_domains)
  elif(user_input in list_formats_info_input):
    # To get a list of formats currently present in the feature model benchmark
    list_of_formats = get_category_sublist("Format")
    string_of_formats = ', '.join(list_of_formats)
    print(string_of_formats)
  elif(user_input in list_features_info_input):
    create_numbers_info(feature_models, "#Features")
  elif(user_input in list_ctc_info_input):
    create_numbers_info(feature_models, "#CTC")
  elif(user_input in list_get_fms_input):
    global isBenchmarkWanted
    isBenchmarkWanted = True
    print('FM Benchmark will be created in a subdirectory of "benchmarks"')
  elif(user_input in list_get_log_input):
    global original_input
    original_input = search_term
    global isConfigWanted
    isConfigWanted = True
    print('FM Config will be created in a configs directory')
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
  # turns numbers separated by "to", "t", "-" or ".." into list of numbers
  values = val.replace("to", " ").replace("t", " ").replace("-", " ").replace("..", " ").split()
  # cover cases with invalid input as range, i.e. not two numbers separated by "to", "t", "-" or ".."
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

def create_numbers_info(fm_list, num_cat):
  """Prints statistics for features or cross-tree constraints

  Keyword argument:
  fm_list -- list of FMs (dicts)
  num_cat -- String (search category, either "#Features" or "#CTC") 
  """
  num_list = []

  if(num_cat == "#Features"):
    num_list = calc_stat(fm_list, num_cat)

  if(num_cat == "#CTC"):
    num_list = calc_stat(fm_list, num_cat)

  num_string = beautify_list_of_tuples(num_list)
  print(num_string)

def calc_stat(fm_list, category):
  """Calculate statistics for a list of FMs

  Goes through list of FMs and calculates statistics for categories represented as numbers:
    - lowest number
    - highest number
    - arithmetic mean
    - median
  (note that geometric mean is not easily possible as FMs can have 0 CTCs)
  Returns list of tuples (name, number)

  Keyword argument:
  fm_list  -- list of FMs (dicts)
  category -- String (search category, either "#Features" or "#CTC") 
  """
  lowest_num = 0
  highest_num = 0
  arith_mean = 0
  median = 0

  num_list = []

  for fm in fm_list:
    for key, value in fm.items():
      if(key == category):
        if(value.isnumeric()):
          num_list.append(int(value))
  if(num_list):
    num_list.sort()
    lowest_num = num_list[0]
    highest_num = num_list[-1]
    arith_mean = statistics.fmean(num_list)
    median = statistics.median(num_list)

  num_values = [lowest_num, highest_num, arith_mean, median]
  num_names = ["Lowest", "Highest", "Arith. Mean", "Median"]

  name_values = list(zip(num_names, num_values))

  return name_values

def beautify_list_of_tuples(tup_list):
  """Turns list of 2-tuples into printable string

  List of tuples like "[('test', 123)]" is turned into string "test: 123" and returned

  Keyword argument:
  tup_list -- list of 2-tuples
  """
  beautiful_list = []

  for tup in tup_list:
    name = tup[0]
    val = tup[1]
    entry = name + ": " + str(val)
    beautiful_list.append(entry)

  beautiful_string = ', '.join(beautiful_list)

  return beautiful_string

print('For help, enter "help", to quit enter "quit" or "exit"')
isSearchRunning = True    # user has not received feature models yet
isCategoryGiven = False   # user has to give category before value
isValueGiven = False      # user has to give category and value to complete search
isBenchmarkWanted = False # user wants the FMs from the found FM benchmark
isConfigWanted = False    # user wants to save config about used FMs and experiment parameters
original_input = ""
category_list = []
value_list = []
excluded_search_key_values = []
while(isSearchRunning):
  isIntersection = False  # comma-separated values
  isUnion = False         # semicolon-separated values
  search_list = []
  search_term = input("Enter: ")
  isLogWithAddedInfoWanted = any(search_term.startswith(pref) for pref in list_get_log_input)
  isFmbAndLogWanted = (search_term.startswith("fmb")) and ("+" in search_term)
  if(search_term in list_exit_input):
    break
  elif(search_term in list_meta_input):
    give_meta_info(search_term)
  elif(isLogWithAddedInfoWanted or isFmbAndLogWanted):
    # case when user provides info about experiment, else it's in "list_meta_input"-elif above
    original_input = search_term
    isConfigWanted = True
  elif(search_term in list_give_all_input):
    for fm in feature_models:
      print(fm)
    if(isConfigWanted):
      create_config(original_input, feature_models)
    if(isBenchmarkWanted):
      create_benchmark(feature_models)
    break
  elif(any(search_term.startswith(pref) for pref in list_read_conf_input)):
    create_benchmark_from_config(search_term)
    break
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
        string_of_domains = ', '.join(list_of_domains)
        print("List of domains:", string_of_domains)
      if(any(x in list_format_input for x in category_list)):
        list_of_formats = get_category_sublist("Format")
        string_of_formats = ', '.join(list_of_formats)
        print("List of formats:", string_of_formats)

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

    '''
    NOT operator: preparatory step
    values to be excluded are moved to new list of category-values tuples
    not yet optimized: Search still also finds FMs to be excluded
                       FMs to be excluded will be removed from final result
    '''
    for i in search_key_values:
      # i is tuple like ('Format', '-XML') so we want to check first char of second tuple item ('-XML')
      if(i[1][0] == "-"):
        excluded_search_key_values.append(i)
    search_key_values = [search_item for search_item in search_key_values if search_item not in excluded_search_key_values]

    # checks if search keys are subset of an FM in our list of FMs
    fm_selection = []
    if(isIntersection):
      for cat,val in search_key_values:
        temp_selection = []
        if((cat == "Domain") or (cat == "Format")):
          temp_selection = add_fm_to_list(feature_models, cat, val)
          if(fm_selection):
            fm_selection = [fm for fm in fm_selection if fm in temp_selection]
          else: 
            fm_selection = temp_selection
        elif((cat == "#Features") or (cat == "#CTC")):
          if(">" in val):
            temp_selection = find_higher(feature_models, cat, val)
          elif("<" in val):
            temp_selection = find_lower(feature_models, cat, val)
          elif(any(range_op in val for range_op in list_range_operators)):
            temp_selection = find_range(feature_models, cat, val)
          else:
            temp_selection = add_fm_to_list(feature_models, cat, val)
          if(fm_selection):
            fm_selection = [fm for fm in fm_selection if fm in temp_selection]
          else:
            fm_selection = temp_selection
      if(excluded_search_key_values):
        remove_fm_selection = []
        for cat,val in excluded_search_key_values:
          # remove "-" from value
          not_val = val[1:]
          if((cat == "Domain") or (cat == "Format")):
            for fm in fm_selection:
              remove_fm_selection = add_fm_to_list(fm_selection, cat, not_val)
          elif((cat == "#Features") or (cat == "#CTC")):
            if(">" in val):
              remove_fm_selection = find_higher(fm_selection, cat, not_val)
            elif("<" in val):
              remove_fm_selection = find_lower(fm_selection, cat, not_val)
            elif(any(range_op in val for range_op in list_range_operators)):
              remove_fm_selection = find_range(fm_selection, cat, not_val)
            else:
              remove_fm_selection = add_fm_to_list(fm_selection, cat, not_val)
        fm_selection = [fm for fm in fm_selection if fm not in remove_fm_selection]
    elif(isUnion):
      pre_fm_selection = []
      if(search_key_values):
        for cat,val in search_key_values:
          temp_selection = []
          if((cat == "Domain") or (cat == "Format")):
            temp_selection = add_fm_to_list(feature_models, cat, val)
            pre_fm_selection = pre_fm_selection + temp_selection
          elif((cat == "#Features") or (cat == "#CTC")):
            if(">" in val):
              temp_selection = find_higher(feature_models, cat, val)
            elif("<" in val):
              temp_selection = find_lower(feature_models, cat, val)
            elif(any(range_op in val for range_op in list_range_operators)):
              temp_selection = find_range(feature_models, cat, val)
            else:
              temp_selection = add_fm_to_list(feature_models, cat, val)
            pre_fm_selection = pre_fm_selection + temp_selection
      if(excluded_search_key_values):
        for cat,val in excluded_search_key_values:
          # remove "-" from value
          not_val = val[1:]
          remove_fm_selection = []
          fm_selection_without_excluded = []
          if((cat == "Domain") or (cat == "Format")):
            remove_fm_selection = add_fm_to_list(feature_models, cat, not_val)
          elif((cat == "#Features") or (cat == "#CTC")):
            if(">" in val):
              remove_fm_selection = find_higher(feature_models, cat, not_val)
            elif("<" in val):
              remove_fm_selection = find_lower(feature_models, cat, not_val)
            elif(any(range_op in val for range_op in list_range_operators)):
              remove_fm_selection = find_range(feature_models, cat, not_val)
            else:
              remove_fm_selection = add_fm_to_list(feature_models, cat, not_val)
          # all FMs without those to be excluded
          fm_selection_without_excluded = [fm for fm in feature_models if fm not in remove_fm_selection]
          # unify the sets of FMs without those to be excluded
          pre_fm_selection = pre_fm_selection + fm_selection_without_excluded
      # remove duplicates
      for fm in pre_fm_selection:
        if(fm not in fm_selection):
          fm_selection.append(fm)

    if(fm_selection):
      for fm in fm_selection:
        print(fm)

    if(isConfigWanted):
      create_config(original_input, fm_selection)
    if(isBenchmarkWanted):
      create_benchmark(fm_selection)

    isSearchRunning = False