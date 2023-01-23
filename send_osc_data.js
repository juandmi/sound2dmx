const dgram = require('dgram')
const OSC = require('osc-js')

// get console arguments
const args = process.argv;
console.log(args);

// assign the 3. argument to the IPAddr variable
const IPAddr = args[2];
console.log(IPAddr);

// create a udp socket
const socket = dgram.createSocket('udp4')

// send a messsage via udp
const message = new OSC.Message('/audio/path', 42, 0.553, 'hello')
const binary = message.pack()

// send the message to the the IPAddr on port 8080
socket.send(binary, 0, binary.length, 8080, IPAddr)
