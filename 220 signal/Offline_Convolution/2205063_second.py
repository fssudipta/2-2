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

if __name__ == "__main__":
    filename = "input_signal.txt"

    with open(filename, "r") as f:
        n_start, n_end = map(int, f.readline().split())
        data = list(map(float, f.readline().split()))
    
    INF = max(abs(n_start), abs(n_end))+10
    x = Signal(INF)

    for i, val in enumerate(data):
        x.set_value_at_time(n_start+i, val)
    
    x.plot("Noisy Input Signal x(n)")
    h = Signal(INF)
    for n in range(-2, 3):
        h.set_value_at_time(n, 1/5)
    
    h.plot("Impulse Response h(n)---5 points moving average filter")
    system = LTI_System(h)
    y = system.output(x)
    y.plot("Smoothed Output Signal y(n)")