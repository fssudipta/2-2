import numpy as np
import matplotlib.pyplot as plt
from PIL import Image as PILImage


# ── Load images ───────────────────────────────────────────────────────────────
image         = np.array(PILImage.open("E:\\2-2\\220 signal\\Practice_DFT\\online 21\\Online_C\\image.png"))
shifted_image = np.array(PILImage.open("E:\\2-2\\220 signal\\Practice_DFT\\online 21\\Online_C\\shifted_image.png"))

def to_gray(img):
    return img.mean(axis=2).astype(np.float64) if img.ndim == 3 else img.astype(np.float64)

img_gray  = to_gray(image)
simg_gray = to_gray(shifted_image)
H, W = img_gray.shape


# ── Helper: FFT-based circular cross-correlation ──────────────────────────────
def cross_corr_fft(a, b):
    """r[l] = IFFT( FFT(a) * conj(FFT(b)) )  — peak at l gives shift of b vs a."""
    A = np.fft.fft(a)
    B = np.fft.fft(b)
    return np.real(np.fft.ifft(A * np.conjugate(B)))


# ── Wise row / column selection ───────────────────────────────────────────────
# Pick row / col that has signal variation in BOTH images (maximises product of variances)
row_idx = int(np.argmax(np.var(img_gray, axis=1) * np.var(simg_gray, axis=1)))
col_idx = int(np.argmax(np.var(img_gray, axis=0) * np.var(simg_gray, axis=0)))
print(f"Selected row {row_idx} for horizontal shift, col {col_idx} for vertical shift")


# ── Step 1: Horizontal shift ──────────────────────────────────────────────────
corr_h = cross_corr_fft(img_gray[row_idx, :], simg_gray[row_idx, :])
h_raw  = int(np.argmax(corr_h))
horizontal_shift = h_raw if h_raw <= W // 2 else h_raw - W
print(f"Detected horizontal shift: {horizontal_shift} pixels")


# ── Step 2: Vertical shift ────────────────────────────────────────────────────
corr_v = cross_corr_fft(img_gray[:, col_idx], simg_gray[:, col_idx])
v_raw  = int(np.argmax(corr_v))
vertical_shift = v_raw if v_raw <= H // 2 else v_raw - H
print(f"Detected vertical shift  : {vertical_shift} pixels")


# ── Step 3: Reverse the shift ─────────────────────────────────────────────────
reversed_shifted_image = np.roll(simg_gray, vertical_shift, axis=0)
reversed_shifted_image = np.roll(reversed_shifted_image, horizontal_shift, axis=1)

diff = np.abs(img_gray - reversed_shifted_image)
print(f"Max pixel difference after realignment : {diff.max():.2f}")
print(f"Mean pixel difference after realignment: {diff.mean():.4f}")


# ── Visualise ─────────────────────────────────────────────────────────────────
plt.figure(figsize=(14, 8))

plt.subplot(2, 3, 1)
plt.imshow(img_gray, cmap='gray'); plt.title("Original Image"); plt.axis('off')

plt.subplot(2, 3, 2)
plt.imshow(simg_gray, cmap='gray'); plt.title("Shifted Image"); plt.axis('off')

plt.subplot(2, 3, 3)
plt.imshow(reversed_shifted_image, cmap='gray')
plt.title(f"Reversed Shifted Image\n(h={horizontal_shift}, v={vertical_shift})")
plt.axis('off')

plt.subplot(2, 3, 4)
plt.plot(corr_h)
plt.axvline(h_raw, color='r', linestyle='--', label=f'peak={h_raw} → shift={horizontal_shift}')
plt.title("Horizontal Cross-Correlation"); plt.xlabel("Lag"); plt.legend(); plt.grid(True)

plt.subplot(2, 3, 5)
plt.plot(corr_v)
plt.axvline(v_raw, color='r', linestyle='--', label=f'peak={v_raw} → shift={vertical_shift}')
plt.title("Vertical Cross-Correlation"); plt.xlabel("Lag"); plt.legend(); plt.grid(True)

plt.subplot(2, 3, 6)
plt.imshow(diff, cmap='hot'); plt.title(f"Difference (max={diff.max():.1f})")
plt.colorbar(); plt.axis('off')

plt.tight_layout()
plt.show()
print("Done.")