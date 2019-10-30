from random import randint
from math import sin, pi
import numpy
import matplotlib.pyplot as plt

#---------------------------------------------------------------------------------------------#
def polarNRZSource( numberOfBits ):
    return [ 2*randint(0,1)-1 for i in range(numberOfBits) ]

class BPSK:
    def __init__(self, listNRZ):
        self.listNRZ = listNRZ

    def expandBits(self , factor):
        return [ item for item in self.listNRZ for i in range(factor) ]
    
    def sinGenerator( A, fc, n ):
        return [ A*round(sin(2*pi*fc*round(i,4)), 5) for i in numpy.arange(0 , 1 , 1.0/n) ]

    def multiply(seq, carrier):
        c = (len(seq)/(len(carrier) )  *carrier )             #Multiple carriers in all sequence
        return [ c[i]*seq[i] for i in range(len(seq)) ]
#---------------------------------------------------------------------------------------------#

nBits  = 10             #number of bits of the source
amp    = 0.8            #amplitude of carrier
cycles = 3              #cycles per bit
n      = cycles*20      #number of samples per bit

source = polarNRZSource(nBits)
print(source)

expandedSource = expandBits(source, n)
#print(expandedSource)

carrier = sinGenerator(amp, cycles, n)
#print(carrier)

output = multiply(expandedSource, carrier)
#print(output)

t = [i for i in numpy.arange(0,nBits, 1.0/(n*1)) ]
fig, axs = plt.subplots(4,1,constrained_layout=True)

axs[0].set_xlim(-0.5,nBits+0.5)
axs[0].set_ylim(-0.1,1.2)
axs[0].plot( [i+0.5 for i in range(len(source))], [(i+1)/2 for i in source], 'ro' )
axs[0].vlines( [i+0.5 for i in range(len(source))],0, [(i+1)/2 for i in source], color='red')
axs[0].set_ylabel('Bitstream')

axs[1].plot( t, expandedSource, 'orange')
axs[1].set_ylabel('NRZ')

axs[2].plot( t, output, 'darkblue', t, expandedSource, 'orange' )
axs[2].set_ylabel('Superposicion')

axs[3].plot( t, output, 'darkblue' )
axs[3].set_ylabel('BPSK')

fig.suptitle('Proceso de transmision', fontsize=16)
plt.show()




