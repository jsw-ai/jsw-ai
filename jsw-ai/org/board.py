"""Interactive Scoreboard page body (HTML + vanilla JS). Fetches ./api/board."""

BODY = r'''
<h1>Scoreboard <span id="samp" style="font-size:12px;background:#3a3320;color:#f7d67a;padding:3px 10px;border-radius:12px;vertical-align:middle;margin-left:8px">sample data</span></h1>
<p style="color:#9aa5b1;margin-top:-4px">Overall Score is a weighted, normalized blend of every metric below — revenue and Fanvue subs weighted highest. Live numbers replace the sample once the platform collectors run.</p>

<div class="card" style="display:flex;gap:14px;flex-wrap:wrap;align-items:flex-end">
  <div style="flex:1;min-width:170px"><label>Search</label><input id="q" placeholder="persona name..."></div>
  <div style="min-width:150px"><label>Team</label><select id="teamf"></select></div>
  <div style="min-width:200px"><label>Chart metric</label><select id="metricf"></select></div>
</div>

<h2>Couples</h2>
<div id="teams" style="display:flex;gap:14px;flex-wrap:wrap"></div>

<h2 id="charttitle">Overall Score</h2>
<div class="card"><div id="chart"></div></div>

<h2>Rankings</h2>
<table id="board"><thead id="bhead"></thead><tbody id="bbody"></tbody></table>

<style>
.bar{height:22px;border-radius:5px;transition:width .5s ease}
.barrow{display:flex;align-items:center;gap:10px;margin:7px 0}
.barrow .nm{width:150px;font-size:13px;color:#e6e6e6}
.barrow .vl{font-size:12px;color:#9aa5b1;min-width:70px}
#board th{cursor:pointer;user-select:none;white-space:nowrap}
#board th:hover{color:#7aa2f7}
.tcard{flex:1;min-width:240px}
.member{display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #222732}
.heart{color:#f7a2c0;text-align:center;font-size:13px;margin:4px 0}
.hl{outline:2px solid #f7a2c0}
tr.hlrow{background:#241b22}
</style>

<script>
const TEAMCOLORS = ['#7aa2f7','#f7a2c0','#7ee2a8','#f7c97a','#c0a2f7','#7ae2e2'];
const ROOT = (window.ORG_ROOT||'').replace(/\/$/,'');
let DATA=null, SORT={key:'score',dir:-1}, teamColor={};

function fmt(key,v){
  if(key==='score') return (+v).toFixed(1);
  if(key==='revenue') return '$'+Math.round(v).toLocaleString();
  if(key==='engagement_rate') return (+v).toFixed(1)+'%';
  return Math.round(v).toLocaleString();
}
function filtered(){
  const q=(document.getElementById('q').value||'').toLowerCase();
  const tf=document.getElementById('teamf').value;
  return DATA.personas.filter(p=>
    (!q||p.name.toLowerCase().includes(q)) && (tf==='__all'||p.team===tf));
}
function renderTeams(){
  const box=document.getElementById('teams'); box.innerHTML='';
  DATA.teams.forEach(t=>{
    const c=teamColor[t.team];
    const m=t.members;
    let inner='';
    m.forEach((x,i)=>{
      inner+=`<div class="member" data-slug="${x.slug}"><span><a href="${ROOT}/model/${x.slug}">${x.name}</a> <span style="color:#6b7280;font-size:12px">${x.geo||''}</span></span><b>${x.score.toFixed(1)}</b></div>`;
      if(i===0 && m.length>1) inner+=`<div class="heart">❤ together</div>`;
    });
    box.innerHTML+=`<div class="card tcard" style="border-top:3px solid ${c}">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <h3 style="margin:0;font-size:16px">#${t.rank} ${t.team}</h3>
        <span class="pill" style="background:${c}22;color:${c}">${t.score.toFixed(1)}</span></div>
      <div style="margin-top:8px">${inner}</div>
      <div style="margin-top:8px;color:#9aa5b1;font-size:12px">Rev $${Math.round(t.revenue).toLocaleString()} · Fanvue ${t.fanvue_subs} subs</div>
    </div>`;
  });
}
function renderChart(){
  const key=document.getElementById('metricf').value;
  const meta=DATA.metrics.find(m=>m.key===key);
  document.getElementById('charttitle').textContent = key==='score'?'Overall Score':meta.label;
  const rows=filtered().slice().sort((a,b)=> (key==='score'? b.score-a.score : (b.metrics[key]-a.metrics[key])));
  const val=p=> key==='score'? p.score : p.metrics[key];
  const max=Math.max(1,...rows.map(val));
  const ch=document.getElementById('chart'); ch.innerHTML='';
  rows.forEach(p=>{
    const w=Math.max(2,(val(p)/max)*100);
    ch.innerHTML+=`<div class="barrow"><div class="nm">${p.name}</div>
      <div class="bar" style="width:${w}%;background:${teamColor[p.team]}"></div>
      <div class="vl">${fmt(key,val(p))}</div></div>`;
  });
}
function renderTable(){
  const cols=[{key:'rank',label:'#'},{key:'name',label:'Persona'},{key:'team',label:'Team'},
              {key:'partner_name',label:'❤ Partner'},{key:'score',label:'Overall'}]
    .concat(DATA.metrics.map(m=>({key:m.key,label:m.label})));
  const head=document.getElementById('bhead');
  head.innerHTML='<tr>'+cols.map(c=>`<th data-k="${c.key}">${c.label}${SORT.key===c.key?(SORT.dir<0?' ▾':' ▴'):''}</th>`).join('')+'</tr>';
  head.querySelectorAll('th').forEach(th=>th.onclick=()=>{
    const k=th.dataset.k; SORT.dir = SORT.key===k? -SORT.dir : -1; SORT.key=k; renderTable();
  });
  let rows=filtered();
  const gv=(p,k)=> k in p? p[k] : (p.metrics[k]!==undefined?p.metrics[k]:'');
  rows.sort((a,b)=>{
    let x=gv(a,SORT.key), y=gv(b,SORT.key);
    if(typeof x==='string'){return SORT.dir*x.localeCompare(y);}
    return SORT.dir*((x||0)-(y||0));
  });
  const body=document.getElementById('bbody'); body.innerHTML='';
  rows.forEach(p=>{
    let tds=cols.map(c=>{
      if(c.key==='rank')return `<td>${p.rank}</td>`;
      if(c.key==='name')return `<td data-slug="${p.slug}"><a href="${ROOT}/model/${p.slug}"><b>${p.name}</b></a></td>`;
      if(c.key==='team')return `<td><span class="pill" style="background:${teamColor[p.team]}22;color:${teamColor[p.team]}">${p.team}</span></td>`;
      if(c.key==='partner_name')return `<td style="color:#f7a2c0">${p.partner_name||''}</td>`;
      if(c.key==='score')return `<td><b>${p.score.toFixed(1)}</b></td>`;
      return `<td>${fmt(c.key,p.metrics[c.key])}</td>`;
    }).join('');
    body.innerHTML+=`<tr data-slug="${p.slug}" data-partner="${p.partner_slug||''}">${tds}</tr>`;
  });
  body.querySelectorAll('tr').forEach(tr=>tr.onclick=()=>{
    const ps=tr.dataset.partner;
    document.querySelectorAll('#bbody tr').forEach(r=>r.classList.remove('hlrow'));
    tr.classList.add('hlrow');
    if(ps){const pr=document.querySelector(`#bbody tr[data-slug="${ps}"]`); if(pr)pr.classList.add('hlrow');}
  });
}
function renderAll(){renderTeams();renderChart();renderTable();}
fetch('api/board').then(r=>r.json()).then(d=>{
  DATA=d;
  d.teams.forEach((t,i)=>teamColor[t.team]=TEAMCOLORS[i%TEAMCOLORS.length]);
  const tf=document.getElementById('teamf');
  tf.innerHTML='<option value="__all">All teams</option>'+d.teams.map(t=>`<option>${t.team}</option>`).join('');
  const mf=document.getElementById('metricf');
  mf.innerHTML='<option value="score">Overall Score</option>'+d.metrics.map(m=>`<option value="${m.key}">${m.label}</option>`).join('');
  ['q','teamf'].forEach(id=>document.getElementById(id).addEventListener('input',renderAll));
  document.getElementById('metricf').addEventListener('input',renderChart);
  if(!d.sample)document.getElementById('samp').style.display='none';
  renderAll();
});
</script>
'''
