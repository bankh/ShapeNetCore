import pandas as pd
import json
import sys

def compile_data(source_file, validation_file, output_json):
    # Load the source CSV
    source_df = pd.read_csv(source_file)
    
    try:
        # Load the validation file and extract modelIds
        with open(validation_file, 'r') as vf:
            # Extract the modelId from each path, assuming it's the fourth segment from the end
            valid_model_ids = {line.strip().split('/')[-3] for line in vf.readlines()}
            print('Valid_model_ids:',valid_model_ids)
    except Exception as e:
        print(f"Error processing validation file: {e}")
        sys.exit(1)

    # Group by synsetId to aggregate children and names
    grouped = source_df.groupby('synsetId')
    output_data = []
    
    for synsetId, group in grouped:
        unique_subsynsets = set(group['subSynsetId'].tolist())
        unique_names = set(group['SynsetName'].tolist() + group['SubSynsetName'].tolist())
        # Ensure names do not include NaN
        unique_names = {name for name in unique_names if pd.notna(name)}
        name = ','.join(unique_names)
        
        # Adjusted calculation for num_instances
        num_instances = sum(group['modelId'].isin(valid_model_ids))
        
        output_data.append({
            'synsetId': str(synsetId).zfill(8),  # Ensure synsetId is a string with leading zeros
            'name': name,
            'children': list(unique_subsynsets),
            'numInstances': num_instances
        })
        
    # Save to JSON
    with open(output_json, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"Data compiled into {output_json}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python csv_to_json.py source_file.csv validation_file.txt output_file.json")
    else:
        source_file, validation_file, output_json = sys.argv[1:4]
        compile_data(source_file, validation_file, output_json)
