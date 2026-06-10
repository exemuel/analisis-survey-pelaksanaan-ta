import pandas as pd
survey_path = "f:/SGS/samuel/proyek/analisis-survey-pelaksanaan-ta/data/survey.xlsx"
df1 = pd.read_excel(survey_path)
print(df1['Program Studi'].unique().tolist())
