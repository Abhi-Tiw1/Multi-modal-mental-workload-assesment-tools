import numpy as np
from scipy import signal, stats
import matplotlib.pyplot as plt
from numpy import abs, sum, linspace
from numpy.fft import rfft

def ratio_ener(fft_vals,fft_freq):

	low_f=np.where((fft_freq>=0.05) & (fft_freq<=0.25))
	hi_f=np.where((fft_freq>=0.25) & (fft_freq<=0.5))
	
	low_e=np.log(np.sum(fft_vals[low_f]))
	hi_e=np.log(np.sum(fft_vals[hi_f]))
	
	rat=hi_e-low_e
	return rat

def br_spectral(br_sig,fs):
	# Get real amplitudes of FFT (only in postive frequencies)
	br_sig=(br_sig-np.mean(br_sig))/np.std(br_sig)
	
	fft_vals = np.absolute(np.fft.rfft(br_sig))
	fft_vals=fft_vals/np.sum(fft_vals)

	# Get frequencies for amplitudes in Hz
	fft_freq = np.fft.rfftfreq(len(br_sig), 1.0/fs)
	
	br_bands=np.linspace(0,1,6)

	band_no=len(br_bands)-1
	br_band_pwr = np.zeros(band_no)
	
	for i in range(0,band_no):
		flo=br_bands[i]
		fhi=br_bands[i+1]
		freq_ix = np.where((fft_freq >= flo) & 
						   (fft_freq <= fhi))[0]
		br_band_pwr[i] = np.mean(fft_vals[freq_ix]*fft_vals[freq_ix])
		
	bnd_ratio=ratio_ener(fft_vals,fft_freq)
	
	#ignoring the low freq regions
	vals=fft_vals[np.where(fft_freq>0.015)]
	freqs=fft_freq[np.where(fft_freq>0.015)]
	br_rate=freqs[np.argmax(vals)]

	#spectral centroid and flatness
	n_spec = vals / sum(vals)  # like a probability mass function
	n_freq = linspace(0, 1, len(n_spec))
	br_cent = sum(n_freq * n_spec)*np.max(freqs)
	
	
	
	return np.hstack((br_band_pwr,bnd_ratio,br_rate,br_cent))
	
def br_stat(br_sig):
	
	br_fts=np.zeros(6)
	
	#br_sig=(br_sig-np.mean(br_sig))/np.std(br_sig)
	
	br_fts[0] = np.mean(br_sig)
	br_fts[1] = np.std(br_sig)
	br_fts[2] = np.max(br_sig)-np.min(br_sig)
	br_fts[3] = stats.skew(br_sig)
	br_fts[4] = stats.kurtosis(br_sig)
	br_fts[5] = np.mean(np.diff(br_sig))
	
	return br_fts
	

def get_br_base_feats(br_sig,fs_br):
	
	br_stats=br_stat(br_sig)
	br_spec=br_spectral(br_sig,fs_br)
	
	return np.hstack((br_stats,br_spec))
	
def get_br_fnms():
	
	fnm_stat=['mean','std','rng','skew','kurt','diff_mn','pwr_ratio','rate','cent']
	fnm_spec=['pwr_0_2','pwr_2_4','pwr_4_6','pwr_6_8','pwr_8_10']
	
	return fnm_stat+fnm_spec
