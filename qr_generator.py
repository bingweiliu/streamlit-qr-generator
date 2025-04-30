#!/usr/bin/env python3

import argparse
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from PIL import Image, ImageColor
import io
import sys
from datetime import datetime

# Define color mappings
COLOR_MAP = {
    "black": "#000000",
    "red": "#FF0000",
    "green": "#00FF00",
    "blue": "#0000FF",
    "yellow": "#FFFF00",
    "purple": "#800080",
    "orange": "#FFA500",
    "pink": "#FFC0CB",
    "brown": "#A52A2A",
    "gray": "#808080",
    "cyan": "#00FFFF",
    "magenta": "#FF00FF",
    "lime": "#00FF00",
    "maroon": "#800000",
    "navy": "#000080",
    "olive": "#808000",
    "teal": "#008080",
    "silver": "#C0C0C0"
}

def get_color_hex(color_input):
    """Convert color input to hex color code."""
    # If input is already a hex color code
    if color_input.startswith('#'):
        return color_input
    
    # Convert color name to lowercase for case-insensitive matching
    color_name = color_input.lower()
    
    # Check if the color name exists in our mapping
    if color_name in COLOR_MAP:
        return COLOR_MAP[color_name]
    
    # If not found, try PIL's color name support
    try:
        # This will raise ValueError if color is not recognized
        ImageColor.getrgb(color_name)
        return color_name
    except ValueError:
        raise ValueError(f"Invalid color: {color_input}. Must be a hex color code (e.g., '#FF0000') or a valid color name.")

def generate_qr_code(url, color_input, format="PNG", output_file=None):
    """Generate a QR code with the specified color."""
    # Get the hex color code
    color_hex = get_color_hex(color_input)
    
    # Convert hex to RGB
    rgb_color = ImageColor.getrgb(color_hex)
    print(f"Color '{color_input}' converted to RGB: {rgb_color}")
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Generate image
    img = qr.make_image(
        fill_color=rgb_color,
        back_color="white"
    )
    
    # Get the PIL image
    pil_img = img.get_image()
    
    # Save or return the image
    if output_file:
        pil_img.save(output_file, format=format)
        print(f"QR code saved to {output_file}")
    else:
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        pil_img.save(img_byte_arr, format=format)
        return img_byte_arr.getvalue()

def main():
    parser = argparse.ArgumentParser(description="Generate QR codes with custom colors")
    parser.add_argument("url", help="URL to encode in the QR code")
    parser.add_argument("--color", "-c", default="black", 
                        help="Color for the QR code (name or hex code)")
    parser.add_argument("--format", "-f", choices=["PNG", "JPEG", "PDF"], 
                        default="PNG", help="Output format")
    parser.add_argument("--output", "-o", help="Output filename")
    
    args = parser.parse_args()
    
    try:
        # Generate QR code
        qr_code = generate_qr_code(
            args.url,
            args.color,
            args.format,
            args.output
        )
        
        if not args.output:
            # If no output file specified, save with default name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"qr_code_{timestamp}.{args.format.lower()}"
            with open(output_file, "wb") as f:
                f.write(qr_code)
            print(f"QR code saved to {output_file}")
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 