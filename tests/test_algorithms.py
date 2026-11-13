import unittest
import numpy as np
import pandas as pd
from modules.dimensionality import apply_pca, apply_tsne, apply_umap
from modules.clustering import apply_kmeans
from modules.anomaly_detection import apply_isolation_forest
from modules.evaluation import compute_metrics


class TestPCA(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame(np.random.rand(50, 4))

    def test_pca_returns_tuple(self):
        result, variance = apply_pca(self.data, n_components=2)
        self.assertEqual(result.shape, (50, 2))
        self.assertEqual(len(variance), 2)
        self.assertTrue(all(0 <= v <= 1 for v in variance))

    def test_pca_3d(self):
        result, variance = apply_pca(self.data, n_components=3)
        self.assertEqual(result.shape, (50, 3))

    def test_pca_too_many_components(self):
        with self.assertRaises(ValueError) as cm:
            apply_pca(self.data, n_components=10)
        self.assertIn("n_components", str(cm.exception).lower())


class TestTSNE(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame(np.random.rand(50, 4))

    def test_tsne_2d(self):
        result = apply_tsne(self.data, n_components=2, perplexity=5)
        self.assertEqual(result.shape, (50, 2))

    def test_tsne_invalid_perplexity(self):
        small_data = pd.DataFrame(np.random.rand(10, 4))
        with self.assertRaises(ValueError) as cm:
            apply_tsne(small_data, n_components=2, perplexity=15)
        self.assertIn("perplexity", str(cm.exception).lower())


class TestUMAP(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame(np.random.rand(50, 4))

    def test_umap_2d(self):
        result = apply_umap(self.data, n_components=2, n_neighbors=5)
        self.assertEqual(result.shape, (50, 2))


class TestClustering(unittest.TestCase):
    def setUp(self):
        self.data = np.random.rand(50, 2)

    def test_kmeans(self):
        labels, score = apply_kmeans(self.data, n_clusters=3)
        self.assertEqual(len(labels), 50)
        self.assertEqual(len(set(labels)), 3)
        self.assertGreater(score, -1)

    def test_kmeans_edge_case(self):
        labels, score = apply_kmeans(self.data, n_clusters=2)
        self.assertEqual(len(set(labels)), 2)


class TestAnomalyDetection(unittest.TestCase):
    def setUp(self):
        self.data = np.random.rand(100, 2)

    def test_isolation_forest(self):
        labels = apply_isolation_forest(self.data, contamination=0.1)
        self.assertEqual(len(labels), 100)
        self.assertTrue(all(l in (0, 1) for l in labels))


class TestEvaluation(unittest.TestCase):
    def test_compute_metrics(self):
        data = np.random.rand(50, 2)
        cluster_labels = np.array([0]*25 + [1]*25)
        anomaly_labels = np.array([0]*45 + [1]*5)
        pca_var = np.array([0.6, 0.3])
        metrics = compute_metrics(data, cluster_labels, anomaly_labels, pca_var)
        self.assertEqual(metrics["num_clusters"], 2)
        self.assertIsNotNone(metrics["silhouette_score"])
        self.assertEqual(metrics["anomaly_count"], 5)
        self.assertAlmostEqual(metrics["anomaly_pct"], 10.0)
        self.assertAlmostEqual(metrics["pca_explained_variance_total"], 0.9)


if __name__ == '__main__':
    unittest.main()
