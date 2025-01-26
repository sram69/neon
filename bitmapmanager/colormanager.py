# SPDX-FileCopyrightText: 2025 Mathias DPX <mathias@mathiasd.fr>
# SPDX-License-Identifier: CC-BY-SA-4.0

import displayio
import json

class BitmapManager:
    def __init__(self, bitmap:displayio.Bitmap, palette=displayio.Palette):
        self.bitmap = bitmap
        self.palette = palette
        self.color_map = {} #hex code : index

    def _get_index_for(self, color):
        index = self.color_map.get(color, None)
        if index != None:
            return index

        if len(self.color_map) >= 65535:
            raise ValueError("Max palette size outreached (max: 65535)")

        index = len(self.color_map)
        print(f"DEBUG: Add 0x{color:06X} to map at {index}")

        self.palette[index] = color
        self.color_map[color] = index
        return index

    def place(self, x, y, color):
        """Place a pixel at (x, y) with the given color."""
        if 0 <= x < self.bitmap.width and 0 <= y < self.bitmap.height:
            self.bitmap[x, y] = self._get_index_for(color)
        else:
            print(f"Out of range ({x};{y})")

    def fill(self, color):
        """Fill the entire display with the given color."""
        for y in range(self.bitmap.height):
            for x in range(self.bitmap.width):
                self.bitmap[x, y] = self._get_index_for(color)

    def render_image(self, img_path, offset_x=0, offset_y=0):
        img = json.load(open(img_path, "r"))
        for y in range(len(img)):
            for x in range(len(img[y])): # Use current line size incase you modify the image
                color = img[y][x]
                if color != -1:
                    self.place(x+offset_x, y+offset_y, color)