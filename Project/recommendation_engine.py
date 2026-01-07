import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# -------------------------------------------------
# Step 1: Mock User Activity Data
# -------------------------------------------------

data = {
    "user_id": [1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 5],
    "product_id": [101, 102, 103, 101, 104, 102, 103, 105, 101, 105, 104],
    "action": [
        "view", "purchase", "click",
        "purchase", "view",
        "click", "purchase", "view",
        "click", "purchase", "view"
    ]
}

df = pd.DataFrame(data)

# -------------------------------------------------
# Step 2: Action to Score Mapping
# -------------------------------------------------

action_weight = {
    "view": 1,
    "click": 2,
    "purchase": 5
}

df["score"] = df["action"].map(action_weight)

# -------------------------------------------------
# Step 3: User–Item Interaction Matrix
# -------------------------------------------------

user_item_matrix = df.pivot_table(
    index="user_id",
    columns="product_id",
    values="score",
    aggfunc="sum",
    fill_value=0
)

# -------------------------------------------------
# Step 4: Collaborative Filtering (Item-Based)
# -------------------------------------------------

item_similarity = cosine_similarity(user_item_matrix.T)

item_similarity_df = pd.DataFrame(
    item_similarity,
    index=user_item_matrix.columns,
    columns=user_item_matrix.columns
)

# -------------------------------------------------
# Step 5: Collaborative Recommendation Function
# -------------------------------------------------

def recommend_products(user_id, top_n=3):
    if user_id not in user_item_matrix.index:
        return "New user – use content-based or trending products"

    user_scores = user_item_matrix.loc[user_id]
    interacted_products = user_scores[user_scores > 0].index

    scores = pd.Series(dtype=float)

    for product in interacted_products:
        scores = scores.add(item_similarity_df[product], fill_value=0)

    scores = scores.drop(interacted_products, errors="ignore")
    return scores.sort_values(ascending=False).head(top_n)

# -------------------------------------------------
# Step 6: Content-Based Filtering
# -------------------------------------------------

products = pd.DataFrame({
    "product_id": [101, 102, 103, 104, 105],
    "description": [
        "running sports shoes",
        "casual leather shoes",
        "sports fitness shoes",
        "wireless bluetooth headphones",
        "noise cancelling over ear headphones"
    ]
})

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(products["description"])

product_similarity = cosine_similarity(tfidf_matrix)

# -------------------------------------------------
# Step 7: Content-Based Recommendation Function
# -------------------------------------------------

def recommend_similar_products(product_id, top_n=2):
    if product_id not in products["product_id"].values:
        return []

    idx = products[products["product_id"] == product_id].index[0]
    similarity_scores = list(enumerate(product_similarity[idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    similar_products = similarity_scores[1:top_n + 1]
    return [products.iloc[i[0]]["product_id"] for i in similar_products]

# -------------------------------------------------
# Step 8: Hybrid Recommendation
# -------------------------------------------------

def hybrid_recommendation(user_id):
    if user_id not in user_item_matrix.index:
        return "New user – show trending products"

    collab_recs = recommend_products(user_id)

    if isinstance(collab_recs, str):
        return collab_recs

    return list(collab_recs.index)
# -------------------------------------------------
# Step 9: Show Output When Run Directly
# -------------------------------------------------

if __name__ == "__main__":

    print("\n--- USER ACTIVITY DATA ---")
    print(df)

    print("\n--- USER-ITEM MATRIX ---")
    print(user_item_matrix)

    print("\n--- COLLABORATIVE RECOMMENDATIONS ---")
    for user in user_item_matrix.index:
        print(f"User {user} recommendations:")
        print(recommend_products(user))
        print("-" * 40)

    print("\n--- CONTENT-BASED RECOMMENDATIONS ---")
    for pid in products["product_id"]:
        print(f"Products similar to {pid}: {recommend_similar_products(pid)}")

    print("\n--- HYBRID RECOMMENDATION EXAMPLE ---")
    print("User 3:", hybrid_recommendation(3))
    print("New User:", hybrid_recommendation(999))

