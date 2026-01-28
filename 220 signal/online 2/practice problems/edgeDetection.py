import numpy as np
import matplotlib.pyplot as plt

class Signal:
    def __init__(self, INF):
        self.INF=INF
        self.n=np.arange(-INF, INF+1)
        self.values=np.zeros(len(self.n))

    def _index(self, t):
        return t+self.INF
    
    def set_value_at_time(self, t, value):
        if -self.INF<=t<=self.INF:
            self.values[self._index(t)]=value
    
    def shift(self, k):
        shifted = Signal(self.INF)
        for t in self.n:
            if -self.INF<=t-k<=self.INF:
                shifted.set_value_at_time(t, self.values[self._index(t-k)])
        return shifted
    
    def add(self, other):
        result = Signal(self.INF)
        result.values=self.values+other.values
        return result
    
    def multiply(self, scalar):
        result = Signal(self.INF)
        result.values=scalar*self.values
        return result
    
    def plot(self, title="Discrete Signal"):
        plt.figure()
        plt.stem(self.n, self.values)
        plt.title(title)
        plt.xlabel("n")
        plt.ylabel("amplitude")
        plt.grid(True)
        plt.xticks(np.arange(self.n[0], self.n[-1] + 1, 2))
        plt.show()


class LTI_System:
    def __init__(self, impulse_response: Signal):
        self.h=impulse_response
        self.INF=impulse_response.INF
        
    def linear_combination_of_impulses(self, input_signal:Signal):
        impulses = []
        coefficients = []

        for k in input_signal.n:
            val = input_signal.values[input_signal._index(k)]
            if val != 0:
                delta = Signal(self.INF)
                delta.set_value_at_time(0,1)
                delta_k = delta.shift(k)
                impulses.append(delta_k)
                coefficients.append(val)

        return impulses, coefficients
    
    def output(self, input_signal:Signal):
        impulses, coefficients = self.linear_combination_of_impulses(input_signal)
        y = Signal(self.INF)
        for delta_k, coeff in zip(impulses, coefficients):
            shifted_h = self.h.shift(delta_k.n[np.argmax(delta_k.values)])
            y=y.add(shifted_h.multiply(coeff))

        return y

# PROBLEM: Edge Detection / First Difference
# A system that detects changes in a signal.

def solve_edge_detection():
    INF = 10
    # Difference Impulse Response: h[n] = [1, -1]
    h = Signal(INF)
    h.set_value_at_time(0, 1)
    h.set_value_at_time(1, -1)
    
    # Step input: 0, 0, 0, 5, 5, 5, 5...
    x = Signal(INF)
    for t in range(2, INF + 1):
        x.set_value_at_time(t, 5)
        
    diff_system = LTI_System(h)
    y = diff_system.output(x)
    
    print("Edge Detection Output:")
    for t in range(0, 6):
        val = y.get_value_at_time(t)
        print(f"y[{t}] = {val:>4}  {'<-- Edge Found!' if val != 0 else ''}")

# Expected: y[2] = 5, all other y[n] = 0. 
# The system "ignored" the constant values and only reacted to the jump at n=2.

if __name__=="__main__":
    solve_edge_detection()