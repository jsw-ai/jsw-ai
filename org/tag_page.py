"""Tag page: assign untagged on-disk photos to a persona + content folder (SFW/X/Fanvue)."""

BODY = r'''
<h1>Tag photos</h1>
<p style="color:#9aa5b1;margin-top:-4px">Every untagged photo on disk is below. For each one, pick the model and the folder it belongs in — it moves straight into that model's library. SFW = IG/TikTok safe · X = X subscriber content · Fanvue = adult.</p>

<div class="card" style="display:flex;gap:14px;flex-wrap:wrap;align-items:center">
  <div><label style="font-size:13px;color:#9aa5b1">Default model for "Assign all shown"</label>
    <select id="bulkModel" style="min-width:180px"></select></div>
  <div style="align-self:flex-end;display:flex;gap:6px">
    <button class="cat sfw" onclick="bulkAll('sfw')">Assign all → SFW</button>
    <button class="cat x" onclick="bulkAll('x')">→ X</button>
    <button class="cat fanvue" onclick="bulkAll('fanvue')">→ Fanvue</button>
  </div>
  <span id="count" style="color:#9aa5b1;font-size:13px;margin-left:auto"></span>
</div>

<div id="grid" class="tgrid"></div>
<p id="empty" style="color:#6b7280;display:none;margin-top:20px">Nothing left to tag — every photo has a home. 🎉</p>

<style>
.tgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px;margin-top:14px}
.tcard{background:#161922;border:1px solid #262b36;border-radius:10px;overflow:hidden}
.tcard img{width:100%;height:200px;object-fit:cover;background:#0f1115;display:block}
.tcard .ctr{padding:10px}
.tcard select{width:100%;margin-bottom:8px}
.cats{display:flex;gap:6px}
.cat{flex:1;background:#222732;color:#9aa5b1;border:0;padding:7px 0;border-radius:6px;cursor:pointer;font-weight:700;font-size:13px}
.cat.sfw:hover{background:#7aa2f7;color:#0f1115}
.cat.x:hover{background:#7ee2a8;color:#0f1115}
.cat.fanvue:hover{background:#f78ac0;color:#0f1115}
.hint{font-size:11px;color:#6b7280;margin-top:6px;text-align:center}
</style>

<script>
const ROOT = (window.ORG_ROOT||'').replace(/\/$/,'');
let PERSONAS=[], ITEMS=[];

Promise.all([
  fetch(ROOT+'/api/board').then(r=>r.json()),
  fetch(ROOT+'/api/untagged').then(r=>r.json())
]).then(([board,unt])=>{
  PERSONAS=board.personas.slice().sort((a,b)=>a.name.localeCompare(b.name));
  ITEMS=unt.images||[];
  const bm=document.getElementById('bulkModel');
  bm.innerHTML=PERSONAS.map(p=>`<option value="${p.slug}">${p.name}</option>`).join('');
  render();
});

function optionsHtml(sel){
  return '<option value="" disabled'+(sel?'':' selected')+'>choose model…</option>'+
    PERSONAS.map(p=>`<option value="${p.slug}">${p.name}</option>`).join('');
}
function render(){
  const grid=document.getElementById('grid'); grid.innerHTML='';
  document.getElementById('count').textContent=ITEMS.length+' untagged';
  document.getElementById('empty').style.display=ITEMS.length?'none':'block';
  ITEMS.forEach(it=>{
    const el=document.createElement('div'); el.className='tcard'; el.dataset.idx=it.idx;
    el.innerHTML=`
      <img loading="lazy" src="${ROOT}/content_img/${it.idx}">
      <div class="ctr">
        <select id="sel_${it.idx}">${optionsHtml()}</select>
        <div class="cats">
          <button class="cat sfw" onclick="assign(${it.idx},'sfw')">SFW</button>
          <button class="cat x" onclick="assign(${it.idx},'x')">X</button>
          <button class="cat fanvue" onclick="assign(${it.idx},'fanvue')">Fanvue</button>
        </div>
        <div class="hint">${it.under_nsfw?'(was in an NSFW folder)':''}</div>
      </div>`;
    grid.appendChild(el);
  });
}
function post(idx,slug,cat){
  return fetch(ROOT+'/api/tag/set',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({idx,slug,category:cat})}).then(r=>r.json());
}
function assign(idx,cat){
  const slug=document.getElementById('sel_'+idx).value;
  if(!slug){ document.getElementById('sel_'+idx).style.borderColor='#f7a2a2'; return; }
  post(idx,slug,cat).then(res=>{
    if(res&&res.ok){ ITEMS=ITEMS.filter(x=>x.idx!==idx); render(); }
  });
}
function bulkAll(cat){
  const slug=document.getElementById('bulkModel').value;
  if(!slug||!ITEMS.length) return;
  if(!confirm('Assign all '+ITEMS.length+' shown photos to '+slug+' → '+cat.toUpperCase()+'?')) return;
  const batch=ITEMS.slice();
  Promise.all(batch.map(it=>post(it.idx,slug,cat))).then(()=>{
    ITEMS=[]; render();
  });
}
</script>
'''
