import ctypes
import time
import socket
import threading
import re
import time

lock = threading.Lock() # create a lock to prevent concurrent access to dmx_data
stop_event = threading.Event() # Create an event to signal threads to stop

# Print computer name and IP address
hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)
print("Your Computer Name is:"+hostname)
print("Your Computer IP Address is:"+IPAddr)

# Declare global variables
global dmx_data_int
dmx_data_int = [0,255,255,255,0] # DMX format: flash, red, green, blue, tilt
stopbit = 0x00
stopbit = bytes(stopbit)
bytes_written = ctypes.c_ulong()
ip = IPAddr
port = 8080

# print_handler function for OSC data received
def print_handler(address, *args):
    global dmx_data_int
    if address == "/dmx/red":
        match = re.search(r'\d+', str(args[0])) # get the first value of the first argument tuple and convert it to an integer
        if match: # if the match is not None
            value = int(match.group())
            with lock:
                dmx_data_int[1] = value # update the second element of the dmx_data list with the red value
        else:
            print(f"Invalid OSC message: {address} {args}")
    elif address == "/dmx/green":
        match = re.search(r'\d+', str(args[0])) # get the first value of the first argument tuple and convert it to an integer
        if match: # if the match is not None
            value = int(match.group())
            with lock:
                dmx_data_int[2] = value # update the third element of the dmx_data list with the green value
        else:
            print(f"Invalid OSC message: {address} {args}")
    elif address == "/dmx/blue":
        match = re.search(r'\d+', str(args[0])) 
        if match: 
            value = int(match.group())
            with lock:
                dmx_data_int[3] = value 
        else:
            print(f"Invalid OSC message: {address} {args}")
    elif address == "/dmx/tilt":
        match = re.search(r'\d+', str(args[0])) 
        if match: 
            value = int(match.group())
            with lock:
                dmx_data_int[4] = value 
        else:
            print(f"Invalid OSC message: {address} {args}")
    elif address == "/dmx/flash":
        match = re.search(r'\d+', str(args[0])) 
        if match: 
            value = int(match.group())
            with lock:
                dmx_data_int[0] = value 
        else:
            print(f"Invalid OSC message: {address} {args}")
    else:
        print(f"Unknown OSC message: {address} {args}")

# default_handler function for OSC data received, do nothing but print the message
def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")

def write_dmx_data():
    global dmx_data_int
    dmx_data = bytes(dmx_data_int)
    global running
    running = True
    # print status function
    def print_status(function, status):
        if status == 0:  # FT_OK
            print(f'{function} OK')
        else:
            print(f'{function} failed')
            exit()

    ft_handle = ctypes.c_void_p() # Declare variable for the handle
    ftd2xx = ctypes.WinDLL("ftd2xx.dll") # Load the DLL

    status = ftd2xx.FT_Open(0, ctypes.byref(ft_handle)) # Open the device
    print_status("FT_Open",status)

    status = ftd2xx.FT_SetBaudRate(ft_handle, 250000) # Set chip modes
    print_status("FT_SetBaudRate",status)

    status = ftd2xx.FT_SetDataCharacteristics(ft_handle, 8, 2, 0)     # Set the data characteristics - Data bits, Stop bits, Parity
    print_status("FT_SetDataCharacteristics",status)

    status = ftd2xx.FT_SetTimeouts(ft_handle, 500, 0) # Set the timeout
    print_status("FT_SetTimeouts",status)

    status = ftd2xx.FT_SetFlowControl(ft_handle, 0, 0, 0) # Set the flow control
    print_status("FT_SetFlowControl",status)

    latency = ctypes.c_ubyte() 
    status = ftd2xx.FT_GetLatencyTimer(ft_handle, ctypes.byref(latency)) # Get the latency timer
    print_status("FT_GetLatencyTimer",status)
    print(f'Latency timer: {latency.value}')

    # Set the break conditions
    status = ftd2xx.FT_SetBreakOn(ft_handle)
    print_status("FT_SetBreakOn",status)
    time.sleep(0.010) # delay 10ms
    status = ftd2xx.FT_SetBreakOff(ft_handle)
    print_status("FT_SetBreakOff",status)
    # Set the mark-after-break
    time.sleep(0.000008)  # delay 8usec

    try: 
        while not stop_event.is_set():
            # when dmx_data changes, send the data
            if dmx_data != bytes(dmx_data_int):
                ftd2xx.FT_SetBreakOn(ft_handle) # Set the break conditions
                time.sleep(0.010) # delay 10ms
                ftd2xx.FT_SetBreakOff(ft_handle) # Set the mark after break conditions
                time.sleep(0.000008)  # Set the mark-after-break
                with lock:
                    dmx_data = bytes(dmx_data_int) # convert the dmx_data list to bytes
                    print(f"DMX data: {dmx_data_int}")
            else:
                ftd2xx.FT_Write(ft_handle, stopbit, 1, ctypes.byref(bytes_written)) # Write the start bit
                ftd2xx.FT_Write(ft_handle, dmx_data, ctypes.c_ulong(len(dmx_data)), ctypes.byref(bytes_written))

    except KeyboardInterrupt:
        print("Stopping DMX data write.")

    print(f"DMX data: {dmx_data_int}")
    print(dmx_data)

    # Close the device
    ftd2xx.FT_Close(ft_handle)
    print("Device closed")

def main():
    from pythonosc.dispatcher import Dispatcher
    from pythonosc.osc_server import BlockingOSCUDPServer

    # start the DMX data writing thread
    dmx_thread = threading.Thread(target=write_dmx_data)
    dmx_thread.start()

    # start the OSC server
    dispatcher = Dispatcher()
    dispatcher.map("/dmx/red", print_handler) # register the print_handler function for the "/dmx/red" address
    dispatcher.map("/dmx/green", print_handler) # register the print_handler function for the "/dmx/green" address
    dispatcher.map("/dmx/blue", print_handler) # register the print_handler function for the "/dmx/blue" address
    dispatcher.map("/dmx/tilt", print_handler) # register the print_handler function for the "/dmx/tilt" address
    dispatcher.map("/dmx/flash", print_handler) # register the print_handler function for the "/dmx/tilt" address
    dispatcher.set_default_handler(default_handler)

    try: 
        # Start OSC server and block forever while waiting for incoming messages. 
        server = BlockingOSCUDPServer((ip, port), dispatcher)
        print("OSC server listening on {}".format(server.server_address))
        server.serve_forever()  # Blocks forever

    except KeyboardInterrupt:
        print("Stopping OSC server.")
        stop_event.set()  # Set the stop_event to stop the DMX writing thread


if __name__ == "__main__":
    main()

