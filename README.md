# QR Code Generator

A web-based QR code generator built with Streamlit that allows you to create customizable QR codes for any URL. The application supports various output formats and color options.

## Features

- Generate QR codes for any URL
- Customizable output formats (PNG, JPEG, PDF)
- Color customization:
  - Predefined basic colors
  - Custom color selection using color picker
- Rounded corners for better aesthetics
- Error correction for better scanning
- Download generated QR codes
- Clean and intuitive user interface

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd qr-code
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

3. In the web interface:
   - Enter the URL you want to encode
   - Select the output format (PNG, JPEG, or PDF)
   - Choose a filename (optional)
   - Select a color for the QR code
   - Click "Generate QR Code"
   - Download the generated QR code

## Available Colors

The application supports the following predefined colors:
- Black
- Blue
- Red
- Green
- Purple
- Orange
- Brown
- Pink
- Gray

You can also use the color picker to select any custom color.

## Output Formats

- PNG (recommended for best quality)
- JPEG
- PDF

## Requirements

- Python 3.7+
- streamlit>=1.24.0
- qrcode[pil]>=7.4.2

## Deployment

This application can be easily deployed to Streamlit Cloud:

1. Create a GitHub repository with your code
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Deploy the application

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [QR Code Python Library](https://github.com/lincolnloop/python-qrcode)
- [Streamlit](https://streamlit.io/)
- [Pillow](https://python-pillow.org/) 