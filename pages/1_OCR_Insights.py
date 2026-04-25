"""
OCR Data Insights - Analisis kualitas data foto OCR dan hasil ekstraksi teks.
Menampilkan sebaran kualitas foto, distribusi panjang teks, dan analisis per kategori nutrisi.
"""

import streamlit as st

from utils.eda_visualizations import (
    ocr_quality_by_nutrient,
    ocr_quality_distribution,
    ocr_quality_summary_stats,
    ocr_text_length_distribution,
    ocr_vocabulary_analysis,
)
from utils.load_data import load_ocr_quality_data
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
    "OCR Insights",
    page_title="DiaBites DS | OCR Data Insights",
    page_icon="🔬",
)
sidebar_brand("OCR Insights")
sidebar_dataset_notes()


# ────────────────────────────────────────────────────────────
# Load & Validate Data
# ────────────────────────────────────────────────────────────
ocr_raw = load_ocr_quality_data()
if ocr_raw.empty:
    st.error("Dataset OCR quality kosong atau tidak dapat dibaca dari folder data.")
    st.stop()


# ────────────────────────────────────────────────────────────
# Hero & Summary Metrics
# ────────────────────────────────────────────────────────────
hero(
    "OCR Data Insights",
    "Analisis mendalam tentang kualitas data foto OCR: sebaran kualitas, hasil ekstraksi teks, dan pola karakter yang terdeteksi.",
)

stats = ocr_quality_summary_stats(ocr_raw)

metric_columns = st.columns(3)
with metric_columns[0]:
    metric_card("Total Gambar", f"{stats['total_images']:,}", "Dataset training OCR")
with metric_columns[1]:
    metric_card("Foto Berkualitas Baik", f"{stats['quality_good_pct']}%", "Status 'clear'")
with metric_columns[2]:
    metric_card("Foto Berkualitas Rendah", f"{stats['quality_poor_pct']}%", "Blur/Glare/Overlap")

st.divider()

# ────────────────────────────────────────────────────────────
# Quality Distribution Analysis
# ────────────────────────────────────────────────────────────
section_title("📊 Distribusi Kualitas Foto")
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        ocr_quality_distribution(ocr_raw),
        use_container_width=True,
    )

with col2:
    st.markdown("""
    **Insight:**
    - Kualitas foto yang baik ('clear') memastikan akurasi ekstraksi teks OCR
    - Foto blur atau dengan glare mengurangi performa model ekstraksi
    - Perlu augmentasi data (Gaussian Blur) untuk meningkatkan robustness
    """)

st.divider()

# ────────────────────────────────────────────────────────────
# Text Extraction Analysis
# ────────────────────────────────────────────────────────────
section_title("📝 Analisis Hasil Ekstraksi Teks")
col1, col2 = st.columns([2, 1])

with col1:
    st.plotly_chart(
        ocr_text_length_distribution(ocr_raw),
        use_container_width=True,
    )

with col2:
    st.markdown(f"""
    **Statistik Teks:**
    - Rata-rata panjang: **{stats['avg_text_length']} karakter**
    - Maksimal panjang: **{stats['max_text_length']} karakter**
    - Rekomendasi sequence length untuk RNN: **64-128 token**
    """)

st.divider()

# ────────────────────────────────────────────────────────────
# Quality by Nutrient Category
# ────────────────────────────────────────────────────────────
section_title("🏷️ Kualitas Foto Berdasarkan Kategori Nutrisi")
st.plotly_chart(
    ocr_quality_by_nutrient(ocr_raw),
    use_container_width=True,
)
st.markdown("""
**Interpretasi:**
- Kategori tertentu mungkin memiliki foto berkualitas lebih tinggi
- Identifikasi kategori dengan banyak blur/glare untuk pengambilan ulang foto
- Pastikan setiap kategori memiliki representasi data yang seimbang
""")

st.divider()

# ────────────────────────────────────────────────────────────
# Character Frequency & Vocabulary
# ────────────────────────────────────────────────────────────
section_title("📚 Analisis Karakter - Vocabulary Frequency")
st.plotly_chart(
    ocr_vocabulary_analysis(ocr_raw, top_n=20),
    use_container_width=True,
)
st.markdown(f"""
**Catatan Teknis:**
- Total unique karakter: **{stats['total_unique_characters']}** (vocabulary size)
- Analisis ini membantu dalam preprocessing dan tokenization
- Karakter dengan frekuensi tinggi adalah angka dan huruf nutrisi umum
""")

st.divider()

# ────────────────────────────────────────────────────────────
# Raw Data Preview
# ────────────────────────────────────────────────────────────
section_title("🔍 Preview Data OCR Quality")
st.dataframe(
    ocr_raw.head(50),
    use_container_width=True,
    hide_index=True,
)
