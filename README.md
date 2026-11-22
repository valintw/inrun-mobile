# InRun

An arcade sunset driving game in a single HTML file, built for phones. You steer and work the pedals by tilting the phone.

## A drive through gaming time
The circuit has seven stages — Coastline, Desert Run, Alpine Pass, Downtown Rain, Beachfront, Sunset Blvd and Neon City.
Every full lap moves the graphics and music one era along — up to HD, a WANTED bonus lap, then back down to EGA
(EGA → Amiga → VGA → SVGA → HD → **WANTED** → SVGA → VGA → Amiga → EGA …):

| Lap | Era | Look |
|---|---|---|
| 1 | 1987 · EGA | ~120 lines, fixed 16-colour EGA palette with ordered dithering, CRT scanlines, PC-speaker beeps |
| 2 | 1989 · Amiga | 180 lines, 32 colours picked live from a 4096-colour (12-bit) range, 4-channel style music |
| 3 | 1992 · VGA | 240 lines, 256-colour palette picked live, drums and bass |
| 4 | 1996 · SVGA | 480 lines, smooth scaling, shaded sprites and true colour |
| 5 | Today · HD | **real-time 3D** (three.js / WebGL): a glTF hero car (metallic-flake clearcoat paint, real wheels and interior), modelled traffic with clearcoat paint and reflections, 3D palms, pines, cacti, rocks, billboards, street lamps and lit skyscrapers, sun lighting with soft shadows, fog, filmic tone mapping, bloom and a chase camera |

Each full era cycle (9 laps, back to EGA) adds 20% more traffic, driving 20% faster. Checkpoint time bonuses start at
45 s and ease off by just 2 s per lap, never dropping below 32 s. The 3D engine downloads in the background after the page loads (from jsDelivr); if WebGL isn't available the HD era falls back to the 2D renderer. The title screen cycles through all five eras.

## Sound through the eras
The audio hardware evolves with the graphics (all synthesised live in the browser):

| Era | Sound |
|---|---|
| 1987 · EGA | **PC speaker** — one square-wave beeper: engine buzz, crash rattle and beeps, no music |
| 1989 · Amiga | **4-channel Paula** — 3-channel tracker tune played on real sampled instruments (strings, brass, sax, harmonica, pizzicato bass, orchestra hits…) crunched to 8-bit, plus recorded drums (hard-panned L/R); 1 channel for the engine, which crashes steal |
| 1992 · VGA | **AdLib FM** — 2-operator FM bass, brass lead, pads and rhythm-mode drums; **Sound Blaster** 8-bit digitised engine and crashes |
| 1996 · SVGA | **Gravis Ultrasound-style mod** — many 16-bit stereo channels of sampled instruments (each stage has its own "sample disk") with recorded drums, harmonies, echo and reverb; overlapping sampled SFX, 5-speed engine crossfading two samples, tyre squeal |
| Today · HD | **Streamed MP3 playlist**, shuffled — "Loading Bar Blues", "Chip on Your Shoulder", "Custom Chip Blues", "Rendered Obsolete", "Chip Tune Funeral" (two takes), "Rendered Obsolete (Extended)" (`assets/music/playlist.json`, see `assets/music/README.md`); the next track is loaded when the current one is half played; falls back to a fuller synthesised score |

### Adaptive music (iMUSE-style)
In the tracker/synth eras the score reacts to the game, in the spirit of LucasArts' iMUSE:
- **Vertical layering by speed** — four intensity levels (cruise → flat out) add or remove parts (drums, lead, arpeggios,
  counter-melody, 16th hi-hats), always switching on a bar line; tempo rises ~15% and hits get harder with speed.
- **Horizontal re-sequencing by stage** — the same theme is re-orchestrated per stage: surf-pop (Coastline), spaghetti
  western with twang guitar and whistle (Desert Run), oom-pah polka with accordion, flugelhorn and tuba (Alpine Pass),
  industrial EBM with metallic clangs (Downtown Rain), calypso with steel pan and ukulele (Beachfront), synthwave (Sunset Blvd) and techno with acid bass (Neon City). Crossing a checkpoint plays a one-bar fill, then the
  new arrangement enters at the top of a phrase. Game over ends on a final chord.

## WANTED bonus lap
After the HD lap comes a bonus lap in the HD renderer with sirens and police lights: survive it. The clock is frozen and
replaced by your lap progress, and a gang of black pickups works together to box you in — one gets in front and
brake-checks, two pull alongside, one lurks in the next lane and swerves into you. Crawl along with a truck on you for
too long and you're **BUSTED**: they haul you out, bash you with baseball caps and drive off in your car (game over).
Finish the lap and you get +25,000 points and +20 s, and the eras head back down. Start straight in it with `?era=6`.

## Time bonus & traffic
- When the clock drops below 10 seconds, a glowing **+20 s stopwatch** drops onto the road ahead at a random moment
  between 8 and 3 seconds left. Drive through it to collect; miss it and it's gone.
- Collisions use each vehicle's length (real 3D lengths in the HD era). Vehicles that collide bounce apart; rear-ending
  a car shunts it forward, and a faster car hitting you shoves you on. Traffic overtakes slower vehicles (and you)
  when a lane is free, and follows when it isn't.

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

The page includes Open Graph / Twitter card tags for link previews, pointing at `https://valintw.github.io/inrun-mobile/`. If you host it somewhere else, update the `og:url`, `og:image` and `twitter:image` URLs in `index.html` (they must be absolute).

Add `?stage=2` … `?stage=7` to the URL to start on a later stage, and `?era=2` … `?era=5` to start in a later era (they can be combined, e.g. `?era=5&stage=3`).

## Credits
The HD-era player car is based on **"Car Concept"** © 2024 Darmstadt Graphics Group GmbH (model and textures by Eric Chadwick),
from the Khronos glTF Sample Assets, licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), modified.
See [`assets/CREDITS.md`](assets/CREDITS.md) for details of the changes. Keep `assets/` next to `index.html` when hosting;
if the model can't be loaded the game uses its built-in procedural car instead.
