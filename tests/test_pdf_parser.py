from app.services.pdf_parser import PDFParser

text = PDFParser.extract_text("sample_resume.pdf")

print(text)