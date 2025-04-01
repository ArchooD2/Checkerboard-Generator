import pytest
from PIL import Image
try:
    # If running with Flask CLI (as a package)
    from ..helper import (
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

# Common test colors
COLOR1 = "#ffffff"
COLOR2 = "#000000"

def _assert_valid_image(img: Image.Image, expected_size=(200, 200)):
    assert isinstance(img, Image.Image)
    assert img.size == expected_size
    assert img.mode == "RGBA"

def test_checkerboard_generation():
    img = generate_checkerboard_image(COLOR1, COLOR2)
    _assert_valid_image(img)

def test_chevron_generation():
    img = generate_chevron_image(COLOR1, COLOR2, stripe_width=20)
    _assert_valid_image(img)

def test_diagonal_generation():
    img = generate_diagonal_image(COLOR1, COLOR2, stripe_width=20)
    _assert_valid_image(img)

def test_stripe_generation_horizontal():
    img = generate_stripe_image(COLOR1, COLOR2, stripe_width=20, orientation="horizontal")
    _assert_valid_image(img)

def test_stripe_generation_vertical():
    img = generate_stripe_image(COLOR1, COLOR2, stripe_width=20, orientation="vertical")
    _assert_valid_image(img)

def test_stripe_invalid_orientation():
    with pytest.raises(ValueError):
        generate_stripe_image(COLOR1, COLOR2, stripe_width=20, orientation="diagonal")

def test_radial_generation():
    img = generate_radial_pattern(COLOR1, COLOR2, ring_width=20)
    _assert_valid_image(img)

def test_diagonal_checker_generation():
    img = generate_diagonal_checker_image(COLOR1, COLOR2, stripe_width=20, square_size=50)
    _assert_valid_image(img)
