# ShapeNetCore

This documentation outlines the process and logic of Python scripts developed for enhancing a dataset stored in CSV format and validating model IDs against an external text file. At the end, these will generate the `taxonomy.json` file which is required by various implementation of ShapeNetCore. The workflow involves two primary steps:

**Adding Synset Names to a CSV File:** The first script reads an input CSV file, adds additional columns with synset names and sub-synset names using the Natural Language Toolkit (NLTK)'s WordNet interface, and saves the enhanced dataset to a new CSV file.

**Validating Model IDs and Compiling Data into JSON:** The second script takes the enhanced CSV file, validates model IDs against a provided text file containing valid model paths, aggregates information by synsetId, and outputs the compiled data into a JSON file, including counts of validated models.

`shapenet_json.py`: Adding Synset and Sub-Synset Names
The first script aims to enrich a dataset by adding two columns by using the associated ids:

SynsetName: The name of the synset associated with each synsetId in the dataset.  
SubSynsetName: The name of the sub-synset associated with each subSynsetId.  

How It Works
- The script reads the source CSV file into a pandas DataFrame.
- For each row in the DataFrame, it uses the synsetId and subSynsetId to fetch synset and sub-synset names from WordNet via NLTK.
- These names are added to new columns for each corresponding row.
- Progress is tracked and displayed as a percentage.
- The enhanced DataFrame is saved to a new CSV file (all_names.csv).
  
```shell
$ python shapenet_json.py source_file.csv all_names.csv
```
`csv_to_json.py`: Validating Model IDs and Compiling Data into JSON
The second script processes the enhanced CSV file (all_names.csv), validates model IDs against a list of valid model paths (contained in json.txt), and compiles aggregated data into a JSON file. This includes counting the number of validated models for each synsetId.

How It Works
- Reads the enhanced CSV file and a validation text file.
- Extracts valid model IDs from the validation file paths, assuming the model ID is located in the fourth segment from the end of each path.
- Groups the DataFrame by synsetId and aggregates information, including unique names and children (subSynsetIds).
- Counts the number of instances where the model ID is found in the set of valid model IDs.
- Compiles this information into a list of dictionaries, each representing a synsetId with its name, children, and the count of validated models.
- Outputs this list to a JSON file (targetjson).

```shell
$ python csv_to_json.py all_names.csv json_validation.txt targetjson.json
```
These scripts provide a systematic approach to enhancing a dataset with meaningful synset information from WordNet and validating model IDs against an external source. The process aids in enriching the dataset for further analysis or usage, ensuring data integrity by validating model IDs and compiling aggregated information into a structured JSON format for easy access and manipulation.
```
...
  {
    "synsetId": "02691156", ## synsetId as groupname
    "name": "biplane,jet,propeller_plane,seaplane,bomber,delta_wing,fighter,airplane,airliner", ## all the subsynsetNames
    "children": [ ## unique susynsetIds
      20000000,
      20000001,
      20000002,
      2867715,
      2690373,
      4160586,
      2842573,
      4012084,
      3595860,
      3335030,
      2691156,
      3174079
    ],
    "numInstances": 2006 ## Total number of models in ShapeNetCore under the associated synsetId
  },
...
```
The rest of the dataset can be found on [HuggingFace](https://huggingface.co/datasets/ShapeNet/ShapeNetCore) after completion of the registration.

If you use this data, please cite the main ShapeNet technical report.
```
@techreport{shapenet2015,
  title       = {{ShapeNet: An Information-Rich 3D Model Repository}},
  author      = {Chang, Angel X. and Funkhouser, Thomas and Guibas, Leonidas and Hanrahan, Pat and Huang, Qixing and Li, Zimo and Savarese, Silvio and Savva, Manolis and Song, Shuran and Su, Hao and Xiao, Jianxiong and Yi, Li and Yu, Fisher},
  number      = {arXiv:1512.03012 [cs.GR]},
  institution = {Stanford University --- Princeton University --- Toyota Technological Institute at Chicago},
  year        = {2015}
}
```

**Reference:**
- ShapeNet Dataset Repository: https://github.com/datasets-mila/datasets--shapenet/tree/master
  
