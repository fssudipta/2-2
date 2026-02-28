import numpy as np
import time

class DiscreteSignal:
    """
    Represents a discrete-time signal.
    """

    def __init__(self, data):
        # Ensure data is a numpy array, potentially complex
        self.data = np.array(data, dtype=np.complex128)

    def __len__(self):
        return len(self.data)

    def pad(self, new_length):
        """
        Zero-pad or truncate signal to new_length.
        Returns a new DiscreteSignal object.
        """
        # TODO: Implement padding logic
        # Placeholder return to prevent crash
        res = np.zeros(new_length, dtype=np.complex128)
        copy_len = min(len(self.data), new_length)
        res[:copy_len] = self.data[:copy_len]
        return DiscreteSignal(res)

    def interpolate(self, new_length):
        """
        Resample signal to new_length using linear interpolation.
        Required for Task 4 (Drawing App).
        """
        # TODO: Implement interpolation logic
        if len(self.data) < 2:
            return DiscreteSignal(np.zeros(new_length))
        old_indices = np.linspace(0, len(self.data) - 1, len(self.data))
        new_indices = np.linspace(0, len(self.data) - 1, new_length)

        new_real = np.interp(new_indices, old_indices, self.data.real)
        new_imag = np.interp(new_indices, old_indices, self.data.imag)
        return DiscreteSignal(new_real + 1j * new_imag)


class DFTAnalyzer:
    """
    Performs Discrete Fourier Transform using O(N^2) method.
    """

    def compute_dft(self, signal: DiscreteSignal):
        """
        Compute DFT using naive summation.
        Returns: numpy array of complex frequency coefficients.
        """
        """x = signal.data
        N = len(x)
        X = np.zeros(N, dtype=np.complex128)
        # TODO: Implement Naive DFT equation
        # Placeholder: Return zeros so UI doesn't crash
        for k in range(N):
            for n in range(N):
                angle = -2j * np.pi * k * n / N
                X[k] += x[n] * np.exp(angle)
        return X"""
        x = signal.data
        N = len(x)
        n = np.arange(N)
        k = n.reshape((N, 1))
        M = np.exp(-2j * np.pi * k * n / N)
        return np.dot(M, x)

    def compute_idft(self, spectrum):
        """
        Compute Inverse DFT using naive summation.
        Returns: numpy array (time-domain samples).
        """
        # TODO: Implement Naive IDFT equation
        """N = len(spectrum)
        x = np.zeros(len(spectrum), dtype=np.complex128)
        for n in range(N):
            for k in range(N):
                angle = 2j * np.pi * k * n / N
                x[n] += spectrum[k] * np.exp(angle)
        return x / N"""
        N = len(spectrum)
        n = np.arange(N)
        k = n.reshape((N, 1))
        M = np.exp(2j * np.pi * k * n / N)
        return np.dot(M, spectrum) / N


class FastFourierTransform(DFTAnalyzer):
    """ "
    implemetns radix-2 decimation-in-time(DIT) FFT.
    """
    
    def compute_dft(self, signal: DiscreteSignal):
        x = signal.data
        N = len(x)
        if (N & (N - 1)) != 0:
            raise ValueError("Signal length must be a power of 2 for this algorithm.")
        return self._recursive_radix2_logic(x)

    def _recursive_radix2_logic(self, x):
        """ "
        custom manual implementatoopn of the cooley-tukey recursion.
        """
        N = len(x)
        if N <= 1:
            return x

        # splitting into even and odd indices
        even = self._recursive_radix2_logic(x[0::2])
        odd = self._recursive_radix2_logic(x[1::2])
        # combine using the butterfly mathematical formula
        # X[k] = E[k]+exp(-2j*pi*k/N)*O[k]
        combined = np.zeros(N, dtype=np.complex128)
        for k in range(N // 2):
            rotator_factor = np.exp(-2j * np.pi * k / N) * odd[k]
            combined[k] = even[k] + rotator_factor
            combined[k + N // 2] = even[k] - rotator_factor
        return combined

    def compute_idft(self, spectrum):
        N = len(spectrum)
        spectrum_conj = np.conj(spectrum)
        transformed = self._recursive_radix2_logic(spectrum_conj)
        return np.conj(transformed) / N