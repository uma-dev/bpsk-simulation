from random import randint
from math import sin, pi
import numpy
import matplotlib.pyplot as plt

#---------------------------------------------------------------------------------------#
def polarNRZSource( numberOfBits ):
    return [ 2*randint(0,1)-1 for i in range(numberOfBits) ]

def expandBits( NRZList, factor ):
    #return [ factor*str(i) for i in NRZList ]
    return [ item for item in NRZList for i in range(factor) ]
    
def sinGenerator( A, fc, fSampling ):
    return [ A*round(sin(2*pi*round(i,4)), 5) for i in numpy.arange(0 , 1 , 1.0/fSampling) ]

def multiply(seq, carrier):
    c = (len(seq)/(len(carrier) )  *carrier )             #Multiple cycles of the carrier
    return [ c[i]*seq[i] for i in range(len(seq)) ]
#---------------------------------------------------------------------------------------#

nBits = 3              #number of bits of the source
amp = 12                #amplitude of carrier
fc = 5                 #freq of carrier
fs = fc*10             #freq of sampling
expandFactor = fs*2  #number of cycles in each bit

source = polarNRZSource(nBits)
print(source)

expandedSource = expandBits(source, expandFactor)
#print(expandedSource)

carrier = sinGenerator(amp, fc, fs)
#print(carrier)

output = multiply(expandedSource, carrier)
#print(output)

#t = [i for i in ]
t = [i for i in range(expandFactor*nBits)]
plt.plot( t, output )
plt.ylabel('Salida modulada BPSK')
plt.show()

