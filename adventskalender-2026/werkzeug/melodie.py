"""Leise, traurige Klaviermelodie (a-Moll, 60 BPM) für alle 24 Folgen.
Abschnitte passen zu den Szenen: 0-24 Kind (Melodie), 24-32 Übergang,
32-52 Damals (nur tiefe Töne), 52-67 Recht (Melodie kehrt zurück), 67-75 Ende."""
import numpy as np, wave, sys

SR = 44100
DUR = 75.0
rng = np.random.default_rng(7)

def hz(n):
    names = {'C':-9,'C#':-8,'D':-7,'D#':-6,'E':-5,'F':-4,'F#':-3,'G':-2,'G#':-1,'A':0,'A#':1,'B':2}
    note, octv = n[:-1], int(n[-1])
    return 440.0 * 2 ** ((names[note] + (octv - 4) * 12) / 12)

out = np.zeros(int(SR * (DUR + 4)))

def piano(t0, note, length, vel=0.5):
    f = hz(note)
    n = int(SR * (length + 2.5))
    t = np.arange(n) / SR
    sig = np.zeros(n)
    for k in range(1, 7):
        sig += (1 / k ** 1.6) * np.sin(2 * np.pi * f * k * (1 + 0.0004 * k) * t) * np.exp(-t * (0.9 + 0.55 * k))
    env = np.minimum(1, t / 0.006)
    # Note release after its length
    rel = np.where(t > length, np.exp(-(t - length) * 3.0), 1.0)
    sig *= env * rel * vel
    i = int(t0 * SR)
    out[i:i + n] += sig[:len(out) - i]

def seq(start, notes, vel):
    t = start
    for n, d in notes:
        if n != '-':
            piano(t, n, d, vel)
        t += d

# --- Melodie (rechte Hand) ---
mel_a = [('E5',1),('D5',1),('C5',2), ('C5',1),('B4',.5),('A4',.5),('A4',2),
         ('G4',1),('A4',1),('C5',1),('E5',1), ('D5',3),('-',1),
         ('E5',1),('D5',1),('C5',1),('B4',1), ('B4',2),('G#4',2)]
seq(0.0, mel_a, 0.42)
seq(24.0, [('A4',4),('-',4)], 0.30)
# Damals: hohe einzelne Töne, sehr leise
for b, n in [(33,'A5'),(41,'E5'),(49,'A5')]:
    piano(b, n, 2.5, 0.14)
mel_b = [('A4',1),('C5',1),('F5',2), ('E5',1),('D5',1),('C5',2),
         ('B4',1),('C5',1),('D5',2), ('C5',1),('B4',1),('A4',2),
         ('E5',1),('D5',1),('C5',2), ('A4',4)]
seq(52.0, mel_b, 0.40)

# --- Begleitung (linke Hand) ---
chords = {'Am':['A2','E3','C4','E3'], 'F':['F2','C3','A3','C3'], 'C':['C3','G3','E4','G3'],
          'G':['G2','D3','B3','D3'], 'E':['E2','B2','G#3','B2'], 'Dm':['D3','A3','F4','A3']}
def arp(bar_start, ch, vel=0.22):
    for i, n in enumerate(chords[ch]):
        piano(bar_start + i, n, 1.6, vel)
for i, ch in enumerate(['Am','F','C','G','Am','E']):
    arp(i * 4, ch)
arp(24, 'Am', 0.18); piano(28, 'F2', 4, 0.20); piano(28, 'C3', 4, 0.14)
for i, ch in enumerate(['Am','Dm','Am','E','Am']):   # 32-52: nur lange tiefe Töne
    r = chords[ch]
    piano(32 + i * 4, r[0], 4, 0.20); piano(32 + i * 4, r[1], 4, 0.13)
for i, ch in enumerate(['F','C','G','Am','Am','F']):
    arp(52 + i * 4, ch, 0.2 if i < 5 else 0.16)

# --- Raum (Hall per FFT-Faltung) ---
ir_len = int(SR * 3.2)
ir = rng.standard_normal(ir_len) * np.exp(-np.arange(ir_len) / SR / 0.9)
ir[0] = 0
n = len(out) + ir_len
N = 1 << (n - 1).bit_length()
wet = np.fft.irfft(np.fft.rfft(out, N) * np.fft.rfft(ir, N), N)[:len(out)]
wet /= np.max(np.abs(wet)) / np.max(np.abs(out))
mix = 0.72 * out + 0.38 * wet
mix = mix[:int(SR * DUR)]
# Ausblenden
t = np.arange(len(mix)) / SR
mix *= np.minimum(1, t / 0.3)
mix *= np.clip((DUR - t) / 3.5, 0, 1)
mix /= np.max(np.abs(mix))
mix *= 10 ** (-3 / 20)
st = np.stack([mix, mix], 1)
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype(np.int16).tobytes())
print('ok', len(mix) / SR)
