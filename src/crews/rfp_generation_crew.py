from crewai import Crew, Process
from src.agents.requirements_analyst import create_requirements_analyst
from src.agents.technical_architect import create_technical_architect
from src.agents.business_analyst import create_business_analyst
from src.agents.compliance_officer import create_compliance_officer
from src.agents.cost_estimator import create_cost_estimator
from src.agents.rfp_writer import create_rfp_writer
from src.tasks.analysis_tasks import create_requirements_extraction_task, create_stakeholder_analysis_task
from src.tasks.technical_tasks import create_architecture_design_task, create_technology_evaluation_task
from src.tasks.business_tasks import create_business_case_task
from src.tasks.compliance_tasks import create_compliance_review_task
from src.tasks.writing_tasks import create_rfp_compilation_task

class RFPGenerationCrew:
    def __init__(self, project_data, verbose=False):
        self.project_data = project_data
        self._setup_agents()
        self._setup_tasks()
        self.verbose = bool(verbose)
        
    def _setup_agents(self):
        """Initialize all agents"""
        self.requirements_analyst = create_requirements_analyst()
        self.technical_architect = create_technical_architect()
        self.business_analyst = create_business_analyst()
        self.compliance_officer = create_compliance_officer()
        self.cost_estimator = create_cost_estimator()
        self.rfp_writer = create_rfp_writer()
        
    def _setup_tasks(self):
        """Initialize all tasks with agents"""
        self.requirements_task = create_requirements_extraction_task(self.requirements_analyst, self.project_data)
        self.stakeholder_task = create_stakeholder_analysis_task(self.requirements_analyst, self.project_data)
        self.architecture_task = create_architecture_design_task(self.technical_architect, self.project_data)
        self.technology_task = create_technology_evaluation_task(self.technical_architect, self.project_data)
        self.business_case_task = create_business_case_task(self.business_analyst, self.project_data)
        self.compliance_task = create_compliance_review_task(self.compliance_officer, self.project_data)
        self.rfp_task = create_rfp_compilation_task(self.rfp_writer, self.project_data)
        
        # Set up task dependencies
        self.architecture_task.context = [self.requirements_task]
        self.technology_task.context = [self.requirements_task, self.architecture_task]
        self.business_case_task.context = [self.requirements_task, self.architecture_task]
        self.compliance_task.context = [self.requirements_task]
        self.rfp_task.context = [
            self.requirements_task, 
            self.stakeholder_task,
            self.architecture_task, 
            self.technology_task,
            self.business_case_task, 
            self.compliance_task
        ]
        
    def create_crew(self):
        """Create and configure the crew"""
        return Crew(
            agents=[
                self.requirements_analyst,
                self.technical_architect,
                self.business_analyst,
                self.compliance_officer,
                self.cost_estimator,
                self.rfp_writer
            ],
            tasks=[
                self.requirements_task,
                self.stakeholder_task,
                self.architecture_task,
                self.technology_task,
                self.business_case_task,
                self.compliance_task,
                self.rfp_task
            ],
            process=Process.sequential,
            verbose=self.verbose,
            memory=False
        )
    
    def generate_rfp(self):
        """Execute the crew and generate RFP"""
        self.project_data["template_config"] = {
            "base_template": "enterprise_dw_template.md",
            "technical_specs": "dw_technical_specs.md"
        }
        crew = self.create_crew()
        result = crew.kickoff(inputs=self.project_data)
        return result
