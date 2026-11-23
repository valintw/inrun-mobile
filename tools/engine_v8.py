# Regenerate the engine loops: BURBLE=0.6 GROWL=1.6 python3 tools/engine_v8.py assets/sfx   (then update ENG_LO_HZ / ENG_HI_HZ in index.html from the printed firing rates)
# Cross-plane V8 engine loops: 8 firings per 720 deg in the order L R R L R L L R (firing order 1-8-4-3-6-5-7-2),
# each bank through its own exhaust, rendered with circular convolution so the loops are seamless.
import numpy as np, wave, json, sys, os
BURBLE = float(os.environ.get('BURBLE', '1'))
GROWL = float(os.environ.get('GROWL', '1'))      # high-rev roughness: bank mismatch + firing irregularity
sr = 22050
def cconv(a, b):
    L = len(a); pb = np.zeros(L); pb[:min(L, len(b))] = b[:L]
    return np.real(np.fft.ifft(np.fft.fft(a) * np.fft.fft(pb)))
def resonator_ir(res, dur, rng):
    n = np.arange(int(dur * sr)) / sr; ir = np.zeros_like(n)
    for f, d, a in res: ir += a * np.exp(-d * n) * np.sin(2 * np.pi * f * n + rng.uniform(0, 6.28))
    return ir
def pulse(width):                      # an exhaust pressure pulse: sharp push, softer suck
    x = np.arange(-3 * width, 6 * width) / width
    return np.exp(-x ** 2) - 0.45 * np.exp(-((x - 1.8) / 1.6) ** 2)
def render_hi(rpm, cycles, seed):
    """High revs, built spectrally so the balance is controllable: a deep, harmonic V8 note (strong fundamental
    and 2nd, upper harmonics falling away with a soft brass bump), amplitude-modulated firing by firing in the
    L R R L R L L R bank pattern for growl, exhaust breath gated by each firing, then saturated for rasp."""
    rng = np.random.default_rng(seed)
    f_fire = rpm / 15; per_cycle = int(round(sr * 8 / f_fire)); L = per_cycle * cycles; f_fire = sr * 8 / per_cycle
    t = np.arange(L) / sr
    note = np.zeros(L)
    for k in range(1, 44):
        f = k * f_fire / 2                    # the note sits on half the firing rate, like the low-rev burble, so the crossfade doesn't jump an octave
        if f > 5000: break
        a = k ** -0.75 * (1 + 0.6 * np.exp(-((f - 1100) / 500) ** 2))      # natural roll-off + brass formant
        if k <= 2: a *= 1.25                                                  # weight in the half-order note and the firing rate
        note += a * np.cos(2 * np.pi * f * t + rng.uniform(0, 6.28))
    # firing-by-firing strength: the bank pattern plus per-cylinder spread (fixed, so it loops) = growl
    bank = np.array([1 if c == 'L' else 0 for c in 'LRRLRLLR'])
    amps = np.clip(1 + GROWL * (0.32 * (bank - 0.5) + rng.normal(0, 0.12, 8)), 0.3, 2)
    fire_idx = (t * f_fire).astype(int) % 8
    phase = (t * f_fire) % 1
    env = amps[fire_idx] * (0.55 + 0.45 * np.exp(-phase * 4))               # a push at each firing
    nz = rng.normal(0, 1, L); F = np.fft.fftfreq(L, 1 / sr)
    nz = np.real(np.fft.ifft(np.fft.fft(nz) * ((np.abs(F) > 200) & (np.abs(F) < 3200))))
    sig = note / np.max(np.abs(note)) + 0.35 * GROWL * nz / np.max(np.abs(nz)) * np.exp(-phase * 6)
    drive = 2.2 + 0.8 * GROWL
    sig = np.tanh(sig * drive) / np.tanh(drive)              # rasp
    sig = sig * env                                          # then the firing-by-firing pulse (kept after the clip: growl)
    S = np.fft.fft(sig); S[np.abs(F) > 5000] *= 0.15; S[np.abs(F) < 25] = 0
    sig = np.real(np.fft.ifft(S)); return sig / np.max(np.abs(sig)) * 0.9, f_fire

def render(rpm, cycles, kind, seed):
    if kind == 'hi': return render_hi(rpm, cycles, seed)
    rng = np.random.default_rng(seed)
    f_fire = rpm / 15                                         # V8: 4 firings per revolution
    per_cycle = int(round(sr * 8 / f_fire)); L = per_cycle * cycles; f_fire = sr * 8 / per_cycle
    banks = 'LRRLRLLR'
    lumpy = 1.0 if kind == 'lo' else 0.45 * GROWL
    cyl_amp = 1 + rng.normal(0, 0.07 * lumpy, 8)
    imp = {'L': np.zeros(L), 'R': np.zeros(L)}
    for c in range(cycles):
        cyc = 1 + rng.normal(0, 0.05 * lumpy)                 # whole-cycle variation: the idle lope
        for k in range(8):
            pos = c * per_cycle + k * per_cycle / 8 + rng.normal(0, 1.2 * lumpy)
            i = int(np.floor(pos)) % L; fr = pos - np.floor(pos)
            a = cyl_amp[k] * cyc * (1 + rng.normal(0, 0.09 * lumpy))
            imp[banks[k]][i] += a * (1 - fr); imp[banks[k]][(i + 1) % L] += a * fr
    p = pulse(sr / 2400 if kind == 'lo' else sr / 6000)
    if kind == 'lo':     # big-bore pipes and mufflers: boomy, round, burbly
        resL = [(58, 16, 1.0), (118, 22, 0.75), (205, 38, 0.55), (340, 60, 0.32), (620, 110, 0.14), (1300, 220, 0.05)]
        delayR, detune, noise_amt, drive, lp = 0.0016 * BURBLE, 1 + 0.08 * BURBLE, 0.10, 1.6, 2200
    else:                # at high revs: brassier pipe resonances for a tuneful rasp
        # deep pipe/muffler modes carry the fundamental and 2nd; mid modes give the brass; top kept soft (no wasp)
        resL = [(140, 40, 0.9), (290, 50, 1.0), (470, 70, 0.75), (820, 110, 0.6), (1300, 170, 0.4), (2100, 260, 0.18), (3200, 380, 0.06)]
        delayR, detune, noise_amt, drive, lp = 0.0005 * GROWL, 1 + 0.025 * GROWL, 0.3, 4.5, 4500
    resR = [(f * detune, d, a) for f, d, a in resL]
    if kind == 'lo': irL = np.convolve(p, resonator_ir(resL, 0.25, np.random.default_rng(seed))); irR = np.convolve(p, resonator_ir(resR, 0.25, np.random.default_rng(seed + 1 if BURBLE > 1 else seed)))   # banks that differ: burble
    else: irL = np.convolve(p, resonator_ir(resL, 0.25, np.random.default_rng(seed))); irR = np.convolve(p, resonator_ir(resR, 0.25, np.random.default_rng(seed)))   # near-matched banks: a tuneful note with a growl under it
    irR = np.concatenate([np.zeros(int(delayR * sr)), irR]) * (0.92 if kind == "lo" else 1.0)
    sig = cconv(imp['L'], irL) + cconv(imp['R'], irR)
    # combustion/exhaust hiss, gated by the pulses
    env = np.abs(cconv(imp['L'] + imp['R'], np.exp(-np.arange(int(0.012 * sr)) / (0.004 * sr))))
    nz = rng.normal(0, 1, L); F = np.fft.fftfreq(L, 1 / sr)
    nz = np.real(np.fft.ifft(np.fft.fft(nz) * ((np.abs(F) > (300 if kind == 'lo' else 250)) & (np.abs(F) < (2500 if kind == 'lo' else 3500)))))
    sig = sig / np.max(np.abs(sig)) + noise_amt * nz / np.max(np.abs(nz)) * env / np.max(env)
    sig = np.tanh(sig * drive) / np.tanh(drive)               # saturation: rasp at the top
    S = np.fft.fft(sig); S[np.abs(F) > lp] *= 0.1; S[np.abs(F) < 25] = 0   # tame fizz, no DC
    sig = np.real(np.fft.ifft(S)); sig = sig / np.max(np.abs(sig)) * 0.9
    return sig, f_fire
out = {}
for name, rpm, cycles, kind, seed in [('engine_lo', 1300, 6, 'lo', 3), ('engine_hi', 4600, 16, 'hi', 5)]:
    sig, f = render(rpm, cycles, kind, seed)
    with wave.open(sys.argv[1] + '/' + name + '.wav', 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((sig * 32767).astype('<i2').tobytes())
    np.save(name + '.npy', sig); out[name] = round(f, 3)
    print(name, 'rpm', rpm, 'firing', round(f, 2), 'Hz', 'len', round(len(sig) / sr, 3), 's')
json.dump(out, open('bases.json', 'w'))
