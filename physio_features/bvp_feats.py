import numpy as np
import matplotlib.pyplot as plt

def get_pwr_bnd_name(bnd):
	_str='pwr_'
	nms=[]
	for ix in range(len(bnd)-1):
		flo=bnd[ix]
		fhi=bnd[ix+1]
		nms.append(_str+str(flo)+'_'+str(fhi))
	
	return nms

def get_band_energy(fft_vals,fft_freq,rngs):
	
	band_no=len(rngs)-1
	band_pwr = np.zeros(band_no)
	
	for i in range(0,band_no):
		flo=rngs[i]
		fhi=rngs[i+1]
		freq_ix = np.where((fft_freq >= flo) & 
						   (fft_freq <= fhi))[0]
		band_pwr[i] = np.mean(fft_vals[freq_ix]*fft_vals[freq_ix])
	
	return band_pwr 

def get_energy_ratio_bvp(fft_vals,fft_freq,rat):
	rat_vals=np.zeros((2))
	for ix,r in enumerate(rat):
		flo=r[0]
		fhi=r[1]
		freq_ix = np.where((fft_freq >= flo) & (fft_freq <= fhi))[0]
		rat_vals[ix] = np.mean(fft_vals[freq_ix]*fft_vals[freq_ix])
	
	ratio=rat_vals[1]/rat_vals[0]
	
	if np.isnan(rat_vals[1]/rat_vals[0]):
		ratio=0
	return ratio

def get_bvp_feats(bvp,fs=64):
	feats_bvp=np.zeros((6))
	
	bvp=(bvp-np.mean(bvp))/np.std(bvp)
	fft_vals = np.absolute(np.fft.rfft(bvp))
	fft_vals=fft_vals/np.sum(fft_vals)
	
	# Get frequencies for amplitudes in Hz
	fft_freq = np.fft.rfftfreq(len(bvp), 1.0/fs)
	
	#0-2.5 Hz divided in five bands
	bnd_rngs=np.linspace(0,2.5,5+1)
	feats_bvp[:5]=get_band_energy(fft_vals,fft_freq,bnd_rngs)
	
	ratio=[[0.04,0.15],[0.15,0.5]]
	feats_bvp[5]=get_energy_ratio_bvp(fft_vals,fft_freq,ratio)
	
	return feats_bvp


def get_bvp_fnms():
	bnd=np.linspace(0,2.5,5+1)
	f1=get_pwr_bnd_name(bnd)
	f2=['ener_ratio']
	return f1+f2
	
