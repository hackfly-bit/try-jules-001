# PDF to Markdown Converter with OCR

This script converts a PDF file into a Markdown file. It uses a hybrid approach:
1.  It first tries to extract text directly from the PDF. This works best for PDFs that are text-based.
2.  If a page contains no extractable text (i.e., it's an image), the script uses Optical Character Recognition (OCR) to detect and extract text.

The final output is a single Markdown file where the content of each page is separated by a heading.

## Dependencies

This project requires Python 3.6+ and a few external software packages.

### 1. Python Libraries

Install the required Python libraries using pip:
```bash
pip install -r requirements.txt
```

### 2. External Software

You also need to install **Tesseract-OCR** (for OCR) and **Poppler** (for PDF to image conversion).

#### On Debian/Ubuntu (Linux)
```bash
sudo apt-get update
sudo apt-get install -y tesseract-ocr poppler-utils
```

#### On Fedora/CentOS/RHEL (Linux)
```bash
sudo dnf install -y tesseract poppler-utils
```

#### On macOS (using Homebrew)
```bash
brew install tesseract poppler
```

#### On Windows
1.  **Tesseract-OCR**:
    *   Download and run the installer from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).
    *   During installation, make sure to check the option to add Tesseract to your system's PATH. If you forget, you'll need to add it manually (e.g., `C:\Program Files\Tesseract-OCR`).
2.  **Poppler**:
    *   Download the latest Poppler binary from [this page](http://blog.alivate.com.au/poppler-windows/).
    *   Extract the archive (e.g., to `C:\poppler-23.11.0`).
    *   Add the `bin` directory from the extracted folder (e.g., `C:\poppler-23.11.0\bin`) to your system's PATH.

## How to Run

Use the command-line interface to specify the input PDF file and the desired output path.

### Basic Usage

```bash
python pdf_to_markdown_converter.py --input path/to/your/file.pdf --output path/to/your/output.md
```

### Example

If you have a PDF named `report.pdf` in the same directory as the script:

```bash
python pdf_to_markdown_converter.py --input report.pdf --output report.md
```

The script will create a file named `report.md` with the converted content. Each page from the PDF will be separated by a header like `## Page 1`, `## Page 2`, etc.