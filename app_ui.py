"""
Streamlit Web UI for Analytics Chatbot
"""
import streamlit as st
import pandas as pd
import os
import tempfile
from pathlib import Path
from PIL import Image
from analytics_chatbot import AnalyticsChatbot
from visualizer import PLOT_TYPES, create_visualizations
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Analytics Chatbot",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stButton>button {
        width: 100%;
        border-radius: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = None
if 'df' not in st.session_state:
    st.session_state.df = None
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'analysis' not in st.session_state:
    st.session_state.analysis = None
if 'plot_paths' not in st.session_state:
    st.session_state.plot_paths = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


def load_data_from_file(uploaded_file):
    """Load data from uploaded file."""
    try:
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        # Initialize chatbot if not already done
        if st.session_state.chatbot is None:
            st.session_state.chatbot = AnalyticsChatbot()
        
        # Load data
        st.session_state.chatbot.load_data(tmp_path)
        st.session_state.df = st.session_state.chatbot.df
        st.session_state.data_loaded = True
        st.session_state.analysis = None
        st.session_state.plot_paths = []
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        return True
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return False


def main():
    # Header
    st.markdown('<h1 class="main-header">Analytics Chatbot</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("Data Upload")
        
        uploaded_file = st.file_uploader(
            "Upload a CSV file",
            type=['csv'],
            help="Select a CSV file to analyze"
        )
        
        if uploaded_file is not None:
            if st.button("Load Dataset", type="primary"):
                with st.spinner("Loading dataset..."):
                    if load_data_from_file(uploaded_file):
                        st.success("Dataset loaded successfully!")
                        st.rerun()
        
        st.markdown("---")
        
        # Data info
        if st.session_state.data_loaded and st.session_state.df is not None:
            st.header("Dataset Info")
            df = st.session_state.df
            st.metric("Rows", f"{df.shape[0]:,}")
            st.metric("Columns", df.shape[1])
            st.metric("Numeric Columns", len(df.select_dtypes(include=[np.number]).columns))
            st.metric("Categorical Columns", len(df.select_dtypes(include=['object', 'category']).columns))
            
            if st.button("Clear Data"):
                st.session_state.data_loaded = False
                st.session_state.df = None
                st.session_state.chatbot = None
                st.session_state.analysis = None
                st.session_state.plot_paths = []
                st.session_state.chat_history = []
                st.rerun()
    
    # Main content area
    if not st.session_state.data_loaded:
        # Welcome screen
        col1, col2, _ = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 2rem;">
                <h2>Welcome to Analytics Chatbot</h2>
                <p style="font-size: 1.2rem; color: #666;">
                    Upload a CSV file to get started with AI-powered data analysis
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            ### Features:
            - **Automatic Data Analysis** - Get instant insights from your data
            - **Interactive Visualizations** - Choose which plots to generate
            - **AI Chat Assistant** - Ask questions about your data
            - **Smart Insights** - Discover patterns and trends
            """)
    else:
        # Main tabs
        tab1, tab2, tab3, tab4 = st.tabs(["Data Preview", "Visualizations", "AI Analysis", "Chat"])
        
        df = st.session_state.df
        
        # Tab 1: Data Preview
        with tab1:
            st.header("Data Preview")
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("First 10 Rows")
                st.dataframe(df.head(10), use_container_width=True)
            
            with col2:
                st.subheader("Dataset Summary")
                st.dataframe(df.describe(), use_container_width=True)
            
            st.subheader("Data Types & Info")
            info_df = pd.DataFrame({
                'Column': df.columns,
                'Type': [str(dtype) for dtype in df.dtypes],
                'Non-Null Count': df.count().values,
                'Null Count': df.isnull().sum().values
            })
            st.dataframe(info_df, use_container_width=True)
        
        # Tab 2: Visualizations
        with tab2:
            st.header("Generate Visualizations")
            
            if df is not None:
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
                
                st.subheader("Select Plot Types")
                
                # Calculate plot counts
                plot_counts = {}
                plot_counts['distribution'] = min(len(numeric_cols), 5) if numeric_cols else 0
                plot_counts['correlation'] = 1 if len(numeric_cols) > 1 else 0
                plot_counts['boxplot'] = min(len(numeric_cols), 5) if numeric_cols else 0
                plot_counts['countplot'] = min(len(categorical_cols), 5) if categorical_cols else 0
                
                # Create plot selection checkboxes
                col1, col2 = st.columns(2)
                
                with col1:
                    plot_types = []
                    for i, (key, description) in enumerate(PLOT_TYPES.items()):
                        count_info = ""
                        if plot_counts[key] > 0:
                            count_info = f" (~{plot_counts[key]} plots)"
                        else:
                            count_info = " (0 plots - no suitable columns)"
                        
                        if st.checkbox(
                            f"**{key.upper()}**",
                            value=False,
                            help=f"{description}{count_info}"
                        ):
                            plot_types.append(key)
                
                with col2:
                    st.info("""
                    **Plot Types:**
                    - **Distribution**: Histograms for numeric columns
                    - **Correlation**: Heatmap showing correlations
                    - **Boxplot**: Box plots for numeric columns
                    - **Countplot**: Bar charts for categorical columns
                    """)
                
                if st.button("Generate Visualizations", type="primary"):
                    if plot_types:
                        with st.spinner("Generating visualizations..."):
                            try:
                                # Create plots directory
                                output_dir = "plots"
                                os.makedirs(output_dir, exist_ok=True)
                                
                                # Generate visualizations
                                plot_paths = create_visualizations(
                                    df, 
                                    output_dir=output_dir,
                                    plot_types=set(plot_types)
                                )
                                
                                st.session_state.plot_paths = plot_paths
                                st.success(f"Generated {len(plot_paths)} visualizations!")
                            except Exception as e:
                                st.error(f"Error generating visualizations: {str(e)}")
                    else:
                        st.warning("Please select at least one plot type.")
                
                # Display generated plots
                if st.session_state.plot_paths:
                    st.markdown("---")
                    st.subheader("Generated Visualizations")
                    
                    for plot_path in st.session_state.plot_paths:
                        if os.path.exists(plot_path):
                            st.image(plot_path, caption=os.path.basename(plot_path))
        
        # Tab 3: AI Analysis
        with tab3:
            st.header("AI-Powered Analysis")
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                query = st.text_input(
                    "Ask a specific question (optional)",
                    placeholder="e.g., What are the key trends in this data?",
                    help="Leave empty for a general analysis"
                )
            
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)  # Spacing
                analyze_button = st.button("Analyze", type="primary", use_container_width=True)
            
            if analyze_button:
                with st.spinner("AI is analyzing your data..."):
                    try:
                        if query:
                            analysis = st.session_state.chatbot.analyze(query=query)
                        else:
                            analysis = st.session_state.chatbot.analyze()
                        
                        st.session_state.analysis = analysis
                    except Exception as e:
                        st.error(f"Error during analysis: {str(e)}")
            
            # Display analysis
            if st.session_state.analysis:
                st.markdown("---")
                st.markdown("### Analysis Results")
                st.markdown(st.session_state.analysis)
        
        # Tab 4: Chat
        with tab4:
            st.header("Chat with AI Assistant")
            
            # Display chat history
            if st.session_state.chat_history:
                st.markdown("### Conversation History")
                for i, (role, message) in enumerate(st.session_state.chat_history):
                    with st.chat_message(role):
                        st.markdown(message)
            
            # Chat input
            user_input = st.chat_input("Ask a question about your data...")
            
            if user_input:
                # Add user message to history
                st.session_state.chat_history.append(("user", user_input))
                
                # Get AI response
                with st.spinner("Thinking..."):
                    try:
                        response = st.session_state.chatbot.chat(user_input)
                        st.session_state.chat_history.append(("assistant", response))
                    except Exception as e:
                        error_msg = f"Error: {str(e)}"
                        st.session_state.chat_history.append(("assistant", error_msg))
                
                st.rerun()


if __name__ == "__main__":
    main()

