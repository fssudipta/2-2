import tkinter as tk
import numpy as np
import math
from discrete_framework import DiscreteSignal, DFTAnalyzer, FastFourierTransform

class DoodlingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fourier Epicycles Doodler")
        
        # --- UI Layout ---
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack()
        
        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)
        
        # Buttons
        tk.Button(control_frame, text="Clear Canvas", command=self.clear).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Draw Epicycles", command=self.run_transform).pack(side=tk.LEFT, padx=5)
        
        # Toggle Switch (Radio Buttons)
        self.use_fft = tk.BooleanVar(value=False)
        tk.Label(control_frame, text=" |  Algorithm: ").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(control_frame, text="Naive DFT", variable=self.use_fft, value=False).pack(side=tk.LEFT)
        tk.Radiobutton(control_frame, text="FFT", variable=self.use_fft, value=True).pack(side=tk.LEFT)

        # State Variables
        self.points = []
        self.drawing = False
        self.fourier_coeffs = None
        self.is_animating = False
        self.after_id = None

        # Bindings
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

    def start_draw(self, event):
        self.is_animating = False
        if self.after_id:
            self.root.after_cancel(self.after_id)
        self.canvas.delete("all")
        self.points = []
        self.drawing = True

    def draw(self, event):
        if self.drawing:
            x, y = event.x, event.y
            self.points.append((x, y))
            r = 2
            self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="black", outline="black")

    def end_draw(self, event):
        self.drawing = False

    def clear(self):
        self.canvas.delete("all")
        self.points = []
        self.is_animating = False
        if self.after_id:
            self.root.after_cancel(self.after_id)

    def draw_epicycle(self, x, y, radius):
        """
        Helper method for students to draw a circle (epicycle).
        x, y: Center coordinates
        radius: Radius of the circle
        """
        self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, outline="blue", tags="epicycle")

    def run_transform(self):
        # if not self.points: return
        if len(self.points)<2: return
        # TODO: Implementation
        # 1. Convert (x,y) points to Complex Signal
        z_data = [complex(p[0], p[1]) for p in self.points]
        signal = DiscreteSignal(z_data)
        # 2. Select Algorithm 
        if self.use_fft.get():
            analyzer = FastFourierTransform()
            N_orig = len(signal)
            new_N = 2**(int(np.ceil(np.log2(N_orig))))
            signal = signal.interpolate(new_N)
        else: 
            analyzer=DFTAnalyzer()
        # 3. Compute Transform
        coeffs = analyzer.compute_dft(signal)
        N = len(coeffs)

        mean_val = coeffs[0]/N
        mean_point = (mean_val.real, mean_val.imag)

        self.fourier_coeffs = []
        for k in range(N):
            self.fourier_coeffs.append({
                'freq': k,
                'radius': np.abs(coeffs[k])/N,
                'phase': np.angle(coeffs[k])
            })
        self.fourier_coeffs.sort(key=lambda c: c['radius'], reverse=True)
        self.canvas.delete("trail")
        self.path_trail=[]

        self.animate_epicycles(mean_point)
        
        print("Transform logic needed.")
        # self.animate_epicycles(mean_point)

    def animate_epicycles(self, center_offset):
        self.is_animating = True
        self.time_step = 0
        # self.num_frames = ...
        self.num_frames = len(self.fourier_coeffs) 
        self.center_offset = center_offset
        self.update_frame()

    def update_frame(self):
        if not self.is_animating: return
        
        self.canvas.delete("epicycle") 
        
        # TODO: Implementation
        # 1. Calculate the current time 't' based on self.time_step
        N = self.num_frames
        t = self.time_step
        # 2. Reconstruct the signal value 'z' at time 't' 
        x = self.center_offset[0]
        y = self.center_offset[1]
        # 3. Draw the epicycles:
        for coeff in self.fourier_coeffs:
            prev_x = x
            prev_y = y
            freq   = coeff['freq']
            radius = coeff['radius']
            phase  = coeff['phase']

            angle = (2 * np.pi * freq * t / N) + phase
            self.draw_epicycle(prev_x, prev_y, radius)
            x += radius * np.cos(angle)
            y += radius * np.sin(angle)
            self.canvas.create_line(prev_x, prev_y, x, y, fill="red", tags="epicycle")

        # 4. Draw the tips
        r=3
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="green", tags="epicycle")
        self.path_trail.append((x, y))
        if len(self.path_trail) > 1:
            for i in range(1, len(self.path_trail)):
                x1, y1 = self.path_trail[i-1]
                x2, y2 = self.path_trail[i]
                self.canvas.create_line(x1, y1, x2, y2,
                                        fill="black", width=2, tags="trail")
        
        self.time_step = (self.time_step + 1) %N
        if self.time_step==0:
            self.path_trail=[]

        # Loop animation
        
        self.after_id = self.root.after(50, self.update_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = DoodlingApp(root)
    root.mainloop()