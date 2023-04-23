# Feature-Model Benchmark

Our comprehensive feature collection provides large, real-world feature models for empirical evaluations.
All currently available feature models, including characteristics and their sources, can be found in *feature_models/original/*.
Further, we provide a .csv file showcasing information for every feature model in *statistics/FullCombined.csv*.
We offer additional functionality to make use of the collection more convenient. 
Users can search for a subset of feature models, create configuration files indicating their subset, and create subsets from existing configuration files.

# Adding New Feature Models
We plan on continually extending our collection to keep a reasonable coverage of the literature. We also highly appreciate if new feature models are added by the community via PR to this repository.

# Search Procedure

## Setup

The script is based on Python3. To install the required dependencies please use:

`pip3 install -r requirements.txt`

## Usage

*scripts/extract_collection.py* can be used to create a filtered subset of the feature model collection.

Show help for the different parameters that can be used for filtering:

`python3 scripts/extract_collection.py -h`


## Example Search Procedures

Create collection with feature models between 500 and 2,000 features:

`python3 scripts/extract_collection.py --features 500..2000`

Create collection with feature models from the automotive domain:

`python3 scripts/extract_collection.py --domains automotive`

Create collection with all feature models but early versions of a history:

`python3 scripts/extract_collection.py --versions last`

Create collection with feature models for which a history is available: 

`python3 scripts/extract_collection.py --evolution` 

Create collection with same feature models as specified in configuration json:

`python3 scripts/extract_collection.py --load_config paper_configs/Krieter2020.json`

