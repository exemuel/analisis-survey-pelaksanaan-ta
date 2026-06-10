import pandas as pd
from dashboard_generator import compute_statistics, generate_summary_text

class DummyConfig:
    MIN_SAMPLE_SIZE = 2

def test_compute_statistics():
    df = pd.DataFrame({
        'canonical_group': ['beragam', 'beragam', 'setara', 'setara', 'setara'],
        'Grade Tugas Akhir I': ['A', 'B', 'A', 'A', 'B'],
        'GPA': [4.0, 3.0, 4.0, 4.0, 3.0]
    })
    config = DummyConfig()
    
    avg_gpa, grade_counts = compute_statistics(df, config)
    
    assert len(avg_gpa) == 2
    beragam_row = avg_gpa[avg_gpa['canonical_group'] == 'beragam'].iloc[0]
    assert beragam_row['Average_GPA'] == 3.5
    assert beragam_row['Sample_Size'] == 2
    
    setara_row = avg_gpa[avg_gpa['canonical_group'] == 'setara'].iloc[0]
    assert round(setara_row['Average_GPA'], 2) == 3.67
    assert setara_row['Sample_Size'] == 3

def test_generate_summary_text():
    avg_gpa = pd.DataFrame({
        'canonical_group': ['beragam', 'setara'],
        'Average_GPA': [3.5, 3.8],
        'Sample_Size': [2, 3]
    })
    
    text = generate_summary_text(avg_gpa)
    assert 'setara' in text
    assert '3.80' in text
    assert 'beragam' not in text
