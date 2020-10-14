import numpy as np

def get_pwr_bnd_name(bnd):
	_str='pwr_'
	nms=[]
	for ix in range(len(bnd)-1):
		fhi=bnd[ix]
		flo=bnd[ix+1]
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


def get_ph_feats(sig,fs=4):
	feats=np.zeros((9))
	
	sig_spec=(sig-np.mean(sig))/np.std(sig)
	fft_vals = np.absolute(np.fft.rfft(sig_spec))
	fft_vals=fft_vals/np.sum(fft_vals)
	
	# Get frequencies for amplitudes in Hz
	fft_freq = np.fft.rfftfreq(len(sig), 1.0/fs)
	
	#0-2.5 Hz divided in five bands
	bnd_rngs=np.linspace(0,0.1,5+1)
	feats[:5]=get_band_energy(fft_vals,fft_freq,bnd_rngs)
	
	feats[5]=np.mean(sig)
	
	feats[6]=np.std(sig)
	
	feats[7]=np.mean(np.diff(sig))
	
	dif_sig=np.diff(sig)
	
	feats[8]=np.mean(dif_sig[dif_sig<0])
	
	return feats
	
def get_ph_fnms():
	bnd=np.linspace(0,0.1,5+1)
	bnd_names=get_pwr_bnd_name(bnd)
	fts=['mn','std','mn_diff','mn_diff_neg']
	
	return bnd_names+fts
