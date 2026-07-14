from pypdf import PdfReader
import io


class PDFExtractionService:

    def extract_text(self, file):

        pdf = PdfReader(io.BytesIO(file.file.read()))

        text = ""

        for page in pdf.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

        return text