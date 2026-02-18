import numpy as np
import matplotlib.pyplot as plt

class ContinuousSignal:
    def __init__(self, t):
        self.t = t
    def values(self):
        raise NotImplementedError("Subclasses must implement this method.")
    def plot(self, title="Signal"):
        plt.figure(figsize=(8, 4))
        plt.plot(self.t, self.values())
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title(title)
        plt.grid(True)
        plt.show()

class CFTAnalyzer:
    def __init__(self, signal, t, frequencies):
        self.signal = signal
        self.t = t
        self.frequencies = frequencies
        self.real_spectrum = None
        self.imag_spectrum = None 

    def compute_cft(self):
        x_t = self.signal.values()
        real_spectrum = np.zeros_like(self.frequencies)
        imag_spectrum = np.zeros_like(self.frequencies)
        
        for i, freq in enumerate(self.frequencies):
            cosine_part = x_t * np.cos(2*np.pi*freq*self.t)
            real_spectrum[i] = np.trapezoid(cosine_part, self.t)

            sine_part = x_t * np.sin(2*np.pi*freq*self.t)
            imag_spectrum[i] = -np.trapezoid(sine_part, self.t)
        
        self.real_spectrum = real_spectrum
        self.imag_spectrum = imag_spectrum
        return (real_spectrum, imag_spectrum)

class Task1Piecewise(ContinuousSignal):
    def values(self):
        y = np.zeros_like(self.t)

        idx1 = (self.t >= -3) & (self.t < -1)
        y[idx1] = (self.t[idx1] + 3)**2
        
        idx2 = (self.t >= -1) & (self.t < 1)
        y[idx2] = 5 - np.abs(self.t[idx2])

        idx3 = (self.t >= 1) & (self.t <= 3)
        y[idx3] = (self.t[idx3] - 3)**2
        
        return y

def solve_task_1_B1B2():
    print("--- Solving B1-B2: Piecewise Function & Parseval ---")
    t = np.linspace(-10, 10, 2000)
    sig = Task1Piecewise(t)
    sig.plot("Figure 1 Implementation (Parabola-Triangle-Parabola)")

    y = sig.values()
    energy_time = np.trapezoid(y**2, t)

    freqs = np.linspace(-5, 5, 1000)
    cft = CFTAnalyzer(sig, t, freqs)
    real, imag = cft.compute_cft()
    
    magnitude_sq = real**2 + imag**2
    energy_freq = np.trapezoid(magnitude_sq, freqs)

    print(f"nrg(Time domain): {energy_time:.5f}")
    print(f"nrg(Freq domain): {energy_freq:.5f}")
    print(f"Diff: {abs(energy_time - energy_freq):.5f}")

class Task2ComplexSignal(ContinuousSignal):
    def values(self):
        term1 = 2 * np.sin(14 * np.pi * self.t)
        term2 = np.sin(2 * np.pi * self.t) * (4 * np.sin(2 * np.pi * self.t) * np.sin(14 * np.pi * self.t) - 1)
        return term1 - term2

def solve_task_2_C1C2():
    print("--- Solving C1-C2: Signal Decomposition ---")
    t = np.linspace(0, 2, 2000) 
    sig = Task2ComplexSignal(t)
    sig.plot("Original Function f(t)")

    freqs = np.linspace(0, 15, 500)
    cft = CFTAnalyzer(sig, t, freqs)
    real, imag = cft.compute_cft()
    mag = np.sqrt(real**2 + imag**2)

    plt.figure(figsize=(8, 4))
    plt.plot(freqs, mag)
    plt.title("Frequency Spectrum (Spikes at 1, 5, and 9 Hz)")
    plt.xlabel("Frequency (Hz)")
    plt.grid(True)
    plt.show()

    sum_sig = np.sin(2*np.pi*1*t) + np.sin(2*np.pi*5*t) + np.sin(2*np.pi*9*t)

    plt.figure(figsize=(10, 4))
    plt.plot(t, sig.values(), label="Original Function", alpha=0.6, lw=3)
    plt.plot(t, sum_sig, '--', label="Sum of Sines (1, 5, 9 Hz)", color='red')
    plt.legend()
    plt.title("Check: Summation vs Original Function")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    solve_task_1_B1B2()
    solve_task_2_C1C2()