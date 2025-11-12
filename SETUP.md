# Quick Setup Guide

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Get Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

## Step 3: Create .env File

Create a file named `.env` in the project root directory with the following content:

```
GEMINI_API_KEY=your_actual_api_key_here
```

Replace `your_actual_api_key_here` with the API key you copied in Step 2.

**Important**: Never commit your `.env` file to version control! It's already in `.gitignore`.

## Step 4: Test It Out

Run the chatbot with a CSV file:

```bash
python app.py your_data.csv
```

Or run in interactive mode:

```bash
python app.py
```

## Troubleshooting

### "GEMINI_API_KEY not found" Error

- Make sure you created a `.env` file (not `.env.example`)
- Check that the file is in the project root directory
- Verify the API key is correct (no extra spaces or quotes)

### Import Errors

If you get import errors, try:

```bash
pip install --upgrade -r requirements.txt
```

### API Key Invalid

- Make sure you copied the entire API key
- Check that the API key hasn't expired
- Verify you're using the correct API key from Google AI Studio

