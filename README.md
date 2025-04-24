# 🍽️ Swiggy’s Restaurant Recommendation System using Streamlit

## 🚀 Overview
Swiggy’s Restaurant Recommendation System is an interactive and intelligent application built with Streamlit that helps users discover restaurants tailored to their preferences. It leverages machine learning techniques like **One-Hot Encoding**, **Clustering**, and **Cosine Similarity** to recommend top restaurants based on inputs such as **City**, **Cuisine**, **Rating**, and **Price**.

---

## 📊 Project Summary

### 🔧 Skills Applied:
- Data Cleaning & Preprocessing
- One-Hot Encoding
- Clustering (K-Means) & Similarity Measures (Cosine Similarity)
- Streamlit Application Development
- Python for Data Analytics

### 📁 Domain:
**Recommendation Systems & Data Analytics**

---

## 🎯 Problem Statement
Build a recommendation system that:
- Takes user inputs (city, cuisine, rating, price).
- Encodes and clusters restaurant data.
- Recommends restaurants using similarity metrics.
- Displays results through an interactive Streamlit interface.

---

## 📌 Dataset Information
The dataset contains the following columns:
['id', 'name', 'city', 'rating', 'rating_count', 'cost', 'cuisine', 'lic_no', 'link', 'address', 'menu']


---

## 🧠 Approach

### 1. 📦 Data Cleaning
- Removed duplicates and handled missing values.
- Saved as: `cleaned_data.csv`

### 2. 🔄 Data Preprocessing
- One-Hot Encoded categorical features.
- Ensured index alignment for mapping.
- Saved encoded data as: `encoded_data.csv`
- Saved encoder model as: `encoder.pkl`

### 3. 🧮 Recommendation Engine
- Used K-Means Clustering or Cosine Similarity to identify similar restaurants.
- Mapped results back to `cleaned_data.csv` for display.

### 4. 💻 Streamlit App
- **User Input:** City, Cuisine, Rating, Cost.
- **Backend:** Encoded input, generated recommendations.
- **Output:** Displayed top restaurant recommendations.

---

## 📈 Results

### ✔️ Cleaned Dataset
- Structured and ready for analysis.

### ✔️ Encoded Dataset
- Transformed categorical to numerical format.

### ✔️ Streamlit App
- Intuitive UI with real-time recommendations.

---

## 💼 Business Use Cases

- **Personalized Recommendations**: Tailor results to user preferences.
- **Enhanced Customer Experience**: Simplify dining choices.
- **Market Insights**: Understand trends in dining behavior.
- **Operational Efficiency**: Help businesses adapt to consumer preferences.

---

## 📊 Evaluation Metrics

- **Recommendation Quality**: Relevance and diversity.
- **Usability**: Streamlit app user experience.
- **Data Alignment**: Index sync between cleaned and encoded datasets.

---

## 📂 Project Deliverables

- `cleaned_data.csv` – Cleaned restaurant dataset.
- `encoded_data.csv` – One-Hot Encoded dataset.
- `encoder.pkl` – Serialized encoder model.
- `app.py` – Streamlit web application.
- `README.md` – Project documentation.
- Final Report – Methodology, analysis, and key insights.

---
