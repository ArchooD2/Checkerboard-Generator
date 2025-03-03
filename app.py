from flask import Flask, request, send_file, render_template
from io import BytesIO
from helper import generate_checkerboard_image, generate_chevron_image, generate_diagonal_image

app = Flask(__name__)

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

@app.route("/chevron", methods=["GET"])
def chevron():
    """Generate and download the chevron image."""
    hex_color1 = request.args.get("color1", "#ffffff")
    hex_color2 = request.args.get("color2")
    stripe_width = int(request.args.get("stripe_width", 20))

    try:
        img = generate_chevron_image(hex_color1, hex_color2, stripe_width=stripe_width, rotation=90)
        img_buffer = BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        file_name = f"chevron_{hex_color1[1:]}"
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

@app.route("/diagonal", methods=["GET"])
def diagonal():
    """Generate and download the diagonal image."""
    hex_color1 = request.args.get("color1", "#ffffff")
    hex_color2 = request.args.get("color2")
    stripe_width = int(request.args.get("stripe_width", 20))

    try:
        img = generate_diagonal_image(hex_color1, hex_color2, stripe_width=stripe_width)
        img_buffer = BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        file_name = f"diagonal_{hex_color1[1:]}"
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
