import streamlit as st
import pandas as pd

# Load datasets
cleaned_df = pd.read_csv(r"D:\GuviProject4\new_cleaned_data.csv")
encoded_df = pd.read_csv(r"D:\GuviProject4\new_encoded_data.csv")

# Fit KMeans model
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=5, random_state=42)
kmeans.fit(encoded_df)

# Assign clusters
encoded_df['cluster'] = kmeans.labels_
cleaned_df['cluster'] = kmeans.labels_

# Streamlit UI
st.title(" Swiggy’s Restaurant Recommendation System")

# Create Main City list with 'Other / Not Listed' option
main_cities = cleaned_df['main_city'].dropna().unique().tolist()
main_cities.insert(0, "Other / Not Listed")  # Insert custom option at the top
main_city_option = st.sidebar.selectbox("Select Main City:", main_cities)

# Conditional logic for dependent City dropdown
if main_city_option == "Other / Not Listed":
    city_options = cleaned_df[cleaned_df['main_city'].isna()]['city'].dropna().unique()
else:
    city_options = cleaned_df[cleaned_df['main_city'] == main_city_option]['city'].dropna().unique()

city_option = st.sidebar.selectbox("Select City:", city_options)

# Other filters
cuisine_option = st.sidebar.selectbox("Select Cuisine:", cleaned_df['cuisine'].dropna().unique())
rating_option = st.sidebar.select_slider("Select Rating:", sorted(cleaned_df['rating'].dropna().unique()))
rating_count_option = st.sidebar.selectbox("Select Rating Count:", ['Less than 100',"100-500",'500-1000','1000-5000','5000-10000','10000 Above'])
price_option = st.sidebar.selectbox("Select Price (₹):",['Less than 100','100-200','200-300','300-500','500-1000','1000-1500','Above 1500'])

# Filter dataset based on selections
if main_city_option == "Other / Not Listed":
    base_filtered_df = cleaned_df[cleaned_df['main_city'].isna()]
else:
    base_filtered_df = cleaned_df[cleaned_df['main_city'] == main_city_option]

if rating_count_option == 'Less than 100':
    rating_count_filter = base_filtered_df['rating_count'] < 100
elif rating_count_option=="100-500":
    rating_count_filter=(base_filtered_df['rating_count']>=100)&(base_filtered_df['rating_count']<500)
elif rating_count_option=='500-1000':
    rating_count_filter=(base_filtered_df['rating_count']>=500)&(base_filtered_df['rating_count']<1000)
elif rating_count_option=='1000-5000':
    rating_count_filter=(base_filtered_df['rating_count']>=1000)&(base_filtered_df['rating_count']<5000)
elif rating_count_option=='5000-10000':
    rating_count_filter=(base_filtered_df['rating_count']>=5000)&(base_filtered_df['rating_count']<10000)
elif rating_count_option=='10000 Above':
    rating_count_filter = base_filtered_df['rating_count'] >=10000
else:
    # You may need to extract the numeric range from the string, for now assume exact match
    rating_count_filter = base_filtered_df['rating_count'] == int(rating_count_option.split('-')[0])

if price_option == 'Less than 100':
    price_filter = base_filtered_df['cost'] < 100
elif price_option =='100-200':
    price_filter = (base_filtered_df['cost']>=100)&(base_filtered_df['cost']<200)
elif price_option =='200-300':
    price_filter = (base_filtered_df['cost']>=200)&(base_filtered_df['cost']<300)
elif price_option =='300-500':
    price_filter = (base_filtered_df['cost']>=300)&(base_filtered_df['cost']<500)
elif price_option=='500-1000':
    price_filter = (base_filtered_df['cost']>=500)&(base_filtered_df['cost']<1000)
elif price_option =='1000-1500':
    price_filter = (base_filtered_df['cost']>=1000)&(base_filtered_df['cost']<1500)
elif price_option=='Above 1500':
    price_filter = base_filtered_df['cost']>=1500
else:
    price_filter = base_filtered_df['cost'] == int(price_option.split('-')[0])


filtered_df = base_filtered_df[
    (base_filtered_df['city'] == city_option) &
    (base_filtered_df['cuisine'] == cuisine_option) &
    (base_filtered_df['rating'] == rating_option) &
    rating_count_filter &
    price_filter
]

# Show Recommendations
if not filtered_df.empty:
    user_cluster = filtered_df.iloc[0]['cluster']
    recommended_restaurants = cleaned_df[cleaned_df['cluster'] == user_cluster][['name', 'cuisine', 'rating', 'rating_count', 'cost']]
    recommended_restaurants = recommended_restaurants.sort_values(by='rating', ascending=False).head(10)
    st.subheader("Recommended Restaurants:")
    st.write(recommended_restaurants)
else:
    st.warning("No matching restaurants found. Try adjusting your filters.")
