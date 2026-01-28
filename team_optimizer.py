"""
Love-OS Team Dynamics Optimizer
-------------------------------
Implements the N-Body Gravity Model for organizational analysis.
Calculates Stability Margins and suggests optimal interventions (Greedy/PGD).
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# --- Core Physics Engine ---

def compute_individual_gravity(L, V, R, eps=0.1):
    """
    Calculates G = (L^2 * V) / (R + eps)
    """
    return (np.array(L)**2 * np.array(V)) / (np.array(R) + eps)

def analyze_team_state(L, V, R, S, kappa=0.02, eps=0.1):
    """
    Computes global team metrics:
    - G: Individual Gravities
    - K_team: Total Binding Energy (Synergy)
    - D_team: Total Dispersion Energy (Friction)
    - Margin: K - D (Stability Score)
    """
    n = len(L)
    G = compute_individual_gravity(L, V, R, eps)
    
    K_team = 0.0
    for i in range(n):
        for j in range(i+1, n):
            # Mutual Gravity k = kappa * Gi * Gj * Sij
            K_team += kappa * G[i] * G[j] * S[i, j]
            
    # Dispersion D = Sum(R) + Sum(Misalignment)
    misalignment = np.triu(1 - S, 1).sum()
    D_team = R.sum() + misalignment
    
    return {
        "G": G,
        "K_team": K_team,
        "D_team": D_team,
        "Margin": K_team - D_team,
        "Is_Stable": K_team > D_team
    }

def calculate_marginal_gains(L, V, R, S, kappa=0.02, eps=0.1):
    """
    Computes partial derivatives (Sensitivity Analysis).
    Returns the impact of changing L, V, R, S on the Stability Margin.
    """
    n = len(L)
    G = compute_individual_gravity(L, V, R, eps)
    
    # Pre-compute weighted sum of interactions for each node
    # Term: kappa * Sum(Sij * Gj)
    interaction_sum = np.array([
        sum(kappa * S[i, j] * G[j] for j in range(n) if i != j)
        for i in range(n)
    ])

    # 1. Derivative w.r.t R (Resistance)
    # dG/dR = -(L^2 * V) / (R+eps)^2
    dG_dR = -(L**2 * V) / (R + eps)**2
    # dM/dR = (Interaction * dG/dR) - 1
    dM_dR = (interaction_sum * dG_dR) - 1.0

    # 2. Derivative w.r.t S (Resonance)
    # dM/dSij = kappa * Gi * Gj + 1
    dM_dS = np.zeros_like(S)
    for i in range(n):
        for j in range(i+1, n):
            val = kappa * G[i] * G[j] + 1.0
            dM_dS[i, j] = dM_dS[j, i] = val

    return dM_dR, dM_dS

# --- Optimization Algorithm ---

def suggest_interventions(L, V, R, S, costs, budget, step=0.1, kappa=0.02, eps=0.1):
    """
    Greedy Strategy: Finds the highest ROI moves to improve Team Stability.
    
    costs: dict with keys 'cR', 'cS' (cost per unit change)
    """
    dM_dR, dM_dS = calculate_marginal_gains(L, V, R, S, kappa, eps)
    suggestions = []
    n = len(L)

    # A. Analyze R-Reduction (Reducing Ego/Fear)
    for i in range(n):
        # Gain is -dM/dR * step (since we reduce R)
        gain = -dM_dR[i] * step
        cost = costs['cR'][i] * step
        if cost > 0:
            roi = gain / cost
            suggestions.append({
                "Type": "Reduce Resistance (R)",
                "Target": i,
                "Target_2": None,
                "ROI": roi,
                "Cost": cost,
                "Impact": gain
            })

    # B. Analyze S-Boost (Improving Communication/Trust)
    for i in range(n):
        for j in range(i+1, n):
            gain = dM_dS[i, j] * step
            cost = costs['cS'][i, j] * step
            if cost > 0:
                roi = gain / cost
                suggestions.append({
                    "Type": "Boost Resonance (S)",
                    "Target": i,
                    "Target_2": j,
                    "ROI": roi,
                    "Cost": cost,
                    "Impact": gain
                })

    # Sort by ROI
    suggestions.sort(key=lambda x: x['ROI'], reverse=True)
    
    # Filter by Budget
    valid_moves = []
    current_spend = 0
    for move in suggestions:
        if current_spend + move['Cost'] <= budget:
            valid_moves.append(move)
            current_spend += move['Cost']
            
    return valid_moves

# --- Visualization ---

def visualize_gravity_network(L, V, R, S, member_names, kappa=0.02, eps=0.1):
    """
    Plots the Team Gravity Network.
    Node Size = Gravity (G)
    Edge Width = Interaction Force (k)
    Edge Color = Resonance (S)
    """
    metrics = analyze_team_state(L, V, R, S, kappa, eps)
    G = metrics["G"]
    
    graph = nx.Graph()
    n = len(L)
    
    # Add Nodes
    for i in range(n):
        graph.add_node(i, label=member_names[i], size=G[i])
        
    # Add Edges
    for i in range(n):
        for j in range(i+1, n):
            weight = kappa * G[i] * G[j] * S[i, j]
            if weight > 0.5: # Visualize significant connections
                graph.add_edge(i, j, weight=weight, resonance=S[i, j])

    pos = nx.spring_layout(graph, k=1.5, seed=42)
    plt.figure(figsize=(10, 8))
    
    # Nodes
    node_sizes = [graph.nodes[n]['size'] * 2 for n in graph.nodes()]
    nx.draw_networkx_nodes(graph, pos, node_size=node_sizes, node_color="#9370DB", alpha=0.9)
    nx.draw_networkx_labels(graph, pos, labels={i: member_names[i] for i in range(n)}, font_color="white", font_weight="bold")
    
    # Edges
    edges = graph.edges(data=True)
    weights = [d['weight'] * 0.5 for u, v, d in edges]
    colors = [d['resonance'] for u, v, d in edges]
    
    nx.draw_networkx_edges(graph, pos, width=weights, edge_color=colors, edge_cmap=plt.cm.coolwarm, edge_vmin=0, edge_vmax=1)
    
    plt.title(f"Love-OS Gravity Network\nStability Margin: {metrics['Margin']:.2f}", fontsize=14)
    plt.axis('off')
    plt.show()
