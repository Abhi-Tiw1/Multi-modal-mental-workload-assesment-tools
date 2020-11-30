# Multi-modal mental workload assessment signal processing
-------
This repository contains code for processing and feature extraction from physiological multimodal signals as done in the paper titled "Movement Artifact-Robust Mental Workload Assessment During Physical Activity Using Multi-Sensor Fusion" presented at SMC 2020

## Pre-processing codes 
These are implemented in matlab. 
Signals used: breathing, electrocardiogram, , blood volume pulse, galvanic skin reponse and temparature. 

**Breathing**:
- Device used for data collection: Bioharness 3
- Downsampling of data from 18Hz to 6Hz
- Low-pass filtering (< 2Hz) using IIR filter

**Electrocardiogram (ECG)**
- Device used for data collection: Bioharness 3
- Band-pass filtering (5Hz-25Hz) using 5th order IIR filter
- RR series extraction using energy based QRS detection algorithm (using mhrv toolbox)

**Blood Volume Pulse (BVP)**
- Data collected using empatica E4 
- Band-pass filrering (8Hz-30Hz) using 5th order IIR filter

**Galvanic Skin Response (GSR)**
- Data collected using empatica E4 
- Downsampling to 4Hz
- This was followed by separation of phasic and tonic components 
- Done using a band-pass filter (0.1Hz-1Hz) using 5th order IIR filter

**Skin Temparature**
- Data collected using empatica E4
- High frequency noise removed by low pass filter (0-0.1Hz) with 40th order FIR filter
- This was followed by removing outliers using winsorization 

## Feature extraction
Feature extraction codes are implemented in Python. The features were extracted over 60 second windows with 45 second overlap
Common feature sets:
- Descriptive features over time series extracted were: mean, standard deviations, mean of 1st difference, min, max, skewness, kurtosis
- Spectral features in the form of spectral band energies (equally spaced) over different bands were extracted. 
These features were extracted for blood volume pulse, galvanic skin response, skin temparature. Similar features were extracted for breathing with added features of breathing rate, spectral ratio and centroids.

Finally, for RR series derived from the ECG signal, standard time and frequency domain features were used.

## Dataset
The dataset is now publicaly avalible with a dataset paper:
- Albuquerque, Isabela, Abhishek Tiwari, Mark Parent, Jean-François Gagnon, Daniel Lafond, Sebastien Tremblay, and Tiago Henrique Falk. "WAUC: A Multi-Modal Database for Mental Workload Assessment under Physical Activity." Frontiers in Neuroscience 14 (2020): 1037.

## Note on EEG processing
I have not included the EEG processing pipeline codes as I used a colleagues pipeline. The general EEG features extraction and analysis pipeline was:
- wavelet ICA was used to clean the data
- This was followed by band decomposition in the standard δ, θ, α, β, and γ1 bands.
- Band powers from the various bands was used as a features


