"""
Main application entry point for the Analytics Chatbot.
Provides both CLI and interactive modes.
"""
import sys
import os
from analytics_chatbot import AnalyticsChatbot


def main():
    """Main function to run the analytics chatbot."""
    print("=" * 60)
    print("Analytics Chatbot - Powered by Gemini AI")
    print("=" * 60)
    print()
    
    # Initialize chatbot
    try:
        chatbot = AnalyticsChatbot()
    except Exception as e:
        print(f"Error initializing chatbot: {e}")
        return
    
    # Check if CSV file provided as command line argument
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
        if not os.path.exists(csv_file):
            print(f"File not found: {csv_file}")
            return
        
        print(f"Loading dataset: {csv_file}")
        try:
            chatbot.load_data(csv_file)
        except Exception as e:
            print(f"Error loading dataset: {e}")
            return
        
        # Generate automatic analysis
        print("\n" + "=" * 60)
        print("Generating Analysis...")
        print("=" * 60 + "\n")
        analysis = chatbot.analyze()
        print(analysis)
        
        # Generate visualizations
        print("\n" + "=" * 60)
        print("Generating Visualizations...")
        print("=" * 60 + "\n")
        try:
            plot_paths = chatbot.generate_visualizations()
            print(f"✓ Generated {len(plot_paths)} visualizations in 'plots' directory")
            for path in plot_paths:
                print(f"  - {path}")
        except Exception as e:
            print(f"⚠️  Error generating visualizations: {e}")
        
        # Interactive mode
        print("\n" + "=" * 60)
        print("Interactive Chat Mode")
        print("=" * 60)
        print("Ask questions about your data! Type 'exit' to quit.\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print("\n👋 Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                print("\n🤖 Assistant: ", end="", flush=True)
                response = chatbot.chat(user_input)
                print(response)
                print()
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}\n")
    
    else:
        # Interactive mode without pre-loaded data
        print("Usage:")
        print("  python app.py <path_to_csv_file>")
        print("\nExample:")
        print("  python app.py data.csv")
        print("\nOr run in interactive mode:")
        print("  python app.py")
        print("\nIn interactive mode, you can:")
        print("  1. Load a dataset")
        print("  2. Ask questions about the data")
        print("  3. Generate visualizations")
        print()
        
        # Simple interactive mode
        print("=" * 60)
        print("Interactive Mode")
        print("=" * 60)
        print("Commands:")
        print("  load <file_path>  - Load a CSV file")
        print("  analyze           - Get automatic analysis")
        print("  plots             - Generate visualizations")
        print("  exit              - Quit")
        print()
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if user_input.startswith('load '):
                    file_path = user_input[5:].strip()
                    if os.path.exists(file_path):
                        chatbot.load_data(file_path)
                        print("✓ Dataset loaded successfully!")
                    else:
                        print(f"File not found: {file_path}")
                
                elif user_input.lower() == 'analyze':
                    if chatbot.df is None:
                        print("Please load a dataset first using 'load <file_path>'")
                    else:
                        print("\nAnalyzing...\n")
                        analysis = chatbot.analyze()
                        print(analysis)
                        print()
                
                elif user_input.lower() == 'plots':
                    if chatbot.df is None:
                        print("Please load a dataset first using 'load <file_path>'")
                    else:
                        print("\nGenerating visualizations...\n")
                        plot_paths = chatbot.generate_visualizations()
                        print(f"✓ Generated {len(plot_paths)} visualizations")
                        for path in plot_paths:
                            print(f"  - {path}")
                        print()
                
                elif user_input:
                    if chatbot.df is None:
                        print("Please load a dataset first using 'load <file_path>'")
                    else:
                        print("\n🤖 Assistant: ", end="", flush=True)
                        response = chatbot.chat(user_input)
                        print(response)
                        print()
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}\n")


if __name__ == "__main__":
    main()

