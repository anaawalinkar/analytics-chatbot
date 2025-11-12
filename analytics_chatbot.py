"""
Analytics Chatbot using LangChain and Gemini API.
"""
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Optional, List
import config
from data_loader import get_data_summary, get_data_info
from visualizer import create_visualizations


class AnalyticsChatbot:
    """
    A chatbot that analyzes datasets and provides insights using Gemini AI.
    """
    
    def __init__(self):
        """Initialize the chatbot with Gemini API."""
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=config.GEMINI_API_KEY,
            temperature=0.7
        )
        self.df: Optional[pd.DataFrame] = None
        self.data_summary: Optional[str] = None
        self.data_info: Optional[dict] = None
    
    def load_data(self, file_path: str):
        """
        Load a CSV file for analysis.
        
        Args:
            file_path: Path to the CSV file
        """
        from data_loader import load_csv
        self.df = load_csv(file_path)
        self.data_summary = get_data_summary(self.df)
        self.data_info = get_data_info(self.df)
        print(f"✓ Loaded dataset: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
    
    def analyze(self, query: str = None) -> str:
        """
        Analyze the loaded dataset and provide insights.
        
        Args:
            query: Optional specific question about the data
            
        Returns:
            Analysis and insights as a string
        """
        if self.df is None:
            return "Please load a dataset first using load_data()"
        
        # Create the system prompt
        system_prompt = """You are an expert data analyst. Your task is to analyze datasets and provide 
        insightful, actionable observations. When analyzing data:
        1. Identify key patterns, trends, and anomalies
        2. Highlight important statistics and correlations
        3. Point out data quality issues (missing values, outliers, etc.)
        4. Suggest potential insights or business implications
        5. Be concise but comprehensive
        6. Use clear, professional language
        
        You will be given a dataset summary. Analyze it thoroughly and provide your insights."""
        
        # Prepare the data context
        data_context = f"""
        Dataset Summary:
        {self.data_summary}
        
        Dataset Information:
        - Shape: {self.data_info['shape']}
        - Columns: {', '.join(self.data_info['columns'])}
        - Numeric columns: {', '.join(self.data_info['numeric_columns']) if self.data_info['numeric_columns'] else 'None'}
        - Categorical columns: {', '.join(self.data_info['categorical_columns']) if self.data_info['categorical_columns'] else 'None'}
        """
        
        # Create the user message
        if query:
            user_message = f"{data_context}\n\nUser Question: {query}\n\nPlease answer the question based on the dataset."
        else:
            user_message = f"{data_context}\n\nPlease provide a comprehensive analysis of this dataset, including key insights, patterns, and recommendations."
        
        # Get response from Gemini
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message)
        ]
        
        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            return f"Error generating analysis: {str(e)}"
    
    def generate_visualizations(self, output_dir: str = "plots") -> List[str]:
        """
        Generate visualizations for the loaded dataset.
        
        Args:
            output_dir: Directory to save plots
            
        Returns:
            List of paths to generated plot files
        """
        if self.df is None:
            raise ValueError("Please load a dataset first using load_data()")
        
        return create_visualizations(self.df, output_dir)
    
    def chat(self, user_input: str) -> str:
        """
        Interactive chat mode for asking questions about the data.
        
        Args:
            user_input: User's question or request
            
        Returns:
            Response from the chatbot
        """
        if self.df is None:
            return "Please load a dataset first using load_data()"
        
        system_prompt = """You are a helpful data analyst assistant. You have access to a dataset and can answer 
        questions about it, provide insights, suggest analyses, and help interpret the data. Be conversational 
        but professional."""
        
        data_context = f"""
        Dataset Summary:
        {self.data_summary}
        
        Dataset Information:
        - Shape: {self.data_info['shape']}
        - Columns: {', '.join(self.data_info['columns'])}
        - Numeric columns: {', '.join(self.data_info['numeric_columns']) if self.data_info['numeric_columns'] else 'None'}
        - Categorical columns: {', '.join(self.data_info['categorical_columns']) if self.data_info['categorical_columns'] else 'None'}
        """
        
        user_message = f"{data_context}\n\nUser: {user_input}\n\nAssistant:"
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message)
        ]
        
        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            return f"Error: {str(e)}"

