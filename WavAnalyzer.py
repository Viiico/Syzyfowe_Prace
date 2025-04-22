from LoadWav import LoadWav
import numpy as np
import matplotlib.pyplot as plt

class WavAnalyzer:
    def __init__(self, fileName):
        self.file = LoadWav(fileName)
        self.signal = self.file.getWavData()
        self.signalFFT = np.fft.fft(self.signal)

    def makeGraph(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        t = np.linspace(0, self.file.getParams()[7], self.file.getParams()[4])
        ax1.plot(t, self.signal, label="xn", color="red")
        ax1.set_title("Sygnał")
        ax1.set_xlabel("t[s]")
        ax1.set_ylabel("A")
        ax1.legend()
        ax1.grid()

        ax2.plot(t, self.signalFFT, label="Xk", color="blue")
        ax2.set_title("Widmo sygnału")
        ax2.set_xlabel("f")
        ax2.set_ylabel("A")
        ax2.legend()
        ax2.grid()
        plt.show()

if __name__ == "__main__":
    wav = WavAnalyzer("Pliki/signalNoise8.wav")
    wav.makeGraph()