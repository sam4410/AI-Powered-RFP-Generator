from crewai import Task

def create_architecture_design_task(agent, project_data):
    return Task(
        description="""
        Design a comprehensive technical architecture based on the requirements analysis:
        
        1. **High-Level Architecture**: System overview and component relationships
        2. **Technology Stack**: Recommended technologies, frameworks, and tools
        3. **Integration Architecture**: How the system will integrate with existing systems
        4. **Data Architecture**: Data flow, storage, and management approach
        5. **Security Architecture**: Security controls and implementation approach
        6. **Scalability and Performance**: How the system will handle growth and load
        7. **Deployment Architecture**: Infrastructure and deployment strategies
        
        Project Details:
        - Project Type: {project_type}
        - Industry: {client_industry}
        - Requirements: Use the output from requirements analysis
        
        Focus on industry best practices and ensure the architecture addresses 
        all functional and non-functional requirements.
        """,
        agent=agent,
        expected_output="""Comprehensive technical architecture document including:
        - System architecture diagrams and component descriptions
        - Technology stack recommendations with justifications
        - Integration patterns and API specifications
        - Data architecture and flow diagrams
        - Security architecture and controls
        - Performance and scalability considerations
        - Infrastructure requirements and deployment strategy"""
    )

def create_technology_evaluation_task(agent, project_data):
    return Task(
        description="""
        Evaluate technology options and provide recommendations:
        
        1. **Technology Assessment**: Evaluate different technology options
        2. **Pros and Cons Analysis**: Benefits and limitations of each approach
        3. **Implementation Complexity**: Effort and risk assessment
        4. **Total Cost of Ownership**: Long-term cost implications
        5. **Vendor Evaluation**: If applicable, assess technology vendors
        6. **Migration Strategy**: If replacing existing systems
        
        Consider factors like:
        - Alignment with client's existing technology stack
        - Industry-specific requirements
        - Long-term maintainability and support
        - Skills availability and training requirements
        """,
        agent=agent,
        expected_output="""Technology evaluation report containing:
        - Detailed comparison matrix of technology options
        - Recommended technology stack with justifications
        - Implementation roadmap and migration strategy
        - Risk assessment and mitigation plans
        - Training and skills development requirements"""
    )
