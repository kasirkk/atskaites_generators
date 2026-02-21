Static web app (GitHub Pages)

What this is
- A small static web application that runs entirely in the browser.
- Users upload CSV files (one per athlete) and the app aggregates minutes and sessions and renders an interactive Plotly chart.

How to use locally
1. Open `web_static/index.html` in your browser (double-click or drag into the browser).
2. Click "Choose files" and select one or more CSVs (one file per athlete).
3. Click "Ģenerēt grafiku" to render the chart.
4. Use "Saglabāt kā HTML" or "Saglabāt kā PNG" to export results.

Deploy to GitHub Pages
1. Add the `web_static` folder to your repository root and commit.
2. In your repo settings -> Pages, set the source to the `main` branch and the `/web_static` folder (or `gh-pages` branch), or move files to top-level.
3. After a minute your site will be available via GitHub Pages URL.

Notes
- The app uses PapaParse to parse CSV and Plotly for visualization (both loaded from CDN).
- If your CSV has different column names, the script attempts common alternatives: `HRZone2Minutes`, `HR Zone 2 Minutes`, `HRZone3Minutes`, `WorkoutDay`, `WorkoutDay`, `WorkoutType`.
- The session counting excludes workout types: strength, other, strength training, pilates, yoga, training, meditation.

Security & Privacy
- Data is processed in the user's browser — nothing is uploaded to a server.
- If you deploy to a public site, users will still keep their CSVs local; they must upload them in-browser each session.

If you want, I can:
- Tweak column name fallbacks for your exact CSVs.
- Add sample CSV files in `web_static/samples/` for testing.
- Move files to repository root for immediate GitHub Pages publishing.
