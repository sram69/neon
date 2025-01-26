# SPDX-FileCopyrightText: 2025 Mathias DPX <mathias@mathiasd.fr>
# SPDX-License-Identifier: CC-BY-SA-4.0

"""
Convert an image to a list readable by BitmapManager
"""

output = "image.json"
input = "example.png"
alpha_threshold = 0 # 0 should be good in most case

from PIL import Image
import json

img = Image.open(input).convert("RGBA")

map = []

def rgb_to_color_int(rgb_tuple):
    r, g, b, a = rgb_tuple
    return (r << 16) | (g << 8) | b

for y in range(img.height):
    line = []
    for x in range(img.width):
        color = img.getpixel((x,y))
        if color[-1] > alpha_threshold:
            line.append(rgb_to_color_int(color))
        else:
            line.append(-1)

    map.append(line)

# Remove spaces for file size
content = json.dumps(map)
content = content.replace(" ", "")

with open(output, "w+") as f:
    f.write(content)