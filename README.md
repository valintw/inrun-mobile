# InRun

An arcade sunset driving game in a single HTML file, built for phones. You steer and work the pedals by tilting the phone.

## A drive through gaming time
Every full lap (all five stages) moves the graphics and music forward an era:

| Lap | Era | Look |
|---|---|---|
| 1 | 1987 · EGA | ~120 lines, fixed 16-colour EGA palette with ordered dithering, CRT scanlines, PC-speaker beeps |
| 2 | 1989 · Amiga | 180 lines, 32 colours picked live from a 4096-colour (12-bit) range, 4-channel style music |
| 3 | 1992 · VGA | 240 lines, 256-colour palette picked live, drums and bass |
| 4 | 1996 · SVGA | 480 lines, smooth scaling, shaded sprites and true colour |
| 5 | Today · HD | **real-time 3D** (three.js / WebGL): a glTF hero car (metallic-flake clearcoat paint, real wheels and interior), modelled traffic with clearcoat paint and reflections, 3D palms, pines, cacti, rocks, billboards, street lamps and lit skyscrapers, sun lighting with soft shadows, fog, filmic tone mapping, bloom and a chase camera |

From lap 5 onward the game stays in HD. The 3D engine downloads in the background after the page loads (from jsDelivr); if WebGL isn't available the HD era falls back to the 2D renderer. The title screen cycles through all five eras.

## Sound through the eras
The audio hardware evolves with the graphics (all synthesised live in the browser):

| Era | Sound |
|---|---|
| 1987 · EGA | **PC speaker** — one square-wave beeper: engine buzz, crash rattle and beeps, no music |
| 1989 · Amiga | **4-channel Paula** — 3-channel tracker tune with 8-bit samples incl. recorded drums (hard-panned L/R), 1 channel for the sampled engine; crashes steal it |
| 1992 · VGA | **AdLib FM** — 2-operator FM bass, brass lead, pads and rhythm-mode drums; **Sound Blaster** 8-bit digitised engine and crashes |
| 1996 · SVGA | **Gravis Ultrasound-style mod** — many 16-bit stereo channels with recorded drums, harmonies, echo and reverb; overlapping sampled SFX, 5-speed engine crossfading two samples, tyre squeal |
| Today · HD | **Streamed MP3** — "Loading Bar Blues" (`assets/music/hd.mp3`, see `assets/music/README.md`); falls back to a fuller synthesised score if it can't load |

## Controls
- **Hold the phone sideways** like a steering wheel.
- **Tilt left / right** to steer.
- **Tilt forward** (top edge away from you) to accelerate. **Tilt back** to brake.
- Your neutral position is calibrated during the 3-2-1 countdown, and again whenever you resume from pause.
- In the pause menu you can flip the pedals, change steering sensitivity, turn sound off, or switch to on-screen touch buttons.

### Desktop / laptop
- **Webcam head tracking:** move your head left / right to steer. Sit centred during the countdown to set straight-ahead.
  A small preview (bottom-left) shows the detected face and your neutral line. Face detection runs locally in the browser
  (MediaPipe, loaded from jsDelivr on first use); no video leaves your machine.
- **Bottom keyboard row is the pedal:** `Z` full brake, `X` `C` lighter braking, `V` coast, `B` `N` part throttle, `M` full throttle.
  If you hold several keys, the one pressed most recently counts.
- Arrow keys / WASD also work, and you can switch to keyboard-only in the menu. P to pause.
- Webcam access also needs HTTPS (or `localhost`).

## Running on a phone
Browsers only send tilt-sensor data to pages served over **HTTPS**. The easiest way is GitHub Pages
(Settings → Pages → deploy from this branch, root folder). On iPhone you'll be asked to allow motion access when you tap START.

Add `?stage=2` … `?stage=5` to the URL to start on a later stage, and `?era=2` … `?era=5` to start in a later era (they can be combined, e.g. `?era=5&stage=3`).

## Credits
The HD-era player car is based on **"Car Concept"** © 2024 Darmstadt Graphics Group GmbH (model and textures by Eric Chadwick),
from the Khronos glTF Sample Assets, licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), modified.
See [`assets/CREDITS.md`](assets/CREDITS.md) for details of the changes. Keep `assets/` next to `index.html` when hosting;
if the model can't be loaded the game uses its built-in procedural car instead.
