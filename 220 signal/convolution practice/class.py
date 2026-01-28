import numpy as np
import matplotlib.pyplot as plt


class ContinuousSignal:
    def __init__(self, func):
        self.func = func

    def shift(self, shift_val):
        return ContinuousSignal(lambda t: self.func(t - shift_val))

    def add(self, other):
        return ContinuousSignal(lambda t: self.func(t) + other.func(t))

    def multiply(self, other):
        return ContinuousSignal(lambda t: self.func(t) * other.func(t))

    def multiply_const_factor(self, scalar):
        return ContinuousSignal(lambda t: scalar * self.func(t))

    def plot(self, t_min, t_max, num_points, title="", ax=None, label=None, color=None):
        t = np.linspace(t_min, t_max, num_points)
        y = self.func(t)
        if ax is None:
            plt.plot(t, y, label=label, color=color)
            plt.title(title)
            plt.grid(True)
        else:
            ax.plot(t, y, label=label, color=color)
            ax.set_title(title)
            ax.grid(True)

class LTI_Continuous:
    def __init__(self, impulse_response):
        self.impulse_response = impulse_response

    def linear_combination_of_impulses(self, input_signal, delta):
        # We define the window for decomposition based on typical T=3 range
        tk_values = np.arange(-3, 3, delta)
        impulses = []
        coefficients = []
        
        for tk in tk_values:
            # Rectangular impulse: 1/delta for 0 <= t < delta, else 0
            rect = lambda t, tk=tk: np.where((t >= tk) & (t < tk + delta), 1.0/delta, 0)
            impulses.append(ContinuousSignal(rect))
            # ck = x(tk) * delta
            coefficients.append(input_signal.func(tk) * delta)
            
        return impulses, coefficients

    def output_approx(self, input_signal, delta):
        raise NotImplementedError("Not required for this practice.")

def main():
    import os
    os.makedirs("convolution practice", exist_ok=True)

    # --- Step 1: Define Signals ---
    # x(t) = e^-t * u(t)
    x_func = lambda t: np.where(t >= 0, np.exp(-t), 0)
    x = ContinuousSignal(x_func)
    
    # h(t) = u(t)
    h_func = lambda t: np.where(t >= 0, 1.0, 0)
    h = ContinuousSignal(h_func)
    
    lti_system = LTI_Continuous(h)
    T = 3

    # --- Figure 1: Input Signal ---
    plt.figure(figsize=(8, 4))
    x.plot(-T, T, 1000, title="Figure 1: Input Signal x(t)")
    plt.xlabel("t (Time)")
    plt.ylabel("x(t)")
    plt.savefig('convolution practice/figure1.png')

    # --- Figure 2: Impulse Components & Reconstruction ---
    delta_fig2 = 0.5
    impulses, coeffs = lti_system.linear_combination_of_impulses(x, delta_fig2)
    
    fig, axes = plt.subplots(5, 3, figsize=(12, 15), constrained_layout=True)
    axes = axes.flatten()
    
    reconstructed_func = lambda t: 0
    reconstructed_signal = ContinuousSignal(reconstructed_func)

    # Plot first 12 components
    for i in range(12):
        comp_signal = impulses[i].multiply_const_factor(coeffs[i])
        comp_signal.plot(-T, T, 500, ax=axes[i], title=f"Component k={i}")
        # Build reconstruction
        old_func = reconstructed_signal.func
        new_comp_func = comp_signal.func
        reconstructed_signal = ContinuousSignal(lambda t, f1=old_func, f2=new_comp_func: f1(t) + f2(t))

    # Plot final reconstruction in the 13th slot
    reconstructed_signal.plot(-T, T, 1000, ax=axes[12], title="Reconstructed Signal")
    for j in range(13, 15): axes[j].axis('off') # Hide empty subplots
    
    plt.savefig('convolution practice/figure2.png')

    # --- Figure 3: Varying Delta ---
    deltas = [0.5, 0.1, 0.05, 0.01]
    fig3, axes3 = plt.subplots(2, 2, figsize=(12, 10))
    axes3 = axes3.flatten()

    for i, d in enumerate(deltas):
        imps, cs = lti_system.linear_combination_of_impulses(x, d)
        # Summing all impulses for reconstruction
        def get_recon(t_val, imps=imps, cs=cs):
            total = np.zeros_like(t_val)
            for imp, c in zip(imps, cs):
                total += c * imp.func(t_val)
            return total
        
        t_space = np.linspace(-T, T, 1000)
        axes3[i].plot(t_space, x.func(t_space), label="Original x(t)", alpha=0.7)
        axes3[i].plot(t_space, get_recon(t_space), '--', label=f"Recon ($\Delta$={d})")
        axes3[i].set_title(f"$\Delta$ = {d}")
        axes3[i].legend()
        axes3[i].grid(True)

    plt.tight_layout()
    plt.savefig('convolution practice/figure3.png')
    plt.show()

if __name__ == "__main__":
    main()