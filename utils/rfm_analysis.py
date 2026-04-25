"""
RFM Analysis Utilities - Product frequency, recommendation distribution, and category analysis.
Provides segmentation and insights into product characteristics across the dataset.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.charts import apply_theme, BLUE, GREEN, AMBER, RED, PANEL, TEXT, SECONDARY


def product_frequency_analysis(df: pd.DataFrame) -> go.Figure:
    """
    Frequency Analysis: Top products by appearance count in dataset.
    Higher frequency = more user profiles or augmentation combinations.
    """
    product_freq = df["product_name"].value_counts().head(15).reset_index()
    product_freq.columns = ["product_name", "frequency"]
    
    fig = px.bar(
        product_freq,
        x="frequency",
        y="product_name",
        orientation="h",
        title="Top 15 Produk Berdasarkan Frekuensi di Dataset",
        labels={"frequency": "Jumlah Records", "product_name": "Nama Produk"},
    )
    fig.update_traces(marker_color=BLUE)
    fig.update_xaxes(title_text="Jumlah Records")
    fig.update_yaxes(title_text="")
    return apply_theme(fig, height=500)


def recommendation_rate_by_product(df: pd.DataFrame) -> go.Figure:
    """
    Monetary/Quality Proxy: Recommendation rate per product.
    High rate = quality product, Low rate = problematic product.
    """
    product_summary = (
        df.groupby("product_name")
        .agg({
            "label": lambda x: (x == "Recommended").sum() / len(x) * 100,
        })
        .reset_index()
    )
    product_summary.columns = ["product_name", "recommendation_rate"]
    product_summary = product_summary.sort_values("recommendation_rate", ascending=False).head(15)
    
    fig = px.bar(
        product_summary,
        x="recommendation_rate",
        y="product_name",
        orientation="h",
        title="Top 15 Produk Berdasarkan Recommendation Rate",
        labels={"recommendation_rate": "Rekomendasi (%)", "product_name": "Nama Produk"},
    )
    
    # Color by rate
    colors = [GREEN if x > 70 else AMBER if x > 40 else RED for x in product_summary["recommendation_rate"]]
    fig.update_traces(marker_color=colors)
    
    fig.update_xaxes(title_text="Rekomendasi Rate (%)")
    fig.update_yaxes(title_text="")
    return apply_theme(fig, height=500)


def rfm_segment_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate RFM-like segmentation:
    - R (Recency): Not applicable here, use category as proxy
    - F (Frequency): Count per product
    - M (Monetary): Use recommendation rate as quality proxy
    """
    product_analysis = (
        df.groupby("product_name")
        .agg({
            "label": ["count", lambda x: (x == "Recommended").sum() / len(x) * 100],
            "category": "first",
            "sugar_g": "mean",
            "sodium_mg": "mean",
        })
        .reset_index()
    )
    
    # Flatten columns
    product_analysis.columns = [
        "product_name",
        "frequency",
        "recommendation_rate",
        "category",
        "avg_sugar_g",
        "avg_sodium_mg",
    ]
    
    # Create segments
    def segment_product(row):
        if row["recommendation_rate"] > 70:
            return "High Quality"
        elif row["recommendation_rate"] > 40:
            return "Moderate Quality"
        else:
            return "Low Quality"
    
    product_analysis["segment"] = product_analysis.apply(segment_product, axis=1)
    
    return product_analysis.sort_values("frequency", ascending=False)


def category_distribution_rfm(df: pd.DataFrame) -> go.Figure:
    """
    Category distribution with recommendation rate overlay.
    Shows which categories have better/worse recommendation rates.
    """
    category_summary = (
        df.groupby("category")
        .agg({
            "label": ["count", lambda x: (x == "Recommended").sum() / len(x) * 100],
        })
        .reset_index()
    )
    
    category_summary.columns = ["category", "total_count", "recommendation_rate"]
    category_summary = category_summary.sort_values("total_count", ascending=False).head(12)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=category_summary["category"],
        y=category_summary["total_count"],
        name="Total Records",
        marker_color=BLUE,
        yaxis="y",
    ))
    
    fig.add_trace(go.Scatter(
        x=category_summary["category"],
        y=category_summary["recommendation_rate"],
        name="Recommendation Rate (%)",
        marker=dict(color=GREEN, size=8),
        yaxis="y2",
        mode="markers+lines",
    ))
    
    fig.update_layout(
        title="Distribusi Kategori dengan Recommendation Rate",
        xaxis_title="Kategori Produk",
        yaxis_title="Total Records",
        yaxis2=dict(
            title="Recommendation Rate (%)",
            overlaying="y",
            side="right",
        ),
        hovermode="x unified",
        height=400,
        template="plotly_dark",
        paper_bgcolor=PANEL,
        plot_bgcolor=PANEL,
        font={"color": TEXT},
    )
    
    return fig


def segment_distribution_summary(df: pd.DataFrame) -> dict:
    """
    Return key RFM segment statistics for metric cards display.
    """
    rfm_data = rfm_segment_summary(df)
    
    total_products = len(rfm_data)
    high_quality = len(rfm_data[rfm_data["segment"] == "High Quality"])
    moderate_quality = len(rfm_data[rfm_data["segment"] == "Moderate Quality"])
    low_quality = len(rfm_data[rfm_data["segment"] == "Low Quality"])
    
    return {
        "total_products": total_products,
        "high_quality_count": high_quality,
        "high_quality_pct": int(high_quality / total_products * 100) if total_products > 0 else 0,
        "moderate_quality_count": moderate_quality,
        "low_quality_count": low_quality,
        "avg_frequency": int(rfm_data["frequency"].mean()),
        "max_frequency": int(rfm_data["frequency"].max()),
    }
