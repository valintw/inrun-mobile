# InRun

An arcade sunset driving game in a single HTML file, built for phones. You steer and work the pedals by tilting the phone.

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

Add `?stage=2` … `?stage=5` to the URL to start on a later stage.
