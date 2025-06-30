from crewai import Task

def create_requirements_extraction_task(agent, project_data):
    return Task(
        description=f"""
        Analyze the provided project description and extract comprehensive requirements:
        
        1. Functional, non-functional, technical, and integration requirements
        2. Business goals, success criteria, constraints, assumptions, and risks
        3. Stakeholder roles and responsibilities
        4. Performance, security, and compliance expectations
        5. Technical, business, and timeline limitations
        6. Measurable outcomes/deliverables that define project success
        
        Input Information:
        - Client Overview: {project_data.get("client_overview", "N/A")}
        - Client Contact Email: {project_data.get("contact_email", "N/A")}
        - RFP Due Date: {project_data.get("due_date", "N/A")}
        - Project Name: {project_data.get("project_name", "N/A")}
        - Project Type: {project_data.get("project_type", "N/A")}
        - Client Company: {project_data.get("client_company", "N/A")}
        - Industry: {project_data.get("client_industry", "N/A")}
        - Budget Range: {project_data.get("budget_range", "N/A")}
        - Timeline: {project_data.get("timeline", "N/A")}
        - Project Description: {project_data.get("description", "N/A")}
        - Project Scope: {project_data.get("project_scope", "N/A")}
        - Project Deliverables: {project_data.get("deliverables", "N/A")}
        - Success Criteria : {project_data.get("succss_criteria", "N/A")}
        - Functional Requirements: {project_data.get("functional_requirements", "N/A")}
        - Non-Functional Requirements: {project_data.get("non_functional_requirements", "N/A")}
        - Technical Requirements: {project_data.get("technical_requirements", "N/A")}
        - Performance Requirements: {project_data.get("performance_requirements", "N/A")}
        - Security Requirements: {project_data.get("security_requirements", "N/A")}
        - Compliance Requirements: {project_data.get("compliance_requirements", "N/A")}
        - Integration Requirements: {project_data.get("integration_requirements", "N/A")}
        - Existing System: {project_data.get("existing_systems", "N/A")}
        - Constraints: {project_data.get("constraints", "N/A")}
        - Success Criteria: {project_data.get("succss_criteria", "N/A")}
        - Assumptions: {project_data.get("assumptions", "N/A")}
        - Stakeholders: {project_data.get("stakeholders", "N/A")}
        - Risk Factors: {project_data.get("risk_factors", "N/A")}
        - Evaluation Criteria: {project_data.get("evaluation_criteria", "N/A")}
        - Timeline Constraints: {project_data.get("timeline_constraints", "N/A")}
        
        Focus on identifying both explicit and implicit requirements. Look for gaps 
        that need clarification and suggest additional requirements based on industry 
        best practices.
        """,
        agent=agent,
        expected_output="""
        A comprehensive requirements analysis document containing:
        - Functional / Non-functional / Technical / Security requirements
        - Stakeholder analysis and mapping with roles and responsibilities  
        - Identified constraints and assumptions
        - Timeline constraints and assumptions
        - Success criteria and KPIs
        - Risk factors and mitigation strategies
        - Recommended clarifications needed from the client
        - Open clarifications
        """
    )

def create_stakeholder_analysis_task(agent, project_data):
    return Task(
        description="""
        Analyze the stakeholder information provided by the client. Create a clear stakeholder matrix including:
        - Names
        - Roles
        - Contact info
        - Their project responsibilities

        Also flag any unclear or missing roles or contacts.
        """,
                agent=agent,
                expected_output="""
        A markdown table of stakeholders with:
        - Name, Role, Contact, Responsibility columns
        - Plus any missing/unclear roles highlighted
        """
            )
  
