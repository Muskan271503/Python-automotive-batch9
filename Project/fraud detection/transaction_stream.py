import random
import time
from fraud_model import FraudDetector


def generate_transaction():
    return {
        "amount": random.choice([50, 100, 200, 500, 10000]),
        "hour": random.randint(0, 23),
        "location_change": random.choice([0, 1]),
        "txn_frequency": random.randint(1, 20)
    }


if __name__ == "__main__":
    detector = FraudDetector()

    print("\n--- Real-Time Fraud Detection Started ---\n")

    for i in range(20):
        txn = generate_transaction()
        score = detector.score_transaction(txn)
        fraud = detector.is_fraud(txn)

        print(f"Transaction {i+1}: {txn}")
        print(f"Fraud Score: {score:.3f}")

        if fraud:
            print("🚨 Suspicious Transaction Detected")
        else:
            print("✅ Transaction is Normal")

        detector.learn(txn)
        print("-" * 50)
        time.sleep(0.5)
