"""
EDA Visualizations - Reusable chart functions derived from EDA notebooks.
All visualizations follow professional data analyst best practices with clear, simple charts.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utils.charts import (
    BLUE,
    GREEN,
    AMBER,
    RED,
    PANEL,
    TEXT,
    SECONDARY,
    COLOR_SEQUENCE,
    apply_theme,
)


# ────────────────────────────────────────────────────────────
# NUTRITION DATASET VISUALIZATIONS (from EDA_data_klasifikasi.ipynb)
# ────────────────────────────────────────────────────────────


def nutrition_sugar_distribution(df: pd.DataFrame) -> go.Figure:
    """
    Histogram with KDE showing sugar distribution (g) across all products.
    Shows concentration of products by sugar content.
    """
    fig = px.histogram(
        df,
        x="sugar_g",
        nbins=30,
        title="Distribusi Kandungan Gula (g)",
        labels={"sugar_g": "Sugar (g)", "count": "Jumlah Produk"},
        marginal="box",
    )
    fig.update_traces(marker_color=BLUE)
    return apply_theme(fig, height=400)


def nutrition_sodium_distribution(df: pd.DataFrame) -> go.Figure:
    """
    Histogram with KDE showing sodium distribution (mg) across all products.
    Shows concentration of products by sodium content.
    """
    fig = px.histogram(
        df,
        x="sodium_mg",
        nbins=30,
        title="Distribusi Kandungan Sodium (mg)",
        labels={"sodium_mg": "Sodium (mg)", "count": "Jumlah Produk"},
        marginal="box",
    )
    fig.update_traces(marker_color=AMBER)
    return apply_theme(fig, height=400)


def nutrition_correlation_heatmap(df: pd.DataFrame) -> go.Figure:
    """
    Correlation heatmap of nutritional features to identify relationships.
    Shows which nutrients are strongly correlated.
    """
    numeric_cols = ["sugar_g", "carbs_g", "calories", "sodium_mg", "fat_g", "protein_g"]
    numeric_cols = [col for col in numeric_cols if col in df.columns]
    
    if len(numeric_cols) < 2:
        return go.Figure().add_annotation(text="Insufficient numeric columns")
    
    corr_matrix = df[numeric_cols].corr()
    
    fig = go.Figure(
        data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale="RdBu",
            zmid=0,
            zmin=-1,
            zmax=1,
            text=corr_matrix.values.round(2),
            texttemplate="%{text}",
            textfont={"size": 12},
            colorbar={"title": "Correlation"},
        )
    )
    fig.update_layout(
        title="Matriks Korelasi Nutrisi",
        xaxis_title="",
        yaxis_title="",
        height=500,
        width=600,
        template="plotly_dark",
        paper_bgcolor=PANEL,
        plot_bgcolor=PANEL,
        font={"color": TEXT},
    )
    return fig


def nutrition_recommendation_by_diabetes(df: pd.DataFrame) -> go.Figure:
    """
    Grouped bar chart showing recommendation distribution across diabetes types.
    Highlights how recommendation rates differ by diabetes profile.
    """
    # Map diabetes_type numeric to readable labels
    diabetes_map = {0: "Normal", 1: "Diabetes Type 1", 2: "Diabetes Type 2"}
    df_copy = df.copy()
    df_copy["diabetes_label"] = df_copy["diabetes_type"].map(diabetes_map)
    
    summary = (
        df_copy.groupby(["diabetes_label", "label"])
        .size()
        .reset_index(name="count")
    )
    
    fig = px.bar(
        summary,
        x="diabetes_label",
        y="count",
        color="label",
        title="Distribusi Rekomendasi Berdasarkan Profil Diabetes",
        labels={"diabetes_label": "Profil Diabetes", "count": "Jumlah Produk", "label": "Rekomendasi"},
        color_discrete_map={"Recommended": GREEN, "Caution": AMBER, "Not Recommended": RED},
        barmode="group",
    )
    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="Jumlah Produk")
    return apply_theme(fig, height=400)


def nutrition_sugar_by_recommendation(df: pd.DataFrame) -> go.Figure:
    """
    Box plot showing sugar distribution by recommendation status.
    Highlights how sugar content differs between recommended/caution/not recommended products.
    """
    fig = px.box(
        df,
        x="label",
        y="sugar_g",
        title="Distribusi Gula Berdasarkan Status Rekomendasi",
        labels={"label": "Status", "sugar_g": "Sugar (g)"},
        color="label",
        color_discrete_map={"Recommended": GREEN, "Caution": AMBER, "Not Recommended": RED},
    )
    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="Gula (g)")
    return apply_theme(fig, height=400)


# ────────────────────────────────────────────────────────────
# OCR QUALITY DATASET VISUALIZATIONS (from EDA_labeldata_ocr.ipynb)
# ────────────────────────────────────────────────────────────


def ocr_quality_distribution(df: pd.DataFrame) -> go.Figure:
    """
    Bar chart showing distribution of image quality levels across OCR dataset.
    Simple overview of data quality before and after labeling.
    """
    quality_counts = df["quality"].value_counts().reset_index()
    quality_counts.columns = ["quality", "count"]
    
    # Order by quality level
    quality_order = {"clear": 0, "blur": 1, "glare": 2, "overlap": 3}
    quality_counts["order"] = quality_counts["quality"].map(quality_order)
    quality_counts = quality_counts.sort_values("order")
    
    color_map = {"clear": GREEN, "blur": RED, "glare": AMBER, "overlap": AMBER}
    
    fig = px.bar(
        quality_counts,
        x="quality",
        y="count",
        title="Distribusi Kualitas Foto OCR",
        labels={"quality": "Kualitas Foto", "count": "Jumlah Gambar"},
        color="quality",
        color_discrete_map=color_map,
    )
    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="Jumlah Gambar")
    fig.update_layout(showlegend=False)
    return apply_theme(fig, height=400)


def ocr_text_length_distribution(df: pd.DataFrame) -> go.Figure:
    """
    Histogram showing distribution of extracted text lengths in OCR dataset.
    Helps understand text extraction success and variability.
    """
    df_copy = df.copy()
    df_copy["text_length"] = df_copy["text"].fillna("").str.len()
    
    fig = px.histogram(
        df_copy,
        x="text_length",
        nbins=20,
        title="Distribusi Panjang Teks Hasil Ekstraksi",
        labels={"text_length": "Jumlah Karakter", "count": "Jumlah Gambar"},
        marginal="box",
    )
    fig.update_traces(marker_color=BLUE)
    return apply_theme(fig, height=400)


def ocr_quality_by_nutrient(df: pd.DataFrame) -> go.Figure:
    """
    Grouped bar chart showing quality distribution across different nutrient categories.
    Shows which nutrient categories have better/worse photo quality.
    """
    df_copy = df.copy()
    # Extract nutrient type from file_name (e.g., "calories_001.png" -> "calories")
    df_copy["nutrient_type"] = df_copy["file_name"].str.extract(r"^([a-zA-Z_]+)_\d")[0]
    
    quality_by_nutrient = (
        df_copy.groupby(["nutrient_type", "quality"])
        .size()
        .reset_index(name="count")
    )
    
    color_map = {"clear": GREEN, "blur": RED, "glare": AMBER, "overlap": AMBER}
    
    fig = px.bar(
        quality_by_nutrient,
        x="nutrient_type",
        y="count",
        color="quality",
        title="Distribusi Kualitas Foto Berdasarkan Kategori Nutrisi",
        labels={"nutrient_type": "Kategori Nutrisi", "count": "Jumlah Gambar", "quality": "Kualitas"},
        color_discrete_map=color_map,
        barmode="stack",
    )
    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="Jumlah Gambar")
    return apply_theme(fig, height=450)


def ocr_vocabulary_analysis(df: pd.DataFrame, top_n: int = 20) -> go.Figure:
    """
    Bar chart of top N most frequent characters in OCR extracted text.
    Shows character frequency for understanding OCR success patterns.
    """
    text_combined = " ".join(df["text"].fillna("").astype(str))
    # Count character frequency (excluding spaces)
    char_freq = pd.Series(list(text_combined)).value_counts().head(top_n)
    char_freq = char_freq[char_freq.index != " "].head(top_n)
    
    char_df = char_freq.reset_index()
    char_df.columns = ["character", "frequency"]
    
    fig = px.bar(
        char_df,
        x="character",
        y="frequency",
        title=f"Top {top_n} Karakter Paling Sering Muncul dalam Hasil Ekstraksi",
        labels={"character": "Karakter", "frequency": "Frekuensi"},
    )
    fig.update_traces(marker_color=BLUE)
    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="Frekuensi")
    return apply_theme(fig, height=400)


# ────────────────────────────────────────────────────────────
# SUMMARY STATISTICS
# ────────────────────────────────────────────────────────────


def ocr_quality_summary_stats(df: pd.DataFrame) -> dict:
    """
    Return key statistics about OCR dataset for display in metric cards.
    """
    df_copy = df.copy()
    df_copy["text_length"] = df_copy["text"].fillna("").str.len()
    
    return {
        "total_images": len(df),
        "total_unique_characters": len(set("".join(df["text"].fillna("").astype(str)))),
        "avg_text_length": int(df_copy["text_length"].mean()),
        "max_text_length": int(df_copy["text_length"].max()),
        "quality_good_pct": int((df["quality"] == "clear").sum() / len(df) * 100),
        "quality_poor_pct": int((df["quality"].isin(["blur", "glare"])).sum() / len(df) * 100),
    }


def nutrition_summary_stats(df: pd.DataFrame) -> dict:
    """
    Return key statistics about nutrition dataset for display in metric cards.
    """
    return {
        "total_records": len(df),
        "total_unique_products": int(df["product_name"].nunique()),
        "recommended_pct": int(
            (df["label"] == "Recommended").sum() / len(df) * 100
        ),
        "not_recommended_pct": int(
            (df["label"] == "Not Recommended").sum() / len(df) * 100
        ),
        "avg_sugar": round(df["sugar_g"].mean(), 1),
        "avg_sodium": round(df["sodium_mg"].mean(), 1),
    }
