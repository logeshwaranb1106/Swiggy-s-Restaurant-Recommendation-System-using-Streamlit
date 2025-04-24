import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans

# Load datasets
cleaned_df = pd.read_csv(r"D:\GuviProject4\cleaned_data.csv")
encoded_df = pd.read_csv(r"D:\GuviProject4\encoded_data.csv")

# Fit KMeans model
kmeans = KMeans(n_clusters=10, random_state=42)
kmeans.fit(encoded_df)

# Assign clusters
encoded_df['cluster'] = kmeans.labels_
cleaned_df['cluster'] = kmeans.labels_

# Streamlit UI
st.write("Restaurant Recommendation using K-Means Clustering")

# Input filters from relevant columns
main_city_option = st.sidebar.selectbox("Select Main City:", cleaned_df['main_city'].dropna().unique())
city_option = st.sidebar.selectbox("Select City:", cleaned_df['city'].dropna().unique())
cuisine_option = st.sidebar.selectbox("Select Cuisine:", cleaned_df['cuisine'].dropna().unique())
rating_option = st.sidebar.select_slider("Select Rating:", sorted(cleaned_df['rating'].dropna().unique(), reverse=True))
rating_count_option = st.sidebar.select_slider("Select Rating Count:", sorted(cleaned_df['rating_count'].dropna().unique(), reverse=True))
price_option = st.sidebar.select_slider("Select Price:", sorted(cleaned_df['cost'].dropna().unique()))

# Filter dataset based on selections
filtered_df = cleaned_df[
    (cleaned_df['main_city'] == main_city_option) &
    (cleaned_df['city'] == city_option) &
    (cleaned_df['cuisine'] == cuisine_option) &
    (cleaned_df['rating'] == rating_option) &
    (cleaned_df['rating_count'] == rating_count_option) &
    (cleaned_df['cost'] == price_option)
]

if not filtered_df.empty:
    user_cluster = filtered_df.iloc[0]['cluster']
    recommended_restaurants = cleaned_df[cleaned_df['cluster'] == user_cluster][['name', 'cuisine', 'rating', 'rating_count', 'cost']]
    st.write("Recommended Restaurants:")
    st.write(recommended_restaurants)
else:
    st.write("No matching restaurants found.")
