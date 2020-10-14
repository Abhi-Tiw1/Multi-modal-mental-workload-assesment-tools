function [rri,tm,tm_end]=process_ecg(ecg_in,fs_ecg) 
%%
% Code to process the ECG signal by doing a bandpass filter (5-25Hz) followed by RR
% detecion and filtering : added functions required: get_rr_values,
% Codes used from the mhrv toolbox: filtrr, load_mhrv_defaults, jqrs
% Input: raw ECG signal , Sampling frequency 
% Output: rr series, timestamp,  total time of signal
%%
ecg_out = (ecg_in-mean(ecg_in))./std(ecg_in);

%Band pass and notch filtering --> physiozoo
ecg_out=bpfilt(ecg_out,fs_ecg,5,25,60,0);

[rri,tm]=get_rr_values(ecg_out,fs_ecg);

ecg_out=ecg_out';

tm_end=length(ecg_out)/fs_ecg;

end