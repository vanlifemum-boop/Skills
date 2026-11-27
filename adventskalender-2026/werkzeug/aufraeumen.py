"""Entfernt weiße Bodenschatten unter den Figuren und speichert alle Posen als WebP (mit Transparenz)."""
import glob, os, numpy as np
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for p in sorted(glob.glob(os.path.join(ROOT, "kinder", "*.png"))):
    im = Image.open(p).convert("RGBA")
    a = np.asarray(im).copy()
    h = a.shape[0]
    y0 = int(h * 0.85)
    sub = a[y0:]
    rgb = sub[..., :3].astype(int)
    mask = (rgb.min(axis=2) > 205) & ((rgb.max(axis=2) - rgb.min(axis=2)) < 28)
    sub[..., 3][mask] = 0
    a[y0:] = sub
    out = Image.fromarray(a)
    out = out.crop(out.getbbox())
    out.save(p[:-4] + ".webp", "WEBP", quality=88, method=5)
    os.remove(p)
print(len(glob.glob(os.path.join(ROOT, "kinder", "*.webp"))))
