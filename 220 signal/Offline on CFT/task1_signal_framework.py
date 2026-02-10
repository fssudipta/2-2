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
        plt.figure(figsize=(10,4))
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

    def sine(self, amplitude, frequency):
        """Generate a sine wave."""
        return amplitude*np.sin(2*np.pi*frequency*self.t)

    def cosine(self, amplitude, frequency):
        """Generate a cosine wave."""
        return amplitude*np.cos(2*np.pi*frequency*self.t)

    def square(self, amplitude, frequency):
        """Generate a square wave using sign of sine."""
        return amplitude*np.sign(np.sin(2*np.pi*frequency*self.t))

    def sawtooth(self, amplitude, frequency):
        """Generate a sawtooth wave."""
        return amplitude*2*(frequency*self.t-np.floor(0.5+frequency*self.t))

    def triangle(self, amplitude, frequency):
        """Generate a triangle wave."""
        return (2*amplitude/np.pi)*np.arcsin(np.sin(2*np.pi*frequency*self.t))

    def cubic(self, coefficient):
        """Generate a cubic polynomial signal."""
        return coefficient*(self.t**3)

    def parabolic(self, coefficient):
        """Generate a parabolic signal."""
        return coefficient*(self.t**2)

    def rectangular(self, width):
        """Generate a rectangular window centered at t=0."""
        rect = np.zeros_like(self.t)  
        rect[np.abs(self.t)<=width/2] = 1
        return rect

    def pulse(self, start, end):
        """Generate a finite pulse active between start and end."""
        pulse = np.zeros_like(self.t)
        pulse[(self.t>=start) & (self.t<=end)] = 1
        return pulse    


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
        if len(self.components) == 0:
            return np.zeros_like(self.t)
        res = np.zeros_like(self.t)
        for component in self.components:
            if isinstance(component, np.ndarray):
                res += component
            elif isinstance(component, ContinuousSignal):
                res += component.values()
            else:
                res += component
        return res 


# =====================================================
# Continuous Fourier Transform Analyzer
# =====================================================
class CFTAnalyzer:
    """
    Computes the Continuous Fourier Transform (CFT)
    using numerical integration (np.trapz).
    """

    def __init__(self, signal, t, frequencies):
        self.signal = signal
        self.t = t
        self.frequencies = frequencies
        self.real_spectrum = None
        self.imag_spectrum = None 

    def compute_cft(self):
        """
        Compute real and imaginary parts of the CFT.
        """
        x_t = self.signal.values()
        real_spectrum = np.zeros_like(self.frequencies)
        imag_spectrum = np.zeros_like(self.frequencies)
        
        for i, freq in enumerate(self.frequencies):
            cosine = x_t * np.cos(2*np.pi*freq*self.t)
            real_spectrum[i] = np.trapezoid(cosine, self.t)

            sine = x_t * np.sin(2*np.pi*freq*self.t)
            imag_spectrum[i] = -np.trapezoid(sine, self.t)
        
        self.real_spectrum = real_spectrum
        self.imag_spectrum = imag_spectrum
        return (real_spectrum, imag_spectrum)

    def plot_spectrum(self):
        """
        Plot magnitude spectrum of the signal.
        Magnitude = sqrt(real*real + imag*imag)
        """
        if self.real_spectrum is None or self.imag_spectrum is None:
            self.compute_cft()
            
        magnitude = np.sqrt(self.real_spectrum**2 + self.imag_spectrum**2)

        plt.figure(figsize=(10,6))
        plt.plot(self.frequencies, magnitude)
        plt.xlabel("Frequency")
        plt.ylabel("Magnitude")
        plt.title("CFT Magnitude Spectrum")
        plt.grid(True)
        plt.show()


# =====================================================
# Inverse Continuous Fourier Transform
# =====================================================
class InverseCFT:
    """
    Reconstructs time-domain signal using ICFT.
    """

    def __init__(self, spectrum, frequencies, t):
        self.spectrum = spectrum
        self.frequencies = frequencies
        self.t = t

    def reconstruct(self):
        """
        Perform inverse CFT using numerical integration.
        """
        real_spectrum, imag_spectrum = self.spectrum
        x_rec = np.zeros_like(self.t)
        
        for i, time in enumerate(self.t):
            cosine = real_spectrum * np.cos(2*np.pi*self.frequencies*time)
            sine = imag_spectrum * np.sin(2*np.pi*self.frequencies*time)
            integrand = cosine - sine
            x_rec[i] = np.trapezoid(integrand, self.frequencies)  
            
        return x_rec


# =====================================================
# Main Execution (Task 1)
# =====================================================
if __name__ == "__main__":
    t = np.linspace(-4, 4, 3000)
    gen = SignalGenerator(t) 

    composite = CompositeSignal(t)
    composite.add_component(gen.sine(2, 1))
    composite.add_component(gen.cosine(0.5, 3))
    composite.add_component(gen.square(1, 1))
    composite.add_component(gen.cubic(1.0) * gen.rectangular(2.0))

    composite.plot("Composite Signal")

    frequencies = np.linspace(-10, 10, 1000)
    
    # Compute CFT
    print("Computing CFT...")
    cft = CFTAnalyzer(composite, t, frequencies)
    cft.compute_cft()  
    cft.plot_spectrum()
    
    # Reconstruct signal using ICFT
    print("Reconstructing signal using Inverse CFT...")
    icft = InverseCFT(cft.spectrum if hasattr(cft, 'spectrum') else (cft.real_spectrum, cft.imag_spectrum), frequencies, t)
    x_rec = icft.reconstruct()

    plt.figure(figsize=(10, 6))
    plt.plot(t, composite.values(), label="Original", linewidth=2)
    plt.plot(t, x_rec, '--', label="Reconstructed", linewidth=2)
    plt.xlabel("Time (t)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.title("Reconstruction using ICFT")
    plt.grid(True)
    plt.show()

    print("\nAnalyzing reconstruction quality with different frequency ranges...")
    freq_ranges = [(-5, 5), (-10, 10), (-20, 20)]
    
    plt.figure(figsize=(15, 10))
    for idx, (f_min, f_max) in enumerate(freq_ranges):
        frequencies_test = np.linspace(f_min, f_max, 500)
        cft_test = CFTAnalyzer(composite, t, frequencies_test)
        spectrum = cft_test.compute_cft()
        icft_test = InverseCFT(spectrum, frequencies_test, t)
        x_rec_test = icft_test.reconstruct()
        
        plt.subplot(3, 1, idx + 1)
        plt.plot(t, composite.values(), label="Original", linewidth=2, alpha=0.7)
        plt.plot(t, x_rec_test, '--', label="Reconstructed", linewidth=2)
        plt.xlabel("Time (t)")
        plt.ylabel("Amplitude")
        plt.title(f"Recon. signal for freq. range [{f_min}, {f_max}]")
        plt.legend()
        plt.grid(True)
        
        # Calculate reconstruction error
        error = np.mean(np.abs(composite.values() - x_rec_test))
        print(f"Frequency range [{f_min}, {f_max}]: Mean Absolute Error = {error:.6f}")
    
    plt.tight_layout()
    plt.show()
    
    print("\nObservations:")
    print("1. Gibbs phenomenon: Oscillations near discontinuities (square wave)")
    print("2. Wider frequency range means better reconstruction accuracy")
    print("3. Limited frequency range means Signal smoothing and detail loss")
    print("4. Numerical integration introduces small errors")