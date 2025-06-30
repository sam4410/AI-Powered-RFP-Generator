import argparse
import sys
import os
from src.utils.rfp_runner import RFPRunner
from dotenv import load_dotenv
load_dotenv(override = True)

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.crews.crew_orchestrator import CrewOrchestrator
from src.utils.file_handler import FileHandler
from src.utils.validation import ValidationUtils

def main():
    """Main application entry point"""
    # Load environment variables
    load_dotenv(override=True)
    
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Generate RFP using AI agents')
    parser.add_argument('--input', '-i', required=True, 
                       help='Input JSON file with project details')
    parser.add_argument('--output', '-o', default='outputs/generated_rfps', 
                       help='Output directory for generated RFP')
    parser.add_argument('--config', '-c', default='config.yaml',
                       help='Configuration file path')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    try:
        # Validate input file exists
        if not os.path.exists(args.input):
            raise FileNotFoundError(f"Input file not found: {args.input}")
        
        # Load project data
        print(f"Loading project data from {args.input}...")
        project_data = FileHandler.load_json(args.input)
        
        # Initialize orchestrator
        print("Initializing RFP generation system...")
        orchestrator = CrewOrchestrator(args.config)
        
        # Generate RFP
        print("Starting RFP generation process...")
        print("This may take several minutes depending on project complexity...")
        
        result = RFPRunner.run_rfp_pipeline(
            input_json_path=args.input,
            config_path=args.config,
            output_dir=args.output,
            verbose=bool(args.verbose)
        )
        
        # Display output and summary
        print(f"\n✅ RFP generated successfully!")
        print(f"📄 Output file: {result['output_file']}")
        print(f"📊 Project: {result['project_name']}")
        
        # Display summary
        print(f"\n📋 Summary:")
        print(f"   Client: {result['client']}")
        print(f"   Industry: {result['industry']}")
        print(f"   Type: {result['project_type']}")
        print(f"   Budget: {result['budget']}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
