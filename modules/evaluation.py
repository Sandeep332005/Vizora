import numpy as np
from sklearn.metrics import silhouette_score


def compute_metrics(data, cluster_labels, anomaly_labels, pca_explained_variance=None):
    """Computes evaluation metrics for the analysis session."""
    metrics = {}

    n_clusters = len(set(cluster_labels))
    metrics["num_clusters"] = n_clusters
    if n_clusters > 1:
        metrics["silhouette_score"] = round(float(silhouette_score(data, cluster_labels)), 4)
    else:
        metrics["silhouette_score"] = None

    anomaly_arr = np.array(anomaly_labels)
    metrics["total_samples"] = len(anomaly_arr)
    metrics["anomaly_count"] = int(anomaly_arr.sum())
    metrics["anomaly_pct"] = round(float(anomaly_arr.mean() * 100), 2)

    if pca_explained_variance is not None:
        metrics["pca_explained_variance_total"] = round(float(np.sum(pca_explained_variance)), 4)
        metrics["pca_explained_variance_per_component"] = [round(float(v), 4) for v in pca_explained_variance]

    return metrics
