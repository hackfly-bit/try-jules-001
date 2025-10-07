import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os
import argparse

# --- Optional: Set Tesseract and Poppler paths for Windows ---
# If Tesseract or Poppler are not in your system's PATH, you can specify their
# locations here. This is often necessary on Windows.
#
# Example for Windows:
# TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# POPPLER_PATH = r'C:\path\to\poppler-xx.x.x\bin'
#
# if os.name == 'nt': # Check if running on Windows
#     pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

def convert_pdf_to_markdown(pdf_path, output_path, poppler_path=None):
    """
    Converts a PDF file to a Markdown file using a hybrid text extraction and OCR approach.

    Args:
        pdf_path (str): The full path to the input PDF file.
        output_path (str): The full path to save the output Markdown file.
        poppler_path (str, optional): The path to the Poppler 'bin' directory.
                                      Required for pdf2image on Windows.
    """
    if not os.path.exists(pdf_path):
        print(f"Error: Input file not found at '{pdf_path}'")
        return

    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    markdown_content = []

    print(f"Processing {len(pdf_document)} pages from '{os.path.basename(pdf_path)}'...")

    for page_num in range(len(pdf_document)):
        page_index = page_num + 1
        markdown_content.append(f"## Page {page_index}\n")

        page = pdf_document.load_page(page_num)

        # 1. Try to extract text directly
        text = page.get_text("text")

        # 2. If text is minimal, use OCR
        # A small threshold helps decide if the page is image-based.
        if len(text.strip()) < 100:
            print(f"Page {page_index}: Minimal text found. Attempting OCR...")
            try:
                # Convert page to image
                images = convert_from_path(
                    pdf_path,
                    dpi=300,
                    first_page=page_index,
                    last_page=page_index,
                    poppler_path=poppler_path
                )

                if images:
                    # Use Pytesseract to extract text from the image
                    ocr_text = pytesseract.image_to_string(images[0], lang='eng') # Specify language if needed
                    text = ocr_text
                    print(f"Page {page_index}: OCR successful.")
                else:
                    print(f"Page {page_index}: Could not convert page to image.")
                    text = "" # No text could be extracted
            except Exception as e:
                print(f"Page {page_index}: OCR failed with error: {e}")
                text = "*(OCR failed for this page)*"
        else:
            print(f"Page {page_index}: Extracted text directly.")

        # Append the extracted text to our content list
        markdown_content.append(text.strip() + "\n")

    # Write the combined content to the output file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(markdown_content))
        print(f"\nSuccessfully converted PDF to Markdown at: '{output_path}'")
    except IOError as e:
        print(f"Error: Could not write to output file '{output_path}'. Reason: {e}")

    # Close the PDF document
    pdf_document.close()

def main():
    """
    Main function to handle command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Convert a PDF file to a Markdown file using direct text extraction and OCR.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to the input PDF file."
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Path to the output Markdown (.md) file."
    )

    parser.add_argument(
        "--poppler_path",
        required=False,
        default=None,
        help="(Optional for Windows) Path to the Poppler 'bin' directory.\n"
             "Needed if Poppler is not in your system's PATH environment variable."
    )

    args = parser.parse_args()

    # On Windows, if tesseract is not in PATH, uncomment and set the path
    # if os.name == 'nt':
    #     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    convert_pdf_to_markdown(args.input, args.output, args.poppler_path)

if __name__ == "__main__":
    main()