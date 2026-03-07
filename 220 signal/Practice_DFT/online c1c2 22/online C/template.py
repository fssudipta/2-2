import cv2
import numpy as np
import math


def fft(x):
    """
    Compute 1D FFT using Radix-2 Cooley-Tukey algorithm.
    Input length must be a power of 2 (caller is responsible for padding).
    """
    x = np.asarray(x, dtype=np.complex128)
    N = len(x)

    # Base case
    if N == 1:
        return x

    if N & (N - 1):
        raise ValueError(f"FFT length must be a power of 2, got {N}")

    # Divide: even / odd indices
    even = fft(x[::2])
    odd  = fft(x[1::2])

    # Twiddle factors
    k  = np.arange(N // 2)
    tw = np.exp(-2j * np.pi * k / N) * odd

    return np.concatenate([even + tw, even - tw])


def ifft(X):
    """
    Compute 1D inverse FFT using the forward FFT function.
    Uses the identity:  IFFT(X) = conj(FFT(conj(X))) / N
    """
    X = np.asarray(X, dtype=np.complex128)
    N = len(X)
    return np.conjugate(fft(np.conjugate(X))) / N


def _next_power_of_2(n):
    p = 1
    while p < n:
        p <<= 1
    return p


def _fft_row(row):
    """Zero-pad row to next power of 2 and compute FFT."""
    N = len(row)
    M = _next_power_of_2(N)
    padded = np.zeros(M, dtype=np.complex128)
    padded[:N] = row
    return fft(padded), N, M


def detect_row_shift(orig_row, shift_row):
    """
    Detect the circular shift of shift_row relative to orig_row using
    FFT-based cross-correlation.

    Cross-correlation in the frequency domain:
        R[k] = FFT(orig)[k] * conj(FFT(shifted)[k])
        r[n] = IFFT(R)[n]
    The lag n at which r[n] is maximum gives the shift amount.
    """
    W = len(orig_row)
    M = _next_power_of_2(W)

    # Pad both rows to the same power-of-2 length
    a = np.zeros(M, dtype=np.complex128)
    b = np.zeros(M, dtype=np.complex128)
    a[:W] = orig_row
    b[:W] = shift_row

    A = fft(a)
    B = fft(b)

    # Cross-correlation: R = FFT(orig) * conj(FFT(shifted))
    R = A * np.conjugate(B)
    r = np.real(ifft(R))

    # Peak location (only consider lags within valid range [0, W-1])
    peak = int(np.argmax(r[:W]))

    # Wrap to [-W/2, W/2) so we get the signed shortest shift
    shift = peak if peak <= W // 2 else peak - W
    return shift


def reconstruct_image_using_fft(original_path, shifted_path, output_path):

    original_img = cv2.imread(original_path)
    shifted_img  = cv2.imread(shifted_path)

    if original_img is None or shifted_img is None:
        print("Error: Could not load images.")
        return

    if original_img.shape != shifted_img.shape:
        print("Error: Image dimensions do not match.")
        return

    # Convert the original and shifted color images to grayscale.
    orig_gray  = cv2.cvtColor(original_img,  cv2.COLOR_BGR2GRAY).astype(np.float64)
    shift_gray = cv2.cvtColor(shifted_img,   cv2.COLOR_BGR2GRAY).astype(np.float64)

    H, W = orig_gray.shape
    reconstructed_img = np.zeros_like(shift_gray)

    print("Reconstructing image using manual FFT...")

    for row_idx in range(H):
        # Detect how much this row was circularly shifted to the right
        s = detect_row_shift(orig_gray[row_idx], shift_gray[row_idx])

        # Reverse the detected shift: roll the shifted row by +s (undo right-shift)
        reconstructed_img[row_idx] = np.roll(shift_gray[row_idx], s)

        if (row_idx + 1) % 50 == 0 or row_idx == H - 1:
            print(f"  Processed {row_idx + 1}/{H} rows ...")

    # Clip to valid uint8 range
    reconstructed_img = np.clip(reconstructed_img, 0, 255).astype(np.uint8)

    cv2.imwrite(output_path, reconstructed_img)
    print(f"Reconstructed image saved to: {output_path}")

    # ── Verification ──────────────────────────────────────────────────────────
    orig_g = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY).astype(np.float64)
    diff   = np.abs(orig_g - reconstructed_img.astype(np.float64))
    print(f"\nVerification:")
    print(f"  Max pixel difference : {diff.max():.2f}")
    print(f"  Mean pixel difference: {diff.mean():.4f}")
    if diff.mean() < 5.0:
        print("  ✓ Reconstruction successful — images match!")
    else:
        print("  ✗ Reconstruction may have errors.")


if __name__ == "__main__":
    reconstruct_image_using_fft(
        "E:\\2-2\\220 signal\\Practice_DFT\\online c1c2 22\\original_image.png",
        "E:\\2-2\\220 signal\\Practice_DFT\\online c1c2 22\\shifted_image.jpg",
        "E:\\2-2\\220 signal\\Practice_DFT\\online c1c2 22\\reconstructed_image_fft.jpg"
    )