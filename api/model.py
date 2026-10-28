from src.predict import predict

class SentimentClassifier:
    def predict(self, text: str) -> dict:
        return predict(text)
