import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# -------------------------------
# SESSION INITIALIZATION
# -------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "data" not in st.session_state:
    st.session_state.data = None

if "model" not in st.session_state:
    st.session_state.model = None

# -------------------------------
# LOGIN PAGE
# -------------------------------
def login_page():
    st.title("Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "123":
            st.session_state.logged_in = True
            st.success("Login Successful")
            st.experimental_rerun()
        else:
            st.error("Invalid Credentials")

# -------------------------------
# DASHBOARD
# -------------------------------
def dashboard():
    st.title("Stock Prediction App")

    # LOGOUT BUTTON
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.data = None
        st.session_state.model = None
        st.experimental_rerun()

    # UPLOAD FILE
    uploaded_file = st.file_uploader("Upload Stock Dataset (CSV)", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.session_state.data = df
        st.success("Dataset Uploaded & Saved in Session")

    # SHOW DATA
    if st.session_state.data is not None:
        st.subheader("Dataset Preview")
        st.write(st.session_state.data.head())

        df = st.session_state.data.copy()
        df["Day"] = np.arange(len(df))

        X = df[["Day"]]
        y = df.iloc[:, 1]   # assumes price is in 2nd column

        model = LinearRegression()
        model.fit(X, y)
        st.session_state.model = model

        st.success("Model Trained Successfully")

        # PREDICTION
        future_days = np.arange(len(df), len(df) + 5).reshape(-1, 1)
        prediction = model.predict(future_days)

        st.subheader("Next 5 Days Prediction")
        st.write(prediction)

# -------------------------------
# MAIN
# -------------------------------
if not st.session_state.logged_in:
    login_page()
else:
    dashboard()