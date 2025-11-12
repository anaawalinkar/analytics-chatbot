"""
Data loading and preprocessing utilities.
"""
import pandas as pd
import os
from typing import Optional


def load_csv(file_path: str) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        pandas DataFrame
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        raise ValueError(f"Error loading CSV file: {str(e)}")


def get_data_summary(df: pd.DataFrame) -> str:
    """
    Generate a text summary of the dataset.
    
    Args:
        df: pandas DataFrame
        
    Returns:
        String summary of the dataset
    """
    summary = []
    summary.append(f"Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns\n")
    summary.append("\nColumn Information:")
    summary.append(df.info())
    summary.append("\n\nFirst few rows:")
    summary.append(df.head().to_string())
    summary.append("\n\nBasic Statistics:")
    summary.append(df.describe().to_string())
    summary.append("\n\nMissing Values:")
    summary.append(df.isnull().sum().to_string())
    
    return "\n".join([str(s) for s in summary])


def get_data_info(df: pd.DataFrame) -> dict:
    """
    Get structured information about the dataset.
    
    Args:
        df: pandas DataFrame
        
    Returns:
        Dictionary with dataset information
    """
    return {
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "dtypes": df.dtypes.to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "numeric_columns": df.select_dtypes(include=['number']).columns.tolist(),
        "categorical_columns": df.select_dtypes(include=['object', 'category']).columns.tolist(),
    }

