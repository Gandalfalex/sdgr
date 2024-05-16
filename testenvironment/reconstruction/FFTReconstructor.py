import numpy as np
from scipy.fft import fft, ifft, fftfreq

class FFTReconstructor():

    def reconstruct(self, imf, t):
        yf = fft(imf)
        xf = fftfreq(n=len(t), d=(t[1] - t[0]))
        N = 100

        t_extended = np.linspace(t[0], t[-1] + N, len(t) + N)

        imf_extended = ifft(yf, n=len(t_extended))

        imf_extended = np.real(imf_extended)
        print(imf_extended.shape)
        return imf_extended