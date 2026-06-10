import pandas as pd
survey_path = "f:/SGS/samuel/proyek/analisis-survey-pelaksanaan-ta/data/survey.xlsx"
df1 = pd.read_excel(survey_path)
col = [c for c in df1.columns if 'puas' in c.lower()][0]
print("Satisfaction column:", col)
print("Unique values:", df1[col].unique().tolist())
