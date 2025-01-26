import time
import json
import board
import requests
import displayio
import framebufferio
import rgbmatrix
from colormanager import BitmapManager

displayio.release_displays()

def get_bikes(id="cdifas3e02ej882u550g"):
    try:
        r = requests.get("https://gbfs.partners.fifteen.eu/gbfs/2.2/landerneau/en/station_status.json")
        for station in r.json()["data"]["stations"]:
            if station["station_id"] != id: continue
            return str(station["num_bikes_available"])
    except: pass        
    return "?"

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

numbers = json.load(open("numbers.json", "r"))

while True:
    available = get_bikes()    
    
    manager.render_image_file("image.json")
    manager.render_image_data(numbers[available], offset_x=9, offset_y=16)
    time.sleep(60)