from crewai.tools import BaseTool
import json
from typing import Dict, List
import yaml
import os

class CostCalculator(BaseTool):
    name: str = "Cost Calculator"
    description: str = "Calculate project costs based on requirements and complexity"

    @property
    def cost_benchmarks(self) -> Dict:
        """Lazily load cost benchmarks from config.yaml, fallback to defaults"""
        if not hasattr(self, '_cost_benchmarks'):
            try:
                config_path = os.path.abspath("config.yaml")
                if os.path.exists(config_path):
                    with open(config_path, 'r') as f:
                        config = yaml.safe_load(f)
                        self._cost_benchmarks = config.get('cost_benchmarks', {})
                else:
                    raise FileNotFoundError
            except:
                self._cost_benchmarks = {
                    'data_warehouse': {'small': 150000, 'medium': 500000, 'large': 1500000},
                    'dotnet_application': {'small': 75000, 'medium': 250000, 'large': 750000},
                    'cloud_migration': {'small': 100000, 'medium': 350000, 'large': 1000000}
                }
        return self._cost_benchmarks

    def _run(self, project_type: str, requirements: str, complexity: str = "medium") -> str:
        """Calculate project costs"""
        try:
            base_cost = self._get_base_cost(project_type, complexity)
            complexity_multiplier = self._calculate_complexity_multiplier(requirements)
            total_cost = base_cost * complexity_multiplier
            cost_breakdown = self._generate_cost_breakdown(total_cost, project_type)

            result = {
                "base_cost": base_cost,
                "complexity_multiplier": complexity_multiplier,
                "total_estimated_cost": total_cost,
                "cost_breakdown": cost_breakdown,
                "assumptions": self._get_cost_assumptions(project_type),
                "risk_contingency": total_cost * 0.15
            }

            return json.dumps(result, indent=2)

        except Exception as e:
            return f"❌ Error calculating costs: {str(e)}"

    def _get_base_cost(self, project_type: str, complexity: str) -> float:
        project_costs = self.cost_benchmarks.get(project_type, {})
        return project_costs.get(complexity, 250000)

    def _calculate_complexity_multiplier(self, requirements: str) -> float:
        complexity_factors = {
            'integration': 1.3,
            'real-time': 1.4,
            'high-availability': 1.2,
            'compliance': 1.25,
            'custom': 1.35,
            'legacy': 1.3,
            'cloud': 1.1,
            'security': 1.2,
            'scalability': 1.15
        }

        multiplier = 1.0
        reqs = requirements.lower()
        for factor, value in complexity_factors.items():
            if factor in reqs:
                multiplier *= value

        return min(multiplier, 2.5)

    def _generate_cost_breakdown(self, total_cost: float, project_type: str) -> Dict[str, float]:
        if project_type == "data_warehouse":
            return {
                "development": total_cost * 0.45,
                "infrastructure": total_cost * 0.25,
                "testing": total_cost * 0.15,
                "project_management": total_cost * 0.10,
                "training": total_cost * 0.05
            }
        elif project_type == "dotnet_application":
            return {
                "development": total_cost * 0.50,
                "ui_ux_design": total_cost * 0.15,
                "testing": total_cost * 0.20,
                "project_management": total_cost * 0.10,
                "deployment": total_cost * 0.05
            }
        else:
            return {
                "development": total_cost * 0.40,
                "infrastructure": total_cost * 0.30,
                "testing": total_cost * 0.15,
                "project_management": total_cost * 0.10,
                "other": total_cost * 0.05
            }

    def _get_cost_assumptions(self, project_type: str) -> List[str]:
        common = [
            "Assumes standard working hours (40 hours/week)",
            "Includes 15% risk contingency",
            "Based on current market rates",
            "Excludes ongoing maintenance costs"
        ]
        specific = {
            "data_warehouse": [
                "Assumes cloud-based infrastructure",
                "Includes data migration costs",
                "ETL development included"
            ],
            "dotnet_application": [
                "Assumes .NET Core/5+ framework",
                "UI/UX design included",
                "Basic security implementation"
            ]
        }
        return common + specific.get(project_type, [])
