from random import randint
from math import sin, pi
import numpy
import matplotlib.pyplot as plt


#---------------------------------------------------------------------------------------------#
def randPolarNRZSource( numberOfBits ):
    return [ 2*randint(0,1)-1 for i in range(numberOfBits) ]

#---------------------------------------------------------------------------------------------#
class BPSKEncode:
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

    def expandBits(self):
        self.expandedList =  [ item for item in self.listNRZ for i in range(self.n) ]
    
    def getExpandedSource(self):
        return self.expandedList

    def carrierGen(self):
        self.carrier = [ self.amp*round(sin(2*pi*self.cycles*round(i,4)), 5) for i in numpy.arange(0 , 1 , 1.0/self.n) ]
    
    def getCarrier(self):
        return self.carrier

    def multiply(self):
        c = (len(self.expandedList)/(len(self.carrier) )  *self.carrier )             #Multiple carriers in all sequence
        self.output = [ c[i]*self.expandedList[i] for i in range(len(self.expandedList)) ]

    def getOutput(self):
        return self.output
#---------------------------------------------------------------------------------------------#

nBits  = 10             #number of bits of the source
amp    = 0.8            #amplitude of carrier
cycles = 3              #cycles per bit
n      = cycles*20      #number of samples per bit

randomSource = randPolarNRZSource(nBits)
print(randomSource)

BPSK = BPSKEncode(randomSource, amp, cycles, n)
#print BPSK.getNRZSource()
BPSK.expandBits()
#print BPSK.getExpandedSource()
BPSK.carrierGen()
#print BPSK.getCarrier() 
BPSK.multiply()
#print BPSK.getOutput()

#t = [i for i in numpy.arange(0,nBits, 1.0/(n*1)) ]
#fig, axs = plt.subplots(4,1,constrained_layout=True)

#axs[0].set_xlim(-0.5,nBits+0.5)
#axs[0].set_ylim(-0.1,1.2)
#axs[0].plot( [i+0.5 for i in range(len(source))], [(i+1)/2 for i in source], 'ro' )
#axs[0].vlines( [i+0.5 for i in range(len(source))],0, [(i+1)/2 for i in source], color='red')
#axs[0].set_ylabel('Bitstream')

#axs[1].plot( t, expandedSource, 'orange')
#axs[1].set_ylabel('NRZ')

#axs[2].plot( t, output, 'darkblue', t, expandedSource, 'orange' )
#axs[2].set_ylabel('Superposicion')

#axs[3].plot( t, output, 'darkblue' )
#axs[3].set_ylabel('BPSK')

#fig.suptitle('Proceso de transmision', fontsize=16)
#plt.show()




