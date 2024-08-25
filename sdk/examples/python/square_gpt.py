import ctypes

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
pps = 64000                         # Points per second, this utilizes persistence of vision. slow this down to watch the frame be drawn.
side_length = 0xFFF // 2            # Length of each side of the square
center_x = 0xFFF // 2               # Center of the square (x)
center_y = 0xFFF // 2               # Center of the square (y)
animationFrames = 1            # Only one frame needed for a static circle
totalFramesToPlay = 100        # Number of times to repeat the circle display

# Calculate corner positions
half_side = side_length // 2
top_left = (center_x - half_side, center_y + half_side)
top_right = (center_x + half_side, center_y + half_side)
bottom_right = (center_x + half_side, center_y - half_side)
bottom_left = (center_x - half_side, center_y - half_side)

# Create a frame
frameType = HeliosPoint * framePointLength
square_frame = frameType()

# Divide the points equally among the square's edges
points_per_edge = framePointLength // 4

# Draw the top edge (left to right)
for i in range(points_per_edge):
    t = i / points_per_edge
    x = int(top_left[0] + t * (top_right[0] - top_left[0]))
    y = int(top_left[1])
    square_frame[i] = HeliosPoint(x, y, 255, 255, 255, 255)

# Draw the right edge (top to bottom)
for i in range(points_per_edge):
    t = i / points_per_edge
    x = int(top_right[0])
    y = int(top_right[1] - t * (top_right[1] - bottom_right[1]))
    square_frame[points_per_edge + i] = HeliosPoint(x, y, 255, 255, 255, 255)

# Draw the bottom edge (right to left)
for i in range(points_per_edge):
    t = i / points_per_edge
    x = int(bottom_right[0] - t * (bottom_right[0] - bottom_left[0]))
    y = int(bottom_right[1])
    square_frame[2 * points_per_edge + i] = HeliosPoint(x, y, 255, 255, 255, 255)

# Draw the left edge (bottom to top)
for i in range(points_per_edge):
    t = i / points_per_edge
    x = int(bottom_left[0])
    y = int(bottom_left[1] + t * (top_left[1] - bottom_left[1]))
    square_frame[3 * points_per_edge + i] = HeliosPoint(x, y, 255, 255, 255, 255)

# Play the frame on the DAC
for _ in range(totalFramesToPlay):
    for j in range(numDevices):
        statusAttempts = 0
        while (statusAttempts < 512 and HeliosLib.GetStatus(j) != 1):
            statusAttempts += 1
        HeliosLib.WriteFrame(j, pps, 0, ctypes.pointer(square_frame), framePointLength)

# Close the DAC connection
HeliosLib.CloseDevices()
