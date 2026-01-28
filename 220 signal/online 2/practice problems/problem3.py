import numpy as np

"""
PROBLEM STATEMENT: Signal Decomposition & Superposition Verification

Scenario:
Any discrete-time signal x[n] can be mathematically decomposed into a weighted 
sum of shifted unit impulses (delta functions). 
For example: if x[n] = [5, -2] (at n=0 and n=1), 
it is the same as x[n] = 5*delta[n] + (-2)*delta[n-1].

Task:
1. Implement Signal, SuperSignal, and LTI_System classes.
2. Create an input signal x[n] and an impulse response h[n].
3. Write a function 'decompose_to_supersignal' that takes a standard Signal 
   and breaks it into individual impulses stored in a SuperSignal object.
4. Calculate the output using TWO methods:
   a) Standard Convolution: y = x[n] * h[n]
   b) Superposition: y = sum( x[k] * (delta[n-k] * h[n]) )
5. Verify that both methods produce identical results.
"""

class Signal:
    def __init__(self, INF):
        self.INF = INF
        # Store values in a range from -INF to INF
        self.values = np.zeros(2 * INF + 1)

    def set_value_at_time(self, time, value):
        if -self.INF <= time <= self.INF:
            self.values[time + self.INF] = value

    def get_value_at_time(self, time):
        if -self.INF <= time <= self.INF:
            return self.values[time + self.INF]
        return 0

class SuperSignal:
    def __init__(self):
        # Stores tuples of (coefficient, Signal_object)
        self.components = []

    def add(self, signal: Signal, coefficient=1.0):
        self.components.append((coefficient, signal))

class LTI_System:
    def __init__(self, h: Signal):
        self.h = h

    def output(self, x: Signal):
        """Method A: Standard Discrete Convolution"""
        inf = x.INF
        result = Signal(inf)
        for n in range(-inf, inf + 1):
            sum_val = 0
            for k in range(-inf, inf + 1):
                sum_val += x.get_value_at_time(k) * self.h.get_value_at_time(n - k)
            result.set_value_at_time(n, sum_val)
        return result

    def output_super(self, super_signal: SuperSignal):
        """Method B: Superposition (Convolution of components)"""
        # Create an empty signal to accumulate results
        # We assume all component signals share the same INF
        sample_sig = super_signal.components[0][1]
        final_output = Signal(sample_sig.INF)
        
        for coeff, x_i in super_signal.components:
            # Convolve this specific component impulse with h
            y_i = self.output(x_i)
            
            # Weighted sum: Accumulate (coeff * y_i) into final_output
            for n in range(-final_output.INF, final_output.INF + 1):
                current_total = final_output.get_value_at_time(n)
                increment = coeff * y_i.get_value_at_time(n)
                final_output.set_value_at_time(n, current_total + increment)
        
        return final_output

def decompose_to_supersignal(sig: Signal):
    """
    Takes a Signal x[n] and breaks it into individual 
    weighted delta functions delta[n-k].
    """
    super_sig = SuperSignal()
    inf = sig.INF
    
    for t in range(-inf, inf + 1):
        val = sig.get_value_at_time(t)
        if val != 0:
            # Create a simple unit impulse delta[n - t]
            delta_k = Signal(inf)
            delta_k.set_value_at_time(t, 1.0)
            # Add it to the SuperSignal with the signal's value as the weight
            super_sig.add(delta_k, val)
            
    return super_sig

# --- EXECUTION ---
if __name__ == "__main__":
    INF_VAL = 5

    # 1. Define input signal x[n] = 3 at n=0, -1 at n=1
    # x[n] = 3*delta[n] - 1*delta[n-1]
    x = Signal(INF_VAL)
    x.set_value_at_time(0, 3)
    x.set_value_at_time(1, -1)

    # 2. Define impulse response h[n] = 1 at n=0, 2 at n=1, 1 at n=2
    h_sig = Signal(INF_VAL)
    h_sig.set_value_at_time(0, 1)
    h_sig.set_value_at_time(1, 2)
    h_sig.set_value_at_time(2, 1)

    system = LTI_System(h_sig)

    # --- Method A: Standard Convolution ---
    y_standard = system.output(x)

    # --- Method B: Superposition through Decomposition ---
    # Break x[n] into [ (3, delta[n]), (-1, delta[n-1]) ]
    super_x = decompose_to_supersignal(x)
    y_super = system.output_super(super_x)

    # 3. Compare Results
    print(f"{'Time n':<8} | {'Standard y[n]':<15} | {'Superposition y[n]':<15}")
    print("-" * 45)
    for n in range(-1, 5):
        val_a = y_standard.get_value_at_time(n)
        val_b = y_super.get_value_at_time(n)
        print(f"{n:<8} | {val_a:<15.2f} | {val_b:<15.2f}")

    # Verification check
    match = True
    for n in range(-INF_VAL, INF_VAL + 1):
        if not np.isclose(y_standard.get_value_at_time(n), y_super.get_value_at_time(n)):
            match = False
            break
    
    print("\nResults Match:", match)