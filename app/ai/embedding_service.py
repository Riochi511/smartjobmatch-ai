from app.ai.model_manager import ModelManager


class EmbeddingService:

    @staticmethod
    def embed(text):

        model = ModelManager.get_model()

        embedding = model.encode(text)

        return embedding