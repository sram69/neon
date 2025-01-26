# Bitmap Manager
Used for simplify pixels placements

# Docs

### `_get_index_for(color: hex) -> int`
- Manages color indices in palette
- If color exists: returns existing index
- If color new: 
  - Adds to palette
  - Assigns next available index
- Raises `ValueError` if palette exceeds 65,535 colors
- Returns palette index for given color

### `place(x: int, y: int, color: hex)`
- Places single pixel at (x, y)

### `fill(color: hex)`
- Fills entire bitmap with single color

### `render_image(img_path: str, offset_x: int = 0, offset_y: int = 0)`
- Place an image loaded from a json made with image_preprocessor.py