"""
Dashboard generation module for Survey Analysis.
Handles logic for computing statistics, generating summaries, and building the Plotly HTML dashboard.
"""
import pandas as pd
import plotly.express as px
from typing import Tuple

def compute_statistics(df: pd.DataFrame, config_module) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Compute average TA1 Score, Satisfaction, and grade counts per canonical group."""
    # Average TA1 Score
    avg_score = df.groupby('canonical_group')['TA1_Score'].agg(['mean', 'count']).reset_index()
    avg_score = avg_score.rename(columns={'mean': 'Average_TA1_Score', 'count': 'Sample_Size'})
    
    # Average Satisfaction
    avg_satisfaction = df.groupby('canonical_group')['Satisfaction_Score'].mean().reset_index(name='Average_Satisfaction')
    avg_score = avg_score.merge(avg_satisfaction, on='canonical_group', how='left')
    
    # Grade Counts
    grade_cols = [col for col in df.columns if 'grade' in col.lower()]
    grade_col = grade_cols[0]
    
    grade_counts = df.groupby(['canonical_group', grade_col]).size().reset_index(name='Count')
    
    return avg_score, grade_counts

def generate_summary_text(avg_score: pd.DataFrame) -> str:
    """Generate a plain-language summary of the statistics in Indonesian."""
    if avg_score.empty:
        return "Tidak ada data untuk dirangkum."
        
    # Find highest Score
    best_group_row = avg_score.loc[avg_score['Average_TA1_Score'].idxmax()]
    best_group = best_group_row['canonical_group']
    best_score = best_group_row['Average_TA1_Score']
    best_count = best_group_row['Sample_Size']
    
    summary = (
        f"Berdasarkan data yang dianalisis, kelompok dengan strategi <strong>{best_group}</strong> "
        f"memiliki rata-rata Nilai Tugas Akhir I tertinggi yaitu <strong>{best_score:.2f}</strong> "
        f"(ukuran sampel: {best_count} mahasiswa)."
    )
    return summary

def generate_dashboard(df: pd.DataFrame, config_module) -> None:
    """Generate the static HTML dashboard using Plotly."""
    avg_score, grade_counts = compute_statistics(df, config_module)
    summary_text = generate_summary_text(avg_score)
    
    # Flag groups with small sample size
    min_sample = config_module.MIN_SAMPLE_SIZE
    avg_score['Display_Name'] = avg_score.apply(
        lambda row: f"{row['canonical_group']} *" if row['Sample_Size'] < min_sample else row['canonical_group'],
        axis=1
    )
    
    # Map back to grade_counts
    grade_counts = grade_counts.merge(avg_score[['canonical_group', 'Display_Name']], on='canonical_group', how='left')
    
    # Common layout settings
    layout_settings = dict(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        font=dict(family="Inter, system-ui, sans-serif"),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    # Chart 1: Bar chart for Average TA1 Score
    fig1 = px.bar(
        avg_score, 
        x='Display_Name', 
        y='Average_TA1_Score', 
        text='Average_TA1_Score',
        color='Display_Name',
        title="Rata-rata Nilai TA I per Strategi",
        labels={'Display_Name': 'Strategi Pengelompokan', 'Average_TA1_Score': 'Rata-rata Nilai TA I'}
    )
    fig1.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig1.update_layout(**layout_settings)
    
    # Chart 4: Bar chart for Average Satisfaction
    fig4 = px.bar(
        avg_score, 
        x='Display_Name', 
        y='Average_Satisfaction', 
        text='Average_Satisfaction',
        color='Display_Name',
        title="Rata-rata Kepuasan (Skala 1-5)",
        labels={'Display_Name': 'Strategi Pengelompokan', 'Average_Satisfaction': 'Tingkat Kepuasan'}
    )
    fig4.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig4.update_layout(**layout_settings)
    
    # Chart 2: Stacked Bar Chart for Grade Distribution
    grade_col = [col for col in df.columns if 'grade' in col.lower()][0]
    fig2 = px.bar(
        grade_counts, 
        x='Display_Name', 
        y='Count', 
        color=grade_col,
        title="Distribusi Nilai TA I",
        labels={'Display_Name': 'Strategi Pengelompokan', 'Count': 'Jumlah Mahasiswa'},
        barmode='stack',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig2.update_layout(**layout_settings)
    
    # Chart 3: Pie Chart for Student Suggestions
    suggestion_counts = df['suggestion_category'].value_counts().reset_index()
    suggestion_counts.columns = ['Suggestion', 'Count']
    fig3 = px.pie(
        suggestion_counts, 
        names='Suggestion', 
        values='Count',
        title="Saran Mahasiswa Kedepannya",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig3.update_layout(**layout_settings)
    
    # Build HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard Analisis Survei</title>
        <style>
            :root {{
                --primary: #4F46E5;
                --background: #F9FAFB;
                --surface: #FFFFFF;
                --text-main: #111827;
                --text-muted: #6B7280;
                --border-radius: 12px;
                --spacing-xs: 8px;
                --spacing-sm: 16px;
                --spacing-md: 24px;
            }}

            @media (prefers-color-scheme: dark) {{
                :root {{
                    --background: #111827;
                    --surface: #1F2937;
                    --text-main: #F9FAFB;
                    --text-muted: #9CA3AF;
                }}
            }}

            body {{
                font-family: 'Inter', system-ui, sans-serif;
                background-color: var(--background);
                color: var(--text-main);
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }}

            .dashboard-wrapper {{
                width: 100%;
                max-width: 1920px;
                height: 100vh;
                max-height: 1080px;
                aspect-ratio: 16/9;
                padding: var(--spacing-md);
                box-sizing: border-box;
                display: flex;
                flex-direction: column;
                gap: var(--spacing-md);
            }}

            @media (max-width: 1920px) or (max-height: 1080px) {{
                .dashboard-wrapper {{
                    height: auto;
                    max-height: none;
                    aspect-ratio: auto;
                    min-height: 100vh;
                }}
            }}

            h1, h2, h3 {{ color: var(--text-main); font-weight: 600; margin-top: 0; }}
            h1 {{ margin-bottom: 4px; }}
            
            .header-text {{ margin-top: 0; color: var(--text-muted); }}

            .card {{
                background-color: var(--surface);
                border-radius: var(--border-radius);
                padding: var(--spacing-md);
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                display: flex;
                flex-direction: column;
                justify-content: center;
            }}

            .kpi-card {{
                background-color: var(--primary);
                color: #FFFFFF;
                border-radius: var(--border-radius);
                padding: var(--spacing-md);
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }}

            .kpi-card h2 {{ color: #FFFFFF; margin-bottom: 8px; }}
            .kpi-card p {{ margin: 0; font-size: 1.1rem; }}
            .kpi-card strong {{ color: #FFFFFF; }}

            .charts-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: var(--spacing-md);
                flex: 1;
                min-height: 0; /* Important for flex child with overflow */
            }}

            @media (max-width: 1024px) {{
                .charts-grid {{
                    grid-template-columns: 1fr;
                }}
            }}
            
            .chart-container {{
                height: 100%;
                min-height: 300px; /* Minimum height for responsive fallback */
                position: relative;
            }}

            .footnote {{
                font-size: 0.875rem;
                color: var(--text-muted);
                margin-top: var(--spacing-sm);
            }}
        </style>
    </head>
    <body>
        <div class="dashboard-wrapper">
            <div class="header">
                <h1>Analisis Pengelompokan Tugas Akhir Mahasiswa</h1>
                <p class="header-text">Dashboard Kinerja Berdasarkan Strategi Pengelompokan Tugas Akhir I</p>
            </div>
            
            <div class="kpi-card">
                <h2>Temuan Utama</h2>
                <p>{summary_text}</p>
            </div>
            
            <div class="charts-grid">
                <div class="card">
                    <div class="chart-container">
                        {fig1.to_html(full_html=False, include_plotlyjs='cdn')}
                    </div>
                </div>
                <div class="card">
                    <div class="chart-container">
                        {fig4.to_html(full_html=False, include_plotlyjs=False)}
                    </div>
                </div>
                <div class="card">
                    <div class="chart-container">
                        {fig2.to_html(full_html=False, include_plotlyjs=False)}
                    </div>
                </div>
                <div class="card">
                    <div class="chart-container">
                        {fig3.to_html(full_html=False, include_plotlyjs=False)}
                    </div>
                    <div class="footnote">
                        * Menandakan kategori dengan responden kurang dari {min_sample}.
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    output_path = config_module.OUTPUT_HTML_PATH
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print(f"\n[SUCCESS] Dashboard successfully generated and saved to {output_path}")
