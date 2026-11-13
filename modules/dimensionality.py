import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap


def apply_pca(data, n_components=2):
    """PCA with validation. Returns (transformed_data, explained_variance_ratio)."""
    n_features = data.shape[1] if hasattr(data, 'shape') else len(data[0])
    if n_components > n_features:
        raise ValueError(f"n_components={n_components} exceeds features={n_features}")
    pca = PCA(n_components=n_components)
    result = pca.fit_transform(data)
    return result, pca.explained_variance_ratio_


def apply_tsne(data, n_components=2, perplexity=30):
    """t-SNE with perplexity validation."""
    n_samples = data.shape[0] if hasattr(data, 'shape') else len(data)
    if perplexity >= n_samples:
        raise ValueError(f"perplexity={perplexity} must be < n_samples={n_samples}")
    tsne = TSNE(n_components=n_components, perplexity=perplexity, random_state=42)
    return tsne.fit_transform(data)


def apply_umap(data, n_components=2, n_neighbors=15, min_dist=0.1):
    """UMAP projection."""
    n_samples = data.shape[0] if hasattr(data, 'shape') else len(data)
    n_neighbors = min(n_neighbors, n_samples - 1)
    reducer = umap.UMAP(n_components=n_components, n_neighbors=n_neighbors, min_dist=min_dist, random_state=42)
    return reducer.fit_transform(data)
