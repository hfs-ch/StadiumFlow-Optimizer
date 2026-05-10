from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np
from scipy.optimize import linprog

from models.optimization_model import OptimizationConfig, OptimizationResult


@dataclass
class SolverOutput:
    result: OptimizationResult
    logs: List[str]


class SmartFlowSimplexSolver:
    """Solveur hybride:
    - SciPy linprog pour robustesse de la solution optimale
    - Tableau Simplexe pedagogique pour historique des iterations
    """

    def __init__(self, config: OptimizationConfig | None = None) -> None:
        self.config = config or OptimizationConfig()

    def solve(self) -> SolverOutput:
        c = -self.config.objective
        a_ub = np.array(
            [
                [1500, 800, 200],
                [1, 1, 0.5],
                [3, 1.5, 1],
                [-1, 0, 0],
            ],
            dtype=float,
        )
        b_ub = np.array(
            [
                self.config.budget_limit,
                self.config.infra_limit,
                self.config.space_limit,
                -self.config.min_police,
            ],
            dtype=float,
        )

        bounds = [(0, None), (0, None), (0, None)]
        linprog_res = linprog(c=c, A_ub=a_ub, b_ub=b_ub, bounds=bounds, method="highs")
        if not linprog_res.success:
            raise RuntimeError(f"Echec optimisation: {linprog_res.message}")

        x = linprog_res.x
        z = float(np.dot(self.config.objective, x))

        saturated = self._detect_saturated_constraints(x)
        tableau_history, simplex_iterations, logs = self._build_simplex_history()

        result = OptimizationResult(
            x1_police=float(x[0]),
            x2_stewards=float(x[1]),
            x3_volunteers=float(x[2]),
            z_max=z,
            saturated_constraints=saturated,
            simplex_iterations=simplex_iterations,
            tableau_history=tableau_history,
        )
        logs.append(
            f"Solution optimale: x1={x[0]:.2f}, x2={x[1]:.2f}, x3={x[2]:.2f}, Z={z:.2f}"
        )
        return SolverOutput(result=result, logs=logs)

    def _detect_saturated_constraints(self, x: np.ndarray) -> List[str]:
        labels = []
        budget = 1500 * x[0] + 800 * x[1] + 200 * x[2]
        infra = x[0] + x[1] + 0.5 * x[2]
        space = 3 * x[0] + 1.5 * x[1] + x[2]
        if abs(budget - self.config.budget_limit) <= 1e-3:
            labels.append("Budget")
        if abs(infra - self.config.infra_limit) <= 1e-3:
            labels.append("Infrastructure")
        if abs(space - self.config.space_limit) <= 1e-3:
            labels.append("Espace")
        if abs(x[0] - self.config.min_police) <= 1e-3:
            labels.append("Securite minimale")
        return labels

    def _build_simplex_history(self) -> Tuple[List[np.ndarray], List[Dict[str, float]], List[str]]:
        # Transformation: y1 = x1 - 4 => y1 >= 0
        # Max Z = 10(y1+4)+18x2+8x3 = 10y1+18x2+8x3 + 40
        # Contraintes:
        # 1500y1 + 800x2 + 200x3 <= 24000
        # y1 + x2 + 0.5x3 <= 12
        # 3y1 + 1.5x2 + x3 <= 24
        a = np.array(
            [
                [1500.0, 800.0, 200.0],
                [1.0, 1.0, 0.5],
                [3.0, 1.5, 1.0],
            ]
        )
        b = np.array([24000.0, 12.0, 24.0])
        c = np.array([10.0, 18.0, 8.0])

        m, n = a.shape
        tableau = np.zeros((m + 1, n + m + 1))
        tableau[:m, :n] = a
        tableau[:m, n : n + m] = np.eye(m)
        tableau[:m, -1] = b
        tableau[-1, :n] = -c
        basis = list(range(n, n + m))

        history: List[np.ndarray] = [tableau.copy()]
        iterations: List[Dict[str, float]] = []
        logs: List[str] = ["Demarrage Simplexe (tableau pedagogique)."]

        for k in range(10):
            obj_row = tableau[-1, :-1]
            entering = int(np.argmin(obj_row))
            if obj_row[entering] >= -1e-9:
                logs.append(f"Optimalite atteinte en {k} iterations tableau.")
                break

            ratios = []
            for i in range(m):
                col_val = tableau[i, entering]
                ratios.append(tableau[i, -1] / col_val if col_val > 1e-9 else np.inf)
            leaving = int(np.argmin(ratios))
            if not np.isfinite(ratios[leaving]):
                logs.append("Probleme non borne detecte.")
                break

            pivot = tableau[leaving, entering]
            tableau[leaving, :] = tableau[leaving, :] / pivot
            for i in range(m + 1):
                if i != leaving:
                    tableau[i, :] -= tableau[i, entering] * tableau[leaving, :]

            basis[leaving] = entering
            history.append(tableau.copy())
            values = np.zeros(n + m)
            for i, var in enumerate(basis):
                values[var] = tableau[i, -1]

            y1, x2, x3 = values[0], values[1], values[2]
            x1 = y1 + 4
            z = 10 * x1 + 18 * x2 + 8 * x3
            iterations.append({"iteration": k + 1, "x1": x1, "x2": x2, "x3": x3, "z": z})
            logs.append(
                f"Iter {k + 1}: enter={entering}, leave={leaving}, x1={x1:.2f}, x2={x2:.2f}, x3={x3:.2f}, Z={z:.2f}"
            )

        return history, iterations, logs
