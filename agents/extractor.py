import pypdf
import os

class PDFExtractorAgent:
    def extract_text(self, pdf_path):
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                reader = pypdf.PdfReader(file)
                for page in reader.pages[:3]:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"PDF extraction error: {e}")
        return text