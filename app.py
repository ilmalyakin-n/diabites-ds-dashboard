import pandas as pd
import streamlit as st

from utils.charts import RECOMMENDATION_COLORS, bar_chart, heatmap_from_crosstab, histogram_chart
from utils.common import value_counts_frame
from utils.load_data import load_nutrition_data, load_ocr_quality_data
from utils.nutrition import (
    PROFILE_OPTIONS,
    diabetes_category_risk,
    diabetes_risk_insight,
    prepare_nutrition_data,
    profile_sensitivity_insight,
    profile_sensitivity_table,
    profile_status_distribution,
)
from utils.rfm_analysis import (
    category_distribution_rfm,
    segment_distribution_summary,
    product_frequency_analysis,
    recommendation_rate_by_product,
)
from utils.ui import (
    chart_subtitle,
    configure_page,
    hero,
    insight_box,
    metric_card,
    section_title,
    sidebar_brand,
    sidebar_dataset_notes,
)


# ────────────────────────────────────────────────────────────
# Page Setup
# ────────────────────────────────────────────────────────────
configure_page(
    "Overview",
    page_title="DiaBites DS Dashboard",
    page_icon="\U0001F4CA",
)
sidebar_brand("Overview")
sidebar_dataset_notes()


# ────────────────────────────────────────────────────────────
# Load & Validate Data
# ────────────────────────────────────────────────────────────
raw_nutrition_data = load_nutrition_data()
if raw_nutrition_data.empty:
    st.error("Dataset nutrisi kosong atau tidak dapat dibaca dari folder data.")
    st.stop()

nutrition_data = prepare_nutrition_data(raw_nutrition_data)

# Load OCR quality data
ocr_raw = load_ocr_quality_data()
ocr_data = pd.DataFrame()
if not ocr_raw.empty:
    ocr_data = ocr_raw.copy()
    # Derive quality_label from quality column
    if "quality" in ocr_data.columns:
        quality_mapping = {"clear": "Good", "blur": "Poor", "glare": "Poor", "overlap": "Medium"}
        ocr_data["quality_label"] = ocr_data["quality"].map(quality_mapping).fillna("Medium")
    # Derive nutrient_type from file_name
    if "file_name" in ocr_data.columns:
        ocr_data["nutrient_type"] = ocr_data["file_name"].str.extract(r"^([a-zA-Z_]+)_\d")[0]

# Dataset validation (collapsible)
with st.expander("📋 Validasi Dataset", expanded=False):
    validation_columns = st.columns(2)
    with validation_columns[0]:
        st.markdown("**nutrition_dataset.csv**")
        st.code(", ".join(raw_nutrition_data.columns.tolist()))
        st.caption(f"{len(raw_nutrition_data):,} baris")
    with validation_columns[1]:
        st.markdown("**ocr_dataset_quality.csv**")
        if not ocr_raw.empty:
            st.code(", ".join(ocr_raw.columns.tolist()))
            st.caption(f"{len(ocr_raw):,} baris")
        else:
            st.warning("Dataset tidak tersedia")


# ────────────────────────────────────────────────────────────
# Hero & Metrics
# ────────────────────────────────────────────────────────────
hero(
    "DiaBites DS Dashboard",
    "Dashboard interaktif untuk menganalisis kandungan nutrisi dan rekomendasi produk berdasarkan profil pengguna.",
)

total_products = nutrition_data["product_name"].nunique()
total_nutrition_rows = len(nutrition_data)
total_categories = nutrition_data["category"].nunique()
total_user_profiles = len(PROFILE_OPTIONS)

metric_columns = st.columns(4)
with metric_columns[0]:
    metric_card("Total Produk", f"{total_products:,}", "Produk unik di dataset")
with metric_columns[1]:
    metric_card("Total Data Nutrisi", f"{total_nutrition_rows:,}", "Baris nutrition_dataset.csv")
with metric_columns[2]:
    metric_card("Total Kategori Produk", f"{total_categories:,}", "Kategori hasil normalisasi")
with metric_columns[3]:
    metric_card("Total Profil Medis", f"{total_user_profiles:,}", "Termasuk diabetes tipe 1 dan tipe 2")

st.divider()


# ────────────────────────────────────────────────────────────
# Research Tabs
# ────────────────────────────────────────────────────────────
section_title("Jawaban Cepat Pertanyaan Riset")
question_tabs = st.tabs(
    [
        "1. Kualitas Foto OCR",
        "2. Risiko Diabetes",
        "3. Status Aman 7 Profil",
    ]
)

# --- Tab 1: Kualitas Foto OCR (from ocr_dataset_quality.csv) ---
with question_tabs[0]:
    if ocr_data.empty:
        st.warning("Dataset ocr_dataset_quality.csv kosong atau tidak ditemukan.")
    elif "quality_label" not in ocr_data.columns:
        st.info("Kolom 'quality' tidak ditemukan di ocr_dataset_quality.csv sehingga analisis kualitas foto tidak tersedia.")
    else:
        total_images = len(ocr_data)
        quality_vc = ocr_data["quality_label"].value_counts()
        summary_parts = []
        for label in ["Good", "Medium", "Poor"]:
            if label in quality_vc.index:
                count = int(quality_vc[label])
                pct = count / total_images * 100
                summary_parts.append(f"{label} {count} gambar ({pct:.0f}%)")
        insight_box(f"Dari {total_images} gambar yang dianalisis: {', '.join(summary_parts)}.")

        if "quality" in ocr_data.columns:
            problem_data = ocr_data[ocr_data["quality"] != "clear"]["quality"].value_counts()
            if len(problem_data) > 0:
                problem_parts = [f"{k} ({v} gambar)" for k, v in problem_data.items()]
                st.markdown(f"**Masalah yang ditemukan:** {', '.join(problem_parts)}")

        st.info("📊 Lihat section *Analisis Kualitas Foto OCR* di bawah untuk visualisasi lengkap.")


# --- Tab 2: Risiko Diabetes ---
with question_tabs[1]:
    diabetes_risk = diabetes_category_risk(nutrition_data)
    insight_box(diabetes_risk_insight(diabetes_risk))
    st.plotly_chart(
        bar_chart(
            diabetes_risk,
            "risk_score",
            "category",
            "Kategori Produk Indonesia Paling Berisiko untuk Diabetes",
            orientation="h",
            text="risk_score",
            height=430,
        ),
        width="stretch",
    )


# --- Tab 3: Status Aman 7 Profil ---
with question_tabs[2]:
    status_distribution = profile_status_distribution(nutrition_data)
    sensitivity_table = profile_sensitivity_table(nutrition_data)
    insight_box(profile_sensitivity_insight(sensitivity_table))
    st.plotly_chart(
        bar_chart(
            status_distribution,
            "selected_profile",
            "percent",
            "Perbedaan Status Aman pada 7 Profil Medis",
            color="recommendation",
            color_map=RECOMMENDATION_COLORS,
            text="percent",
            height=430,
        ),
        width="stretch",
    )
    st.dataframe(sensitivity_table, width="stretch", hide_index=True)

st.divider()


# ────────────────────────────────────────────────────────────
# Top 10 Categories + User Profiles
# ────────────────────────────────────────────────────────────
left_column, right_column = st.columns(2)

with left_column:
    section_title("10 Kategori Produk Terbanyak")
    category_counts = value_counts_frame(nutrition_data, "category", "total_products")
    if len(category_counts) > 8:
        top_categories = category_counts.head(10).sort_values("total_products", ascending=True)
        st.plotly_chart(
            bar_chart(
                top_categories,
                "total_products",
                "category",
                "10 Kategori Produk Terbanyak",
                orientation="h",
                text="total_products",
                height=420,
            ),
            width="stretch",
        )
    else:
        st.plotly_chart(
            bar_chart(
                category_counts,
                "category",
                "total_products",
                "Kategori Produk",
                text="total_products",
                height=420,
            ),
            width="stretch",
        )

with right_column:
    section_title("Jumlah Data per Profil Pengguna")

    PROFILE_FRIENDLY_LABELS = {
        "diabetes tipe 1": "Diabetes Tipe 1",
        "diabetes tipe 2": "Diabetes Tipe 2",
        "hipertensi": "Hipertensi",
        "diet": "Diet",
        "atlet": "Atlet",
        "anak": "Anak",
        "umum": "Umum",
    }

    profile_counts = value_counts_frame(nutrition_data, "user_profile", "total_rows")
    profile_counts["user_profile"] = profile_counts["user_profile"].map(
        lambda x: PROFILE_FRIENDLY_LABELS.get(x, x.title())
    )
    profile_counts = profile_counts.sort_values("total_rows", ascending=True)
    st.plotly_chart(
        bar_chart(
            profile_counts,
            "total_rows",
            "user_profile",
            "Jumlah Data per Profil Pengguna",
            orientation="h",
            text="total_rows",
            height=420,
        ),
        width="stretch",
    )

st.divider()


# ────────────────────────────────────────────────────────────
# Nutrient Distributions (3 separate cards)
# ────────────────────────────────────────────────────────────
section_title("Distribusi Kandungan Nutrisi")

sugar_q1, sugar_q3 = nutrition_data["sugar_g"].quantile(0.25), nutrition_data["sugar_g"].quantile(0.75)
sodium_q1, sodium_q3 = nutrition_data["sodium_mg"].quantile(0.25), nutrition_data["sodium_mg"].quantile(0.75)
cal_q1, cal_q3 = nutrition_data["calories"].quantile(0.25), nutrition_data["calories"].quantile(0.75)

histogram_columns = st.columns(3)
with histogram_columns[0]:
    chart_subtitle(f"Sebagian besar produk memiliki gula {sugar_q1:.0f}\u2013{sugar_q3:.0f} gram.")
    st.plotly_chart(
        histogram_chart(nutrition_data, "sugar_g", "Distribusi Gula", nbins=25),
        width="stretch",
    )
with histogram_columns[1]:
    chart_subtitle(f"Sebagian besar produk memiliki sodium {sodium_q1:.0f}\u2013{sodium_q3:.0f} mg.")
    st.plotly_chart(
        histogram_chart(nutrition_data, "sodium_mg", "Distribusi Sodium", nbins=25),
        width="stretch",
    )
with histogram_columns[2]:
    chart_subtitle(f"Sebagian besar produk memiliki kalori {cal_q1:.0f}\u2013{cal_q3:.0f} kkal.")
    st.plotly_chart(
        histogram_chart(nutrition_data, "calories", "Distribusi Kalori", nbins=25),
        width="stretch",
    )

st.divider()


# ────────────────────────────────────────────────────────────
# OCR Quality Analysis  (from ocr_dataset_quality.csv)
# ────────────────────────────────────────────────────────────
section_title("Analisis Kualitas Foto OCR")
st.caption("Sumber data: ocr_dataset_quality.csv")

if ocr_data.empty:
    st.warning("Dataset ocr_dataset_quality.csv tidak tersedia atau kosong.")
else:
    # ── Row 1: Quality distribution + Photo problems ──
    ocr_left, ocr_right = st.columns(2)

    with ocr_left:
        if "quality_label" in ocr_data.columns:
            quality_counts = ocr_data["quality_label"].value_counts().reset_index()
            quality_counts.columns = ["quality_label", "jumlah"]
            sort_order = {"Good": 0, "Medium": 1, "Poor": 2}
            quality_counts["sort_order"] = quality_counts["quality_label"].map(sort_order)
            quality_counts = quality_counts.sort_values("sort_order").drop("sort_order", axis=1)
            quality_color_map = {"Good": "#22C55E", "Medium": "#F59E0B", "Poor": "#EF4444"}
            st.plotly_chart(
                bar_chart(
                    quality_counts,
                    "quality_label",
                    "jumlah",
                    "Distribusi Kualitas Gambar",
                    color="quality_label",
                    color_map=quality_color_map,
                    text="jumlah",
                    height=400,
                ),
                width="stretch",
            )
        else:
            st.info("Visualisasi ini tidak tersedia karena kolom 'quality' belum ada di dataset.")

    with ocr_right:
        if "quality" in ocr_data.columns:
            problems = ocr_data[ocr_data["quality"] != "clear"]
            if not problems.empty:
                problem_counts = problems["quality"].value_counts().reset_index()
                problem_counts.columns = ["masalah", "jumlah"]
                problem_counts = problem_counts.sort_values("jumlah", ascending=True)
                st.plotly_chart(
                    bar_chart(
                        problem_counts,
                        "jumlah",
                        "masalah",
                        "Masalah Foto yang Paling Sering Terjadi",
                        orientation="h",
                        text="jumlah",
                        height=400,
                    ),
                    width="stretch",
                )
            else:
                st.info("Tidak ada masalah foto yang ditemukan di dataset.")
        else:
            st.info("Visualisasi ini tidak tersedia karena kolom 'quality' belum ada di dataset.")

    # ── Row 2: Heatmap nutrient_type vs quality_label ──
    has_nutrient_type = "nutrient_type" in ocr_data.columns
    has_quality_label = "quality_label" in ocr_data.columns

    if has_nutrient_type and has_quality_label:
        crosstab = pd.crosstab(ocr_data["nutrient_type"], ocr_data["quality_label"])
        column_order = [c for c in ["Good", "Medium", "Poor"] if c in crosstab.columns]
        crosstab = crosstab[column_order]
        st.plotly_chart(
            heatmap_from_crosstab(crosstab, "Heatmap: Jenis Nutrisi vs Kualitas Foto", height=380),
            width="stretch",
        )
    else:
        missing_cols = []
        if not has_nutrient_type:
            missing_cols.append("nutrient_type (diturunkan dari file_name)")
        if not has_quality_label:
            missing_cols.append("quality_label (diturunkan dari quality)")
        st.info(
            f"Heatmap tidak ditampilkan karena kolom berikut tidak tersedia: {', '.join(missing_cols)}"
        )

    # ── Row 3: Auto insights ──
    section_title("Insight Otomatis")
    generated_insights = []

    if "quality_label" in ocr_data.columns:
        dominant_vc = ocr_data["quality_label"].value_counts()
        dominant_label = dominant_vc.index[0]
        dominant_pct = dominant_vc.values[0] / len(ocr_data) * 100
        generated_insights.append(
            f"Sebagian besar gambar termasuk kategori {dominant_label} ({dominant_pct:.0f}%)."
        )

    if "quality" in ocr_data.columns:
        problem_vc = ocr_data[ocr_data["quality"] != "clear"]["quality"].value_counts()
        if len(problem_vc) > 0:
            top_problems = problem_vc.head(2)
            problem_text = " dan ".join([f"{k} ({v} gambar)" for k, v in top_problems.items()])
            generated_insights.append(f"Masalah yang paling sering terjadi adalah {problem_text}.")

    if has_nutrient_type and has_quality_label:
        poor_images = ocr_data[ocr_data["quality_label"] == "Poor"]
        if not poor_images.empty:
            poor_by_nutrient = poor_images["nutrient_type"].value_counts()
            if poor_by_nutrient.max() > poor_by_nutrient.min():
                worst_nutrients = poor_by_nutrient.head(2).index.tolist()
                generated_insights.append(
                    f"Kandungan {' dan '.join(worst_nutrients)} paling sering memiliki kualitas Poor."
                )
            else:
                avg_poor = poor_by_nutrient.mean()
                generated_insights.append(
                    f"Semua jenis nutrisi memiliki sekitar {avg_poor:.0f} gambar berkualitas Poor."
                )

    if generated_insights:
        for insight_text in generated_insights:
            insight_box(insight_text)
    else:
        st.info("Tidak ada insight yang dapat dihasilkan dari data saat ini.")

st.divider()


# ────────────────────────────────────────────────────────────
# RFM Analysis - Product Segmentation & Quality Insights
# ────────────────────────────────────────────────────────────
section_title("RFM Analysis - Product Segmentation")

rfm_stats = segment_distribution_summary(nutrition_data)

rfm_metric_columns = st.columns(4)
with rfm_metric_columns[0]:
    metric_card("Total Produk Unik", f"{rfm_stats['total_products']:,}", "Frequency measure")
with rfm_metric_columns[1]:
    metric_card("High Quality", f"{rfm_stats['high_quality_count']:,}", f"{rfm_stats['high_quality_pct']}% dari total")
with rfm_metric_columns[2]:
    metric_card("Rata-rata Frekuensi", f"{rfm_stats['avg_frequency']}", "Records per product")
with rfm_metric_columns[3]:
    metric_card("Frekuensi Maksimal", f"{rfm_stats['max_frequency']}", "Produk paling sering muncul")

st.divider()

rfm_col1, rfm_col2 = st.columns(2)

with rfm_col1:
    st.plotly_chart(
        product_frequency_analysis(nutrition_data),
        use_container_width=True,
    )

with rfm_col2:
    st.plotly_chart(
        recommendation_rate_by_product(nutrition_data),
        use_container_width=True,
    )

st.divider()

section_title("Kategori vs Recommendation Rate")
st.plotly_chart(
    category_distribution_rfm(nutrition_data),
    use_container_width=True,
)

st.markdown("""
**RFM Analysis Insight:**
- **Frequency**: Top products muncul lebih sering di berbagai profil user
- **Recommendation Rate**: Proxy untuk quality - produk dengan rate tinggi = quality baik
- **Category Analysis**: Kategori tertentu memiliki recommendation rate lebih tinggi
- Gunakan analisis ini untuk identifying premium vs problematic products
""")

st.divider()


# ────────────────────────────────────────────────────────────
# Preview Dataset
# ────────────────────────────────────────────────────────────
section_title("Preview Dataset Nutrisi")
st.dataframe(nutrition_data.head(20), width="stretch", hide_index=True)
