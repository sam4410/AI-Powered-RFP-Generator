from crewai import Agent
from src.tools.template_engine import TemplateEngine

def create_rfp_writer():
    return Agent(
        role="Senior RFP Writer",
        goal="Compile an extensively detailed, full-length RFP of at least 5,000 words",
        backstory="""You are a professional technical writer with extensive experience in 
        creating RFPs for enterprise technology projects. You understand how to structure 
        complex information clearly, write compelling narratives, and ensure all stakeholder 
        needs are addressed. You have helped organizations successfully procure millions 
        of dollars in technology solutions through well-crafted RFPs.""",
        tools=[TemplateEngine()],
        verbose=True,
        allow_delegation=False,
        max_execution_time=500
    )
