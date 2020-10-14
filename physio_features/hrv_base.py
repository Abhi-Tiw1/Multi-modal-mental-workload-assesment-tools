import numpy as np
from scipy import stats
#from pyentrp import entropy as ent
#import nolds
from scipy import signal
#from am_analysis import am_analysis as ama
#from hrv.classical import frequency_domain  #Adding in VERSION 1.1
from scipy.signal import welch
from spectrum import pburg
from scipy import interpolate
import scipy.fftpack as fftpack

'''
Description
% hrv0--> mean RR
% hrv1 --> sdRR
% hrv2---> Coeffcient of Variation
% hrv3--> rmsdd
% hrv4--> pNN50
% hrv5--> mean of first differences
% hrv6--> std of absolute first differences
% hrv7--> mean of absolute first differences (Normalized)
%Assuming input RR series is in msec scale (for pNN50 calculation)
'''
def time_domain_hrv(rr):
	hrv=np.zeros([8])

	hrv[0]=np.mean(rr)

	hrv[1]=np.std(rr)

	hrv[2]=hrv[1]/hrv[0]
	
	norm_rr=(rr-hrv[0])/hrv[1]

	first_diff_norm=np.diff(norm_rr)
	first_diff=np.diff(rr)

	#for i in range(1,len(rr)):
		#first_diff[i-1]=rr[i]-rr[i-1]
		#first_diff_norm[i-1]=norm_rr[i]-norm_rr[i-1]

	
	abs_first_diff=abs(first_diff)
	abs_first_diff_norm=abs(first_diff_norm)
	
	
	hrv[3]=np.sqrt(np.mean(first_diff**2))

	hrv[4]=np.sum((abs_first_diff>50)*1)*100/len(abs_first_diff)

	hrv[5]=np.mean(first_diff)

	hrv[6]=np.std(abs_first_diff)

	hrv[7]=np.mean(abs_first_diff_norm)

	return hrv

	
'''
Requires pyentrp and nolds package for calculation

Feature Description
hrv0 --> Sample Entropy
hrv1 --> Shannon Entropy
hrv2 --> Approximate Entropy
hrv3 --> Permutation Entropy
hrv4 ---> Correlation Dimension
hrv5 --> Modified Permutation Entropy
NOT IMPLEMENTED YET
hrv6 --> LLE
hrv7 --> Detrend Fluctuation Analysis
'''

def non_linear_hrv(rr,lag):
	rr_std=np.std(rr)
	rval=0.2*rr_std
	hrv=np.zeros([1])
	
	#hrv[0]=nolds.sampen(rr,emb_dim=3,tolerance=rval)

	#hrv[0]=ent.shannon_entropy(rr)

	#hrv[2]=ApEn(rr,3,rval)

	#hrv[1]=ent.permutation_entropy(rr,3,lag)
	
	#hrv[2]=nolds.corr_dim(rr,3)

	#hrv[2]=mod_pe(rr,3,lag)

	#hrv[6]=nolds.lyap_r(rr)
	
	#hrv[7]=nolds.dfa(rr)

	return hrv




def freq_domain_hrv(rri,tm,fs=4):
	rri=rri[np.where(rri>0)]

	freq_feat = frequency_domain(rri=rri,time=tm,fs=fs,method='welch',interp_method='cubic',detrend='linear') #
	feats=np.array(list(freq_feat.values())) 

	return feats
	

def frequency_domain(rri, time=None, fs=4.0, method='welch',
					 interp_method='cubic', vlf_band=(0, 0.04),
					 lf_band=(0.04, 0.15), hf_band=(0.15, 0.4), **kwargs):

	if time is None:
		print('Need time in the hacked version')
		exit()
		
	#normalizes the signal - mean 0 std 1
	rri=signal.detrend(rri, axis=-1)


	if interp_method is not None:
		rri = _interpolate_rri(rri, time, fs, interp_method)
	

	"""
	#plotting the spectrum of RR series
	# Number of samplepoints
	N = len(rri)
	# sample spacing
	T = 1.0 / 4.0
	x = np.linspace(0.0, N*T, N)
	xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
	yf = fftpack.fft(rri)
	plt.plot(xf, 2.0/N * np.abs(yf[:N//2]))
	plt.show()
	"""
	
	if method == 'welch':
		fxx, pxx = welch(x=rri, fs=fs, **kwargs)
	elif method == 'ar':
		fxx, pxx = _calc_pburg_psd(rri=rri,  fs=fs, **kwargs)

	return _auc(fxx, pxx, vlf_band, lf_band, hf_band)
	
def _auc(fxx, pxx, vlf_band, lf_band, hf_band):
	vlf_indexes = np.logical_and(fxx >= vlf_band[0], fxx < vlf_band[1])
	lf_indexes = np.logical_and(fxx >= lf_band[0], fxx < lf_band[1])
	hf_indexes = np.logical_and(fxx >= hf_band[0], fxx < hf_band[1])

	vlf = np.trapz(y=pxx[vlf_indexes], x=fxx[vlf_indexes])
	lf = np.trapz(y=pxx[lf_indexes], x=fxx[lf_indexes])
	hf = np.trapz(y=pxx[hf_indexes], x=fxx[hf_indexes])
	total_power = vlf + lf + hf
	lf_hf = lf / hf
	lfnu = (lf / (total_power - vlf)) * 100
	hfnu = (hf / (total_power - vlf)) * 100

	return dict(zip(['total_power', 'vlf', 'lf', 'hf', 'lf_hf', 'lfnu',
					'hfnu'], [total_power, vlf, lf, hf, lf_hf, lfnu, hfnu]))

def _calc_pburg_psd(rri, fs, order=16, nfft=None):
	burg = pburg(data=rri, order=order, NFFT=nfft, sampling=fs)
	burg.scale_by_freq = False
	burg()
	return np.array(burg.frequencies()), burg.psd
	
def _interpolate_rri(rri, time, fs=4, interp_method='cubic'):
	if interp_method == 'cubic':
		return _interp_cubic_spline(rri, time, fs)
	elif interp_method == 'linear':
		return _interp_linear(rri, time, fs)


def _interp_cubic_spline(rri, time, fs):
	time_rri_interp = _create_interp_time(time, fs)
	tck = interpolate.splrep(time, rri, s=0)
	rri_interp = interpolate.splev(time_rri_interp, tck, der=0)
	
	#Interpolated periodogram and original heart rate series
	#plt.plot(time,rri)
	#plt.plot(time_rri_interp,rri_interp)
	#plt.show()
	
	return rri_interp


def _interp_linear(rri, time, fs):
	time_rri_interp = _create_interp_time(time, fs)
	rri_interp = np.interp(time_rri_interp, time, rri)

	return rri_interp
	
def _create_interp_time(time, fs):
	time_resolution = 1 / float(fs)
	return np.arange(0, time[-1] + time_resolution, time_resolution)

def get_time_fname():
	nm_time=['meanRR','sdRR','Coef_Var','rmsdd','pNN50','mn_1st_diff','std_abs_1st_diff','mn_abs_1st_diff_norm']
	
	return nm_time
	

def get_freq_fname(func=0):
	nm_freq=['total_f','vlf','lf','hf','lf_hf','lfnu','hfnu']
	
	return nm_freq

def get_hrv_fnms():
	f1=get_time_fname()
	f2=get_freq_fname()
	
	return f1+f2

def get_hrv_feats(rr,tm,fs):
	f1=time_domain_hrv(rr)
	f2=freq_domain_hrv(rr,tm,fs=4)
	ft=np.hstack((f1,f2))
	return ft
