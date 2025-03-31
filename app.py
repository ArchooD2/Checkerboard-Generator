from flask import Flask, request, send_file, render_template
from io import BytesIO
try:
    # If running with Flask CLI (as a package)
    from .helper import (
        generate_checkerboard_image,
        generate_chevron_image,
        generate_diagonal_image,
        generate_stripe_image,
        generate_radial_pattern,
        generate_diagonal_checker_image
    )
except ImportError:
    # If running directly (e.g. `python app.py`)
    from helper import (
        generate_checkerboard_image,
        generate_chevron_image,
        generate_diagonal_image,
        generate_stripe_image,
        generate_radial_pattern,
        generate_diagonal_checker_image
    )

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



@app.route("/stripes", methods=["GET"])
def stripes():
    """Generate and download the stripe image."""
    hex_color1 = request.args.get("color1", "#ffffff")
    hex_color2 = request.args.get("color2")
    stripe_width = int(request.args.get("stripe_width", 20))
    orientation = request.args.get("orientation", "horizontal")

    try:
        img = generate_stripe_image(hex_color1, hex_color2, stripe_width=stripe_width, orientation=orientation)
        img_buffer = BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        file_name = f"stripes_{orientation}_{hex_color1[1:]}"
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
    
@app.route("/radial", methods=["GET"])
def radial():
    """Generate and download a radial pattern image."""
    hex_color1 = request.args.get("color1", "#ffffff")
    hex_color2 = request.args.get("color2")
    ring_width = int(request.args.get("ring_width", 20))

    try:
        img = generate_radial_pattern(hex_color1, hex_color2, ring_width=ring_width)
        img_buffer = BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        file_name = f"radial_{hex_color1[1:]}"
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

@app.route("/diagonalchecker", methods=["GET"])
def diagonalChecker():
    """Generate and download a diagonal-striped pattern masked by a checkerboard."""
    hex_color1 = request.args.get("color1", "#ffffff")
    hex_color2 = request.args.get("color2")
    stripe_width = int(request.args.get("stripe_width", 20))
    square_size = int(request.args.get("square_size", 50))

    try:
        img = generate_diagonal_checker_image(
            hex_color1, hex_color2, stripe_width=stripe_width, square_size=square_size
        )
        img_buffer = BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        file_name = f"diagonal_checker_{hex_color1[1:]}"
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

