from pythonosc import dispatcher
from pythonosc import osc_server

# define a message-handler function for the server to call.
def audio_handler(unused_addr, args, data):
    global dmx_data
    dmx_data = data
    print("audio data:", data)

# create the dispatcher
disp = dispatcher.Dispatcher()

# add the function to the dispatcher to handle audio OSC messages
disp.map("/audio", audio_handler)

# start the OSC server
server = osc_server.ThreadingOSCUDPServer(("localhost", 1234), disp)
server.serve_forever()
