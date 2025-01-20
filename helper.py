from PIL import Image
import numpy as np

def generate_checkerboard_image(hex_color1, hex_color2=None, width=200, height=200, square_size=50):
    """Generate a checkerboard pattern as an in-memory image."""
    color1 = tuple(int(hex_color1[i : i + 2], 16) for i in (1, 3, 5)) + (255,)  # Add full opacity
    color2 = (0, 0, 0, 0)  # Default to fully transparent
    if hex_color2:
        color2 = tuple(int(hex_color2[i : i + 2], 16) for i in (1, 3, 5)) + (255,)  # Add full opacity if specified

    rows, cols = height // square_size, width // square_size
    img_data = np.zeros((height, width, 4), dtype=np.uint8)  # Use 4 channels for RGBA

    for y in range(rows):
        for x in range(cols):
            color_to_use = color1 if (x + y) % 2 == 0 else color2
            img_data[
                y * square_size : (y + 1) * square_size,
                x * square_size : (x + 1) * square_size,
            ] = color_to_use

    return Image.fromarray(img_data, mode="RGBA")

def generate_chevron_image(hex_color1, hex_color2=None, width=200, height=200, stripe_width=20):
    """Generate a chevron pattern as an in-memory image."""
    color1 = tuple(int(hex_color1[i : i + 2], 16) for i in (1, 3, 5)) + (255,)
    color2 = (0, 0, 0, 0)
    if hex_color2:
        color2 = tuple(int(hex_color2[i : i + 2], 16) for i in (1, 3, 5)) + (255,)

    img_data = np.zeros((height, width, 4), dtype=np.uint8)
    mid_x = width // 2  # Vertical midpoint for mirroring

    for y in range(height):
        for x in range(width):
            mirrored_x = abs(mid_x - x)
            stripe = ((mirrored_x + y) // stripe_width) % 2
            img_data[y, x] = color1 if stripe == 0 else color2

    return Image.fromarray(img_data, mode="RGBA")

def generate_diagonal_image(hex_color1, hex_color2=None, width=200, height=200, stripe_width=20):
    """Generate a diagonal stripe pattern as an in-memory image."""
    color1 = tuple(int(hex_color1[i : i + 2], 16) for i in (1, 3, 5)) + (255,)
    color2 = (0, 0, 0, 0)
    if hex_color2:
        color2 = tuple(int(hex_color2[i : i + 2], 16) for i in (1, 3, 5)) + (255,)

    img_data = np.zeros((height, width, 4), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            stripe = ((x + y) // stripe_width) % 2
            img_data[y, x] = color1 if stripe == 0 else color2

    return Image.fromarray(img_data, mode="RGBA")
