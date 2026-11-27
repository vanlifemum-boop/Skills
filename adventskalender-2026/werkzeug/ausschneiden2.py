"""Schneidet neue Figurenblätter frei und legt neue Räume ab.
Blätter: 4x2 Posen auf Weiß, Namen je Pose in Lesereihenfolge (oben links -> unten rechts)."""
import os, sys, numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as nd
sys.path.insert(0, os.path.dirname(__file__))

UP = "/root/.claude/uploads/e73e5dc2-c174-5b34-a820-4256d6ebf970/"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAEUME = {  # Upload -> Dateiname in raeume/
    "fbceaa93": "kinderzimmer_tag", "9c3c3d1f": "archiv", "040fc798": "eingang", "a0ebbc46": "kueche_zuhause",
    "46764f43": "kinderzimmer_nacht", "3c884bb5": "gemeinschaftsraum", "efc3df91": "heim1960", "d191e61d": "pflegefamilie",
    "1a5ef53c": "konferenzsaal", "76f3743c": "lager", "d064bb90": "heimstube", "41b2c24a": "anhoerung",
    "1fc1e180": "fenster", "7d95a41d": "kueche_wohngruppe", "1e96c95f": "untersuchung", "ccc291f6": "amtsstube",
    "45423c8a": "bahnhof", "69467cb8": "garten",
    "a3fbc981": "schulhof", "b56da81b": "jugendwerkhof", "6a789b76": "gerichtssaal",
    "80a92514": "dorfstrasse", "0ef27cb2": "konferenzraum",
}
SITZ = ["sitz_traurig", "sitz_froehlich", "sitz_nachdenklich", "sitz_weinend", "malt", "schreibt", "knie", "sitz_hoffnungsvoll"]
HEIM = ["traurig", "gerade", "schrubbt", "isst", "weinend", "aengstlich", "kopfgesenkt", "hoffnungsvoll"]
ALT = ["mikrofon", "kinderfoto", "weinend", "hoffnungsvoll", "sitzend", "nachdenklich", "hand", "laecheln"]
JWH = ["aengstlich", "wuetend", "still", "marschiert", "pritsche", "arbeitet", "weinend", "trotzig"]
AMT = ["schreibt", "stempelt", "ueberreicht", "ernst", "aktentasche", "notiert", "kopfschuetteln", "unterschreibt"]
HALT = ["tel_traurig", "tel_tapfer", "brief", "stern", "plaetzchen", "hinten", "wartet", "bett"]
HIST = ["sitz_traurig", "sitz_aengstlich", "gefaltet", "still", "hinten", "schrubbt", "koffer", "decke"]
MAMA = ["traurig", "weinend", "tel_traurig", "tel_laechelnd", "hoffnungsvoll", "arme", "tisch", "fenster"]
BLAETTER = {  # Upload -> (Präfix, Posen)
    "284790bf": ("k04_heute", SITZ), "a4a51f94": ("k01_heute", SITZ), "6b018b3a": ("k02_heute", SITZ),
    "9c577501": ("alt_frau", ALT), "07a2f234": ("alt_mann", ALT),
    "5e6caf36": ("jwh_junge", JWH), "52e68e2e": ("jwh_maedchen", JWH),
    "3b45392a": ("k08_heim60", HEIM), "be99db48": ("k05_heim60", HEIM), "05a31b32": ("k01_heim60", HEIM),
    "b00fa3d0": ("fuersorgerin", AMT), "0553e1f1": ("beamter", AMT),
    "df311035": ("pflegemutter", ["freundlich", "unsicher", "hand", "brief", "nachdenklich", "sitzend", "besorgt", "erklaert"]),
    "06bf3db4": ("erzieherin", ["streng", "zeigt", "liste", "haendehinten", "glocke", "schimpft", "schluessel", "hinten"]),
    "8ef5bbe1": ("mutter1940", ["verzweifelt", "ruft", "foto", "sucht", "arme", "umarmt", "hoffnungsvoll", "trauernd"]),
    "2938e3db": ("k05_heute", HALT), "814ea0bb": ("k08_damals", HIST), "9bcf12ba": ("k06_damals", HIST),
    "aa2a4b33": ("jugendamt", ["akte", "schreibt", "kalender", "ernst", "freundlich", "erklaert", "telefoniert", "aktearm"]),
    "eca2dd7e": ("k07_damals", HIST), "0bdf8b2d": ("k09_damals", HIST), "287ad79d": ("k02_damals", HIST),
    "07e08ec2": ("k07_heute", HALT), "8302c2cd": ("k03_damals", HIST), "1183007a": ("mama01", MAMA),
    "bb7fb389": ("k05_damals", HIST), "cf5e554e": ("k01_damals", HIST), "1e4358a4": ("k04_damals", HIST),
    "3c93c091": ("mama02", MAMA), "7ef8fd23": ("k02_heute", HALT), "adf019a4": ("k08_heute", HALT),
    "c60ed62e": ("k09_heute", HALT), "254f2b2d": ("k06_heute", HALT),
    "468708d5": ("k03_heute", HALT), "e2173fb5": ("k01_heute", HALT), "1f81ee92": ("k04_heute", HALT),
    "f5a9b906": ("k08_heute", SITZ), "475c777f": ("k07_heute", SITZ), "5d6db163": ("k09_heute", SITZ),
    "e88b0db8": ("k06_heute", SITZ), "82b66a27": ("k05_heute", SITZ), "be10d9a8": ("k03_heute", SITZ),
    "059b20b2": ("betreuerin", ["freundlich", "hoertzu", "erklaert", "nachdenklich", "besorgt", "kniet", "telefoniert", "akte"]),
}


def cut_sheet(path, prefix, names, out):
    a = np.asarray(Image.open(path).convert("RGB")).astype(int)
    h, w, _ = a.shape
    ink = (a.min(axis=2) < 225)
    ink[:62] = False
    for it in (4, 2, 1, 0):
        lab, n = nd.label(nd.binary_dilation(ink, iterations=it) if it else ink)
        objs = nd.find_objects(lab)
        figs = [(sl, i + 1) for i, sl in enumerate(objs) if sl is not None and sl[0].stop - sl[0].start > 200]
        if len(figs) == 8:
            break
    if len(figs) != 8:
        print("WARN", prefix, len(figs)); return
    rows = sorted(figs, key=lambda f: (f[0][0].start + f[0][0].stop) / 2)
    order = sorted(rows[:4], key=lambda f: f[0][1].start) + sorted(rows[4:], key=lambda f: f[0][1].start)
    for k, (sl, li) in enumerate(order):
        y0, y1 = max(0, sl[0].start - 4), min(h, sl[0].stop + 4)
        x0, x1 = max(0, sl[1].start - 4), min(w, sl[1].stop + 4)
        own = (lab[y0:y1, x0:x1] == li)
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
        alpha = ~bg
        pure = (crop.min(axis=2) > 247)
        pl, pn = nd.label(pure)
        if pn:
            sizes = nd.sum(pure, pl, range(1, pn + 1))
            lower = int(crop.shape[0] * 0.5)
            for idx, sz in enumerate(sizes, 1):
                if sz > 25:
                    ys = np.nonzero(pl == idx)[0]
                    if ys.min() > lower:
                        alpha[pl == idx] = False
        alpha = nd.binary_erosion(alpha, iterations=2)
        cl, cn = nd.label(alpha)
        if cn > 1:
            cs = nd.sum(alpha, cl, range(1, cn + 1))
            alpha = np.isin(cl, [i + 1 for i, v in enumerate(cs) if v > 0.03 * cs.max()])
        am = Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
        rgba = Image.fromarray(crop.astype(np.uint8)).convert("RGBA"); rgba.putalpha(am)
        rgba = rgba.crop(rgba.getbbox())
        rgba = rgba.resize((rgba.width * 2, rgba.height * 2), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.6, 60, 2))
        rgba.save(os.path.join(out, f"{prefix}_{names[k]}.png"))


if __name__ == "__main__":
    for up, name in RAEUME.items():
        im = Image.open(UP + up + "-image.png").convert("RGB")
        im = im.resize((int(im.width * 1920 / im.height), 1920), Image.LANCZOS)
        im.save(os.path.join(ROOT, "raeume", name + ".jpg"), quality=90)
        b = im.resize((im.width // 4, im.height // 4)).filter(ImageFilter.GaussianBlur(6)).resize(im.size)
        from PIL import ImageEnhance
        ImageEnhance.Brightness(b).enhance(0.75).save(os.path.join(ROOT, "raeume", name + "_weich.jpg"), quality=85)
    for up, (prefix, names) in BLAETTER.items():
        cut_sheet(UP + up + "-image.png", prefix, names, os.path.join(ROOT, "kinder"))
    print("fertig")
