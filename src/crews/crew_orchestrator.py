from typing import Dict, Any
from src.crews.rfp_generation_crew import RFPGenerationCrew
from src.models.project_models import ProjectRequirements, RFPOutput
from src.utils.validation import ValidationUtils
from src.utils.file_handler import FileHandler
import logging
import os
from datetime import datetime

class CrewOrchestrator:
    def __init__(self, config_path: str = "config.yaml", verbose: bool = False):
        self.config = FileHandler.load_yaml(config_path)
        self.setup_logging()
        self.verbose = bool(verbose)
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('rfp_generation.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def orchestrate_rfp_generation(self, project_data: Dict[str, Any]) -> str:
        """Main orchestration method"""
        try:
            # Validate input data
            self.logger.info("Validating project data...")
            ValidationUtils.validate_project_data(project_data)
            
            # Create project requirements model
            requirements = ProjectRequirements(**project_data)
            self.logger.info(f"Processing project: {requirements.project_name}")
            
            # Initialize and run crew
            self.logger.info("Initializing RFP generation crew...")
            rfp_crew = RFPGenerationCrew(project_data, verbose=self.verbose)
            
            self.logger.info("Starting RFP generation process...")
            result = rfp_crew.generate_rfp()
            
            self.logger.info("RFP generation completed successfully")
            return result
            
        except Exception as e:
            self.logger.error(f"Error during RFP generation: {str(e)}")
            raise
    
    def save_results(self, result, project_name, output_dir):

        os.makedirs(output_dir, exist_ok=True)

        filename = f"RFP_{project_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        output_path = os.path.join(output_dir, filename)

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                # FIX: Convert result to string
                f.write(str(result))
        except Exception as e:
            raise RuntimeError(f"❌ Failed to write RFP to file: {str(e)}")

        return output_path
