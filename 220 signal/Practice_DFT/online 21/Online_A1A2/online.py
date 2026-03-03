import numpy as np

# Example usage
x = 65767879797907
y = 765454532435435345

# Converting to digit arrays (discrete signal)
x_digits = [int(digit) for digit in str(x)]
y_digits = [int(digit) for digit in str(y)]


def next_power_of_2(n):
    p = 1
    while p < n:
        p <<= 1
    return p


def fft(x):
    N = len(x)
    if N == 1:
        return x
    even = fft(x[::2])
    odd  = fft(x[1::2])
    k    = np.arange(N // 2)
    tw   = np.exp(-2j * np.pi * k / N) * odd
    return np.concatenate([even + tw, even - tw])


def ifft(X):
    N = len(X)
    return np.conjugate(fft(np.conjugate(X))) / N


def dft_multiply(a, b):
    """
    Multiply two non-negative integers represented as digit lists using
    DFT-based (FFT) polynomial multiplication (linear convolution).

    Steps:
      1. Pad both arrays to length >= len(a)+len(b)-1, rounded up to next
         power of 2 (ensures circular convolution == linear convolution).
      2. FFT both padded arrays.
      3. Multiply element-wise in frequency domain.
      4. IFFT back to time domain.
      5. Round to nearest integer and handle carry-overs.
    """
    # Length of the linear convolution result
    lin_len = len(a) + len(b) - 1
    # Pad to next power of 2
    N = next_power_of_2(lin_len)

    a_pad = np.zeros(N, dtype=np.complex128)
    b_pad = np.zeros(N, dtype=np.complex128)
    a_pad[:len(a)] = a
    b_pad[:len(b)] = b

    # FFT
    A = fft(a_pad)
    B = fft(b_pad)

    # Multiply in frequency domain  (circular convolution of padded = linear conv)
    C = A * B

    # IFFT and round to nearest integer
    c = np.real(ifft(C))
    c = np.round(c).astype(int)

    # Keep only the meaningful part
    c = c[:lin_len].tolist()

    # Handle carry-overs from right to left
    result = []
    carry = 0
    for val in reversed(c):
        val += carry
        result.append(val % 10)
        carry = val // 10

    # Flush remaining carry
    while carry:
        result.append(carry % 10)
        carry //= 10

    # Reverse to get most-significant digit first
    result.reverse()

    # Convert digit list to integer
    return int(''.join(map(str, result)))


product = dft_multiply(x_digits, y_digits)

print(f"x = {x}")
print(f"y = {y}")
print(f"DFT-based product  : {product}")
print(f"Direct verification: {x * y}")
print(f"Match: {product == x * y}")

tx = 65767879797907
ty = 765454532435435345
expected = 50342321679976816694244164822915

tx_digits = [int(d) for d in str(tx)]
ty_digits = [int(d) for d in str(ty)]
test_result = dft_multiply(tx_digits, ty_digits)

print(f"\n--- Test Case ---")
print(f"Result  : {test_result}")
print(f"Expected: {expected}")
print(f"Pass: {test_result == expected}")