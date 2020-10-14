function [temp_lf,temp_hf]=process_temp(temp_in)
%%
% Code to process temparature signal
% First winsorization is performed with the range 1% to 99%
% Following this a low pass filtering operation is performed
% Input: raw temparature signal
% Output: processed temp signal, high freq component of temparature signal
%%
temp_out=winsor(temp_in,[1,99]);

%create a low frequency component
%ma_f = ones(1, 200)/200;

b=fir1(40,0.01,'low',chebwin(41,30));
%learn applying a low pass filter properly
temp_lf = filtfilt(b, 1, temp_out);

temp_hf=temp_out-temp_lf;

end