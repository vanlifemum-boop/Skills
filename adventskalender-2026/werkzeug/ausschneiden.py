"""Schneidet die 8 Posen jedes Charakterblatts frei (weißer Hintergrund -> transparent), 2x hochskaliert."""
import sys, os, numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as nd

UP = "/root/.claude/uploads/e73e5dc2-c174-5b34-a820-4256d6ebf970/"
HIST = ["ffaec6d8","e6111b76","2dad4d17","246c6113","fc906163","4b298fc1","5685c473","a99eb2c8","e768f1cc"]
XMAS = ["5521f27a","b6bc41b7","edfe9cf4","8695fc8c","f82a3efd","f133f798","947a02a7","e560579c","757972a3"]
EMO = ["froehlich","traurig","weinend","wuetend","ueberrascht","nachdenklich","aengstlich","hoffnungsvoll"]
OUT = sys.argv[1]

def cut(path, prefix):
    a = np.asarray(Image.open(path).convert("RGB")).astype(int)
    h, w, _ = a.shape
    ink = (a.min(axis=2) < 225)
    ink[:48] = False                      # Titelzeile weg
    for it in (4, 2, 1, 0):
        lab, n = nd.label(nd.binary_dilation(ink, iterations=it) if it else ink)
        objs = nd.find_objects(lab)
        if sum(1 for sl in objs if sl[0].stop - sl[0].start > 220) == 8:
            break
    figs = []
    for i, sl in enumerate(objs):
        hh = sl[0].stop - sl[0].start
        if hh > 220:
            figs.append((sl, i + 1))
    if len(figs) != 8:
        print("WARN", prefix, len(figs), [ (s[0].stop-s[0].start, s[1].stop-s[1].start) for s,_ in figs]); 
    rows = sorted(figs, key=lambda f: f[0][0].start)
    top = sorted(rows[:4], key=lambda f: f[0][1].start); bot = sorted(rows[4:], key=lambda f: f[0][1].start)
    for k, (sl, li) in enumerate(top + bot):
        y0, y1 = max(0, sl[0].start - 4), min(h, sl[0].stop + 4)
        x0, x1 = max(0, sl[1].start - 4), min(w, sl[1].stop + 4)
        own = (lab[y0:y1, x0:x1] == li)
        # Beschriftung unter den Füßen abschneiden: unterste Lücke aus leeren Zeilen im unteren Drittel
        rows_ink = (ink[y0:y1, x0:x1] & own).any(axis=1)
        H = len(rows_ink); cut_at = H; gap = 0
        for y in range(H - 1, int(H * 0.7), -1):
            if not rows_ink[y]:
                gap += 1
                if gap >= 3 and rows_ink[:y].any() and rows_ink[y + gap:].any():
                    cut_at = y; break
            else:
                gap = 0
        y1 = min(y1, y0 + cut_at + 2)
        own = (lab[y0:y1, x0:x1] == li)
        crop = a[y0:y1, x0:x1]
        bgc = (crop.min(axis=2) > 232) & ((crop.max(axis=2) - crop.min(axis=2)) < 18)
        bl, _ = nd.label(bgc)
        border = set(np.unique(np.concatenate([bl[0], bl[-1], bl[:, 0], bl[:, -1]]))) - {0}
        bg = np.isin(bl, list(border)) | ~own
        alpha = (~bg).astype(np.uint8) * 255
        # reinweiße Inseln zwischen Beinen/Armen ebenfalls transparent
        pure = (crop.min(axis=2) > 247)
        pl, pn = nd.label(pure)
        sizes = nd.sum(pure, pl, range(1, pn + 1))
        lower = int(crop.shape[0] * 0.55)
        for idx, sz in enumerate(sizes, 1):
            if sz > 25:
                ys = np.nonzero(pl == idx)[0]
                if ys.min() > lower:          # nur zwischen den Beinen
                    alpha[pl == idx] = 0
        alpha = nd.binary_erosion(alpha > 0, iterations=2)
        # nur die Figur behalten (Beschriftungsreste sind eigene kleine Inseln)
        cl, cn = nd.label(alpha)
        if cn > 1:
            cs = nd.sum(alpha, cl, range(1, cn + 1))
            keep = [i + 1 for i, v in enumerate(cs) if v > 0.03 * cs.max()]
            alpha = np.isin(cl, keep)
        alpha = nd.binary_fill_holes(alpha) if False else alpha
        am = Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
        rgba = Image.fromarray(crop.astype(np.uint8)).convert("RGBA"); rgba.putalpha(am)
        bbox = rgba.getbbox(); rgba = rgba.crop(bbox)
        rgba = rgba.resize((rgba.width * 2, rgba.height * 2), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.6, 60, 2))
        rgba.save(os.path.join(OUT, f"{prefix}_{EMO[k]}.png"))

for i, f in enumerate(HIST):
    cut(UP + f + "-image.png", f"k{i+1:02d}_damals")
for i, f in enumerate(XMAS):
    cut(UP + f + "-image.png", f"k{i+1:02d}_heute")
print("fertig")
