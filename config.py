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
    'A': 4.0,
    'AB': 3.5,
    'B': 3.0,
    'BC': 2.5,
    'C': 2.0,
    'CD': 1.5,
    'D': 1.0,
    'E': 0.0
}

# Grouping by Program Studi
PROGRAM_STUDI_GROUPING: Dict[str, str] = {
    'Informatika': 'beragam',
    'Teknik Elektro': 'beragam',
    'Sistem Informasi': 'setara'
}

# Grouping Suggestion Fuzzy Mapping
# Maps substring keywords found in the survey to canonical short names.
GROUPING_SUGGESTION_MAPPING: Dict[str, str] = {
    'beragam': 'beragam',
    'setara': 'setara',
    'sendiri': 'mandiri',
    'mandiri': 'mandiri'
}

# Minimum sample size to display without a warning flag
MIN_SAMPLE_SIZE: int = 5
