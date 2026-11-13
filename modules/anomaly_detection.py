from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
import numpy as np


def apply_isolation_forest(data, contamination=0.1):
    iso = IsolationForest(contamination=contamination, random_state=42)
    preds = iso.fit_predict(data)
    labels = np.where(preds == -1, 1, 0)
    return labels


def apply_lof(data, n_neighbors=20, contamination=0.1):
    lof = LocalOutlierFactor(n_neighbors=n_neighbors, contamination=contamination)
    preds = lof.fit_predict(data)
    labels = np.where(preds == -1, 1, 0)
    return labels
