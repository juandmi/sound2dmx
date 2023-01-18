import time
import sys, ftd2xx as ftd2xx

# Variables
OP = 0x01            # Bit mask for output D0
dmx_data = [0xfe if i in [1,2,3] else 0x00 for i in range(512)]

# define variable for DMX stop bit
dmx_stop = 0x00

# print status function
def print_status(function, status):
    if status == 0:  # FT_OK
        print(f'{function} OK')
    else:
        print(f'{function} failed')
        print(f'{function} error code = {status}')
        exit()

d = ftd2xx.open(0)    # Open first FTDI device
print(d.getDeviceInfo())

# Set the baud rate
print(d.setBaudRate(250000))

# Set the data characteristics
print(d.setDataCharacteristics(8, 0, 0))

# Set the timeout
print(d.setTimeouts(5000, 1000))

# Set the flow control
print(d.setFlowControl(0, 0, 0))

# Get the status of the device
print(d.getStatus())

t_end = time.time() + 1
while time.time() < t_end:
    # Set the break condition
    status = ftd2xx.FT_SetBreakOn(ft_handle)
    print_status("FT_SetBreakOn",status)
    time.sleep(0.088)  # delay 88ms

    status = ftd2xx.FT_SetBreakOff(ft_handle)
    print_status("FT_SetBreakOff",status)

    # Set the mark-after-break
    time.sleep(0.008)  # delay 8ms

    # Write the start code
    status = ftd2xx.FT_Write(ft_handle, "0x00", 1, ctypes.byref(bytes_written))
    print_status("FT_Write_Start",status)
    print(f'{bytes_written.value} status bytes written')

    # Write the DMX data 
    status = ftd2xx.FT_Write(ft_handle, dmx_data, ctypes.c_ulong(len(dmx_data)), ctypes.byref(bytes_written))
    print_status("FT_Write_Data",status)
    print(f'{bytes_written.value} bytes written')
    time.sleep(0.024)  # delay 24ms

# print dmx_data
print(dmx_data)

# Close the device
print(d.close())