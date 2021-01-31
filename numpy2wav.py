import numpy
from scipy.io import wavfile

fs = 44100
f = numpy.loadtxt('received_file.txt',dtype=numpy.float32)
wavfile.write('audio.wav', fs, f)
