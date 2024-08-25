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
framePointLength = 1000             # Number of points in the frame
pps = 64000                         # Points per second
radius = 0xFFF // 10                # Radius of the basketball
center_x = 0xFFF // 2               # Center of the circle (x)
ground_y = radius                   # Y position for the ground (minimum y for the ball)
ceiling_y = 0xFFF - radius          # Y position for the ceiling (maximum y for the ball)
gravity = -1                   # Gravity effect (negative for downward motion)
bounce_factor = -0.8                # Bounce factor (negative to reverse direction, <1 for energy loss)
frames_per_bounce = 50              # Number of frames for one bounce
totalFramesToPlay = 300             # Total number of frames for the entire animation

# Create the frames for bouncing animation
frames = []
for i in range(totalFramesToPlay):
    frameType = HeliosPoint * framePointLength
    frame = frameType()

    # Calculate the ball's position using simple physics
    time_step = (i % frames_per_bounce) / frames_per_bounce
    velocity_y = math.sqrt(-2 * gravity * (ceiling_y - ground_y))  # Initial upward velocity for a bounce
    y = ceiling_y + (velocity_y * time_step + 0.5 * gravity * time_step**2) * (1 if time_step < 0.5 else -1)

    if y < ground_y:
        y = ground_y
        velocity_y *= bounce_factor

    # Draw the basketball as a circle
    for j in range(framePointLength):
        angle = (2 * math.pi * j) / framePointLength
        x = center_x + int(radius * math.cos(angle))
        y_point = int(y + radius * math.sin(angle))
        frame[j] = HeliosPoint(x, y_point, 255, 165, 0, 255)  # Orange color with full intensity

    frames.append(frame)

# Play the frames on the DAC
for i in range(totalFramesToPlay):
    for j in range(numDevices):
        statusAttempts = 0
        while (statusAttempts < 512 and HeliosLib.GetStatus(j) != 1):
            statusAttempts += 1
            time.sleep(0.001)  # Small delay to avoid busy-waiting
        HeliosLib.WriteFrame(j, pps, 0, ctypes.pointer(frames[i % len(frames)]), framePointLength)

# Close the DAC connection
HeliosLib.CloseDevices()
