import os
from src.crews.crew_orchestrator import CrewOrchestrator
from src.utils.file_handler import FileHandler

class RFPRunner:
    @staticmethod
    def run_rfp_pipeline(input_json_path: str, config_path: str, output_dir: str, verbose: bool = False):
        if not os.path.exists(input_json_path):
            raise FileNotFoundError(f"Input file not found: {input_json_path}")

        if verbose:
            print(f"Loading project data from {input_json_path}...")

        # Load project data
        project_data = FileHandler.load_json(input_json_path)

        if verbose:
            print("Initializing RFP generation system...")

        orchestrator = CrewOrchestrator(config_path, verbose=verbose)

        if verbose:
            print("Generating RFP... This may take a few minutes...")

        # Orchestrate generation
        result = orchestrator.orchestrate_rfp_generation(project_data)

        # Save result
        project_name = project_data.get('project_name', 'Unknown_Project')
        output_path = orchestrator.save_results(result, project_name, output_dir)

        # Create summary dictionary
        summary = {
            "output_file": output_path,
            "docx_file": output_path.replace(".md", ".docx"),
            "project_name": project_name,
            "client": project_data.get("client_company", "N/A"),
            "industry": project_data.get("client_industry", "N/A"),
            "project_type": project_data.get("project_type", "N/A").replace("_", " ").title(),
            "budget": project_data.get("budget_range", "TBD")
        }

        return summary
