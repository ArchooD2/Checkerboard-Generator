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

def generate_chevron_image(hex_color1, hex_color2=None, width=200, height=200, stripe_width=20, rotation=90):
    """Generate a chevron pattern with optional rotation."""
    # Parse colors
    color1 = tuple(int(hex_color1[i : i + 2], 16) for i in (1, 3, 5)) + (255,)
    color2 = (0, 0, 0, 0)  # Transparent by default
    if hex_color2:
        color2 = tuple(int(hex_color2[i : i + 2], 16) for i in (1, 3, 5)) + (255,)

    # Create the base chevron pattern
    img_data = np.zeros((height, width, 4), dtype=np.uint8)
    mid_x = width // 2  # Vertical midpoint for mirroring

    for y in range(height):
        for x in range(width):
            mirrored_x = abs(mid_x - x)
            stripe = ((mirrored_x + y) // stripe_width) % 2
            img_data[y, x] = color1 if stripe == 0 else color2

    chevron_img = Image.fromarray(img_data, mode="RGBA")

    # Rotate the image if requested
    if rotation != 0:
        chevron_img = chevron_img.rotate(rotation, expand=True)

    return chevron_img

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


def generate_stripe_image(hex_color1, hex_color2=None, width=200, height=200, stripe_width=20, orientation='horizontal'):
    """Generate a striped pattern as an in-memory image."""
    color1 = tuple(int(hex_color1[i : i + 2], 16) for i in (1, 3, 5)) + (255,)
    color2 = (0, 0, 0, 0)
    if hex_color2:
        color2 = tuple(int(hex_color2[i : i + 2], 16) for i in (1, 3, 5)) + (255,)

    img_data = np.zeros((height, width, 4), dtype=np.uint8)

    if orientation == 'horizontal':
        for y in range(height):
            stripe = (y // stripe_width) % 2
            img_data[y, :] = color1 if stripe == 0 else color2
    elif orientation == 'vertical':
        for x in range(width):
            stripe = (x // stripe_width) % 2
            img_data[:, x] = color1 if stripe == 0 else color2
    else:
        raise ValueError("Invalid orientation. Use 'horizontal' or 'vertical'.")
    return Image.fromarray(img_data, mode="RGBA")

def generate_radial_pattern(hex_color1, hex_color2=None, width=200, height=200, ring_width=20):
    """Generate a radial pattern of concentric circles as an in-memory image."""
    import math

    color1 = tuple(int(hex_color1[i : i + 2], 16) for i in (1, 3, 5)) + (255,)
    color2 = (0, 0, 0, 0)
    if hex_color2:
        color2 = tuple(int(hex_color2[i : i + 2], 16) for i in (1, 3, 5)) + (255,)

    img_data = np.zeros((height, width, 4), dtype=np.uint8)
    cx, cy = width // 2, height // 2

    for y in range(height):
        for x in range(width):
            dist = math.hypot(x - cx, y - cy)
            ring = int(dist // ring_width) % 2
            img_data[y, x] = color1 if ring == 0 else color2

    return Image.fromarray(img_data, mode="RGBA")
