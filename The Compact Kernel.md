# Love-OS Team Dynamics: The Compact Kernel

[![Version](https://img.shields.io/badge/Love--OS-v0.7-purple)]()
[![Build](https://img.shields.io/badge/Status-Stable-green)]()
[![License](https://img.shields.io/badge/License-MIT-blue)]()

## 🌌 Overview

The **Love-OS Team Compressor** is a diagnostic engine that distills complex N-body organizational dynamics into **minimal viable signals**.

Instead of storing massive interaction logs, this kernel applies the "Physics of Awakening" ($G = L^2 V / R$) to calculate the gravitational stability of a team. It performs real-time destructive stress testing and outputs a **3-Layer Compressed Report** for decision-making.

## 📐 The 3-Layer Compression Architecture

To make the model usable for mobile apps and real-time dashboards, we compress the data into three layers:

### Layer 1: Executive 1-Pager (Decision)
A single text summary for leaders.
- **TGI (Team Gravity Index):** The fundamental "health score" of the cluster.
- **Top Risk:** Identifies the single most dangerous failure mode (e.g., "Leader Burnout").
- **Action:** One immediate prescription (e.g., "Reduce Resistance for Alice").

### Layer 2: Resilience Triplet (Metrics)
Three sensitivity metrics tracking the team's fragility:
1.  **R-Sensitivity:** Vulnerability to ego/stress spikes.
2.  **Exit-Sensitivity:** Vulnerability to key person departure (Bus Factor).
3.  **Edge-Sensitivity:** Vulnerability to relationship conflicts.

### Layer 3: Lightweight JSON (System)
A minimal JSON payload (< 5KB) containing the pruned topology.
- **Node Compression:** Stores only state parameters ($L, V, R, G$).
- **Edge Pruning:** Retains only the top edges contributing to 90% of the Binding Energy ($K$).

  ### 3. Input Data Format (Example)
The model accepts a list of nodes (members) and a resonance matrix ($S$).
See `team_compressor.py` for the demo data structure.

## 🧠 Core Physics

**Individual Gravity ($G$):**
$$
G_i = \frac{L_i^2 \cdot V_i}{R_i + \varepsilon}
$$
*Where $L$=Integration (Love), $V$=Vacuum, $R$=Resistance.*

**Binding Energy ($K$):**
$$
K_{\text{team}} = \sum_{i<j} \kappa \cdot G_i \cdot G_j \cdot S_{ij}
$$

**Stability Margin ($\mathcal{M}$):**
$$
\mathcal{M} = K_{\text{team}} - D_{\text{team}}
$$


## 🚀 Usage

### 1. Installation
```bash
pip install -r requirements.txt
```
---
*Architected by the Love-OS Project.*
