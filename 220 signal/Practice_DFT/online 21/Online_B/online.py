import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


# ── Load encrypted image ──────────────────────────────────────────────────────
image = Image.open("E:\\2-2\\220 signal\\Practice_DFT\\online 21\\Online_B\\encrypted_image.tiff")
encrypted_image = np.array(image, dtype=np.float64)

# ── Step 1: Identify the key row ──────────────────────────────────────────────
# Clue: the key row has much smaller pixel values than all encrypted rows.
# Find the row index corresponding to the minimum value in any column.
# We use the sum of each row as a proxy (smallest sum = key row).
row_sums = encrypted_image.sum(axis=1)
key_row_idx = int(np.argmin(row_sums))
print(f"Key row index: {key_row_idx}")

key_row = encrypted_image[key_row_idx, :]

# ── Step 2: Decrypt every row via DFT ────────────────────────────────────────
# Encryption: encrypted_row = original_row ⊛ key_row
# In frequency domain: E(k) = O(k) * KEY(k)
# Therefore: O(k) = E(k) / KEY(k)  →  original_row = IFFT( FFT(encrypted) / FFT(key) )

KEY = np.fft.fft(key_row)

decrypted_image = np.zeros_like(encrypted_image)

for i in range(encrypted_image.shape[0]):
    E_row = np.fft.fft(encrypted_image[i, :])
    # Avoid division by zero (shouldn't happen for a valid key, but just in case)
    O_row = E_row / (KEY + 1e-12)
    decrypted_row = np.real(np.fft.ifft(O_row))
    decrypted_image[i, :] = decrypted_row

# Clip to valid pixel range
decrypted_image = np.clip(np.round(decrypted_image), 0, 255).astype(np.uint8)

# ── Visualise ─────────────────────────────────────────────────────────────────
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(encrypted_image, cmap='gray')
plt.title("Encrypted Image")
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(decrypted_image, cmap='gray')
plt.title("Decrypted Image")
plt.axis('off')

plt.tight_layout()
plt.show()
print("Done. Decrypted image saved.")