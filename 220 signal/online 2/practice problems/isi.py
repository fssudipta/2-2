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

def solve_isi_problem(INF=20):
    # Digital Input Signal: 1, 0, 1, 1
    # We leave space between bits to see the smear
    x = Signal(INF)
    bits = [1, 0, 1, 1]
    for i, b in enumerate(bits):
        x.set_value_at_time(i*2, b) # Bits sent at n=0, 2, 4, 6
    
    # Channel Response: Distorts and delays the signal
    h = Signal(INF)
    h.set_value_at_time(0, 1.0)
    h.set_value_at_time(1, 0.8)
    h.set_value_at_time(2, 0.3)
    
    channel = LTI_System(h)
    y = channel.output(x)
    
    x.plot("Clean Binary Bits")
    y.plot("Distorted Bits (ISI) reaching the Receiver")

# Observation: The output pulses overlap, making it hard to tell 
# where one bit ends and the next begins.

if __name__=="__main__":
    solve_isi_problem()