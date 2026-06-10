import pandas as pd

survey_path = "f:/SGS/samuel/proyek/analisis-survey-pelaksanaan-ta/data/survey.xlsx"
grades_path = "f:/SGS/samuel/proyek/analisis-survey-pelaksanaan-ta/data/nilai-tugas-akhir-mahasiswa.xlsx"

print("Survey Columns:")
try:
    df1 = pd.read_excel(survey_path)
    print(df1.columns.tolist())
    print(df1.head(2))
except Exception as e:
    print(e)

print("\nGrades Columns:")
try:
    df2 = pd.read_excel(grades_path)
    print(df2.columns.tolist())
    print(df2.head(2))
except Exception as e:
    print(e)
