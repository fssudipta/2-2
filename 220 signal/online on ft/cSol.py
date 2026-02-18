import numpy as np
import matplotlib.pyplot as plt

# =====================================================
# Abstract Base Class for Continuous-Time Signals
# =====================================================
class ContinuousSignal:
    """
    Abstract base class for all continuous-time signals.
    Every signal must be defined over a time axis t.
    """

    def __init__(self, t):
        self.t = t

    def values(self):
        """
        Returns the signal values evaluated over time axis t.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def plot(self, title="Signal"):
        """
        Plot the signal in the time domain.
        """
        plt.figure(figsize=(10, 4))
        plt.plot(self.t, self.values())
        plt.xlabel("Time (t)")
        plt.ylabel("Amplitude")
        plt.title(title)
        plt.grid(True)
        plt.show()


# =====================================================
# Signal Generator Class
# =====================================================
class SignalGenerator(ContinuousSignal):
    """
    Generates various continuous-time signals.
    Each method returns a numpy array of signal samples.
    """

    def square(self, amplitude=1, frequency=1):
        return amplitude * np.sign(np.sin(2 * np.pi * frequency * self.t))

    def triangle(self, amplitude=1, frequency=1):
        return (2 * amplitude / np.pi) * np.arcsin(
            np.sin(2 * np.pi * frequency * self.t)
        )


# =====================================================
# Composite Signal Class
# =====================================================
class CompositeSignal(ContinuousSignal):
    """
    Combines multiple signals into a single composite signal.
    """

    def __init__(self, t):
        super().__init__(t)
        self.components = []

    def add_component(self, signal):
        """
        Add a signal component to the composite signal.
        Signal can be either a numpy array or another ContinuousSignal object.
        """
        self.components.append(signal)

    def values(self):
        """
        Sum all signal components.
        Returns the composite signal as sum of all components
        """
        if not self.components:
            return np.zeros_like(self.t)
        total = np.zeros_like(self.t)
        for c in self.components:
            total += c
        return total


class SignalModifier(ContinuousSignal):
    def __init__(self, original_signal, t, a, f0):
        super().__init__(t)
        self.original = original_signal
        self.a = a
        self.f0 = f0

    def values(self):
        x_at = np.interp(
            self.a * self.t, self.original.t, self.original.values(), left=0, right=0
        )
        return x_at * np.exp(1j * 2 * np.pi * self.f0 * self.t)


# =====================================================
# Continuous Fourier Transform Analyzer
# =====================================================
class CFTAnalyzer:
    """
    Computes the Continuous Fourier Transform (CFT)
    using numerical integration (np.trapz).
    """

    def __init__(self, signal, t, f):
        self.signal = signal
        self.t = t
        self.f = f

    def compute_cft(self):
        """
        Compute real and imaginary parts of the CFT.
        """
        x_t = self.signal.values()
        real_spectrum = np.zeros_like(self.f)
        imag_spectrum = np.zeros_like(self.f)

        for i, freq in enumerate(self.f):
            cosine = x_t * np.cos(2 * np.pi * freq * self.t)
            real_spectrum[i] = np.trapezoid(cosine, self.t)

            sine = x_t * np.sin(2 * np.pi * freq * self.t)
            imag_spectrum[i] = -np.trapezoid(sine, self.t)

        self.real_spectrum = real_spectrum
        self.imag_spectrum = imag_spectrum
        return real_spectrum, imag_spectrum

    def mag_phase(self):
        real, imag = self.compute_cft()
        mag = np.sqrt(real**2 + imag**2)
        phase = np.arctan2(imag, real)
        return mag, phase

    def plot_spectrum(self):
        """
        Plot magnitude spectrum of the signal.
        Magnitude = sqrt(real*real + imag*imag)
        """
        if self.real_spectrum is None or self.imag_spectrum is None:
            self.compute_cft()

        magnitude = np.sqrt(self.real_spectrum**2 + self.imag_spectrum**2)

        plt.figure(figsize=(10, 6))
        plt.plot(self.frequencies, magnitude)
        plt.xlabel("Frequency")
        plt.ylabel("Magnitude")
        plt.title("CFT Magnitude Spectrum")
        plt.grid(True)
        plt.show()


# =====================================================
# Main Execution (Task 1)
# =====================================================
if __name__ == "__main__":
    f0 = 10
    a = 10
    t = np.linspace(-5, 5, 2000)
    f = np.linspace(-10, 10, 1000)
    gen = SignalGenerator(t)
    x = CompositeSignal(t)
    x.add_component(gen.square())
    x.add_component(gen.triangle())
    y = SignalModifier(x, t, a, f0)
    cft_x = CFTAnalyzer(x, t, f)
    mag_x, phase_x = cft_x.mag_phase()
    cft_y = CFTAnalyzer(y, t, f)
    mag_y, phase_y = cft_y.mag_phase()

    shifted_freq = (f - f0) / a
    mag_X_interp = np.interp(shifted_freq, f, mag_x, left=0, right=0)
    phase_X_interp = np.interp(shifted_freq, f, phase_x, left=0, right=0)

    theoretical_mag = (1 / abs(a)) * mag_X_interp
    theoretical_phase = phase_X_interp
    MSE_magnitude = np.mean((mag_y - theoretical_mag) ** 2)
    MSE_phase = np.mean((phase_y - theoretical_phase) ** 2)
    print("MSE mag =", MSE_magnitude)
    print("MSE phase =", MSE_phase)
    plt.figure()
    plt.plot(f, mag_y, label="|Y(f)|")
    plt.plot(f, theoretical_mag, "--", label="1/|a| |X((f-f0)/a)|")
    plt.legend()
    plt.title("Magnitude Verification")
    plt.grid()
    plt.show()

    plt.figure()
    plt.plot(f, phase_y, label="∠Y(f)")
    plt.plot(f, theoretical_phase, "--", label="∠X((f-f0)/a)")
    plt.legend()
    plt.title("Phase Verification")
    plt.grid()
    plt.show()
