class TextCleaningService:

    def clean(self, text: str):

        text = text.replace("\n", " ")
        text = text.replace("\t", " ")

        while "  " in text:
            text = text.replace("  ", " ")

        return text.strip()