import pandas as pd
import pytest

from recommendation_engine import (
    df,
    user_item_matrix,
    recommend_products,
    recommend_similar_products,
    hybrid_recommendation
)

# -------------------------------------------------
# Test 1: Data Availability
# -------------------------------------------------

def test_data_not_empty():
    assert not df.empty

# -------------------------------------------------
# Test 2: User-Item Matrix Creation
# -------------------------------------------------

def test_user_item_matrix_exists():
    assert user_item_matrix.shape[0] > 0
    assert user_item_matrix.shape[1] > 0

# -------------------------------------------------
# Test 3: Collaborative Recommendation (Valid User)
# -------------------------------------------------

def test_recommend_products_valid_user():
    result = recommend_products(1)
    assert isinstance(result, pd.Series)
    assert len(result) <= 3

# -------------------------------------------------
# Test 4: Collaborative Recommendation (Invalid User)
# -------------------------------------------------

def test_recommend_products_invalid_user():
    result = recommend_products(999)
    assert isinstance(result, str)

# -------------------------------------------------
# Test 5: Content-Based Recommendation
# -------------------------------------------------

def test_content_based_recommendation():
    result = recommend_similar_products(101)
    assert isinstance(result, list)
    assert len(result) > 0

# -------------------------------------------------
# Test 6: Content-Based Recommendation (Invalid Product)
# -------------------------------------------------

def test_content_based_invalid_product():
    result = recommend_similar_products(9999)
    assert result == []

# -------------------------------------------------
# Test 7: Hybrid Recommendation (Existing User)
# -------------------------------------------------

def test_hybrid_existing_user():
    result = hybrid_recommendation(3)
    assert isinstance(result, list)

# -------------------------------------------------
# Test 8: Hybrid Recommendation (New User)
# -------------------------------------------------

def test_hybrid_new_user():
    result = hybrid_recommendation(999)
    assert isinstance(result, str)
