import pytest
from fraud_model import FraudDetector


@pytest.fixture
def detector():
    return FraudDetector(threshold=0.5)


@pytest.fixture
def normal_transaction():
    return {
        "amount": 100,
        "hour": 10,
        "location_change": 0,
        "txn_frequency": 2
    }


@pytest.fixture
def suspicious_transaction():
    return {
        "amount": 10000,
        "hour": 2,
        "location_change": 1,
        "txn_frequency": 15
    }


def test_score_returns_float(detector, normal_transaction):
    score = detector.score_transaction(normal_transaction)
    assert isinstance(score, float)


def test_fraud_detection_returns_boolean(detector, suspicious_transaction):
    result = detector.is_fraud(suspicious_transaction)
    assert isinstance(result, bool)


def test_model_learns_without_error(detector, normal_transaction):
    detector.learn(normal_transaction)
    score_after_learning = detector.score_transaction(normal_transaction)
    assert isinstance(score_after_learning, float)


def test_invalid_transaction_type(detector):
    with pytest.raises(TypeError):
        detector.score_transaction(["invalid", "data"])
