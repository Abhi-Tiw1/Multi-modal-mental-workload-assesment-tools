function [rri,tm]=get_rr_values(ecg_,fs_ecg)
%%
% Requirement: mhrv toolbox --> functions alrready added: 
%  - Codes used from the mhrv toolbox: filtrr, load_mhrv_defaults, jqrs
% Code extracts RR series (using energy based QRS detector) from from ECG signal along with filtering of the
% RR signal, this is done using the mhrv toolbox in matlab
%
% Input: Raw ECG signal
% Output: rr series, timestamps of rr values
%%

tm = 1/fs_ecg:1/fs_ecg:length(ecg_)/fs_ecg;
ecg_=ecg_';

qrs_pos=jqrs(ecg_,fs_ecg,0.4,0.250,0);
rri=diff(qrs_pos)/fs_ecg;
mhrv_load_defaults()

tm=tm(qrs_pos(1:end-1));
[rri,tm]=filtrr(rri,tm);
rri=rri*1000;

end