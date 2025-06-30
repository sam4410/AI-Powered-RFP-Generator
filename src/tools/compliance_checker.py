from crewai.tools import BaseTool
from typing import List, Dict

class ComplianceChecker(BaseTool):
    name: str = "Compliance Checker"
    description: str = "Check compliance requirements based on industry and project type"
    
    def _run(self, industry: str, project_type: str, requirements: str = "") -> str:
        """Check compliance requirements"""
        try:
            compliance_reqs = self._get_industry_compliance(industry)
            project_specific = self._get_project_compliance(project_type)
            
            all_requirements = compliance_reqs + project_specific
            
            result = {
                "industry_compliance": compliance_reqs,
                "project_specific_compliance": project_specific,
                "recommended_frameworks": self._get_compliance_frameworks(industry),
                "security_requirements": self._get_security_requirements(project_type)
            }
            
            return str(result)
            
        except Exception as e:
            return f"Error checking compliance: {str(e)}"
    
    def _get_industry_compliance(self, industry: str) -> List[str]:
        """Get industry-specific compliance requirements"""
        industry_compliance = {
            "financial": ["SOX", "PCI-DSS", "GDPR", "SOC 2"],
            "healthcare": ["HIPAA", "HITECH", "FDA 21 CFR Part 11"],
            "manufacturing": ["ISO 27001", "GDPR", "Industry 4.0 Standards"],
            "retail": ["PCI-DSS", "GDPR", "CCPA"],
            "government": ["FedRAMP", "FISMA", "Section 508"],
            "education": ["FERPA", "COPPA", "GDPR"]
        }
        
        return industry_compliance.get(industry.lower(), ["GDPR", "ISO 27001"])
    
    def _get_project_compliance(self, project_type: str) -> List[str]:
        """Get project-type specific compliance requirements"""
        project_compliance = {
            "data_warehouse": ["Data Privacy Laws", "Data Retention Policies", "Audit Trails"],
            "dotnet_application": ["OWASP Top 10", "Secure Coding Standards", "Authentication Standards"],
            "cloud_migration": ["Cloud Security Framework", "Data Residency Requirements"]
        }
        
        return project_compliance.get(project_type, ["General Security Standards"])
    
    def _get_compliance_frameworks(self, industry: str) -> List[str]:
        """Get recommended compliance frameworks"""
        frameworks = {
            "financial": ["NIST Cybersecurity Framework", "ISO 27001", "COBIT"],
            "healthcare": ["NIST Cybersecurity Framework", "HITRUST CSF"],
            "manufacturing": ["IEC 62443", "NIST Manufacturing Profile"],
            "default": ["NIST Cybersecurity Framework", "ISO 27001"]
        }
        
        return frameworks.get(industry.lower(), frameworks["default"])
    
    def _get_security_requirements(self, project_type: str) -> List[str]:
        """Get security requirements by project type"""
        return [
            "Multi-factor authentication",
            "Data encryption at rest and in transit",
            "Regular security assessments",
            "Incident response procedures",
            "Access control and privilege management",
            "Security monitoring and logging"
        ]
