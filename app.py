from flask import Flask, request, send_file, render_template
from PIL import Image
import numpy as np
from io import BytesIO

app = Flask(__name__)


def generate_checkerboard_image(
    hex_color1, hex_color2=None, width=200, height=200, square_size=50
):
    """Generate a checkerboard pattern as an in-memory image."""
    color1 = tuple(int(hex_color1[i : i + 2], 16) for i in (1, 3, 5)) + (
        255,
    )  # Add full opacity
    color2 = (0, 0, 0, 0)  # Default to fully transparent
    if hex_color2:
        color2 = tuple(int(hex_color2[i : i + 2], 16) for i in (1, 3, 5)) + (
            255,
        )  # Add full opacity if specified

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


@app.route("/")
def home():
    """Render the main page."""
    return render_template("index.html")


@app.route("/checkerboard", methods=["GET"])
def checkerboard():
    """Generate and download the checkerboard image."""
    hex_color1 = request.args.get("color1", "#ffffff")
    hex_color2 = request.args.get("color2")  # Default is None
    use_second_color = request.args.get("use_second_color")  # Checkbox value

    try:
        for color in [hex_color1, hex_color2]:
            if color and (
                len(color) != 7
                or not color.startswith("#")
                or any(c not in "0123456789abcdefABCDEF" for c in color[1:])
            ):
                return "Invalid color code! Use format: #RRGGBB", 400

        # Only use the second color if the checkbox is checked
        if use_second_color != "on":
            hex_color2 = None

        img = generate_checkerboard_image(hex_color1, hex_color2)
        img_buffer = BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        file_name = f"checkerboard_{hex_color1[1:]}"
        if hex_color2:
            file_name += f"_{hex_color2[1:]}"
        file_name += ".png"
        return send_file(
            img_buffer,
            mimetype="image/png",
            as_attachment=True,
            download_name=file_name,
        )
    except Exception as e:
        return f"Error: {e}", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
