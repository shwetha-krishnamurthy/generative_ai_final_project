# import streamlit as st
# import json
# import os
# from vector_search import ProductSearchBot  # Import your backend class
# from typing import Dict, Any

# st.set_page_config(layout="wide")

#     # Initialize session state
# if 'shopping_cart' not in st.session_state:
#     st.session_state.shopping_cart = []
# if 'search_results' not in st.session_state:
#     st.session_state.search_results = None
# if 'last_search_query' not in st.session_state:
#     st.session_state.last_search_query = None

# def display_product_card(product: Dict[str, Any]):
#     """Display a product card with image and details"""
#     with st.container():
#         col1, col2 = st.columns([1, 2])
        
#         with col1:
#             # Display the main product image
#             if product['images'] and len(product['images']) > 0:
#                 main_image = product['images'][0].get('large', '')
#                 if main_image:
#                     st.image(main_image, use_container_width=True)
                    
#                 # Create a horizontal layout for thumbnail images
#                 if len(product['images']) > 1:
#                     thumbnail_cols = st.columns(min(4, len(product['images'])-1))
#                     for idx, thumb_col in enumerate(thumbnail_cols):
#                         if idx + 1 < len(product['images']):
#                             thumb_image = product['images'][idx+1].get('thumb', '')
#                             if thumb_image:
#                                 thumb_col.image(thumb_image, use_container_width=True)
        
#         with col2:
#             st.subheader(product['title'])
            
#             # Price and ratings in the same line
#             col_price, col_rating = st.columns(2)
#             with col_price:
#                 if product['price']:
#                     st.write(f"💰 Price: ${product['price']}")
#                 else:
#                     st.write("💰 Price: Not available")
            
#             with col_rating:
#                 if product['rating']:
#                     st.write(f"⭐ Rating: {product['rating']} ({product['num_ratings']} reviews)")
            
#             # Store name
#             if product['store']:
#                 st.write(f"🏪 Seller: {product['store']}")
            
#             # Features in an expandable section
#             if product['features']:
#                 with st.expander("📋 Product Features"):
#                     for feature in product['features']:
#                         st.write(f"• {feature}")
            
#             # Product details in an expandable section
#             if product['details']:
#                 with st.expander("ℹ️ Product Details"):
#                     for key, value in product['details'].items():
#                         st.write(f"**{key}:** {value}")
            
#             # Add to cart functionality
#             cart_key = f"in_cart_{product['id']}"  # Changed key prefix to avoid conflict
#             if cart_key not in st.session_state:
#                 st.session_state[cart_key] = False
                
#             if st.button(f"🛒 Add to Cart", key=f"add_{product['id']}"):
#                 st.session_state.shopping_cart.append({
#                     'id': product['id'],
#                     'title': product['title'],
#                     'price': product['price']
#                 })
#                 st.session_state[cart_key] = True
                
#             # Show success message if item was just added
#             if st.session_state[cart_key]:
#                 st.success("Added to cart!")
#                 # Reset the state after showing the message
#                 st.session_state[cart_key] = False

# def main():
#     st.title("🛍️ AI Shopping Assistant")
    
#     # Initialize the bot (you'll need to add your API key)
#     bot = ProductSearchBot(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
#     # Search interface
#     with st.form("search_form"):
#         user_query = st.text_input("What are you looking for?")
#         search_button = st.form_submit_button("🔍 Search")
    
#     # Display shopping cart in sidebar
#     with st.sidebar:
#         st.header("🛒 Shopping Cart")
#         if not st.session_state.shopping_cart:
#             st.write("Your cart is empty")
#         else:
#             for item in st.session_state.shopping_cart:
#                 st.write(f"• {item['title']}")
#                 if item['price']:
#                     st.write(f"  ${item['price']}")
            
#             if st.button("Clear Cart"):
#                 st.session_state.shopping_cart = []
#                 st.success("Cart cleared!")
    
#     # Process search when button is clicked
#     if search_button and user_query:
#         if user_query != st.session_state.last_search_query:
#             with st.spinner("🔍 Searching for products..."):
#                 # Replace this with your actual retrieval function
#                 def mock_retrieval_function(search_string):
#                     # This is where you'll implement your vector store query
#                     pass
                
#                 results = bot.process_user_query(user_query)
#                 st.session_state.search_results = results
#                 st.session_state.last_search_query = user_query

#     # Display results if they exist in session state
#     if st.session_state.search_results:
#         results = st.session_state.search_results
#         if results['found']:
#             # Display shopping advice
#             st.markdown("### 🤖 Shopping Assistant Advice")
#             st.write(results['shopping_advice'])
            
#             # Display products
#             st.markdown("### 📦 Found Products")
#             for product in results['results']:
#                 with st.container():
#                     display_product_card(product)
#                     st.divider()
#         else:
#             st.warning("No products found. Try different search terms!")

# if __name__ == "__main__":
#     main()

import streamlit as st
import json
import os
from vector_search import ProductSearchBot  # Import your backend class
from typing import Dict, Any

st.set_page_config(layout="wide")

    # Initialize session state
if 'shopping_cart' not in st.session_state:
    st.session_state.shopping_cart = []
if 'search_results' not in st.session_state:
    st.session_state.search_results = None
if 'last_search_query' not in st.session_state:
    st.session_state.last_search_query = None

def display_product_card(product: Dict[str, Any]):
    """Display a product card with image and details"""
    with st.container():
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Display the main product image
            if product['images'] and len(product['images']) > 0:
                main_image = product['images'][0].get('large', '')
                if main_image:
                    st.image(main_image, use_container_width=True)
                    
                # Create a horizontal layout for thumbnail images
                if len(product['images']) > 1:
                    thumbnail_cols = st.columns(min(4, len(product['images'])-1))
                    for idx, thumb_col in enumerate(thumbnail_cols):
                        if idx + 1 < len(product['images']):
                            thumb_image = product['images'][idx+1].get('thumb', '')
                            if thumb_image:
                                thumb_col.image(thumb_image, use_container_width=True)
        
        with col2:
            st.subheader(product['title'])
            
            # Price and ratings in the same line
            col_price, col_rating = st.columns(2)
            with col_price:
                if product['price']:
                    st.write(f"💰 Price: ${product['price']}")
                else:
                    st.write("💰 Price: Not available")
            
            with col_rating:
                if product['rating']:
                    st.write(f"⭐ Rating: {product['rating']} ({product['num_ratings']} reviews)")
            
            # Store name
            if product['store']:
                st.write(f"🏪 Seller: {product['store']}")
            
            # Features in an expandable section
            if product['features']:
                with st.expander("📋 Product Features"):
                    for feature in product['features']:
                        st.write(f"• {feature}")
            
            # Product details in an expandable section
            if product['details']:
                with st.expander("ℹ️ Product Details"):
                    for key, value in product['details'].items():
                        st.write(f"**{key}:** {value}")
            
            # Add to cart functionality
            cart_key = f"in_cart_{product['id']}"
            if cart_key not in st.session_state:
                st.session_state[cart_key] = False
                
            if st.button(f"🛒 Add to Cart", key=f"add_{product['id']}"):
                st.session_state.shopping_cart.append({
                    'id': product['id'],
                    'title': product['title'],
                    'price': product['price']
                })
                st.session_state[cart_key] = True
                st.rerun()  # Force sidebar to update
                
            # Show success message if item was just added
            if st.session_state[cart_key]:
                st.success("Added to cart!")
                st.session_state[cart_key] = False

def main():
    st.title("🛍️ AI Shopping Assistant")
    
    # Initialize the bot (you'll need to add your API key)
    bot = ProductSearchBot(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    # Search interface
    with st.form("search_form"):
        user_query = st.text_input("What are you looking for?")
        search_button = st.form_submit_button("🔍 Search")
    
    # Display shopping cart in sidebar
    with st.sidebar:
        st.header("🛒 Shopping Cart")
        if not st.session_state.shopping_cart:
            st.write("Your cart is empty")
        else:
            total = 0
            for idx, item in enumerate(st.session_state.shopping_cart, 1):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"{idx}. {item['title'][:50]}...")  # Truncate long titles
                with col2:
                    if item['price']:
                        st.write(f"${item['price']}")
                        total += float(item['price'])
            
            st.divider()
            if total > 0:
                st.write(f"Total: ${total:.2f}")
            
            if st.button("🗑️ Clear Cart"):
                st.session_state.shopping_cart = []
                st.success("Cart cleared!")
                st.rerun()
    
    # Process search when button is clicked
    if search_button and user_query:
        if user_query != st.session_state.last_search_query:
            with st.spinner("🔍 Searching for products..."):
                
                results = bot.process_user_query(user_query)
                st.session_state.search_results = results
                st.session_state.last_search_query = user_query

    # Display results if they exist in session state
    if st.session_state.search_results:
        results = st.session_state.search_results
        if results['found']:
            # Display shopping advice
            st.markdown("### 🤖 Shopping Assistant Advice")
            st.write(results['shopping_advice'])
            
            # Display products
            st.markdown("### 📦 Found Products")
            for product in results['results']:
                with st.container():
                    display_product_card(product)
                    st.divider()
        else:
            st.warning("No products found. Try different search terms!")

if __name__ == "__main__":
    main()
