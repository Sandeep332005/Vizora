import numpy as np
from scipy import signal
import networkx as nx
from typing import Dict, List, Tuple, Any
from modules.eeg_processor import ELECTRODE_MONTAGE, CHANNEL_NAMES


def compute_phase_locking_value(signals: np.ndarray) -> np.ndarray:
    """Computes pairwise Phase-Locking Value (PLV) across all channels using the Hilbert transform."""
    n_channels, n_samples = signals.shape
    # Instantaneous phase via Hilbert transform
    analytic_signal = signal.hilbert(signals, axis=1)
    phases = np.angle(analytic_signal)

    plv_matrix = np.eye(n_channels, dtype=np.float64)

    for i in range(n_channels):
        for j in range(i + 1, n_channels):
            phase_diff = phases[i] - phases[j]
            plv = np.abs(np.mean(np.exp(1j * phase_diff)))
            plv_matrix[i, j] = plv
            plv_matrix[j, i] = plv

    return plv_matrix


def compute_correlation_matrix(signals: np.ndarray) -> np.ndarray:
    """Computes absolute Pearson correlation matrix across all channels."""
    corr = np.corrcoef(signals)
    corr = np.nan_to_num(corr, nan=0.0)
    return np.abs(corr)


def build_functional_network(
    coherence_matrix: np.ndarray,
    channel_names: List[str] = CHANNEL_NAMES,
    threshold: float = 0.45,
) -> Dict[str, Any]:
    """Constructs a NetworkX graph from thresholded coherence matrix and detects Louvain communities."""
    n_channels = len(channel_names)
    G = nx.Graph()

    for idx, ch in enumerate(channel_names):
        pos = ELECTRODE_MONTAGE.get(ch, (0.0, 0.0, 0.0))
        G.add_node(ch, index=idx, pos=pos)

    edge_list = []
    for i in range(n_channels):
        for j in range(i + 1, n_channels):
            w = float(coherence_matrix[i, j])
            if w >= threshold:
                G.add_edge(channel_names[i], channel_names[j], weight=w)
                edge_list.append({
                    "source": channel_names[i],
                    "target": channel_names[j],
                    "weight": round(w, 4),
                    "pos_source": ELECTRODE_MONTAGE.get(channel_names[i], (0, 0, 0)),
                    "pos_target": ELECTRODE_MONTAGE.get(channel_names[j], (0, 0, 0)),
                })

    # Louvain community detection
    try:
        communities = list(nx.community.louvain_communities(G, seed=42))
    except Exception:
        communities = [{n} for n in G.nodes()]

    node_community = {}
    for c_idx, comm in enumerate(communities):
        for node in comm:
            node_community[node] = c_idx

    # Graph connectivity metrics
    try:
        efficiency = float(nx.global_efficiency(G))
    except Exception:
        efficiency = 0.0

    degrees = dict(G.degree())
    triu_indices = np.triu_indices(n_channels, k=1)
    mean_coherence = float(np.mean(coherence_matrix[triu_indices]))

    nodes_data = []
    for ch in channel_names:
        pos = ELECTRODE_MONTAGE.get(ch, (0.0, 0.0, 0.0))
        nodes_data.append({
            "name": ch,
            "x": pos[0],
            "y": pos[1],
            "z": pos[2],
            "community": node_community.get(ch, 0),
            "degree": degrees.get(ch, 0),
        })

    return {
        "graph": G,
        "nodes": nodes_data,
        "edges": edge_list,
        "num_communities": len(communities),
        "global_efficiency": round(efficiency, 4),
        "mean_coherence": round(mean_coherence, 4),
        "density": round(nx.density(G), 4),
    }
