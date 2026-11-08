"""Berechnet die Schriftgrösse für das Takeaway-Widget, sodass alle Teile sicher Platz haben.

Aufruf: python3 tools/fit.py "Titel" "1. ..." "2. ..." "3. ..." "Sonnenkind-Satz"
Schreibt zeilen.txt mit einem sechsten Teil: Breite geteilt durch Schriftgrösse, mal 10, als ganze Zahl
(z.B. 172 heisst Schrift = Breite / 17.2). Ganze Zahl, weil Dezimalpunkte je nach Sprache falsch gelesen werden.
Das Layout hier entspricht make.py (Abstände, Breiten, Zeilenhöhe).
"""
import sys
from pathlib import Path
from PIL import ImageFont

FONTS = Path(__file__).resolve().parent.parent / "fonts"
ROOT = Path(__file__).resolve().parent.parent

W = 1000.0
H = W * 0.72          # Seitenverhältnis des 3x2-Widgets (3 breit, 2 hoch) auf dem Pixel, aus Screenshot gemessen
TEXT_W = 0.88 * W
LINE = 1.32           # Zeilenhöhe im Verhältnis zur Schriftgrösse (gemessen am Screenshot)
TOP = 0.04 * H
BOTTOM = 0.035 * H    # Rand unten, der frei bleiben soll
SAFETY = 0.93         # Reserve für Abweichungen beim Rendern
MAX_K = 1 / 20.0      # nicht grösser als das, sonst wirkt es klobig


def lines(text, font):
    words, n, cur = text.split(), 1, ""
    for w in words:
        trial = (cur + " " + w).strip()
        if font.getlength(trial) <= TEXT_W:
            cur = trial
        else:
            n, cur = n + 1, w
    return n


def height(parts, s):
    reg = ImageFont.truetype(str(FONTS / "Lora-Regular.ttf"), s)
    bold = ImageFont.truetype(str(FONTS / "Lora-Bold.ttf"), s * 1.45)
    ital = ImageFont.truetype(str(FONTS / "Lora-Italic.ttf"), s)
    title, steps, sk = parts[0], parts[1:4], parts[4] if len(parts) > 4 else ""
    h = TOP + lines(title, bold) * LINE * s * 1.45 + s / 4
    for st in steps:
        h += lines(st, reg) * LINE * s + s / 4
    if sk:
        h += s * 0.5 + lines(sk, ital) * LINE * s
    return h + BOTTOM


def fit(parts):
    lo, hi = 5.0, W * MAX_K
    if height(parts, hi) <= H:
        return hi / W
    for _ in range(40):
        mid = (lo + hi) / 2
        if height(parts, mid) <= H:
            lo = mid
        else:
            hi = mid
    return lo * SAFETY / W


if __name__ == "__main__":
    parts = sys.argv[1:]
    if len(parts) not in (4, 5):
        sys.exit("Erwartet: Titel, drei Schritte, optional Sonnenkind-Satz")
    k = fit(parts)
    (ROOT / "zeilen.txt").write_text("~".join(parts + [str(round(10 / k))]))
    (ROOT / "takeaway.txt").write_text("\n".join(parts) + "\n")
    print(f"Schriftgrösse: Breite / {1 / k:.1f}")
