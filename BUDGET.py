import streamlit as st
import pandas as pd

st.set_page_config(page_title="Budget Manager 2025", layout="wide")

st.title("💰 Personal Budget Manager – 2025")

# Initialize session state for transactions
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Date", "Category", "Description", "Amount"])

# Sidebar: Add new transaction
st.sidebar.header("➕ Add Transaction")
with st.sidebar.form("transaction_form"):
    date = st.date_input("Date")
    category = st.selectbox("Category", ["Income", "Rent", "Groceries", "Utilities", "Transport", "Entertainment", "Other"])
    description = st.text_input("Description")
    amount = st.number_input("Amount", step=0.01, format="%.2f")
    submit = st.form_submit_button("Add")

if submit:
    new_entry = pd.DataFrame([[date, category, description, amount]],
                             columns=["Date", "Category", "Description", "Amount"])
    st.session_state.data = pd.concat([st.session_state.data, new_entry], ignore_index=True)
    st.success("Transaction added!")

# Display data
st.subheader("📋 Transactions")
df = st.session_state.data
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date", ascending=False)
st.dataframe(df, use_container_width=True)

# Summary
st.subheader("📈 Summary")
total_income = df[df["Category"] == "Income"]["Amount"].sum()
total_expense = df[df["Category"] != "Income"]["Amount"].sum()
balance = total_income - total_expense

col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"${total_income:,.2f}")
col2.metric("Total Expenses", f"${total_expense:,.2f}")
col3.metric("Balance", f"${balance:,.2f}")

# Chart: Expenses by category
st.subheader("📊 Expenses by Category")
expense_data = df[df["Category"] != "Income"]
category_totals = expense_data.groupby("Category")["Amount"].sum()

if not category_totals.empty:
    st.bar_chart(category_totals)

# Export option
st.download_button(
    label="Download CSV",
    data=df.to_csv(index=False).encode(),
    file_name="budget_2025.csv",
    mime="text/csv"
)
