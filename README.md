# Analytics Chatbot 🤖

An intelligent chatbot that analyzes datasets (CSV files) and provides insights, visualizations, and summaries using Google's Gemini AI and LangChain.

## Features

- 📊 **Automatic Data Analysis**: Load any CSV file and get instant insights
- 💬 **Interactive Chat**: Ask questions about your data in natural language
- 📈 **Visualizations**: Automatically generates plots and charts
- 🔍 **Smart Insights**: Uses Gemini AI to identify patterns, trends, and anomalies
- 🛠️ **Easy Setup**: Simple configuration with API key

## Prerequisites

- Python 3.8 or higher
- Gemini API key (get it from [Google AI Studio](https://makersuite.google.com/app/apikey))

## Installation

1. **Clone or download this repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Gemini API key**:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and replace `your_gemini_api_key_here` with your actual Gemini API key

## Usage

### Basic Usage

Run the chatbot with a CSV file:

```bash
python app.py path/to/your/data.csv
```

This will:
1. Load the dataset
2. Generate an automatic analysis
3. Create visualizations (saved in `plots/` directory)
4. Enter interactive chat mode

### Interactive Mode

Run without arguments for interactive mode:

```bash
python app.py
```

Commands:
- `load <file_path>` - Load a CSV file
- `analyze` - Get automatic analysis
- `plots` - Generate visualizations
- Ask any question about your data
- `exit` - Quit

### Example

```bash
python app.py sales_data.csv
```

Then in chat mode:
```
You: What are the top 5 products by sales?
You: Show me trends over time
You: Are there any outliers in the data?
```

## Project Structure

```
analytics-chatbot/
├── app.py                 # Main application entry point
├── analytics_chatbot.py   # Core chatbot class with Gemini integration
├── data_loader.py         # CSV loading and preprocessing utilities
├── visualizer.py          # Visualization generation
├── config.py              # Configuration and API key management
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment file
├── .env                  # Your API key (create this file)
└── README.md             # This file
```

## Configuration

### API Key Location

Put your Gemini API key in the `.env` file:

```
GEMINI_API_KEY=your_actual_api_key_here
```

The `config.py` file automatically loads this key. Make sure `.env` is in your `.gitignore` if you're using version control!

## How It Works

1. **Data Loading**: Reads CSV files using pandas
2. **Data Summary**: Generates statistical summaries and metadata
3. **AI Analysis**: Uses LangChain with Gemini to analyze the data
4. **Visualizations**: Creates various plots (distributions, correlations, etc.)
5. **Interactive Chat**: Allows natural language queries about the data

## Dependencies

- `langchain` - LLM framework
- `langchain-google-genai` - Gemini integration for LangChain
- `google-generativeai` - Google's Gemini API
- `pandas` - Data manipulation
- `matplotlib` - Plotting
- `seaborn` - Statistical visualizations
- `python-dotenv` - Environment variable management

## Troubleshooting

### API Key Issues

If you see an error about the API key:
1. Make sure you created a `.env` file
2. Check that your API key is correct
3. Verify the key has proper permissions

### Import Errors

If you get import errors, make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### File Not Found

Make sure the CSV file path is correct. Use absolute paths if needed:
```bash
python app.py /full/path/to/data.csv
```

## License

This project is open source and available for personal and commercial use.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests!

