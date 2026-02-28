import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import time
import scipy.io.wavfile as wav
import sounddevice as sd
from discrete_framework import DFTAnalyzer, DiscreteSignal, FastFourierTransform

class AudioEqualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("DFT Audio Equalizer")
        
        self.samplerate = 0
        self.original_audio = None
        self.processed_audio = None
        
        # --- UI Layout ---
        top_frame = tk.Frame(root)
        top_frame.pack(pady=10)
        
        tk.Button(top_frame, text="Load WAV File", command=self.load_file).pack(side=tk.LEFT, padx=10)
        tk.Button(top_frame, text="Process & Play", command=self.process_and_play).pack(side=tk.LEFT, padx=10)
        tk.Button(top_frame, text="Stop Audio", command=sd.stop).pack(side=tk.LEFT, padx=10)
        
        # Toggle Switch
        control_frame = tk.Frame(root)
        control_frame.pack(pady=5)
        self.use_fft = tk.BooleanVar(value=False)
        tk.Label(control_frame, text="Algorithm: ").pack(side=tk.LEFT)
        tk.Radiobutton(control_frame, text="DFT (Slow)", variable=self.use_fft, value=False).pack(side=tk.LEFT)
        tk.Radiobutton(control_frame, text="FFT (Fast)", variable=self.use_fft, value=True).pack(side=tk.LEFT)

        # Equalizer Sliders
        self.slider_frame = tk.Frame(root)
        self.slider_frame.pack(pady=20, padx=20)
        
        self.sliders = []
        labels = ["Low", "Low-Mid", "Mid", "High-Mid", "High"]
        for i in range(5):
            frame = tk.Frame(self.slider_frame)
            frame.pack(side=tk.LEFT, padx=5)
            tk.Label(frame, text=labels[i], font=("Arial", 8)).pack()
            slider = tk.Scale(frame, from_=2.0, to=0.0, resolution=0.1, length=150, orient=tk.VERTICAL)
            slider.set(1.0)
            slider.pack()
            self.sliders.append(slider)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if file_path:
            try:
                self.samplerate, data = wav.read(file_path)
                
                # Normalize to float [-1, 1]
                if data.dtype == np.int16:
                    data = data.astype(np.float32) / 32768.0
                elif data.dtype == np.int32:
                    data = data.astype(np.float32) / 2147483648.0
                elif data.dtype == np.uint8:
                    data = (data.astype(np.float32) - 128.0) / 128.0
                
                # If already float, just ensure float32
                if data.dtype != np.float32:
                    data = data.astype(np.float32)

                # Convert to mono if stereo
                if len(data.shape) > 1:
                    data = np.mean(data, axis=1)
                
                self.original_audio = data
                self.processed_audio = None
                duration = len(data) / self.samplerate
                print(f"Loaded: {len(data)} samples, {self.samplerate} Hz, {duration:.1f}s")
            except Exception as e:
                messagebox.showerror("Error", f"Could not load file: {e}")

    def process_and_play(self):
        if self.original_audio is None:
            messagebox.showwarning("Warning", "Please load a WAV file first.")
            return
        
        print("Starting processing...")
        # Get Slider Values
        gains = [s.get() for s in self.sliders]
        
        # TODO: Implement the chunking, FFT, filtering, IFFT, and overlap-add here.
        if self.use_fft.get():
            analyzer = FastFourierTransform()
        else:
            analyzer = DFTAnalyzer()
        chunk_size = 1024
        audio = self.original_audio.astype(np.float64)
        total_samples = len(audio)
        output = np.zeros(total_samples, dtype=np.float64)

        num_chunks = int(np.ceil(total_samples/chunk_size))
        for i in range(num_chunks):
            # extract chunk
            start = i*chunk_size
            end = min(start+chunk_size, total_samples)
            chunk = audio[start:end]
            actual_len = len(chunk)

            # zero pad last chunk to chunk_size if needed
            if actual_len<chunk_size:
                padded = np.zeros(chunk_size, dtype=np.float64)
                padded[:actual_len]=chunk
                chunk_to_process = padded
            else:
                chunk_to_process=chunk
            t_start=time.time()

            N = len(chunk_to_process)
            # frequency analysis
            signal = DiscreteSignal(chunk_to_process)
            spectrum = analyzer.compute_dft(signal)
            t_end = time.time()
            print(f"Chunk {i+1}/{num_chunks} | DFT time: {t_end - t_start:.4f}s")
            # filtering
            filtered_spectrum = spectrum.copy()
            band_size = N//5
            for idx in range(5):
                gain= gains[idx]
                pos_start=idx*band_size #pos freq bin range for this band
                pos_end = (idx+1)*band_size if idx<4 else N//2+1
                #applying gain to the pos bins
                filtered_spectrum[pos_start:pos_end]*=gain
                #mirror symmetrically to negative freq bins
                #negative counterpart of bin k is bin N-k
                if pos_start>0:
                    neg_start = N - pos_end +1
                    neg_end = N-pos_start+1
                    if 0<neg_start<N and neg_end<=N:
                        filtered_spectrum[neg_start:neg_end]*=gain
            #reconstruction
            time_domain = analyzer.compute_idft(filtered_spectrum)
            # take real part only
            reconstructed = time_domain.real[:actual_len]
            #stitch the chunks
            output[start:end] = reconstructed
        # nomalizing to prevent clipping while preserving relative dynamics
        max_val = np.max(np.abs(output))
        if max_val>1e-9:
            output=output/max_val
        self.processed_audio=output.astype(np.float32)
        print(f"Processing complete. Output: {len(self.processed_audio)} samples")
        
        # For starter code, we just play the original audio so the button "works"
        # In the final version, this should play self.processed_audio

        """output_audio = self.original_audio 
        self.processed_audio = output_audio """
    
        sd.stop()
        #default_output = sd.default.device[0]
        #sd.play(self.processed_audio, self.samplerate, device=default_output)
        sd.play(self.processed_audio, self.samplerate)

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioEqualizer(root)
    root.mainloop()