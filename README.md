# Feature-Model Benchmark

Our comprehensive feature collection provides large, real-world feature models for empirical evaluations.
All currently available feature models, including characteristics and their sources, can be found in *feature_models/original/*.
Further, we provide a .csv file showcasing information for every feature model in *statistics/FullCombined.csv*.
We offer additional functionality to make use of the collection more convenient. 
Users can search for a subset of feature models, create configuration files indicating their subset, and create subsets from existing configuration files.

## Included Feature Models
As of now, 5,662 feature models our included in our collection covering various domains. Below you can find an overview about the include feature models. For more details on the feature models, we refer to `statistics/FullCombined.csv`.

|Domain           | #Systems| #Feature Models| #Histories| Feature Range | Constraint Range|
|-----------------|---------|----------------|-----------|---------------|-------------|
|Automotive       | 2       | 5              | 1         | 2,513--18,253 | 666--2,833  |
|Business         | 1       | 1              | 0         | 1,920         | 59,044      |
|Cloud            | 1       | 1              | 0         | 2,513--18,253 | 200--3,000  | 
|Database         | 1       | 1              | 0         | 117           | 282         | 
|Deep Learning    | 1       | 2              | 0         | 3,296--6,867  | 9--76       |
|E-Commerce       | 2       | 2              | 0         | 17--2,238     | 0           |
|Finance          | 4       | 13             | 1         | 142--774      | 4--1,148    |
|Games            | 1       | 1              | 0         | 2,513--18,253 | 200--3,000  |
|Hardware         | 3       | 3              | 0         | 2,513--18,253 | 200--3,000  | 
|Navigation       | 2       | 2              | 0         | 2,513--18,253 | 200--3,000  | 
|Security         | 2       | 1,464          | 0         | 101--4,351    | 1--8,138    |
|Systems Software | 135     | 4,166          | 2         | 179--62,483   | 26--343,944 | 
|Text             | 1       | 1              | 0         | 2,513--18,253 | 200--3000   |
|**Overall**      | **156** | **5,662**      | **4**     | **117--62,483**| **0--343,944**|                            

## Adding New Feature Models
We plan on continually extending our collection to keep a reasonable coverage of the literature. We also highly appreciate if new feature models are added by the community via PR to this repository.

## Dataset Extraction Procedure

### Setup

The script is based on Python3. To install the required dependencies please use:

`pip3 install -r requirements.txt`

### Usage

*scripts/extract_collection.py* can be used to create a filtered subset of the feature model collection.

Show help for the different parameters that can be used for filtering:

`python3 scripts/extract_collection.py -h`


### Example Extraction Procedures

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

