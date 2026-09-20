#!/usr/bin/env python3
"""Write simple PNG app icons (stdlib only)."""
import struct
import zlib
from pathlib import Path

BG = (14, 17, 22)
GREEN = (52, 199, 89)
WHITE = (234, 255, 240)

ROOT = Path(__file__).resolve().parent.parent


def chunk(tag: bytes, data: bytes) -> bytes:
    return (
        struct.pack(">I", len(data))
        + tag
        + data
        + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    )


def write_png(path: Path, pixels: list[list[tuple[int, int, int]]]) -> None:
    h = len(pixels)
    w = len(pixels[0])
    raw = b"".join(
        b"\x00" + b"".join(bytes(px) for px in row)
        for row in pixels
    )
    png = b"".join(
        [
            b"\x89PNG\r\n\x1a\n",
            chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)),
            chunk(b"IDAT", zlib.compress(raw, 9)),
            chunk(b"IEND", b""),
        ]
    )
    path.write_bytes(png)


def lerp(a, b, t):
    return int(a + (b - a) * t)


def dist(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def rounded_rect(px, py, cx, cy, hw, hh, r):
    dx = abs(px - cx) - (hw - r)
    dy = abs(py - cy) - (hh - r)
    if dx <= 0 and dy <= 0:
        return True
    if dx <= 0:
        return dy <= r
    if dy <= 0:
        return dx <= r
    return dist(dx, dy, 0, 0) <= r


def on_check(px, py, size):
    """Thick check mark in the center 55% of the icon."""
    # Coordinates in 0..1 of icon
    x = px / (size - 1)
    y = py / (size - 1)
    thickness = 0.075
    # Two segments: (0.28,0.52)->(0.44,0.68) and (0.44,0.68)->(0.74,0.34)
    def near_segment(x1, y1, x2, y2):
        vx, vy = x2 - x1, y2 - y1
        length = (vx * vx + vy * vy) ** 0.5
        if length == 0:
            return False
        t = max(0.0, min(1.0, ((x - x1) * vx + (y - y1) * vy) / (length * length)))
        qx, qy = x1 + t * vx, y1 + t * vy
        return dist(x, y, qx, qy) <= thickness

    return near_segment(0.28, 0.50, 0.44, 0.68) or near_segment(0.42, 0.68, 0.74, 0.32)


def make_icon(size: int) -> list[list[tuple[int, int, int]]]:
    cx = cy = (size - 1) / 2
    hw = hh = size * 0.42
    r = size * 0.18
    pixels = []
    for y in range(size):
        row = []
        for x in range(size):
            if rounded_rect(x, y, cx, cy, hw, hh, r):
                row.append(GREEN if on_check(x, y, size) else tuple(lerp(c, 31, 0.15) for c in GREEN))
                # Recolor: green fill, white check
                if on_check(x, y, size):
                    row[-1] = WHITE
                else:
                    row[-1] = GREEN
            else:
                row.append(BG)
        pixels.append(row)
    return pixels


def main():
    for size, name in ((192, "icon-192.png"), (512, "icon-512.png")):
        write_png(ROOT / name, make_icon(size))
        print("wrote", name)


if __name__ == "__main__":
    main()
