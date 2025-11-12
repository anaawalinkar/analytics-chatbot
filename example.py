"""
Example script showing how to use the Analytics Chatbot programmatically.
"""
from analytics_chatbot import AnalyticsChatbot


def example_usage():
    """Example of using the chatbot programmatically."""
    
    # Initialize the chatbot
    chatbot = AnalyticsChatbot()
    
    # Load a dataset (replace with your CSV file path)
    csv_file = "your_data.csv"  # Change this to your file path
    print(f"Loading dataset: {csv_file}")
    chatbot.load_data(csv_file)
    
    # Get automatic analysis
    print("\n" + "="*60)
    print("Automatic Analysis")
    print("="*60)
    analysis = chatbot.analyze()
    print(analysis)
    
    # Ask specific questions
    print("\n" + "="*60)
    print("Answering Questions")
    print("="*60)
    
    questions = [
        "What are the main trends in this data?",
        "Are there any outliers or anomalies?",
        "What insights can you provide about the numeric columns?",
    ]
    
    for question in questions:
        print(f"\nQ: {question}")
        answer = chatbot.chat(question)
        print(f"A: {answer}")
    
    # Generate visualizations
    print("\n" + "="*60)
    print("Generating Visualizations")
    print("="*60)
    plot_paths = chatbot.generate_visualizations()
    print(f"Generated {len(plot_paths)} visualizations:")
    for path in plot_paths:
        print(f"  - {path}")


if __name__ == "__main__":
    example_usage()

