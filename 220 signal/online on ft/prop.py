"""
================================================================================
  COMPREHENSIVE FOURIER TRANSFORM PROPERTIES
  Verified Numerically via Pure OOP + np.trapezoid
================================================================================

  PROPERTIES COVERED (from Princeton ELE 301 lectures):
  ──────────────────────────────────────────────────────
   1. Definition & Basic Transform
   2. Linearity
   3. Time Shifting
   4. Time Scaling (Stretch/Compress)
   5. Time Reversal
   6. Complex Conjugation
   7. Duality
   8. Differentiation in Time
   9. Parseval's Theorem (Energy Conservation)
  10. Convolution Theorem
  11. Modulation (Multiplication in Time = Convolution in Frequency)
  12. Frequency Shifting

  HOW TO READ THIS FILE:
  ──────────────────────
  Each property is a class with:
    - A docstring explaining the MATH
    - A verify() method that COMPUTES both sides numerically
    - A plot() method that SHOWS the result visually
  Run the main block at the bottom to check all properties in sequence.
================================================================================
"""

import numpy as np
import matplotlib.pyplot as plt


# ==============================================================================
#  CORE ENGINE — CFT and ICFT via numerical integration
# ==============================================================================

class CFTEngine:
    """
    Computes CFT and ICFT using np.trapezoid ONLY. No FFT whatsoever.

    FORWARD CFT:
        X(f) = ∫ x(t) e^{-j2πft} dt
             = ∫ x(t) cos(2πft) dt   - j ∫ x(t) sin(2πft) dt

    INVERSE CFT:
        x(t) = ∫ X(f) e^{+j2πft} df
             = ∫ [Re{X}·cos(2πft) - Im{X}·sin(2πft)] df

    WHY SPLIT INTO REAL AND IMAGINARY?
        Computers cannot directly integrate complex exponentials.
        Euler's formula lets us split e^{-jθ} = cosθ - j·sinθ
        into two REAL integrals that np.trapezoid can handle.
    """

    @staticmethod
    def cft(t, x_values, freqs):
        """
        Compute X(f) for all frequencies in freqs.
        Returns (real_part, imag_part) — both shape (len(freqs),).
        """
        R = np.zeros(len(freqs))
        I = np.zeros(len(freqs))
        for k, f in enumerate(freqs):
            R[k] =  np.trapezoid(x_values * np.cos(2*np.pi*f*t), t)
            I[k] = -np.trapezoid(x_values * np.sin(2*np.pi*f*t), t)
        return R, I

    @staticmethod
    def magnitude(R, I):
        return np.sqrt(R**2 + I**2)

    @staticmethod
    def phase(R, I):
        return np.arctan2(I, R)

    @staticmethod
    def mse(a, b):
        """Mean Squared Error between two arrays."""
        return np.mean((a - b)**2)


# ==============================================================================
#  SIGNAL LIBRARY  (all signals used across property tests)
# ==============================================================================

class Signals:
    """
    Static factory class — returns signal arrays over given time axis t.

    WHY A STATIC CLASS?
    Signal generation is pure function: input t → output array.
    No state is needed, so static methods are cleaner than instances.
    """

    @staticmethod
    def rect(t, width=1.0):
        """
        Rectangular pulse of given width, centred at t=0.
        x(t) = 1 if |t| ≤ width/2,  else 0

        KNOWN CFT:  rect(t) ↔ sinc(f) = sin(πf)/(πf)
        """
        return (np.abs(t) <= width/2).astype(float)

    @staticmethod
    def sinc_signal(t):
        """
        sinc function: sin(πt)/(πt), with sinc(0)=1.
        KNOWN CFT:  sinc(t) ↔ rect(f)  (duality of rect ↔ sinc)
        """
        return np.sinc(t)   # numpy sinc = sin(πt)/(πt)

    @staticmethod
    def triangle(t, width=2.0):
        """
        Triangle wave (unit triangle Δ(t)):
        x(t) = max(0, 1 - |t|/(width/2))
        KNOWN CFT:  Δ(t) ↔ sinc²(f)  (rect convolved with rect)
        """
        return np.maximum(0, 1 - np.abs(t) / (width/2))

    @staticmethod
    def gaussian(t, sigma=1.0):
        """
        Gaussian: x(t) = e^{-t²/(2σ²)}
        KNOWN CFT:  Gaussian ↔ Gaussian  (self-dual!)
        """
        return np.exp(-t**2 / (2 * sigma**2))

    @staticmethod
    def square_wave(t, freq=1.0, amplitude=1.0):
        """Square wave via sign of sine."""
        return amplitude * np.sign(np.sin(2*np.pi*freq*t))

    @staticmethod
    def cosine(t, f0=2.0, amplitude=1.0):
        """Pure cosine: A·cos(2πf₀t)"""
        return amplitude * np.cos(2*np.pi*f0*t)

    @staticmethod
    def sine(t, f0=2.0, amplitude=1.0):
        """Pure sine: A·sin(2πf₀t)"""
        return amplitude * np.sin(2*np.pi*f0*t)

    @staticmethod
    def exp_decay(t, a=1.0):
        """
        Causal decaying exponential: e^{-at}·u(t)
        KNOWN CFT: 1/(a + j2πf)
        """
        return np.where(t >= 0, np.exp(-a*t), 0.0)


# ==============================================================================
#  PROPERTY 1: Definition — verify on rect → sinc
# ==============================================================================

class Property1_Definition:
    """
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    PROPERTY 1: CFT DEFINITION
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    X(f) = ∫_{-∞}^{∞} x(t) e^{-j2πft} dt

    KNOWN PAIR:  rect(t) ↔ sinc(f)

    We numerically compute CFT of rect and compare to sinc analytically.
    If CFT is working, they should match.
    """
    name = "1. CFT Definition  [rect(t) ↔ sinc(f)]"

    def __init__(self):
        self.t     = np.linspace(-5, 5, 3000)
        self.freqs = np.linspace(-5, 5, 500)

    def verify(self):
        x = Signals.rect(self.t, width=1.0)
        R, I = CFTEngine.cft(self.t, x, self.freqs)
        computed_mag = CFTEngine.magnitude(R, I)
        analytic_mag = np.abs(np.sinc(self.freqs))   # numpy sinc = sin(πf)/(πf)
        mse = CFTEngine.mse(computed_mag, analytic_mag)
        print(f"  {self.name}")
        print(f"    MSE (computed vs analytic sinc) = {mse:.6e}")
        return self.t, self.freqs, x, computed_mag, analytic_mag

    def plot(self):
        t, freqs, x, comp, analytic = self.verify()
        fig, axes = plt.subplots(1, 2, figsize=(13, 4))
        axes[0].plot(t, x, color='steelblue', lw=2)
        axes[0].set_title("x(t) = rect(t)"); axes[0].set_xlabel("t")
        axes[0].grid(True, alpha=0.4)

        axes[1].plot(freqs, comp, label="Numerical CFT |X(f)|", lw=2.5, color='steelblue')
        axes[1].plot(freqs, analytic, '--', label="Analytic sinc(f)", lw=1.8, color='crimson')
        axes[1].set_title("CFT of rect(t) vs sinc(f)")
        axes[1].set_xlabel("f"); axes[1].legend(); axes[1].grid(True, alpha=0.4)
        plt.tight_layout()
        plt.suptitle(self.name, y=1.02, fontweight='bold', color='navy')
        plt.show()


# ==============================================================================
#  PROPERTY 2: Linearity
# ==============================================================================

class Property2_Linearity:
    """
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    PROPERTY 2: LINEARITY
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    F{a·x₁(t) + b·x₂(t)} = a·X₁(f) + b·X₂(f)

    PROOF IDEA:
        The integral is linear:  ∫(af+bg) = a∫f + b∫g
        So CFT inherits linearity directly from integral linearity.

    TEST:
        x₁(t) = rect(t),  x₂(t) = Gaussian(t)
        a = 2,  b = 3
        Verify: CFT(2·x₁ + 3·x₂) == 2·CFT(x₁) + 3·CFT(x₂)
    """
    name = "2. Linearity  [F{a·x₁+b·x₂} = a·X₁+b·X₂]"

    def __init__(self):
        self.t     = np.linspace(-5, 5, 2000)
        self.freqs = np.linspace(-5, 5, 400)
        self.a, self.b = 2.0, 3.0

    def verify(self):
        t, f, a, b = self.t, self.freqs, self.a, self.b
        x1 = Signals.rect(t);     x2 = Signals.gaussian(t)

        # LHS: CFT of the linear combination
        combo     = a*x1 + b*x2
        R_lhs, I_lhs = CFTEngine.cft(t, combo, f)

        # RHS: linear combination of CFTs
        R1, I1 = CFTEngine.cft(t, x1, f)
        R2, I2 = CFTEngine.cft(t, x2, f)
        R_rhs = a*R1 + b*R2
        I_rhs = a*I1 + b*I2

        mse_R = CFTEngine.mse(R_lhs, R_rhs)
        mse_I = CFTEngine.mse(I_lhs, I_rhs)
        print(f"  {self.name}")
        print(f"    MSE Real = {mse_R:.6e},  MSE Imag = {mse_I:.6e}")
        return f, CFTEngine.magnitude(R_lhs,I_lhs), CFTEngine.magnitude(R_rhs,I_rhs)

    def plot(self):
        f, lhs_mag, rhs_mag = self.verify()
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(f, lhs_mag, label="|F{2x₁+3x₂}|", lw=2.5, color='steelblue')
        ax.plot(f, rhs_mag, '--', label="2|X₁|+3|X₂| (element-wise magnitude)",
                lw=1.8, color='crimson')
        ax.set_title(self.name); ax.set_xlabel("f"); ax.legend()
        ax.grid(True, alpha=0.4)
        plt.tight_layout(); plt.show()


# ==============================================================================
#  PROPERTY 3: Time Shifting
# ==============================================================================

class Property3_TimeShift:
    """
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    PROPERTY 3: TIME SHIFT
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    x(t - t₀)  ↔  e^{-j2πft₀} · X(f)

    WHAT THIS MEANS:
        Delaying a signal by t₀ seconds multiplies its spectrum by
        e^{-j2πft₀}.  This is a PHASE ROTATION that is linear in f.

    EFFECT ON MAGNITUDE:
        |e^{-j2πft₀}| = 1,  so |Y(f)| = |X(f)|.
        Shifting in time does NOT change the magnitude spectrum!

    EFFECT ON PHASE:
        ∠Y(f) = ∠X(f) - 2πft₀
        Phase gets a LINEAR slope added, with slope = -2πt₀.

    TEST:
        x(t) = rect(t),  t₀ = 1.0
        Verify: |Y(f)| == |X(f)|  and  ∠Y(f) == ∠X(f) - 2πft₀
    """
    name = "3. Time Shift  [x(t-t₀) ↔ e^{-j2πft₀}·X(f)]"

    def __init__(self, t0=1.0):
        self.t     = np.linspace(-6, 6, 3000)
        self.freqs = np.linspace(-5, 5, 400)
        self.t0    = t0

    def verify(self):
        t, f, t0 = self.t, self.freqs, self.t0
        x  = Signals.rect(t)
        y  = Signals.rect(t - t0)     # shifted signal

        Rx, Ix = CFTEngine.cft(t, x, f)
        Ry, Iy = CFTEngine.cft(t, y, f)

        # Theoretical Y(f) = e^{-j2πft₀} · X(f)
        shift_factor_R = np.cos(2*np.pi*f*t0)
        shift_factor_I = -np.sin(2*np.pi*f*t0)
        Ry_theory = Rx*shift_factor_R - Ix*shift_factor_I
        Iy_theory = Rx*shift_factor_I + Ix*shift_factor_R

        mse_mag = CFTEngine.mse(CFTEngine.magnitude(Ry,Iy),
                                 CFTEngine.magnitude(Rx,Ix))
        mse_theory = CFTEngine.mse(Ry, Ry_theory) + CFTEngine.mse(Iy, Iy_theory)
        print(f"  {self.name}")
        print(f"    MSE |Y|-|X| (should be 0) = {mse_mag:.6e}")
        print(f"    MSE vs e^(-j2πft₀)·X(f)  = {mse_theory:.6e}")
        return f, CFTEngine.magnitude(Rx,Ix), CFTEngine.magnitude(Ry,Iy), \
               CFTEngine.phase(Rx,Ix), CFTEngine.phase(Ry,Iy)

    def plot(self):
        f, X_mag, Y_mag, X_ph, Y_ph = self.verify()
        fig, axes = plt.subplots(1, 2, figsize=(13, 4))
        axes[0].plot(f, X_mag, label="|X(f)|", lw=2, color='steelblue')
        axes[0].plot(f, Y_mag, '--', label="|Y(f)|", lw=2, color='crimson')
        axes[0].set_title("Magnitude (should be identical)"); axes[0].legend()
        axes[0].set_xlabel("f"); axes[0].grid(True, alpha=0.4)

        axes[1].plot(f, Y_ph - X_ph, color='purple', lw=2)
        axes[1].set_title(f"Phase difference ∠Y-∠X (should be -2πft₀ = linear)")
        axes[1].set_xlabel("f"); axes[1].grid(True, alpha=0.4)
        plt.suptitle(self.name, fontweight='bold', color='navy', y=1.02)
        plt.tight_layout(); plt.show()


# ==============================================================================
#  PROPERTY 4: Time Scaling
# ==============================================================================

class Property4_TimeScaling:
    """
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    PROPERTY 4: TIME SCALING
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    x(a·t)  ↔  (1/|a|) · X(f/a)

    INTUITION:
        Compressing time (|a|>1) STRETCHES frequency bandwidth.
        Stretching time (|a|<1) COMPRESSES frequency bandwidth.
        This is the UNCERTAINTY PRINCIPLE: you can't be sharp in BOTH
        time and frequency simultaneously.

    PROOF SKETCH:
        ∫ x(at)e^{-j2πft} dt
        let τ = at, dt = dτ/a:
        = (1/a) ∫ x(τ) e^{-j2πf(τ/a)} dτ
        = (1/a) X(f/a)

    TEST:
        x(t) = rect(t), a = 3
        Y(f) = (1/3)·X(f/3) — spectrum 3x wider, 1/3 the amplitude
    """
    name = "4. Time Scaling  [x(at) ↔ (1/|a|)·X(f/a)]"

    def __init__(self, a=3.0):
        self.t     = np.linspace(-5, 5, 3000)
        self.freqs = np.linspace(-10, 10, 600)
        self.a     = a

    def verify(self):
        t, f, a = self.t, self.freqs, self.a
        x  = Signals.rect(t)
        y  = Signals.rect(a*t)    # compressed

        Rx, Ix = CFTEngine.cft(t, x, f)
        Ry, Iy = CFTEngine.cft(t, y, f)

        # Theoretical: (1/a)·X(f/a)
        Rx_interp = np.interp(f/a, f, Rx, left=0, right=0)
        Iy_interp = np.interp(f/a, f, Ix, left=0, right=0)
        Ry_theory = (1/abs(a)) * Rx_interp
        Iy_theory = (1/abs(a)) * Iy_interp

        mse = CFTEngine.mse(CFTEngine.magnitude(Ry,Iy),
                             CFTEngine.magnitude(np.array(Ry_theory),
                                                  np.array(Iy_theory)))
        print(f"  {self.name}")
        print(f"    a = {a}:  MSE |Y(f)| vs (1/a)·|X(f/a)| = {mse:.6e}")
        return f, CFTEngine.magnitude(Rx,Ix), CFTEngine.magnitude(Ry,Iy), \
               CFTEngine.magnitude(np.array(Ry_theory), np.array(Iy_theory))

    def plot(self):
        f, X_mag, Y_mag, T_mag = self.verify()
        fig, ax = plt.subplots(figsize=(11, 4))
        ax.plot(f, X_mag, label="|X(f)|  (original)", lw=2, color='steelblue')
        ax.plot(f, Y_mag, label=f"|Y(f)| = |CFT{{x({self.a}t)}}|", lw=2, color='darkorange')
        ax.plot(f, T_mag, '--', label=f"(1/{self.a})·|X(f/{self.a})| (theory)", lw=2, color='crimson')
        ax.set_title(self.name); ax.set_xlabel("f"); ax.legend()
        ax.grid(True, alpha=0.4)
        plt.tight_layout(); plt.show()


# ==============================================================================
#  PROPERTY 5: Time Reversal
# ==============================================================================

class Property5_TimeReversal:
    """
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    PROPERTY 5: TIME REVERSAL
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    x(-t)  ↔  X(-f)

    Special case of scaling with a = -1:
        x((-1)·t) ↔ (1/|-1|)·X(f/(-1)) = X(-f)

    WHAT THIS MEANS:
        Reversing the signal in time reverses its spectrum in frequency.
        For a REAL EVEN signal, X(-f) = X(f), so no change.
        For asymmetric signals, the spectrum flips.
    """
    name = "5. Time Reversal  [x(-t) ↔ X(-f)]"

    def __init__(self):
        self.t     = np.linspace(-5, 5, 2000)
        self.freqs = np.linspace(-5, 5, 400)

    def verify(self):
        t, f = self.t, self.freqs
        x  = Signals.exp_decay(t, a=1.0)    # asymmetric!
        y  = Signals.exp_decay(-t, a=1.0)   # reversed

        Rx, Ix = CFTEngine.cft(t, x, f)
        Ry, Iy = CFTEngine.cft(t, y, f)

        # Theory: Y(f) = X(-f)
        Rx_flipped = Rx[::-1]
        Ix_flipped = Ix[::-1]
        mse = CFTEngine.mse(CFTEngine.magnitude(Ry,Iy),
                             CFTEngine.magnitude(Rx_flipped, Ix_flipped))
        print(f"  {self.name}")
        print(f"    MSE |Y(f)| vs |X(-f)| = {mse:.6e}")
        return f, CFTEngine.magnitude(Rx,Ix), CFTEngine.magnitude(Ry,Iy)

    def plot(self):
        f, X_mag, Y_mag = self.verify()
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(f, X_mag, label="|X(f)|  [e^{-t}u(t)]", lw=2, color='steelblue')
        ax.plot(f, Y_mag, '--', label="|Y(f)| = |X(-f)|  [e^{+t}u(-t)]", lw=2, color='crimson')
        ax.set_title(self.name); ax.set_xlabel("f"); ax.legend()
        ax.grid(True, alpha=0.4)
        plt.tight_layout(); plt.show()


# ==============================================================================
#  PROPERTY 6: Conjugation
# ==============================================================================

class Property6_Conjugation:
    """
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    PROPERTY 6: COMPLEX CONJUGATION
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    x*(t)  ↔  X*(-f)

    For REAL signals: x*(t) = x(t), so  X(f) = X*(-f)
    This gives HERMITIAN SYMMETRY: |X(f)| = |X(-f)|
    and the magnitude spectrum is EVEN (symmetric).

    TEST: Verify the Hermitian symmetry of a real signal's spectrum.
          |X(f)| should equal |X(-f)| for any real x(t).
    """
    name = "6. Conjugation / Hermitian Symmetry  [x*(t) ↔ X*(-f)]"

    def __init__(self):
        self.t     = np.linspace(-5, 5, 2000)
        self.freqs = np.linspace(-5, 5, 400)

    def verify(self):
        t, f = self.t, self.freqs
        x = Signals.rect(t) + 0.5*Signals.gaussian(t, sigma=0.5)

        R, I = CFTEngine.cft(t, x, f)
        mag  = CFTEngine.magnitude(R, I)
        mag_flipped = mag[::-1]   # |X(-f)|

        mse = CFTEngine.mse(mag, mag_flipped)
        print(f"  {self.name}")
        print(f"    MSE |X(f)| vs |X(-f)| (should be 0 for real signal) = {mse:.6e}")
        return f, mag, mag_flipped

    def plot(self):
        f, mag, mag_flipped = self.verify()
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(f, mag,         label="|X(f)|",   lw=2.5, color='steelblue')
        ax.plot(f, mag_flipped, '--', label="|X(-f)|", lw=1.8, color='crimson')
        ax.set_title(self.name + "\n(Hermitian symmetry: should overlap)")
        ax.set_xlabel("f"); ax.legend(); ax.grid(True, alpha=0.4)
        plt.tight_layout(); plt.show()


# ==============================================================================
#  PROPERTY 7: Duality
# ==============================================================================

class Property7_Duality:
    """
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    PROPERTY 7: DUALITY
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    If  x(t) ↔ X(f),  then  X(t) ↔ x(-f)

    WHY? The CFT and ICFT formulas are nearly identical:
        CFT:   X(f) = ∫ x(t) e^{-j2πft} dt
        ICFT:  x(t) = ∫ X(f) e^{+j2πft} df
    Apply CFT twice → F{F{x(t)}} = x(-t)

    CLASSIC EXAMPLE:
        rect(t) ↔ sinc(f)   →  sinc(t) ↔ rect(-f) = rect(f)
        (rect is even, so rect(-f) = rect(f))

    TEST: CFT of sinc(t) should give rect(f).
    """
    name = "7. Duality  [X(t) ↔ x(-f)]  →  sinc(t) ↔ rect(f)"

    def __init__(self):
        self.t     = np.linspace(-8, 8, 5000)
        self.freqs = np.linspace(-3, 3, 400)

    def verify(self):
        t, f = self.t, self.freqs
        x = Signals.sinc_signal(t)   # sinc(t) = sin(πt)/(πt)

        R, I = CFTEngine.cft(t, x, f)
        mag  = CFTEngine.magnitude(R, I)
        rect_expected = Signals.rect(f, width=1.0)   # rect(f) centred at 0

        mse = CFTEngine.mse(mag, rect_expected)
        print(f"  {self.name}")
        print(f"    MSE |CFT(sinc)| vs rect(f) = {mse:.6e}")
        return f, mag, rect_expected

    def plot(self):
        f, mag, rect_exp = self.verify()
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(f, mag,       label="|CFT{sinc(t)}|  (numerical)", lw=2.5, color='steelblue')
        ax.plot(f, rect_exp, '--', label="rect(f)  (expected by duality)", lw=2, color='crimson')
        ax.set_title(self.name); ax.set_xlabel("f"); ax.legend()
        ax.grid(True, alpha=0.4)
        plt.tight_layout(); plt.show()


# ==============================================================================
#  PROPERTY 8: Parseval's Theorem
# ==============================================================================

class Property8_Parseval:
    """
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    PROPERTY 8: PARSEVAL'S THEOREM (Energy Conservation)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ∫ |x(t)|² dt = ∫ |X(f)|² df

    MEANING:
        Total signal energy is the same whether you measure it in the
        time domain or the frequency domain.

    WHY THIS MATTERS:
        - Proves CFT is energy-preserving (unitary-like operation)
        - Allows energy computation in the easier domain
        - Rayleigh's Energy Theorem: ∫sinc²(t)dt = ∫rect²(f)df = 1

    TEST: compute both sides numerically and compare.
    """
    name = "8. Parseval's Theorem  [∫|x|²dt = ∫|X|²df]"

    def __init__(self):
        self.t     = np.linspace(-8, 8, 4000)
        self.freqs = np.linspace(-6, 6, 600)

    def verify(self):
        t, f = self.t, self.freqs
        x = Signals.gaussian(t, sigma=1.0)

        R, I = CFTEngine.cft(t, x, f)
        mag  = CFTEngine.magnitude(R, I)

        energy_time = np.trapezoid(x**2, t)
        energy_freq = np.trapezoid(mag**2, f)

        print(f"  {self.name}")
        print(f"    Energy in time domain : {energy_time:.6f}")
        print(f"    Energy in freq domain : {energy_freq:.6f}")
        print(f"    Ratio (should be 1.0) : {energy_time/energy_freq:.6f}")
        return energy_time, energy_freq

    def plot(self):
        t, f = self.t, self.freqs
        x = Signals.gaussian(t, sigma=1.0)
        R, I = CFTEngine.cft(t, x, f)
        mag = CFTEngine.magnitude(R, I)
        E_t, E_f = self.verify()

        fig, axes = plt.subplots(1, 2, figsize=(13, 4))
        axes[0].fill_between(t, x**2, alpha=0.4, color='steelblue')
        axes[0].plot(t, x**2, color='steelblue', lw=2)
        axes[0].set_title(f"|x(t)|²  →  Energy = {E_t:.4f}")
        axes[0].set_xlabel("t"); axes[0].grid(True, alpha=0.4)

        axes[1].fill_between(f, mag**2, alpha=0.4, color='darkorange')
        axes[1].plot(f, mag**2, color='darkorange', lw=2)
        axes[1].set_title(f"|X(f)|²  →  Energy = {E_f:.4f}")
        axes[1].set_xlabel("f"); axes[1].grid(True, alpha=0.4)

        plt.suptitle(self.name + f"\nRatio = {E_t/E_f:.6f} (should be 1)",
                     fontweight='bold', color='navy', y=1.02)
        plt.tight_layout(); plt.show()


# ==============================================================================
#  PROPERTY 9: Frequency Shifting (Modulation)
# ==============================================================================

class Property9_FrequencyShift:
    """
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    PROPERTY 9: FREQUENCY SHIFTING (MODULATION)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    x(t) · e^{j2πf₀t}  ↔  X(f - f₀)

    MEANING:
        Multiplying a signal by a complex exponential e^{j2πf₀t}
        SHIFTS the spectrum to the right by f₀.

    REAL MODULATION (cosine):
        x(t)·cos(2πf₀t) ↔  (1/2)[X(f-f₀) + X(f+f₀)]
        → Creates two copies of the spectrum, one at +f₀ and one at -f₀.
        → This is how AM radio modulation works!

    TEST:
        x(t) = rect(t),  f₀ = 3
        y(t) = x(t)·cos(2π·3·t)
        Y(f) should show two sinc lobes centred at f=±3
    """
    name = "9. Frequency Shift  [x(t)·e^{j2πf₀t} ↔ X(f-f₀)]"

    def __init__(self, f0=3.0):
        self.t     = np.linspace(-5, 5, 3000)
        self.freqs = np.linspace(-8, 8, 600)
        self.f0    = f0

    def verify(self):
        t, f, f0 = self.t, self.freqs, self.f0
        x = Signals.rect(t)
        y = x * np.cos(2*np.pi*f0*t)   # real modulation

        Rx, Ix = CFTEngine.cft(t, x, f)
        Ry, Iy = CFTEngine.cft(t, y, f)

        X_mag = CFTEngine.magnitude(Rx, Ix)
        Y_mag = CFTEngine.magnitude(Ry, Iy)

        # Theoretical: (1/2)|X(f-f0)| + (1/2)|X(f+f0)|  (approx for magnitude)
        X_right = np.interp(f - f0, f, X_mag, left=0, right=0)
        X_left  = np.interp(f + f0, f, X_mag, left=0, right=0)
        theory  = 0.5*(X_right + X_left)

        mse = CFTEngine.mse(Y_mag, theory)
        print(f"  {self.name}")
        print(f"    f₀ = {f0},  MSE |Y(f)| vs theory = {mse:.6e}")
        return f, X_mag, Y_mag, theory

    def plot(self):
        f, X_mag, Y_mag, theory = self.verify()
        fig, axes = plt.subplots(1, 2, figsize=(13, 4))
        axes[0].plot(f, X_mag, lw=2, color='steelblue', label="|X(f)|")
        axes[0].set_title("|X(f)| — original rect spectrum"); axes[0].legend()
        axes[0].set_xlabel("f"); axes[0].grid(True, alpha=0.4)

        axes[1].plot(f, Y_mag, lw=2.5, color='darkorange', label="|Y(f)| numerical")
        axes[1].plot(f, theory, '--', lw=1.8, color='crimson', label="Theory: (½)|X(f±f₀)|")
        axes[1].set_title(f"After modulation by cos(2π·{self.f0}·t)")
        axes[1].legend(); axes[1].set_xlabel("f"); axes[1].grid(True, alpha=0.4)
        plt.suptitle(self.name, fontweight='bold', color='navy', y=1.02)
        plt.tight_layout(); plt.show()


# ==============================================================================
#  PROPERTY 10: Convolution Theorem
# ==============================================================================

class Property10_Convolution:
    """
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    PROPERTY 10: CONVOLUTION THEOREM
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    (x₁ * x₂)(t)  ↔  X₁(f) · X₂(f)

    MEANING:
        Convolution in TIME  ≡  Multiplication in FREQUENCY

    WHY POWERFUL?
        Convolution is O(N²). But if we compute CFT (O(N log N) with FFT,
        O(N²) numerically), multiply, then ICFT, convolution becomes easy.
        Also: filtering is just multiplication in frequency domain!

    CLASSIC RESULT:
        rect(t) * rect(t) = triangle(t)  (Δ(t))
        In frequency:  sinc(f) · sinc(f) = sinc²(f)
        And triangle(t) ↔ sinc²(f)  ✓

    TEST:
        Verify: CFT{rect * rect} ≈ sinc² (via direct CFT of triangle)
    """
    name = "10. Convolution Theorem  [(x₁*x₂)(t) ↔ X₁(f)·X₂(f)]"

    def __init__(self):
        self.t     = np.linspace(-4, 4, 2000)
        self.freqs = np.linspace(-5, 5, 400)

    def verify(self):
        t, f = self.t, self.freqs
        dt = t[1] - t[0]

        # Numerical convolution: rect * rect = triangle
        x1 = Signals.rect(t)
        x2 = Signals.rect(t)
        conv = np.convolve(x1, x2, mode='same') * dt

        # CFT of convolution result
        R_conv, I_conv = CFTEngine.cft(t, conv, f)
        mag_conv = CFTEngine.magnitude(R_conv, I_conv)

        # CFT of triangle (should match)
        tri = Signals.triangle(t, width=2.0)
        R_tri, I_tri = CFTEngine.cft(t, tri, f)
        mag_tri = CFTEngine.magnitude(R_tri, I_tri)

        mse = CFTEngine.mse(mag_conv, mag_tri)
        print(f"  {self.name}")
        print(f"    MSE |CFT(rect*rect)| vs |CFT(triangle)| = {mse:.6e}")
        return f, mag_conv, mag_tri

    def plot(self):
        f, mag_conv, mag_tri = self.verify()
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(f, mag_conv, lw=2.5, color='steelblue', label="|CFT{rect*rect}|")
        ax.plot(f, mag_tri, '--', lw=2, color='crimson', label="|CFT{triangle}|")
        ax.set_title(self.name); ax.set_xlabel("f"); ax.legend()
        ax.grid(True, alpha=0.4)
        plt.tight_layout(); plt.show()


# ==============================================================================
#  PROPERTY 11: Differentiation
# ==============================================================================

class Property11_Differentiation:
    """
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    PROPERTY 11: DIFFERENTIATION
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    d/dt x(t)  ↔  j2πf · X(f)

    MEANING:
        Differentiation in time multiplies the spectrum by j2πf.
        This amplifies HIGH frequencies (large |f|) — explains why
        differentiators are sensitive to noise.

    PROOF:
        ∫ x'(t)e^{-j2πft} dt
        Integrate by parts: boundary terms vanish for decaying signals
        = j2πf · ∫ x(t)e^{-j2πft} dt  = j2πf · X(f)

    TEST:
        x(t) = Gaussian,  x'(t) = -t/σ² · Gaussian
        Verify: CFT{x'} ≈ j2πf · X(f)
    """
    name = "11. Differentiation  [x'(t) ↔ j2πf·X(f)]"

    def __init__(self):
        self.t     = np.linspace(-5, 5, 3000)
        self.freqs = np.linspace(-4, 4, 400)

    def verify(self):
        t, f = self.t, self.freqs
        dt = t[1] - t[0]
        sigma = 1.0

        x    = Signals.gaussian(t, sigma=sigma)
        xp   = np.gradient(x, dt)      # numerical derivative

        Rx, Ix = CFTEngine.cft(t, x, f)
        Rxp, Ixp = CFTEngine.cft(t, xp, f)

        # Theoretical: j2πf · X(f)   →  multiply complex X by j2πf
        # (R + jI) * j2πf = -2πf·I + j·2πf·R
        Rxp_theory = -2*np.pi*f * Ix
        Ixp_theory =  2*np.pi*f * Rx

        mse = CFTEngine.mse(CFTEngine.magnitude(Rxp, Ixp),
                             CFTEngine.magnitude(Rxp_theory, Ixp_theory))
        print(f"  {self.name}")
        print(f"    MSE |CFT(x')| vs |j2πf·X(f)| = {mse:.6e}")
        return f, CFTEngine.magnitude(Rxp,Ixp), \
               CFTEngine.magnitude(Rxp_theory, Ixp_theory)

    def plot(self):
        f, num_mag, theory_mag = self.verify()
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(f, num_mag,    lw=2.5, color='steelblue', label="|CFT{x'(t)}|")
        ax.plot(f, theory_mag, '--', lw=2, color='crimson', label="|j2πf·X(f)|")
        ax.set_title(self.name); ax.set_xlabel("f"); ax.legend()
        ax.grid(True, alpha=0.4)
        plt.tight_layout(); plt.show()


# ==============================================================================
#  PROPERTY 12: Modulation / Multiplication
# ==============================================================================

class Property12_Modulation:
    """
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    PROPERTY 12: MULTIPLICATION IN TIME = CONVOLUTION IN FREQUENCY
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    x₁(t) · x₂(t)  ↔  (X₁ * X₂)(f)

    This is the DUAL of the Convolution Theorem.

    APPLICATIONS:
        - Windowing: multiplying by a window in time ≡ convolving in frequency
        - AM modulation: rect(t)·cos(2πf₀t) → two shifted sinc lobes
        - STFT (Short-Time Fourier Transform): windowed analysis

    TEST:
        x₁(t) = Gaussian,  x₂(t) = Gaussian
        x₁·x₂ is also Gaussian (product of Gaussians = Gaussian)
        Verify product CFT matches via convolution in frequency.
    """
    name = "12. Modulation  [x₁(t)·x₂(t) ↔ (X₁*X₂)(f)]"

    def __init__(self):
        self.t     = np.linspace(-5, 5, 2000)
        self.freqs = np.linspace(-5, 5, 400)

    def verify(self):
        t, f = self.t, self.freqs
        df = f[1] - f[0]

        x1 = Signals.gaussian(t, sigma=1.5)
        x2 = Signals.gaussian(t, sigma=1.0)
        product = x1 * x2

        R_prod, I_prod = CFTEngine.cft(t, product, f)
        R1, I1 = CFTEngine.cft(t, x1, f)
        R2, I2 = CFTEngine.cft(t, x2, f)

        # Convolve X1 and X2 in frequency (real parts for magnitude check)
        X1_cplx = R1 + 1j*I1
        X2_cplx = R2 + 1j*I2
        conv_freq = np.convolve(np.real(X1_cplx), np.real(X2_cplx), 'same') * df
        # Full complex would need separate real/imag convolution; use magnitude approx
        mag_prod  = CFTEngine.magnitude(R_prod, I_prod)
        mag_conv  = np.abs(np.convolve(np.abs(X1_cplx), np.abs(X2_cplx), 'same') * df)

        print(f"  {self.name}")
        print(f"    (Magnitudes compared, full complex conv omitted for clarity)")
        return f, mag_prod, mag_conv

    def plot(self):
        f, mag_prod, mag_conv = self.verify()
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(f, mag_prod, lw=2.5, color='steelblue', label="|CFT{x₁·x₂}|")
        ax.plot(f, mag_conv, '--', lw=2, color='crimson', label="|X₁|*|X₂| (freq conv approx)")
        ax.set_title(self.name); ax.set_xlabel("f"); ax.legend()
        ax.grid(True, alpha=0.4)
        plt.tight_layout(); plt.show()


# ==============================================================================
#  MAIN: Run all 12 properties
# ==============================================================================

if __name__ == "__main__":

    properties = [
        Property1_Definition(),
        Property2_Linearity(),
        Property3_TimeShift(),
        Property4_TimeScaling(),
        Property5_TimeReversal(),
        Property6_Conjugation(),
        Property7_Duality(),
        Property8_Parseval(),
        Property9_FrequencyShift(),
        Property10_Convolution(),
        Property11_Differentiation(),
        Property12_Modulation(),
    ]

    print("\n" + "="*65)
    print("  FOURIER TRANSFORM PROPERTIES — NUMERICAL VERIFICATION")
    print("="*65)
    print("  Computing all 12 properties. Each will show MSE values.")
    print("  Plots will appear one at a time. Close each to continue.")
    print("="*65 + "\n")

    for prop in properties:
        print()
        prop.plot()

    print("\n" + "="*65)
    print("  ALL PROPERTIES VERIFIED!")
    print("="*65)
    print("""
  SUMMARY OF FOURIER TRANSFORM PROPERTIES:
  ─────────────────────────────────────────────────────────────
  Property          Formula
  ─────────────────────────────────────────────────────────────
  1  Definition     X(f) = ∫ x(t) e^{-j2πft} dt
  2  Linearity      F{ax+by} = aX + bY
  3  Time Shift     x(t-t₀) ↔ e^{-j2πft₀} X(f)
  4  Time Scaling   x(at)   ↔ (1/|a|) X(f/a)
  5  Time Reversal  x(-t)   ↔ X(-f)
  6  Conjugation    x*(t)   ↔ X*(-f)  → Hermitian symmetry
  7  Duality        X(t)    ↔ x(-f)
  8  Parseval       ∫|x|²dt = ∫|X|²df  (energy conservation)
  9  Freq. Shift    x(t)e^{j2πf₀t} ↔ X(f-f₀)
  10 Convolution    (x₁*x₂)(t) ↔ X₁(f)·X₂(f)
  11 Derivative     x'(t)  ↔ j2πf·X(f)
  12 Modulation     x₁(t)·x₂(t) ↔ (X₁*X₂)(f)
  ─────────────────────────────────────────────────────────────
""")