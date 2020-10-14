function [phase,tone]=process_gsr(gsr_in)
%%
% Filter to extract phasic and tonic component from the GSR signal
% Input: raw GSR signal
% Output: phasic and tonic signal component
%%
fs_gsr=4;
%need separation of phasic and tonic components
phase=bpfilt(gsr_in,fs_gsr,10^-1,1,1.5,0);
tone=gsr_in-phase;
end