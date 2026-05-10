from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

import numpy as np


@dataclass
class OptimizationConfig:
    budget_limit: float = 30000
    infra_limit: float = 16
    space_limit: float = 36
    min_police: float = 4
    objective: np.ndarray = field(default_factory=lambda: np.array([10.0, 18.0, 8.0]))


@dataclass
class OptimizationResult:
    x1_police: float
    x2_stewards: float
    x3_volunteers: float
    z_max: float
    saturated_constraints: List[str]
    simplex_iterations: List[Dict[str, float]]
    tableau_history: List[np.ndarray]


MATCH_SCENARIOS = {
    "Faible affluence": {"arrival_rate": 80, "risk": 0.2},
    "Moyenne affluence": {"arrival_rate": 140, "risk": 0.35},
    "Forte affluence": {"arrival_rate": 210, "risk": 0.5},
    "Scenario critique": {"arrival_rate": 300, "risk": 0.75},
}
