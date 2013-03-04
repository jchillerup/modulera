#!/usr/bin/python2

import sys, wave, math, struct

if len(sys.argv) != 2:
    print "Not enough arguments"
    sys.exit()

infile = open(sys.argv[1], 'rb')
outfile = wave.open('out.wav', 'wb')

framerate = 11025.0
amplitude = 8000
sample_width = 2
number_of_channels = 2
number_of_frames_per_byte = 1000
compression_type = "NONE"
compression_name = "not compressed"

outfile.setparams((number_of_channels, sample_width, framerate, number_of_frames_per_byte, compression_type, compression_name))

base_scale = [369.994, 415.305, 466.164, 554.365, 622.254,] # F# major pentatonic

scale = [0]

for multiplier in [0.5, 1, 2]:
    for tone in base_scale:
        scale.append(multiplier*tone)

# Make the signal and write it to the file
count = 0
while True:
    count += 1
    byte = infile.read(1)
    if not byte:
        break

    high_nibble = ((ord(byte) & 0xF0) >> 4)
    low_nibble = (ord(byte) & 0x0F)

    left_multiplier  = 2*math.pi*scale[high_nibble]/framerate
    right_multiplier = 2*math.pi*scale[low_nibble]/framerate
    
    for i in range(number_of_frames_per_byte):
        waveData = ""
        
        waveData += struct.pack('h', amplitude*math.sin( left_multiplier * i))
        waveData += struct.pack('h', amplitude*math.sin( right_multiplier * i))

        outfile.writeframes(waveData)
            
    sys.stdout.write("Byte count: %s\r" % count)

sys.stdout.write("\n")
outfile.close()
infile.close()
