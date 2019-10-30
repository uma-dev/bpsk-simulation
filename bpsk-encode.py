from random import randint
from math import sin, pi
import numpy
import matplotlib.pyplot as plt

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

#---------------------------------------------------------------------------------------------#

nBits   = 10                                 #number of bits of the source
amp     = 0.8                                #amplitude of carrier
cycles  = 3                                  #cycles per bit
n       = cycles*20                          #number of samples per bit
randSrc = randPolarNRZSource(nBits)          #get a random list or NRZ values

BPSK = BPSK(randSrc, amp, cycles, n)
BPSK.encode()
BPSK.plotEncoding()

#print BPSK.getOutput()
#print BPSK.getNRZSource()
#print BPSK.getExpandedSource()
#print BPSK.getCarrier() 





