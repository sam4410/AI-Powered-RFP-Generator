from typing import Dict, List, Any
from src.models.project_models import ProjectRequirements, ProjectType

class ValidationUtils:
    @staticmethod
    def validate_project_data(data: Dict[str, Any]) -> bool:
        """Validate project input data"""
        required_fields = ['project_name', 'project_type', 'client_company', 'description']
        
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"Required field '{field}' is missing or empty")
        
        if data['project_type'] not in [pt.value for pt in ProjectType]:
            raise ValueError(f"Invalid project type: {data['project_type']}")
        
        return True
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize input text"""
        if not isinstance(text, str):
            return str(text)
        return text.strip()
