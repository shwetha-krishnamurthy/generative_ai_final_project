# AI Shopping Assistant

An intelligent shopping assistant powered by Claude Sonnet that helps users find products through natural conversation and provides personalized recommendations.

## Demo

<!-- Choose one of these options based on your video format: -->

![Demo](GenAI-Final-Project-Video.gif)

[Insert screenshot of main interface here - showing search bar and assistant's response]

## Features

### 🤖 AI-Powered Search
- Natural language understanding for product searches
- Personalized shopping advice based on user needs
- Context-aware recommendations
- Vector similarity search for accurate product matching

### 📦 Smart Product Display
- Visual product galleries with main images and thumbnails
- Detailed product information including:
  - Prices and ratings
  - Product features
  - Technical specifications
  - Seller information
- Expandable sections for additional details

[Insert screenshot of product display here - showing product cards with images and details]

### 🛒 Shopping Cart Management
- Real-time cart updates
- Running total calculation
- Easy cart management
- Clear cart functionality
- Persistent cart across searches

[Insert screenshot of shopping cart sidebar here]

## Technical Architecture

### Backend Components
1. **Product Search Bot**
   - Anthropic's Claude API integration
   - Vector store querying
   - Keyword optimization
   - Multi-turn conversation handling

2. **Vector Search**
   - Embedding-based similarity search
   - Product metadata processing
   - Relevance scoring

### Frontend Components (Streamlit)
1. **Search Interface**
   - Real-time query processing
   - Loading state management
   - Error handling

2. **Product Display**
   - Responsive grid layout
   - Image gallery management
   - Dynamic content expansion

3. **Shopping Cart**
   - Session state management
   - Cart persistence
   - Total calculation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-shopping-assistant.git
cd ai-shopping-assistant
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

4. Run the application:
```bash
streamlit run app.py
```

## Configuration

### API Setup
1. Obtain an API key from Anthropic
2. Configure the vector store connection
3. Set up product database access

### Customization
The application can be customized through several configuration options:
- Model selection (default: Claude 3 Sonnet)
- Number of search results
- Product display format
- Cart behavior

## Usage

1. **Starting a Search**
   - Enter your product requirements in natural language
   - The AI assistant will analyze your needs and search for relevant products

2. **Browsing Products**
   - Review the AI's shopping advice
   - Browse through product cards
   - Expand sections for more details
   - View product images

3. **Managing Cart**
   - Add products to cart with one click
   - Review cart contents in the sidebar
   - Clear cart as needed
   - View running total

## Development

### Project Structure
```
ai-shopping-assistant/
├── app.py                 # Streamlit frontend
├── product_search_bot.py  # Backend logic
├── requirements.txt       # Dependencies
├── README.md             # Documentation
└── config/               # Configuration files
```

### Key Components
1. `ProductSearchBot`: Handles AI interactions and search
2. `process_user_query`: Manages query processing and results
3. `display_product_card`: Handles product visualization
4. `generate_shopping_advice`: Creates personalized recommendations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Anthropic's Claude API for AI capabilities
- Streamlit for the frontend framework
- [Add any other libraries or resources used]
