import pandas as pd
import numpy as np
from datetime import datetime
import os

class WorkoutReportGenerator:
    def __init__(self, metrics_file, workouts_file):
        """Initialize the report generator with CSV files."""
        self.metrics_df = pd.read_csv(metrics_file)
        self.workouts_df = pd.read_csv(workouts_file)
        self.process_data()
    
    def process_data(self):
        """Process and clean the data."""
        # Convert timestamps to datetime
        self.metrics_df['Timestamp'] = pd.to_datetime(self.metrics_df['Timestamp'])
        self.workouts_df['WorkoutDay'] = pd.to_datetime(self.workouts_df['WorkoutDay'])
        
        # Pivot metrics to have one row per date
        self.metrics_pivot = self.metrics_df.pivot(
            index='Timestamp', 
            columns='Type', 
            values='Value'
        ).reset_index()
    
    def calculate_statistics(self):
        """Calculate key statistics from the data."""
        stats = {}
        
        # Metrics statistics
        if 'Sleep Hours' in self.metrics_pivot.columns:
            stats['avg_sleep'] = pd.to_numeric(self.metrics_pivot['Sleep Hours'], errors='coerce').mean()
            stats['min_sleep'] = pd.to_numeric(self.metrics_pivot['Sleep Hours'], errors='coerce').min()
            stats['max_sleep'] = pd.to_numeric(self.metrics_pivot['Sleep Hours'], errors='coerce').max()
        
        if 'HRV' in self.metrics_pivot.columns:
            stats['avg_hrv'] = pd.to_numeric(self.metrics_pivot['HRV'], errors='coerce').mean()
            stats['min_hrv'] = pd.to_numeric(self.metrics_pivot['HRV'], errors='coerce').min()
            stats['max_hrv'] = pd.to_numeric(self.metrics_pivot['HRV'], errors='coerce').max()
        
        if 'Pulse' in self.metrics_pivot.columns:
            stats['avg_pulse'] = pd.to_numeric(self.metrics_pivot['Pulse'], errors='coerce').mean()
        
        # Workout statistics
        stats['total_workouts'] = len(self.workouts_df)
        stats['total_duration_hours'] = self.workouts_df['TimeTotalInHours'].sum()
        
        workout_types = self.workouts_df['WorkoutType'].value_counts()
        stats['workout_types'] = workout_types.to_dict()
        
        if 'HeartRateAverage' in self.workouts_df.columns:
            stats['avg_hr_workout'] = self.workouts_df['HeartRateAverage'].mean()
            stats['max_hr_workout'] = self.workouts_df['HeartRateMax'].max()
        
        return stats
    
    def generate_html_report(self, output_file='report.html'):
        """Generate HTML report."""
        stats = self.calculate_statistics()
        
        html_content = f"""<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta charset="utf-8">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Training & Wellness Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 3px solid #3498db;
            padding-bottom: 15px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-left: 4px solid #3498db;
            padding-left: 15px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .stat-card.green {{
            background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
        }}
        .stat-card.blue {{
            background: linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%);
        }}
        .stat-card.orange {{
            background: linear-gradient(135deg, #f46b45 0%, #eea849 100%);
        }}
        .stat-label {{
            font-size: 14px;
            opacity: 0.9;
            margin-bottom: 5px;
        }}
        .stat-value {{
            font-size: 32px;
            font-weight: bold;
        }}
        .stat-unit {{
            font-size: 16px;
            opacity: 0.8;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        th {{
            background-color: #3498db;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}
        td {{
            padding: 10px 12px;
            border-bottom: 1px solid #ecf0f1;
        }}
        tr:hover {{
            background-color: #f8f9fa;
        }}
        .summary-box {{
            background-color: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .date-range {{
            text-align: center;
            color: #7f8c8d;
            font-style: italic;
            margin: 10px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🏋️ Training & Wellness Report</h1>
        <div class="date-range">
            Report Period: {self.metrics_pivot['Timestamp'].min().strftime('%Y-%m-%d')} to {self.metrics_pivot['Timestamp'].max().strftime('%Y-%m-%d')}
        </div>
        
        <h2>📊 Key Metrics Summary</h2>
        <div class="stats-grid">
            <div class="stat-card green">
                <div class="stat-label">Average Sleep</div>
                <div class="stat-value">{stats.get('avg_sleep', 0):.2f} <span class="stat-unit">hours</span></div>
            </div>
            <div class="stat-card blue">
                <div class="stat-label">Average HRV</div>
                <div class="stat-value">{stats.get('avg_hrv', 0):.1f} <span class="stat-unit">ms</span></div>
            </div>
            <div class="stat-card orange">
                <div class="stat-label">Resting Heart Rate</div>
                <div class="stat-value">{stats.get('avg_pulse', 0):.0f} <span class="stat-unit">bpm</span></div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total Workouts</div>
                <div class="stat-value">{stats.get('total_workouts', 0)}</div>
            </div>
        </div>
        
        <h2>💤 Sleep Analysis</h2>
        <div class="summary-box">
            <p><strong>Sleep Duration:</strong> Min: {stats.get('min_sleep', 0):.2f}h | Max: {stats.get('max_sleep', 0):.2f}h | Avg: {stats.get('avg_sleep', 0):.2f}h</p>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Sleep Hours</th>
                    <th>Deep Sleep</th>
                    <th>Light Sleep</th>
                    <th>REM Sleep</th>
                    <th>HRV</th>
                    <th>Pulse</th>
                </tr>
            </thead>
            <tbody>
"""
        
        # Add sleep data rows
        for _, row in self.metrics_pivot.iterrows():
            html_content += f"""                <tr>
                    <td>{row['Timestamp'].strftime('%Y-%m-%d')}</td>
                    <td>{row.get('Sleep Hours', '-')}</td>
                    <td>{row.get('Time In Deep Sleep', '-')}</td>
                    <td>{row.get('Time In Light Sleep', '-')}</td>
                    <td>{row.get('Time In REM Sleep', '-')}</td>
                    <td>{row.get('HRV', '-')}</td>
                    <td>{row.get('Pulse', '-')}</td>
                </tr>
"""
        
        html_content += """            </tbody>
        </table>
        
        <h2>🏃 Workout Summary</h2>
        <div class="summary-box">
"""
        
        html_content += f"            <p><strong>Total Training Duration:</strong> {stats.get('total_duration_hours', 0):.2f} hours</p>\n"
        html_content += "            <p><strong>Workout Types:</strong></p>\n            <ul>\n"
        
        for workout_type, count in stats.get('workout_types', {}).items():
            html_content += f"                <li>{workout_type}: {count} sessions</li>\n"
        
        html_content += """            </ul>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Type</th>
                    <th>Duration (h)</th>
                    <th>Avg HR</th>
                    <th>Max HR</th>
                    <th>RPE</th>
                    <th>Feeling</th>
                </tr>
            </thead>
            <tbody>
"""
        
        # Add workout data rows
        for _, row in self.workouts_df.iterrows():
            html_content += f"""                <tr>
                    <td>{pd.to_datetime(row['WorkoutDay']).strftime('%Y-%m-%d')}</td>
                    <td>{row['WorkoutType']}</td>
                    <td>{row['TimeTotalInHours']:.2f}</td>
                    <td>{row.get('HeartRateAverage', '-')}</td>
                    <td>{row.get('HeartRateMax', '-')}</td>
                    <td>{row.get('Rpe', '-')}</td>
                    <td>{row.get('Feeling', '-')}</td>
                </tr>
"""
        
        html_content += """            </tbody>
        </table>
        
        <h2>📈 HRV Analysis</h2>
        <div class="summary-box">
"""
        
        html_content += f"""            <p><strong>HRV Range:</strong> Min: {stats.get('min_hrv', 0):.0f} | Max: {stats.get('max_hrv', 0):.0f} | Avg: {stats.get('avg_hrv', 0):.1f}</p>
            <p><strong>Note:</strong> Higher HRV generally indicates better recovery and readiness to train.</p>
        </div>
        
        <div class="date-range" style="margin-top: 40px;">
            Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
</body>
</html>
"""
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Report generated successfully: {output_file}")
        return output_file


def main():
    """Main function to run the report generator."""
    # File paths - adjust these to match your file locations
    metrics_file = 'metrics.csv'
    workouts_file = 'workouts.csv'
    output_file = 'training_report.html'
    
    # Check if files exist
    if not os.path.exists(metrics_file):
        print(f"❌ Error: {metrics_file} not found!")
        return
    
    if not os.path.exists(workouts_file):
        print(f"❌ Error: {workouts_file} not found!")
        return
    
    # Generate report
    print("🔄 Generating report...")
    generator = WorkoutReportGenerator(metrics_file, workouts_file)
    generator.generate_html_report(output_file)
    print(f"📄 Open {output_file} in your browser to view the report.")


if __name__ == "__main__":
    main()
