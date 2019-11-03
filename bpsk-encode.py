from random import randint
from math import sin, pi
import numpy
import matplotlib.pyplot as plt
from scipy import signal

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
        self.output = []

    def getNRZSource(self):
        return self.listNRZ
 
    def getExpandedSource(self):
        return self.expandedList
    
    def getCarrier(self):
        return self.carrier

    def encode(self):
        self.expandedList =  [ item for item in self.listNRZ for i in range(self.n) ]
        self.carrier = [ self.amp*round(sin(2*pi*self.cycles*round(i,4)), 5) for i in numpy.arange(0 , 1 , 1.0/self.n) ]
        c = (len(self.expandedList)/(len(self.carrier) )  *self.carrier )             #Multiple carriers in all sequence
        self.output = [ c[i]*self.expandedList[i] for i in range(len(self.expandedList)) ]        
        
    def getOutput(self):
        return self.output

    def plotEncoding(self):
        t = [i for i in numpy.arange(0,len(self.listNRZ), 1.0/(self.n*1)) ]
        fig, axs = plt.subplots(4,1,constrained_layout=True)
        axs[0].set_xlim(-0.5,len(self.listNRZ)+0.5)
        axs[0].set_ylim(-0.1,1.2)
        axs[0].plot( [i+0.5 for i in range(len(self.listNRZ))], [(i+1)/2 for i in self.listNRZ], 'ro' )
        axs[0].vlines( [i+0.5 for i in range(len(self.listNRZ))],0, [(i+1)/2 for i in self.listNRZ], color='red')
        axs[0].set_ylabel('Bitstream')
        axs[1].plot( t, self.expandedList, 'orange')
        axs[1].set_ylabel('NRZ')
        axs[2].plot( t, self.output, 'darkblue', t, self.expandedList, 'orange' )
        axs[2].set_ylabel('Superposicion')
        axs[3].plot( t, self.output, 'darkblue' )
        axs[3].set_ylabel('BPSK')
        fig.suptitle('Proceso de transmision', fontsize=16)
        plt.show()

    def decode(self, bpskList):
        #-------------------------------mult 2 signals------------------------------------------
        c = (len(bpskList)/(len(self.carrier) )  *self.carrier )
        multiplied = [c[i]*bpskList[i] for i in  range(len(bpskList)) ]  #2 components for signal        
        plt.plot(multiplied)
        #--------------------------------- filtering -------------------------------------------
        fc = self.cycles                    # identity cos^2 a = cos 2a   fc = 0.5*f_signal
        w = float(fc) / (self.n / 2)        # Normalize the frequency
        b, a = signal.butter(5, w, 'low')
        out = signal.filtfilt(b, a, multiplied)
        plt.plot(out,'r')
        #-------------------------------- decision --------------------------------------------
        goodOut = [ 1 if(i>0) else 0  for i in out ]
        plt.plot(goodOut,'g')
        plt.show()
        
#---------------------------------------------------------------------------------------------#
nBits   =10                                   #number of bits of the source
randSrc = randPolarNRZSource(nBits)           #get a random list or NRZ values
amp     = 0.8                                 #amplitude of carrier
cycles  = 100                                  #cycles per bit
n       = 1000                                 #number of samples per bit

#--------------------------------MAIN Program-------------------------------------------------#
BPSK1 = BPSK(randSrc, amp, cycles, n)
BPSK1.encode()
inputData  = BPSK1.getNRZSource()
output = BPSK1.getOutput()
print inputData
BPSK1.plotEncoding()
BPSK1.decode(output)
#print BPSK.getOutput()
#print BPSK.getExpandedSource()
#print BPSK.getCarrier() 





