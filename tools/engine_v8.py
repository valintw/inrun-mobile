# Regenerate the engine loops: BURBLE=0.6 python3 tools/engine_v8.py assets/sfx   (then update ENG_LO_HZ / ENG_HI_HZ in index.html from the printed firing rates)
# Cross-plane V8 engine loops: 8 firings per 720 deg in the order L R R L R L L R (firing order 1-8-4-3-6-5-7-2),
# each bank through its own exhaust, rendered with circular convolution so the loops are seamless.
import numpy as np, wave, json, sys, os
BURBLE = float(os.environ.get('BURBLE', '1'))
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
def render(rpm, cycles, kind, seed):
    rng = np.random.default_rng(seed)
    f_fire = rpm / 15                                         # V8: 4 firings per revolution
    per_cycle = int(round(sr * 8 / f_fire)); L = per_cycle * cycles; f_fire = sr * 8 / per_cycle
    banks = 'LRRLRLLR'
    lumpy = 1.0 if kind == 'lo' else 0.35
    cyl_amp = 1 + rng.normal(0, 0.07 * lumpy, 8)
    imp = {'L': np.zeros(L), 'R': np.zeros(L)}
    for c in range(cycles):
        cyc = 1 + rng.normal(0, 0.05 * lumpy)                 # whole-cycle variation: the idle lope
        for k in range(8):
            pos = c * per_cycle + k * per_cycle / 8 + rng.normal(0, 1.2 * lumpy)
            i = int(np.floor(pos)) % L; fr = pos - np.floor(pos)
            a = cyl_amp[k] * cyc * (1 + rng.normal(0, 0.09 * lumpy))
            imp[banks[k]][i] += a * (1 - fr); imp[banks[k]][(i + 1) % L] += a * fr
    p = pulse(sr / 2400 if kind == 'lo' else sr / 9000)
    if kind == 'lo':     # big-bore pipes and mufflers: boomy, round, burbly
        resL = [(58, 16, 1.0), (118, 22, 0.75), (205, 38, 0.55), (340, 60, 0.32), (620, 110, 0.14), (1300, 220, 0.05)]
        delayR, detune, noise_amt, drive, lp = 0.0016 * BURBLE, 1 + 0.08 * BURBLE, 0.10, 1.6, 2200
    else:                # at high revs: brassier pipe resonances for a tuneful rasp
        resL = [(180, 90, 0.35), (520, 140, 0.5), (1050, 160, 0.75), (1700, 220, 0.7), (2600, 300, 0.5), (3800, 420, 0.25)]
        delayR, detune, noise_amt, drive, lp = 0.0, 1.0, 0.22, 3.6, 7000
    resR = [(f * detune, d, a) for f, d, a in resL]
    if kind == 'lo': irL = np.convolve(p, resonator_ir(resL, 0.25, np.random.default_rng(seed))); irR = np.convolve(p, resonator_ir(resR, 0.25, np.random.default_rng(seed + 1 if BURBLE > 1 else seed)))   # banks that differ: burble
    else: irL = np.convolve(p, resonator_ir(resL, 0.25, np.random.default_rng(seed))); irR = np.convolve(p, resonator_ir(resR, 0.25, np.random.default_rng(seed)))   # matched banks: a clean, tuneful note
    irR = np.concatenate([np.zeros(int(delayR * sr)), irR]) * (0.92 if kind == "lo" else 1.0)
    sig = cconv(imp['L'], irL) + cconv(imp['R'], irR)
    # combustion/exhaust hiss, gated by the pulses
    env = np.abs(cconv(imp['L'] + imp['R'], np.exp(-np.arange(int(0.012 * sr)) / (0.004 * sr))))
    nz = rng.normal(0, 1, L); F = np.fft.fftfreq(L, 1 / sr)
    nz = np.real(np.fft.ifft(np.fft.fft(nz) * ((np.abs(F) > (300 if kind == 'lo' else 900)) & (np.abs(F) < (2500 if kind == 'lo' else 6000)))))
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
