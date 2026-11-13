import numpy as np
from scipy import signal
from typing import Dict, List, Tuple, Any

# Standard 16-channel 10-20 international montage with normalized 3D scalp coordinates (x, y, z)
ELECTRODE_MONTAGE = {
    "Fp1": (-0.30, 0.85, 0.35),
    "Fp2": (0.30, 0.85, 0.35),
    "F7":  (-0.75, 0.50, 0.20),
    "F3":  (-0.45, 0.55, 0.65),
    "F4":  (0.45, 0.55, 0.65),
    "F8":  (0.75, 0.50, 0.20),
    "T7":  (-0.85, 0.00, 0.10),
    "C3":  (-0.55, 0.00, 0.75),
    "C4":  (0.55, 0.00, 0.75),
    "T8":  (0.85, 0.00, 0.10),
    "P7":  (-0.75, -0.50, 0.20),
    "P3":  (-0.45, -0.55, 0.65),
    "P4":  (0.45, -0.55, 0.65),
    "P8":  (0.75, -0.50, 0.20),
    "O1":  (-0.30, -0.85, 0.25),
    "O2":  (0.30, -0.85, 0.25),
}

CHANNEL_NAMES = list(ELECTRODE_MONTAGE.keys())

# Frequency band boundaries (Hz)
BANDS = {
    "Delta": (0.5, 4.0),
    "Theta": (4.0, 8.0),
    "Alpha": (8.0, 13.0),
    "Beta":  (13.0, 30.0),
    "Gamma": (30.0, 45.0),
}


def generate_eeg_simulation(
    state: str = "alpha_rest",
    duration_sec: float = 2.0,
    fs: int = 256,
    noise_level: float = 0.3,
    random_seed: int = 42,
) -> Tuple[np.ndarray, List[str]]:
    """Generates realistic synthetic 16-channel EEG signals for different cognitive states."""
    np.random.seed(random_seed)
    n_samples = int(duration_sec * fs)
    t = np.linspace(0, duration_sec, n_samples, endpoint=False)
    n_channels = len(CHANNEL_NAMES)

    signals = np.zeros((n_channels, n_samples), dtype=np.float64)

    # Base background pink noise simulation (1/f)
    white_noise = np.random.randn(n_channels, n_samples)
    b, a = signal.butter(1, 0.05, btype="low")
    pink_noise = signal.filtfilt(b, a, white_noise, axis=1)

    for i, ch in enumerate(CHANNEL_NAMES):
        # Base 1/f noise
        ch_sig = pink_noise[i] * noise_level

        if state == "alpha_rest":
            # Pronounced alpha rhythm (10 Hz) in occipital and parietal regions
            if ch in ["O1", "O2", "P3", "P4", "P7", "P8"]:
                phase = np.random.uniform(0, 0.2)
                ch_sig += 1.8 * np.sin(2 * np.pi * 10.0 * t + phase)
            else:
                ch_sig += 0.4 * np.sin(2 * np.pi * 10.0 * t)

        elif state == "beta_focus":
            # Prominent beta rhythm (20 Hz) in frontal and central cortex
            if ch in ["Fp1", "Fp2", "F3", "F4", "F7", "F8", "C3", "C4"]:
                phase = np.random.uniform(0, 0.3)
                ch_sig += 1.6 * np.sin(2 * np.pi * 20.0 * t + phase)
            else:
                ch_sig += 0.5 * np.sin(2 * np.pi * 20.0 * t)

        elif state == "theta_fatigue":
            # Prominent theta rhythm (6 Hz) characteristic of drowsiness/fatigue
            if ch in ["F3", "F4", "C3", "C4"]:
                ch_sig += 1.7 * np.sin(2 * np.pi * 6.0 * t)
            else:
                ch_sig += 0.6 * np.sin(2 * np.pi * 6.0 * t)

        elif state == "spike_anomaly":
            # Paroxysmal epileptiform sharp transients / spikes
            ch_sig += 0.5 * np.sin(2 * np.pi * 8.0 * t)
            spike_times = [int(0.5 * fs), int(1.2 * fs), int(1.7 * fs)]
            for st_idx in spike_times:
                if 0 <= st_idx < n_samples - 20:
                    spike_shape = -np.exp(-((np.arange(20) - 10) ** 2) / 6.0) * 5.0
                    ch_sig[st_idx:st_idx + 20] += spike_shape

        signals[i] = ch_sig

    return signals, CHANNEL_NAMES


def apply_bandpass_filter(
    signals: np.ndarray,
    low_cut: float = 0.5,
    high_cut: float = 50.0,
    fs: int = 256,
    order: int = 4,
) -> np.ndarray:
    """Zero-phase Butterworth bandpass filter across all channels."""
    nyq = 0.5 * fs
    low = max(0.01, low_cut / nyq)
    high = min(0.99, high_cut / nyq)
    b, a = signal.butter(order, [low, high], btype="band")
    return signal.filtfilt(b, a, signals, axis=1)


def apply_notch_filter(
    signals: np.ndarray,
    notch_freq: float = 50.0,
    fs: int = 256,
    quality_factor: float = 30.0,
) -> np.ndarray:
    """Notch filter for 50 Hz or 60 Hz electrical mains noise elimination."""
    nyq = 0.5 * fs
    freq = notch_freq / nyq
    if 0 < freq < 1:
        b, a = signal.iirnotch(freq, quality_factor)
        return signal.filtfilt(b, a, signals, axis=1)
    return signals


def compute_spectral_band_power(
    signals: np.ndarray,
    fs: int = 256,
) -> Dict[str, Any]:
    """Computes Welch Power Spectral Density and relative power for Delta, Theta, Alpha, Beta, Gamma."""
    n_channels = signals.shape[0]
    nperseg = min(signals.shape[1], int(fs * 1.0))
    freqs, psd = signal.welch(signals, fs=fs, nperseg=nperseg, axis=1)

    band_powers = {b: np.zeros(n_channels) for b in BANDS}
    total_power = np.zeros(n_channels)

    for band_name, (f_low, f_high) in BANDS.items():
        idx_band = np.logical_and(freqs >= f_low, freqs <= f_high)
        # Trapezoidal numerical integration of spectral density
        bp = np.trapezoid(psd[:, idx_band], freqs[idx_band], axis=1) if hasattr(np, "trapezoid") else np.trapz(psd[:, idx_band], freqs[idx_band], axis=1)
        band_powers[band_name] = bp

    for bp in band_powers.values():
        total_power += bp

    total_power[total_power == 0] = 1e-9
    relative_powers = {b: band_powers[b] / total_power for b in BANDS}

    # Aggregate feature vector: channels × 5 bands
    feature_matrix = np.column_stack([relative_powers[b] for b in BANDS])
    feature_vector = feature_matrix.flatten()

    return {
        "freqs": freqs,
        "psd": psd,
        "absolute": band_powers,
        "relative": relative_powers,
        "feature_vector": feature_vector,
        "mean_alpha_beta_ratio": float(np.mean(relative_powers["Alpha"] / (relative_powers["Beta"] + 1e-6))),
    }
