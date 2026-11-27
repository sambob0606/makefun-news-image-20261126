# One image summing up the world news of Thursday 26 November 2026.
# Python 3.13, standard library only. Writes /output/entry.png (1024x1024).
# Local run: mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import os
import struct
import zlib

W = 1024
H = 1024

PAPER = (244, 241, 234)
INK = (24, 26, 32)
MUTED = (96, 100, 110)
RED = (178, 34, 44)
NAVY = (27, 48, 92)
TEAL = (18, 110, 108)
GOLD = (196, 138, 30)
GREEN = (46, 125, 72)
PURPLE = (96, 62, 140)
ORANGE = (204, 102, 34)
SKY = (58, 112, 168)
CARD = (255, 255, 255)
LINE = (210, 205, 194)

FONT = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "C": [".####", "#....", "#....", "#....", "#....", "#....", ".####"],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
    "G": [".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "I": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"],
    "J": ["..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "Q": [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"],
    "X": ["#...#", ".#.#.", "..#..", "..#..", "..#..", ".#.#.", "#...#"],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    "Z": ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
    "0": [".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."],
    "1": ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", "#####"],
    "2": [".###.", "#...#", "....#", "..##.", ".#...", "#....", "#####"],
    "3": ["####.", "....#", "....#", ".###.", "....#", "....#", "####."],
    "4": ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
    "5": ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
    "6": [".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."],
    "7": ["#####", "....#", "...#.", "..#..", "..#..", "..#..", "..#.."],
    "8": [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
    "9": [".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."],
    " ": [".....", ".....", ".....", ".....", ".....", ".....", "....."],
    ".": [".....", ".....", ".....", ".....", ".....", ".##..", ".##.."],
    ",": [".....", ".....", ".....", ".....", ".##..", ".##..", "#...."],
    ":": [".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."],
    "-": [".....", ".....", ".....", "#####", ".....", ".....", "....."],
    "/": ["....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."],
    "%": ["##..#", "##.#.", "....#", "...#.", "..#..", ".#...", "#..##"],
    "+": [".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."],
    "'": ["..#..", "..#..", ".#...", ".....", ".....", ".....", "....."],
    "!": ["..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."],
    "?": [".###.", "#...#", "....#", "..##.", "..#..", ".....", "..#.."],
    "(": ["...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."],
    ")": [".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."],
}


class Canvas:
    def __init__(self):
        self.px = bytearray(bytes(PAPER) * (W * H))

    def set(self, x, y, color):
        if 0 <= x < W and 0 <= y < H:
            i = (y * W + x) * 3
            self.px[i] = color[0]
            self.px[i + 1] = color[1]
            self.px[i + 2] = color[2]

    def rect(self, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, color)

    def frame(self, x, y, w, h, color, t=3):
        self.rect(x, y, w, t, color)
        self.rect(x, y + h - t, w, t, color)
        self.rect(x, y, t, h, color)
        self.rect(x + w - t, y, t, h, color)

    def circle(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy) <= r * r:
                    self.set(xx, yy, color)

    def ring(self, cx, cy, r, color, t=4):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d = (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy)
                if (r - t) * (r - t) <= d <= r * r:
                    self.set(xx, yy, color)

    def line(self, x0, y0, x1, y1, color, t=4):
        steps = max(abs(x1 - x0), abs(y1 - y0), 1)
        for s in range(steps + 1):
            x = x0 + (x1 - x0) * s // steps
            y = y0 + (y1 - y0) * s // steps
            self.rect(x - t // 2, y - t // 2, t, t, color)

    def text(self, x, y, s, scale, color):
        cx = x
        for ch in s.upper():
            glyph = FONT.get(ch, FONT[" "])
            for row in range(7):
                for col in range(5):
                    if glyph[row][col] == "#":
                        self.rect(cx + col * scale, y + row * scale, scale, scale, color)
            cx += 6 * scale
        return cx - x

    def text_w(self, s, scale):
        return len(s) * 6 * scale - scale

    def centered(self, y, s, scale, color):
        x = (W - self.text_w(s, scale)) // 2
        self.text(x, y, s, scale, color)

    def wrap(self, x, y, s, scale, color, max_w, leading=None):
        if leading is None:
            leading = 9 * scale
        words = s.upper().split()
        lines = []
        cur = ""
        for word in words:
            trial = (cur + " " + word).strip()
            if self.text_w(trial, scale) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        for i, ln in enumerate(lines):
            self.text(x, y + i * leading, ln, scale, color)
        return y + len(lines) * leading

    def png_bytes(self):
        raw = bytearray()
        stride = W * 3
        for y in range(H):
            raw.append(0)
            raw += self.px[y * stride:(y + 1) * stride]

        def chunk(kind, data):
            body = kind + data
            return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

        ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
        return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
                + chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b""))


def icon_drone(c, x, y, color):
    c.line(x, y, x + 64, y + 64, color, 5)
    c.line(x + 64, y, x, y + 64, color, 5)
    for dx, dy in [(0, 0), (64, 0), (0, 64), (64, 64)]:
        c.ring(x + dx, y + dy, 13, color, 4)
    c.circle(x + 32, y + 32, 9, color)


def icon_tariff(c, x, y, color):
    c.frame(x, y + 14, 72, 48, color, 5)
    c.line(x + 12, y + 14, x + 12, y + 62, color, 4)
    c.line(x + 36, y + 14, x + 36, y + 62, color, 4)
    c.line(x + 60, y + 14, x + 60, y + 62, color, 4)
    c.text(x + 6, y + 66, "40%", 2, color)


def icon_shield(c, x, y, color):
    c.rect(x + 6, y, 60, 10, color)
    c.rect(x + 6, y, 8, 44, color)
    c.rect(x + 58, y, 8, 44, color)
    c.line(x + 10, y + 44, x + 36, y + 74, color, 7)
    c.line(x + 62, y + 44, x + 36, y + 74, color, 7)
    c.line(x + 20, y + 28, x + 32, y + 40, color, 5)
    c.line(x + 32, y + 40, x + 54, y + 16, color, 5)


def icon_coin(c, x, y, color):
    c.ring(x + 36, y + 36, 34, color, 6)
    c.text(x + 14, y + 22, "ECB", 3, color)


def icon_storm(c, x, y, color):
    c.circle(x + 24, y + 28, 16, color)
    c.circle(x + 48, y + 28, 18, color)
    c.rect(x + 8, y + 28, 56, 14, color)
    c.line(x + 40, y + 46, x + 28, y + 66, GOLD, 6)
    c.line(x + 28, y + 66, x + 44, y + 66, GOLD, 6)
    c.line(x + 44, y + 66, x + 32, y + 84, GOLD, 6)


def icon_cross(c, x, y, color):
    c.ring(x + 36, y + 36, 33, color, 5)
    c.rect(x + 30, y + 14, 12, 44, color)
    c.rect(x + 14, y + 30, 44, 12, color)


def icon_virus(c, x, y, color):
    c.circle(x + 36, y + 36, 17, color)
    for dx, dy in [(-30, -30), (0, -34), (30, -30), (34, 0), (30, 30), (0, 34), (-30, 30), (-34, 0)]:
        c.line(x + 36, y + 36, x + 36 + dx, y + 36 + dy, color, 4)
        c.circle(x + 36 + dx, y + 36 + dy, 5, color)


def icon_ship(c, x, y, color):
    c.line(x + 6, y + 40, x + 66, y + 40, color, 6)
    c.line(x + 6, y + 40, x + 18, y + 58, color, 6)
    c.line(x + 66, y + 40, x + 54, y + 58, color, 6)
    c.line(x + 18, y + 58, x + 54, y + 58, color, 6)
    c.rect(x + 26, y + 20, 20, 20, color)
    for i in range(3):
        c.line(x + 2 + i * 24, y + 70, x + 18 + i * 24, y + 70, SKY, 5)


def panel(c, x, y, w, h, tag, tag_color, head, body, icon):
    c.rect(x, y, w, h, CARD)
    c.frame(x, y, w, h, LINE, 2)
    c.rect(x, y, w, 8, tag_color)
    c.text(x + 18, y + 18, tag, 2, tag_color)
    icon(c, x + w - 96, y + 16, tag_color)
    yy = c.wrap(x + 18, y + 48, head, 3, INK, w - 120)
    c.wrap(x + 18, yy + 4, body, 2, MUTED, w - 36)


def build():
    c = Canvas()
    # Masthead
    c.rect(0, 0, W, 148, NAVY)
    c.centered(22, "THURSDAY 26 NOVEMBER 2026", 5, (255, 255, 255))
    c.centered(84, "THE WORLD IN ONE DAY", 3, (255, 214, 120))
    c.rect(0, 148, W, 6, RED)

    # Lead story
    c.rect(28, 172, 968, 196, CARD)
    c.frame(28, 172, 968, 196, LINE, 2)
    c.rect(28, 172, 968, 10, RED)
    c.text(52, 196, "KUWAIT - MIDDLE EAST", 2, RED)
    icon_drone(c, 880, 196, RED)
    yy = c.wrap(52, 228, "Drone strike kills two Italians in Kuwait", 4, INK, 800)
    c.wrap(52, yy + 6, "Italy blames Iran. Tehran denies it and offers a joint probe.", 2, MUTED, 800)

    # Grid: two columns, three rows (sized so the footer strip fits)
    panels = [
        ("WASHINGTON - TRADE", ORANGE, "US proposes tariffs on 14 partners",
         "Up to 40% on China. EU and Japan push back.", icon_tariff),
        ("UKRAINE - WAR", SKY, "Russia and Ukraine trade strikes",
         "Kyiv downs 87 missiles and drones. Trump urges Putin to pull back.", icon_shield),
        ("BRUSSELS - EUROPE", GOLD, "Spain's Hernandez de Cos to lead ECB",
         "First Spaniard to run the euro central bank, from Feb 2027.", icon_coin),
        ("USA - WEATHER", NAVY, "Storms snarl Thanksgiving travel",
         "800,000+ lose power. Macy's 100th parade postponed.", icon_storm),
        ("AFRICA - HEALTH", GREEN, "Cheaper HIV jab reaches Africa",
         "Twice-yearly lenacapavir, nearly 100% effective.", icon_cross),
        ("DR CONGO - HEALTH", PURPLE, "Ebola cases pass 12,000",
         "Second-largest outbreak on record. Fighting hampers aid.", icon_virus),
    ]
    x0, y0, pw, ph, gap = 28, 384, 474, 162, 14
    for i, (tag, col, head, body, icon) in enumerate(panels):
        x = x0 + (i % 2) * (pw + gap)
        y = y0 + (i // 2) * (ph + gap)
        panel(c, x, y, pw, ph, tag, col, head, body, icon)

    # Footer strip: one more story + dateline
    fy = y0 + 3 * ph + 2 * gap + 14
    c.rect(28, fy, 968, 84, INK)
    icon_ship(c, 52, fy + 4, (255, 255, 255))
    c.text(160, fy + 16, "IBIZA: DIESEL TANKER CAPSIZES, ONE CREW DEAD", 2, (255, 255, 255))
    c.text(160, fy + 46, "26 NOV 2026 - WORLD NEWS IN ONE IMAGE", 2, (255, 214, 120))
    return c


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = build().png_bytes()
    with open(os.path.join(out_dir, "entry.png"), "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()
