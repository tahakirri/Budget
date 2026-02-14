import streamlit as st
import pandas as pd
import os
from io import StringIO

# =====================
# CONFIG
# =====================
PASSWORD = "Admin@2025"
DATA_FILE = "shared_table.csv"

st.set_page_config(
    page_title="Shared Excel Table",
    layout="wide"
)

st.title("📊 Shared Excel Table (Paste from Excel)")

# =====================
# DISPLAY SHARED TABLE
# =====================
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    st.subheader("📌 Current Shared Table")
    st.dataframe(df, use_container_width=True)
else:
    st.info("No table has been shared yet.")

st.divider()

# =====================
# ADMIN SECTION
# =====================
st.subheader("🔐 Admin Section")

password = st.text_input("Password", type="password")

if password == PASSWORD:
    st.success("Access granted")

    pasted_table = st.text_area(
        "Paste table from Excel here (Ctrl + V)",
        height=220,
        placeholder="Paste the copied Excel cells here"
    )

    if st.button("Save / Update Table"):
        if pasted_table.strip():
            try:
                df_new = pd.read_csv(
                    StringIO(pasted_table),
                    sep="\t"
                )

                df_new.to_csv(DATA_FILE, index=False)

                st.success("Table saved successfully!")
                st.subheader("✅ Updated Table")
                st.dataframe(df_new, use_container_width=True)

            except Exception as e:
                st.error(f"Could not read table: {e}")
        else:
            st.warning("Please paste a table first.")

elif password:
    st.error("Incorrect password")

# =====================
# FOOTER
# =====================
st.caption("Simple shared table – password protected for quick use")
