"Joes Version"

# -*- coding: utf-8 -*-
"""
Example for using Helios DAC libraries in python (using C library with ctypes)

NB: If you haven't set up udev rules you need to use sudo to run the program for it to detect the DAC.
"""




xRes = 500
animationFrames = 50
framePointLength = 1000                                          #1000, cant be less than 1000, seems like buffer max pps
vSteps = 50                                                        #30, also steps. Should match animationFrames for a full height.
animationLoops = 1
totalFramesToPlay = animationFrames * animationLoops               #compare to animationFrames to push more than 1 loop
pps = 64000                                                     #30000, speed to push to driver, 64000 is fastest


det_top = 500
det_bottom = 200
det_right = 600
det_left = 200



import ctypes

#Define point structure
class HeliosPoint(ctypes.Structure):
    #_pack_=1
    _fields_ = [('x', ctypes.c_uint16),
                ('y', ctypes.c_uint16),
                ('r', ctypes.c_uint8),
                ('g', ctypes.c_uint8),
                ('b', ctypes.c_uint8),
                ('i', ctypes.c_uint8)]

#Load and initialize library
HeliosLib = ctypes.cdll.LoadLibrary("./libHeliosDacAPI.so")
numDevices = HeliosLib.OpenDevices()
print("Found ", numDevices, "Helios DACs")

#Create sample frames
frames = [0 for x in range(animationFrames)]
frameType = HeliosPoint * framePointLength   #number of points in frame, each of [x, y, r, g, b, i]
x = 0
y = 0


#below is draw a left/right/left line of resolution framePoint length, which steps up a the full height in vStep quantized steps
for i in range(animationFrames):                            #index the animation Frames
    y = round(i * 0xFFF / vSteps)                             #y is converting 4095 into 30 slots from above. this is only time y is written on frame!
    frames[i] = frameType()                                 #for this frame within the animation, give it framePointLength points to play with
    for j in range(framePointLength):     #1000                              #go through each of the points in the single frame
        if (j < (xRes/2)):  #500                                 #count of the total frame length to use for x
            x = round(j * 0xFFF / (xRes/2))   # /500             # per each of the incoming X indexes, move over by 1 resolution of Y
        else:
            x = round(0xFFF - ((j - (xRes/2)) * 0xFFF / (xRes/2)))   #if past half the incoming bitstream, go reverse

        frames[i][j] = HeliosPoint(int(x),int(y),10,0,0,10)        #single point color and intensity assigned to i= frame of animation, j = ID of framePoint within the stream

#Play frames on DAC
for i in range(round(totalFramesToPlay)):
    for j in range(numDevices):
        statusAttempts = 0
        # Make 512 attempts for DAC status to be ready. After that, just give up and try to write the frame anyway
        while (statusAttempts < 512 and HeliosLib.GetStatus(j) != 1):
            statusAttempts += 1
        HeliosLib.WriteFrame(j, pps, 0, ctypes.pointer(frames[i % animationFrames]), framePointLength) #Send the frame, last var was 1000
        
HeliosLib.CloseDevices()
