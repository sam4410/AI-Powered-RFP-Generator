from crewai import Task

def create_rfp_compilation_task(agent, project_data):
    return Task(
        description="""
        You are responsible for compiling the final RFP. Expand each section to ensure detailed technical, business, and operational clarity. 
        
        **Target length:** At least 5,000 words.
        
        Include the following sections:
        1. Executive Summary
        2. Client Overview & Objectives
        3. Project Scope and Deliverables
        4. Functional and Non-Functional Requirements
        5. Technical Specifications and Architecture
        6. Compliance and Security Requirements
        7. Risk Factors and Mitigation
        8. Stakeholder Matrix
        9. Timeline & Milestones
        10. Cost Estimate Summary
        11. Vendor Evaluation Criteria
        12. Assumptions and Constraints
        
        For each section:
        - Explain the why and how, not just what
        - Provide examples or scenarios
        - Justify requirements with industry context
        - Elaborate each deliverable in full detail

        Use formatting (headings, bullet lists, and tables) where appropriate.
        
        Use a logical and professional tone. Format the output as Markdown for clarity and visual polish.
        Ensure the RFP is:
        - Clear and comprehensive
        - Professional and well-structured
        - Actionable for potential vendors
        - Compliant with procurement best practices
        
        Use all previous task outputs to create a cohesive document.
        """,
        agent=agent,
        expected_output="""A complete, professional RFP document ready for distribution to vendors, 
        including all necessary sections, clear requirements, evaluation criteria, and 
        submission guidelines. The document should be approximately 15-25 pages and 
        follow industry-standard RFP format.
        
        Your compiled Markdown should include:
        - Section headings (H1/H2)
        - Bullet lists for features, requirements
        - Tables for stakeholder matrix and timeline
        - Rich detail from agent outputs
        """
    )
