import streamlit as st
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
import os
from PIL import Image, ImageColor
import io
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

def generate_qr_code(url, color_input, format="PNG"):
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
    
    # Convert to bytes
    img_byte_arr = io.BytesIO()
    pil_img.save(img_byte_arr, format=format)
    img_byte_arr = img_byte_arr.getvalue()
    
    return img_byte_arr

st.set_page_config(
    page_title="QR Code Generator",
    page_icon="🔲",
    layout="centered"
)

st.title("🔲 QR Code Generator")
st.markdown("Generate QR codes for any URL with customizable options.")

# Input form
with st.form("qr_form"):
    url = st.text_input("Enter URL", placeholder="https://example.com")
    
    # Create two columns for format and color options
    col1, col2 = st.columns(2)
    
    with col1:
        format_choice = st.selectbox(
            "Output Format",
            ["png", "jpeg", "pdf"],
            index=0
        )
    
    with col2:
        color_choice = st.selectbox(
            "Select Color",
            list(COLOR_MAP.keys()),
            index=0
        )
    
    # Filename input on its own line
    filename = st.text_input(
        "Output Filename (without extension)",
        value="qr_code"
    )
    
    submitted = st.form_submit_button("Generate QR Code")

if submitted:
    if not url:
        st.error("Please enter a URL")
    else:
        try:
            # Get the color code
            color_code = COLOR_MAP[color_choice]
            
            # Generate QR code
            qr_code = generate_qr_code(url, color_code, format_choice.lower())
            
            # Display the QR code
            st.image(qr_code, caption="Generated QR Code", width=200)

            # Generate output filename
            output_file = f"{filename}.{format_choice.lower()}"

            # Save the image to a bytes buffer
            img_buffer = io.BytesIO()
            if format_choice.lower() == 'pdf':
                img_buffer.write(qr_code)
                mime_type = "application/pdf"
            else:
                img_buffer.write(qr_code)
                mime_type = f"image/{format_choice}"

            # Create download button
            st.download_button(
                label="Download QR Code",
                data=img_buffer.getvalue(),
                file_name=output_file,
                mime=mime_type
            )

            # Log success
            logger.info(f"Successfully generated QR code for URL: {url} with color: {color_code}")

        except Exception as e:
            error_msg = f"Error generating QR code: {str(e)}"
            st.error(error_msg)
            logger.error(error_msg)

# Add some helpful information
st.markdown("""
### How to use:
1. Enter the URL you want to encode
2. Choose your preferred output format (PNG, JPEG, or PDF)
3. Optionally specify a custom filename
4. Select a color for the QR code
5. Click "Generate QR Code"
6. Download your QR code

### Tips:
- The QR code will be generated with rounded corners for better aesthetics
- PNG format is recommended for best quality
- The QR code uses error correction level L (7% of data can be restored)
- Choose colors with good contrast against white background for better scanning
""")

# Color examples
st.markdown("### Color Examples")
st.markdown("You can use either color names or hex codes:")
st.markdown("""
- Color names: `red`, `blue`, `green`, `purple`, `orange`, etc.
- Hex codes: `#FF0000`, `#0000FF`, `#00FF00`, etc.
""")

# Available colors
st.markdown("### Available Color Names")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    - black
    - white
    - red
    - green
    - blue
    - yellow
    """)
with col2:
    st.markdown("""
    - purple
    - orange
    - pink
    - brown
    - gray
    - cyan
    """)
with col3:
    st.markdown("""
    - magenta
    - lime
    - maroon
    - navy
    - olive
    - teal
    """) 