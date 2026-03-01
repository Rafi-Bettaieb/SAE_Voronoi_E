# SAE S6 : Diagrammes de Voronoï

Application Python permettant de générer, visualiser et exporter des diagrammes de Voronoï à partir d’une liste de points 2D.

---

## Installation

1. Clonez le dépôt :

   ```bash
   git clone https://github.com/Rafi-Bettaieb/SAE_S6.git
   cd SAE_S6
   ```

2. Créez et activez un environnement Python :

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS / Linux
   source .venv/bin/activate
   ```


3. Lancez les tests pour vérifier l’installation :

   ```bash
   python -m pytest
   ```

## Structure du projet

- **phase1/**
  - `src/` – calculs de triangulation & Voronoï
  - `tests/` – tests unitaires phase 1
- **phase2/**
  - `chatgpt/`, `Claude/`, … – différentes implémentations d’algorithmes
  - `data/`
  - `tests/` – tests unitaires phase 2
- **phase3/** – Travaux Individuels.

---

## Phase 1 – Algorithme de base

Un algorithme développé tout seul sans utilisation d’outils d’IA, basé sur la triangulation de Delaunay et la construction du diagramme de Voronoï.

**Fonctionnalités**

- Importation de fichiers de points (`.txt`).
- Calcul de la triangulation de Delaunay (Bowyer–Watson) puis transformation en diagramme de Voronoï.
- Affichage et export (image/SVG).

**Notes techniques**

- On parcourt tous les triplets de points ; un triangle est valide s’il n’existe aucun point dans le cercle circonscrit.
- Les centres des cercles circonscrits forment les **sommets** du diagramme de Voronoï.
- Deux centres sont reliés si les triangles correspondants partagent une arête.  
  Les arêtes non partagées sont prolongées perpendiculairement vers le bord de l’espace.

Fichiers clés :  
`phase1/src/diagramme_triangulation.py` et sous‑répertoire `autres_methodes/`.

---

## Phase 2 – Multiples versions à partir plusieurs outils d’IA.

Différentes versions/modèles comparés :

- **chatgpt** – version générée avec l’aide de ChatGPT.
- **Claude** – implémentation inspirée du modèle Claude.
- **gemini** – version modulaire avec `domain.py`, `engine.py`, etc.
- **grok** – code consolidé avec interface graphique et utilitaires.

Chaque sous‑dossier comporte son propre `src/` et `tests/` pour valider la logique.

Exécution d’une version (exemple, `gemini`) :

```bash
cd phase2/gemini/src
python main.py          # lance l’interface ou le calcul
```

Tests :

```bash
python -m pytest phase2/**/*.py
```

---

## Phase 3 – Travaux individuels

Ce dossier est consacré aux recherches et réflexions personnelles de chaque membre du groupe. Les thématiques abordées peuvent inclure :

- **Environnement**
- **Coût économique, souveraineté et géopolitique**
- **Légalité et responsabilité**
- **Conséquences pour les personnes travaillant avec l'IA**
- **Qualité du logiciel et maintenance**
- **Réputation et appropriation du produit par le public**

---
