# Analisis Pengelompokan Tugas Akhir Mahasiswa

This program analyzes the relationship between students' preferences for final project grouping and their grades.

## Expected Data Schema

To run this tool successfully, the input Excel files must adhere to the following schemas.

### 1. Survey Data (`survey.xlsx`)
- **Required Columns**:
  - `'NIM '` or `'NIM'`: The unique identifier for the student.
  - `'Apa saran anda tentang pengelompokan tugas akhir di masa yang akan datang?'`: The grouping preference column.
- **Expected Data**:
  - The grouping suggestion column must contain text that fuzzy-matches predefined canonical keys (e.g., `"beragam"`, `"setara"`, `"sendiri"` / `"mandiri"`).

### 2. Grades Data (`nilai-tugas-akhir-mahasiswa.xlsx`)
- **Required Columns**:
  - `'NIM'`: The unique identifier for the student.
  - `'Grade Tugas Akhir I'`: The student's grade.
- **Expected Data**:
  - The grades should be standard categorical Indonesian GPA grades: `A`, `AB`, `B`, `BC`, `C`, `CD`, `D`, `E`.
  - Unrecognized or empty grades will be mapped to `NaN` and dropped from the average calculations.
