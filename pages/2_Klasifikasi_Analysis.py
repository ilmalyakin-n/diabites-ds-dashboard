"""
Klasifikasi Data Distribution - Analisis sebaran dataset nutrisi hasil augmentasi.
Menampilkan distribusi gula, sodium, korelasi nutrisi, dan rekomendasi per profil diabetes.
"""

import streamlit as st

from utils.eda_visualizations import (
    nutrition_correlation_heatmap,
    nutrition_recommendation_by_diabetes,
    nutrition_sodium_distribution,
    nutrition_sugar_by_recommendation,
    nutrition_sugar_distribution,
    nutrition_summary_stats,
)
from utils.load_data import load_nutrition_data
from utils.nutrition import prepare_nutrition_data
from utils.ui import (
    configure_page,
    hero,
    metric_card,
    section_title,
    sidebar_brand,
    sidebar_dataset_notes,
)


# ────────────────────────────────────────────────────────────
# Page Setup
# ────────────────────────────────────────────────────────────
configure_page(
    "Klasifikasi Analysis",
    page_title="DiaBites DS | Klasifikasi Data Distribution",
    page_icon="📈",
)
sidebar_brand("Klasifikasi Analysis")
sidebar_dataset_notes()


# ────────────────────────────────────────────────────────────
# Load & Validate Data
# ────────────────────────────────────────────────────────────
raw_nutrition_data = load_nutrition_data()
if raw_nutrition_data.empty:
    st.error("Dataset nutrisi kosong atau tidak dapat dibaca dari folder data.")
    st.stop()

nutrition_data = prepare_nutrition_data(raw_nutrition_data)


# ────────────────────────────────────────────────────────────
# Hero & Summary Metrics
# ────────────────────────────────────────────────────────────
hero(
    "Klasifikasi Data Distribution",
    "Analisis sebaran dataset nutrition hasil augmentasi dengan 7 profil medis. Memahami distribusi rekomendasi, korelasi nutrisi, dan karakteristik produk.",
)

stats = nutrition_summary_stats(nutrition_data)

metric_columns = st.columns(4)
with metric_columns[0]:
    metric_card("Total Records", f"{stats['total_records']:,}", "Hasil augmentasi 7 profil")
with metric_columns[1]:
    metric_card("Produk Unik", f"{stats['total_unique_products']:,}", "Distinct products")
with metric_columns[2]:
    metric_card("Recommended", f"{stats['recommended_pct']}%", "Status rekomendasi")
with metric_columns[3]:
    metric_card("Not Recommended", f"{stats['not_recommended_pct']}%", "Produk tidak aman")

st.divider()

# ────────────────────────────────────────────────────────────
# Sugar & Sodium Distribution
# ────────────────────────────────────────────────────────────
section_title("📊 Distribusi Kandungan Nutrisi Kritis")

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(
        nutrition_sugar_distribution(nutrition_data),
        use_container_width=True,
    )

with col2:
    st.plotly_chart(
        nutrition_sodium_distribution(nutrition_data),
        use_container_width=True,
    )

st.markdown("""
**Key Finding:**
- Kandungan gula terkonsentrasi di range 0-15g dengan beberapa outlier
- Sodium bervariasi signifikan - penting untuk profil hipertensi
- Identifikasi outlier membantu dalam validasi data
""")

st.divider()

# ────────────────────────────────────────────────────────────
# Nutrient Correlation
# ────────────────────────────────────────────────────────────
section_title("🔗 Korelasi Antar Nutrisi")
col1, col2 = st.columns([1.5, 1])

with col1:
    st.plotly_chart(
        nutrition_correlation_heatmap(nutrition_data),
        use_container_width=True,
    )

with col2:
    st.markdown("""
    **Insight Korelasi:**
    - **Calorie-Fat (0.76)**: Korelasi kuat
    - **Calorie-Carbs (0.64)**: Korelasi sedang
    - Nutrisi independen bermanfaat untuk profil berbeda
    - Model rekomendasi dapat memanfaatkan hubungan ini
    """)

st.divider()

# ────────────────────────────────────────────────────────────
# Recommendation Distribution by Diabetes Type
# ────────────────────────────────────────────────────────────
section_title("⚕️ Distribusi Rekomendasi Berdasarkan Profil Diabetes")
st.plotly_chart(
    nutrition_recommendation_by_diabetes(nutrition_data),
    use_container_width=True,
)
st.markdown("""
**Insight Penting:**
- Pengguna normal: mayoritas produk "Recommended" (safe)
- Diabetes Type 1: "Recommended" menurun drastis, "Not Recommended" meningkat 3x
- Diabetes Type 2: Lebih fleksibel dibanding Type 1, tapi tetap strict pada gula
- Profil berbeda memerlukan strategi rekomendasi yang berbeda
""")

st.divider()

# ────────────────────────────────────────────────────────────
# Sugar Distribution by Recommendation Status
# ────────────────────────────────────────────────────────────
section_title("🍬 Kandungan Gula Berdasarkan Status Rekomendasi")
st.plotly_chart(
    nutrition_sugar_by_recommendation(nutrition_data),
    use_container_width=True,
)
st.markdown("""
**Pola Penting:**
- **Recommended**: Median ~0g gula - strict zero sugar policy
- **Caution**: Range 5-15g - moderate sugar content
- **Not Recommended**: Average >10g - terlalu banyak gula untuk diabetes
- Validasi scoring algorithm tersebut akurat
""")

st.divider()

# ────────────────────────────────────────────────────────────
# Raw Data Preview
# ────────────────────────────────────────────────────────────
section_title("🔍 Preview Data Klasifikasi")
st.dataframe(
    nutrition_data.head(100),
    use_container_width=True,
    hide_index=True,
)

# ────────────────────────────────────────────────────────────
# Data Quality Notes
# ────────────────────────────────────────────────────────────
st.divider()
with st.expander("📋 Catatan Kualitas Data", expanded=False):
    st.markdown("""
    **Dataset Augmentation Pipeline:**
    1. Raw products loaded dari sumber original
    2. Augmented dengan 7 profil medis berbeda (age_group × bmi_category × diabetes_type)
    3. Setiap kombinasi di-score menggunakan nutrient-based rules
    4. Hasil: 3-label classification (Recommended/Caution/Not Recommended)
    
    **Kolom Dataset:**
    - product_name: Nama produk
    - Nutrien: sugar_g, carbs_g, calories, sodium_mg, fat_g
    - Profil: age_group, bmi_category, diabetes_type
    - Label: Rekomendasi final berdasarkan rules
    """)
