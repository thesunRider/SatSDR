import numpy as np
import matplotlib.pyplot as plt


fs_data = 144000          # sample rate (your GQRX rate)
fc = 137.9e6      # desired RF frequency

samples = np.fromfile('D:\\projects\\electronics\\SatSDR\\data\\gqrx_20191103_133844_137900000_144000_fc.raw', np.complex64) # Read in file.  We have to tell it what format it is
time_recording = len(samples)/fs_data

print(samples,"time(s)=",time_recording)