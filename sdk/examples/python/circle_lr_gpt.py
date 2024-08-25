import ctypes
import math

# Define point structure for Helios DAC
class HeliosPoint(ctypes.Structure):
    _fields_ = [('x', ctypes.c_uint16),
                ('y', ctypes.c_uint16),
                ('r', ctypes.c_uint8),
                ('g', ctypes.c_uint8),
                ('b', ctypes.c_uint8),
                ('i', ctypes.c_uint8)]

# Load and initialize Helios DAC library
HeliosLib = ctypes.cdll.LoadLibrary("./libHeliosDacAPI.so")
numDevices = HeliosLib.OpenDevices()
print("Found ", numDevices, "Helios DACs")

# Parameters
framePointLength = 1000             # Number of points in the frame
pps = 64000                         # Points per second
radius = 0xFFF // 10                # Radius of the circle
framesCount = 100                   # Number of frames in the animation
start_x = 0xFFF // 10               # Starting x position (left side)
end_x = 0xFFF - start_x             # Ending x position (right side)
center_y = 0xFFF // 2               # y position (centered vertically)

# Create frames for the moving circle
frames = []
for i in range(framesCount):
    frameType = HeliosPoint * framePointLength
    circle_frame = frameType()

    # Calculate the x position for this frame
    t = i / (framesCount - 1)
    center_x = int(start_x + t * (end_x - start_x))

    # Draw the circle for this frame
    for j in range(framePointLength):
        angle = (2 * math.pi * j) / framePointLength
        x = center_x + int(radius * math.cos(angle))
        y = center_y + int(radius * math.sin(angle))
        circle_frame[j] = HeliosPoint(x, y, 255, 255, 255, 255)

    frames.append(circle_frame)

# Play the frames on the DAC
for i in range(framesCount):
    for j in range(numDevices):
        statusAttempts = 0
        while (statusAttempts < 512 and HeliosLib.GetStatus(j) != 1):
            statusAttempts += 1
        HeliosLib.WriteFrame(j, pps, 0, ctypes.pointer(frames[i]), framePointLength)

# Close the DAC connection
HeliosLib.CloseDevices()
