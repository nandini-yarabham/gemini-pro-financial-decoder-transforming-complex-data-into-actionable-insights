import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Financial Decoder", layout="centered")

st.title("📊 Gemini Pro Financial Decoder")
st.write("Transform complex financial data into actionable insights")

# File upload
uploaded_file = st.file_uploader("Upload Financial CSV", type=["csv"])

def analyze_data(df):
    categories = df["Category"].str.lower().tolist()

    if "assets" in categories:
        return "Balance Sheet"
    elif "revenue" in categories:
        return "Profit & Loss"
    elif "operating cash flow" in categories:
        return "Cash Flow"
    else:
        return "Unknown"

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Uploaded Data")
    st.dataframe(df)

    statement_type = analyze_data(df)

    st.success(f"Detected Statement: {statement_type}")

    st.subheader("🧾 Summary & Insights")

    if statement_type == "Balance Sheet":
        assets = df.loc[df["Category"] == "Assets", "Amount"].values[0]
        liabilities = df.loc[df["Category"] == "Liabilities", "Amount"].values[0]
        equity = df.loc[df["Category"] == "Equity", "Amount"].values[0]

        st.write(f"**Assets:** ₹{assets:,}")
        st.write(f"**Liabilities:** ₹{liabilities:,}")
        st.write(f"**Equity:** ₹{equity:,}")

        if assets > liabilities:
            st.success("Company is financially stable.")
        else:
            st.error("Liabilities exceed assets.")

    elif statement_type == "Profit & Loss":
        revenue = df.loc[df["Category"] == "Revenue", "Amount"].values[0]
        expenses = df.loc[df["Category"] == "Expenses", "Amount"].values[0]
        profit = df.loc[df["Category"] == "Net Profit", "Amount"].values[0]

        st.write(f"**Revenue:** ₹{revenue:,}")
        st.write(f"**Expenses:** ₹{expenses:,}")
        st.write(f"**Net Profit:** ₹{profit:,}")

        if profit > 0:
            st.success("Business is profitable.")
        else:
            st.warning("Business is running at a loss.")

    elif statement_type == "Cash Flow":
        net_cash = df.loc[df["Category"] == "Net Cash Flow", "Amount"].values[0]

        st.write(f"**Net Cash Flow:** ₹{net_cash:,}")

        if net_cash > 0:
            st.success("Strong liquidity position.")
        else:
            st.warning("Cash flow risk detected.")

    else:
        st.error("Unable to detect statement type.")

    st.subheader("📈 Visualization")

    fig, ax = plt.subplots()
    ax.bar(df["Category"], df["Amount"])
    plt.xticks(rotation=45)
    st.pyplot(fig)

else:
    st.info("Upload a financial CSV file to begin.")
