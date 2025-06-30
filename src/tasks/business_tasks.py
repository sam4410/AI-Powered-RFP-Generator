from crewai import Task

def create_business_case_task(agent, project_data):
    return Task(
        description="""
        Develop a comprehensive business case for the project:
        
        1. **Business Value Proposition**: How the solution addresses business needs
        2. **ROI Analysis**: Financial returns and payback period
        3. **Cost-Benefit Analysis**: Detailed cost vs. benefit breakdown
        4. **Risk Assessment**: Business and technical risks with mitigation strategies
        5. **Strategic Alignment**: How the project supports business strategy
        6. **Success Metrics**: KPIs and measurement criteria
        
        Use the requirements analysis and technical architecture to inform your analysis.
        Consider industry-specific factors and market conditions.
        """,
        agent=agent,
        expected_output="""Complete business case document including:
        - Executive summary of business value
        - Detailed ROI calculation and financial projections
        - Risk analysis with mitigation strategies
        - Strategic alignment assessment
        - Success metrics and measurement plan
        - Implementation timeline and milestones"""
    )
