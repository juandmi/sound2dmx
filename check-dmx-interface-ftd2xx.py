import time
import sys, ftd2xx as ftd2xx

# Variables
dmx_data = [0x00,0xFF,0xFF,0xFF,0x80]
dmx_data = bytes(dmx_data)

d = ftd2xx.open(0)    # Open first FTDI device
print(d.getDeviceInfo())

# Set the baud rate
d.setBaudRate(250000)

# Set the data characteristics
d.setDataCharacteristics(8, 2, 0)

# Set the timeout
d.setTimeouts(5000, 1000)

# Set the flow control
d.setFlowControl(0, 0, 0)

# print the latency timer
start = time.time()
seconds = time.time()
print("time before breaks=", (seconds - start)*1000)

# Set the break condition
d.setBreakOn()
time.sleep(0.010) # delay 10ms
seconds = time.time()
print("time after breaks on=", (seconds - start)*1000)
d.setBreakOff()
# Set the mark-after-break
time.sleep(0.000008)  # delay 8usec
seconds = time.time()
print("time after breaks off=", (seconds - start)*1000)

i = 0
# Now continously send the slot 1 to 512 DMX data 
t_end = time.time() + 1
while time.time() < t_end:
    # Write the start bit
    d.write(b"\x00")
    n = d.write(dmx_data)
    print("bytes written =",n)
    # print time after dmx data sent and i
    i += 1
    seconds = time.time()
    print("time after dmx data sent=",i ," ", (seconds - start)*1000)

# print dmx_data
print(dmx_data)

# Close the device
d.close()