# Asset credits

## assets/car.glb — player car

Based on **"Car Concept"** from the Khronos glTF Sample Assets
(<https://github.com/KhronosGroup/glTF-Sample-Assets/tree/main/Models/CarConcept>).

- © 2024 Darmstadt Graphics Group GmbH — model and textures by Eric Chadwick
- Licensed under **Creative Commons Attribution 4.0 International (CC BY 4.0)**:
  <https://creativecommons.org/licenses/by/4.0/>
- Itself derived from a public-domain (CC0) model by "Unity Fan" on Sketchfab.

### Changes made for InRun
- Removed the Khronos logo artwork (number plate texture replaced with a plain "IN RUN 5" plate; logo emissive removed from other parts).
- Removed the material variants, the windscreen wipers and several small interior/under-hood parts.
- Removed the glass transmission extension (the game substitutes its own glass material).
- Mesh simplified (~213k → ~92k triangles), textures resized to ≤1024 px and converted to WebP, meshopt compression applied.

No endorsement by the Khronos Group or Darmstadt Graphics Group is implied.

## assets/sfx/ — sound samples

- `kick.wav`, `snare.wav`, `hat.wav`, `ohat.wav`, `cymbal.wav`: trimmed, compressed and resampled from the
  **Versilian Community Sample Library (VCSL)** by Versilian Studios LLC — <https://github.com/sgossner/VCSL> —
  released under **CC0 1.0** (public domain). The kick is a shortened orchestral bass-drum hit.
- `crash.wav`: a mix of three VCSL (CC0) recordings — a hammer-struck brake drum, clash cymbals and a bass drum.
- `engine_lo.wav`, `engine_hi.wav`: original physically-modelled 4-cylinder engine loops made for InRun (no third-party audio).

## assets/music/ — HD-era soundtrack

Supplied by the project owner for InRun's final ("Today") era:
- **"Loading Bar Blues"** (`loading-bar-blues.mp3`)
- **"Chip on Your Shoulder"** (`chip-on-your-shoulder.mp3`)
- **"Custom Chip Blues"** (`custom-chip-blues.mp3`)
- **"Rendered Obsolete"** (`rendered-obsolete.mp3`)
- **"Chip Tune Funeral"** (`chip-tune-funeral.mp3`, `chip-tune-funeral-take-2.mp3`)
- **"Rendered Obsolete (Extended)"** (`rendered-obsolete-extended.mp3`)

## assets/inst/ — sampled instruments for the tracker eras (Amiga / Gravis Ultrasound)

All public domain (**CC0 1.0**), from Versilian Studios' open libraries — trimmed, resampled to 22 kHz mono,
tuned to their measured pitch, and (for sustained instruments) given seamless tracker-style loop points:

- **VS Chamber Orchestra 2: Community Edition** (<https://github.com/sgossner/VSCO-2-CE>): violin section (`strings`),
  contrabass pizzicato (`pizz`), trumpet, French horn (`horn`), tuba, clarinet, flute, harp, upright piano (`piano`)
  and pipe organ (`organ`, sampled by Simon Dalzell of Ivy Audio).
- **Versilian Community Sample Library** (<https://github.com/sgossner/VCSL>): tenor saxophone (`sax`), Hohner harmonica,
  vibraphone (`vibes`), marimba, and the timpani in the orchestra hit.
- `orchhit`: an orchestra-hit stab layered from VSCO violin-section spiccato, trumpet and horn staccato, VCSL timpani and clash cymbals.
