import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import warnings

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 1 — FORWARD LAPLACE TRANSFORM  (numerical)
#  X(s) = ∫ x(t) e^{-st} dt   (trapezoidal rule)
# ─────────────────────────────────────────────────────────────────────────────


def laplace_transform(x, t, s):
    """
    Numerically compute the one-sided Laplace transform of signal x(t)
    at a single complex frequency s.

        X(s) = ∫₀^∞  x(t) e^{-st} dt

    Parameters
    ----------
    x   : array_like  — sampled signal values
    t   : array_like  — time samples (uniform spacing assumed)
    s   : complex     — point in the s-plane at which to evaluate

    Returns
    -------
    complex  — X(s)
    """
    s = complex(s)
    dt = t[1] - t[0]
    integrand = x * np.exp(-s * t)
    # Trapezoidal rule: (dt/2)*(f[0]+f[-1]) + dt*sum(f[1:-1])
    return (dt / 2) * (integrand[0] + integrand[-1] + 2 * np.sum(integrand[1:-1]))


def laplace_transform_along_contour(x, t, s_list):
    """
    Evaluate X(s) at every point in s_list (vectorised wrapper).

    Returns
    -------
    np.ndarray of complex  — X(s) for each s in s_list
    """
    return np.array([laplace_transform(x, t, s) for s in s_list])


# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 2 — INVERSE LAPLACE TRANSFORM  (Bromwich / numerical)
#
#  x(t) = (1/2πj) ∫_{c-j∞}^{c+j∞}  X(s) e^{st} ds
#
#  Numerical approximation (Riemann sum over ω):
#  x(t) ≈ (Δω/2π) · Re{ Σ_k X(c + jω_k) e^{(c+jω_k)t} }
#
#  σ = c must lie INSIDE the ROC of X(s).
# ─────────────────────────────────────────────────────────────────────────────


def bromwich_contour(c=0.5, W=100.0, N=2000):
    """
    Build the discrete Bromwich contour: a vertical line Re{s} = c
    sampled at N equally-spaced points from c-jW to c+jW.

    Parameters
    ----------
    c  : float  — real part of the contour (must be inside the ROC)
    W  : float  — half-bandwidth in the imaginary direction
    N  : int    — number of sample points

    Returns
    -------
    np.ndarray of complex  — s_list
    """
    domega = 2 * W / N
    omega_k = -W + np.arange(N) * domega
    return c + 1j * omega_k


def inverse_laplace(X_s_vals, s_list, t):
    """
    Numerically invert X(s) → x(t) using the Bromwich integral.

        x(t) ≈ (Δω/2π) · e^{ct} · Re{ Σ_k X(c+jω_k) e^{jω_k·t} }

    Parameters
    ----------
    X_s_vals : array_like of complex  — X(s) evaluated at each s in s_list
    s_list   : array_like of complex  — Bromwich contour points
    t        : array_like of float    — time axis

    Returns
    -------
    np.ndarray of float  — reconstructed x(t)
    """
    s_arr = np.asarray(s_list, dtype=complex)
    X_arr = np.asarray(X_s_vals, dtype=complex)
    omega = np.imag(s_arr)
    domega = omega[1] - omega[0]
    c = np.real(s_arr[0])

    # Matrix: rows = ω_k, cols = t  →  exp(jω_k · t)
    exp_mat = np.exp(1j * np.outer(omega, t))
    complex_sum = np.dot(X_arr, exp_mat)  # shape: (len(t),)

    x_t = (domega / (2 * np.pi)) * np.real(complex_sum) * np.exp(c * t)
    return x_t


# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 3 — ANALYTICAL LAPLACE TRANSFORM PAIRS
#  (right-sided, causal signals)
# ─────────────────────────────────────────────────────────────────────────────


def lt_unit_impulse():
    """δ(t)  ←→  1,   ROC: entire s-plane"""
    return "1", "all s"


def lt_unit_step(s):
    """u(t)  ←→  1/s,   ROC: Re{s} > 0"""
    return 1.0 / s


def lt_right_exponential(s, a):
    """e^{-at}u(t)  ←→  1/(s+a),   ROC: Re{s} > -a"""
    return 1.0 / (s + a)


def lt_left_exponential(s, a):
    """-e^{-at}u(-t)  ←→  1/(s+a),   ROC: Re{s} < -a"""
    return 1.0 / (s + a)


def lt_ramp(s):
    """t·u(t)  ←→  1/s²,   ROC: Re{s} > 0"""
    return 1.0 / s**2


def lt_t_exp(s, a):
    """t·e^{-at}u(t)  ←→  1/(s+a)²,   ROC: Re{s} > -a"""
    return 1.0 / (s + a) ** 2


def lt_t_n_exp(s, a, n):
    """
    t^{n-1}/(n-1)! · e^{-at}u(t)  ←→  1/(s+a)^n,   ROC: Re{s} > -a
    (generalised, from s-domain differentiation property)
    """
    from math import factorial

    return 1.0 / (s + a) ** n  # coefficient 1/(n-1)! absorbed into signal def


def lt_cos(s, omega_0):
    """cos(ω₀t)u(t)  ←→  s/(s²+ω₀²),   ROC: Re{s} > 0"""
    return s / (s**2 + omega_0**2)


def lt_sin(s, omega_0):
    """sin(ω₀t)u(t)  ←→  ω₀/(s²+ω₀²),   ROC: Re{s} > 0"""
    return omega_0 / (s**2 + omega_0**2)


def lt_damped_cos(s, a, omega_0):
    """e^{-at}cos(ω₀t)u(t)  ←→  (s+a)/((s+a)²+ω₀²),   ROC: Re{s} > -a"""
    return (s + a) / ((s + a) ** 2 + omega_0**2)


def lt_damped_sin(s, a, omega_0):
    """e^{-at}sin(ω₀t)u(t)  ←→  ω₀/((s+a)²+ω₀²),   ROC: Re{s} > -a"""
    return omega_0 / ((s + a) ** 2 + omega_0**2)


def lt_two_sided_exp(s, b):
    """
    e^{-b|t|}  ←→  -2b/(s²-b²),   ROC: -b < Re{s} < b   (b > 0)
    Sum of right-sided e^{-bt}u(t) and left-sided e^{bt}u(-t).
    """
    return -2 * b / (s**2 - b**2)


# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 4 — ROC PROPERTIES  (from 6_-_Laplace.pdf)
# ─────────────────────────────────────────────────────────────────────────────


def roc_properties_summary():
    """
    Print a human-readable summary of all 8 ROC properties.
    """
    props = [
        (
            "Property 1",
            "Strips parallel to jω-axis",
            "Convergence depends only on Re{s}=σ, not Im{s}=ω, because |e^{-jωt}|=1.\n"
            "  → If (σ+jω) ∈ ROC, then ALL points on the vertical line Re{s}=σ are in the ROC.",
        ),
        (
            "Property 2",
            "ROC contains NO poles",
            "X(s) → ∞ at a pole, violating the finite-convergence requirement.\n"
            "  → The ROC is always an open region that excludes every pole.",
        ),
        (
            "Property 3",
            "Finite-duration & absolutely integrable  →  ROC = entire s-plane",
            "Over a finite interval the integral ∫|x(t)|e^{-σt}dt is bounded for every finite σ.\n"
            "  → ROC = ℂ  (watch out: apparent poles may cancel — use L'Hôpital).",
        ),
        (
            "Property 4",
            "Right-sided signals  →  ROC is a RIGHT half-plane",
            "If Re{s}=σ₀ is in the ROC and x(t)=0 for t<T₁, then all σ₁ > σ₀ also converge\n"
            "  because e^{-σ₁t} decays faster than e^{-σ₀t} as t→+∞.\n"
            "  → ROC: Re{s} > σ_min   (right of some vertical line).",
        ),
        (
            "Property 5",
            "Left-sided signals  →  ROC is a LEFT half-plane",
            "Analogous to Property 4 but for t→−∞.\n"
            "  → ROC: Re{s} < σ_max   (left of some vertical line).",
        ),
        (
            "Property 6",
            "Two-sided signals  →  ROC is a STRIP (if it exists)",
            "x(t) = x_L(t) + x_R(t).  ROC = ROC_L ∩ ROC_R = vertical strip σ_R < Re{s} < σ_L.\n"
            "  → If σ_R ≥ σ_L the Laplace transform does NOT exist.",
        ),
        (
            "Property 7",
            "Rational X(s): ROC is bounded by poles or extends to ∞",
            "Rational transforms are built from exponentials; each exponential's ROC is\n"
            "  bounded by its pole.  The intersection of such regions is again pole-bounded.\n"
            "  → No poles lie inside the ROC.",
        ),
        (
            "Property 8",
            "Rational X(s) + sidedness  →  precise ROC rule",
            "  • Right-sided x(t)  →  ROC to the RIGHT of the RIGHTMOST pole.\n"
            "  • Left-sided  x(t)  →  ROC to the LEFT  of the LEFTMOST  pole.",
        ),
    ]

    print("=" * 70)
    print("  ROC PROPERTIES — SUMMARY")
    print("=" * 70)
    for name, title, detail in props:
        print(f"\n  [{name}]  {title}")
        for line in detail.split("\n"):
            print(f"    {line}")
    print("\n" + "=" * 70)


def identify_roc(signal_type, poles_real_parts):
    """
    Given signal type and pole locations, return the ROC as a string.

    Parameters
    ----------
    signal_type      : str   — 'right', 'left', 'two_sided', or 'finite'
    poles_real_parts : list  — real parts of all poles

    Returns
    -------
    str  — human-readable ROC description
    """
    if signal_type == "finite":
        return "ROC: entire s-plane (finite-duration signal)"
    if not poles_real_parts:
        return "ROC: entire s-plane (no poles)"

    rightmost = max(poles_real_parts)
    leftmost = min(poles_real_parts)

    if signal_type == "right":
        return f"ROC: Re{{s}} > {rightmost}  (right of rightmost pole)"
    elif signal_type == "left":
        return f"ROC: Re{{s}} < {leftmost}  (left of leftmost pole)"
    elif signal_type == "two_sided":
        if leftmost >= rightmost:
            return "ROC: does NOT exist (strip is empty)"
        return f"ROC: {leftmost} < Re{{s}} < {rightmost}  (strip between poles)"
    else:
        return "Unknown signal type"


# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 5 — LT PROPERTIES  (from 7_-_More_Laplace.pdf)
# ─────────────────────────────────────────────────────────────────────────────


# 5.1  Linearity
def lt_linearity(X1_s, X2_s, a=1.0, b=1.0):
    """
    ax₁(t) + bx₂(t)  ←→  a·X₁(s) + b·X₂(s)
    ROC contains at least R₁ ∩ R₂  (may be larger if poles cancel).
    """
    return a * X1_s + b * X2_s


# 5.2  Time Shifting
def lt_time_shift(X_s, s, t0):
    """
    x(t − t₀)  ←→  e^{-s·t₀} · X(s)      ROC unchanged
    Delay multiplies the transform by an exponential factor.
    """
    return np.exp(-s * t0) * X_s


# 5.3  s-Domain Shifting (frequency shift)
def lt_s_shift(X_s_fn, s, s0):
    """
    e^{s₀t} x(t)  ←→  X(s − s₀)          ROC shifts right by Re{s₀}
    Multiplication by a complex exponential shifts the s-domain argument.
    """
    return X_s_fn(s - s0)


# 5.4  Time Scaling
def lt_time_scale(X_s_fn, s, a):
    """
    x(at)  ←→  (1/|a|) · X(s/a)           ROC scales by factor a
    Compression in time → expansion in s-domain (and vice versa).
    """
    assert a != 0, "Scaling factor a must be non-zero."
    return (1.0 / abs(a)) * X_s_fn(s / a)


# 5.5  Time Reversal
def lt_time_reversal(X_s_fn, s):
    """
    x(−t)  ←→  X(−s)                      ROC = −R  (mirrored)
    Special case of time scaling with a = −1.
    """
    return X_s_fn(-s)


# 5.6  Conjugation
def lt_conjugation(X_s, s):
    """
    x*(t)  ←→  X*(s*)                     ROC unchanged
    For real x(t): X*(s*) = X(s) → poles/zeros come in conjugate pairs.
    """
    return np.conj(X_s)  # caller must evaluate at conj(s) if needed


# 5.7  Convolution
def lt_convolution(X1_s, X2_s):
    """
    x₁(t) * x₂(t)  ←→  X₁(s) · X₂(s)    ROC ⊇ R₁ ∩ R₂
    Convolution in time ↔ multiplication in s-domain.
    """
    return X1_s * X2_s


# 5.8  Time Differentiation
def lt_time_diff(X_s, s):
    """
    d/dt x(t)  ←→  s · X(s)              ROC contains R (may expand if pole at s=0 cancels)
    Every derivative introduces a factor of s — turns ODEs into algebra.
    """
    return s * X_s


# 5.9  s-Domain Differentiation
def lt_s_diff_numerical(X_s_fn, s, ds=1e-7):
    """
    −t·x(t)  ←→  dX(s)/ds               ROC unchanged
    Differentiation w.r.t. s ↔ multiplication by −t in time.
    Uses central finite difference for numerical approximation.
    """
    return (X_s_fn(s + ds) - X_s_fn(s - ds)) / (2 * ds)


# 5.10  Time Integration
def lt_time_integration(X_s, s):
    """
    ∫_{−∞}^{t} x(τ)dτ  ←→  (1/s) · X(s)    ROC ⊇ R ∩ {Re{s}>0}
    Integration introduces a factor of 1/s (a pole at s=0 unless cancelled).
    """
    assert s != 0, "Division by zero: s=0 is not in the ROC of the integral."
    return X_s / s


def lt_properties_summary():
    """Print a compact summary table of all LT properties."""
    rows = [
        ("Linearity", "ax₁(t)+bx₂(t)", "aX₁(s)+bX₂(s)", "⊇ R₁∩R₂"),
        ("Time shifting", "x(t-t₀)", "e^{−st₀}·X(s)", "Same R"),
        ("s-Domain shifting", "e^{s₀t}·x(t)", "X(s−s₀)", "R + Re{s₀}"),
        ("Time scaling", "x(at)", "(1/|a|)·X(s/a)", "scaled aR"),
        ("Time reversal", "x(-t)", "X(−s)", "−R"),
        ("Conjugation", "x*(t)", "X*(s*)", "Same R"),
        ("Convolution", "x₁(t)*x₂(t)", "X₁(s)·X₂(s)", "⊇ R₁∩R₂"),
        ("Time differentiation", "d/dt x(t)", "s·X(s)", "⊇ R"),
        ("s-Differentiation", "-t·x(t)", "dX(s)/ds", "Same R"),
        ("Time integration", "∫x(τ)dτ", "(1/s)·X(s)", "⊇ R∩{Re{s}>0}"),
    ]
    print("\n" + "=" * 80)
    print(f"  {'Property':<24} {'Time Domain':<22} {'s-Domain':<24} {'ROC'}")
    print("  " + "-" * 76)
    for row in rows:
        print(f"  {row[0]:<24} {row[1]:<22} {row[2]:<24} {row[3]}")
    print("=" * 80 + "\n")


# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 6 — PARTIAL FRACTION EXPANSION  (inverse via residues)
# ─────────────────────────────────────────────────────────────────────────────


def partial_fraction_residues(num_coeffs, den_coeffs):
    """
    Compute residues, poles, and direct terms WITHOUT Scipy.
    Formula for distinct poles: Residue(p) = N(p) / D'(p)
    """
    # 1. Find Poles (Roots of denominator)
    poles = np.roots(den_coeffs)

    # 2. Derivative of denominator for residue calculation
    den_der = np.polyder(den_coeffs)

    # 3. Calculate Residues: R_i = N(p_i) / D'(p_i)
    residues = []
    for p in poles:
        r = np.polyval(num_coeffs, p) / np.polyval(den_der, p)
        residues.append(r)

    # 4. Calculate Direct Term (k) using polynomial division
    # k is non-empty only if degree(num) >= degree(den)
    k, _ = np.polydiv(num_coeffs, den_coeffs)

    return np.array(residues), poles, k


def invert_partial_fraction(residues, poles, t, roc_type="right"):
    """
    Given residues {Aᵢ} and poles {pᵢ}, reconstruct x(t) from:

        X(s) = Σ Aᵢ / (s − pᵢ)

    Each term inverts as:
        • ROC to RIGHT of pole  →  +Aᵢ · e^{pᵢt} · u(t)
        • ROC to LEFT  of pole  →  −Aᵢ · e^{pᵢt} · u(−t)

    Parameters
    ----------
    residues  : array_like of complex
    poles     : array_like of complex
    t         : array_like of float
    roc_type  : 'right' | 'left' | list of 'right'/'left' per pole

    Returns
    -------
    np.ndarray of float  — x(t)
    """
    x = np.zeros(len(t), dtype=complex)
    for i, (A, p) in enumerate(zip(residues, poles)):
        side = roc_type if isinstance(roc_type, str) else roc_type[i]
        if side == "right":
            x += A * np.exp(p * t) * (t >= 0)
        else:
            x -= A * np.exp(p * t) * (t <= 0)
    return np.real(x)


# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 7 — LTI SYSTEM ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────


def system_function_from_ode(a_coeffs, b_coeffs):
    """
    Derive the system function H(s) = Y(s)/X(s) from an LCCDE:

        Σ aₖ · d^k y/dt^k  =  Σ bₖ · d^k x/dt^k

    Under zero initial conditions: differentiation → multiply by s.

    Parameters
    ----------
    a_coeffs : list  — [a₀, a₁, ..., aₙ]  (output/y side, index = derivative order)
    b_coeffs : list  — [b₀, b₁, ..., bₘ]  (input/x side)

    Returns
    -------
    Function H(s) evaluating the rational system function at any complex s.

    Example
    -------
    dy/dt + 3y = x  →  a_coeffs=[3,1], b_coeffs=[1]
    H(s) = 1 / (s + 3)
    """

    def H(s):
        s = complex(s)
        num = sum(b * s**k for k, b in enumerate(b_coeffs))
        den = sum(a * s**k for k, a in enumerate(a_coeffs))
        return num / den

    return H


def check_causality(poles):
    """
    A causal system has ROC to the RIGHT of the rightmost pole.
    Returns True and a description string.
    """
    rightmost = max(np.real(poles))
    roc_str = f"Re{{s}} > {rightmost:.4f}"
    return True, roc_str  # by assumption of causality


def check_stability_causal(poles):
    """
    A causal LTI system is BIBO-stable iff ALL poles lie in the LEFT half-plane
    (Re{pᵢ} < 0), which ensures the jω-axis is inside the ROC.

    Returns
    -------
    stable : bool
    details : str
    """
    real_parts = np.real(poles)
    stable = bool(np.all(real_parts < 0))
    worst = max(real_parts)
    if stable:
        details = f"All poles in LHP (rightmost at Re={{s}}={worst:.4f}). STABLE."
    else:
        details = f"Pole(s) in RHP or on jω-axis (rightmost at Re={{s}}={worst:.4f}). UNSTABLE."
    return stable, details


def lti_zero_state_response(H_fn, x, t, s_list):
    """
    Compute the zero-state output y(t) = h(t)*x(t) via Laplace:
        Y(s) = H(s) · X(s)   →   y(t) = L⁻¹{Y(s)}

    Parameters
    ----------
    H_fn   : callable  — system function H(s)
    x      : array_like — input signal
    t      : array_like — time axis
    s_list : array_like — Bromwich contour

    Returns
    -------
    np.ndarray  — y(t)
    """
    X_s = laplace_transform_along_contour(x, t, s_list)
    Y_s = np.array([H_fn(s) * X_s_val for s, X_s_val in zip(s_list, X_s)])
    return inverse_laplace(Y_s, s_list, t)


# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 8 — ERROR METRICS  (for system performance evaluation)
# ─────────────────────────────────────────────────────────────────────────────


def steady_state_value(h, fraction=0.05):
    """Mean of the last `fraction` of the signal — estimates h_ss."""
    n = max(1, int(fraction * len(h)))
    return float(np.mean(h[-n:]))


def ise(h, t):
    """
    Integral of Squared Error:  ISE = ∫ (h_ss − h(t))² dt
    Penalises persistent deviations from the steady-state value.
    Lower ISE → output tracks h_ss more accurately over time.
    """
    h_ss = steady_state_value(h)
    integrand = (h_ss - h) ** 2
    return float(np.trapz(integrand, t))


def iae(h, t):
    """
    Integral of Absolute Error:  IAE = ∫ |h_ss − h(t)| dt
    Less sensitive to large outliers than ISE.
    """
    h_ss = steady_state_value(h)
    integrand = np.abs(h_ss - h)
    return float(np.trapz(integrand, t))


def itae(h, t):
    """
    Integral of Time-weighted Absolute Error:  ITAE = ∫ t·|h_ss − h(t)| dt
    Heavily penalises errors that persist late in time.
    """
    h_ss = steady_state_value(h)
    integrand = t * np.abs(h_ss - h)
    return float(np.trapz(integrand, t))


def response_energy(h, t):
    """
    Response Energy:  E = ∫ h(t)² dt
    Total energy contained in the output signal.
    """
    return float(np.trapz(h**2, t))


def input_energy(u, t):
    """
    Input Energy:  E_u = ∫ u(t)² dt
    Total energy injected by the input signal.
    """
    return float(np.trapz(u**2, t))


def time_constant_metric(h, t):
    """Time for h(t) to first reach 63.2 % of its steady-state value."""
    h_ss = steady_state_value(h)
    if h_ss <= 0:
        return float("nan")
    idx = np.where(h >= 0.632 * h_ss)[0]
    return float(t[idx[0]]) if len(idx) > 0 else float("nan")


def rise_time_metric(h, t):
    """Time for h(t) to travel from 10 % to 90 % of h_ss."""
    h_ss = steady_state_value(h)
    if h_ss <= 0:
        return float("nan")
    return np.interp(0.9 * h_ss, h, t) - np.interp(0.1 * h_ss, h, t)


def settling_time_metric(h, t, band=0.02):
    """Last time h(t) exits the ±`band`·h_ss corridor (2 % by default)."""
    h_ss = steady_state_value(h)
    if h_ss <= 0:
        return float("nan")
    out = np.where(np.abs(h - h_ss) > band * abs(h_ss))[0]
    if len(out) == 0:
        return 0.0
    idx = out[-1]
    return float(t[idx + 1]) if idx + 1 < len(t) else float(t[-1])


def overshoot_metric(h):
    """Percentage overshoot: (h_max − h_ss) / h_ss × 100."""
    h_ss = steady_state_value(h)
    h_max = float(np.max(h))
    if h_ss <= 0 or h_max <= h_ss:
        return 0.0
    return float((h_max - h_ss) / h_ss * 100)


def compute_all_metrics(h, t):
    """Compute and return a dict of all performance metrics."""
    return {
        "steady_state": steady_state_value(h),
        "time_constant": time_constant_metric(h, t),
        "rise_time": rise_time_metric(h, t),
        "settling_time": settling_time_metric(h, t),
        "overshoot_%": overshoot_metric(h),
        "ISE": ise(h, t),
        "IAE": iae(h, t),
        "ITAE": itae(h, t),
        "response_energy": response_energy(h, t),
    }


# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 9 — VISUALISATION HELPERS
# ─────────────────────────────────────────────────────────────────────────────


def plot_pole_zero(
    poles, zeros, title="Pole-Zero Plot", roc_right=None, roc_strip=None
):
    """
    Draw a pole-zero plot in the s-plane.

    Parameters
    ----------
    poles      : array_like of complex — pole locations (drawn as ×)
    zeros      : array_like of complex — zero locations (drawn as ○)
    title      : str
    roc_right  : float or None  — if given, shade Re{s} > roc_right
    roc_strip  : (float,float)  — if given, shade the strip between the two values
    """
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.axhline(0, color="k", lw=0.8)
    ax.axvline(0, color="k", lw=0.8, label="jω-axis (Fourier)")

    # shade ROC
    xlim = (-4, 4)
    ylim = (-4, 4)
    if roc_right is not None:
        ax.axvspan(
            roc_right,
            xlim[1],
            alpha=0.12,
            color="green",
            label=f"ROC: Re{{s}} > {roc_right}",
        )
    if roc_strip is not None:
        ax.axvspan(
            roc_strip[0],
            roc_strip[1],
            alpha=0.12,
            color="green",
            label=f"ROC: {roc_strip[0]} < Re{{s}} < {roc_strip[1]}",
        )

    for p in np.atleast_1d(poles):
        ax.plot(np.real(p), np.imag(p), "rx", ms=12, mew=2)
    for z in np.atleast_1d(zeros):
        ax.plot(np.real(z), np.imag(z), "bo", ms=9, mew=2, fillstyle="none")

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_xlabel("Re{s}")
    ax.set_ylabel("Im{s}")
    ax.set_title(title, fontweight="bold")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_signal_pair(t, u, h, title, label_u="Input u(t)", label_h="Output h(t)"):
    """Simple two-signal overlay plot."""
    plt.figure(figsize=(8, 4))
    plt.plot(t, u, "b--", lw=1.8, label=label_u)
    plt.plot(t, h, "r-", lw=2.2, label=label_h)
    plt.title(title, fontweight="bold")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 10 — DEMO / SELF-TEST
# ─────────────────────────────────────────────────────────────────────────────


def demo():
    """
    End-to-end demonstration covering:
      1. Analytical LT pair verification
      2. ROC identification
      3. LT properties table
      4. Numerical forward + inverse LT round-trip
      5. LTI system H(s) = b/(s+a), step input
      6. Stability & causality check
      7. All error metrics
      8. Pole-zero plot
    """
    print("\n" + "█" * 70)
    print("  LAPLACE TRANSFORM TEMPLATE — DEMO")
    print("█" * 70)

    t = np.arange(0, 20 + 0.01, 0.01)
    dt = t[1] - t[0]

    # ── 1. Analytical pair: e^{-at}u(t) ←→ 1/(s+a) ──────────────────────
    print("\n[1] Analytical pair: e^{-2t}u(t)  ←→  1/(s+2),  ROC: Re{s} > -2")
    a = 2.0
    x_t = np.exp(-a * t)  # right-sided (u(t)=1 for t≥0)
    s_pt = 1.0 + 0j  # test point inside ROC
    X_num = laplace_transform(x_t, t, s_pt)
    X_ana = lt_right_exponential(s_pt, a)
    print(f"   Numerical X({s_pt}) = {X_num:.6f}")
    print(f"   Analytical X({s_pt}) = {X_ana:.6f}")
    print(f"   Error = {abs(X_num - X_ana):.2e}")

    # ── 2. ROC identification ─────────────────────────────────────────────
    print("\n[2] ROC identification examples:")
    print("   " + identify_roc("right", [-1, -2]))
    print("   " + identify_roc("left", [-1, -2]))
    print("   " + identify_roc("two_sided", [-2, 2]))  # strip: -2 < Re{s} < 2
    print("   " + identify_roc("finite", []))

    # ── 3. Properties table ───────────────────────────────────────────────
    print("\n[3] LT Properties Table:")
    lt_properties_summary()

    # ── 4. ROC properties ─────────────────────────────────────────────────
    print("[4] ROC Properties Summary:")
    roc_properties_summary()

    # ── 5. Numerical round-trip: forward then inverse LT ─────────────────
    print("[5] Round-trip test: x(t)=e^{-0.5t}  →  X(s)  →  x̂(t)")
    x_orig = np.exp(-0.5 * t)
    s_list = bromwich_contour(c=0.5, W=80.0, N=2000)
    X_s = laplace_transform_along_contour(x_orig, t, s_list)
    x_recon = inverse_laplace(X_s, s_list, t)
    err = np.mean(np.abs(x_orig - x_recon))
    print(f"   Mean absolute reconstruction error: {err:.4e}")

    # ── 6. LTI system: H(s)=1/(s+0.5), step input ────────────────────────
    print("\n[6] LTI system  H(s)=1/(s+0.5), step input u(t)=1")
    a_sys = 0.5
    b_sys = 1.0
    H = system_function_from_ode(a_coeffs=[a_sys, 1.0], b_coeffs=[b_sys])
    u_in = np.ones_like(t)
    y_out = lti_zero_state_response(H, u_in, t, s_list)
    y_ss = steady_state_value(y_out)
    print(f"   Analytical steady-state = {b_sys/a_sys:.4f}")
    print(f"   Numerical  steady-state = {y_ss:.4f}")

    # ── 7. Stability & causality ──────────────────────────────────────────
    print("\n[7] Stability check:")
    poles_stable = np.array([-0.5])
    poles_unstable = np.array([+2.0])
    _, s1 = check_stability_causal(poles_stable)
    _, s2 = check_stability_causal(poles_unstable)
    print(f"   poles={poles_stable}: {s1}")
    print(f"   poles={poles_unstable}: {s2}")

    # ── 8. Error metrics ──────────────────────────────────────────────────
    print("\n[8] Performance metrics for the step response:")
    metrics = compute_all_metrics(y_out, t)
    for k, v in metrics.items():
        print(f"   {k.replace('_',' ').title():<22}: {v:.4f}")

    # ── 9. Pole-zero plot ─────────────────────────────────────────────────
    print("\n[9] Pole-zero plot: H(s) = (s-1)/((s+1)(s+2))")
    plot_pole_zero(
        poles=[-1 + 0j, -2 + 0j],
        zeros=[1 + 0j],
        title="Pole-Zero: H(s)=(s-1)/((s+1)(s+2))",
        roc_right=-1,
    )

    print("\n" + "█" * 70)
    print("  DEMO COMPLETE")
    print("█" * 70 + "\n")


# ─────────────────────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    demo()
