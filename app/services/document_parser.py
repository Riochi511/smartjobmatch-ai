import os

from app.services.pdf_parser import PDFParser
from app.services.docx_parser import DOCXParser


class DocumentParser:

    @staticmethod
    def extract_text(file_path):

        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".pdf":
            return PDFParser.extract_text(file_path)

        elif extension == ".docx":
            return DOCXParser.extract_text(file_path)

        raise ValueError(
            f"Unsupported file type: {extension}"
        )