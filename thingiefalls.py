from flask import Flask, request, send_file, render_template
from PIL import Image
import numpy as np
from io import BytesIO

app = Flask(__name__)

def generate_checkerboard_image(hex_code, width=200, height=200, square_size=50):
    """Generate a checkerboard pattern as an in-memory image."""
    color = tuple(int(hex_code[i:i+2], 16) for i in (1, 3, 5)) + (255,)  # Add alpha
    alt_color = (0, 0, 0, 0)  # Transparent

    rows, cols = height // square_size, width // square_size
    pattern = np.indices((rows, cols)).sum(axis=0) % 2
    img_data = np.zeros((height, width, 4), dtype=np.uint8)

    for y in range(rows):
        for x in range(cols):
            color_to_use = color if pattern[y, x] == 0 else alt_color
            img_data[y * square_size:(y + 1) * square_size, x * square_size:(x + 1) * square_size] = color_to_use

    return Image.fromarray(img_data)

@app.route("/")
def home():
    """Render the main page."""
    return render_template("index.html")

@app.route("/checkerboard", methods=["GET"])
def checkerboard():
    """Generate and download the checkerboard image."""
    hex_code = request.args.get("color", "#ff0000")
    try:
        # Validate hex code
        if len(hex_code) != 6 or any(c not in "0123456789abcdefABCDEF" for c in hex_code[1:]):
            return "Invalid color code! Use format: RRGGBB", 400

        # Generate image
        img = generate_checkerboard_image(hex_code)
        img_buffer = BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        # Download image
        return send_file(
            img_buffer,
            mimetype="image/png",
            as_attachment=True,
            download_name=f"checkerboard_{hex_code.strip('#')}.png"
        )
    except Exception as e:
        return f"Error: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
