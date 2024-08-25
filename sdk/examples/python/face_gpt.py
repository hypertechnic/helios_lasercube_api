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
center_x = 0xFFF // 2               # Center of the face (x)
center_y = 0xFFF // 2               # Center of the face (y)
radius = 0xFFF // 4                 # Radius for the face outline

# Create a frame
frameType = HeliosPoint * framePointLength
face_frame = frameType()

# Function to draw a circle (used for face outline and eyes)
def draw_circle(center_x, center_y, radius, start_index, color=(255, 255, 255)):
    for i in range(framePointLength // 6):  # Divide points for multiple features
        angle = (2 * math.pi * i) / (framePointLength // 6)
        x = center_x + int(radius * math.cos(angle))
        y = center_y + int(radius * math.sin(angle))
        face_frame[start_index + i] = HeliosPoint(x, y, color[0], color[1], color[2], 255)

# Draw the face outline
draw_circle(center_x, center_y, radius, 0)

# Draw the left eye
left_eye_x = center_x - radius // 2
left_eye_y = center_y + radius // 4
eye_radius = radius // 8
draw_circle(left_eye_x, left_eye_y, eye_radius, framePointLength // 6)

# Draw the right eye
right_eye_x = center_x + radius // 2
right_eye_y = center_y + radius // 4
draw_circle(right_eye_x, right_eye_y, eye_radius, framePointLength // 3)

# Draw the nose (as a simple triangle)
nose_height = radius // 3
for i in range(framePointLength // 6):
    t = i / (framePointLength // 6)
    x = int(center_x + (1 - t) * (-eye_radius) + t * eye_radius)
    y = int(center_y - t * nose_height)
    face_frame[framePointLength // 2 + i] = HeliosPoint(x, y, 255, 255, 255, 255)

# Draw the mouth (as a simple curve)
mouth_width = radius // 2
mouth_height = radius // 8
for i in range(framePointLength // 6):
    t = (i / (framePointLength // 6)) * math.pi
    x = int(center_x + mouth_width * (i / (framePointLength // 6)) - mouth_width // 2)
    y = int(center_y - radius // 3 - mouth_height * math.sin(t))
    face_frame[2 * framePointLength // 3 + i] = HeliosPoint(x, y, 255, 255, 255, 255)

# Play the frame on the DAC
for j in range(numDevices):
    statusAttempts = 0
    while (statusAttempts < 512 and HeliosLib.GetStatus(j) != 1):
        statusAttempts += 1
    HeliosLib.WriteFrame(j, pps, 0, ctypes.pointer(face_frame), framePointLength)

# Close the DAC connection
HeliosLib.CloseDevices()
