from crewai.tools import BaseTool
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import os
import json

class TemplateEngine(BaseTool):
    name: str = "Template Engine"
    description: str = "Generate RFP sections using predefined templates"

    @property
    def envs(self):
        """Lazily initialize and cache environments per template directory"""
        if not hasattr(self, '_envs'):
            base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
            self._template_dirs = {
                "common": os.path.join(base, "common"),
                "data_warehouse": os.path.join(base, "data_warehouse"),
                "dotnet_application": os.path.join(base, "dotnet_application")
            }
            self._envs = {
                key: Environment(loader=FileSystemLoader(path))
                for key, path in self._template_dirs.items()
                if os.path.exists(path)
            }
        return self._envs

    def _run(self, template_name: str, data: str) -> str:
        try:
            # Try to parse JSON string safely, fallback to original if it's already a dict
            if isinstance(data, str):
                try:
                    template_data = json.loads(data)
                except json.JSONDecodeError as e:
                    return f"❌ TemplateEngine JSON parsing error: {str(e)}\n🔍 Input was: {data}"
            else:
                template_data = data

            project_type = template_data.get("project_type", "data_warehouse")

            env = self.envs.get(project_type)
            if env:
                try:
                    template = env.get_template(template_name)
                    base_output = template.render(**template_data)
                    # Append technical specs if configured
                    config = template_data.get("template_config", {})
                    technical_file = config.get("technical_specs")
                    if technical_file:
                        try:
                            tech_template = env.get_template(technical_file)
                            appendix_output = tech_template.render(**template_data)
                            return f"{base_output}\n\n---\n\n{appendix_output}"
                        except TemplateNotFound:
                            base_output += "\n\n❌ Technical appendix template not found."
                    return base_output
                except TemplateNotFound:
                    pass

            common_env = self.envs.get("common")
            if common_env:
                try:
                    template = common_env.get_template(template_name)
                    return template.render(**template_data)
                except TemplateNotFound:
                    pass

            return self._render_builtin(template_name, template_data)

        except Exception as e:
            return f"❌ Error generating template: {str(e)}"

    def _render_builtin(self, template_type: str, context: dict) -> str:
        from jinja2 import Template

        templates = {
            "executive_summary": """
# Executive Summary

## Client Overview
{{ client_overview }}

## Business Objective
{{ description }}

## Contact & Submission
Proposals are due by **{{ due_date }}** and should be sent to **{{ contact_email }}**

{{ project_name }} is a {{ project_type.replace('_', ' ').title() }} initiative for {{ client_company }} in the {{ client_industry }} industry.

## Description
{{ description }}

## Benefits
{% for criterion in success_criteria or [] %}
- {{ criterion }}
{% endfor %}

## Budget & Timeline
- Budget: {{ budget_range or "TBD" }}
- Timeline: {{ timeline or "TBD" }}

# Timeline & Milestones

**Start Date:** {{ timeline_constraints.start_date }}  
**End Date:** {{ timeline_constraints.end_date }}

## Milestones
{% for item in timeline_constraints.critical_milestones %}
- {{ item }}
{% endfor %}

# Stakeholder Matrix

| Name | Role | Contact | Responsibilities |
|------|------|---------|------------------|
{% for s in stakeholders %}
| {{ s.name }} | {{ s.role }} | {{ s.contact }} | {{ s.responsibilities }} |
{% endfor %}
""",
            "vendor_evaluation": """
# Vendor Evaluation Criteria

## Technical
- Relevant {{ project_type.replace('_', ' ').title() }} experience
- Architecture
- Dev practices

## Business Fit
- Cost
- Timeline
- Industry understanding
"""
        }

        raw_template = templates.get(template_type)
        if raw_template:
            return Template(raw_template).render(**context)
        else:
            return f"❌ Template '{template_type}' not found in files or built-in templates."
