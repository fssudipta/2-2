import numpy as np
import matplotlib.pyplot as plt

class CFTEngine:
    def cft(t, x_val, f):
        R= np.zeros(len(f))
        I=np.zeros(len(f))
        for k, f in enumerate(f):
            R[k]=np.trapezoid(x_val*np.cos(2*np.pi*f*t), t)
            I[k]=-np.trapezoid(x_val*np.sin(2*np.pi*f*t), t)
        return R, I

    def mag(r,i):
        return np.sqrt(r**2+i**2)
    def phase(r,i):
        return np.arctan2(i,r)
    def mse(a,b):
        return np.mean((a-b)**2) 
    
class Signal:
    def rect(t, width=1.0):
        return ((np.abs(t)<=width/2).astype(float))
    def sinc_sig(t):
        return np.sinc(t)
    def gaussian(t, sigma=1.0):
        return np.exp(-t**2/(2*sigma**2))
    def triangle(t, width=2.0):
        return np.maximum(0, 1-np.abs(t)/(width/2))
    def squarewave(t, freq=1.0, amp=1.0):
        return amp*np.sign(np.sin(2*np.pi*freq*t))
    def cosine(t,f0=2.0,amp=1.0):
        return amp*np.cos(2*np.pi*f0*t)
    def sine(t,f0=2.0,amp=1.0):
        return amp*np.sin(2*np.pi*f0*t)
    def exp_decay(t,a=1.0):
        return np.where(t>=0,np.exp(-a*t),0.0)

class Property1_def:
    name="1.CFT Definition[rect(t) to sinc(f)]"
    def __init__(self):
        self.t=np.linspace(-5,5,3000)
        self.f=np.linspace(-5,5,500)
    def verify(self):
        x=Signal.rect(self.t, width=1.0)
        r,i=CFTEngine.cft(self.t,x,self.f)
        comp_mag=CFTEngine.mag(r,i)
        ana_mag=np.abs(np.sinc(self.f))
        mse=CFTEngine.mse(comp_mag,ana_mag)
        print(f"MSE(computed vs analytic sinc)={mse:.6e}")
        return self.t, self.f, x, comp_mag,ana_mag
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

class Property2_linearity:
    name="2.Linearity"
    def __init__(self):
        self.t     = np.linspace(-5, 5, 2000)
        self.freqs = np.linspace(-5, 5, 400)
        self.a, self.b = 2.0, 3.0
    def verify(self):
        t,f,a,b=self.t, self.f, self.a, self.b
        x1=Signal.rect(t)
        x2=Signal.gaussian(t)
        combo=a*x1+b*x2
        rlhs,ilhs=CFTEngine.cft(t,combo,f)
        R1, I1 = CFTEngine.cft(t, x1, f)
        R2, I2 = CFTEngine.cft(t, x2, f)
        R_rhs = a*R1 + b*R2
        I_rhs = a*I1 + b*I2
        mser=CFTEngine.mse(rlhs, R_rhs)
        msei=CFTEngine.mse(ilhs,I_rhs)
        print(f"  {self.name}")
        print(f"    MSE Real = {mser:.6e},  MSE Imag = {msei:.6e}")
        return f, CFTEngine.mag(rlhs,ilhs), CFTEngine.magnitude(R_rhs,I_rhs)
    def plot(self):
        f, lhs_mag, rhs_mag = self.verify()
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(f, lhs_mag, label="|F{2x₁+3x₂}|", lw=2.5, color='steelblue')
        ax.plot(f, rhs_mag, '--', label="2|X₁|+3|X₂| (element-wise magnitude)",
                lw=1.8, color='crimson')
        ax.set_title(self.name); ax.set_xlabel("f"); ax.legend()
        ax.grid(True, alpha=0.4)
        plt.tight_layout(); plt.show()

class prop_diff:
    name="differentiation"
    def __init__(self):
        self.t=np.linspace(-5,5,3000)
        self.freq=np.linspace(-4,4,400)
    def verify(self):
        t,f=self.t, self.freq
        dt=t[1]-t[0]
        sigma=1.0
        x=Signal.gaussian(t,sigma=sigma)
        xp=np.gradient(x,dt)
        rx,ix=CFTEngine.cft(t,x,f)
        rxp,ixp=CFTEngine.cft(t,xp,f)
        rxp_theory=2*np.pi*f*ix
        ixp_theory=2*np.pi*f*rx
        mse=CFTEngine.mse(CFTEngine.mag(rxp, ixp), CFTEngine.mag(rxp_theory,ixp_theory))
        return f,CFTEngine.mag(rxp, ixp), CFTEngine.mag(rxp_theory,ixp_theory)
    def plot(self):
        f, num_mag, theory_mag = self.verify()
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(f, num_mag,    lw=2.5, color='steelblue', label="|CFT{x'(t)}|")
        ax.plot(f, theory_mag, '--', lw=2, color='crimson', label="|j2πf·X(f)|")
        ax.set_title(self.name); ax.set_xlabel("f"); ax.legend()
        ax.grid(True, alpha=0.4)
        plt.tight_layout(); plt.show()

class prop_modulation:
    name="modulation"
    def __init__(self):
        self.t     = np.linspace(-5, 5, 2000)
        self.freqs = np.linspace(-5, 5, 400)
    def verify(self):
        t,f=self.t,self.freqs
        df=f[1]-f[0]
        x1=Signal.gaussian(t,sigma=1.5)
        x2=Signal.gaussian(t,sigma=1.0)
        product=x1*x2
        rprod,iprod=CFTEngine.cft(t,x1,f)
        R1, I1 = CFTEngine.cft(t, x1, f)
        R2, I2 = CFTEngine.cft(t, x2, f)
        X1_cplx = R1 + 1j*I1
        X2_cplx = R2 + 1j*I2
        conv_freq = np.convolve(np.real(X1_cplx), np.real(X2_cplx), 'same') * df
        mag_prod=CFTEngine.mag(rprod,iprod)
        mag_conv=np.abs(np.convolve(np.abs(X1_cplx), np.abs(X2_cplx),'same'),df)