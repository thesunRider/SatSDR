## SatSDR

Hardware:
- RPI Pico 2 - Rp2350
- Si5351 Clock source
- MC1496/Ne612 mixer


## Satellite Info

Meteor M2 - N4 
Meteor M2 - N3

M2 - N4 is preffered as it is operational and has a higher strength antenna compared to N3 where the antenna deployment didnt happen properly.

Mode : LRPT
Bitrate: 72k/80k
Modulation: QPSK / OQPSK (Offset QPSK)
Typical LRPT Bandwidth needed by SDR: 150Khz
Frequency of operation: 137.9MHz


Details about Meteor satellites: https://usradioguy.com/meteor-satellite/ (view changelogs here too)
Track satellites using: https://www.n2yo.com/satellite/?s=59051


The parameters from below are verified from reddit users (especially frequency and bitrate has been verified from reddit comments to be working)

| Parameter     | Meteor M 2-3 / General | Meteor M 2-4        |
|--------------|------------------------|---------------------|
| Frequency    | 137.900 MHz            | 137.9 MHz           |
| Symbol Rate  | 72 K                   | 72 K                |
| LRPT Status  | Active                 | Active              |
| HRPT Status  | Active on 1700 MHz     | Active on 1700 MHz  |
| APID 64      | ON                     | ON                  |
| APID 65      | ON                     | ON                  |
| APID 66      | OFF                    | OFF                 |
| APID 67      | ON                     | ON                  |
| APID 68      | OFF                    | OFF                 |
| APID 69      | OFF                    | OFF                 |
| MODE         | 124 mode               | 123 mode			  |


## Architecture
Ability to configure the frequency if needed - Currently configured for Meteor, need to make switchable components to make it work for 144 Mhz Nasa downlink too.

Clock1 : 250/2 = 125Mhz
Clock2 : 250/19 = 13.15Mhz, 14.3Mhz
		 250/20 = 12.5Mhz, 13.7Mhz
		 250/21 = 11.9Mhz, 13.1Mhz

Signal is: 137.8Mhz to 138Mhz
Hence frequency coverage is:
13.15Mhz: 138.15Mhz, 139.35Mhz
12.5Mhz:  137.5Mhz , 138.7Mhz
11.9Mhz:  136.9Mhz , 138.1Mhz

Bw: 1.2Mhz
Mix1: 137.9Mhz  - 125Mhz = 12.9Mhz
Mix2: 12.9Mhz - 12.5Mhz


									             ----LPF (1st order LC - 130Mhz) --LO (Si5351 130Mhz)
												 |
Antenna (137.9Mhz) - BPF (137-138.5Mhz) - LNA - MIXER - BPF(7-9Mhz) - Kiss Mixer - LNA - LPF - ADC (1Mhz) 
																			|
																			----- LPF (1st order LC - 10Mhz) --- LO (Si5351 8Mhz)

A demo test on Gnuradio will be done before making the hardware

The architecture is built so that each stage in the above shown figure is modular and built on seperate perfboards and interconnected using sma cables, so as to allow maximum portability and interchangability ( I dont know if this is the best choice ,but this is what I have ;-) )

## Hardware Design Choices

Below listed is why I chose these hardwares:


### Antenna
Simple V - dipole (matched with NanoVNA for minimal SWR at target Band)
Dipole given here:
BW Measured:
SWR Meaured:

### BPF 
A simple LC third order Bandpass filter, tuned with nano VNA
Reference from:

https://github.com/cernohorsky/137MHz-BandPassFilter

Bandwidth Measured:
Insertion Loss Measured:


### Mixer

There are two mixer choices, either use MC1496 and drive it asa mixer or use a simple ne612 I has as a mixer.Since MC1496 is still available in production I decided to givce it a try and it is cheaper and more available than the NE/SA612 ic's.If it is too hassle I will go back to MC1496 based designs

##### Mc1496
Double balanced mixer or Product detector design
Reference of mixer from: https://www.qsl.net/va3iul/1496_HDR_20m_TRX/1496_HDR_20m_TRX.htm

Tried simulation



#### NE612


### RPI Pico

Driving Si5351
Driving i2c for oled
saving to sdcard if needed
knob for frequency adjustment
Clock speed 250Mhz
Ethernet using libpico100basetx
USB comms
PWM based if needed for audio out
small HF transmitter/reciever

ADC cycle speed: 1 sample /96 clock
defaults to usb clock: 48Mhz, change to sys clock: 250Mhz
New adc speed: 2.6Ms/s
Bandwidth: 1.3Mhz Usable: 1.1Ms/s easily tranmsittable through libpicobase100tx


## Reference

Amplifier and Mixer - https://www.n6qw.com/MC1496.html
Double balacned kiss mixer - https://www.vk2sja.org/piffle/2014/10/10/mixer-melodies-kiss-kiss-v2-and-double-kiss/


https://github.com/carlk3/no-OS-FatFS-SD-SDIO-SPI-RPi-Pico

We can save to sdcard instead of dummping to PC

Metero m2 sample: https://chaospixel.com/pub/rtlsdr/gqrx_meteor/samples/
Sample data details: https://blog.chaospixel.com/linux/2019/12/receive-meteor-satellite-images-with-rtlsdr-gqrx-linux.html