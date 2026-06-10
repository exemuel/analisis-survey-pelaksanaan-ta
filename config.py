"""
Configuration settings for the Survey Analysis project.
"""
from typing import Dict

# File Paths
SURVEY_FILE_PATH: str = 'data/survey.xlsx'
GRADES_FILE_PATH: str = 'data/nilai-tugas-akhir-mahasiswa.xlsx'
OUTPUT_HTML_PATH: str = 'dashboard.html'

# Grade Mappings
# Maps standard categorical grades to numerical TA1 Score
GRADE_MAPPING: Dict[str, float] = {
    'A': 79.5,
    'AB': 72.0,
    'B': 64.5,
    'BC': 57.0,
    'C': 49.5,
    'D': 34.0,
    'E': 0.0
}

# Grouping by Program Studi
PROGRAM_STUDI_GROUPING: Dict[str, str] = {
    'Informatika': 'dikelompokkan beragam',
    'Teknik Elektro': 'dikelompokkan beragam',
    'Sistem Informasi': 'dikelompokkan setara'
}

# Grouping Suggestion Fuzzy Mapping
# Maps substring keywords found in the survey to canonical short names.
GROUPING_SUGGESTION_MAPPING: Dict[str, str] = {
    'beragam': 'dikelompokkan beragam',
    'setara': 'dikelompokkan setara',
    'sendiri': 'mandiri membuat kelompok',
    'mandiri': 'mandiri membuat kelompok'
}

# Minimum sample size to display without a warning flag
MIN_SAMPLE_SIZE: int = 5
