import pandas as pd
import json

def clean_features(features):
    """Clean and format features list/dict"""
    if pd.isna(features) or not features:
        return ""
    try:
        if isinstance(features, str):
            features = json.loads(features)
        if isinstance(features, dict):
            return " ".join(f"{k}: {v}" for k, v in features.items())
        elif isinstance(features, list):
            return " ".join(str(f) for f in features)
        return str(features)
    except:
        return str(features)

def clean_categories(categories):
    """Clean and format categories list"""
    if pd.isna(categories) or not categories:
        return ""
    try:
        if isinstance(categories, str):
            categories = json.loads(categories)
        if isinstance(categories, list):
            return " > ".join(str(c) for c in categories)
        return str(categories)
    except:
        return str(categories)

def clean_details(details):
    """Clean and format details dictionary"""
    if pd.isna(details) or not details:
        return ""
    try:
        if isinstance(details, str):
            details = json.loads(details)
        if isinstance(details, dict):
            return " ".join(f"{k}: {v}" for k, v in details.items())
        return str(details)
    except:
        return str(details)

def prepare_text_for_embedding(row):
    """Prepare text for embedding by combining relevant fields"""
    # Start with the title as it's most important
    components = []
    
    # Add title with proper context
    if not pd.isna(row['title']):
        components.append(f"Title: {row['title']}")
    
    # Add categories with hierarchy
    cat_text = clean_categories(row['categories'])
    if cat_text:
        components.append(f"Categories: {cat_text}")
    
    # Add features as structured information
    feat_text = clean_features(row['features'])
    if feat_text:
        components.append(f"Features: {feat_text}")
    
    # Add details as structured information
    det_text = clean_details(row['details'])
    if det_text:
        components.append(f"Details: {det_text}")
    
    # Add description last as it's typically longer
    if not pd.isna(row['description']):
        components.append(f"Description: {row['description']}")
    
    # Join all components with clear separation
    return " | ".join(components)

# Example usage
def process_dataset(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Create the embedding text
    df['embedding_text'] = df.apply(prepare_text_for_embedding, axis=1)
    
    # Save the processed data
    df.to_csv(output_file, index=False)
    
    # Print a sample
    print("\nSample embedding text:")
    print(df['embedding_text'].iloc[0])
    print("\nNumber of processed rows:", len(df))

# Process the file
process_dataset('beauty_and_personal_care_metadata.csv', 'beauty_and_personal_care_metadata_processed.csv')
