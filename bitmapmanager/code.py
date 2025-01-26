# SPDX-FileCopyrightText: 2025 Mathias DPX <mathias@mathiasd.fr>
# SPDX-License-Identifier: CC-BY-SA-4.0

import board
import displayio
import framebufferio
import rgbmatrix
from colormanager import BitmapManager

displayio.release_displays()

# Initialize the display
matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=1,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1)
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=True)
bitmap = displayio.Bitmap(display.width, display.height, 65535)
palette = displayio.Palette(65535)
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
group = displayio.Group(scale=1)
group.append(tile_grid)
display.root_group = group

manager = BitmapManager(bitmap, palette)

manager.fill(0x000000)

import time
for x in range(64):
    for y in range(32):
        manager.place(x,y , 0x2E5984)
    time.sleep(0.1)

manager.render_image("image.json")