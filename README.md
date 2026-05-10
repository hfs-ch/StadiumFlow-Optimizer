# SONARGES SmartFlow Optimizer

Application desktop Python (PyQt6) pour modeliser, simuler et optimiser le flux des supporters du Grand Stade de Marrakech pour la Coupe du Monde 2030 avec la methode du Simplexe.

## Fonctionnalites

- Interface centre de controle futuriste (dark mode neon/cyan).
- Ecrans: Splash, Login, Dashboard, Optimisation, Simulation temps reel, Graphiques, Rapports, Logs.
- Optimisation Simplexe:
  - Variables: Police Nationale (`x1`), Stewards (`x2`), Benevoles (`x3`).
  - Objectif: `Max Z = 10x1 + 18x2 + 8x3`.
  - Contraintes budget, infrastructure, espace, securite.
- Visualisations dynamiques Matplotlib.
- Exports PDF premium et Excel.
- Mode test "Simulation de Match".
- Recommandations IA simulees (anomalies/congestion).

## Architecture

Architecture MVC modulaire:

- `models/` definitions metier et scenarios.
- `solver/` solveur Simplexe (tableaux + solution optimale via SciPy).
- `controllers/` orchestration applicative.
- `ui/` fenetres et pages.
- `simulations/` moteur de simulation temps reel.
- `charts/` generation et mise a jour des graphiques.
- `reports/` generation PDF.
- `exports/` export Excel/PNG.
- `animations/` animations Qt.
- `utils/` logging applicatif.

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Lancement

```bash
python main.py
```

## Notes

- Compatible Python 3.12.
- Le son d'alerte utilise `QApplication.beep()` pour rester portable.
- La capture PNG dashboard exporte le widget principal en image.
