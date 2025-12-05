# Gojopad
GojoPad is a fully 3D-printed 4-key macropad featuring a rotary encoder, a small OLED display, and a single RGB LED, named after the 1mm-deep Gojo etching on its surface. Its firmware provides dynamic media, voice chat, and display control, making it both functional and visually engaging.


## Features
- Fully 3D-printed dual-layer case with a 2° ergonomic tilt.
- 128x32 OLED display showing multiple modes: uptime clock, custom mode label, simple graphic, and volume bar.
- EC11 rotary encoder:
-   Rotate clockwise to increase volume, counterclockwise to decrease volume.
-   Push to toggle mute.
- 5 programmable keys:
-   SW1: cycle OLED display modes
-   W2: next track
-   SW3: previous track
-   SW4: voice chat toggle
-   SW5: play/pause
-   2 SK6812 MINI-E LEDs: red when muted, blue when unmuted.
-   KMK firmware support for full macro and input customization.


## CAD Model
The case is composed of two 3D-printed pieces:
Base: secures the PCB and provides structural support and sits on a roughly 2˚ tilt.
Top housing: holds switches, diffuses LED light, and features the Gojo etching.

Assembly uses 4 M3 screws with heatset inserts.

<img width="683" height="360" alt="Screenshot 2025-12-05 at 7 08 00 pm" src="https://github.com/user-attachments/assets/28388dad-e0d5-4b3d-a5c9-b6644cd574b6" />


How it will fit together:

<img width="844" height="684" alt="Screenshot 2025-12-05 at 7 24 44 pm" src="https://github.com/user-attachments/assets/7676b1fa-ec75-4ebd-ac03-92fa7d52d46f" />


## PCB
The PCB is designed in KiCad with MX-style switch footprints and supports future enhancements like a ground plane.

Schematic:

<img width="969" height="617" alt="Screenshot 2025-12-05 at 7 09 11 pm" src="https://github.com/user-attachments/assets/b894a0de-f565-4e7c-b08b-8c19cbd93a47" />


PCB Layout:

<img width="788" height="620" alt="Screenshot 2025-12-05 at 7 09 35 pm" src="https://github.com/user-attachments/assets/f8cf122a-5d2d-4801-af4c-facbe1d64ddb" />


## Firmware Overview

GojoPad runs KMK firmware:
- Rotary encoder adjusts volume in 5% steps, push toggles mute.
- OLED cycles through four modes: uptime clock, custom label, simple graphic, and volume bar.
- Keys handle media control, voice chat toggle, and OLED mode cycling.
- NeoPixel LED reflects mute state (red = muted, blue = unmuted).


## BOM (Bill of Materials)
- 4x Cherry MX switches
- 4x Keycaps (DSA recommended)
- 4x M3x5mx4mm heatset inserts
- 4x M3x16mm screws
- 2x SK6812 MINI-E LEDs
- 1x 0.91" 128x32 OLED display
- 1x EC11 rotary encoder
- 1x XIAO RP2040
- Case: 3D-printed parts
