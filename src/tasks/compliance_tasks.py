from crewai import Task

def create_compliance_review_task(agent, project_data):
    return Task(
        description="""
        Conduct a comprehensive compliance and security review:
        
        1. **Regulatory Requirements**: Identify applicable laws and regulations
        2. **Industry Standards**: Relevant frameworks and best practices
        3. **Security Requirements**: Security controls and implementation guidelines
        4. **Data Protection**: Privacy and data handling requirements
        5. **Audit Requirements**: Logging, monitoring, and audit trail needs
        6. **Compliance Testing**: Validation and certification requirements
        
        Focus on:
        - Industry: {client_industry}
        - Project Type: {project_type}
        - Geographic considerations (if applicable)
        """,
        agent=agent,
        expected_output="""Compliance and security assessment including:
        - Applicable regulatory requirements and standards
        - Security framework recommendations
        - Data protection and privacy requirements
        - Compliance validation and testing approach
        - Audit and monitoring requirements
        - Risk management and incident response procedures"""
    )
