import pandas as pd
import shutil
import os
import sys

def validate_and_prepare_directories(source_csv, validation_txt, target_dir):
    # Step 1: Read the validation file and create a set of valid model IDs
    valid_model_ids = set()
    with open(validation_txt, 'r') as val_file:
        for line in val_file:
            model_id = line.strip().split('/')[-3]
            valid_model_ids.add(model_id)

    # Step 2: Read the source CSV
    try:
        df = pd.read_csv(source_csv)
    except Exception as e:
        print(f"Error reading {source_csv}: {e}")
        sys.exit(1)

    # Prepare the counter and total rows for progress tracking
    total_rows = len(df)
    processed_count = 0

    # Step 3: Process each row and copy folders
    for index, row in df.iterrows():
        model_id = row['modelId']
        split = row['split']
        processed_count += 1

        # Construct the source directory path for the model
        # You need to adjust this path based on your actual source directory structure
        source_model_dir = f"../data/SHAPENET/ShapeNetCore/{row['synsetId']}/{model_id}/models/"

        # Construct the target directory path based on the split
        target_split_dir = os.path.join(target_dir, split, model_id)

        if model_id in valid_model_ids:
            print(f"{processed_count}/{total_rows} - Valid model ID found: {model_id}. Copying to {target_split_dir}.")
            if not os.path.exists(target_split_dir):
                os.makedirs(target_split_dir)
            # Copy the directory
            # shutil.copytree(source_model_dir, target_split_dir) # Uncomment this line to perform the copy
        else:
            print(f"{processed_count}/{total_rows} - Model ID {model_id} not found in validation.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <source_csv_file> <validation_txt_file> <target_directory>")
        sys.exit(1)
    
    source_csv = sys.argv[1]
    validation_txt = sys.argv[2]
    target_directory = sys.argv[3]
    validate_and_prepare_directories(source_csv, validation_txt, target_directory)
