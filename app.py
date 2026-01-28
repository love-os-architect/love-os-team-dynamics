import streamlit as st
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# ==========================================
# 🌌 PHYSICS ENGINE (Love-OS Kernel)
# ==========================================

CONST_KAPPA = 0.02
CONST_EPSILON = 0.1

def compute_gravity(L, V, R):
    """ G = L^2 * V / (R + epsilon) """
    return (L**2 * V) / (R + CONST_EPSILON)

def analyze_team(df_nodes, df_edges):
    """ Calculate K (Binding Energy) vs D (Dispersion Energy) """
    nodes = df_nodes.set_index('name').T.to_dict()
    G_map = {}
    
    # 1. Calculate Individual Gravity (G)
    for name, params in nodes.items():
        G = compute_gravity(params['L'], params['V'], params['R'])
        G_map[name] = G
        nodes[name]['G'] = G

    # 2. Calculate Team Metrics
    K_total = 0.0
    misalignment = 0.0
    
    # Process edges
    active_edges = []
    for _, row in df_edges.iterrows():
        p1, p2, s = row['source'], row['target'], row['S']
        if p1 in G_map and p2 in G_map:
            k = CONST_KAPPA * G_map[p1] * G_map[p2] * s
            K_total += k
            misalignment += (1.0 - s)
            active_edges.append({'p1': p1, 'p2': p2, 'weight': k, 'S': s})

    # D = Sum(R) + Sum(1-S)
    R_total = sum(p['R'] for p in nodes.values())
    D_total = R_total + misalignment
    
    margin = K_total - D_total
    
    return {
        'G_map': G_map,
        'nodes': nodes,
        'edges': active_edges,
        'K': K_total,
        'D': D_total,
        'Margin': margin,
        'Is_Stable': margin > 0
    }

def suggest_action(nodes, edges_data):
    """ Simple Greedy AI for Suggestion """
    # Find highest R
    worst_R_node = max(nodes.items(), key=lambda x: x[1]['R'])
    # Find strongest potential G
    best_G_node = max(nodes.items(), key=lambda x: x[1]['G'])
    
    actions = []
    
    # Rule 1: R-Spike Check
    if worst_R_node[1]['R'] > 1.0:
        actions.append(f"⚠️ **CRITICAL:** {worst_R_node[0]}'s Resistance is too high (R={worst_R_node[1]['R']}). Immediate rest required.")
    
    # Rule 2: Vacuum Check
    if best_G_node[1]['V'] < 3.0:
        actions.append(f"🛑 **WARNING:** Leader {best_G_node[0]} has no Vacuum (V={best_G_node[1]['V']}). Burnout imminent.")
        
    if not actions:
        actions.append("✅ **STATUS GREEN:** System is stable. Focus on increasing L (Integration).")
        
    return actions

# ==========================================
# 📱 UI / UX (Streamlit App)
# ==========================================

st.set_page_config(page_title="Love-OS Kernel", layout="wide", page_icon="🧬")

# Sidebar: Personal Calibration
st.sidebar.header("🧬 Commander Status")
st.sidebar.markdown("Input your current parameters:")

my_L = st.sidebar.slider("L (Love/Mass)", 0.0, 12.0, 10.0, help="Integration level, Skill, Will")
my_V = st.sidebar.slider("V (Vacuum)", 0.0, 12.0, 6.0, help="Inner space, Time, Capacity")
my_R = st.sidebar.slider("R (Resistance)", 0.0, 3.0, 0.5, help="Ego, Fear, Friction")

my_G = compute_gravity(my_L, my_V, my_R)
st.sidebar.metric("Your Gravity (G)", f"{my_G:.1f}", delta=f"R: {my_R}")

st.sidebar.markdown("---")
st.sidebar.markdown("**Love-OS v0.1**\n*Physics of Awakening*")

# Main Area
st.title("Love-OS Tactical Dashboard 🪐")
st.markdown("### Organizational Gravity & Stability Analysis")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("1. Team Configuration")
    
    # Default Data
    default_nodes = pd.DataFrame([
        {'name': 'Commander (You)', 'L': my_L, 'V': my_V, 'R': my_R},
        {'name': 'Ace (Kai)',       'L': 10.0, 'V': 5.0,  'R': 0.8},
        {'name': 'Blocker (Yuki)',  'L': 6.0,  'V': 4.0,  'R': 1.5},
        {'name': 'New (Hana)',      'L': 8.0,  'V': 8.0,  'R': 0.2}
    ])
    
    edited_nodes = st.data_editor(default_nodes, num_rows="dynamic", key="nodes_editor")
    
    st.markdown("---")
    st.markdown("**Resonance (S) Matrix**")
    
    # Simple Edge Creator for Demo
    node_names = edited_nodes['name'].tolist()
    default_edges = pd.DataFrame([
        {'source': node_names[0], 'target': node_names[1], 'S': 0.9},
        {'source': node_names[0], 'target': node_names[2], 'S': 0.3},
        {'source': node_names[1], 'target': node_names[2], 'S': 0.2},
    ])
    edited_edges = st.data_editor(default_edges, num_rows="dynamic", key="edges_editor")

with col2:
    st.subheader("2. Gravity Network Visualization")
    
    # Run Analysis
    try:
        metrics = analyze_team(edited_nodes, edited_edges)
        
        # Display Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Binding Energy (K)", f"{metrics['K']:.0f}")
        m2.metric("Friction (D)", f"{metrics['D']:.1f}")
        m3.metric("Stability Margin", f"{metrics['Margin']:.0f}", 
                  delta="STABLE" if metrics['Is_Stable'] else "COLLAPSE",
                  delta_color="normal" if metrics['Is_Stable'] else "inverse")
        
        # Draw Graph
        G = nx.Graph()
        for name, data in metrics['nodes'].items():
            G.add_node(name, size=data['G'], R=data['R'])
        for edge in metrics['edges']:
            G.add_edge(edge['p1'], edge['p2'], weight=edge['weight'], S=edge['S'])
            
        fig, ax = plt.subplots(figsize=(8, 6))
        pos = nx.spring_layout(G, k=2.0, seed=42)
        
        # Draw Nodes
        node_sizes = [metrics['nodes'][n]['G'] * 2 for n in G.nodes()]
        node_colors = [metrics['nodes'][n]['R'] for n in G.nodes()]
        
        nodes = nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, 
                               cmap=plt.cm.coolwarm, vmin=0, vmax=2.0, edgecolors='black')
        
        # Draw Edges
        edge_weights = [d['weight'] * 0.01 for u,v,d in G.edges(data=True)]
        edge_colors = [d['S'] for u,v,d in G.edges(data=True)]
        
        nx.draw_networkx_edges(G, pos, width=edge_weights, edge_color=edge_colors, 
                               edge_cmap=plt.cm.Greens, edge_vmin=0, edge_vmax=1.0)
        
        nx.draw_networkx_labels(G, pos, font_color='black', font_weight='bold')
        
        # Colorbars
        cbar = plt.colorbar(nodes, ax=ax, label="Resistance (Red=High Risk)")
        
        ax.axis('off')
        st.pyplot(fig)
        
        # AI Prescription
        st.subheader("3. AI Tactical Advice")
        advice_list = suggest_action(metrics['nodes'], edited_edges)
        for advice in advice_list:
            st.info(advice)
            
    except Exception as e:
        st.error(f"Simulation Error: {e}")
        st.caption("Please ensure names in Edges match Names in Nodes.")
