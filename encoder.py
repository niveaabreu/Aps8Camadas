
#importe as bibliotecas
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import soundfile as sf
from scipy import signal as sg
import time


class Encode:
    def __init__(self) -> None:
        self.signal = signalMeu()
        self.fs = 44100
        self.A = 1
        print("--->Inicializando encoder\n")
        sd.default.samplerate = self.fs
        sd.default.channels = 1  #voce pode ter que alterar isso dependendo da sua placa
        self.audio, self.samplerate = sf.read('guns.wav')
        self.T = int(len(self.audio[:336000,0])/self.samplerate)
        self.t=np.arange(0,len(self.audio[:336000,0])/self.samplerate,1/self.samplerate)
        sd.play(self.audio[:336000,0], self.fs)
        sd.wait()

    def LPF(self,signal, cutoff_hz):
        nyq_rate = self.fs/2
        width = 5.0/nyq_rate
        ripple_db = 60.0 #dB
        N , beta = sg.kaiserord(ripple_db, width)
        taps = sg.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
        return( sg.lfilter(taps, 1.0, signal))

    def signal_handler(self,signal, frame):
            print('You pressed Ctrl+C!')
            sys.exit(0)
        
    def normalize(self,sinal):
        max = np.max(np.abs(sinal))
        return sinal/max

    def todB(self,s):
        sdB = 10*np.log10(s)
        return(sdB)

    def main(self):
        print("-->  Tocando Áudio filtrado\n")
        audio_res = self.LPF(self.audio[:336000,0],2500)

        plt.plot(self.t,audio_res)
        plt.title('Sinal de áudio filtrado – domínio do tempo')
        plt.show()

        X, Y = self.signal.calcFFT(audio_res, self.fs)
        plt.plot(X, np.abs(Y))
        plt.xlabel('Hz')
        plt.title('Sinal de áudio filtrado – domínio da frequência')
        plt.show()

        sd.play(audio_res, self.fs)
        sd.wait()
        _,portadora = self.signal.generateSin(13000,self.A,self.T,self.samplerate)
        sinal = audio_res*portadora
        print("--> Áudio modularizado\n")

        plt.plot(self.t,sinal)
        plt.title('sinal de áudio modulado – domínio do tempo ')
        plt.show()

        Xmod, Ymod = self.signal.calcFFT(sinal, self.fs)
        plt.plot(Xmod, np.abs(Ymod))
        plt.xlabel('Hz')
        plt.title('sinal de áudio modulado – domínio da frequência')
        plt.show()

        sd.play(sinal, self.fs)
        sd.wait()
        print("--> Normalizando modularização\n")
        sinal_normalizado = self.normalize(sinal)
        print("--> Executando sinal normalizado\n")
        sd.play(sinal_normalizado, self.fs)
        sd.wait()
        filename = 'sinal_modulado.wav'
        sf.write(filename, sinal_normalizado, self.fs)
    

if __name__ == "__main__":
    a = Encode()
    a.main()
