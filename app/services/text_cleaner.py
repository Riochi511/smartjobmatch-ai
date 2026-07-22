import re


class TextCleaner:

    @staticmethod
    def clean(text: str) -> str:
        """
        Clean extracted resume text.
        """

        # Remove multiple spaces, tabs and newlines
        text = re.sub(r"\s+", " ", text)

        # Remove leading and trailing spaces
        text = text.strip()

        return text