# sound2dmx Project
A Project to generate a compelling light show from a music live-stream

# Hardware
## KMtronic DMX adapter
https://info.kmtronic.com/kmtronic-dmx-adapter.html

![KMtronic DMX adapter](./images/kmtronic-usb-dmx-thumb.jpg)

## Involight Crystal LED BALL 53
https://www.deejayladen.de/de/involight-crystal-led-ball-53/pd/60632

![Involight Crystal LED BALL 53](./images/involight-crystal-led-ball-53-thumb.jpg)

Ch1: flash speed <br>
Ch2: red <br>
Ch3: green <br>
Ch4: blue <br>
Ch5: rotation <br>
  >0-127: angle position, rotary speed , 143-157: faster, , 188-202: insane, 203-217: warp 9 <br>
  >128-255: rotation speed <br>
    >>128-142: very slow <br>
    >>143-157: still slow <br>
    >>158-172: normal <br>
    >>173-187: fast <br>
    >>188-202: 70 swings per minute <br>
    >>203-217: 82 swings per minute <br>
    >>218-232: 88 swings per minute (RAP) <br>
    >>233-247: 111 swings per minute (HOUSE) <br>
    >>248-255: 142 swings per minute (TECHNO) <br>
  
# Software
## DMX USB Driver
https://ftdichip.com/drivers/d2xx-drivers/

## D2XX Programmer's Guide
https://ftdichip.com/wp-content/uploads/2020/08/D2XX_Programmers_GuideFT_000071.pdf


# Usage
## Test the DMX interface by sending 
python .\check-dmx-interface-ftd2xx.py
