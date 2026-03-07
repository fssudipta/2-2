import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

image = Image.open("E:\\2-2\\220 signal\\Practice_DFT\\online 21\\Online_B\\encrypted_image.tiff")
encrypted_image = np.array(image, dtype=np.float64)

row_sums=encrypted_image.sum(axis=1)
key_row_idx=int(np.argmin(row_sums))

key_row=encrypted_image[key_row_idx, :]
key = np.fft.fft(key_row)
decrypted_image=np.zeros_like(encrypted_image)
for i in range(encrypted_image.shape[0]):
    e_row = np.fft.fft(encrypted_image[i, :])
    O_row = e_row/(key+1e-12)
    decrypted_row=np.real(np.fft.ifft(O_row))
    decrypted_image[i,:]=decrypted_row
decrypted_image=np.clip(np.round(decrypted_image))