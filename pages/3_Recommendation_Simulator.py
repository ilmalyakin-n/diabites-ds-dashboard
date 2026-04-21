import html

import streamlit as st

from utils.charts import RECOMMENDATION_COLORS, bar_chart, nutrition_comparison_bar
from utils.load_data import load_nutrition_data
from utils.nutrition import (
    GENDER_OPTIONS,
    PROFILE_OPTIONS,
    TARGET_OPTIONS,
    available_display_columns,
    comparison_frame,
    prepare_nutrition_data,
    profile_summary,
    recommendation_explanation,
    score_products,
    status_products,
    top_recommended_products,
)
from utils.ui import configure_page, empty_state, hero, insight_box, metric_card, section_title, sidebar_brand, status_badge


configure_page("Recommendation Simulator", page_title="DiaBites DS | Recommendation Simulator")
sidebar_brand("Recommendation Simulator")

raw_nutrition_data = load_nutrition_data()
if raw_nutrition_data.empty:
    st.error("Dataset nutrisi kosong atau tidak dapat dibaca dari folder data.")
    st.stop()

nutrition_data = prepare_nutrition_data(raw_nutrition_data)

hero(
    "Recommendation Simulator",
    "Simulasikan profil pengguna untuk menemukan produk yang paling sesuai dengan kebutuhan nutrisi.",
)

with st.form("recommendation_form"):
    form_columns = st.columns(3)
    with form_columns[0]:
        age = st.number_input("usia", min_value=1, max_value=100, value=30, step=1)
        gender = st.selectbox("jenis kelamin", GENDER_OPTIONS)
    with form_columns[1]:
        health_condition = st.selectbox("kondisi kesehatan", PROFILE_OPTIONS)
        target = st.selectbox("target", TARGET_OPTIONS)
    with form_columns[2]:
        max_results = st.slider("jumlah produk", min_value=5, max_value=10, value=10)

    submitted = st.form_submit_button("Tampilkan rekomendasi")

if not submitted:
    st.info("Isi profil pengguna lalu tekan tombol untuk melihat rekomendasi produk.")
    st.stop()

scored_data = score_products(nutrition_data, health_condition, target)
recommended_products = top_recommended_products(scored_data, max_results)
caution_products = status_products(scored_data, "Caution", 5, ascending=False)
not_recommended_products = status_products(scored_data, "Not Recommended", 5, ascending=True)

section_title("Profil Nutrisi yang Digunakan")
metric_columns = st.columns(4)
with metric_columns[0]:
    metric_card("Usia", f"{age} tahun")
with metric_columns[1]:
    metric_card("Jenis Kelamin", gender.title())
with metric_columns[2]:
    metric_card("Kondisi", health_condition.title())
with metric_columns[3]:
    metric_card("Target", target.title())

insight_box(profile_summary(health_condition, target))

if recommended_products.empty:
    empty_state(
        "Belum ada produk yang cocok untuk kombinasi profil ini. "
        "Coba target yang lebih umum atau cek produk dengan kadar gula, sodium, dan kalori lebih rendah."
    )
else:
    section_title("5-10 Produk Paling Direkomendasikan")
    for _, product_row in recommended_products.iterrows():
        product_name = html.escape(str(product_row["product_name"]))
        category = html.escape(str(product_row["category"]))
        reason = html.escape(str(product_row["reason"]))
        score = float(product_row["score"])
        st.markdown(
            f"""
            <div class="product-card">
                <div style="display:flex;justify-content:space-between;gap:1rem;align-items:center;flex-wrap:wrap;">
                    <div>
                        <div style="color:#FFFFFF;font-weight:800;font-size:1.05rem;">{product_name}</div>
                        <div style="color:#D1D5DB;">Kategori: {category} | Score: {score:.1f}</div>
                        <div style="color:#D1D5DB;margin-top:0.35rem;">Alasan: {reason}</div>
                    </div>
                    {status_badge("Recommended", "Recommended")}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.download_button(
        "Download hasil rekomendasi ke CSV",
        data=recommended_products[available_display_columns(recommended_products)].to_csv(index=False).encode("utf-8"),
        file_name="diabites_recommendations.csv",
        mime="text/csv",
    )

    st.divider()

    left_column, right_column = st.columns(2)
    with left_column:
        section_title("Top 10 Produk Recommended")
        st.plotly_chart(
            bar_chart(
                recommended_products,
                "score",
                "product_name",
                "Top 10 Produk Recommended",
                color="recommendation",
                color_map=RECOMMENDATION_COLORS,
                orientation="h",
                text="score",
                height=430,
            ),
            width="stretch",
        )

    with right_column:
        section_title("Perbandingan Nutrisi Produk Terpilih")
        selected_product = st.selectbox(
            "pilih produk",
            recommended_products["product_name"].tolist(),
        )
        selected_row = recommended_products[recommended_products["product_name"] == selected_product].iloc[0]
        st.plotly_chart(
            nutrition_comparison_bar(
                comparison_frame(selected_row),
                "Sugar, Sodium, Protein, dan Calories",
                height=430,
            ),
            width="stretch",
        )

    section_title("Kenapa Produk Ini Direkomendasikan?")
    insight_box(recommendation_explanation(selected_row, health_condition, target))

if not caution_products.empty:
    st.divider()
    section_title("Produk Status Caution")
    for _, caution_row in caution_products.iterrows():
        st.markdown(
            f"""
            <div class="product-card">
                <div style="display:flex;justify-content:space-between;gap:1rem;align-items:center;flex-wrap:wrap;">
                    <div>
                        <div style="color:#FFFFFF;font-weight:800;">{html.escape(str(caution_row["product_name"]))}</div>
                        <div style="color:#D1D5DB;">Alasan: {html.escape(str(caution_row["reason"]))}</div>
                    </div>
                    {status_badge("Caution", "Caution")}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

if not not_recommended_products.empty:
    st.divider()
    section_title("Produk Not Recommended")
    for _, not_recommended_row in not_recommended_products.iterrows():
        st.markdown(
            f"""
            <div class="product-card">
                <div style="display:flex;justify-content:space-between;gap:1rem;align-items:center;flex-wrap:wrap;">
                    <div>
                        <div style="color:#FFFFFF;font-weight:800;">{html.escape(str(not_recommended_row["product_name"]))}</div>
                        <div style="color:#D1D5DB;">Alasan: {html.escape(str(not_recommended_row["reason"]))}</div>
                    </div>
                    {status_badge("Not Recommended", "Not Recommended")}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
