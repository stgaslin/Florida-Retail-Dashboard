import os
port = int(os.environ.get("PORT", 8501))
import streamlit as st
st.title("Hello, Florida Retail Dashboard")
st.write("More features coming soon!")
import pandas as pd
import numpy as np
import os

# --- Authentication Settings ---
USERNAME = "sgaslin@lee-associates.com"
PASSWORD = "BearSavannaReynolds"

# --- Page Config ---
st.set_page_config(page_title="Florida Retail Dashboard", layout="wide")
# --- Authentication System ---
def login():
    st.sidebar.header("Login")
    username_input = st.sidebar.text_input("Username")
    password_input = st.sidebar.text_input("Password", type="password")
    login_button = st.sidebar.button("Login")

    if login_button:
        if username_input == USERNAME and password_input == PASSWORD:
            st.session_state["logged_in"] = True
        else:
            st.sidebar.error("Invalid username or password.")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()

# --- Data Upload / Load ---
@st.cache_data
def load_data():
    file_path = os.path.join('data', 'sales_data.csv')
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return df
    else:
        return pd.DataFrame()

data = load_data()

st.title("🏢 Florida Retail Sales Dashboard")

if data.empty:
    st.warning("No sales data found. Please upload your Florida shopping center sales file into `/data/` folder.")
# --- Filtering Section ---
if not data.empty:
    st.sidebar.header("Filter Sales Data")

    city_filter = st.sidebar.multiselect("City", options=sorted(data['City'].dropna().unique()))
    zip_filter = st.sidebar.multiselect("ZIP Code", options=sorted(data['Zip Code'].dropna().unique()))
    min_price = st.sidebar.number_input("Minimum Sale Price ($)", value=0)
    max_price = st.sidebar.number_input("Maximum Sale Price ($)", value=500000000)
    min_sqft = st.sidebar.number_input("Minimum Building Size (Sq Ft)", value=0)
    max_sqft = st.sidebar.number_input("Maximum Building Size (Sq Ft)", value=5000000)
    min_cap_rate = st.sidebar.number_input("Minimum Cap Rate (%)", value=0.0)
    max_cap_rate = st.sidebar.number_input("Maximum Cap Rate (%)", value=20.0)

    filtered_data = data.copy()

    if city_filter:
        filtered_data = filtered_data[filtered_data['City'].isin(city_filter)]

    if zip_filter:
        filtered_data = filtered_data[filtered_data['Zip Code'].isin(zip_filter)]

    filtered_data = filtered_data[
        (filtered_data['Sale Price'] >= min_price) &
        (filtered_data['Sale Price'] <= max_price) &
        (filtered_data['Building Size (Sq Ft)'] >= min_sqft) &
        (filtered_data['Building Size (Sq Ft)'] <= max_sqft) &
        (filtered_data['Cap Rate'] >= min_cap_rate) &
        (filtered_data['Cap Rate'] <= max_cap_rate)
    ]

    st.write(f"### Filtered Results ({len(filtered_data)} properties)")
    st.dataframe(filtered_data)

    # --- Export Section ---
    st.download_button(
        label="Download Filtered Results as Excel",
        data=filtered_data.to_csv(index=False).encode('utf-8'),
        file_name="filtered_sales_data.csv",
        mime="text/csv"
    )
# --- Footer ---
st.markdown("---")
st.markdown("Built by [Your Company Name] - Florida Retail Sales Intelligence Dashboard")
