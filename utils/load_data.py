from pathlib import Path

import pandas as pd
import streamlit as st


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


@st.cache_data(show_spinner=False)
def _load_csv(filename: str) -> pd.DataFrame:
    """Read a CSV file from the data folder and show a clear error when missing."""
    file_path = DATA_DIR / filename

    if not file_path.exists():
        st.error(f"File dataset tidak ditemukan: {file_path}")
        return pd.DataFrame()

    try:
        return pd.read_csv(file_path)
    except Exception as error:
        st.error(f"Gagal membaca dataset {file_path}: {error}")
        return pd.DataFrame()


def load_nutrition_data() -> pd.DataFrame:
    """Load the nutrition dataset used by every dashboard page."""
    return _load_csv("nutrition_dataset.csv")


def load_yolo_quality_data() -> pd.DataFrame:
    """Load the YOLO dataset quality CSV for OCR photo quality analysis."""
    return _load_csv("yolo_dataset_quality.csv")
