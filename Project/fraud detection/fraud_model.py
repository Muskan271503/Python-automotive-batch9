from river import anomaly
from river import preprocessing


class FraudDetector:
    def __init__(self, threshold=0.7):
        self.threshold = threshold

        scaler = preprocessing.StandardScaler()
        model = anomaly.HalfSpaceTrees(
            n_trees=25,
            height=10,
            window_size=250,
            seed=42
        )

        self.model = scaler | model

    def score_transaction(self, transaction: dict):
        if not isinstance(transaction, dict):
            raise TypeError("Transaction must be a dictionary")

        score = self.model.score_one(transaction)

        # Ensure numeric output (River may return int initially)
        return float(score)

    def is_fraud(self, transaction: dict) -> bool:
        score = self.score_transaction(transaction)
        return score > self.threshold

    def learn(self, transaction: dict):
        self.model.learn_one(transaction)
