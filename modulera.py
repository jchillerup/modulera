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
number_of_channels = 1
number_of_frames_per_nibble = 500
compression_type = "NONE"
compression_name = "not compressed"

outfile.setparams((number_of_channels, sample_width, framerate, number_of_frames_per_nibble, compression_type, compression_name))

base_scale = [369.994, 415.305, 466.164, 554.365, 622.254,] # F# major pentatonic

scale = [0]

for multiplier in [1, 2, 4]:
    for tone in base_scale:
        scale.append(multiplier*tone)

# Make the signal and write it to the file
count = 0
while True:
    count += 1
    byte = infile.read(1)
    if not byte:
        break

    nibble1 = ((ord(byte) & 0xF0) >> 4)
    nibble2 = (ord(byte) & 0x0F)
    
    #for nibble in [((ord(byte) & 0xF0) >> 4), (ord(byte) & 0x0F)]:
        #print nibble
    for i in range(number_of_frames_per_nibble):
        frequencies = [scale[nibble1], scale[nibble2]] # add more frequencies for polyphony

        frame = 0
        for frequency in frequencies:
            frame += math.sin( 2 * math.pi * frequency * (i/framerate))

            frame /= len(frequencies) # normalize
        
            outfile.writeframes(struct.pack('h', frame * amplitude/2))

    sys.stdout.write("Byte count: %s\r" % count)


outfile.close()
infile.close()
