import os
from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageEnhance, ImageOps

def resize_image(image, width, height):
    """Resizes an image to the given width and height."""
    return image.resize((width, height))

def rotate_image(image, angle):
    """Rotates the image by a specified angle."""
    return image.rotate(angle)

def crop_image(image, box):
    """Crops the image to the specified box (x1, y1, x2, y2)."""
    return image.crop(box)

def convert_to_grayscale(image):
    """Converts an image to grayscale."""
    return image.convert("L")

def apply_blur(image, radius=2):
    """Applies Gaussian blur to the image."""
    return image.filter(ImageFilter.GaussianBlur(radius))

def adjust_brightness(image, factor):
    """Adjusts brightness using a given factor (1.0 = original, <1.0 = darker, >1.0 = brighter)."""
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def invert_colors(image):
    """Inverts the colors of an image."""
    return ImageOps.invert(image)

def add_text(image, text, position, font_size):
    """Adds text overlay to an image at the specified position."""
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
    draw.text(position, text, font=font, fill="white")
    return image

def process_image(image_path, operations, output_directory):
    """Applies a sequence of operations to an image and saves the output."""
    image = Image.open(image_path)
    output_format = None  # Default format is the same as the input

    for operation in operations:
        op_type = operation["type"]

        if op_type == "resize":
            image = resize_image(image, operation["width"], operation["height"])
        elif op_type == "rotate":
            image = rotate_image(image, operation["angle"])
        elif op_type == "crop":
            image = crop_image(image, tuple(operation["box"]))
        elif op_type == "grayscale":
            image = convert_to_grayscale(image)
        elif op_type == "blur":
            image = apply_blur(image, operation.get("radius", 2))
        elif op_type == "brightness":
            image = adjust_brightness(image, operation["factor"])
        elif op_type == "invert":
            image = invert_colors(image)
        elif op_type == "add_text":
            image = add_text(image, operation["text"], tuple(operation["position"]), operation["font_size"])
        elif op_type == "save_format":
            output_format = operation["format"]

    # Determine output file name and format
    file_name = os.path.splitext(os.path.basename(image_path))[0]
    output_extension = output_format if output_format else image.format.lower()
    output_path = os.path.join(output_directory, f"{file_name}.{output_extension}")

    image.save(output_path, format=output_format.upper() if output_format else image.format)
    print(f"Processed and saved: {output_path}")
