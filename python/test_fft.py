import numpy as np
import matplotlib.pyplot as plt
import cmsisdsp as dsp

# -----------------------
# Parameters
# -----------------------
fs = 1_000_000  # 1 MHz sampling
N = 4096

t = np.arange(N) / fs

# -----------------------
# Test signal (multi-tone)
# -----------------------
x = (
    np.cos(2*np.pi*100e3*t) +
    0.5*np.cos(2*np.pi*200e3*t) +
    0.2*np.cos(2*np.pi*300e3*t)
)



# -----------------------
# Equivalent to arm_rfft_fast_f32
# -----------------------
X = np.fft.rfft(x)   # real FFT

# Frequency axis
f = np.fft.rfftfreq(N, 1/fs)

# Magnitude
mag = np.abs(X)


def bandpass_q31(f1, f2, fs, num_taps):
    n = np.arange(num_taps) - (num_taps - 1) / 2

    w1 = 2 * np.pi * f1 / fs
    w2 = 2 * np.pi * f2 / fs

    h = np.zeros(num_taps)

    for i, ni in enumerate(n):
        if ni == 0:
            h[i] = (w2 - w1) / np.pi
        else:
            h[i] = (np.sin(w2 * ni) - np.sin(w1 * ni)) / (np.pi * ni)

    # Hamming window
    hamming = 0.54 - 0.46 * np.cos(2 * np.pi * np.arange(num_taps) / (num_taps - 1))
    h *= hamming

    # Normalize
    h /= np.sum(h)

    # Convert to Q31
    q31 = np.clip(h * (2**31 - 1), 0, 2**31 - 1).astype(np.int32)

    return q31


def calculate_fft_dsp(x):
    #------ One time Initialisation 
    rfft_instance = dsp.arm_rfft_fast_instance_f32()
    return_code = dsp.arm_rfft_fast_init_f32(rfft_instance,4096)

    #-----------
    fft_ydata = dsp.arm_rfft_fast_f32(rfft_instance,x,0)
    rfft_mag = dsp.arm_cmplx_mag_f32(fft_ydata)
    return rfft_mag


def calculate_band_pass(x,coeffs):
    #------ One time Initialisation
    block_size = len(x) -100
    rfft_instance = dsp.arm_fir_instance_q31()
    state = np.zeros(len(coeffs) + block_size - 1)
    return_code = dsp.arm_fir_init_q31(rfft_instance,len(coeffs),coeffs,state)
    #-----------

    return dsp.arm_fir_q31(rfft_instance,x)

rfft_mag = calculate_fft_dsp(x)


plt.plot(f, mag)
plt.plot(f[1:],  rfft_mag )



f1 = 50_000
f2 = 150_000
num_taps = 101

coeffs = bandpass_q31(f1, f2, fs, num_taps)

print(coeffs[:10])
got_value = calculate_band_pass(x,coeffs)

X = np.fft.rfft(got_value)
mag = np.abs(X)

plt.plot(f,  mag )




# -----------------------
# Plot
# -----------------------
plt.title("512-point RFFT (Python equivalent)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.grid()
plt.ticklabel_format(style='sci', axis='x', scilimits=(3,3))
plt.show()
