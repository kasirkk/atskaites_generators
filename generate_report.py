
# Importi 
import pandas as pd
import os

# Datu apstrāde un izņēmumi
def apkopot_sportistu_datus(failu_celi):
    nevēlamie_veidi = [
        'strength', 'other', 'strength training', 'pilates', 'yoga', 'training', 'meditation'
    ]
    rezultati = {}
    overall_min = None
    overall_max = None
    for fails in failu_celi:
        vards = os.path.splitext(os.path.basename(fails))[0]
        df = pd.read_csv(fails)
        # Parse dates and update overall range
        if 'WorkoutDay' in df.columns:
            try:
                dts = pd.to_datetime(df['WorkoutDay'], errors='coerce')
                file_min = dts.min()
                file_max = dts.max()
                if pd.notna(file_min):
                    overall_min = file_min if overall_min is None else min(overall_min, file_min)
                if pd.notna(file_max):
                    overall_max = file_max if overall_max is None else max(overall_max, file_max)
            except Exception:
                pass
        # Sessions count excludes unwanted workout types
        df_filt = df[~df['WorkoutType'].str.lower().isin(nevēlamie_veidi)]
        sessions = len(df_filt)
        # Minutes are counted across ALL sessions (including those excluded from session count)
        zona2_all = pd.to_numeric(df['HRZone2Minutes'], errors='coerce').fillna(0).sum()
        zona3_all = pd.to_numeric(df['HRZone3Minutes'], errors='coerce').fillna(0).sum()
        minutes = zona2_all * 1 + zona3_all * 2
        rezultati[vards] = {
            'minutes': int(minutes),
            'sessions': int(sessions)
        }
    # Format date range string if available
    if overall_min is not None and overall_max is not None:
        date_range_str = f"{overall_min.strftime('%d.%m.%Y')} - {overall_max.strftime('%d.%m.%Y')}"
    else:
        date_range_str = None
    return rezultati, date_range_str

# --- Grafika ģenerēšana ---
def genereet_kopsavilkuma_grafiku(rezultati, izvada_fails='kopsavilkums.html', datumu_range=None):
    import plotly.graph_objects as go
    import plotly.io as pio
    vardi = list(rezultati.keys())
    minutes = [rezultati[v]['minutes'] for v in vardi]
    sessions = [rezultati[v].get('sessions', 0) for v in vardi]
    sakartots = sorted(zip(vardi, minutes, sessions), key=lambda x: x[1])
    vardi, minutes, sessions = zip(*sakartots)
    limeni = [0, 150, 300, 1000]
    limenu_nosaukumi = [
        'Enerģijas ražotājs',
        'Labsajūtas meistars',
        'Metabolisma Inženieris',
        'Izturības Arhitekts',
        'Kaizen Leģenda'
    ]
    limenu_krasa = 'rgba(46, 204, 113, 0.15)'
    fig = go.Figure()
    for i in range(len(limeni)-1):
        fig.add_shape(
            type="rect",
            xref="paper", yref="y",
            x0=0, x1=1,
            y0=limeni[i], y1=limeni[i+1],
            fillcolor=limenu_krasa, line_width=0, layer="below"
        )
    fig.add_trace(go.Bar(
        x=vardi,
        y=minutes,
        marker_color='black',
        text=minutes,
        textposition='outside',
        textfont=dict(size=12, color='black'),
        name='Minūtes zonās',
        hovertemplate='<b>%{x}</b><br>Minūtes: %{y}<br>Sesijas: %{customdata}',
        customdata=sessions
    ))
    # Sessions displayed inside bar as white text
    for xv, ym, sc in zip(vardi, minutes, sessions):
        fig.add_annotation(
            x=xv, y=(ym * 0.5) if ym > 4 else (ym + 2),
            text=str(sc),
            showarrow=False,
            font=dict(size=10, color='white')
        )
    for y in [150, 300]:
        fig.add_shape(
            type="line",
            xref="paper", yref="y",
            x0=0, x1=1,
            y0=y, y1=y,
            line=dict(color="green", width=3),
            layer="below"
        )
    # Pozīcijas līmeņu nosaukumiem (ārpus grafika kreisajā pusē)
    max_y_val = max(350, max(minutes) + 50)
    # remove fixed pixel width; let plotly resize automatically
    # note: left margin will be adjusted below
    fig.update_layout(
        height=600,
        autosize=True,
        margin=dict(l=120, r=40, t=90, b=180),
    )
    # izvairīsimies no cietām vērtībām — izmantojam procentus no augstuma
    y_positions = [max_y_val * 0.03, max_y_val * 0.2, max_y_val * 0.45, max_y_val * 0.7, max_y_val * 0.95]
    for i, nosaukums in enumerate(limenu_nosaukumi):
        fig.add_annotation(
            xref="paper", yref="y",
            x=-0.01, y=y_positions[i],
            text=nosaukums,
            showarrow=False,
            font=dict(size=14, color="#2d3436"),
            align="right",
            xanchor="right"
        )
    if datumu_range:
        title = f"Active For Life ({datumu_range})"
    else:
        title = "Active For Life"
    # general layout settings, autosize allows full width
    fig.update_layout(
        title=title,
        title_x=0.02,
        font=dict(family='Segoe UI, Tahoma, Arial', size=12, color='#2d3436'),
        xaxis_title=None,
        yaxis_title=None,
        yaxis=dict(range=[0, max(350, max(minutes)+50)], gridcolor='rgba(0,0,0,0.06)'),
        bargap=0.15,
        plot_bgcolor='white',
        margin=dict(l=180, r=40, t=90, b=180),
        height=600,
        autosize=True
    )
    fig.update_xaxes(tickangle=30, tickfont=dict(size=10), automargin=True, domain=[0,1])
    fig.update_yaxes(automargin=True)
    pio.write_html(fig, file=izvada_fails, auto_open=False)
    return izvada_fails

# --- GUI ---
def palaist_gui():
    import tkinter as tk
    from tkinter import filedialog, messagebox
    import webbrowser

    def izveleties_failus():
        faili = filedialog.askopenfilenames(
            title="Izvēlieties sportistu CSV failus",
            filetypes=[("CSV faili", "*.csv")]
        )
        if faili:
            failu_ievades_var.set("; ".join(faili))
            pogas_generet.config(state=tk.NORMAL)
        else:
            pogas_generet.config(state=tk.DISABLED)

    def generet_atskaiti():
        failu_celi = failu_ievades_var.get().split('; ')
        if not failu_celi or not failu_celi[0]:
            messagebox.showerror("Kļūda", "Nav izvēlēti faili!")
            return
        # ask where to save the report
        save_path = filedialog.asksaveasfilename(
            title="Saglabāt atskaiti kā",
            defaultextension=".html",
            filetypes=[("HTML faili", "*.html")],
            initialfile="kopsavilkums.html"
        )
        if not save_path:
            return
        try:
            rezultati, datumu_range = apkopot_sportistu_datus(failu_celi)
            izvada_fails = genereet_kopsavilkuma_grafiku(rezultati, izvada_fails=save_path, datumu_range=datumu_range)
            messagebox.showinfo("Gatavs!", f"Atskaites fails saglabāts: {izvada_fails}")
            if messagebox.askyesno("Atvērt?", "Vai vēlaties atvērt atskaiti pārlūkā?"):
                webbrowser.open(izvada_fails)
        except Exception as e:
            messagebox.showerror("Kļūda", f"Radās kļūda: {e}")

    sakne = tk.Tk()
    sakne.title("Sportistu kopsavilkuma ģenerators")
    sakne.geometry("600x200")

    failu_ievades_var = tk.StringVar()

    tk.Label(sakne, text="Izvēlieties sportistu CSV failus:", font=("Arial", 12)).pack(pady=10)
    tk.Entry(sakne, textvariable=failu_ievades_var, width=70, state='readonly').pack(pady=5)
    tk.Button(sakne, text="Izvēlēties failus", command=izveleties_failus).pack(pady=5)
    pogas_generet = tk.Button(sakne, text="Ģenerēt kopsavilkuma atskaiti", command=generet_atskaiti, state=tk.DISABLED)
    pogas_generet.pack(pady=15)

    sakne.mainloop()

# --- Starta punkts ---
if __name__ == "__main__":
    palaist_gui()
    
    def generate_charts(self):
        """Generate interactive charts using Plotly."""
        charts_html = ""
        
        # Chart 1: Sleep Hours Trend
        if 'Sleep Hours' in self.metrics_pivot.columns:
            sleep_data = self.metrics_pivot[['Timestamp', 'Sleep Hours']].copy()
            sleep_data['Sleep Hours'] = pd.to_numeric(sleep_data['Sleep Hours'], errors='coerce')
            
            fig_sleep = go.Figure()
            fig_sleep.add_trace(go.Scatter(
                x=sleep_data['Timestamp'],
                y=sleep_data['Sleep Hours'],
                mode='lines+markers',
                name='Miega stundas',
                line=dict(color='#3498db', width=3),
                marker=dict(size=8),
                fill='tozeroy',
                fillcolor='rgba(52, 152, 219, 0.2)'
            ))
            
            fig_sleep.add_hline(
                y=sleep_data['Sleep Hours'].mean(),
                line_dash="dash",
                line_color="red",
                annotation_text=f"Vidēji: {sleep_data['Sleep Hours'].mean():.2f}h"
            )
            
            fig_sleep.update_layout(
                title='Miega Ilgums Laika Gaitā',
                xaxis_title='Datums',
                yaxis_title='Stundas',
                hovermode='x unified',
                template='plotly_white',
                height=400
            )
            
            charts_html += f'<div class="chart-container">{fig_sleep.to_html(include_plotlyjs=False, div_id="sleep_chart")}</div>'
        
        
        # Chart 4: Workout Duration by Type
        if len(self.workouts_df) > 0:
            workout_summary = self.workouts_df.groupby('WorkoutType')['TimeTotalInHours'].sum().reset_index()
            
            fig_workouts = go.Figure(data=[go.Bar(
                x=workout_summary['WorkoutType'],
                y=workout_summary['TimeTotalInHours'],
                marker=dict(color='#e67e22'),
                text=workout_summary['TimeTotalInHours'].round(2),
                textposition='auto'
            )])
            
            fig_workouts.update_layout(
                title='Kopējais Treniņu Ilgums pēc Veida',
                xaxis_title='Treniņa Veids',
                yaxis_title='Stundas',
                template='plotly_white',
                height=400
            )
            
            charts_html += f'<div class="chart-container">{fig_workouts.to_html(include_plotlyjs=False, div_id="workout_chart")}</div>'
        
       


def main():
    """Main function to run the report generator with GUI."""
    root = tk.Tk()
    app = ReportGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
