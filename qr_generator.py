#!/usr/bin/env python3

import argparse
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
import os

def generate_qr_code(url, output_format='png'):
    # Validate output format
    valid_formats = ['png', 'jpeg', 'pdf']
    if output_format.lower() not in valid_formats:
        raise ValueError(f"Invalid format. Must be one of: {', '.join(valid_formats)}")

    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Add data
    qr.add_data(url)
    qr.make(fit=True)

    # Create image with rounded corners
    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        fill_color="black",
        back_color="white"
    )

    # Generate output filename if not provided
    if not output_file:
        output_file = f"qr_code.{output_format.lower()}"
    else:
        # Ensure the output file has the correct extension
        if not output_file.lower().endswith(f".{output_format.lower()}"):
            output_file = f"{output_file}.{output_format.lower()}"

    # Save the image
    if output_format.lower() == 'pdf':
        # Convert to PDF using PIL
        img.save(output_file, "PDF", resolution=100.0)
    else:
        img.save(output_file, output_format.upper())

    print(f"QR code generated successfully and saved as {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Generate QR code for a given URL')
    parser.add_argument('url', nargs='?', help='URL to encode in QR code')
    parser.add_argument('--url', dest='url_arg', help='URL to encode in QR code')
    parser.add_argument('--format', choices=['png', 'jpeg', 'pdf'], default='png',
                      help='Output format (default: png)')
    
    args = parser.parse_args()

    # Get URL from either positional argument or --url option
    url = args.url_arg or args.url
    if not url:
        parser.error("URL is required. Please provide it as a positional argument or using --url")

    try:
        generate_qr_code(url, args.format)
    except Exception as e:
        print(f"Error generating QR code: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main() 