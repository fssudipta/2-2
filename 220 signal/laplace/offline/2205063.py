import numpy as np
import matplotlib.pyplot as plt


class SmartIrrigation:
    def __init__(self, a=0.5, b=1.0, t_max=20, dt=0.01):
        self.a = a
        self.b = b
        self.t_max = t_max
        self.dt = dt
        self.t = np.arange(0, t_max + dt, dt)

    def u_step(self):
        return np.ones_like(self.t)

    def u_ramp(self):
        return 0.1 * self.t

    def u_sin(self):
        return np.sin(0.5 * self.t)

    def u_exponential(self):
        return 1 - np.exp(-0.3 * self.t)

    def u_pulse(self):
        return np.where(self.t < 5, 1.0, 0.0)

    def laplace_transform(self, f, s):
        s = complex(s)  # making sure s is complex
        integrand = f * np.exp(-s * self.t)  # the function inside the integral
        if len(integrand) < 2:
            return 0.0
        # trapezoidal rule(from slides): (dt/2)*(first+last)+dt*sum(mid points)
        integral = (self.dt / 2) * (
            integrand[0] + integrand[-1] + 2 * np.sum(integrand[1:-1])
        )
        return integral

    def inverse_laplace(self, s_list, F_s_values):
        s_arr = np.asarray(s_list, dtype=complex)  # all s points on the contour
        H_arr = np.asarray(F_s_values, dtype=complex)
        omega = np.imag(s_arr)  # extract the omega values
        if len(omega) < 2:
            return np.zeros_like(self.t)
        domega = omega[1] - omega[0]
        c = np.real(s_arr[0])  # real part is the same for all
        exp_i_terms = np.exp(1j * np.outer(omega, self.t))
        complex_sum = np.dot(H_arr, exp_i_terms)  # sum over all contour points
        # final formula
        h = (domega / (2 * np.pi)) * np.real(complex_sum) * np.exp(c * self.t)
        return h

    def H_s(self, s, U_s):
        # trasnfer func according to the pdf
        s = complex(s)
        return (self.b / (self.a + s)) * U_s

    def steady_state(self, h):
        """Mean of last 5% of signal."""
        n5 = max(1, int(0.05 * len(h)))
        return float(np.mean(h[-n5:]))

    def time_constant(self, h):
        """Time to first reach 63.2% of steady-state."""
        h_ss = self.steady_state(h)
        if h_ss <= 0:
            return float("nan")
        tgt = 0.632 * h_ss
        idx = np.where(h >= tgt)[0]
        return float(self.t[idx[0]] if len(idx) > 0 else float("nan"))

    def rise_time(self, h):
        """Time to go from 10% to 90% of steady-state."""
        h_ss = self.steady_state(h)
        if h_ss <= 0:
            return float("nan")
        t10 = np.interp(0.1 * h_ss, h, self.t)
        t90 = np.interp(0.9 * h_ss, h, self.t)
        return t90 - t10

    def settling_time(self, h):
        """Time after which h(t) stays permanently within ±2% of h_ss."""
        h_ss = self.steady_state(h)
        if h_ss <= 0:
            return float("nan")
        band = 0.02 * abs(h_ss)
        out = np.where(np.abs(h - h_ss) > band)[0]
        if len(out) == 0:
            return 0.0
        last_violation_idx = out[-1]
        if last_violation_idx + 1 < len(self.t):
            return float(self.t[last_violation_idx + 1])
        else:
            return float(self.t[-1])  # already at the end

    def overshoot(self, h):
        """Percentage overshoot: (h_max - h_ss) / h_ss * 100."""
        h_ss = self.steady_state(h)
        if h_ss <= 0:
            return 0.0
        h_max = float(np.max(h))
        if h_max <= h_ss:
            return 0.0
        return float((h_max - h_ss) / h_ss * 100)

    def compute_metrics(self, h):

        return {
            "steady_state": self.steady_state(h),
            "time_constant": self.time_constant(h),
            "rise_time": self.rise_time(h),
            "settling_time": self.settling_time(h),
            "overshoot_%": self.overshoot(h),
        }

    def euler_simulate(self, u):
        """
        Euler method for dh/dt = -a*h(t) + b*u(t)
        h[n+1] = h[n] + dt * (-a*h[n] + b*u[n])
        """
        h = np.zeros_like(self.t)
        for n in range(len(self.t) - 1):
            dhdt = -self.a * h[n] + self.b * u[n]
            h[n + 1] = h[n] + self.dt * dhdt
        return h


# Change values of a, b to experiment with different system dynamics
configs = [
    {"name": "Default (a=0.5, b=1.0)...standard dynamics", "a": 0.5, "b": 1.0},
    {"name": "Slower response (a=0.25, b=1.0)...smaller a", "a": 0.25, "b": 1.0},
    {"name": "Faster response (a=1.0, b=1.0)...larger a", "a": 1.0, "b": 1.0},
    {"name": "Higher gain (a=0.5, b=2.0)...larger b", "a": 0.5, "b": 2.0},
]

for cfg in configs:
    print(cfg["name"])
    system = SmartIrrigation(a=cfg["a"], b=cfg["b"], t_max=20, dt=0.01)

    inputs = {
        "Step Input": system.u_step(),
        "Ramp Input": system.u_ramp(),
        "Sinusoidal Input": system.u_sin(),
        "Exponential Input": system.u_exponential(),
        "Pulse Input": system.u_pulse(),
    }

    # Bromwich contour parameters, set these values
    c = 0.5  # vertical line position. must be >pole at -0.5
    W = 100.0  # covers all frequencies, small W gives us crazy wiggles
    # W basically defines how far up and down tthe vertical line we integrate
    N = 2000  # N controls how finely we sample the vertical line
    domega = 2 * W / N
    omega_k = -W + np.arange(N) * domega
    s_list = c + 1j * omega_k

    colors = ["#2196F3", "#4CAF50", "#FF5722", "#9C27B0", "#FF9800"]

    for idx, (name, u) in enumerate(inputs.items()):
        print(f"Processing: {name}...")

        # --- Laplace --- set these values
        U_s_vals = np.array([system.laplace_transform(u, s) for s in s_list])
        H_s_vals = np.array([system.H_s(s, U_s) for s, U_s in zip(s_list, U_s_vals)])
        h_laplace = system.inverse_laplace(s_list, H_s_vals)
        print(f"\n  ► {name}")
        metrics = system.compute_metrics(h_laplace)
        for k, v in metrics.items():
            print(f"      {k.replace('_',' ').title():<22}: {v}")

        # --- Euler ---
        h_euler = system.euler_simulate(u)

        # --- Plot ---
        fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=False)
        fig.suptitle(f"Smart Irrigation — {name}", fontsize=13, fontweight="bold")

        # Laplace subplot
        axes[0].plot(system.t, u, "b--", lw=1.8, label="Input u(t)")
        axes[0].plot(
            system.t, h_laplace, color=colors[idx], lw=2.2, label="Output h(t)"
        )
        axes[0].set_title("Laplace Transform Simulation", fontweight="bold")
        axes[0].set_xlabel("Time (s)", fontsize=11)
        axes[0].set_ylabel("Water Level / Input", fontsize=11)
        axes[0].legend(fontsize=10)
        axes[0].grid(True, alpha=0.3)

        # Euler subplot
        axes[1].plot(system.t, u, "b--", lw=1.8, label="Input u(t)")
        axes[1].plot(system.t, h_euler, color="tomato", lw=2.2, label="Output h(t)")
        axes[1].set_title("Euler Method Simulation", fontweight="bold")
        axes[1].set_xlabel("Time (s)", fontsize=11)
        axes[1].set_ylabel("Water Level / Input", fontsize=11)
        axes[1].legend(fontsize=10)
        axes[1].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()
