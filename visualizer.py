"""
Visualization generation utilities.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from typing import List, Optional, Set
import numpy as np

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Available plot types
PLOT_TYPES = {
    'distribution': 'Distribution plots (histograms) - one plot per numeric column (up to 5 columns)',
    'correlation': 'Correlation heatmap - single plot showing correlations between all numeric columns',
    'boxplot': 'Box plots - one plot per numeric column (up to 5 columns)',
    'countplot': 'Count plots (bar charts) - one plot per categorical column (up to 5 columns)'
}


def get_plot_type_selection(df: Optional[pd.DataFrame] = None) -> Set[str]:
    """
    Interactive multiple choice menu for selecting plot types.
    
    Args:
        df: Optional DataFrame to analyze and show plot counts
    
    Returns:
        Set of selected plot type keys
    """
    print("\n" + "=" * 60)
    print("Select Plot Types")
    print("=" * 60)
    print("Choose which types of plots you want to generate:")
    print()
    
    # Analyze dataset if provided to show plot counts
    numeric_cols = []
    categorical_cols = []
    if df is not None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Display options with counts
    plot_keys = list(PLOT_TYPES.keys())
    for i, (key, description) in enumerate(PLOT_TYPES.items(), 1):
        count_str = ""
        if df is not None:
            # Calculate how many plots this type will generate
            if key in ['distribution', 'boxplot']:
                count = min(len(numeric_cols), 5)
                count_str = f" (~{count} plots)" if count > 1 else ""
            elif key == 'correlation':
                count_str = " (1 plot)" if len(numeric_cols) > 1 else " (0 plots - requires 2+ numeric columns)"
            elif key == 'countplot':
                count = min(len(categorical_cols), 5)
                count_str = f" (~{count} plots)" if count > 1 else ""
        print(f"  {i}. {key.upper()}: {description}{count_str}")
    
    print(f"  {len(PLOT_TYPES) + 1}. ALL: Generate all plot types")
    print("  0. Cancel")
    print()
    
    while True:
        try:
            selection = input("Enter your choices (comma-separated numbers, e.g., 1,2,3): ").strip()
            
            if not selection:
                print("Please enter at least one choice.")
                continue
            
            # Check if user wants all
            if selection == str(len(PLOT_TYPES) + 1):
                return set(PLOT_TYPES.keys())
            
            # Check if user wants to cancel
            if selection == '0':
                return set()
            
            # Parse selections
            choices = [c.strip() for c in selection.split(',')]
            selected_keys = set()
            
            for choice in choices:
                choice_num = int(choice)
                if choice_num < 1 or choice_num > len(PLOT_TYPES):
                    print(f"Invalid choice: {choice_num}. Please enter numbers between 1 and {len(PLOT_TYPES) + 1}.")
                    break
                selected_keys.add(plot_keys[choice_num - 1])
            else:
                # All choices were valid
                if selected_keys:
                    return selected_keys
                else:
                    print("Please select at least one plot type.")
                    
        except ValueError:
            print("Invalid input. Please enter comma-separated numbers.")
        except KeyboardInterrupt:
            print("\n\nCancelled.")
            return set()


def create_visualizations(df: pd.DataFrame, output_dir: str = "plots", plot_types: Optional[Set[str]] = None) -> List[str]:
    """
    Generate various visualizations for the dataset.
    
    Args:
        df: pandas DataFrame
        output_dir: Directory to save plots
        plot_types: Set of plot types to generate. If None, generates all plot types.
                    Valid values: 'distribution', 'correlation', 'boxplot', 'countplot'
        
    Returns:
        List of file paths to generated plots
    """
    os.makedirs(output_dir, exist_ok=True)
    plot_paths = []
    
    # If plot_types is None, generate all plots (backward compatibility)
    if plot_types is None:
        plot_types = set(PLOT_TYPES.keys())
    
    # If empty set, return empty list
    if not plot_types:
        return plot_paths
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # 1. Distribution plots for numeric columns
    if 'distribution' in plot_types:
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
    if 'correlation' in plot_types and len(numeric_cols) > 1:
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
    if 'boxplot' in plot_types:
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
    if 'countplot' in plot_types:
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

