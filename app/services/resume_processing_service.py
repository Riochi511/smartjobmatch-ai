from fastapi import UploadFile

from app.services.pdf_extraction_service import PDFExtractionService
from app.services.text_cleaning_service import TextCleaningService


class ResumeProcessingService:

    def __init__(self):
        self.pdf_service = PDFExtractionService()
        self.cleaning_service = TextCleaningService()

    def process_resume(self, file: UploadFile):

        if file.content_type != "application/pdf":
            return {
                "error": "Only PDF files are supported for now."
            }

        extracted_text = self.pdf_service.extract_text(file)

        cleaned_text = self.cleaning_service.clean(extracted_text)

        return {
            "filename": file.filename,
            "characters": len(cleaned_text),
            "resume_preview": cleaned_text[:500]
        }