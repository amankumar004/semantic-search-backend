from pypdf import PdfReader

class PDFService:
    def extract_text_from_pdf(self, file_path):
        """
        Extracts text from a PDF file.

        :param pdf_path: Path to the PDF file.
        :return: Extracted text as a string.
        """
        # Implementation for extracting text from PDF
        reader = PdfReader(file_path)
        text = ""
        
        for page in reader.pages:
            text += page.extract_text()
            
        return text.strip()