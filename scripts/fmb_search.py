import csv
import os
import shutil
import time
import ast
import statistics
import argparse
import sys
import json

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
# to change how FM data output (default: dictionary), give format after command
list_translation_input = ['translate', 'trans', 'tra', 't']
allowed_input = list_meta_input + list_category_input + list_give_all_input + list_read_conf_input + list_translation_input

list_separators_AND = [',', '&']
list_separators_OR = [';', '|']

list_range_operators = ['to', 't', '-', '..']

list_stats_request = ['statistics', 'stats', 'stat', 's']

list_data_formats = ['yaml', 'json', 'csv', 'xml']

# for command line arguments
parser = argparse.ArgumentParser(description="Processes categories and values")
parser.add_argument("--cat", help="Provide categories to search for.")
parser.add_argument("--val", help="Provide the values for the respective categories.")
parser.add_argument("--cft", help="Allowed input: log, fmb, fmb+log, one of the formats to translate into")
args = parser.parse_args()

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
  (for numerical values, "k" and "m" can substitute "000" and "000000", e.g. "50k" instead of "50000")
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
  - Possible are config-commands with and without additional information,
    e.g., both "log+fmb" or "fmb+log(name;analysis;ARE;publication)
Get statistics about features and CTCs of found FMs only:
  - Add "+s" or "+stats" to category
  - Example: dom+s
Create FMB from config txt-file:
  - Command: rc config.txt (extension is optional, filename is enough)
  - Config-file needs to be txt-file in configs-directory
  - FMs have to be String-representations of dictionaries, starting with "{'"
    no other entry than FMs should start with "{'" (open curly brace followed by single quotation mark)
  - Benchmark is created in benchmarks-directory
Translate FMs to different format:
  - Currently available formats: CSV, JSON, XML, YAML
  - XML and YAML need extra libraries to work:
    - XML 
      - Library: dicttoxml
      - Install: pip install dicttoxml
    - YAML
      - Library: PyYAML
      - Install: pip install pyyaml
  - FMs can be either from the current search or from a file with FM-dictionaries
  - A file as source of FMs must be stored in configs-directory
  - Command: trans (filename) format
    - Second parameter "filename" is optional
    - Command "trans format" uses FMs from the current search
    - Command "trans filename format" retrieves FMs from the file and exits the program
  - Example 1: trans json
  - Example 2: trans config_20221214_081414 csv
  - Creates a file in configs-directory, name beginning with "tlconfig" ("tl" for "translated")
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
     Solution 7.1:
      domain;features
      business;-<70000
    Solution 7.2:
      domain;features
      business;-<70k
'''

def translate_fms(fm_source, fm_format):
  """Translate FM-dicts into format specified in a new file

  User wants to translate FM-dicts into a different format of which the following are
  currently supported: CSV, JSON, YAML, XML
  Source of FMs is either 
   - List of FMs from regular FM search
   - Config-file with FM-dicts
  In case of the latter, the FMs are extracted from the file (must be in configs-directory)
  FMs are then translated but note that YAML and XML need extra libraries
   - YAML: PyYaml
   - XML: dict2xml
  The translated FMs are written to a new file, filename beginning with "tlconfig", in configs-directory

  Keyword argument:
  fm_source -- Either config-filename or list of FM-dicts
  fm_format -- String (format to translate FMs into) 
  """
  fm_indicator = "{'"
  extension = ""
  fm_list = []
  translated_fms = []

  # 1. Retrieving the FMs
  # either list of FM-dictionaries is given
  if(isinstance(fm_source, list)):
    fm_list = fm_source
  # or the name of a config-file to get FMs from
  elif(isinstance(fm_source, str)):
    fm_list = get_fms_from_config(fm_source, fm_indicator)
  
  # 2. Translating the FMs
  if(fm_format.lower() == "yaml"):
    import yaml
    extension = ".yaml"
    for fm in fm_list:
      fm_yaml = yaml.dump(fm)
      translated_fms.append(fm_yaml)
  elif(fm_format.lower() == "xml"):
    import dicttoxml
    extension = ".xml"
    for fm in fm_list:
      fm_xml = dicttoxml.dicttoxml(fm)
      translated_fms.append(fm_xml)
  elif(fm_format.lower() == "json"):
    extension = ".json"
    for fm in fm_list:
      fm_json = json.dumps(fm)
      translated_fms.append(fm_json)
  elif(fm_format.lower() == "csv"):
    extension = ".csv"
    first_line = "Name,Domain,Format,#Features,#CTC,Source"
    translated_fms.append(first_line)
    for fm in fm_list:
      fm_csv = ",".join(fm.values())
      translated_fms.append(fm_csv)

  # 3. Creating the file with translated FMs
  config_directory = os.path.join(os.path.dirname(__file__), '..', 'configs')
  config_time = time.gmtime()
  time_for_names = time.strftime("%Y%m%d_%H%M%S", config_time)
  tlconfig_filename = "tlconfig_" + time_for_names + extension
  tlconf_filepath = os.path.join(config_directory, tlconfig_filename)
  with open(tlconf_filepath, "a") as conf_file:
    if(translated_fms):
      for fm in translated_fms:
        tlfm_entry = str(fm) + "\n"
        conf_file.write(tlfm_entry)
  conf_file.close()

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

def create_config(search_term, fm_list, isFmbWanted = False):
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
  isFmbWanted -- Boolean to indicate whether FMB should be created or not
  """
  config_directory = os.path.join(os.path.dirname(__file__), '..', 'configs')
  # configs-directory may not yet exist
  if (not os.path.isdir(config_directory)):
    os.makedirs(config_directory)

  config_time = time.gmtime()
  time_for_names = time.strftime("%Y%m%d_%H%M%S", config_time)

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
  fm_list = []

  # first step: retrieve config-filename from user input
  for pref in list_read_conf_input:
    if(search_term.startswith(pref)):
      conf_filename = search_term.removeprefix(pref).strip()

  fm_list = get_fms_from_config(conf_filename, "{'")

  # create benchmark in benchmarks-directory with feature models
  if(fm_list):
    create_benchmark(fm_list)

def get_fms_from_config(conf_filename, fm_indicator):
  """Retrieves FMs from a config file and returns them in a list

  Searches the configs-directory for a file with the given conf_filename.
  If it finds the file, it opens the file and 
  searches for lines beginning with the fm_indicator-String,
  retrieves the FMs, saves them in a list and returns the list of FMs.

  Keyword argument:
  conf_filename -- Name of the FM-containing config-file to search and read
  fm_indicator  -- String indicating the start of a FM in the config-file to know what to read
  """
  # will be list of dicts (representing FMs)
  fm_list = []
  read_config_file_path = ""
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
              if(line.startswith(fm_indicator)):
                  fm = ast.literal_eval(line)
                  fm_list.append(fm)
          read_conf.close()
  else:
      print("No config-file found")
  
  return fm_list

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
    print('FM benchmark will be created in a subdirectory of "benchmarks"')
  elif(user_input in list_get_log_input):
    global original_input
    original_input = search_term
    global isConfigWanted
    isConfigWanted = True
    print('FM config will be created in directory configs')
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
  act_val = kilo_mil_to_zeroes(act_val)
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
  act_val = kilo_mil_to_zeroes(act_val)
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
  # user can now add "k" in number to represent "000"
  values = kilo_mil_to_zeroes(values)
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

def kilo_mil_to_zeroes(numeric_string):
  """Replaces "k" and "m" in strings with "000" and "000000" respectively

  For the find_range, find_lower and find_higher functions.
  Allows user to input, for example, 50k instead of all the zeroes.

  Keyword argument:
  numeric_string -- String or list of strings
  """
  # the case for the range function
  if isinstance(numeric_string, list):
    for index,val in enumerate(numeric_string):
      if("k" in val):
        numeric_string[index] = val.replace("k", "000")
      if("m" in val):
        numeric_string[index] = val.replace("m", "000000")
    return numeric_string
  # in case of find_lower or find_higher functions
  else:
    if("k" in numeric_string):
      numeric_string = numeric_string.replace("k", "000")
    if("m" in numeric_string):
      numeric_string = numeric_string.replace("m", "000000")
    return numeric_string

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
  print(num_cat + ": " + num_string)

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

def create_fmb_keys(category_list):
  """Maps category input to category name used in the program

  Keyword argument:
  category_list -- list of strings (user category input)
  """
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
  return fmb_keys

def create_intersection_fm_selection(fm_selection, search_key_values, excluded_search_key_values):
  """Creates list of FMs when user asks for intersection (comma, ampersand)

  Keyword argument:
  fm_selection               -- empty list
  search_key_values          -- list of domain-value-tuples
  excluded_search_key_values -- list of "NOT"-values
  """
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
  return fm_selection

def create_union_fm_selection(fm_selection, search_key_values, excluded_search_key_values):
  """Creates list of FMs when user asks for union (semicolon, pipe)

  Keyword argument:
  fm_selection               -- empty list
  search_key_values          -- list of domain-value-tuples
  excluded_search_key_values -- list of "NOT"-values
  """
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
  return fm_selection

if(args.cat and args.val):
  isIntersection = False
  isUnion = False
  category_list = []
  value_list = []
  excluded_search_key_values = []
  isAndInCat = any(x in list_separators_AND for x in args.cat)
  isAndInVal = any(x in list_separators_AND for x in args.val)
  isOrInCat = any(x in list_separators_OR for x in args.cat)
  isOrInVal = any(x in list_separators_OR for x in args.val)
  if(isAndInCat and isAndInVal):
    isIntersection = True
    category_list = split_with_separators(args.cat, list_separators_AND)
    value_list = split_with_separators(args.val, list_separators_AND)
  elif(isOrInCat and isOrInVal):
    isUnion = True
    category_list = split_with_separators(args.cat, list_separators_OR)
    value_list = split_with_separators(args.val, list_separators_OR)
  else:
    isUnion = True
    category_list.append(args.cat)
    value_list.append(args.val)

  fmb_keys = create_fmb_keys(category_list)
  search_key_values = list(zip(fmb_keys, value_list))

  for i in search_key_values:
    if(i[1][0] == "-"):
      excluded_search_key_values.append(i)
  search_key_values = [search_item for search_item in search_key_values if search_item not in excluded_search_key_values]

  fm_selection = []
  if(isIntersection):
    fm_selection = create_intersection_fm_selection(fm_selection, search_key_values, excluded_search_key_values)
  elif(isUnion):
    fm_selection = create_union_fm_selection(fm_selection, search_key_values, excluded_search_key_values)

  if(fm_selection):
    for fm in fm_selection:
      print(fm)

  if(args.cft):
    if(args.cft == "log"):
      create_config(args.cft, fm_selection)
    if(args.cft == "fmb"):
      create_benchmark(fm_selection)
    if((args.cft == "fmb+log" or args.cft == "log+fmb")):
      create_config(args.cft, fm_selection, True)
    if(args.cft in list_data_formats):
      translate_fms(fm_selection, args.cft)
  sys.exit()

print('For help, enter "help", to quit enter "quit" or "exit"')
isSearchRunning = True      # user has not received feature models yet
isCategoryGiven = False     # user has to give category before value
isValueGiven = False        # user has to give category and value to complete search
isBenchmarkWanted = False   # user wants the FMs from the found FM benchmark
isConfigWanted = False      # user wants to save config about used FMs and experiment parameters
isConfAndFmbWanted = False  # user wants config and benchmark
isAddStatsWanted = False    # user wants statistics about FMs found through search
isTranslationWanted = False # user wants output in different format than dictionary
translation_format = ""
translation_filename = ""
original_input = ""
category_list = []
value_list = []
excluded_search_key_values = []
translated_fm_selection = []
while(isSearchRunning):
  isIntersection = False  # comma-separated values
  isUnion = False         # semicolon-separated values
  search_list = []
  search_term = input("Enter: ")
  # user wants to exit the program
  if(search_term.lower() in list_exit_input):
    break
  # user wants log and FMB, or category and statistics: seearch term concatenated with "+"
  elif("+" in search_term):
    plus_split = search_term.split("+")
    if(len(plus_split) == 2):
      isFmbRequest = any(st in plus_split for st in list_get_fms_input)
      isLogRequest = any(any(st.startswith(pref) for pref in list_get_log_input) for st in plus_split)
      isStatsRequest = any(st in plus_split for st in list_stats_request)
      if(isFmbRequest and isLogRequest):
        original_input = search_term
        isConfigWanted = True
        isConfAndFmbWanted = True
        print("FM config and benchmark will be created in subdirectory of configs")
      if(isStatsRequest):
        isAddStatsWanted = True
        for st in plus_split:
          if(st not in list_stats_request):
            search_term = st
    else:
      print('Use the "+"-operator only with two operands')
  # user wants information or creation of simple FMB or log
  elif(search_term.lower() in list_meta_input):
    give_meta_info(search_term.lower())
  # user wants log and provides additional information ("log(...)")
  elif(any(search_term.startswith(pref) for pref in list_get_log_input)):
    original_input = search_term
    isConfigWanted = True
    print('FM config with additional info will be created in directory configs')
  # user wants all available feature models
  elif(search_term.lower() in list_give_all_input):
    for fm in feature_models:
      print(fm)
    if(isConfigWanted):
      create_config(original_input, feature_models)
    if(isBenchmarkWanted):
      create_benchmark(feature_models)
    break
  # user gives name of config-file and wants benchmark from it
  elif(any(search_term.startswith(pref) for pref in list_read_conf_input)):
    create_benchmark_from_config(search_term)
    break
  # user wants FM dictionaries translated into other output format like JSON, YAML or CSV
  elif(any(search_term.lower().startswith(p) for p in list_translation_input) and any(search_term.lower().endswith(s) for s in list_data_formats)):
    isTranslationWanted = True
    # command is something like "trans (filename) format" with filename being optional
    # split into list, either ["trans", "format"] or ["trans", "filename", "format"]
    com_list = search_term.split()
    translation_format = com_list[-1]
    if(len(com_list) == 3):
      translation_filename = com_list[1]
      translate_fms(translation_filename, translation_format)
      break
    print("Output format will be", translation_format)

  if(search_term):
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
    if(isNotCategories and isCategoryGiven): # value has to be provided by user after category
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
    fmb_keys = create_fmb_keys(category_list)

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
      fm_selection = create_intersection_fm_selection(fm_selection, search_key_values, excluded_search_key_values)
    elif(isUnion):
      fm_selection = create_union_fm_selection(fm_selection, search_key_values, excluded_search_key_values)

    if(fm_selection):
        for fm in fm_selection:
          print(fm)

    if(isAddStatsWanted):
      create_numbers_info(fm_selection, "#Features")
      create_numbers_info(fm_selection, "#CTC")
    if(isConfigWanted):
      create_config(original_input, fm_selection, isConfAndFmbWanted)
    if(isBenchmarkWanted):
      create_benchmark(fm_selection)
    if(isTranslationWanted):
      translate_fms(fm_selection, translation_format)

    isSearchRunning = False