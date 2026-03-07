import numpy as np
from discrete_framework import FastFourierTransform, DiscreteSignal


class ArbitraryFFTAnalyzer:
    """
    -power of 2: use existing Radix-2 FFT
    -composite: use Mixed-Radix
    -prime: use Bluestein's algorithm
    """

    def __init__(self):
        self.radix2 = FastFourierTransform()

    def compute_dft(self, signal: DiscreteSignal):
        x = signal.data
        N = len(x)

        if self._is_power_of_two(N):
            return self.radix2.compute_dft(signal)

        factors = self._factorize(N)

        if len(factors) > 1:
            return self._mixed_radix_fft(x)

        return self._bluestein_fft(x)

    def compute_idft(self, spectrum):
        N = len(spectrum)
        return np.conj(self.compute_dft(DiscreteSignal(np.conj(spectrum)))) / N

    def _is_power_of_two(self, n):
        return (n & (n - 1)) == 0 and n != 0

    def _factorize(self, n):
        factors = []
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors.append(d)
                n //= d
            d += 1
        if n > 1:
            factors.append(n)
        return factors

    # mixed radix fft

    def _mixed_radix_fft(self, x):
        N = len(x)
        factors = self._factorize(N)

        p = factors[0]   # first prime factor (radix)
        m = N // p       # length of each sub-sequence

        # Cooley-Tukey decimation requires x[i], x[i+p], x[i+2p], ... for sub-seq i.
        X_blocks = np.zeros((p, m), dtype=np.complex128)
        for i in range(p):
            sub_signal = DiscreteSignal(x[i::p])   # <-- was x.reshape(p,m)[i]
            X_blocks[i] = self.compute_dft(sub_signal)

        X = np.zeros(N, dtype=np.complex128)

        for k in range(N):
            value = 0
            for i in range(p):
                # Twiddle factor: W_N^(i * k)
                twiddle = np.exp(-2j * np.pi * i * k / N)
                value += X_blocks[i][k % m] * twiddle
            X[k] = value

        return X

    # bluestein's algo

    def _bluestein_fft(self, x):
        N = len(x)
        M = 1
        while M < 2 * N - 1:
            M *= 2
        n = np.arange(N)

        # chirp-multiply the input
        a = x * np.exp(-1j * np.pi * n**2 / N)
        b = np.zeros(M, dtype=np.complex128)
        b[:N] = np.exp(1j * np.pi * n**2 / N)
        # indices M-N+1 .. M-1 should hold exp(+j*pi*k²/N) for k = N-1 .. 1
        b[M - N + 1:] = np.exp(1j * np.pi * (np.arange(N - 1, 0, -1))**2 / N)

        a_padded = np.zeros(M, dtype=np.complex128)
        a_padded[:N] = a

        A = self.radix2.compute_dft(DiscreteSignal(a_padded))
        B = self.radix2.compute_dft(DiscreteSignal(b))
        C = A * B
        c = self.radix2.compute_idft(C)

        result = c[:N] * np.exp(-1j * np.pi * n**2 / N)
        return result 