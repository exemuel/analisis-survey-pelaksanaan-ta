import pandas as pd
import numpy as np
import pytest
from data_processing import clean_column_names, validate_and_deduplicate, normalize_grouping_suggestions, map_grades

def test_clean_column_names():
    df = pd.DataFrame({' NIM ': [1, 2], 'Nama ': ['A', 'B']})
    df_clean = clean_column_names(df)
    assert list(df_clean.columns) == ['NIM', 'Nama']

def test_validate_and_deduplicate():
    survey_df = pd.DataFrame({'NIM': [1, 2, 2], 'Val': ['A', 'B', 'C']})
    grades_df = pd.DataFrame({'NIM': [1, 1, 2], 'Grade': ['A', 'A', 'B']})
    
    s_out, g_out = validate_and_deduplicate(survey_df, grades_df)
    
    assert len(s_out) == 2
    assert len(g_out) == 2
    assert s_out['NIM'].tolist() == [1, 2]
    assert s_out['Val'].tolist() == ['A', 'B']

def test_normalize_grouping_suggestions():
    df = pd.DataFrame({'saran': ['saya mau beragam', 'SETARA dong', 'pilih sendiri aja', 'bebas']})
    mapping = {'beragam': 'beragam', 'setara': 'setara', 'sendiri': 'mandiri'}
    
    df_out = normalize_grouping_suggestions(df, 'saran', mapping)
    
    expected = ['beragam', 'setara', 'mandiri', 'lainnya']
    assert df_out['canonical_group'].tolist() == expected

def test_map_grades():
    df = pd.DataFrame({'Grade Tugas Akhir I': ['A', ' AB ', 'C', 'Z', np.nan]})
    mapping = {'A': 4.0, 'AB': 3.5, 'C': 2.0}
    
    df_out = map_grades(df, 'Grade Tugas Akhir I', mapping)
    
    gpas = df_out['GPA'].tolist()
    assert gpas[0] == 4.0
    assert gpas[1] == 3.5
    assert gpas[2] == 2.0
    assert np.isnan(gpas[3])
    assert np.isnan(gpas[4])
