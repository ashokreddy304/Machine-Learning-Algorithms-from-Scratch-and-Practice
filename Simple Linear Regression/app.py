import streamlit as st
import pickle
import numpy as np

import pandas as pd

# Load the saved model (pipeline or regressor)
model = pickle.load(open(r'lr_model.pkl', 'rb'))

st.title("🏡 House Price Prediction")

st.write("Enter the house details below to predict the price (in Lakhs).")

# -------------------------
# Inputs
# -------------------------
bedrooms = st.number_input("Number of Bedrooms:", min_value=1, max_value=6, value=2)
bathrooms = st.number_input("Number of Bathrooms:", min_value=1, max_value=4, value=1)
stories = st.number_input("Number of Stories:", min_value=1, max_value=4, value=1)

mainroad = st.selectbox("Main Road:", ["Yes", "No"])
guestroom = st.selectbox("Guestroom:", ["Yes", "No"])
basement = st.selectbox("Basement (Parking place):", ["Yes", "No"])
hotwaterheating = st.selectbox("Hot Water Heating:", ["Yes", "No"])
airconditioning = st.selectbox("Air Conditioning:", ["Yes", "No"])

parking = st.number_input("Parking Spaces (0–3):", min_value=0, max_value=3, value=1)

prefarea = st.selectbox("Preferred Area:", ["Yes", "No"])

furnishingstatus = st.selectbox("Furnishing Status:", ["Furnished", "Semi-furnished", "Unfurnished"])

# Area input → converted to log
area = st.number_input("Enter Area (sqft):", min_value=400, max_value=10000, value=1200, step=50)
log_area = np.log1p(area)   # log transform

# -------------------------
# Convert categorical inputs to numeric (same as training)
# -------------------------
def encode_yes_no(val):
    return 1 if val == "Yes" else 0

mainroad = encode_yes_no(mainroad)
guestroom = encode_yes_no(guestroom)
basement = encode_yes_no(basement)
hotwaterheating = encode_yes_no(hotwaterheating)
airconditioning = encode_yes_no(airconditioning)
prefarea = encode_yes_no(prefarea)

# Furnishing one-hot encoding
furnishingstatus_semi_furnished = 1 if furnishingstatus == "Semi-furnished" else 0
furnishingstatus_unfurnished = 1 if furnishingstatus == "Unfurnished" else 0
# Furnished is baseline (both = 0)

# -------------------------
# Prediction
# -------------------------
if st.button("Predict House Price"):
    input_data = pd.DataFrame([[
        bedrooms, bathrooms, stories, mainroad, guestroom, basement,
        hotwaterheating, airconditioning, parking, prefarea,
        furnishingstatus_semi_furnished, furnishingstatus_unfurnished, log_area
    ]], columns=[
        'bedrooms', 'bathrooms', 'stories', 'mainroad', 'guestroom', 'basement',
        'hotwaterheating', 'airconditioning', 'parking', 'prefarea',
        'furnishingstatus_semi-furnished', 'furnishingstatus_unfurnished', 'log_area'
    ])
    
    prediction = model.predict(input_data)
    st.success(f"🏠 Predicted House Price: ₹{prediction[0]:,.2f} Lakhs")
