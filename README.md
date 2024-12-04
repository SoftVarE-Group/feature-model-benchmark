[![DOI](https://zenodo.org/badge/527877748.svg)](https://zenodo.org/doi/10.5281/zenodo.11652924)

# Feature-Model Benchmark

Our comprehensive feature collection provides large, real-world feature models for empirical evaluations.
All currently available feature models, including jsons indicating characteristics and sources of the respective feature models, can be found in *feature_models/original/*.
Further, we provide a .csv file showcasing information for every feature model in *statistics/Complete.csv*.
We offer additional functionality to make use of the collection more convenient. 
Users can search for a subset of feature models, create configuration files indicating their subset, and create subsets from existing configuration files.

## Included Feature Models
As of now, 2,518 feature models our included in our collection covering various domains. Below you can find an overview about the include feature models. For more details on the feature models, we refer to `statistics/Complete.csv`.

| Domain           | #Systems | #Feature Models | #Histories | Feature Range   | Clause Range   |
| ---------------- | -------- | --------------- | ---------- | --------------- | -------------- |
| Automotive       | 2        | 5               | 1          | 2,513--18,253   | 666--2,833     |
| Business         | 1        | 1               | 0          | 1,920           | 59,044         |
| Cloud            | 1        | 1               | 0          | 145             | 16             |
| Database         | 1        | 1               | 0          | 117             | 282            |
| Deep Learning    | 1        | 2               | 0          | 3,296--6,867    | 9--76          |
| E-Commerce       | 2        | 2               | 0          | 173--2,238      | 0              |
| Finance          | 4        | 13              | 1          | 142--774        | 4--1,148       |
| Games            | 1        | 1               | 0          | 144             | 0              |
| Hardware         | 2        | 2               | 0          | 172--364        | 0--12          |
| Navigation       | 2        | 2               | 0          | 103--145        | 2--13          |
| Security         | 2        | 1,464           | 0          | 101--4,351      | 1--8,138       |
| Systems Software | 21       | 1,025           | 5          | 179--80,258     | 26--767,040    |
| Text             | 1        | 1               | 0          | 137             | 102            |
| **Overall**      | **41**   | **2,518**       | **5**      | **101--80,258** | **0--767,040** |

## Repository Structure

The directory `feature_models/` contains the feature models in `original`, `dimacs`, and `uvl` format. Note that feature models originally in dimacs or UVL format are stored in `original` with no redundant copy in dimacs or UVL, respectively.
To get *all* feature models in the specific format, use the extraction script which will take care of such models for you. See below for usage examples.

`scripts` includes some scripts to interact with the collection. If you want to *use* the dataset, `scripts/extract_collection.py` should the most relevant for you to extract your collection. `scripts/dimacs_tools.py` provides several capabilities to preprocess dimacs files.
`scripts/manage_statistics.py` is used to update the statistics files in `statistics/` after adding or updating feature models.

The jsons in `paper_configs` each include a list of feature models used in other work on feature-model analysis. After using a subset of our benchmark, we welcome the addition of your .json. In `pre_configs` we provide subsets of the benchmark with certain properties that may be more suitable for specific use-case than the entire set. 

## Extracting Feature-Model Collections

### Setup

The script is based on Python3. To install the required dependencies please use:

`pip3 install -r requirements.txt`

### Usage

*scripts/extract_collection.py* can be used to create a filtered subset of the feature model collection.

Show help for the different parameters that can be used for filtering:

`python3 scripts/extract_collection.py -h`


### Example Extraction Procedures

Create collection with feature models between 500 and 2,000 features in UVL format:

`python3 scripts/extract_collection.py --features 500..2000 --output_format uvl`

Create collection with feature models from the automotive domain:

`python3 scripts/extract_collection.py --domains automotive`

Create collection with feature models in UVL format from the systems-software domain with at least 500 features

`python3 scripts/extract_collection.py --features 500.. --domains systems_software --output_format uvl`

Create collection with all feature models but early versions of a history:

`python3 scripts/extract_collection.py --versions last`

Create collection with feature models for which a history is available: 

`python3 scripts/extract_collection.py --evolution` 

Create collection with same feature models as specified in configuration json:

`python3 scripts/extract_collection.py --load_config paper_configs/Krieter2020.json`

Create collection with all feature models in UVL with a flat hierarchy in the target directory:
`python3 scripts/extract_collection.py --output_format uvl --flat`

## Contributing

We highly appreciate if new feature models are added by the community via PR to this repository.
For every (group of) feature models, we require a json that indicates some meta information on the origin of the feature model. See an example below for the format.
Please provide at least: *Name*, *Year*, *OriginalFormat*, *Publication*, and *Source*. 

```
{
    "Name" : "Automotive01",
    "Year" : 2016,
    "OriginalFormat" : "FeatureIDE",
    "Hierarchy" : true,
    "History":  [],
    "Publication" : "https://doi.org/10.1145/3093335.2993248",
    "Source" : "https://github.com/FeatureIDE/FeatureIDE",
    "Keywords" : [
        "Obfuscated",
        "Proprietary",
        "Automatic"
    ],
    "ConversionTool" : ""
}
```

## Relevant Repositories

* [Feature-Model Analysis](https://github.com/SundermannC/feature-model-batch-analysis): FeatureIDE-based Java tool for creating analysis results for the csv files in statistics
* [Feature-Model Conversion (TraVarT extension)](https://github.com/SundermannC/TraVarT/): TraVarT-based conversion for various formats to DIMACS and UVL


## Cite our work
If you use this collection for your research, please cite this work below.
```
@inproceedings{SBK+:SPLC24,
	author = {Sundermann, Chico and Brancaccio, Vincenzo Francesco and Kuiter, Elias and Krieter, Sebastian and He{\ss}, Tobias and Th{\"{u}}m, Thomas},
	title = {{Collecting Feature Models from the Literature: A Comprehensive Dataset for Benchmarking}},
	booktitle = "Proc.\ Int'l Systems and Software Product Line Conf.\ (SPLC)",
	year = 2024,
	month = SEP,
	publisher = "ACM",
    address = "New York, NY, USA"
}
```