Static web app (GitHub Pages)

What this is
- A small static web application that runs entirely in the browser.
- Users upload CSV files (one per athlete) and the app aggregates minutes and sessions and renders an interactive Plotly chart.

How to use locally
1. Open `index.html` in your browser (double-click or drag into the browser).
2. Click "Choose files" and select one or more CSVs (one file per athlete).
3. Click "Ģenerēt grafiku" to render the chart.
4. Use "Saglabāt kā HTML" or "Saglabāt kā PNG" to export results.

Deploy to GitHub Pages
1. Commit and push these root files to your repository `main` branch.
2. In your repo Settings → Pages, set Source to `Branch: main` and `Folder: / (root)`.
3. Save — after a minute your site will be available via the GitHub Pages URL shown in Settings.

Notes
- The app uses PapaParse to parse CSV and Plotly for visualization (both loaded from CDN).
- If your CSV has different column names, the script attempts common alternatives: `HRZone2Minutes`, `HR Zone 2 Minutes`, `HRZone3Minutes`, `WorkoutDay`, `WorkoutType`.
- The session counting excludes workout types: strength, other, strength training, pilates, yoga, training, meditation.

Security & Privacy
- Data is processed in the user's browser — nothing is uploaded to a server.

If you want, I can:
- Add sample CSV files in `samples/` for testing.
- Create a GitHub Action to automatically deploy to the `gh-pages` branch.
