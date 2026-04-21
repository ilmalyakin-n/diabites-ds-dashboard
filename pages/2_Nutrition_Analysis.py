import streamlit as st

from utils.charts import RECOMMENDATION_COLORS, bar_chart, box_chart, scatter_chart
from utils.load_data import load_nutrition_data
from utils.nutrition import (
    PROFILE_OPTIONS,
    RECOMMENDATION_OPTIONS,
    available_display_columns,
    diabetes_category_risk,
    diabetes_risk_insight,
    filter_nutrition_data,
    not_recommended_reason_counts,
    nutrition_insight,
    prepare_nutrition_data,
    profile_sensitivity_insight,
    profile_sensitivity_table,
    score_products,
)
from utils.ui import configure_page, hero, insight_box, metric_card, section_title, sidebar_brand


configure_page("Nutrition Analysis", page_title="DiaBites DS | Nutrition Analysis")
sidebar_brand("Nutrition Analysis")

raw_nutrition_data = load_nutrition_data()
if raw_nutrition_data.empty:
    st.error("Dataset nutrisi kosong atau tidak dapat dibaca dari folder data.")
    st.stop()

nutrition_data = prepare_nutrition_data(raw_nutrition_data)

st.sidebar.markdown("## Filter")
selected_profile = st.sidebar.selectbox("user_profile", PROFILE_OPTIONS)
category_options = sorted(nutrition_data["category"].dropna().unique())
selected_categories = st.sidebar.multiselect("category", category_options, default=category_options)
selected_recommendations = st.sidebar.multiselect(
    "recommendation",
    RECOMMENDATION_OPTIONS,
    default=RECOMMENDATION_OPTIONS,
)

scored_data = score_products(nutrition_data, selected_profile)
filtered_data = filter_nutrition_data(scored_data, selected_categories, selected_recommendations)

hero(
    "Nutrition Analysis",
    "Menjawab alasan produk tidak aman, kategori paling berisiko bagi diabetes, dan perubahan status pada 7 profil medis.",
)

if filtered_data.empty:
    st.warning("Tidak ada produk yang sesuai dengan filter saat ini.")
    st.stop()

recommended_count = int((filtered_data["recommendation"] == "Recommended").sum())
caution_count = int((filtered_data["recommendation"] == "Caution").sum())
not_recommended_count = int((filtered_data["recommendation"] == "Not Recommended").sum())
average_score = filtered_data["score"].mean()

metric_columns = st.columns(4)
with metric_columns[0]:
    metric_card("Profil Analisis", selected_profile.title())
with metric_columns[1]:
    metric_card("Recommended", f"{recommended_count:,}")
with metric_columns[2]:
    metric_card("Caution", f"{caution_count:,}")
with metric_columns[3]:
    metric_card("Not Recommended", f"{not_recommended_count:,}", f"Average score {average_score:.1f}")

insight_message, insight_severity = nutrition_insight(filtered_data)
if insight_severity == "warning":
    st.warning(insight_message)
else:
    insight_box(insight_message)

section_title("Tabel Data Hasil Filter")
display_columns = available_display_columns(filtered_data)
st.dataframe(
    filtered_data[display_columns].sort_values("score", ascending=False),
    width="stretch",
    hide_index=True,
)

st.divider()

left_column, right_column = st.columns(2)
with left_column:
    section_title("Top Alasan Produk Caution/Not Recommended")
    reason_counts = not_recommended_reason_counts(filtered_data)
    st.plotly_chart(
        bar_chart(
            reason_counts,
            "total_products",
            "reason",
            "Kandungan yang Paling Sering Membuat Produk Tidak Direkomendasikan",
            orientation="h",
            text="total_products",
            height=420,
        ),
        width="stretch",
    )

with right_column:
    section_title("Boxplot Calories per Category")
    st.plotly_chart(
        box_chart(
            filtered_data,
            "category",
            "calories",
            "Boxplot Calories per Category",
            color="category",
            height=420,
        ),
        width="stretch",
    )

st.divider()

section_title("Scatter Plot Sugar vs Sodium")
st.plotly_chart(
    scatter_chart(
        filtered_data,
        "sugar_g",
        "sodium_mg",
        "Scatter Plot Sugar vs Sodium",
        color="recommendation",
        size="score",
        height=470,
        color_map=RECOMMENDATION_COLORS,
        hover_name="product_name",
        hover_data=["category", "reason", "score", "calories", "protein_g"],
    ),
    width="stretch",
)

st.divider()

diabetes_column, profile_column = st.columns(2)
with diabetes_column:
    section_title("Kategori Produk Paling Berisiko untuk Diabetes")
    diabetes_risk = diabetes_category_risk(nutrition_data)
    insight_box(diabetes_risk_insight(diabetes_risk))
    st.plotly_chart(
        bar_chart(
            diabetes_risk,
            "risk_score",
            "category",
            "Risk Score Diabetes Tipe 1 dan Tipe 2",
            orientation="h",
            text="risk_score",
            height=430,
        ),
        width="stretch",
    )

with profile_column:
    section_title("Perubahan Status Aman pada 7 Profil Medis")
    sensitivity_table = profile_sensitivity_table(nutrition_data)
    insight_box(profile_sensitivity_insight(sensitivity_table))
    st.dataframe(sensitivity_table, width="stretch", hide_index=True)
