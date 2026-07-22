from sentence_transformers import SentenceTransformer


class ModelManager:

    _model = None

    @classmethod
    def get_model(cls):

        if cls._model is None:
            cls._model = SentenceTransformer(
                "all-MiniLM-L6-v2",
                device="cpu"
            )

        return cls._model