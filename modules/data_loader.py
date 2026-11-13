import streamlit as st
import pandas as pd


def load_data(uploaded_file):
    """Loads a CSV or Excel file into a DataFrame."""
    try:
        name = uploaded_file.name.lower()
        if name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format. Upload CSV or Excel.")
            return None
        if df.empty:
            st.error("Uploaded file is empty.")
            return None
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None


def get_dataset_summary(df):
    """Returns a dict summary of the dataset."""
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "numeric_features": len(numeric_cols),
        "categorical_features": len(categorical_cols),
        "numeric_columns": numeric_cols,
        "categorical_columns": categorical_cols,
        "missing_values": int(df.isnull().sum().sum()),
        "missing_pct": round(float(df.isnull().mean().mean() * 100), 2),
        "dtypes": {col: str(dt) for col, dt in df.dtypes.items()},
    }
