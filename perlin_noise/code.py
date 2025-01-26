# SPDX-FileCopyrightText: 2025 Mathias DPX <mathias@mathiasd.fr>
# SPDX-License-Identifier: CC-BY-SA-4.0

import random
import time
import board
import displayio
import framebufferio
import rgbmatrix

FRAMERATE = 1/4 # 4 frames per sec
SEED = random.randint(0, 1000)
PALETTE = [0x000000, 0x1D1D1D, 0x3A3A3A, 0x575757, 0x747474, 0x919191, 0xAEAEAE, 0xCBCBCB, 0xE8E8E8, 0xFFFFFF]

class PerlinNoise:
    def __init__(self, seed=None):
        self.seed = seed or SEED
        random.seed(self.seed)
        self.p = list(range(256))
        random.shuffle(self.p)
        self.p += self.p

    def noise(self, x, y):
        X = int(x) & 255
        Y = int(y) & 255
        x -= int(x)
        y -= int(y)
        
        u = self._fade(x)
        v = self._fade(y)
        
        A = self.p[X] + Y
        B = self.p[X+1] + Y
        
        return self._lerp(v, 
            self._lerp(u, 
                self._grad(self.p[A], x, y), 
                self._grad(self.p[B], x-1, y)
            ),
            self._lerp(u, 
                self._grad(self.p[A+1], x, y-1), 
                self._grad(self.p[B+1], x-1, y-1)
            )
        )

    def _fade(self, t):
        return t * t * t * (t * (t * 6 - 15) + 10)

    def _lerp(self, t, a, b):
        return a + t * (b - a)

    def _grad(self, hash, x, y):
        h = hash & 15
        grad_x = 1 if h < 8 else -1
        grad_y = 1 if h < 4 else (2 if h == 12 or h == 14 else -1)
        return grad_x * x + grad_y * y

displayio.release_displays()

matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=1,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1)

display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

# Generate palette
bitmap = displayio.Bitmap(display.width, display.height, len(PALETTE))
palette = displayio.Palette(len(PALETTE))
for i in range(len(PALETTE)):
    palette[i] = int(str(PALETTE[i]))

tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
group = displayio.Group()
group.append(tile_grid)
display.root_group = group

noise_y = PerlinNoise()
noise_x = PerlinNoise()

scale_y = 0.05
scale_x = 0.05
z_x = 0
z_y = 0

while True:
    for x in range(display.width):
        for y in range(display.height):
            nx = noise_x.noise(x * scale_x + z_x, y * scale_x) # X movements
            ny = noise_y.noise(x * scale_y, y * scale_y + z_y) # Y movements
            
            n = (nx + ny) / 2
            color_index = min(max(int(((n + 1) / 2) * len(PALETTE)-1), 0), len(PALETTE)-1)
            bitmap[x, y] = color_index
    
    display.refresh()
    z_x += 0.1
    z_y += 0.1
    time.sleep(FRAMERATE)