#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas
import numpy as np
import sounddevice as sd
from scipy import signal
import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from suaBibSignal import *
import peakutils
from scipy import signal as sg
import time
import soundfile as sf


class Decode:
    def __init__(self) -> None:
        print("--->Inicializando decoder\n")
        self.signal = signalMeu()
        self.fs = 44100
        self.audio, self.samplerate = sf.read('sinal_modulado.wav')
        self.A = 1
        self.T = int(len(self.audio[:308700])/self.samplerate)
        self.t=np.arange(0,len(self.audio[:308700])/self.samplerate,1/self.samplerate)
        print("--->Ouvindo sinal a ser demodularizado\n")
        sd.play(self.audio, self.fs)
        sd.wait()
    
    def LPF(self,signal, cutoff_hz):
        nyq_rate = self.fs/2
        width = 5.0/nyq_rate
        ripple_db = 60.0 #dB
        N , beta = sg.kaiserord(ripple_db, width)
        taps = sg.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
        return( sg.lfilter(taps, 1.0, signal))

    def todB(self,s):
        sdB = 10*np.log10(s)
        return(sdB)

    def main(self):
    
        _,portadora = self.signal.generateSin(13000,self.A,self.T,self.samplerate)
        sinal = self.audio[:308700] * portadora
        audio_res = self.LPF(sinal,2500)

        Xdmod, Ydemod = self.signal.calcFFT(sinal, self.samplerate)
        Xdmodfil, Ydemodfil = self.signal.calcFFT(audio_res, self.samplerate)
        plt.plot(Xdmod, np.abs(Ydemod))
        plt.xlabel('Hz')
        plt.title('Sinal de áudio demodulado – domínio da frequência')
        plt.show()

        plt.plot(Xdmodfil, np.abs(Ydemodfil))
        plt.xlabel('Hz')
        plt.title('Sinal de áudio demodulado e filtrado – domínio da frequência')
        plt.show()

        print("--->Ouvindo sinal demodularizado\n")
        sd.play(sinal, self.fs)
        sd.wait()
        print("--->Ouvindo sinal demodularizado filtrado\n")
        sd.play(audio_res, self.fs)
        sd.wait()

if __name__ == "__main__":
    a = Decode()
    a.main()
