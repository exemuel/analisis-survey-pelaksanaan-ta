"""
Data processing module for Survey Analysis.
Handles loading, validation, cleaning, and merging of data.
"""
import pandas as pd
import numpy as np
from typing import Tuple, Dict

def load_data(survey_path: str, grades_path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load data from Excel files and log raw columns."""
    try:
        survey_df = pd.read_excel(survey_path)
    except Exception as e:
        raise RuntimeError(f"Failed to load survey data from {survey_path}: {e}")

    try:
        grades_df = pd.read_excel(grades_path)
    except Exception as e:
        raise RuntimeError(f"Failed to load grades data from {grades_path}: {e}")

    print("--- Loaded Survey Data ---")
    print(f"File: {survey_path}")
    print(f"Raw Columns: {survey_df.columns.tolist()}")
    print(f"Rows: {len(survey_df)}")

    print("\n--- Loaded Grades Data ---")
    print(f"File: {grades_path}")
    print(f"Raw Columns: {grades_df.columns.tolist()}")
    print(f"Rows: {len(grades_df)}")

    return survey_df, grades_df

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Strip whitespace from column names."""
    df.columns = df.columns.str.strip()
    return df

def validate_and_deduplicate(survey_df: pd.DataFrame, grades_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Validate presence of NIM and remove duplicates."""
    if 'NIM' not in survey_df.columns:
        raise ValueError(f"Column 'NIM' not found in survey.xlsx. Available columns: {survey_df.columns.tolist()}")
    if 'NIM' not in grades_df.columns:
        raise ValueError(f"Column 'NIM' not found in nilai-tugas-akhir-mahasiswa.xlsx. Available columns: {grades_df.columns.tolist()}")

    # Deduplicate survey
    survey_dups = survey_df.duplicated(subset=['NIM'], keep=False)
    if survey_dups.any():
        num_dups = survey_dups.sum()
        print(f"\n[WARNING] Found {num_dups} duplicate NIMs in survey data. Keeping the first occurrence.")
        survey_df = survey_df.drop_duplicates(subset=['NIM'], keep='first')

    # Deduplicate grades
    grades_dups = grades_df.duplicated(subset=['NIM'], keep=False)
    if grades_dups.any():
        num_dups = grades_dups.sum()
        print(f"[WARNING] Found {num_dups} duplicate NIMs in grades data. Keeping the first occurrence.")
        grades_df = grades_df.drop_duplicates(subset=['NIM'], keep='first')

    return survey_df, grades_df

def assign_grouping_by_prodi(df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
    """Assign canonical group based on Program Studi."""
    def map_prodi(val):
        if pd.isna(val):
            return "lainnya"
        val_str = str(val).strip()
        return mapping.get(val_str, "lainnya")

    df['canonical_group'] = df['Program Studi'].apply(map_prodi)
    return df

def normalize_grouping_suggestions(df: pd.DataFrame, suggestion_col: str, mapping: Dict[str, str]) -> pd.DataFrame:
    """Apply fuzzy mapping to canonicalize grouping suggestions."""
    def map_suggestion(val):
        if pd.isna(val):
            return np.nan
        val_lower = str(val).lower().strip()
        for key, canonical in mapping.items():
            if key in val_lower:
                return canonical
        return "lainnya"

    df['suggestion_category'] = df[suggestion_col].apply(map_suggestion)
    return df

def map_grades(df: pd.DataFrame, grade_col: str, mapping: Dict[str, float]) -> pd.DataFrame:
    """Map categorical grades to numeric TA1_Score, setting unrecognized to NaN."""
    def map_grade(val):
        if pd.isna(val):
            return np.nan
        val_str = str(val).strip().upper()
        return mapping.get(val_str, np.nan)

    df['TA1_Score'] = df[grade_col].apply(map_grade)
    
    unrecognized = df['TA1_Score'].isna().sum()
    if unrecognized > 0:
        print(f"[WARNING] Found {unrecognized} unmapped or missing grades. They have been set to NaN.")
        
    return df

def process_data(survey_path: str, grades_path: str, config_module) -> pd.DataFrame:
    """Main pipeline for data processing."""
    survey_df, grades_df = load_data(survey_path, grades_path)

    survey_df = clean_column_names(survey_df)
    grades_df = clean_column_names(grades_df)

    survey_df, grades_df = validate_and_deduplicate(survey_df, grades_df)

    if 'Program Studi' not in survey_df.columns:
        raise ValueError(f"Could not find 'Program Studi' in survey data. Columns: {survey_df.columns.tolist()}")

    # Identify the satisfaction column
    puas_cols = [col for col in survey_df.columns if 'puas' in col.lower()]
    if not puas_cols:
        raise ValueError(f"Could not find satisfaction column. Columns: {survey_df.columns.tolist()}")
    survey_df = survey_df.rename(columns={puas_cols[0]: 'Satisfaction_Score'})

    # Identify the suggestion column (we look for a column containing "saran")
    saran_cols = [col for col in survey_df.columns if 'saran' in col.lower()]
    if not saran_cols:
        raise ValueError(f"Could not find a column containing 'saran' in survey data. Columns: {survey_df.columns.tolist()}")
    saran_col = saran_cols[0]

    # Identify the grade column (we look for 'Grade Tugas Akhir I')
    grade_cols = [col for col in grades_df.columns if 'grade' in col.lower()]
    if not grade_cols:
        raise ValueError(f"Could not find a column containing 'grade' in grades data. Columns: {grades_df.columns.tolist()}")
    grade_col = grade_cols[0]

    survey_df = assign_grouping_by_prodi(survey_df, config_module.PROGRAM_STUDI_GROUPING)
    survey_df = normalize_grouping_suggestions(survey_df, saran_col, config_module.GROUPING_SUGGESTION_MAPPING)
    grades_df = map_grades(grades_df, grade_col, config_module.GRADE_MAPPING)

    # Merge
    print(f"\n--- Merging Data ---")
    merged_df = pd.merge(survey_df, grades_df, on='NIM', how='inner')
    
    survey_lost = len(survey_df) - len(merged_df)
    grades_lost = len(grades_df) - len(merged_df)
    
    print(f"Merged dataframe has {len(merged_df)} rows.")
    print(f"Rows dropped from survey data: {survey_lost}")
    print(f"Rows dropped from grades data: {grades_lost}")

    # Handle NaNs in TA1_Score before analysis
    nan_score_count = merged_df['TA1_Score'].isna().sum()
    if nan_score_count > 0:
        print(f"[WARNING] Dropping {nan_score_count} rows from the merged dataset due to missing or unrecognized TA1_Score.")
        merged_df = merged_df.dropna(subset=['TA1_Score'])
        print(f"Final dataset size for analysis: {len(merged_df)} rows.")
        
    return merged_df
