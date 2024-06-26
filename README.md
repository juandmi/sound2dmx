# sound2dmx Project
A project to generate a compelling light show from a music live-stream. 

Completed: 
  - Python script that receives OSC values
  - The script can change the lights on the LED light via the USB interface

Todo:
  - Analyze music and create OSC signals depending on music beat, harmonics, type, etc.

# Hardware
## KMtronic DMX adapter
https://info.kmtronic.com/kmtronic-dmx-adapter.html

![KMtronic DMX adapter](./images/kmtronic-usb-dmx-thumb.jpg)

## Involight Crystal LED BALL 53
https://www.deejayladen.de/de/involight-crystal-led-ball-53/pd/60632

![Involight Crystal LED BALL 53](./images/involight-crystal-led-ball-53-thumb.jpg)

* Ch1: flash speed <br>
* Ch2: red <br>
* Ch3: green <br>
* Ch4: blue <br>
* Ch5: rotation <br>
  - 0-127: angle position <br>
  - 128-255: rotation speed <br>
    - 128-142: very slow <br>
    - 143-157: still slow <br>
    - 158-172: normal <br>
    - 173-187: fast <br>
    - 188-202: 70 swings per minute <br>
    - 203-217: 82 swings per minute <br>
    - 218-232: 88 swings per minute (RAP) <br>
    - 233-247: 111 swings per minute (HOUSE) <br>
    - 248-255: 142 swings per minute (TECHNO) <br>
  
# Software
## DMX USB Driver
https://ftdichip.com/drivers/d2xx-drivers/

## D2XX Programmer's Guide
https://ftdichip.com/wp-content/uploads/2020/08/D2XX_Programmers_GuideFT_000071.pdf

# Usage
## Test the interface by sending DMX data
python .\check-dmx-interface-ftd2xx.py

## Test OSC sending and receiving part
```
npm install socket.io
npm install osc-js
```

Run the the receiving and sending scripts in separate consoles: <br>
```
python .\receive_osc_data.py 
node   .\send_osc_data.js     <target ip address: e.g. 192.168.0.8> 
```

Result: 
```
python  .\receive_osc_data.py
Your Computer Name is:DESKTOP1234
Your Computer IP Address is:192.168.0.8
/audio/path: (42, 0.5529999732971191, 'hello')
```

## Run the ligth show
WIP

First basic steps to control a light changes from Andorid OSC Controller App.
Andorid device and the Windows PC must be in the same network. 

```
python  .\receive_osc_send_dmx.py
Your Computer Name is:DESKTOP1234
Your Computer IP Address is:192.168.0.8
```

Configure the App:
IP Adress: as provided by the python script
Port: 8080
OSC Patch: /dmx


## Configure parameters
WIP

# Helpful Links 
#### Decimal-hexadecimal-binary conversion table: 
https://kb.iu.edu/d/afdl

#### DMX explained
https://community.element14.com/technologies/open-source-hardware/b/blog/posts/dmx-explained-dmx512-and-rs-485-protocol-detail-for-lighting-applications <br>
https://www.erwinrol.com/page/articles/dmx512/ <br>
https://www.thedmxwiki.com/dmx_basics/dmx_timing 

#### KMTronic programming example
https://info.kmtronic.com/control-dmx512-devices-via-raspberry-pi.html

#### Python wrappers around the D2XX DLL from FTDI
https://pypi.org/project/ftd2xx/ <br>
https://github.com/snmishra/ftd2xx  <br>
https://pypi.org/project/PyDMX/ <br>
https://pypi.org/project/PyDMX-Drivers-FTDI/  <br>

#### Audio motion analyzer
https://github.com/hvianna/audioMotion-analyzer

#### Open Sound Control server and client implementations in pure python (3.5+)
https://pypi.org/project/python-osc/

#### Open Sound Control library for JavaScript applications
https://www.npmjs.com/package/osc-js <br>
https://github.com/adzialocha/osc-js

#### A no frills Open Sound Control client and server
https://github.com/MylesBorins/node-osc

#### DMX controller library for node.js
https://github.com/node-dmx

#### OSC controler for Android
https://play.google.com/store/apps/details?id=com.ffsmultimedia.osccontroller&hl=de
