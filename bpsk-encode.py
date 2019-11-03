from random import randint
from math import cos, pi
import numpy
import matplotlib.pyplot as plt
from scipy import signal, integrate

#---------------------------------------------------------------------------------------------#

def randPolarNRZSource( numberOfBits ):
    return [ 2*randint(0,1)-1 for i in range(numberOfBits) ]

#---------------------------------------------------------------------------------------------#

class BPSK:
    def __init__(self, listNRZ, amp, cycles, n):
        self.listNRZ = listNRZ
        self.amp = amp
        self.cycles = cycles 
        self.n = n
        self.expandedList = []
        self.carrier = []
        self.modulated = []
        self.filtered = []
        self.multiplied = []
        self.demodulated = []
        self.bpskList = []
        self.integrated = []

    def getNRZSource(self):
        return self.listNRZ
 
    def getExpandedSource(self):
        return self.expandedList
    
    def getCarrier(self):
        return self.carrier

    def encode(self):
        self.expandedList =  [ item for item in self.listNRZ for i in range(self.n) ]
        self.carrier = [ self.amp*round(cos(2*pi*self.cycles*round(i,4)), 5) for i in numpy.arange(0 , 1 , 1.0/self.n) ]
        c = int(len(self.expandedList)/len(self.carrier) )  * self.carrier              #Multiple carriers in all sequence
        self.modulated = [ c[i]*self.expandedList[i] for i in range(len(self.expandedList)) ]        
        
    def getModulated(self):
        return self.modulated

    def plotEncoding(self):
        t = [i for i in numpy.arange(0,len(self.listNRZ), 1.0/(self.n)) ]
        fig, axs = plt.subplots(4,1,constrained_layout=True)
        axs[0].set_xlim(-0.5,len(self.listNRZ)+0.5)
        axs[0].set_ylim(-0.1,1.2)
        axs[0].plot( [i+0.5 for i in range(len(self.listNRZ))], [(i+1)/2 for i in self.listNRZ], 'ro' )
        axs[0].vlines( [i+0.5 for i in range(len(self.listNRZ))],0, [(i+1)/2 for i in self.listNRZ], color='red')
        axs[0].set_ylabel('Bitstream')
        axs[1].set_xlim(-0.5,len(self.listNRZ)+0.5)
        axs[1].plot( t, self.expandedList, 'orange')
        axs[1].set_ylabel('NRZ')
        axs[2].set_xlim(-0.5,len(self.listNRZ)+0.5)
        axs[2].plot( t, self.modulated, 'darkblue', t, self.expandedList, 'orange' )
        axs[2].set_ylabel('Superposicion')
        axs[3].set_xlim(-0.5,len(self.listNRZ)+0.5)
        axs[3].plot( t, self.modulated, 'darkblue' )
        axs[3].set_ylabel('BPSK')
        fig.suptitle('Proceso de transmision', fontsize=16)
        plt.show()

    def decode(self, bpskList, threshold, nBits):
        #------------------------------ mult 2 signals --------------------------------------
        self.bpskList = bpskList
        c =  int(len(self.bpskList)/len(self.carrier)) * self.carrier
        self.multiplied = [c[i]*self.bpskList[i] for i in  range(len(self.bpskList)) ]  #2 components for signal        
        #------------------------------ filtering -------------------------------------------
        fc = self.cycles                    # identity cos^2 a = cos 2a   fc = 0.5*f_signal
        fs = self.n
        w = float(fc) / (fs / 2)            # Normalize the frequency
        b, a = signal.butter(5, w, 'low')
        self.filtered = signal.filtfilt(b, a, self.multiplied)
        #------------------------------ integrate -------------------------------------------
        for i in range(0,len(self.bpskList), int(len(self.bpskList)/nBits) ):
            f = self.multiplied[i:i+self.n]
            self.integrated += list(integrate.cumtrapz(f, initial=0) )

        self.filtered = self.integrated
        #-------------------------------- decision ------------------------------------------
        self.demodulated = [ 1 if(i>threshold) else -1  for i in self.filtered ]

    def plotDecoding(self):
        t = [i for i in numpy.arange(0,len(self.listNRZ), 1.0/(self.n)) ]
        fig, axs = plt.subplots(4,1,constrained_layout=True)
        axs[0].plot(t, self.bpskList, 'darkblue')
        axs[0].set_ylabel('Entrada')
        axs[1].plot( t, self.multiplied, 'orange')
        axs[1].set_ylabel('Multiplicacion')
        axs[2].plot( t, self.multiplied, 'orange', t, self.filtered, 'g' )
        axs[2].set_ylabel('Filtrado (NRZ)')
        axs[3].plot( t, self.demodulated, 'red' )
        axs[3].set_ylabel('Decision (NRZ)')
        fig.suptitle('Proceso de recepcion', fontsize=16)
        plt.show()

    def plotComparison(self):
        t = [i for i in numpy.arange(0,len(self.listNRZ), 1.0/(self.n)) ]
        fig, axs = plt.subplots(3,1,constrained_layout=True)
        axs[0].plot(t, self.expandedList, 'blue')
        axs[0].set_ylabel('Entrada')
        axs[1].plot( t, self.demodulated, 'red')
        axs[1].set_ylabel('Salida')
        axs[2].plot( t, self.expandedList, 'blue', t, self.demodulated, 'red' )
        axs[2].set_ylabel('Superposicion')
        fig.suptitle('Comparacion entrada-salida', fontsize=16)
        plt.show()
        
#---------------------------------------------------------------------------------------------#
nBits     = 20                                  #number of bits of the source
n         = 100                                 #number of samples per bit
amp       = 1.0                                 #amplitude of carrier
cycles    = 3                                  #cycles per bit
threshold = 0                                   #threshold used for the '0' or '1' decision

#--------------------------------MAIN Program-------------------------------------------------#
randSrc   = randPolarNRZSource(nBits)        
BPSK1 = BPSK(randSrc, amp, cycles, n)
BPSK1.encode()
BPSK1.plotEncoding()
outputBPSK = BPSK1.getModulated()

BPSK1.decode(outputBPSK, threshold, nBits)
BPSK1.plotDecoding()
BPSK1.plotComparison()

print ('La entrada es',  BPSK1.getNRZSource())




