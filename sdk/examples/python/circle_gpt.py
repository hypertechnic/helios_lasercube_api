import ctypes
import math
import time

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
xRes = 1000                    # Horizontal resolution
framePointLength = 1000        # Number of points in the frame
pps = 64000                    # Points per second
radius = 0xFFF // 4            # Radius of the circle (1/4th of the maximum value for DAC)
center_x = 0xFFF // 2          # Center of the circle (x)
center_y = 0xFFF // 2          # Center of the circle (y)
animationFrames = 1            # Only one frame needed for a static circle
totalFramesToPlay = 100        # Number of times to repeat the circle display

# Create the frame
frameType = HeliosPoint * framePointLength
circle_frame = frameType()

# Calculate the points for a circle
for i in range(framePointLength):
    angle = (2 * math.pi * i) / framePointLength  # Divide the circle into equal segments
    x = center_x + int(radius * math.cos(angle))
    y = center_y + int(radius * math.sin(angle))
    circle_frame[i] = HeliosPoint(x, y, 255, 0, 0, 255)  # Red color with full intensity

# Play the circle frame on the DAC
for _ in range(totalFramesToPlay):
    for j in range(numDevices):
        statusAttempts = 0
        while (statusAttempts < 512 and HeliosLib.GetStatus(j) != 1):
            statusAttempts += 1
            time.sleep(0.001)  # Small delay to avoid busy-waiting
        HeliosLib.WriteFrame(j, pps, 0, ctypes.pointer(circle_frame), framePointLength)

# Close the DAC connection
HeliosLib.CloseDevices()
