import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


def plot_2d(result, labels=None, title="2D Projection", color_label="Cluster"):
    """Interactive 2D scatter plot."""
    df_plot = pd.DataFrame(result[:, :2], columns=["Dim1", "Dim2"])
    if labels is not None:
        df_plot[color_label] = [str(l) for l in labels]
        fig = px.scatter(df_plot, x="Dim1", y="Dim2", color=color_label,
                         title=title, template="plotly_dark",
                         hover_data={color_label: True})
    else:
        fig = px.scatter(df_plot, x="Dim1", y="Dim2", title=title, template="plotly_dark")
    fig.update_layout(height=500)
    return fig


def plot_3d(result, labels=None, title="3D Projection", color_label="Cluster"):
    """Interactive 3D scatter plot."""
    df_plot = pd.DataFrame(result[:, :3], columns=["Dim1", "Dim2", "Dim3"])
    if labels is not None:
        df_plot[color_label] = [str(l) for l in labels]
        fig = px.scatter_3d(df_plot, x="Dim1", y="Dim2", z="Dim3", color=color_label,
                            title=title, template="plotly_dark",
                            hover_data={color_label: True})
    else:
        fig = px.scatter_3d(df_plot, x="Dim1", y="Dim2", z="Dim3", title=title, template="plotly_dark")
    fig.update_layout(height=600)
    return fig


def plot_explained_variance(variance_ratio):
    """Bar chart of PCA explained variance per component."""
    components = [f"PC{i+1}" for i in range(len(variance_ratio))]
    cumulative = np.cumsum(variance_ratio)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=components, y=variance_ratio, name="Individual", marker_color="#636EFA"))
    fig.add_trace(go.Scatter(x=components, y=cumulative, name="Cumulative", mode="lines+markers",
                             marker_color="#EF553B"))
    fig.update_layout(title="PCA Explained Variance", template="plotly_dark",
                      yaxis_title="Variance Ratio", height=400)
    return fig


def plot_anomalies_2d(result, anomaly_labels, title="Anomaly Detection"):
    """2D scatter with anomalies highlighted in red."""
    df_plot = pd.DataFrame(result[:, :2], columns=["Dim1", "Dim2"])
    df_plot["Type"] = ["Anomaly" if a == 1 else "Normal" for a in anomaly_labels]
    fig = px.scatter(df_plot, x="Dim1", y="Dim2", color="Type",
                     color_discrete_map={"Normal": "#636EFA", "Anomaly": "#EF553B"},
                     title=title, template="plotly_dark")
    fig.update_layout(height=500)
    return fig


def generate_report_html(metrics, figures):
    """Generates a standalone HTML report with metrics and plots."""
    plots_html = ""
    for name, fig in figures.items():
        plots_html += f"<h2>{name}</h2>\n{fig.to_html(full_html=False)}\n"

    metrics_rows = "".join(f"<tr><td><b>{k}</b></td><td>{v}</td></tr>" for k, v in metrics.items())
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>VIZORA Analysis Report</title>
<style>body{{font-family:system-ui;max-width:1200px;margin:auto;padding:20px;background:#1a1a2e;color:#eee}}
table{{border-collapse:collapse;width:100%}}td{{padding:8px;border-bottom:1px solid #333}}</style></head>
<body><h1>VIZORA Analysis Report</h1>
<table>{metrics_rows}</table>
{plots_html}
</body></html>"""
