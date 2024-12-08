# Import the Pinecone library
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import time
import os
import pandas as pd
import numpy as np
from tqdm import tqdm
import math

# Initialize a Pinecone client with your API key
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

def upsert_index(index, records, namespace="product-search-index"):
    try:
        # Upsert the records into the index
        index.upsert(
            vectors=records,
            namespace=namespace
        )
    except Exception as e:
        print("Skipped upserting records due to error:", e)
        pass

def create_vector_store(df, text_column, embedding_column):
    # Delete the index if it already exists
    pc.delete_index("product-search-index")

    print("Deleted existing index if it existed.")

    # Create a serverless index
    index_name = "product-search-index"

    if not pc.has_index(index_name):
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(
                cloud='aws', 
                region='us-east-1'
            ) 
        ) 

    # Wait for the index to be ready
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)
    
    print("Index created successfully!")

    # Target the index where you'll store the vector embeddings
    index = pc.Index("product-search-index")

    # Prepare the records for upsert
    # Each contains an 'id', the embedding 'values', and the original text as 'metadata'
    id = 0
    for row in tqdm(df.itertuples(), total=len(df)):
        records = [{
            "id": str(id),
            "values": row.ada_embedding, 
            "metadata": {"main_category": row.main_category,
                         "title": row.title,
                         "average_rating": row.average_rating,
                         "rating_number": row.rating_number,
                         "features": row.features,
                         "description": row.description,
                         "price": row.price,
                         "images": row.images,
                         "videos": row.videos,
                         "store": row.store,
                         "categories": row.categories,
                         "details": row.details
                         }
        }]

        upsert_index(index, records)

        id += 1

    print("Data loaded into index successful!")

if __name__ == '__main__':
    df = pd.read_csv('embedded_bpc.csv')
    df = df.fillna('')
    df['ada_embedding'] = df['ada_embedding'].apply(eval).apply(np.array)
    print("Data loaded successfully!")
    create_vector_store(df, 'embedding_text', 'ada_embedding')
