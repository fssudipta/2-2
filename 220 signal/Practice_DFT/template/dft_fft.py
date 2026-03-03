import numpy as np
import time
import matplotlib.pyplot as plt
 
EPS = 1e-12
 
# ----------------------------
# Error metrics
# ----------------------------
def max_abs_error(a, b):
    a = np.asarray(a); b = np.asarray(b)
    return np.max(np.abs(a - b))
 
def rel_l2_error(a, b):
    a = np.asarray(a); b = np.asarray(b)
    return np.linalg.norm(a - b) / (np.linalg.norm(a) + EPS)
 
# ----------------------------
# Discrete signal (OOP)
# ----------------------------
class DiscreteSignal:
    def __init__(self, data):
        self.data = np.array(data, dtype=np.complex128)
 
    def __len__(self):
        return len(self.data)
 
    def copy(self):
        return DiscreteSignal(self.data.copy())
 
    def pad(self, new_length):
        new_length = int(new_length)
        x = self.data
        out = np.zeros(new_length, dtype=np.complex128)
        L = min(len(x), new_length)
        out[:L] = x[:L]
        return DiscreteSignal(out)
 
    def interpolate(self, new_length):
        # For completeness (UI apps), but for DFT property proofs prefer pad(), not interpolate().
        N = len(self.data)
        new_length = int(new_length)
        old_n = np.arange(N)
        new_n = np.linspace(0, N - 1, new_length)
        re = np.interp(new_n, old_n, np.real(self.data))
        im = np.interp(new_n, old_n, np.imag(self.data))
        return DiscreteSignal(re + 1j * im)
 
    # --- Time-domain transformations ---
    def scale(self, a):
        return DiscreteSignal(a * self.data)
 
    def add(self, other: "DiscreteSignal"):
        if len(self) != len(other):
            raise ValueError("Length mismatch")
        return DiscreteSignal(self.data + other.data)
 
    def circular_shift(self, m):
        N = len(self.data)
        n = np.arange(N)
        return DiscreteSignal(self.data[(n - m) % N])  # x[(n-m) mod N]
 
    def modulate_bins(self, m):
        # Multiply by exp(+j2πmn/N): circular frequency shift by m bins.
        N = len(self.data)
        n = np.arange(N)
        return DiscreteSignal(self.data * np.exp(2j * np.pi * m * n / N))
 
    def time_reverse(self):
        # x[(-n) mod N]
        N = len(self.data)
        n = np.arange(N)
        return DiscreteSignal(self.data[(-n) % N])
 
    def conjugate(self):
        return DiscreteSignal(np.conjugate(self.data))
 
    def apply_window(self, w):
        w = np.asarray(w, dtype=np.float64)
        if len(w) != len(self.data):
            raise ValueError("Window length mismatch")
        return DiscreteSignal(self.data * w)
 
    # --- “Forbidden built-in conv/corr” replacements ---
    def circular_convolve(self, other: "DiscreteSignal"):
        if len(self) != len(other):
            raise ValueError("Length mismatch")
        x = self.data
        h = other.data
        N = len(x)
        y = np.zeros(N, dtype=np.complex128)
        for n in range(N):
            s = 0j
            for m in range(N):
                s += x[m] * h[(n - m) % N]
            y[n] = s
        return DiscreteSignal(y)
 
    def linear_convolve(self, other: "DiscreteSignal"):
        x = self.data
        h = other.data
        Lx, Lh = len(x), len(h)
        y = np.zeros(Lx + Lh - 1, dtype=np.complex128)
        for n in range(Lx + Lh - 1):
            s = 0j
            m_min = max(0, n - (Lh - 1))
            m_max = min(n, Lx - 1)
            for m in range(m_min, m_max + 1):
                s += x[m] * h[n - m]
            y[n] = s
        return DiscreteSignal(y)
 
    def circular_corr(self, other: "DiscreteSignal"):
        # One common circular definition:
        # r_xy[l] = sum_n x[n] * conj(y[(n-l) mod N])
        if len(self) != len(other):
            raise ValueError("Length mismatch")
        x = self.data
        y = other.data
        N = len(x)
        r = np.zeros(N, dtype=np.complex128)
        for l in range(N):
            s = 0j
            for n in range(N):
                s += x[n] * np.conjugate(y[(n - l) % N])
            r[l] = s
        return DiscreteSignal(r)
 
# ----------------------------
# Analyzers (DFT / FFT / Bluestein)
# ----------------------------
class DFTAnalyzer:
    # O(N^2)
    def compute_dft(self, signal: DiscreteSignal):
        N = len(signal)
        n = np.arange(N)
        k = np.arange(N).reshape(-1, 1)
        W = np.exp(-2j * np.pi * k * n / N)
        return W @ signal.data
 
    def compute_idft(self, spectrum):
        X = np.asarray(spectrum, dtype=np.complex128)
        N = len(X)
        n = np.arange(N)
        k = np.arange(N).reshape(-1, 1)
        W = np.exp(2j * np.pi * k * n / N)
        return np.asarray((W @ X) / N, dtype=np.complex128)
 
class Radix2FFT(DFTAnalyzer):
    # Radix-2 recursive DIT FFT, requires N power-of-two.
    def _is_pow2(self, N):
        return N > 0 and (N & (N - 1)) == 0
 
    def _fft_rec(self, x):
        N = len(x)
        if N == 1:
            return x
        Xe = self._fft_rec(x[::2])
        Xo = self._fft_rec(x[1::2])
        k = np.arange(N // 2)
        tw = np.exp(-2j * np.pi * k / N) * Xo
        return np.concatenate([Xe + tw, Xe - tw])
 
    def compute_dft(self, signal: DiscreteSignal):
        x = signal.data
        N = len(x)
        if not self._is_pow2(N):
            raise ValueError("Radix2FFT requires N to be a power of 2 (pad with zeros first).")
        return self._fft_rec(x)
 
    def compute_idft(self, spectrum):
        X = np.asarray(spectrum, dtype=np.complex128)
        N = len(X)
        if not self._is_pow2(N):
            raise ValueError("Radix2FFT requires N to be a power of 2.")
        return np.asarray(np.conjugate(self._fft_rec(np.conjugate(X))) / N, dtype=np.complex128)
 
class BlueStein(Radix2FFT):
    # DFT for arbitrary N using chirp-z / Bluestein; uses Radix2FFT internally for convolution.
    def _next_pow2(self, n):
        p = 1
        while p < n:
            p <<= 1
        return p
 
    def compute_dft(self, signal: DiscreteSignal):
        x = signal.data
        N = len(x)
        n = np.arange(N)
        W = np.exp(-1j * np.pi * (n ** 2) / N)
        chirp = np.conjugate(W)
 
        a = x * W
        M = self._next_pow2(2 * N - 1)
 
        b = np.zeros(M, dtype=np.complex128)
        b[:N] = chirp
        b[M - N + 1:] = chirp[1:][::-1]
 
        a_pad = np.zeros(M, dtype=np.complex128)
        a_pad[:N] = a
 
        A = self._fft_rec(a_pad)
        B = self._fft_rec(b)
        conv = np.conjugate(self._fft_rec(np.conjugate(A * B))) / M
 
        return W * conv[:N]
 
    def compute_idft(self, spectrum):
        X = np.asarray(spectrum, dtype=np.complex128)
        N = len(X)
        return np.asarray(np.conjugate(self.compute_dft(DiscreteSignal(np.conjugate(X)))) / N, dtype=np.complex128)
 
# ----------------------------
# DFT property predictions (spectrum-domain)
# ----------------------------
class DFTProperties:
    @staticmethod
    def predicted_linearity(X1, X2, a, b):
        return a * X1 + b * X2
 
    @staticmethod
    def predicted_shift(X, m):
        N = len(X)
        k = np.arange(N)
        return X * np.exp(-2j * np.pi * m * k / N)
 
    @staticmethod
    def predicted_modulation(X, m):
        N = len(X)
        k = np.arange(N)
        return X[(k - m) % N]
 
    @staticmethod
    def predicted_time_reverse(X):
        N = len(X)
        k = np.arange(N)
        return X[(-k) % N]
 
    @staticmethod
    def predicted_conjugate(X):
        N = len(X)
        k = np.arange(N)
        return np.conjugate(X[(-k) % N])
 
# ----------------------------
# Windows + spectrum helpers
# ----------------------------
class Windows:
    @staticmethod
    def rectangular(N):
        return np.ones(int(N))
 
    @staticmethod
    def hann(N):
        N = int(N)
        n = np.arange(N)
        return 0.5 - 0.5 * np.cos(2 * np.pi * n / (N - 1 + EPS))
 
    @staticmethod
    def hamming(N):
        N = int(N)
        n = np.arange(N)
        return 0.54 - 0.46 * np.cos(2 * np.pi * n / (N - 1 + EPS))
 
class SpectrumTools:
    @staticmethod
    def freq_axis_hz(N, Fs):
        # DFT bin k corresponds to frequency k*Fs/N (0..Fs*(N-1)/N)
        k = np.arange(int(N))
        return k * (Fs / N)
 
    @staticmethod
    def mag_phase(X):
        X = np.asarray(X, dtype=np.complex128)
        return np.abs(X), np.angle(X)
 
    @staticmethod
    def plot_mag_phase_hz(X, Fs, title_prefix=""):
        N = len(X)
        f = SpectrumTools.freq_axis_hz(N, Fs)
        mag, ph = SpectrumTools.mag_phase(X)
 
        plt.figure()
        plt.stem(f, mag)
        plt.title(f"{title_prefix}Magnitude Spectrum")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("|X[k]|")
        plt.grid(True)
 
        plt.figure()
        plt.stem(f, ph)
        plt.title(f"{title_prefix}Phase Spectrum")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("∠X[k] (rad)")
        plt.grid(True)
 
# ----------------------------
# Lab tasks (each is a typical test question)
# ----------------------------
class LabTasks:
    def __init__(self, analyzer):
        self.A = analyzer
 
    # 1) Manual DFT / IDFT already covered by analyzer interface
    def dft_idft_reconstruction_error(self, x: DiscreteSignal):
        X = self.A.compute_dft(x)
        xhat = self.A.compute_idft(X)
        return max_abs_error(x.data, xhat), rel_l2_error(x.data, xhat)
 
    # 2) Magnitude/Phase plotting in Hz
    def plot_mag_phase(self, x: DiscreteSignal, Fs, prefix=""):
        X = self.A.compute_dft(x)
        SpectrumTools.plot_mag_phase_hz(X, Fs, title_prefix=prefix)
 
    # 2) Linearity property
    def verify_linearity(self, x1: DiscreteSignal, x2: DiscreteSignal, a, b):
        if len(x1) != len(x2):
            raise ValueError("Length mismatch")
        X1 = self.A.compute_dft(x1)
        X2 = self.A.compute_dft(x2)
 
        y = x1.scale(a).add(x2.scale(b))
        Y = self.A.compute_dft(y)
        Yp = DFTProperties.predicted_linearity(X1, X2, a, b)
        return max_abs_error(Y, Yp), rel_l2_error(Y, Yp)
 
    # 2) Time shifting property
    def verify_time_shift(self, x: DiscreteSignal, m):
        X = self.A.compute_dft(x)
        y = x.circular_shift(m)
        Y = self.A.compute_dft(y)
        Yp = DFTProperties.predicted_shift(X, m)
        return max_abs_error(Y, Yp), rel_l2_error(Y, Yp)
 
    # 3) Zero padding: compare spectra (resolution effect)
    def zero_padding_demo(self, x_small: DiscreteSignal, N_big, Fs):
        Xs = self.A.compute_dft(x_small)
        x_big = x_small.pad(N_big)
        Xb = self.A.compute_dft(x_big)
        SpectrumTools.plot_mag_phase_hz(Xs, Fs, title_prefix=f"N={len(x_small)} ")
        SpectrumTools.plot_mag_phase_hz(Xb, Fs, title_prefix=f"N={len(x_big)} (zero-padded) ")
        return Xs, Xb
 
    # 3) Conjugate symmetry (real input)
    def verify_conjugate_symmetry_real(self, x_real: DiscreteSignal):
        if np.max(np.abs(np.imag(x_real.data))) > 1e-9:
            raise ValueError("Signal not real-valued (approximately).")
        X = self.A.compute_dft(x_real)
        N = len(x_real)
        k = np.arange(N)
        lhs = X[(-k) % N]           # X[-k]
        rhs = np.conjugate(X)       # conj(X[k])
        return max_abs_error(lhs, rhs), rel_l2_error(lhs, rhs)
 
    # 4) Circular vs linear convolution using DFT/FFT + padding
    def linear_convolution_via_dft(self, x: DiscreteSignal, h: DiscreteSignal, use_pow2=True):
        L = len(x) + len(h) - 1
        N = L
        if use_pow2:
            # choose next power-of-two for radix-2 speed
            p = 1
            while p < N:
                p <<= 1
            N = p
 
        xN = x.pad(N)
        hN = h.pad(N)
 
        X = self.A.compute_dft(xN)
        H = self.A.compute_dft(hN)
        yN = self.A.compute_idft(X * H)
        y_lin = yN[:L]
        return DiscreteSignal(y_lin)
 
    # 4) Spectral leakage & windowing demo
    def leakage_windowing_demo(self, N, Fs, f0_hz):
        n = np.arange(N)
        x = DiscreteSignal(np.cos(2 * np.pi * f0_hz * n / Fs))
 
        X_rect = self.A.compute_dft(x.apply_window(Windows.rectangular(N)))
        X_hann = self.A.compute_dft(x.apply_window(Windows.hann(N)))
        X_hamm = self.A.compute_dft(x.apply_window(Windows.hamming(N)))
 
        SpectrumTools.plot_mag_phase_hz(X_rect, Fs, title_prefix="Rect window ")
        SpectrumTools.plot_mag_phase_hz(X_hann, Fs, title_prefix="Hann window ")
        SpectrumTools.plot_mag_phase_hz(X_hamm, Fs, title_prefix="Hamming window ")
 
        return X_rect, X_hann, X_hamm
 
    # 4) Noise removal by “nulling bins” and IDFT
    def denoise_by_bin_nulling(self, x_noisy: DiscreteSignal, keep_bins=None, zero_bins=None):
        """
        keep_bins: iterable of bins to keep (all others set to 0)
        zero_bins: iterable of bins to zero (others untouched)
        """
        X = self.A.compute_dft(x_noisy)
        N = len(X)
        Xc = X.copy()
 
        if keep_bins is not None:
            mask = np.zeros(N, dtype=bool)
            for k in keep_bins:
                mask[int(k) % N] = True
            Xc[~mask] = 0
 
        if zero_bins is not None:
            for k in zero_bins:
                Xc[int(k) % N] = 0
 
        x_clean = self.A.compute_idft(Xc)
        return DiscreteSignal(x_clean), X, Xc
 
    # 3) Timing: naive DFT vs FFT (your FFT, not np.fft)
    @staticmethod
    def benchmark(analyzer_a, analyzer_b, Ns, trials=3):
        results = []
        rng = np.random.default_rng(0)
        for N in Ns:
            x = DiscreteSignal(rng.standard_normal(int(N)))
            # Warmup
            analyzer_a.compute_dft(x)
            analyzer_b.compute_dft(x)
 
            ta = []
            tb = []
            for _ in range(trials):
                t0 = time.perf_counter()
                analyzer_a.compute_dft(x)
                ta.append(time.perf_counter() - t0)
 
                t0 = time.perf_counter()
                analyzer_b.compute_dft(x)
                tb.append(time.perf_counter() - t0)
 
            results.append((int(N), float(np.median(ta)), float(np.median(tb))))
        return results

    # 4) Cross-correlation via FFT (much faster than time-domain loops)
    def cross_correlation_via_fft(self, x: DiscreteSignal, y: DiscreteSignal):
        """
        Compute cross-correlation r_xy[l] = sum_n x[n] * conj(y[(n-l) mod N])
        using FFT: IFFT( FFT(x) * conj(FFT(y)) )
        Returns: DiscreteSignal of length N (circular correlation)
        """
        N = len(x)
        if len(y) != N:
            raise ValueError("Length mismatch")
        
        X = self.A.compute_dft(x)
        Y = self.A.compute_dft(y)
        R = self.A.compute_idft(X * np.conjugate(Y))
        return DiscreteSignal(R)
    
    # 4) Auto-correlation via FFT (useful for pitch detection, periodicity)
    def auto_correlation_via_fft(self, x: DiscreteSignal):
        """
        Auto-correlation r_xx[l] = sum_n x[n] * conj(x[(n-l) mod N])
        Uses Wiener-Khinchin theorem: IFFT( |FFT(x)|^2 )
        """
        X = self.A.compute_dft(x)
        R = self.A.compute_idft(np.abs(X)**2)
        return DiscreteSignal(np.real(R))  # Auto-correlation is real-valued
    
    # 4) Linear cross-correlation (non-circular) via FFT padding
    def linear_cross_correlation_via_fft(self, x: DiscreteSignal, y: DiscreteSignal):
        """
        Linear (non-circular) cross-correlation via zero-padding.
        Output length = len(x) + len(y) - 1
        """
        Lx, Ly = len(x), len(y)
        L = Lx + Ly - 1
        
        # Pad to next power-of-2 for FFT efficiency
        N = 1
        while N < L:
            N <<= 1
        
        x_pad = x.pad(N)
        y_pad = y.pad(N)
        
        X = self.A.compute_dft(x_pad)
        Y = self.A.compute_dft(y_pad)
        R_pad = self.A.compute_idft(X * np.conjugate(Y))
        
        # Return only the valid linear correlation region
        return DiscreteSignal(np.real(R_pad.data[:L]))
    
    # 4) Frequency-domain FIR filtering (multiply by frequency response)
    #    Also works for polynomial multiplication
    def frequency_domain_filter(self, x: DiscreteSignal, h_ir: DiscreteSignal):
        """
        Apply FIR filter h by frequency-domain multiplication.
        Much faster for long signals.
        """
        N = len(x)
        if len(h_ir) != N:
            raise ValueError("Filter length must match signal length")
        
        X = self.A.compute_dft(x)
        H = self.A.compute_dft(h_ir)
        Y = self.A.compute_idft(X * H)
        return DiscreteSignal(Y)
    
    # 4) Spectral averaging (noise reduction for multiple noisy observations)
    def spectral_averaging(self, noisy_signals: list[DiscreteSignal], keep_fraction=0.5):
        """
        Average spectra of multiple noisy observations of same signal.
        keep_fraction: keep top keep_fraction of strongest bins, average others to 0
        """
        N = len(noisy_signals[0])
        if any(len(x) != N for x in noisy_signals):
            raise ValueError("All signals must have same length")
        
        # Compute individual spectra
        spectra = [self.A.compute_dft(x) for x in noisy_signals]
        
        # Find consistent strong bins across all spectra
        mags = np.array([np.abs(X) for X in spectra])
        mean_mag = np.mean(mags, axis=0)
        strong_bins = np.argsort(mean_mag)[-int(N * keep_fraction):]
        
        # Average spectra, zeroing weak bins
        avg_spectrum = np.zeros(N, dtype=np.complex128)
        for k in strong_bins:
            avg_spectrum[k] = np.mean([X[k] for X in spectra])
        
        # Inverse transform
        x_avg = self.A.compute_idft(avg_spectrum)
        return DiscreteSignal(x_avg), spectra, avg_spectrum
    
    # 4) Overlap-add (OLA) processing for STFT-like processing
    def overlap_add_demo(self, x: DiscreteSignal, hop_size=32, window=None):
        """
        Demo of overlap-add processing using FFT windows.
        Useful for STFT, vocoders, time-frequency processing.
        """
        N = len(x)
        frame_len = 128  # FFT size
        
        if window is None:
            window = Windows.hann(frame_len)
        
        y = np.zeros(N, dtype=np.complex128)
        frame_idx = 0
        
        # Process overlapping frames
        while frame_idx * hop_size < N:
            start = frame_idx * hop_size
            end = min(start + frame_len, N)
            
            # Extract frame, pad if needed
            frame = np.zeros(frame_len, dtype=np.complex128)
            frame[:end-start] = x.data[start:end]
            frame = DiscreteSignal(frame * window)
            
            # FFT -> modify (here: just identity) -> IFFT
            X = self.A.compute_dft(frame)
            frame_ifft = self.A.compute_idft(X)  # Perfect reconstruction
            
            # Overlap-add contribution
            y[start:start+frame_len] += np.real(frame_ifft.data)
            frame_idx += 1
        
        return DiscreteSignal(np.real(y))
    
    # 4) Verify FFT-based correlation matches direct time-domain computation
    def verify_correlation_efficiency(self, x: DiscreteSignal, y: DiscreteSignal, N_trials=3):
        """
        Benchmark: verify FFT correlation matches slow time-domain loops,
        but is much faster for large N.
        """
        print(f"Correlation benchmark (N={len(x)})...")
        
        # Time-domain (slow, O(N^2))
        t0 = time.perf_counter()
        r_direct = x.circular_corr(y)
        t_direct = time.perf_counter() - t0
        
        # FFT-domain (fast, O(N log N))
        t0 = time.perf_counter()
        r_fft = self.cross_correlation_via_fft(x, y)
        t_fft = time.perf_counter() - t0
        
        error = max_abs_error(r_direct.data, r_fft.data)
        speedup = t_direct / t_fft
        
        print(f"  Max error: {error:.2e}")
        print(f"  Direct: {t_direct:.4f}s, FFT: {t_fft:.4f}s ({speedup:.1f}x faster)")
        
        return error < 1e-10, speedup
    
    # 4) Matched filter (correlation-based signal detection)
    def matched_filter_demo(self, noisy_signal: DiscreteSignal, template: DiscreteSignal):
        """
        Detect template in noisy signal using matched filtering (correlation).
        Peak location = time of best match.
        """
        # Pad template to match noisy signal length for circular correlation
        template_pad = template.pad(len(noisy_signal))
        
        # Matched filter = correlation with time-reversed conjugate template
        h_matched = template_pad.time_reverse().conjugate()
        detection_statistic = self.cross_correlation_via_fft(noisy_signal, h_matched)
        
        # Find peak (detection)
        peak_idx = np.argmax(np.abs(detection_statistic.data))
        peak_value = np.abs(detection_statistic.data[peak_idx])
        
        plt.figure(figsize=(10, 4))
        plt.subplot(1, 2, 1)
        plt.plot(np.real(noisy_signal.data))
        plt.plot(np.real(template.data), linewidth=3)
        plt.title("Noisy Signal + Template")
        plt.grid(True)
        
        plt.subplot(1, 2, 2)
        plt.plot(np.abs(detection_statistic.data))
        # plt.axvline(peak_idx, color='r', linestyle='--', label=f'Peak at {peak_idx}')
        plt.title(f'Matched Filter Output (peak={peak_value:.1f})')
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        return detection_statistic, peak_idx, peak_value

# ----------------------------
# Example "lab test" runner
# ----------------------------
def main():
    # Choose analyzer:
    # - DFTAnalyzer(): easiest for proofs
    # - Radix2FFT(): fastest, but requires N power-of-two
    # - BlueStein(): arbitrary N
    A = BlueStein()
    tasks = LabTasks(A)
 
    # ----- Core Implementations: DFT/IDFT -----
    N = 64
    n = np.arange(N)
    x = DiscreteSignal(np.cos(2*np.pi*5*n/N))
    emax, erel = tasks.dft_idft_reconstruction_error(x)
    print("Reconstruction max error:", emax, "rel L2:", erel)
 
    # ----- Magnitude / phase in Hz -----
    Fs = 1000.0
    tasks.plot_mag_phase(x, Fs, prefix="Cos ")
 
    # ----- Linearity -----
    x1 = DiscreteSignal(np.cos(2*np.pi*5*n/N))
    x2 = DiscreteSignal(np.cos(2*np.pi*11*n/N))
    lin_err = tasks.verify_linearity(x1, x2, a=2.0, b=-0.5)
    print("Linearity (max, rel):", lin_err)
 
    # ----- Time shifting -> phase ramp -----
    shift_err = tasks.verify_time_shift(x1, m=12)
    print("Time-shift (max, rel):", shift_err)
 
    # ----- Zero padding demo -----
    x4 = DiscreteSignal([1, 2, 3, 4])
    tasks.zero_padding_demo(x4, N_big=16, Fs=Fs)
 
    # ----- Conjugate symmetry for real signals -----
    sym_err = tasks.verify_conjugate_symmetry_real(x1)
    print("Conjugate symmetry (max, rel):", sym_err)
 
    # ----- Circular vs linear convolution -----
    xa = DiscreteSignal([1, 2, 3, 4])
    ha = DiscreteSignal([4, 3, 2, 1])
    y_lin_td = xa.linear_convolve(ha)
    y_lin_fd = tasks.linear_convolution_via_dft(xa, ha, use_pow2=True)
    print("Linear conv via loops vs via DFT (max err):",
          max_abs_error(y_lin_td.data, y_lin_fd.data))
 
    # ----- Leakage & windowing -----
    # pick f0 not exactly on a DFT bin to force leakage
    tasks.leakage_windowing_demo(N=128, Fs=Fs, f0_hz=73.5)
 
    # ----- Noise removal (demo) -----
    Nn = 256
    n = np.arange(Nn)
    f_sig = 60.0
    f_noise = 310.0
    rng = np.random.default_rng(1)
    x_clean = np.cos(2*np.pi*f_sig*n/Fs)
    x_noise = 0.6*np.cos(2*np.pi*f_noise*n/Fs)
    x_noisy = DiscreteSignal(x_clean + x_noise + 0.1*rng.standard_normal(Nn))
 
    # If you know the noise frequency, compute its bin and null it + its mirror:
    k_noise = int(round(f_noise * Nn / Fs))
    zero_bins = [k_noise, (-k_noise) % Nn]
    x_denoised, X_orig, X_filt = tasks.denoise_by_bin_nulling(x_noisy, zero_bins=zero_bins)
 
    # Plot before/after spectra
    SpectrumTools.plot_mag_phase_hz(X_orig, Fs, title_prefix="Noisy ")
    SpectrumTools.plot_mag_phase_hz(X_filt, Fs, title_prefix="Filtered ")
 
    plt.figure()
    plt.plot(np.real(x_noisy.data), label="noisy")
    plt.plot(np.real(x_denoised.data), label="denoised")
    plt.grid(True)
    plt.legend()
    plt.title("Time-domain: noisy vs denoised")
 
    # ----- Timing: naive DFT vs radix-2 FFT (power-of-two Ns only) -----
    Ns = [64, 128, 256, 512, 1024]
    bench = LabTasks.benchmark(DFTAnalyzer(), Radix2FFT(), Ns, trials=5)
    for N, t_dft, t_fft in bench:
        print(f"N={N:4d}  naiveDFT={t_dft:.6f}s  radix2FFT={t_fft:.6f}s")
 
    plt.show()

    # Add these examples after your existing main() code:

    # ----- NEW: Cross-correlation verification -----
    print("\n=== Cross-correlation efficiency ===")
    xc = DiscreteSignal(np.cos(2*np.pi*5*n/N) + 0.5*np.cos(2*np.pi*12*n/N))
    yc = DiscreteSignal(np.cos(2*np.pi*5*n/N) + 0.3*np.sin(2*np.pi*7*n/N))
    corr_ok, speedup = tasks.verify_correlation_efficiency(xc, yc)
    print(f"Correlation verified: {corr_ok}, Speedup: {speedup:.1f}x")

    # ----- NEW: Matched filtering demo -----
    print("\n=== Matched filtering ===")
    N_match = 128
    n_match = np.arange(N_match)
    template = DiscreteSignal(np.cos(2*np.pi*8*n_match/N_match))
    noise = 0.3 * rng.standard_normal(N_match)
    noisy_with_template = np.zeros(256, dtype=np.complex128)
    noisy_with_template[40:40+len(template)] = template.data
    noisy_with_template += noise + 0.1j * noise
    noisy_sig = DiscreteSignal(noisy_with_template)

    detection, peak_idx, peak_val = tasks.matched_filter_demo(noisy_sig, template)
    print(f"Template detected at index {peak_idx} (expected ~40), strength {peak_val:.1f}")

    # ----- NEW: Spectral averaging -----
    print("\n=== Spectral averaging ===")
    noisy_ensemble = []
    for i in range(5):
        noise_i = 0.2 * rng.standard_normal(Nn) + 0.1j * rng.standard_normal(Nn)
        noisy_i = DiscreteSignal(x_clean + noise_i)
        noisy_ensemble.append(noisy_i)

    x_avg, spectra, avg_spec = tasks.spectral_averaging(noisy_ensemble, keep_fraction=0.3)
    print("Spectral averaging complete")

    plt.show()

 
if __name__ == "__main__":
    main()
 

# ============================================================
# ADDITIONS based on Lecture 2 & 3 slides
# ============================================================

# ----------------------------
# Bit-reversal utility
# ----------------------------
def bit_reverse_permute(x):
    """
    Return a copy of array x with elements reordered by bit-reversal of indices.
    N must be a power of 2.
    """
    x = np.asarray(x, dtype=np.complex128).copy()
    N = len(x)
    bits = int(np.log2(N))
    for i in range(N):
        j = int('{:0{w}b}'.format(i, w=bits)[::-1], 2)
        if j > i:
            x[i], x[j] = x[j], x[i]
    return x


# ----------------------------
# Iterative Radix-2 DIT FFT
# (matches the pseudocode in Lecture 2 slide 14)
# ----------------------------
class Radix2FFT_Iterative(DFTAnalyzer):
    """
    Iterative (in-place) Radix-2 Decimation-in-Time FFT.
    Input:  natural order  ->  Output: natural order
    Uses bit-reversal permutation before butterfly stages.
    N must be a power of 2.
    """

    def _is_pow2(self, N):
        return N > 0 and (N & (N - 1)) == 0

    def compute_dft(self, signal: DiscreteSignal):
        x = signal.data.copy()
        N = len(x)
        if not self._is_pow2(N):
            raise ValueError("Radix2FFT_Iterative requires N to be a power of 2.")

        # Step 1: Bit-reverse permutation
        x = bit_reverse_permute(x)

        # Step 2: Butterfly stages  (s = 1 .. log2(N))
        num_stages = int(np.log2(N))
        for s in range(1, num_stages + 1):
            M    = 1 << s                      # M = 2^s  (block size)
            W_M  = np.exp(-2j * np.pi / M)    # Principal M-th root of unity
            for l in range(0, N, M):           # Start of each M-point block
                W = 1.0 + 0j                   # Current twiddle factor W^0
                for k in range(M // 2):
                    g = x[l + k]
                    h = W * x[l + k + M // 2]
                    x[l + k]          = g + h  # X[k]
                    x[l + k + M // 2] = g - h  # X[k + M/2]
                    W *= W_M
        return x

    def compute_idft(self, spectrum):
        X = np.asarray(spectrum, dtype=np.complex128)
        return np.conjugate(self.compute_dft(DiscreteSignal(np.conjugate(X)))) / len(X)


# ----------------------------
# Radix-2 DIF FFT
# (Decimation-in-Frequency — Lecture 2, slides 15-17)
# ----------------------------
class Radix2DIF_FFT(DFTAnalyzer):
    """
    Radix-2 Decimation-in-Frequency FFT.
    DIF splits the TIME indices into first/second halves:
      a[n] = x[n] + x[n + N/2]          -> even outputs X[2m]
      b[n] = (x[n] - x[n + N/2]) * W^n_N -> odd  outputs X[2m+1]
    Then recurses. Natural-order input, natural-order output.
    N must be a power of 2.
    """

    def _is_pow2(self, N):
        return N > 0 and (N & (N - 1)) == 0

    def _dif_rec(self, x):
        N = len(x)
        if N == 1:
            return x
        half = N // 2
        n    = np.arange(half)
        tw   = np.exp(-2j * np.pi * n / N)   # W^n_N

        a = x[:half] + x[half:]               # -> X[0], X[2], X[4] ...
        b = (x[:half] - x[half:]) * tw        # -> X[1], X[3], X[5] ...

        A = self._dif_rec(a)
        B = self._dif_rec(b)

        # Interleave: even-indexed outputs first, then odd
        out = np.empty(N, dtype=np.complex128)
        out[0::2] = A
        out[1::2] = B
        return out

    def compute_dft(self, signal: DiscreteSignal):
        x = signal.data.copy()
        N = len(x)
        if not self._is_pow2(N):
            raise ValueError("Radix2DIF_FFT requires N to be a power of 2.")
        return self._dif_rec(x)

    def compute_idft(self, spectrum):
        X = np.asarray(spectrum, dtype=np.complex128)
        return np.conjugate(self.compute_dft(DiscreteSignal(np.conjugate(X)))) / len(X)


# ----------------------------
# Radix-3 FFT
# (Lecture 3, slides 6-7)
# N must be a power of 3.
# ----------------------------
class Radix3FFT(DFTAnalyzer):
    """
    Radix-3 Decimation-in-Time FFT.
    Splits x[n] into three subsequences (index mod 3 = 0, 1, 2),
    computes three N/3-point DFTs, then combines with the 3-point butterfly:

      X[k]       = G0[k] + W^k_N  G1[k] + W^2k_N  G2[k]
      X[k+N/3]   = G0[k] + W^1_3 (W^k_N G1[k]) + W^2_3 (W^2k_N G2[k])
      X[k+2N/3]  = G0[k] + W^2_3 (W^k_N G1[k]) + W^4_3 (W^2k_N G2[k])

    N must be a power of 3.
    """

    def _is_pow3(self, N):
        if N < 1:
            return False
        while N % 3 == 0:
            N //= 3
        return N == 1

    def _fft3_rec(self, x):
        N = len(x)
        if N == 1:
            return x
        N3 = N // 3

        G0 = self._fft3_rec(x[0::3])
        G1 = self._fft3_rec(x[1::3])
        G2 = self._fft3_rec(x[2::3])

        k    = np.arange(N3)
        T1   = np.exp(-2j * np.pi * k / N) * G1       # W^k_N  * G1
        T2   = np.exp(-4j * np.pi * k / N) * G2       # W^2k_N * G2
        W3_1 = np.exp(-2j * np.pi / 3)                 # W^1_3
        W3_2 = np.exp(-4j * np.pi / 3)                 # W^2_3

        X = np.empty(N, dtype=np.complex128)
        X[:N3]     = G0 + T1           + T2
        X[N3:2*N3] = G0 + W3_1 * T1   + W3_2 * T2
        X[2*N3:]   = G0 + W3_2 * T1   + (W3_2 ** 2) * T2
        return X

    def compute_dft(self, signal: DiscreteSignal):
        x = signal.data
        N = len(x)
        if not self._is_pow3(N):
            raise ValueError(f"Radix3FFT requires N to be a power of 3, got {N}.")
        return self._fft3_rec(x)

    def compute_idft(self, spectrum):
        X = np.asarray(spectrum, dtype=np.complex128)
        return np.conjugate(self.compute_dft(DiscreteSignal(np.conjugate(X)))) / len(X)


# ----------------------------
# Bailey's Four-Step FFT
# (General Cooley-Tukey N = N1 x N2, Lecture 3 slides 8-13)
# ----------------------------
class BaileyFFT(DFTAnalyzer):
    """
    Bailey's Four-Step FFT (General Cooley-Tukey matrix formulation).
    Handles any N = N1 * N2.

    Algorithm:
      1. Arrange x[n] in an N1 x N2 matrix, column-major (n = N1*n2 + n1).
      2. N2-point DFT of each row (->).
      3. Multiply entry (n1, k2) by twiddle factor W^(n1*k2)_N.
      4. N1-point DFT of each column (down).
      Output read row-major: k = N2*k1 + k2.
    """

    def __init__(self, N1, N2, row_analyzer=None, col_analyzer=None):
        self.N1  = N1
        self.N2  = N2
        self.row_A = row_analyzer or BlueStein()   # for N2-point row DFTs
        self.col_A = col_analyzer or BlueStein()   # for N1-point col DFTs

    def compute_dft(self, signal: DiscreteSignal):
        x  = signal.data
        N  = self.N1 * self.N2
        if len(x) != N:
            raise ValueError(f"Signal length {len(x)} != N1*N2 = {N}")

        # Step 1: Reshape to N1 x N2 (column-major fill)
        M = x.reshape(self.N2, self.N1).T.copy()   # shape (N1, N2)

        # Step 2: N2-point DFT of each row
        for i in range(self.N1):
            M[i, :] = self.row_A.compute_dft(DiscreteSignal(M[i, :]))

        # Step 3: Twiddle factors  W^(n1 * k2)_N
        n1 = np.arange(self.N1).reshape(-1, 1)
        k2 = np.arange(self.N2).reshape(1, -1)
        M *= np.exp(-2j * np.pi * n1 * k2 / N)

        # Step 4: N1-point DFT of each column
        for j in range(self.N2):
            M[:, j] = self.col_A.compute_dft(DiscreteSignal(M[:, j]))

        # Read output row-major: k = N2*k1 + k2
        return M.flatten()

    def compute_idft(self, spectrum):
        X = np.asarray(spectrum, dtype=np.complex128)
        return np.conjugate(self.compute_dft(DiscreteSignal(np.conjugate(X)))) / len(X)


# ----------------------------
# DFT Property: Conjugate Symmetry for real signals
# Lecture slides: X[N-k] = conj(X[k])  (i.e. X[-k mod N] = conj(X[k]))
# ----------------------------
DFTProperties.predicted_conjugate_symmetry = staticmethod(
    lambda X: np.conjugate(X[(-np.arange(len(X))) % len(X)])
)


# ----------------------------
# Quick self-test for all new additions
# ----------------------------
if __name__ == "__main__":
    rng = np.random.default_rng(42)
    ref = BlueStein()

    print("=" * 55)
    print("Self-test: additions from Lecture 2 & 3 slides")
    print("=" * 55)

    N = 64
    x64 = DiscreteSignal(rng.standard_normal(N))
    X_ref = ref.compute_dft(x64)

    # Iterative DIT
    X_dit = Radix2FFT_Iterative().compute_dft(x64)
    print(f"Iterative DIT  (N={N}):        max_err = {max_abs_error(X_ref, X_dit):.2e}")

    # DIF FFT
    X_dif = Radix2DIF_FFT().compute_dft(x64)
    print(f"Radix-2 DIF    (N={N}):        max_err = {max_abs_error(X_ref, X_dif):.2e}")

    # Radix-3 FFT
    N3 = 27
    x27 = DiscreteSignal(rng.standard_normal(N3))
    X_ref3 = ref.compute_dft(x27)
    X_r3   = Radix3FFT().compute_dft(x27)
    print(f"Radix-3 DIT    (N={N3}):           max_err = {max_abs_error(X_ref3, X_r3):.2e}")

    # Bailey's Four-Step FFT
    N1, N2 = 4, 16
    x_b    = DiscreteSignal(rng.standard_normal(N1 * N2))
    X_refb  = ref.compute_dft(x_b)
    X_bailey = BaileyFFT(N1, N2).compute_dft(x_b)
    print(f"Bailey's FFT   (N={N1*N2}, N1={N1}, N2={N2}): max_err = {max_abs_error(X_refb, X_bailey):.2e}")

    # Conjugate symmetry (should be ~0 for real input)
    x_real = DiscreteSignal(rng.standard_normal(N))
    X_real = ref.compute_dft(x_real)
    X_sym  = DFTProperties.predicted_conjugate_symmetry(X_real)
    print(f"Conjugate sym  (N={N}):        max_err = {max_abs_error(X_real, X_sym):.2e}  (expect ~0)")

    print("=" * 55)
    print("All tests complete.")