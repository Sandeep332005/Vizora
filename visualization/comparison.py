import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np


def plot_comparison(results_dict, labels=None):
    """Side-by-side 2D comparison of multiple algorithms."""
    names = list(results_dict.keys())
    n = len(names)
    fig = make_subplots(rows=1, cols=n, subplot_titles=names, horizontal_spacing=0.05)

    colors = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A"]

    for i, name in enumerate(names):
        result = results_dict[name]
        x = result[:, 0]
        y = result[:, 1]
        if labels is not None:
            unique_labels = sorted(set(labels))
            for j, lab in enumerate(unique_labels):
                mask = np.array(labels) == lab
                fig.add_trace(
                    go.Scatter(x=x[mask], y=y[mask], mode="markers", name=f"{name} C{lab}",
                               marker=dict(color=colors[j % len(colors)], size=5),
                               showlegend=(i == 0)),
                    row=1, col=i + 1)
        else:
            fig.add_trace(
                go.Scatter(x=x, y=y, mode="markers", name=name,
                           marker=dict(color=colors[i % len(colors)], size=5)),
                row=1, col=i + 1)

    fig.update_layout(height=500, title_text="Algorithm Comparison (2D)", template="plotly_dark")
    return fig
