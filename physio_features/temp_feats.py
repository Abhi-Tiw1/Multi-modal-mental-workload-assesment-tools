import numpy as np
from scipy.stats import kurtosis
from scipy.stats import skew

def get_temp_feats(temp,fs=4):
	feats=np.empty((10))
	
	feats[0]=np.mean(temp)
	
	feats[1]=np.mean(np.diff(temp))
	
	feats[2]=np.std(temp)
	
	feats[3]=np.max(temp)-np.min(temp)
	
	feats[4]=np.max(temp)
	
	feats[5]=np.min(temp)
	
	feats[6]=skew(temp)
	
	feats[7]=kurtosis(temp)
	
	temp=(temp-np.mean(temp))/np.std(temp)
	# Get real amplitudes of FFT (only in postive frequencies)
	fft_vals = np.absolute(np.fft.rfft(temp))
	fft_vals=fft_vals/np.sum(fft_vals)
	
	# Get frequencies for amplitudes in Hz
	fft_freq = np.fft.rfftfreq(len(temp), 1.0/fs)
	
	feats[8]=np.sum(fft_vals[np.where((fft_freq>0) & (fft_freq<=0.1))])
	
	feats[9]=np.sum(fft_vals[np.where((fft_freq>0.1) & (fft_freq<=0.2))])
	
	return feats
	


def get_temp_fnms():
	fnms=['mn','mn_der','std','rng','max','min','skew','kurt','pwr_0_0.1','pwr_0.1_0.2']
	return fnms


