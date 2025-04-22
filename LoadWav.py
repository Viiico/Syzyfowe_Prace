import numpy as np
import wave

class LoadWav:

    def __init__(self, fileName):
        self.fileName = fileName
        file = wave.open(self.fileName, "rb")
        self.nchannels = file.getnchannels()
        self.sampwidth = file.getsampwidth()
        self.framerate = file.getframerate()
        self.nframes = file.getnframes()
        self.comptype = file.getcomptype()
        self.compname = file.getcompname()
        self.t = (self.nframes - 1)/self.framerate

        if self.sampwidth == 1:
            self.wavData = np.frombuffer(file.readframes(self.nframes), dtype=np.int8)
        elif self.sampwidth == 2:
            self.wavData = np.frombuffer(file.readframes(self.nframes), dtype=np.int16)
        elif self.sampwidth == 4:
            self.wavData = np.frombuffer(file.readframes(self.nframes), dtype=np.int32)

        if self.nchannels == 2:
            self.wavData = self.wavData.reshape(-1, 2)

        file.close()

    def printParams(self):
        print("nchannels: " + str(self.nchannels))
        print("sampwidth: " + str(self.sampwidth))
        print("framerate: " + str(self.framerate))
        print("nframes: " + str(self.nframes))
        print("comptype: " + str(self.comptype))
        print("compname: " + str(self.compname))
        print("t: " + str(self.t))

    def getParams(self):
        return self.fileName, self.nchannels, self.sampwidth, self.framerate, self.nframes, self.compname, self.comptype, self.t

    def getWavData(self):
        return self.wavData

if __name__ == "__main__":
    file = LoadWav("Pliki/signalNoise8.wav")
    file.printParams()
    file.getWavData()