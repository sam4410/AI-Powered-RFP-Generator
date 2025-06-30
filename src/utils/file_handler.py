import os
import json
from datetime import datetime
from typing import Any
import yaml

class FileHandler:
    @staticmethod
    def load_json(filepath: str) -> dict:
        """Load JSON file and return dictionary"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Error loading JSON file {filepath}: {str(e)}")
    
    @staticmethod
    def save_json(data: dict, filepath: str) -> None:
        """Save dictionary as JSON file"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
    
    @staticmethod
    def load_yaml(filepath: str) -> dict:
        """Load YAML configuration file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    @staticmethod
    def save_rfp_document(rfp_content: str, output_dir: str, project_name: str) -> str:
        """Save RFP document to markdown file"""
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"RFP_{project_name.replace(' ', '_')}_{timestamp}.md"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(rfp_content)
        
        return filepath
