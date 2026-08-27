"""Interactive Org page: reporting tree, clickable agent detail drawer, activity log."""

BODY = r'''
<h1>Org</h1>
<p style="color:#9aa5b1;margin-top:-4px">Click any agent to see what it's doing, its live status, and its activity log. Lines show who reports to whom.</p>

<div class="card" style="display:flex;gap:14px;flex-wrap:wrap;align-items:center">
  <div style="display:flex;gap:6px">
    <button id="tabTree" class="tab on">Org Tree</button>
    <button id="tabLog" class="tab">Activity Log</button>
  </div>
  <div style="flex:1;min-width:180px"><input id="q" placeholder="search agents..."></div>
  <span id="counts" style="color:#9aa5b1;font-size:13px"></span>
</div>

<div id="treeView" style="display:flex;gap:16px;align-items:flex-start">
  <div id="tree" class="card" style="flex:1;min-width:340px;max-height:620px;overflow:auto"></div>
  <div id="drawer" class="card" style="width:380px;min-height:300px">
    <p style="color:#6b7280">Select an agent to see details.</p>
  </div>
</div>

<div id="logView" style="display:none" class="card"></div>

<style>
.tab{background:#222732;color:#9aa5b1;border:0;padding:7px 14px;border-radius:6px;cursor:pointer;font-weight:600}
.tab.on{background:#7aa2f7;color:#0f1115}
.node{padding:2px 0}
.nrow{display:flex;align-items:center;gap:8px;padding:5px 7px;border-radius:6px;cursor:pointer}
.nrow:hover{background:#1c212b}
.nrow.sel{background:#243044}
.kids{margin-left:16px;border-left:1px solid #2a3040;padding-left:10px}
.dot{width:9px;height:9px;border-radius:50%;flex:none}
.d-run{background:#7ee2a8}.d-idle{background:#5b6472}.d-err{background:#f7a2a2}
.tw{font-size:11px;color:#6b7280;margin-left:auto}
.tgl{width:14px;color:#6b7280;font-size:11px;cursor:pointer;user-select:none}
.logline{display:flex;gap:10px;padding:6px 0;border-bottom:1px solid #222732;font-size:13px}
.logline .t{color:#6b7280;min-width:120px}
.kpill{font-size:11px;background:#222732;color:#9aa5b1;padding:1px 7px;border-radius:10px}
</style>

<script>
let AG=[], BYNAME={}, KIDS={}, SEL=null;
const Kcolor={leadership:'#c0a2f7',manager:'#f7c97a',reviewer:'#7ae2e2',model:'#7aa2f7',platform:'#7ee2a8',function:'#f7a2c0'};
function tclass(s){return s==='running'?'d-run':s==='error'?'d-err':'d-idle';}
function ago(ts){ if(!ts)return ''; const s=(Date.now()/1000)-ts; if(s<90)return 'just now'; if(s<3600)return Math.round(s/60)+'m ago'; if(s<86400)return Math.round(s/3600)+'h ago'; return Math.round(s/86400)+'d ago';}

function renderTree(){
  const q=(document.getElementById('q').value||'').toLowerCase();
  const box=document.getElementById('tree'); box.innerHTML='';
  const roots=AG.filter(a=>!a.reports_to);
  roots.forEach(r=>box.appendChild(node(r,q)));
  document.getElementById('counts').textContent = AG.length+' agents · '+AG.filter(a=>a.status==='running').length+' running';
}
function node(a,q){
  const wrap=document.createElement('div'); wrap.className='node';
  const row=document.createElement('div'); row.className='nrow'+(SEL===a.id?' sel':'');
  const kids=(KIDS[a.name]||[]);
  const hasKids=kids.length>0;
  const match=q && a.title.toLowerCase().includes(q);
  row.innerHTML=`<span class="tgl">${hasKids?'▾':''}</span>
     <span class="dot ${tclass(a.status)}"></span>
     <span style="color:${Kcolor[a.kind]||'#e6e6e6'};font-weight:600">${a.title}</span>
     <span class="kpill">${a.kind}</span>
     <span class="tw">${a.current_task?('• '+a.current_task):''}</span>`;
  if(match) row.style.background='#33321f';
  row.onclick=(e)=>{ if(e.target.classList.contains('tgl'))return; openAgent(a.id); };
  wrap.appendChild(row);
  if(hasKids){
    const kd=document.createElement('div'); kd.className='kids';
    kids.forEach(k=>kd.appendChild(node(k,q)));
    wrap.appendChild(kd);
    const tgl=row.querySelector('.tgl');
    tgl.onclick=()=>{ kd.style.display = kd.style.display==='none'?'block':'none'; tgl.textContent = kd.style.display==='none'?'▸':'▾'; };
  }
  return wrap;
}
function openAgent(id){
  SEL=id; renderTree();
  fetch('api/agent/'+id).then(r=>r.json()).then(a=>{
    const d=document.getElementById('drawer');
    const reports = a.direct_reports.length? a.direct_reports.map(r=>`<span class="kpill" style="cursor:pointer" onclick="openAgent(${r.id})">${r.title}</span>`).join(' ') : '<span style="color:#6b7280">none</span>';
    const boss = a.reports_to_obj? `<span class="kpill" style="cursor:pointer" onclick="openAgent(${a.reports_to_obj.id})">${a.reports_to_obj.title}</span>` : '<span style="color:#6b7280">— top of org —</span>';
    const log = a.log.length? a.log.map(e=>`<div class="logline"><span class="t">${ago(e.ts)}</span><span>${e.msg}</span></div>`).join('') : '<p style="color:#6b7280">No activity yet.</p>';
    d.innerHTML=`
      <div style="display:flex;justify-content:space-between;align-items:center">
        <h2 style="margin:0;color:${Kcolor[a.kind]||'#e6e6e6'}">${a.title}</h2>
        <span class="dot ${tclass(a.status)}" style="width:12px;height:12px"></span></div>
      <div style="color:#9aa5b1;font-size:13px;margin:4px 0 12px">${a.kind}${a.persona?(' · '+a.persona):''}${a.team?(' · '+a.team):''} · status <b>${a.status}</b></div>
      ${(a.kind==='model'&&a.slug)?`<div style="margin-bottom:12px"><a href="${(window.ORG_ROOT||'').replace(/\/$/,'')}/model/${a.slug}">View full profile →</a></div>`:''}
      <div style="display:flex;gap:8px;margin-bottom:14px">
        <button class="tab on" onclick="ctl(${a.id},'start')">▶ Start</button>
        <button class="tab" onclick="ctl(${a.id},'stop')">■ Stop</button></div>
      <h3 style="font-size:13px;color:#9aa5b1">Currently</h3>
      <p>${a.current_task||'<span style=color:#6b7280>Idle</span>'}</p>
      <h3 style="font-size:13px;color:#9aa5b1">Reports to</h3><p>${boss}</p>
      <h3 style="font-size:13px;color:#9aa5b1">Direct reports (${a.direct_reports.length})</h3><p style="line-height:2">${reports}</p>
      <h3 style="font-size:13px;color:#9aa5b1">Config</h3>
      <p style="color:#9aa5b1;font-size:13px">Cycle every ${a.interval||60}s · last active ${a.last_beat?ago(a.last_beat):'—'}</p>
      <h3 style="font-size:13px;color:#9aa5b1;margin-top:14px">Activity log</h3>${log}
      <h3 style="font-size:13px;color:#9aa5b1;margin-top:16px">Instructions (SOP) — the agent's brief</h3>
      <textarea id="sop" style="width:100%;height:220px;background:#0f1115;border:1px solid #333a48;color:#e6e6e6;border-radius:6px;padding:10px;box-sizing:border-box;font:inherit;font-size:12px"></textarea>
      <div style="margin-top:8px"><button onclick="saveSop(${a.id})">Save instructions</button><span id="sopmsg" style="color:#7ee2a8;font-size:12px;margin-left:10px"></span></div>`;
    document.getElementById('sop').value = a.sop || '';
  });
}
function saveSop(id){
  const v=document.getElementById('sop').value;
  fetch('api/sop/'+id,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({sop:v})})
    .then(r=>r.json()).then(()=>{const m=document.getElementById('sopmsg'); m.textContent='Saved ✓'; setTimeout(()=>m.textContent='',2000);});
}
function ctl(id,action){ fetch('api/agent/'+id+'/'+action,{method:'POST'}).then(r=>r.json()).then(()=>load(()=>openAgent(id))); }
function renderLog(){
  fetch('api/activity').then(r=>r.json()).then(d=>{
    const box=document.getElementById('logView');
    box.innerHTML='<h2 style="margin-top:0">Activity Log</h2>'+ (d.length? d.map(e=>
      `<div class="logline"><span class="t">${ago(e.ts)}</span><span style="min-width:170px;color:${Kcolor[e.kind]||'#7aa2f7'}">${e.title}</span><span>${e.msg}</span></div>`).join('') : '<p style="color:#6b7280">No activity yet.</p>');
  });
}
function load(cb){
  fetch('api/org').then(r=>r.json()).then(d=>{
    AG=d.agents; BYNAME={}; KIDS={};
    AG.forEach(a=>BYNAME[a.name]=a);
    AG.forEach(a=>{ if(a.reports_to){ (KIDS[a.reports_to]=KIDS[a.reports_to]||[]).push(a); } });
    renderTree(); if(cb)cb();
  });
}
document.getElementById('q').addEventListener('input',renderTree);
document.getElementById('tabTree').onclick=()=>{setTab('tree');};
document.getElementById('tabLog').onclick=()=>{setTab('log');renderLog();};
function setTab(t){
  document.getElementById('treeView').style.display=t==='tree'?'flex':'none';
  document.getElementById('logView').style.display=t==='log'?'block':'none';
  document.getElementById('tabTree').classList.toggle('on',t==='tree');
  document.getElementById('tabLog').classList.toggle('on',t==='log');
}
load();
</script>
'''
