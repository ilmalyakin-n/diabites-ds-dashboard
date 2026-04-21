import pandas as pd


def first_existing(columns: pd.Index, candidates: list[str]) -> str | None:
    """Find the first matching column name from a list of possible aliases."""
    normalized_columns = {column.lower(): column for column in columns}
    for candidate in candidates:
        if candidate.lower() in normalized_columns:
            return normalized_columns[candidate.lower()]
    return None


def count_user_profiles(dataframe: pd.DataFrame) -> int:
    """Count unique user profile combinations from the available nutrition columns."""
    if "user_profile" in dataframe.columns:
        return int(dataframe["user_profile"].nunique())

    profile_columns = [
        column
        for column in ["age_group", "bmi_category", "diabetes_type"]
        if column in dataframe.columns
    ]
    if not profile_columns:
        return 0
    return int(dataframe[profile_columns].drop_duplicates().shape[0])


def value_counts_frame(dataframe: pd.DataFrame, column: str, count_name: str = "total") -> pd.DataFrame:
    """Build a dataframe from value counts so chart helpers receive consistent input."""
    if column not in dataframe.columns or dataframe.empty:
        return pd.DataFrame(columns=[column, count_name])

    return (
        dataframe[column]
        .fillna("tidak diketahui")
        .astype(str)
        .value_counts()
        .rename_axis(column)
        .reset_index(name=count_name)
    )


def numeric_columns(dataframe: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Coerce selected columns to numeric values without mutating the original dataframe."""
    cleaned_dataframe = dataframe.copy()
    for column in columns:
        if column in cleaned_dataframe.columns:
            cleaned_dataframe[column] = pd.to_numeric(cleaned_dataframe[column], errors="coerce").fillna(0)
    return cleaned_dataframe
