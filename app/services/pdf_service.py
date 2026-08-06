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
        pages = []
        
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                pages.append(page_text)
            
        return "\n".join(pages).strip()