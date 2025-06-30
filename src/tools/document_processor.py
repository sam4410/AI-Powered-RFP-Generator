from crewai.tools import BaseTool
from typing import Dict, List
import re

class DocumentProcessor(BaseTool):
    name: str = "Document Processor"
    description: str = "Process and extract information from project documents and requirements"
    
    def _run(self, text: str) -> str:
        """Process document text and extract key information"""
        try:
            # Extract key sections
            sections = self._extract_sections(text)
            
            # Analyze requirements
            requirements = self._extract_requirements(text)
            
            # Identify stakeholders
            stakeholders = self._extract_stakeholders(text)
            
            result = {
                "sections": sections,
                "requirements": requirements,
                "stakeholders": stakeholders,
                "word_count": len(text.split()),
                "complexity_indicators": self._assess_complexity_indicators(text)
            }
            
            return str(result)
            
        except Exception as e:
            return f"Error processing document: {str(e)}"
    
    def _extract_sections(self, text: str) -> Dict[str, str]:
        """Extract different sections from text"""
        sections = {}
        
        # Look for common section headers
        section_patterns = {
            'objectives': r'(?i)(objective|goal|purpose)s?:?\s*(.+?)(?=\n\n|\n[A-Z]|$)',
            'requirements': r'(?i)requirements?:?\s*(.+?)(?=\n\n|\n[A-Z]|$)',
            'constraints': r'(?i)constraints?:?\s*(.+?)(?=\n\n|\n[A-Z]|$)',
            'timeline': r'(?i)(timeline|schedule|deadline)s?:?\s*(.+?)(?=\n\n|\n[A-Z]|$)'
        }
        
        for section_name, pattern in section_patterns.items():
            match = re.search(pattern, text, re.DOTALL)
            if match:
                sections[section_name] = match.group(2).strip()
        
        return sections
    
    def _extract_requirements(self, text: str) -> List[str]:
        """Extract requirements from text"""
        requirements = []
        
        # Look for numbered or bulleted requirements
        requirement_patterns = [
            r'(?i)(?:requirement|req|must|should|shall)\s*\d*:?\s*(.+?)(?=\n|$)',
            r'[-•*]\s*(.+?)(?=\n|$)',
            r'\d+\.\s*(.+?)(?=\n|$)'
        ]
        
        for pattern in requirement_patterns:
            matches = re.findall(pattern, text)
            requirements.extend([match.strip() for match in matches if len(match.strip()) > 10])
        
        return list(set(requirements))  # Remove duplicates
    
    def _extract_stakeholders(self, text: str) -> List[str]:
        """Extract stakeholder information"""
        stakeholder_keywords = [
            'stakeholder', 'user', 'client', 'customer', 'manager', 'admin', 'executive',
            'team', 'department', 'business analyst', 'project manager'
        ]
        
        stakeholders = []
        for keyword in stakeholder_keywords:
            pattern = rf'(?i){keyword}s?\b'
            if re.search(pattern, text):
                stakeholders.append(keyword.title())
        
        return list(set(stakeholders))
    
    def _assess_complexity_indicators(self, text: str) -> List[str]:
        """Assess project complexity based on text content"""
        complexity_indicators = []
        
        complexity_keywords = {
            'high': ['enterprise', 'large-scale', 'complex', 'integration', 'real-time', 'high-availability'],
            'medium': ['moderate', 'standard', 'typical', 'conventional'],
            'low': ['simple', 'basic', 'straightforward', 'minimal']
        }
        
        text_lower = text.lower()
        for level, keywords in complexity_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    complexity_indicators.append(f"{level}: {keyword}")
        
        return complexity_indicators
