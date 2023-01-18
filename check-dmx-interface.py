import ctypes
import time

# Variables
dmx_data = [0xfe if i in [1,2,3] else 0x00 for i in range(512)]
#dmx_data = (ctypes.c_ubyte * len(dmx_data))(*dmx_data)
dmx_data = bytes(dmx_data)

bytes_written = ctypes.c_ulong()

# Declare variables to store the status
lpdwAmountInRxQueue = ctypes.c_ulong()
lpdwAmountInTxQueue = ctypes.c_ulong()
lpdwEventStatus = ctypes.c_ulong()

# print status function
def print_status(function, status):
    if status == 0:  # FT_OK
        print(f'{function} OK')
    else:
        print(f'{function} failed')
        exit()

# Declare variable for the handle
ft_handle = ctypes.c_void_p()
# Load the DLL
ftd2xx = ctypes.WinDLL("ftd2xx.dll")
# Open the device
status = ftd2xx.FT_Open(0, ctypes.byref(ft_handle))
print_status("FT_Open",status)

# Set chip modes
status = ftd2xx.FT_SetBaudRate(ft_handle, 250000)
print_status("FT_SetBaudRate",status)

# Set the data characteristics
status = ftd2xx.FT_SetDataCharacteristics(ft_handle, 8, 2, 0)
print_status("FT_SetDataCharacteristics",status)

# Set the timeout
status = ftd2xx.FT_SetTimeouts(ft_handle, 500, 0);
print_status("FT_SetTimeouts",status)

# Set the flow control
status = ftd2xx.FT_SetFlowControl(ft_handle, 0, 0, 0)
print_status("FT_SetFlowControl",status)

# Get the latency timer
latency = ctypes.c_ubyte()
status = ftd2xx.FT_GetLatencyTimer(ft_handle, ctypes.byref(latency))
print_status("FT_GetLatencyTimer",status)
print(f'Latency timer: {latency.value}')

# Get the status of the device
status = ftd2xx.FT_GetStatus(ft_handle, ctypes.byref(lpdwAmountInRxQueue), ctypes.byref(lpdwAmountInTxQueue), ctypes.byref(lpdwEventStatus))
print_status("FT_GetStatus",status)

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

# print(dmx_data)
# for val in dmx_data:
#    print(val)

# Close the device
ftd2xx.FT_Close(ft_handle)
print("Device closed")
