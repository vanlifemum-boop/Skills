"""Warme, weiche Hintergrundmusik (d-Moll, sehr ruhig) für alle Folgen.
Weicher Klangteppich (Pad) aus reinen Sinustönen mit langsamem Einschwingen,
dazu ein gedämpftes Klavier in mittlerer Lage. Keine hohen Obertöne, Tiefpass gegen Schärfe.
Abschnitte: 0-24 Kind, 24-32 Übergang, 32-52 Damals (nur Teppich), 52-67 Recht, 67-75 Ende."""
import numpy as np, wave, sys

SR = 44100
DUR = float(sys.argv[2]) if len(sys.argv) > 2 else 75.0
out = np.zeros(int(SR * (DUR + 6)))
NAMES = {'C':-9,'C#':-8,'D':-7,'Eb':-6,'E':-5,'F':-4,'F#':-3,'G':-2,'Ab':-1,'A':0,'Bb':1,'B':2}

def hz(n):
    return 440.0 * 2 ** ((NAMES[n[:-1]] + (int(n[-1]) - 4) * 12) / 12)

def add(t0, sig):
    i = int(t0 * SR)
    j = min(len(out), i + len(sig))
    out[i:j] += sig[:j - i]

def pad(t0, notes, length, vol=0.05):
    n = int(SR * (length + 3))
    t = np.arange(n) / SR
    env = np.clip(t / 2.2, 0, 1) ** 2
    env *= np.where(t > length, np.exp(-(t - length) / 1.4), 1)
    sig = np.zeros(n)
    for note in notes:
        f = hz(note)
        for det in (-0.12, 0.0, 0.12):          # leichte Schwebung = Wärme
            sig += np.sin(2 * np.pi * f * (1 + det / 100) * t + det * 7)
        sig += 0.12 * np.sin(2 * np.pi * 2 * f * t)
    add(t0, sig * env * vol / len(notes))

def felt(t0, note, length, vel=0.22):
    f = hz(note)
    n = int(SR * (length + 3))
    t = np.arange(n) / SR
    sig = np.sin(2 * np.pi * f * t) + 0.22 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 2.5)
    env = np.clip(t / 0.03, 0, 1) * np.exp(-t * 0.55)
    env *= np.where(t > length, np.exp(-(t - length) * 2.0), 1)
    add(t0, sig * env * vel)

chords = {'Dm': ['D3','F3','A3'], 'Bb': ['Bb2','D3','F3'], 'F': ['F2','A2','C3'], 'C': ['C3','E3','G3'],
          'Gm': ['G2','Bb2','D3'], 'A': ['A2','C#3','E3']}
prog = ['Dm','Bb','F','C','Dm','Bb','Gm','A',  'Dm','Bb','F','C','Gm','Dm','Bb','A',  'Dm','Bb','F']
for i, ch in enumerate(prog):
    t0 = i * 4
    if t0 >= DUR: break
    notes = chords[ch] + [chords[ch][0][:-1] + str(int(chords[ch][0][-1]) + 1)]
    pad(t0, notes, 4.2, 0.055)
    felt(t0, chords[ch][0][:-1] + '2', 3.8, 0.13)            # weicher Bass

def seq(t, notes, vel=0.2):
    for n, d in notes:
        if n != '-': felt(t, n, d * 1.4, vel)
        t += d

# Melodie in mittlerer Lage (A3-F4), langsam
seq(0,  [('A3',2),('F4',1),('E4',1), ('D4',3),('-',1), ('C4',2),('A3',1),('C4',1), ('E4',4),
         ('F4',2),('E4',1),('D4',1), ('D4',3),('-',1)])
seq(52, [('A3',2),('D4',1),('E4',1), ('F4',3),('-',1), ('E4',2),('D4',1),('C4',1), ('D4',4)])
seq(68, [('F4',2),('E4',2), ('D4',4)], 0.16)

# Hall
rng = np.random.default_rng(3)
L = int(SR * 3.5)
ir = rng.standard_normal(L) * np.exp(-np.arange(L) / SR / 1.1); ir[:200] = 0
N = 1 << (len(out) + L - 1).bit_length()
wet = np.fft.irfft(np.fft.rfft(out, N) * np.fft.rfft(ir, N), N)[:len(out)]
wet *= np.max(np.abs(out)) / (np.max(np.abs(wet)) + 1e-9)
mix = 0.7 * out + 0.45 * wet
# Tiefpass (zweimal einpolig, ~2,5 kHz) gegen jede Schärfe
a = np.exp(-2 * np.pi * 2500 / SR)
for _ in range(2):
    y = np.empty_like(mix); acc = 0.0
    for_k = mix
    # vektorisiert über lfilter-Ersatz
    from itertools import accumulate
    y = np.array(list(accumulate(for_k, lambda p, x: a * p + (1 - a) * x)))
    mix = y
mix = mix[:int(SR * DUR)]
t = np.arange(len(mix)) / SR
mix *= np.clip(t / 1.5, 0, 1) * np.clip((DUR - t) / 4.0, 0, 1)
mix = mix / np.max(np.abs(mix)) * 0.7
st = np.stack([mix, mix], 1)
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype(np.int16).tobytes())
print('ok')
