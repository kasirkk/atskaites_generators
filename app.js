// app.js — client-side aggregator + Plotly chart

const unwanted = ['strength','other','strength training','pilates','yoga','training','meditation'];
const fileInput = document.getElementById('fileInput');
const generateBtn = document.getElementById('generateBtn');
const downloadHtmlBtn = document.getElementById('downloadHtmlBtn');
const downloadPngBtn = document.getElementById('downloadPngBtn');
const chartDiv = document.getElementById('chart');
const messageDiv = document.getElementById('message');
let lastFig = null;

fileInput.addEventListener('change', () => {
  generateBtn.disabled = fileInput.files.length === 0;
  downloadHtmlBtn.disabled = true;
  downloadPngBtn.disabled = true;
  messageDiv.textContent = '';
});

generateBtn.addEventListener('click', () => {
  const files = Array.from(fileInput.files);
  if (!files.length) return;
  messageDiv.textContent = 'Lasu un apstrādāju failus...';
  Promise.all(files.map(f => parseCsvFile(f))).then(results => {
    const aggregated = aggregate(results);
    if (Object.keys(aggregated.rezultati).length === 0) {
      messageDiv.textContent = 'Nav derīgu datu.';
      return;
    }
    renderChart(aggregated.rezultati, aggregated.dateRange);
    messageDiv.textContent = '';
    downloadHtmlBtn.disabled = false;
    downloadPngBtn.disabled = false;
  }).catch(err => {
    console.error(err);
    messageDiv.textContent = 'Kļūda apstrādē: ' + err.message;
  });
});

function parseCsvFile(file){
  return new Promise((resolve, reject) => {
    Papa.parse(file, {
      header: true,
      skipEmptyLines: true,
      complete: (res) => {
        const data = res.data.map(row => {
          const norm = {};
          for (const k in row) {
            norm[k.trim()] = row[k];
          }
          return norm;
        });
        resolve({name: file.name.replace(/\.csv$/i,'').replace(/[^\w\s-]/g,''), rows: data});
      },
      error: (err) => reject(err)
    });
  });
}

function aggregate(filesData){
  const rezultati = {};
  let overallMin = null, overallMax = null;
  filesData.forEach(f => {
    const rows = f.rows;
    let zona2 = 0, zona3 = 0, sessions = 0;
    rows.forEach(r => {
      const wt = (r['WorkoutType'] || r['Workout type'] || '').toString().toLowerCase().trim();
      if (!unwanted.includes(wt)) sessions += 1;
      const z2 = parseFloat(r['HRZone2Minutes'] || r['HR Zone 2 Minutes'] || r['HRZone2'] || 0) || 0;
      const z3 = parseFloat(r['HRZone3Minutes'] || r['HR Zone 3 Minutes'] || r['HRZone3'] || 0) || 0;
      zona2 += z2; zona3 += z3;
      const wd = r['WorkoutDay'] || r['Workout Day'] || r['Date'] || r['date'];
      if (wd) {
        const dt = new Date(wd);
        if (!isNaN(dt)){
          if (!overallMin || dt < overallMin) overallMin = dt;
          if (!overallMax || dt > overallMax) overallMax = dt;
        }
      }
    });
    const minutes = Math.round(zona2 * 1 + zona3 * 2);
    rezultati[f.name] = {minutes: minutes, sessions: sessions};
  });
  const dateRange = (overallMin && overallMax) ? formatDate(overallMin) + ' - ' + formatDate(overallMax) : null;
  return {rezultati, dateRange};
}

function formatDate(d){
  const dd = String(d.getDate()).padStart(2,'0');
  const mm = String(d.getMonth()+1).padStart(2,'0');
  const yyyy = d.getFullYear();
  return `${dd}.${mm}.${yyyy}`;
}

function renderChart(rezultati, dateRange){
  const items = Object.entries(rezultati).map(([k,v])=>({name:k, minutes:v.minutes, sessions:v.sessions}));
  items.sort((a,b)=>a.minutes-b.minutes);
  const names = items.map(i=>i.name);
  const minutes = items.map(i=>i.minutes);
  const sessions = items.map(i=>i.sessions);

  const limeni = [0,150,300,1000];
  const limenu_nosaukumi = ['Enerģijas ražotājs','Labsajūtas meistars','Metabolisma Inženieris','Izturības Arhitekts','Kaizen Leģenda'];

  const shapes = [];
  for (let i=0;i<limeni.length-1;i++){
    shapes.push({type:'rect', xref:'paper', yref:'y', x0:0,x1:1, y0:limeni[i], y1:limeni[i+1], fillcolor:'rgba(46,204,113,0.12)', line:{width:0}, layer:'below'});
  }
  shapes.push({type:'line', xref:'paper', yref:'y', x0:0,x1:1, y0:150,y1:150, line:{color:'green', width:3}, layer:'below'});
  shapes.push({type:'line', xref:'paper', yref:'y', x0:0,x1:1, y0:300,y1:300, line:{color:'green', width:3}, layer:'below'});

  const trace = {type:'bar', x:names, y:minutes, marker:{color:'black'}, name:'Minūtes zonās', hovertemplate:'<b>%{x}</b><br>Minūtes: %{y}<br>Sesijas: %{customdata}', customdata:sessions};

  const maxY = Math.max(350, Math.max(...minutes)+50);

  const annotations = [];
  const y_positions = [maxY*0.03, maxY*0.2, maxY*0.45, maxY*0.7, maxY*0.95];
  limenu_nosaukumi.forEach((n,i)=>{
    annotations.push({xref:'paper', yref:'y', x:-0.02, y:y_positions[i], text:n, showarrow:false, font:{size:14,color:'#2d3436'}, align:'right', xanchor:'right'});
  });

  const outlineOffsets = [[-1,0],[1,0],[0,-1],[0,1],[-1,-1],[-1,1],[1,-1],[1,1]];
  const maxMin = Math.max(...minutes,0);
  names.forEach((n, idx)=>{
    const ym = minutes[idx];
    const sc = sessions[idx];
    const yPos = Math.max(ym * 0.5, 10);
    annotations.push({x:n, y:yPos, text:String(sc), showarrow:false, font:{size:10, color: 'white'}});
    const yTop = ym + Math.max(8, Math.round(maxMin*0.02));
    outlineOffsets.forEach(off => {
      annotations.push({x:n, y:yTop, xref:'x', yref:'y', xshift:off[0], yshift:off[1], text:String(ym), showarrow:false, font:{size:12, color:'black'}});
    });
    annotations.push({x:n, y:yTop, xref:'x', yref:'y', text:String(ym), showarrow:false, font:{size:12, color:'white'}});
  });

  if (dateRange){
    var title = `Active For Life (${dateRange})`;
  } else {
    var title = 'Active For Life';
  }

  const layout = {
    title: {text:title, x:0.02},
    shapes: shapes,
    annotations: annotations,
    height:600,
    margin:{l:180, r:40, t:90, b:140},
    yaxis:{range:[0,maxY], gridcolor:'rgba(0,0,0,0.06)'},
    plot_bgcolor:'white',
    bargap:0.15
  };

  const fig = {data:[trace], layout:layout};
  Plotly.newPlot(chartDiv, fig.data, fig.layout, {responsive:true});
  lastFig = {data:fig.data, layout:fig.layout};
}

downloadHtmlBtn.addEventListener('click', ()=>{
  if (!lastFig) return;
  const html = `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Active For Life — Kopsavilkums</title><script src="https://cdn.plot.ly/plotly-2.24.2.min.js"></script></head><body>${chartDiv.innerHTML}<script>var fig = ${JSON.stringify(lastFig)};Plotly.newPlot(document.querySelector('#' + Object.keys(document.querySelectorAll('div')[0].id || {}).join()), fig.data, fig.layout);</script></body></html>`;
  const blob = new Blob([html], {type:'text/html'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = 'kopsavilkums.html'; document.body.appendChild(a); a.click(); a.remove();
});

downloadPngBtn.addEventListener('click', ()=>{
  if (!lastFig) return;
  Plotly.toImage(chartDiv, {format:'png', height:600, width:1000}).then(dataUrl => {
    const a = document.createElement('a'); a.href = dataUrl; a.download = 'kopsavilkums.png'; document.body.appendChild(a); a.click(); a.remove();
  });
});
