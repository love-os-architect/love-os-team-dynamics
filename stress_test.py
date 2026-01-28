"""
Love-OS Stress Test Module
--------------------------
Performs destructive testing on the Team Gravity Model.
1. Monte Carlo Simulation (Noise tolerance)
2. Worst-Case Scenarios (Edge break, R-spike, Node exit)
"""

import numpy as np
import copy
import team_optimizer as love_os  # Assuming team_optimizer.py is in the same directory

def run_monte_carlo_simulation(L, V, R, S, iterations=5000, noise_scale=0.1):
    """
    Applies random noise to all parameters to estimate probability of instability.
    """
    margins = []
    unstable_count = 0
    n = len(L)

    for _ in range(iterations):
        # Apply Gaussian noise (ensure non-negative)
        L_noise = np.maximum(0, L + np.random.normal(0, noise_scale * 2, n))
        V_noise = np.maximum(0, V + np.random.normal(0, noise_scale * 2, n))
        R_noise = np.maximum(0, R + np.random.normal(0, noise_scale * 0.5, n))
        
        # S noise (clip between 0 and 1)
        S_noise = S + np.random.normal(0, noise_scale * 0.5, (n, n))
        S_noise = np.clip(S_noise, 0, 1)
        # Symmetrize S
        S_noise = (S_noise + S_noise.T) / 2

        metrics = love_os.analyze_team_state(L_noise, V_noise, R_noise, S_noise)
        margins.append(metrics['Margin'])
        
        if not metrics['Is_Stable']:
            unstable_count += 1

    return {
        "Mean_Margin": np.mean(margins),
        "Min_Margin": np.min(margins),
        "Unstable_Probability": unstable_count / iterations,
        "5th_Percentile": np.percentile(margins, 5)
    }

def run_worst_case_scenarios(L, V, R, S, kappa=0.02, eps=0.1):
    """
    Simulates 3 critical failure modes.
    """
    base_metrics = love_os.analyze_team_state(L, V, R, S, kappa, eps)
    results = {}
    n = len(L)
    G = base_metrics['G']

    # Identify Key Elements
    top_node_idx = np.argmax(G)
    
    # Find strongest edge
    max_k = -1
    strongest_edge = (0, 1)
    for i in range(n):
        for j in range(i+1, n):
            k = kappa * G[i] * G[j] * S[i, j]
            if k > max_k:
                max_k = k
                strongest_edge = (i, j)

    # --- Scenario A: Strongest Edge Break (S drops by 40%) ---
    S_broken = S.copy()
    u, v = strongest_edge
    S_broken[u, v] *= 0.6
    S_broken[v, u] *= 0.6
    res_a = love_os.analyze_team_state(L, V, R, S_broken, kappa, eps)
    results['Edge_Break'] = {
        'Description': f"Strongest Edge ({u}-{v}) S -40%",
        'Margin_Drop': base_metrics['Margin'] - res_a['Margin'],
        'New_Margin': res_a['Margin']
    }

    # --- Scenario B: Resistance Spike (R + 0.6 to top node) ---
    R_spiked = R.copy()
    R_spiked[top_node_idx] += 0.6
    res_b = love_os.analyze_team_state(L, V, R_spiked, S, kappa, eps)
    results['R_Spike'] = {
        'Description': f"Top Node ({top_node_idx}) R +0.6",
        'Margin_Drop': base_metrics['Margin'] - res_b['Margin'],
        'New_Margin': res_b['Margin']
    }

    # --- Scenario C: Key Person Exit (Remove top node) ---
    # Create reduced arrays
    mask = np.ones(n, dtype=bool)
    mask[top_node_idx] = False
    
    L_rem = L[mask]
    V_rem = V[mask]
    R_rem = R[mask]
    S_rem = S[mask][:, mask]
    
    res_c = love_os.analyze_team_state(L_rem, V_rem, R_rem, S_rem, kappa, eps)
    results['Node_Exit'] = {
        'Description': f"Top Node ({top_node_idx}) Removed",
        'Margin_Drop': base_metrics['Margin'] - res_c['Margin'],
        'New_Margin': res_c['Margin']
    }

    return results, base_metrics['Margin']

def print_stress_report(L, V, R, S, names):
    """
    Runs tests and prints a formatted report.
    """
    print("==========================================")
    print("⚡ LOVE-OS TEAM STRESS TEST REPORT ⚡")
    print("==========================================\n")

    # 1. Monte Carlo
    mc_res = run_monte_carlo_simulation(L, V, R, S)
    print(f"[1] Monte Carlo Simulation (N=5000)")
    print(f"    - Probability of Instability: {mc_res['Unstable_Probability']:.2%}")
    print(f"    - Mean Stability Margin:      {mc_res['Mean_Margin']:.2f}")
    print(f"    - Worst 5% Case Margin:       {mc_res['5th_Percentile']:.2f}")
    
    if mc_res['Unstable_Probability'] > 0.05:
        print("    ⚠️  WARNING: Team is fragile to minor shocks.")
    else:
        print("    ✅  PASSED: Team is robust against noise.")
    print("")

    # 2. Worst Case
    wc_res, base_margin = run_worst_case_scenarios(L, V, R, S)
    print(f"[2] Worst-Case Scenarios (Base Margin: {base_metrics['Margin']:.2f})")
    
    # Sort by damage
    sorted_scenarios = sorted(wc_res.items(), key=lambda x: x[1]['Margin_Drop'], reverse=True)
    
    for name, data in sorted_scenarios:
        drop_pct = (data['Margin_Drop'] / base_margin) * 100
        print(f"    💥 {name}: {data['Description']}")
        print(f"       Drop: -{data['Margin_Drop']:.2f} (-{drop_pct:.1f}%) | Result: {data['New_Margin']:.2f}")

    print("\n------------------------------------------")
    most_dangerous = sorted_scenarios[0][0]
    print(f"🛑 CRITICAL THREAT: {most_dangerous}")
    
    if most_dangerous == 'R_Spike':
        print("👉 ADVICE: Monitor ego/burnout of key leaders. Implement 'R-Guard'.")
    elif most_dangerous == 'Node_Exit':
        print("👉 ADVICE: Key Person dependency is high. Implement 'Dual-Core'.")
    elif most_dangerous == 'Edge_Break':
        print("👉 ADVICE: Key relationship is fragile. Implement 'Bridge Weaving'.")
    print("==========================================")

# --- Usage Example ---
if __name__ == "__main__":
    # Example Data (Same as simulation.ipynb)
    names = ["Sora", "Kai", "Yuki", "Hana"]
    L = np.array([12.0, 10.0, 5.0, 8.0]) 
    V = np.array([ 8.0,  6.0, 4.0, 9.0])
    R = np.array([ 0.2,  0.8, 1.5, 0.3]) 
    n = len(names)
    S = np.ones((n, n)) * 0.5
    S[0, 1] = 0.8; S[0, 2] = 0.3; S[1, 2] = 0.2

    # Need to get base_metrics for the report logic to work perfectly in main block
    # (In actual function call, base_margin is calculated inside)
    # Just running the report function:
    base_metrics = love_os.analyze_team_state(L, V, R, S)
    print_stress_report(L, V, R, S, names)
