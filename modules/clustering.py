from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.metrics import silhouette_score, davies_bouldin_score
import numpy as np


def apply_kmeans(data, n_clusters=3):
    n_samples = data.shape[0] if hasattr(data, 'shape') else len(data)
    n_clusters = min(n_clusters, n_samples - 1)
    if n_clusters < 2:
        labels = np.zeros(n_samples, dtype=int)
        return labels, -1.0

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(data)

    score = silhouette_score(data, labels) if len(set(labels)) > 1 else -1.0
    return labels, score


def apply_dbscan(data, eps=0.5, min_samples=5):
    db = DBSCAN(eps=eps, min_samples=min_samples)
    labels = db.fit_predict(data)
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    score = silhouette_score(data, labels) if n_clusters > 1 else -1.0
    return labels, score


def apply_hierarchical(data, n_clusters=3):
    n_samples = data.shape[0] if hasattr(data, 'shape') else len(data)
    n_clusters = min(n_clusters, n_samples - 1)
    if n_clusters < 2:
        return np.zeros(n_samples, dtype=int), -1.0
    hc = AgglomerativeClustering(n_clusters=n_clusters)
    labels = hc.fit_predict(data)
    score = silhouette_score(data, labels) if len(set(labels)) > 1 else -1.0
    return labels, score


def compute_davies_bouldin(data, labels):
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    if n_clusters < 2:
        return -1.0
    mask = np.array(labels) != -1
    if mask.sum() < 2:
        return -1.0
    return davies_bouldin_score(data[mask], np.array(labels)[mask])
