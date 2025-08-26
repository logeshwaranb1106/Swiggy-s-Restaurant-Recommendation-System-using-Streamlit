import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os, zipfile

# --- Configure page ---
st.set_page_config(page_title="Swiggy Recommender", layout="centered", initial_sidebar_state="expanded")

# --- Ensure encoded_data.csv is available ---
ZIP_PATH = "encoded_data.zip"
CSV_PATH = "encoded_data.csv"

if not os.path.exists(CSV_PATH) and os.path.exists(ZIP_PATH):
    with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
        zip_ref.extractall(".")
    print(f"✅ Extracted {ZIP_PATH} to current directory")

# --- Load data with caching for performance ---
@st.cache_data
def load_cleaned_data():
    return pd.read_csv("cleaned_data.csv")

@st.cache_data
def load_encoded_data():
    return pd.read_csv("encoded_data.csv")

@st.cache_data
def load_encoder():
    with open("encoder_scaler.pkl", "rb") as f:
        return pickle.load(f)

# Load data
cleaned_df = load_cleaned_data()
encoded_df = load_encoded_data()
encoder = load_encoder()

# --- App Header ---
st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🍽️ Swiggy Restaurant Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True) 

# --- Input Form ---
st.sidebar.subheader("🔍 Filter Your Preferences")

main_city = st.sidebar.selectbox("🌆 Main City", sorted(cleaned_df['main_city'].dropna().unique()))
filtered_cities = cleaned_df[cleaned_df["main_city"] == main_city]["city"].dropna().unique()
city = st.sidebar.selectbox("📍 City", sorted(filtered_cities))

city_df = cleaned_df[cleaned_df['city'] == city]
cuisine_options = sorted(city_df['cuisine'].dropna().unique())
cuisine = st.sidebar.selectbox("🍜 Cuisine", cuisine_options)

rating = st.sidebar.slider("⭐ Minimum Rating", 0.0, 5.0, 4.0, step=0.5)
cost = st.sidebar.number_input("💰 Max Cost (₹)", min_value=50, max_value=2000, value=300, step=100)

# --- Recommendation Engine ---
if st.sidebar.button("✨ Get Recommendations"):
    filtered_cleaned_df = cleaned_df[
        (cleaned_df['city'] == city) &
        (cleaned_df['cuisine'] == cuisine) &
        (cleaned_df['rating'] >= rating) &   # 🔹 changed from <= to >= for logic
        (cleaned_df['cost'] <= cost)
    ].reset_index(drop=True)

    if filtered_cleaned_df.empty:
        st.warning("No restaurants match your exact preferences. Try adjusting your filters.")
    else:
        matching_indices = filtered_cleaned_df.index
        filtered_encoded_df = encoded_df.loc[matching_indices].reset_index(drop=True)

        user_input = {
            f"city_{city}": 1,
            f"cuisine_{cuisine}": 1, 
            "rating": rating, 
            "cost": cost
        }

        input_vector = pd.DataFrame([user_input])
        for col in encoded_df.columns:
            if col not in input_vector.columns:
                input_vector[col] = 0
        input_vector = input_vector[encoded_df.columns]

        similarity = cosine_similarity(input_vector, filtered_encoded_df)[0] 
        top_indices = similarity.argsort()[-5:][::-1]
        recommendations = filtered_cleaned_df.iloc[top_indices][['name', 'city', 'cuisine', 'rating', 'cost']]

        st.markdown("## 🏆 Top 5 Recommended Restaurants")
        for _, row in recommendations.iterrows():
            with st.container():
                st.markdown(f"""
                    <div style='
                        background-color: #fff8f0;
                        border: 2px solid #f0c674;
                        padding: 16px;
                        border-radius: 12px;
                        margin-bottom: 10px;
                    '>
                        <h4 style='color: #d45500; margin-bottom: 8px;'>🍽️ {row['name']}</h4>
                        <p style='margin: 4px 0;'><strong>🌆 Main City:</strong> {main_city}</p>
                        <p style='margin: 4px 0;'><strong>📍 City:</strong> {row['city']}</p>
                        <p style='margin: 4px 0;'><strong>🍜 Cuisine:</strong> {row['cuisine']}</p>
                        <p style='margin: 4px 0;'><strong>⭐ Rating:</strong> {row['rating']:.1f}</p>
                        <p style='margin: 4px 0;'><strong>💰 Cost:</strong> ₹{row['cost']:.0f}</p>
                    </div>
                """, unsafe_allow_html=True)

else:
    st.info("Select your preferences and click '✨ Get Recommendations' to see suggestions!")
