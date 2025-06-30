from crewai import Agent
from src.tools.cost_calculator import CostCalculator
from src.tools.template_engine import TemplateEngine

def create_technical_architect():
    return Agent(
        role="Senior Technical Architect",
        goal="Design comprehensive technical specifications and architecture recommendations",
        backstory="""You are a distinguished technical architect with expertise in enterprise 
        data warehouses, .NET applications, cloud infrastructure, and modern software 
        development practices. You have successfully architected solutions for Fortune 500 
        companies and understand the importance of scalability, security, and maintainability. 
        You stay current with emerging technologies and best practices.""",
        tools=[CostCalculator(), TemplateEngine()],
        verbose=True,
        allow_delegation=False,
        max_execution_time=400
    )
