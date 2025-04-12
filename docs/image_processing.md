# Image Processing with StarBot

StarBot now supports extracting text from images using Optical Character Recognition (OCR). This allows you to use images as data sources for your chatbot.

## Prerequisites

Before using the image processing capabilities, you need to install the required dependencies:

1. Install Python packages:
   ```bash
   pip install pytesseract Pillow
   ```

2. Install Tesseract OCR engine:
   - **Windows**: Download and install from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
   - **Linux**: `sudo apt-get install tesseract-ocr`
   - **macOS**: `brew install tesseract`

## Using Images as Data Sources

### From Python Code

You can use images as data sources in your Python code:

```python
from starbot.data.ingestion import DataIngestion

# Initialize the data ingestion module
data_ingestion = DataIngestion()

# Process a single image
documents = data_ingestion.ingest_image("path/to/image.jpg")

# Process all images in a directory
documents = data_ingestion.ingest_image_directory("path/to/images/")

# Process multiple data sources including images
documents = data_ingestion.ingest_multiple_sources(
    text_files=["path/to/file.txt"],
    pdf_files=["path/to/document.pdf"],
    image_files=["path/to/image.jpg"],
    urls=["https://example.com"],
    directories=["path/to/text_files/"],
    image_directories=["path/to/images/"]
)

# Create a vector store from the documents
vector_store = data_ingestion.create_vector_store(documents, "my-collection")
```

### Using the Example Scripts

StarBot includes example scripts to demonstrate image processing:

1. **Image Extraction Example**:
   ```bash
   python examples/image_extraction_example.py --image path/to/image.jpg
   ```
   
   Or process a directory of images:
   ```bash
   python examples/image_extraction_example.py --image_dir path/to/images/
   ```

2. **Mixed Data Sources Example**:
   ```bash
   python examples/mixed_data_sources_example.py --image path/to/image.jpg --url https://example.com
   ```

## Best Practices for Image Processing

For optimal results with OCR:

1. **Use High-Quality Images**: Higher resolution images yield better OCR results
2. **Good Contrast**: Black text on white background works best
3. **Clean Images**: Avoid images with background patterns, watermarks, or noise
4. **Proper Orientation**: Text should be properly oriented (not sideways or upside down)
5. **Common Fonts**: Standard fonts are recognized more accurately than decorative ones

## Supported Image Formats

StarBot supports the following image formats:
- JPEG/JPG
- PNG
- GIF
- BMP
- TIFF

## Language Support

By default, StarBot uses English for OCR, but you can specify other languages:

```python
# Process an image with French text
documents = data_ingestion.ingest_image("path/to/french_text.jpg", language="fra")
```

Common language codes:
- `eng`: English
- `fra`: French
- `deu`: German
- `spa`: Spanish
- `ita`: Italian
- `por`: Portuguese
- `ara`: Arabic
- `hin`: Hindi
- `chi_sim`: Simplified Chinese
- `chi_tra`: Traditional Chinese
- `jpn`: Japanese
- `kor`: Korean

For a complete list of supported languages, refer to the [Tesseract documentation](https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html).

## Limitations

- OCR accuracy depends on image quality and text clarity
- Processing large images or many images can be slow
- Some fonts or special characters may not be recognized correctly
- Handwritten text has lower recognition accuracy
