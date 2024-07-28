# import sys
# from docx import Document

# def docxExtract(docxfile):
#     try:
#         document = Document(docxfile)
#     except Exception as e:
#         print("Error opening docx:", e)
#         sys.exit()

#     # Fetch all the text out of the document we just created
#     paratextlist = [para.text for para in document.paragraphs]

#     # Return text of document with two newlines under each paragraph
#     return '\n'.join(paratextlist)

# # Example usage
# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Usage: python extractdocx.py <docx-file>")
#         sys.exit()

#     docxfile = sys.argv[1]
#     try:
#         extracted_text = docxExtract(docxfile)
#         print(extracted_text)
#     except Exception as e:
#         print("An error occurred:", e)

import sys
import fitz  # PyMuPDF

def docxExtract(docxfile):
    try:
        document = fitz.open(docxfile)
        text = ""
        for page in document:
            text += page.get_text()
    except Exception as e:
        print("Error extracting text:", e)
        sys.exit()

    return text

# Example usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extractdocx.py <docx-file>")
        sys.exit()

    docxfile = sys.argv[1]
    print(extract_text_from_docx(docxfile))
