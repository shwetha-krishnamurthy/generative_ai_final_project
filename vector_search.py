import os
from get_embeddings import get_embedding
from pinecone.grpc import PineconeGRPC as Pinecone
from anthropic import Anthropic
from typing import List, Dict, Optional
import json

pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

# To get the unique host for an index, 
# see https://docs.pinecone.io/guides/data/target-an-index
index = pc.Index(host="https://product-search-index-l47ppoh.svc.aped-4627-b74a.pinecone.io")


def search_vector_db(input_text, namespace="product-search-index"):
    embedding_vector = get_embedding(input_text)
    results = index.query(
        namespace=namespace,
        vector=embedding_vector,
        top_k=5, # Return top 5 results
        include_metadata=True # Include metadata in the response.
    )

    return results


class ProductSearchBot:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.conversation_history = []
        
    def _generate_search_keywords(self, user_input: str) -> str:
        """
        Generate optimized search string based on user input using Claude.
        Returns a single string optimized for vector similarity search.
        """
        # Create the messages array without system message
        messages = [
            {
                "role": "user",
                "content": f"Generate a search string for: {user_input}"
            }
        ]
        
        # Add relevant conversation history for context
        for msg in self.conversation_history[-3:]:  # Last 3 messages
            messages.append({
                "role": "user" if msg["type"] == "user" else "assistant",
                "content": msg["content"]
            })
            
        response = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            messages=messages,
            system="You are a product search expert. Generate a clear, detailed search string based on the user's query. The output should be a single coherent string that includes key product attributes, categories, and features. Format it as natural language, not a list. Include synonyms where relevant. Focus on terms that would be useful for vector similarity search. Example input: 'I need a waterproof laptop bag for hiking' Example output: 'waterproof hiking backpack laptop compartment outdoor adventure bag water resistant computer carrier mountaineering daypack durable weather protection mobile office gear'",
            max_tokens=150,
            temperature=0.3
        )
        
        # Clean and normalize the response
        search_string = response.content[0].text.strip()
        # Remove any line breaks and normalize spaces
        search_string = ' '.join(search_string.split())

        return search_string
    
    def generate_shopping_advice(self, user_input: str, processed_results: List[Dict]) -> str:
        """
        Generate personalized shopping advice based on user query and found products.
        """
        # Prepare the product summaries for the context
        product_summaries = []
        for i, product in enumerate(processed_results, 1):
            summary = f"Product {i}: {product['title']}"
            if product['price']:
                summary += f" (${product['price']})"
            if product['rating']:
                summary += f" - {product['rating']} stars from {product['num_ratings']} reviews"
            product_summaries.append(summary)
        
        products_context = "\n".join(product_summaries)
        
        messages = [
            {
                "role": "user",
                "content": f"Based on my search for '{user_input}', analyze these products and give me personalized shopping advice:\n\n{products_context}"
            }
        ]
        
        response = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            messages=messages,
            system="You are a helpful and knowledgeable shopping assistant. Analyze the user's needs and the available products to provide personalized recommendations. Be conversational and empathetic. Explain why specific products would solve their problems. Highlight key features that match their needs. Keep the tone friendly and consultative.",
            max_tokens=400,
            temperature=0.7
        )
        
        return response.content[0].text

    def generate_product_descriptions(self, search_results: Dict) -> List[Dict]:
        """
        Generate engaging product descriptions for all matches in the search results.
        
        Args:
            search_results: Dictionary containing search matches from vector store
            
        Returns:
            List of dictionaries containing processed product information and descriptions
        """
        processed_results = []
        
        for match in search_results.get('matches', []):
            metadata = match['metadata']
            
            # Extract key product details
            product_info = {
                'id': match['id'],
                'title': metadata.get('title', ''),
                'price': metadata.get('price', ''),
                'rating': metadata.get('average_rating', 0),
                'num_ratings': metadata.get('rating_number', 0),
                'store': metadata.get('store', ''),
                'categories': eval(metadata.get('categories', '[]')),
                'features': eval(metadata.get('features', '[]')),
                'images': eval(metadata.get('images', '[]')),
                'details': eval(metadata.get('details', '{}')),
                'score': match.get('score', 0)
            }
            
            # Generate engaging description
            messages = [
                {
                    "role": "user",
                    "content": f"Generate a product description for this item, focusing on its key features and benefits: {json.dumps(metadata)}"
                }
            ]
            
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                messages=messages,
                system="You are a creative product copywriter. Generate a concise, engaging product description that highlights key features, benefits, and unique selling points. The description should be conversational and persuasive. Focus on the most relevant features for the user's search context.",
                max_tokens=200,
                temperature=0.7
            )
            
            product_info['generated_description'] = response.content[0].text
            processed_results.append(product_info)
            
        return processed_results

    def process_user_query(self, user_input: str, retrieval_function=search_vector_db) -> Dict:
        """
        Process a user query and return relevant product information.
        
        Args:
            user_input: The user's search query
            retrieval_function: Function to retrieve products based on keywords
                              Should accept str and return Dict with search matches
        
        Returns:
            Dict containing the response and processed product information
        """
        # Store user message in conversation history
        self.conversation_history.append({
            "type": "user",
            "content": user_input
        })
        
        # Generate search string
        search_string = self._generate_search_keywords(user_input)
        
        # Retrieve product data using provided function
        search_results = retrieval_function(search_string)
        
        if not search_results.get('matches'):
            response = {
                "found": False,
                "message": "I couldn't find any products matching your description. Could you please provide more details or try different search terms?"
            }
            # Store bot response in conversation history
            self.conversation_history.append({
                "type": "assistant",
                "content": response["message"]
            })
            return response
            
        # Process results and generate descriptions
        processed_results = self.generate_product_descriptions(search_results)
        
        # Generate personalized shopping advice
        shopping_advice = self.generate_shopping_advice(user_input, processed_results)
        
        # Store bot response in conversation history
        self.conversation_history.append({
            "type": "assistant",
            "content": shopping_advice
        })
        
        return {
            "found": True,
            "shopping_advice": shopping_advice,
            "results": processed_results,
            "total_results": len(processed_results)
        }

    def clear_conversation(self):
        """Reset the conversation history."""
        self.conversation_history = []


if __name__ == "__main__":
    # Example usage
    bot = ProductSearchBot(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    # Example search
    result = bot.process_user_query(
        "I'm looking for something for the strand like thing on top of my head so that it doesn't feel like a bird's nest."
    )
    
    print(json.dumps(result, indent=2))
