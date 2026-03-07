import numpy as np


def fft(a):
    N = len(a)
    if N == 1:
        return a
    even = fft(a[::2])
    odd = fft(a[1::2])
    k = np.arange(N // 2)
    tw = np.exp(-2j * np.pi * k / N) * odd
    return np.concatenate([even + tw, even - tw])


def ifft(a):
    N = len(a)
    return np.conjugate(fft(np.conjugate(a))) / N


def next_power_of_2(n):
    p = 1
    while p < n:
        p <<= 1
    return p


def weighted_polynomial_multiply(P, Q, W):

    # A[i] = wi * pi
    A = [p * w for p, w in zip(P, W)]

    n = len(A)
    m = len(Q)

    size = next_power_of_2(n + m - 1)

    A_pad = np.zeros(size, dtype=np.complex128)
    Q_pad = np.zeros(size, dtype=np.complex128)

    A_pad[:n] = A
    Q_pad[:m] = Q

    FA = fft(A_pad)
    FQ = fft(Q_pad)

    FR = FA * FQ

    result = np.real(ifft(FR))
    result = np.round(result).astype(int)

    return result[:n + m - 1].tolist()


if __name__ == "__main__":

    P = [1, 3, 2, 6, 7]
    Q = [4, 1]
    W = [3, 2, 1, 5, 6]

    # convert to ascending order
    P.reverse()
    Q.reverse()
    W.reverse()

    R = weighted_polynomial_multiply(P, Q, W)

    print("Result:", R)