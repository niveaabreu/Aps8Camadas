
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
        self.T = 5
        self.t = np.linspace(-self.T/2,self.T/2,self.T*self.fs)
        print("--->Inicializando encoder\n")
        sd.default.samplerate = self.fs
        sd.default.channels = 2  #voce pode ter que alterar isso dependendo da sua placa
        print("-->Gravação irá se iniciar em 3s...\n")
        time.sleep(3.3)
        print("-->Gravação Iniciada\n")
        numAmostras = self.fs * self.T
        audio = sd.rec(int(numAmostras), self.fs, channels=1)
        sd.wait()
        print("-->Gravação encerrada\n")
        self.audio = audio[:,0]
        filename = 'gravacao.wav'
        sf.write(filename, audio, self.fs)

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
        return np.array(map(lambda x:x/max,sinal))

    def todB(self,s):
        sdB = 10*np.log10(s)
        return(sdB)

    def main(self):
        print("--> Em 3s iremos iniciar a transmissão do sinal modulado\n")
        audio_res = self.LPF(self.audio,2500)
        _,portadora = self.signal.generateSin(13000,self.A,self.T,self.fs)
        sinal = audio_res*portadora
        sd.play(sinal, self.fs)
        sd.wait()
        print("--> Finalizado áudio controlado\n")
        sinal_normalizado = self.normalize(sinal)
        print("--> Executando sinal normalizado\n")
        sd.play(sinal_normalizado, self.fs)
        sd.wait()
        filename = 'sinal_modulado.wav'
        sf.write(filename, sinal_normalizado, self.fs)
    

if __name__ == "__main__":
    a = Encode()
    a.main()
