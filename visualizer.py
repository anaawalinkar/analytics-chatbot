"""
Visualization generation utilities.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from typing import List, Optional
import numpy as np

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


def create_visualizations(df: pd.DataFrame, output_dir: str = "plots") -> List[str]:
    """
    Generate various visualizations for the dataset.
    
    Args:
        df: pandas DataFrame
        output_dir: Directory to save plots
        
    Returns:
        List of file paths to generated plots
    """
    os.makedirs(output_dir, exist_ok=True)
    plot_paths = []
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # 1. Distribution plots for numeric columns
    for col in numeric_cols[:5]:  # Limit to first 5 numeric columns
        try:
            plt.figure(figsize=(10, 6))
            df[col].hist(bins=30, edgecolor='black')
            plt.title(f'Distribution of {col}')
            plt.xlabel(col)
            plt.ylabel('Frequency')
            path = os.path.join(output_dir, f'distribution_{col}.png')
            plt.savefig(path, dpi=150, bbox_inches='tight')
            plt.close()
            plot_paths.append(path)
        except Exception as e:
            print(f"Error creating distribution plot for {col}: {e}")
    
    # 2. Correlation heatmap if multiple numeric columns
    if len(numeric_cols) > 1:
        try:
            plt.figure(figsize=(12, 10))
            correlation_matrix = df[numeric_cols].corr()
            sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0)
            plt.title('Correlation Heatmap')
            path = os.path.join(output_dir, 'correlation_heatmap.png')
            plt.savefig(path, dpi=150, bbox_inches='tight')
            plt.close()
            plot_paths.append(path)
        except Exception as e:
            print(f"Error creating correlation heatmap: {e}")
    
    # 3. Box plots for numeric columns
    for col in numeric_cols[:5]:
        try:
            plt.figure(figsize=(10, 6))
            df.boxplot(column=col)
            plt.title(f'Box Plot of {col}')
            plt.ylabel(col)
            path = os.path.join(output_dir, f'boxplot_{col}.png')
            plt.savefig(path, dpi=150, bbox_inches='tight')
            plt.close()
            plot_paths.append(path)
        except Exception as e:
            print(f"Error creating box plot for {col}: {e}")
    
    # 4. Count plots for categorical columns
    for col in categorical_cols[:5]:
        try:
            plt.figure(figsize=(12, 6))
            value_counts = df[col].value_counts().head(10)
            value_counts.plot(kind='bar')
            plt.title(f'Top 10 Values in {col}')
            plt.xlabel(col)
            plt.ylabel('Count')
            plt.xticks(rotation=45, ha='right')
            path = os.path.join(output_dir, f'countplot_{col}.png')
            plt.savefig(path, dpi=150, bbox_inches='tight')
            plt.close()
            plot_paths.append(path)
        except Exception as e:
            print(f"Error creating count plot for {col}: {e}")
    
    return plot_paths

