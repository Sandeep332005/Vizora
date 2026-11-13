import unittest
import numpy as np
from modules.eeg_processor import (
    generate_eeg_simulation,
    apply_bandpass_filter,
    apply_notch_filter,
    compute_spectral_band_power,
    CHANNEL_NAMES,
    BANDS,
)
from modules.connectome import (
    compute_phase_locking_value,
    compute_correlation_matrix,
    build_functional_network,
)


class TestEEGProcessor(unittest.TestCase):
    def setUp(self):
        self.fs = 256
        self.duration = 2.0
        self.raw_signals, self.channels = generate_eeg_simulation(
            state="alpha_rest", duration_sec=self.duration, fs=self.fs, random_seed=42
        )

    def test_simulation_shape(self):
        expected_samples = int(self.duration * self.fs)
        self.assertEqual(self.raw_signals.shape, (len(CHANNEL_NAMES), expected_samples))
        self.assertEqual(len(self.channels), 16)

    def test_filter_pipeline(self):
        filtered = apply_bandpass_filter(self.raw_signals, low_cut=0.5, high_cut=50.0, fs=self.fs)
        notched = apply_notch_filter(filtered, notch_freq=50.0, fs=self.fs)
        self.assertEqual(notched.shape, self.raw_signals.shape)
        self.assertFalse(np.isnan(notched).any())
        self.assertFalse(np.isinf(notched).any())

    def test_spectral_band_decomposition(self):
        powers = compute_spectral_band_power(self.raw_signals, fs=self.fs)
        self.assertIn("relative", powers)
        for b in BANDS.keys():
            self.assertIn(b, powers["relative"])
            self.assertEqual(len(powers["relative"][b]), 16)

        # Relative power across bands should sum to ~1.0 for each channel
        rel_sum = np.zeros(16)
        for b in BANDS.keys():
            rel_sum += powers["relative"][b]
        np.testing.assert_allclose(rel_sum, np.ones(16), atol=1e-4)

    def test_alpha_dominance_in_rest(self):
        rest_sig, _ = generate_eeg_simulation(state="alpha_rest", duration_sec=2.0, fs=self.fs)
        focus_sig, _ = generate_eeg_simulation(state="beta_focus", duration_sec=2.0, fs=self.fs)
        rest_p = compute_spectral_band_power(rest_sig, fs=self.fs)
        focus_p = compute_spectral_band_power(focus_sig, fs=self.fs)

        mean_alpha_rest = np.mean(rest_p["relative"]["Alpha"])
        mean_alpha_focus = np.mean(focus_p["relative"]["Alpha"])
        self.assertGreater(mean_alpha_rest, mean_alpha_focus)


class TestConnectome(unittest.TestCase):
    def setUp(self):
        self.signals, _ = generate_eeg_simulation(state="alpha_rest", duration_sec=2.0, fs=256)

    def test_plv_mathematical_bounds(self):
        plv = compute_phase_locking_value(self.signals)
        self.assertEqual(plv.shape, (16, 16))
        # Diagonals must be exactly 1.0
        np.testing.assert_allclose(np.diag(plv), np.ones(16), atol=1e-5)
        # All values must be bounded in [0.0, 1.0]
        self.assertTrue(np.all(plv >= 0.0))
        self.assertTrue(np.all(plv <= 1.0 + 1e-6))
        # Matrix must be symmetric
        np.testing.assert_allclose(plv, plv.T, atol=1e-5)

    def test_functional_network_generation(self):
        plv = compute_phase_locking_value(self.signals)
        net = build_functional_network(plv, threshold=0.35)
        self.assertEqual(len(net["nodes"]), 16)
        self.assertGreaterEqual(net["num_communities"], 1)
        self.assertGreaterEqual(net["global_efficiency"], 0.0)
        self.assertLessEqual(net["global_efficiency"], 1.0)


if __name__ == "__main__":
    unittest.main()
