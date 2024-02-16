import pandas as pd
import nltk
from nltk.corpus import wordnet as wn
import sys

# Ensure WordNet is downloaded
nltk.download('wordnet', quiet=True)

def get_synset_name(synsetId):
    synset = wn.synset_from_pos_and_offset('n', int(synsetId))
    return synset.name().split('.')[0]

def get_sub_synset_name(synsetId):
    synset = wn.synset_from_pos_and_offset('n', int(synsetId))
    # For simplicity, fetch the first lemma's name of the synset
    # Adjust this logic based on your actual needs for the SubSynetName
    return synset.lemmas()[0].name() if synset.lemmas() else ''

def add_synset_columns(source_file, target_file):
    # Read the source CSV
    df = pd.read_csv(source_file)
    
    # Add new columns, initialize with empty strings
    df['SynsetName'] = ''
    df['SubSynsetName'] = ''  # New column for SubSynsetName
    
    for index, row in df.iterrows():
        try:
            # Assuming 'synsetId' is the column with synset ID
            synsetId = str(row['synsetId'])
            subsynsetId = str(row['subSynsetId'])
            df.at[index, 'SynsetName'] = get_synset_name(synsetId)
            df.at[index, 'SubSynsetName'] = get_sub_synset_name(subsynsetId)  # Fetch and set SubSynsetName
        except Exception as e:
            print(f"Error processing row {index}: {e}")
        
        # Track progress
        sys.stdout.write(f"\rProcessing: {int((index + 1) / len(df) * 100)}%")
        sys.stdout.flush()

    # Save to target CSV
    df.to_csv(target_file, index=False)
    print("\nDone.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python add_synset_columns.py source_file.csv target_file.csv")
    else:
        source_file, target_file = sys.argv[1], sys.argv[2]
        add_synset_columns(source_file, target_file)
