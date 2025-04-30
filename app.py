import streamlit as st
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
import os
from PIL import Image
import io
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define basic colors
BASIC_COLORS = {
    "Black": "#000000",
    "Blue": "#0000FF",
    "Red": "#FF0000",
    "Green": "#00FF00",
    "Purple": "#800080",
    "Orange": "#FFA500",
    "Brown": "#A52A2A",
    "Pink": "#FFC0CB",
    "Gray": "#808080",
    "Custom": None
}

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
    
    # Create three columns for format, filename, and color options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        format_choice = st.selectbox(
            "Output Format",
            ["png", "jpeg", "pdf"],
            index=0
        )
    
    with col2:
        filename = st.text_input(
            "Output Filename (without extension)",
            value="qr_code"
        )
    
    with col3:
        color_mode = st.selectbox(
            "Color Selection Mode",
            ["Basic Colors", "Custom Color"],
            index=0
        )
    
    # Color selection based on mode
    if color_mode == "Basic Colors":
        color_choice = st.selectbox(
            "Select Color",
            list(BASIC_COLORS.keys()),
            index=0
        )
        if color_choice == "Custom":
            color_code = st.color_picker("Pick a color", "#000000")
        else:
            color_code = BASIC_COLORS[color_choice]
    else:
        color_code = st.color_picker("Pick a color", "#000000")
    
    submitted = st.form_submit_button("Generate QR Code")

if submitted:
    if not url:
        st.error("Please enter a URL")
    else:
        try:
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

            # Create image with rounded corners and custom color
            img = qr.make_image(
                image_factory=StyledPilImage,
                module_drawer=RoundedModuleDrawer(),
                fill_color=color_code,
                back_color="white"
            )

            # Convert to PIL Image for display and saving
            pil_img = img.get_image()

            # Display the QR code
            st.image(pil_img, caption="Generated QR Code", use_container_width=True)

            # Generate output filename
            output_file = f"{filename}.{format_choice.lower()}"

            # Save the image to a bytes buffer
            img_buffer = io.BytesIO()
            if format_choice.lower() == 'pdf':
                pil_img.save(img_buffer, format="PDF", resolution=100.0)
                mime_type = "application/pdf"
            else:
                pil_img.save(img_buffer, format=format_choice.upper())
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
5. Click 'Generate QR Code'
6. Download your QR code

### Tips:
- The QR code will be generated with rounded corners for better aesthetics
- PNG format is recommended for best quality
- The QR code uses error correction level L (7% of data can be restored)
- Choose colors with good contrast against white background for better scanning
""") 