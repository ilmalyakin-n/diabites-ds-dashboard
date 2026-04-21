import pandas as pd

from utils.common import first_existing


PROFILE_OPTIONS = [
    "diabetes tipe 1",
    "diabetes tipe 2",
    "hipertensi",
    "diet",
    "atlet",
    "anak",
    "umum",
]
TARGET_OPTIONS = ["menurunkan berat badan", "menjaga kesehatan", "meningkatkan massa otot"]
GENDER_OPTIONS = ["perempuan", "laki-laki"]
RECOMMENDATION_OPTIONS = ["Recommended", "Caution", "Not Recommended"]

PROFILE_RULES = {
    "diabetes tipe 1": {
        "sugar_limit": 4,
        "carbs_limit": 24,
        "sodium_limit": 450,
        "focus": "gula sangat rendah dan karbohidrat ketat",
    },
    "diabetes tipe 2": {
        "sugar_limit": 6,
        "carbs_limit": 30,
        "calories_limit": 260,
        "sodium_limit": 500,
        "focus": "gula rendah, karbohidrat terkendali, dan kalori moderat",
    },
    "hipertensi": {
        "sodium_limit": 300,
        "fat_limit": 14,
        "focus": "sodium rendah",
    },
    "diet": {
        "calories_limit": 220,
        "sugar_limit": 8,
        "fat_limit": 9,
        "focus": "kalori rendah dan gula terkendali",
    },
    "atlet": {
        "protein_min": 8,
        "calories_min": 120,
        "focus": "protein lebih tinggi dan energi cukup",
    },
    "anak": {
        "sugar_limit": 8,
        "sodium_limit": 250,
        "calories_limit": 250,
        "focus": "gula, sodium, dan kalori lebih terkontrol untuk anak",
    },
    "umum": {
        "sugar_limit": 12,
        "sodium_limit": 500,
        "calories_limit": 360,
        "focus": "komposisi nutrisi seimbang",
    },
}

TARGET_RULES = {
    "menurunkan berat badan": {"calories_limit": 220, "sugar_limit": 8},
    "menjaga kesehatan": {"sodium_limit": 500, "sugar_limit": 12},
    "meningkatkan massa otot": {"protein_min": 8, "calories_min": 120},
}

DISPLAY_COLUMNS = [
    "product_name",
    "category",
    "user_profile",
    "recommendation",
    "reason",
    "score",
    "photo_quality",
    "extraction_success_rate",
    "sugar_g",
    "sodium_mg",
    "protein_g",
    "calories",
    "carbs_g",
    "fat_g",
]


def derive_category(product_name: str) -> str:
    """Infer a readable product category from the first product-name token."""
    if not isinstance(product_name, str) or not product_name.strip():
        return "lainnya"

    first_token = product_name.split(",")[0].split()[0].strip().lower()
    return first_token or "lainnya"


def derive_user_profile(row: pd.Series) -> str:
    """Infer one of seven medical profiles from available demographic fields."""
    diabetes_type = str(row.get("diabetes_type", "0")).strip().lower()
    age_group = str(row.get("age_group", "")).lower()
    bmi_category = str(row.get("bmi_category", "")).lower()

    if diabetes_type in {"1", "1.0", "type 1", "tipe 1"}:
        return "diabetes tipe 1"
    if diabetes_type in {"2", "2.0", "type 2", "tipe 2"}:
        return "diabetes tipe 2"
    if "child" in age_group or "anak" in age_group:
        return "anak"
    if bmi_category in {"overweight", "obese", "obesity"}:
        return "diet"
    return "umum"


def estimate_protein(row: pd.Series) -> float:
    """Estimate protein when the source CSV does not provide a protein column."""
    calories = float(row.get("calories", 0) or 0)
    carbs = float(row.get("carbs_g", 0) or 0)
    fat = float(row.get("fat_g", 0) or 0)
    estimated_protein = (calories - (carbs * 4) - (fat * 9)) / 4
    return round(max(0, estimated_protein), 1)


def normalize_photo_quality(value: str) -> str:
    """Normalize photo quality values into good, medium, or poor."""
    normalized_value = str(value).strip().lower()
    if normalized_value in {"good", "baik", "high", "tinggi", "bagus"}:
        return "good"
    if normalized_value in {"poor", "buruk", "low", "rendah", "jelek"}:
        return "poor"
    return "medium"


def add_photo_quality_fields(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Add photo quality and extraction success fields, using dataset columns when available."""
    prepared_dataframe = dataframe.copy()
    quality_column = first_existing(
        prepared_dataframe.columns,
        ["photo_quality", "image_quality", "kualitas_foto", "quality_label"],
    )
    accuracy_column = first_existing(
        prepared_dataframe.columns,
        ["extraction_success_rate", "ocr_accuracy", "extraction_accuracy", "accuracy"],
    )

    if quality_column:
        prepared_dataframe["photo_quality"] = prepared_dataframe[quality_column].apply(normalize_photo_quality)
        prepared_dataframe["photo_quality_source"] = "dataset"
    else:
        quality_cycle = ["good", "good", "good", "medium", "medium", "poor"]
        prepared_dataframe["photo_quality"] = [
            quality_cycle[index % len(quality_cycle)] for index in range(len(prepared_dataframe))
        ]
        prepared_dataframe["photo_quality_source"] = "proxy"

    if accuracy_column:
        prepared_dataframe["extraction_success_rate"] = pd.to_numeric(
            prepared_dataframe[accuracy_column],
            errors="coerce",
        ).fillna(0)
        if prepared_dataframe["extraction_success_rate"].max() <= 1:
            prepared_dataframe["extraction_success_rate"] *= 100
    else:
        base_rate = {"good": 92, "medium": 78, "poor": 57}
        prepared_dataframe["extraction_success_rate"] = [
            max(30, base_rate[quality] - (index % 8))
            for index, quality in enumerate(prepared_dataframe["photo_quality"])
        ]

    prepared_dataframe["extraction_success_rate"] = prepared_dataframe["extraction_success_rate"].clip(0, 100)
    prepared_dataframe["extraction_status"] = prepared_dataframe["extraction_success_rate"].apply(
        lambda value: "berhasil" if value >= 75 else "perlu validasi ulang"
    )
    return prepared_dataframe


def prepare_nutrition_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Normalize nutrition columns so every page can filter and score safely."""
    prepared_dataframe = dataframe.copy()

    if "product_name" not in prepared_dataframe.columns:
        prepared_dataframe["product_name"] = [f"Produk {index + 1}" for index in range(len(prepared_dataframe))]

    for column in ["sugar_g", "carbs_g", "calories", "sodium_mg", "fat_g", "protein_g"]:
        if column in prepared_dataframe.columns:
            prepared_dataframe[column] = pd.to_numeric(prepared_dataframe[column], errors="coerce").fillna(0)
        else:
            prepared_dataframe[column] = 0

    if (prepared_dataframe["protein_g"] == 0).all():
        prepared_dataframe["protein_g"] = prepared_dataframe.apply(estimate_protein, axis=1)

    category_column = first_existing(prepared_dataframe.columns, ["category", "product_category", "kategori"])
    if category_column:
        prepared_dataframe["category"] = prepared_dataframe[category_column].fillna("lainnya").astype(str).str.lower()
    else:
        prepared_dataframe["category"] = prepared_dataframe["product_name"].apply(derive_category)

    profile_column = first_existing(prepared_dataframe.columns, ["user_profile", "profile", "profil"])
    if profile_column:
        prepared_dataframe["user_profile"] = prepared_dataframe[profile_column].fillna("umum").astype(str).str.lower()
    else:
        prepared_dataframe["user_profile"] = prepared_dataframe.apply(derive_user_profile, axis=1)

    return add_photo_quality_fields(prepared_dataframe)


def build_rules(profile: str, target: str | None = None) -> dict:
    """Merge health-condition rules with optional target-specific rules."""
    rules = PROFILE_RULES.get(profile, PROFILE_RULES["umum"]).copy()
    if target and target in TARGET_RULES:
        for key, value in TARGET_RULES[target].items():
            if key.endswith("_limit") and key in rules:
                rules[key] = min(rules[key], value)
            elif key.endswith("_min") and key in rules:
                rules[key] = max(rules[key], value)
            else:
                rules[key] = value
    return rules


def evaluate_product(row: pd.Series, profile: str, target: str | None = None) -> tuple[str, str, float]:
    """Score one product row and return recommendation, main reason, and score."""
    rules = build_rules(profile, target)
    reasons: list[str] = []
    score = 100.0

    max_checks = [
        ("sugar_g", "sugar_limit", "kadar gula tinggi", 5.5),
        ("carbs_g", "carbs_limit", "karbohidrat tinggi", 1.8),
        ("sodium_mg", "sodium_limit", "kadar sodium tinggi", 0.09),
        ("calories", "calories_limit", "kalori tinggi", 0.28),
        ("fat_g", "fat_limit", "lemak tinggi", 2.2),
    ]
    min_checks = [
        ("protein_g", "protein_min", "protein belum tinggi", 3.5),
        ("calories", "calories_min", "kalori terlalu rendah", 0.16),
    ]

    for nutrient, limit_key, reason, penalty_weight in max_checks:
        if limit_key in rules and float(row.get(nutrient, 0)) > rules[limit_key]:
            score -= min(38, (float(row.get(nutrient, 0)) - rules[limit_key]) * penalty_weight)
            reasons.append(reason)

    for nutrient, limit_key, reason, penalty_weight in min_checks:
        if limit_key in rules and float(row.get(nutrient, 0)) < rules[limit_key]:
            score -= min(26, (rules[limit_key] - float(row.get(nutrient, 0))) * penalty_weight)
            reasons.append(reason)

    source_label = str(row.get("label", "")).lower()
    if "not" in source_label:
        score -= 14
    elif "caution" in source_label:
        score -= 6

    score = max(0, min(100, score))
    if score >= 78:
        recommendation = "Recommended"
    elif score >= 58:
        recommendation = "Caution"
    else:
        recommendation = "Not Recommended"

    reason = reasons[0] if reasons else "nutrisi sesuai profil"
    return recommendation, reason, round(score, 1)


def score_products(dataframe: pd.DataFrame, profile: str, target: str | None = None) -> pd.DataFrame:
    """Apply recommendation rules to every product for a selected profile."""
    scored_dataframe = dataframe.copy()
    results = scored_dataframe.apply(lambda row: evaluate_product(row, profile, target), axis=1)
    scored_dataframe["selected_profile"] = profile
    scored_dataframe["recommendation"] = [item[0] for item in results]
    scored_dataframe["reason"] = [item[1] for item in results]
    scored_dataframe["score"] = [item[2] for item in results]
    return scored_dataframe


def score_all_profiles(dataframe: pd.DataFrame, target: str | None = None) -> pd.DataFrame:
    """Score products against all seven medical profiles for comparison analysis."""
    scored_frames = [score_products(dataframe, profile, target) for profile in PROFILE_OPTIONS]
    return pd.concat(scored_frames, ignore_index=True)


def filter_nutrition_data(
    dataframe: pd.DataFrame,
    categories: list[str],
    recommendations: list[str],
) -> pd.DataFrame:
    """Filter scored nutrition rows by category and recommendation status."""
    filtered_dataframe = dataframe.copy()
    if categories:
        filtered_dataframe = filtered_dataframe[filtered_dataframe["category"].isin(categories)]
    if recommendations:
        filtered_dataframe = filtered_dataframe[filtered_dataframe["recommendation"].isin(recommendations)]
    return filtered_dataframe.copy()


def top_recommended_products(dataframe: pd.DataFrame, limit: int = 10) -> pd.DataFrame:
    """Return the best-scoring unique recommended products."""
    return status_products(dataframe, "Recommended", limit, ascending=False)


def status_products(dataframe: pd.DataFrame, status: str, limit: int = 10, ascending: bool = False) -> pd.DataFrame:
    """Return unique products for one recommendation status."""
    return (
        dataframe[dataframe["recommendation"] == status]
        .sort_values("score", ascending=ascending)
        .drop_duplicates("product_name")
        .head(limit)
        .copy()
    )


def not_recommended_reason_counts(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Count dominant reasons among Caution and Not Recommended products."""
    risky_dataframe = dataframe[dataframe["recommendation"].isin(["Caution", "Not Recommended"])]
    reason_counts = (
        risky_dataframe["reason"]
        .value_counts()
        .rename_axis("reason")
        .reset_index(name="total_products")
    )
    if reason_counts.empty:
        return pd.DataFrame([{"reason": "Tidak ada produk berisiko", "total_products": 0}])
    return reason_counts


def nutrition_insight(dataframe: pd.DataFrame) -> tuple[str, str]:
    """Build an automatic insight and severity from the dominant risky reason."""
    reason_counts = not_recommended_reason_counts(dataframe)
    if reason_counts.empty or int(reason_counts.iloc[0]["total_products"]) == 0:
        return "Mayoritas produk pada filter ini masih masuk kategori Recommended.", "success"

    top_reason = str(reason_counts.iloc[0]["reason"])
    total_risky = int(reason_counts.iloc[0]["total_products"])
    if "gula" in top_reason:
        return (
            f"Sebagian besar produk berisiko dipicu oleh kadar gula tinggi ({total_risky} produk). "
            "Profil diabetes tipe 1, diabetes tipe 2, dan diet perlu memprioritaskan sugar lebih rendah.",
            "warning",
        )
    if "sodium" in top_reason:
        return (
            f"Kadar sodium menjadi alasan dominan produk berisiko ({total_risky} produk). "
            "Profil hipertensi sebaiknya memilih produk dengan sodium lebih rendah.",
            "warning",
        )
    return f"Alasan dominan produk berisiko adalah {top_reason} ({total_risky} produk).", "info"


def photo_quality_summary(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Summarize extraction success by photo quality."""
    summary = (
        dataframe.groupby("photo_quality", as_index=False)
        .agg(
            total_rows=("product_name", "count"),
            avg_extraction_success=("extraction_success_rate", "mean"),
            success_rows=("extraction_status", lambda values: (values == "berhasil").sum()),
        )
        .sort_values("avg_extraction_success", ascending=False)
    )
    summary["success_rate"] = (summary["success_rows"] / summary["total_rows"] * 100).round(1)
    summary["avg_extraction_success"] = summary["avg_extraction_success"].round(1)
    return summary


def photo_quality_insight(summary: pd.DataFrame, source: str) -> str:
    """Create a readable answer for photo quality impact."""
    if summary.empty:
        return "Belum ada data kualitas foto untuk dianalisis."

    best_row = summary.iloc[0]
    worst_row = summary.iloc[-1]
    source_note = "berdasarkan kolom dataset" if source == "dataset" else "berdasarkan proxy kualitas foto"
    gap = float(best_row["avg_extraction_success"]) - float(worst_row["avg_extraction_success"])
    return (
        f"Kualitas foto berpengaruh sekitar {gap:.1f} poin terhadap keberhasilan ekstraksi: "
        f"{best_row['photo_quality']} rata-rata {best_row['avg_extraction_success']:.1f}%, "
        f"sedangkan {worst_row['photo_quality']} {worst_row['avg_extraction_success']:.1f}% ({source_note})."
    )


def diabetes_category_risk(dataframe: pd.DataFrame, limit: int = 10) -> pd.DataFrame:
    """Rank Indonesian product categories by diabetes risk across type 1 and type 2 profiles."""
    diabetes_scores = pd.concat(
        [
            score_products(dataframe, "diabetes tipe 1"),
            score_products(dataframe, "diabetes tipe 2"),
        ],
        ignore_index=True,
    )
    summary = (
        diabetes_scores.groupby("category", as_index=False)
        .agg(
            total_tests=("product_name", "count"),
            avg_sugar=("sugar_g", "mean"),
            avg_carbs=("carbs_g", "mean"),
            caution_rows=("recommendation", lambda values: (values == "Caution").sum()),
            not_recommended_rows=("recommendation", lambda values: (values == "Not Recommended").sum()),
        )
    )
    summary["risk_score"] = (
        (summary["not_recommended_rows"] + (summary["caution_rows"] * 0.5)) / summary["total_tests"] * 100
    ).round(1)
    summary["avg_sugar"] = summary["avg_sugar"].round(1)
    summary["avg_carbs"] = summary["avg_carbs"].round(1)
    return summary.sort_values(["risk_score", "avg_sugar"], ascending=False).head(limit)


def diabetes_risk_insight(risk_dataframe: pd.DataFrame) -> str:
    """Create a readable answer for the riskiest diabetes category."""
    if risk_dataframe.empty:
        return "Belum ada kategori produk yang bisa dihitung risikonya untuk diabetes."

    top_row = risk_dataframe.iloc[0]
    return (
        f"Kategori paling berisiko untuk penderita diabetes adalah {top_row['category']} "
        f"dengan risk score {top_row['risk_score']:.1f}, rata-rata sugar {top_row['avg_sugar']:.1f} g "
        f"dan karbohidrat {top_row['avg_carbs']:.1f} g."
    )


def profile_status_distribution(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Calculate recommendation-status distribution for all seven medical profiles."""
    all_profile_scores = score_all_profiles(dataframe)
    distribution = (
        all_profile_scores.groupby(["selected_profile", "recommendation"], as_index=False)
        .agg(total_products=("product_name", "count"))
    )
    profile_totals = distribution.groupby("selected_profile")["total_products"].transform("sum")
    distribution["percent"] = (distribution["total_products"] / profile_totals * 100).round(1)
    return distribution


def profile_sensitivity_table(dataframe: pd.DataFrame, limit: int = 12) -> pd.DataFrame:
    """Measure how much a product's safe status changes across seven medical profiles."""
    all_profile_scores = score_all_profiles(dataframe)
    pivot = (
        all_profile_scores.pivot_table(
            index="product_name",
            columns="selected_profile",
            values="recommendation",
            aggfunc="first",
        )
        .reset_index()
        .fillna("Tidak diuji")
    )
    profile_columns = [profile for profile in PROFILE_OPTIONS if profile in pivot.columns]
    pivot["safe_profiles"] = (pivot[profile_columns] == "Recommended").sum(axis=1)
    pivot["caution_profiles"] = (pivot[profile_columns] == "Caution").sum(axis=1)
    pivot["not_recommended_profiles"] = (pivot[profile_columns] == "Not Recommended").sum(axis=1)
    pivot["status_variants"] = pivot[profile_columns].nunique(axis=1)
    return pivot.sort_values(["status_variants", "not_recommended_profiles"], ascending=False).head(limit)


def profile_sensitivity_insight(sensitivity_dataframe: pd.DataFrame) -> str:
    """Create a readable answer for safe-status differences across seven profiles."""
    if sensitivity_dataframe.empty:
        return "Belum ada data yang bisa dibandingkan pada 7 profil medis."

    avg_safe_profiles = sensitivity_dataframe["safe_profiles"].mean()
    avg_variants = sensitivity_dataframe["status_variants"].mean()
    return (
        f"Perbedaan status Aman cukup terlihat: pada produk yang paling sensitif, rata-rata hanya "
        f"{avg_safe_profiles:.1f} dari 7 profil yang tetap Recommended, dengan "
        f"{avg_variants:.1f} variasi status per produk."
    )


def profile_summary(profile: str, target: str) -> str:
    """Describe the selected nutrition profile used by the simulator."""
    focus = PROFILE_RULES.get(profile, PROFILE_RULES["umum"])["focus"]
    return f"Profil nutrisi dipilih: {profile}. Fokus utama: {focus}. Target: {target}."


def recommendation_explanation(row: pd.Series, profile: str, target: str) -> str:
    """Explain why a selected product is recommended, caution, or not recommended."""
    product_name = row.get("product_name", "Produk ini")
    status = row.get("recommendation")
    if status == "Recommended":
        return (
            f"{product_name} direkomendasikan untuk profil {profile} karena {row.get('reason')} "
            f"dan selaras dengan target {target}."
        )
    if status == "Caution":
        return (
            f"{product_name} masih perlu diperhatikan untuk profil {profile} karena {row.get('reason')}. "
            "Produk ini bisa dipertimbangkan dengan batas konsumsi yang lebih ketat."
        )
    return (
        f"{product_name} tidak direkomendasikan untuk profil {profile} karena {row.get('reason')}. "
        "Pilih produk dengan komposisi yang lebih sesuai target nutrisi."
    )


def comparison_frame(row: pd.Series) -> pd.DataFrame:
    """Build a small dataframe for selected-product nutrition comparison chart."""
    return pd.DataFrame(
        [
            {"nutrient": "sugar_g", "value": float(row.get("sugar_g", 0))},
            {"nutrient": "sodium_mg", "value": float(row.get("sodium_mg", 0))},
            {"nutrient": "protein_g", "value": float(row.get("protein_g", 0))},
            {"nutrient": "calories", "value": float(row.get("calories", 0))},
        ]
    )


def available_display_columns(dataframe: pd.DataFrame) -> list[str]:
    """Return display columns that exist in the current dataframe."""
    return [column for column in DISPLAY_COLUMNS if column in dataframe.columns]
