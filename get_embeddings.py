from openai import OpenAI, OpenAIError
import pandas as pd

client = OpenAI()

def get_embedding(text, model="text-embedding-3-small"):
    embedding_dimension = 1536
    default_embedding = [0.0] * embedding_dimension
    try:
        text = text.replace("\n", " ")
        response = client.embeddings.create(input = [text], model=model)
        return response.data[0].embedding
    except OpenAIError as e:
        # Check if it's a token length error or something else
        # If it's the maximum context length error, return the default vector
        if "maximum context length" in str(e):
            return default_embedding
        else:
            # For other errors, you might also choose to return default
            # or handle differently
            return default_embedding

if __name__ == '__main__':
   df = pd.read_csv('beauty_and_personal_care_metadata_processed.csv')
   df['ada_embedding'] = df['embedding_text'].apply(lambda x: get_embedding(x, model='text-embedding-3-small'))
   df.to_csv('embedded_bpc.csv', index=False)
