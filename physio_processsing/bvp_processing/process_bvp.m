function bvp_out=process_bvp(bvp_in)
%%
% BVP processing code: filters signal between 0.5-8Hz
%%
%bandpass filtering
bvp_out=bpfilt(bvp_in,64,0.5,8,30,0);

end