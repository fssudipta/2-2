import numpy as np
import matplotlib.pyplot as plt
#from imageio import imread
import imageio.v2 as imageio
imread = imageio.imread

# =====================================================
# Continuous Image Class
# =====================================================
class ContinuousImage:
    """
    Represents an image as a continuous 2D signal.
    """

    def __init__(self, image_path):
        self.image = imread(image_path, mode='L')
        self.image = self.image / np.max(self.image)

        # Define continuous spatial axes
        self.x = np.linspace(-1, 1, self.image.shape[1])
        self.y = np.linspace(-1, 1, self.image.shape[0])

    def show(self, title="Image"):
        plt.figure(figsize=(8,8))
        plt.imshow(self.image, cmap='gray')
        plt.title(title)
        plt.axis('off')
        plt.show()


# =====================================================
# 2D Continuous Fourier Transform Class
# =====================================================
class CFT2D:
    """
    Computes 2D Continuous Fourier Transform
    using separability and numerical integration.
    """

    def __init__(self, image_obj:ContinuousImage):
        self.I = image_obj.image
        self.x = image_obj.x
        self.y = image_obj.y
        self.u=np.linspace(-1,1,self.I.shape[1])
        self.v=np.linspace(-1,1,self.I.shape[0])

    def compute_cft(self):
        """
        Compute real and imaginary parts of 2D CFT.
        """
        num_u=len(self.u)
        num_v=len(self.v)
        rows,cols=self.I.shape
        R_x=np.zeros((num_u,rows))
        I_x=np.zeros((num_u,rows))
        
        for k in range(num_u):
            u_val= self.u[k]
            phase_x= 2*np.pi*u_val*self.x
            R_x[k, :] =np.trapezoid(self.I * np.cos(phase_x), self.x,axis=1)
            I_x[k, :] =np.trapezoid(self.I*(-np.sin(phase_x)), self.x, axis=1)
            
        real_part=np.zeros((num_v, num_u))
        imag_part=np.zeros((num_v, num_u))
        for m in range(num_v):
            v_val= self.v[m]
            phase_y=2*np.pi*v_val*self.y
            cos_y=np.cos(phase_y)
            sin_y=np.sin(phase_y)
            real_part[m, :]=np.trapezoid(R_x*cos_y+I_x*sin_y,self.y,axis=1)
            imag_part[m, :]=np.trapezoid(I_x*cos_y-R_x*sin_y,self.y,axis=1)
            
        self.real= real_part
        self.imag= imag_part
        return real_part,imag_part

    def plot_magnitude(self):
        """
        Plot log-scaled magnitude spectrum.
        """
        magnitude=np.sqrt(self.real**2+self.imag**2)
        plt.figure(figsize=(8,8))
        plt.imshow(np.log(1+magnitude), cmap='inferno')
        plt.title("2D CFT Magnitude spectrum")
        plt.axis('off')
        plt.show()


# =====================================================
# Frequency Filtering
# =====================================================
class FrequencyFilter:
    def low_pass(self, real, imag, cutoff):
        rows, cols = real.shape
        cx, cy = rows//2, cols//2

        for i in range(rows):
            for j in range(cols):
                if np.sqrt((i-cx)**2 + (j-cy)**2) > cutoff:
                    real[i,j] = 0
                    imag[i,j] = 0
        return real, imag

# =====================================================
# Inverse 2D Continuous Fourier Transform
# =====================================================
class InverseCFT2D:
    """
    Reconstructs image from 2D frequency spectrum.
    """

    def __init__(self, real, imag, x, y):
        self.real=real 
        self.imag = imag
        self.x = x
        self.y = y
        self.u=np.linspace(-1,1,real.shape[1])
        self.v=np.linspace(-1,1,real.shape[0])

    def reconstruct(self):
        """
        Perform inverse 2D CFT using numerical integration.
        """
        num_x=len(self.x)
        num_y=len(self.y) 
        R_u=np.zeros((num_x, len(self.v)))
        I_u=np.zeros((num_x, len(self.v)))
        
        for k in range(num_x):
            x_val=self.x[k]
            phase_u=2*np.pi*x_val*self.u
            cos_u=np.cos(phase_u)
            sin_u=np.sin(phase_u)
            
            R_u[k, :]=np.trapezoid(self.real*cos_u-self.imag*sin_u,self.u,axis=1)
            I_u[k, :]=np.trapezoid(self.real*sin_u+self.imag*cos_u,self.u,axis=1)
            
        recon=np.zeros((num_y, num_x))
        for m in range(num_y):
            v_phase=2*np.pi*self.y[m]*self.v
            recon[m, :]=np.trapezoid(R_u*np.cos(v_phase)-I_u*np.sin(v_phase),self.v,axis=1)
            
        recon=(recon-np.min(recon)) / (np.max(recon)-np.min(recon))
        return recon


# =====================================================
# Main Execution (Task 2)
# =====================================================
if __name__=="__main__":
    img = ContinuousImage("E:\\2-2\\220 signal\\Offline on CFT\\noisy_image.png")
    img.show("Original Image")
    cft2d = CFT2D(img)
    real, imag = cft2d.compute_cft()
    cft2d.plot_magnitude()

    filt = FrequencyFilter()
    real_f, imag_f = filt.low_pass(real, imag, cutoff=40)

    icft2d = InverseCFT2D(real_f, imag_f, img.x, img.y)
    denoised = icft2d.reconstruct()

    plt.imshow(denoised, cmap='gray')
    plt.title("Reconstructed (Denoised) Image")
    plt.axis('off')
    plt.show()
