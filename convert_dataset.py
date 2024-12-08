import json
import pandas as pd

def convert_jsonl_to_csv(input_file, output_file, max_rows=25000):
    # Read JSONL file
    data = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= max_rows:
                break
            if line.strip():  # Skip empty lines
                data.append(json.loads(line.strip()))
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Converted {input_file} to {output_file}")
    print(f"Number of records: {len(df)}")
    print(f"Columns: {', '.join(df.columns)}\n")

# Convert files
convert_jsonl_to_csv('meta_Beauty_and_Personal_Care.jsonl', 'beauty_and_personal_care_metadata.csv')
