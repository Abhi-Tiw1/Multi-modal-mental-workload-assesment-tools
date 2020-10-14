function [br_fin,fs_br,br_ts]=process_br(br_in,br_ts)
%%
% Code to process breathing signal
% Downsample signal from 18 Hz to 6 Hz
% Low pass filtering using chebechev 2Hz, 8th order filter
% Input: raw breathing signal (Input freq=18Hz), Signal timestamps
%%
%reducing to 6 Hz instead of 4Hz
br_out=downsample(br_in,3);
br_ts=br_ts(1:3:end);
fs_br=6;
br_ts=0:1/fs_br:length(br_out)/fs_br;

%Normalization of signal
%lowpass chebechev 2Hz, 8th order filter
[b,a]=cheby1(8,10,2/3,'low');
br_fin = filter(b,a,br_out);
fs_br=6;

end