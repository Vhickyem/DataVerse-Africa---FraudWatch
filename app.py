import streamlit as st
import pandas as pd
import requests
from datetime import datetime, date

st.set_page_config(page_title="Fraud Detection Dashboard", layout="wide")

st.title("💳 Active Fraud Detection Dashboard")

# API endpoint
API_URL = "http://127.0.0.1:8000/predict"  # Change if deployed

# Sidebar for transaction input
st.sidebar.header("Enter Transaction Details")
transaction_data = {
    "transaction_id": st.sidebar.text_input("Transaction ID", "TX100002"),
    "user_id": st.sidebar.text_input("User ID", "user_6390"),
    "transaction_type": st.sidebar.selectbox(
        "Transaction Type",
        ['Withdraw Cash', 'Send Money', 'Deposit Cash', 'Lipa na M-Pesa', 'Buy Airtime', 'Pay Bill']
    ),
    "amount": st.sidebar.number_input("Amount", min_value=0.0, step=0.01),
    "location": st.sidebar.selectbox(
        "Location",
        ['Nakuru', 'Garissa', 'Nyeri', 'Nairobi', 'Machakos', 'Meru', 'Kisumu', 'Mombasa', 'Eldoret', 'Thika']
    ),
    "device_type": st.sidebar.selectbox(
        "Device Type",
        ["Feature Phone", "Ios", "Android"]
    ),
    "network_provider": st.sidebar.selectbox(
        "Network Provider",
        ['Telkom Kenya', 'Safaricom', 'Airtel']
    ),
    "user_type": st.sidebar.selectbox(
        "User Type",
        ["Individual", "Agent"]
    ),
    "time_of_day": st.sidebar.selectbox(
        "Time of Day",
        ["Morning", "Afternoon", "Evening", "Night"]
    ),
    "is_foreign_number": st.sidebar.selectbox("Foreign Number?", [0, 1]),
    "is_sim_recently_swapped": st.sidebar.selectbox("SIM Recently Swapped?", [0, 1]),
    "has_multiple_accounts": st.sidebar.selectbox("Has Multiple Accounts?", [0, 1]),
    "datetime": datetime.now().isoformat(),
    "date": date.today().isoformat(),
    "hour": datetime.now().hour
}

# Predict button
if st.sidebar.button("Predict Fraud"):
    try:
        response = requests.post(API_URL, json=transaction_data)
        if response.status_code == 200:
            result = response.json()
            prediction = result["prediction"]
            
            if prediction == "Fraudulent":
                st.error("⚠️ Transaction likely FRAUDULENT!")
            else:
                st.success("✅ Transaction appears legitimate.")
        else:
            st.error(f"API Error {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"Connection error: {e}")

# Optional: Upload batch transactions for scoring
st.subheader("Batch Prediction")
uploaded_file = st.file_uploader("Upload CSV with transaction data", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    try:
        batch_response = requests.post(API_URL + "/batch", json=df.to_dict(orient="records"))
        if batch_response.status_code == 200:
            batch_preds = batch_response.json()
            df["Prediction"] = batch_preds
            st.dataframe(df)
        else:
            st.error(f"API Error: {batch_response.text}")
    except Exception as e:
        st.error(f"Connection error: {e}")
