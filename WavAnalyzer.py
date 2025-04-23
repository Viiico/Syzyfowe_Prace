from LoadWav import LoadWav
import numpy as np
import matplotlib.pyplot as plt

class WavAnalyzer:
    def __init__(self, fileName):
        self.file = LoadWav(fileName)
        self.signal = self.file.getWavData()
        self.t = np.linspace(0, self.file.getParams()[7], self.file.getParams()[4])
        self.signalFFT = []
        self.freq = []


        # wydlużenie sygnału do najbliższej potęgi 2, potrzebne do użycia FFT
    def padSignal(self):
        n = len(self.signal)
        i = 1
        while(True):
            if(i >= n):
                return np.concatenate((self.signal, np.zeros(i-n)))
            else:
                i *= 2

        # aglorytm rekurencyjny FFT Cooley–Tukey
    def fft(self):
        def fft2(x):
            n = len(x)
            if n <= 1:
                return x
            even = fft2(x[0::2])
            odd = fft2(x[1::2])
            t = [np.exp(-2j * np.pi * k / n) * odd[k] for k in range(n // 2)]
            return [even[k] + t[k] for k in range(n // 2)] + \
                [even[k] - t[k] for k in range(n // 2)]

        padX = self.padSignal()
        self.signalFFT = fft2(padX)
        self.freq = np.linspace(0, self.file.getParams()[3]//2, len(self.signalFFT)//2)
        self.freq = np.concatenate((self.freq, -self.freq[::-1]))

        # znajdowanie głównych składowych sygnału
    def findPeaks(self, ignoreRatio, spacing):
        peaks = []
        values = []
        amax = 0
        for i in range(0, len(self.signalFFT) - 1):
            if(abs(self.signalFFT[i]) >= amax):
                amax = abs(self.signalFFT[i])

        for i in range(1, len(self.signalFFT) - 1):
            if(abs(self.signalFFT[i]) > amax * ignoreRatio and abs(self.signalFFT[i]) > abs(self.signalFFT[i-1]) and abs(self.signalFFT[i]) > abs(self.signalFFT[i+1]) and self.freq[i] >= 0):
                if(len(peaks) == 0):
                    peaks.append(self.freq[i])
                    values.append(abs(self.signalFFT[i]))
                else:
                    if(self.freq[i] - peaks[-1] > spacing):
                        peaks.append(self.freq[i])
                        values.append(abs(self.signalFFT[i]))
                    elif(abs(self.signalFFT[i]) > values[-1]):
                        peaks[-1] = self.freq[i]
                        values[-1] = abs(self.signalFFT[i])

        return peaks, values

        # rysowanie wykresów
    def makeGraph(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

        ax1.plot(self.t, self.signal, "o", label="x(t)", color="red")
        ax1.set_title("Sygnał")
        ax1.set_xlabel("t[s]")
        ax1.set_ylabel("A")
        ax1.legend()
        ax1.grid()

        ax2.plot(self.freq, np.abs(self.signalFFT), label="X(f)", color="blue")
        ax2.set_title("Widmo sygnału")
        ax2.set_xlabel("f[Hz]")
        ax2.set_ylabel("|X(f)|")
        ax2.legend()
        ax2.grid()

        plt.show()

if __name__ == "__main__":
    wav = WavAnalyzer("Pliki/signalNoise8.wav")
    wav.fft()
    wav.makeGraph()
    peaks = wav.findPeaks(0.1, 100)
    for i in range(0, len(peaks[0])):
        print(f"f = {peaks[0][i]:.2f}Hz, |X(f)| = {peaks[1][i]:.2f}")