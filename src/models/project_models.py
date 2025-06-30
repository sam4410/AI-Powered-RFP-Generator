from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime

class ProjectType(str, Enum):
    DATA_WAREHOUSE = "data_warehouse"
    DOTNET_APPLICATION = "dotnet_application"
    CLOUD_MIGRATION = "cloud_migration"
    INTEGRATION_PLATFORM = "integration_platform"

class ProjectComplexity(str, Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

class Stakeholder(BaseModel):
    name: str
    role: str
    contact: str
    responsibilities: str

class TimelineConstraints(BaseModel):
    start_date: str
    end_date: str
    critical_milestones: List[str]

class ProjectRequirements(BaseModel):
    project_name: str
    project_type: ProjectType
    client_company: str
    client_industry: str
    contact_email: str
    due_date: str
    description: str
    budget_range: Optional[str]
    timeline: Optional[str]
    client_overview: Optional[str]
    functional_requirements: List[str]
    non_functional_requirements: List[str]
    technical_requirements: List[str]
    performance_requirements: Dict[str, str]
    security_requirements: List[str]
    compliance_requirements: List[str]
    integration_requirements: List[str]
    existing_systems: List[str]
    constraints: List[str]
    assumptions: List[str]
    stakeholders: List[Stakeholder]
    success_criteria: List[str]
    risk_factors: List[str]
    evaluation_criteria: List[str]
    timeline_constraints: Optional[TimelineConstraints]

class TechnicalSpec(BaseModel):
    architecture_overview: str
    technology_stack: List[str]
    integration_points: List[str]
    security_requirements: List[str]
    performance_requirements: List[str]
    scalability_considerations: str

class BusinessAnalysis(BaseModel):
    business_case: str
    roi_analysis: str
    risk_assessment: List[str]
    strategic_alignment: str

class CostEstimate(BaseModel):
    total_cost: float
    cost_breakdown: Dict[str, float]
    assumptions: List[str]
    complexity_factor: float

class RFPOutput(BaseModel):
    project_info: ProjectRequirements
    executive_summary: str
    technical_specifications: TechnicalSpec
    business_analysis: BusinessAnalysis
    cost_estimate: CostEstimate
    timeline: str
    deliverables: List[str]
    vendor_evaluation_criteria: List[str]
    compliance_requirements: List[str]
    generated_at: datetime = Field(default_factory=datetime.now)
