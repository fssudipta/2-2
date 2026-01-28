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

def solve_accumulator_problem(INF=20):
    # Input: Constant signal of 1 for n=0 to n=10
    x = Signal(INF)
    for i in range(0, 11):
        x.set_value_at_time(i, 1.0)
    
    # Impulse Response: Unit step h[n] = 1 for all n >= 0
    # (Represented here by a long finite sequence of 1s)
    h = Signal(INF)
    for i in range(0, 15):
        h.set_value_at_time(i, 1.0)
    
    system = LTI_System(h)
    y = system.output(x)
    
    x.plot("Input: Constant Value x(n)=1")
    y.plot("Output: Accumulated Sum (Linear Growth)")

# Logic: y[0]=1, y[1]=2, y[2]=3 ... y[10]=11.

if __name__ == "__main__":
    solve_accumulator_problem()