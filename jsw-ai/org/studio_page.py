"""ZenCreator Studio: select model -> face/body refs auto-load -> any Zen tool + ALL its
options (form rendered live from the tool's input_schema) -> generate -> output lands in
the model's SFW/X/Fanvue folder. Served at /studio/<slug>."""

BODY = r'''
<div id="top"></div>
<div style="display:flex;gap:16px;align-items:flex-start;flex-wrap:wrap">
  <div class="card" style="flex:1;min-width:380px">
    <h2 style="margin-top:0">1 · Tool</h2>
    <select id="toolSel"></select>
    <p id="toolDesc" style="color:#9aa5b1;font-size:13px;white-space:pre-wrap;max-height:130px;overflow:auto"></p>
    <h2>2 · Options</h2>
    <div id="form"></div>
    <h2>3 · Destination</h2>
    <div style="display:flex;gap:8px;align-items:center">
      <select id="catSel" style="max-width:200px">
        <option value="sfw">SFW folder (IG/TikTok)</option>
        <option value="x">X folder</option>
        <option value="fanvue">Fanvue folder</option>
      </select>
      <button id="go" onclick="generate()">✦ Generate</button>
      <span id="msg" style="color:#f7a2a2;font-size:13px"></span>
    </div>
  </div>
  <div style="width:420px;min-width:320px">
    <div class="card">
      <h2 style="margin-top:0">Identity refs</h2>
      <div id="refs" style="display:flex;gap:10px"></div>
    </div>
    <div class="card">
      <h2 style="margin-top:0">Jobs</h2>
      <div id="jobs"><p style="color:#6b7280">No generations yet.</p></div>
    </div>
  </div>
</div>

<div class="card" style="margin-top:16px">
  <h2 style="margin-top:0">✨ Template gallery <span id="tplTotal" style="color:#6b7280;font-size:13px"></span></h2>
  <p style="color:#9aa5b1;font-size:13px;margin-top:0">Ready-made Zen presets — click <b>Load into form</b> and the tool + all options fill in above (your selected refs are kept).</p>
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px">
    <input id="tplQ" placeholder="Search presets… (e.g. beach, selfie, yacht, dance)" style="flex:1;min-width:220px" onkeydown="if(event.key==='Enter')tplLoad(1)">
    <select id="tplTool" style="max-width:190px" onchange="tplLoad(1)"><option value="">All tools</option></select>
    <button class="ab" onclick="tplLoad(1)">Search</button>
  </div>
  <div id="tplList" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:10px"><p style="color:#6b7280">Loading templates…</p></div>
  <div style="margin-top:10px;display:flex;gap:8px;align-items:center">
    <button class="ab" onclick="tplLoad(TPLPAGE-1)">‹ Prev</button>
    <span id="tplPage" style="font-size:12px;color:#9aa5b1"></span>
    <button class="ab" onclick="tplLoad(TPLPAGE+1)">Next ›</button>
  </div>
</div>

<style>
.f{margin-bottom:12px}
.f label{display:block;font-size:13px;color:#9aa5b1;margin-bottom:4px}
.f .req{color:#f7c97a}
.f textarea{width:100%;height:70px;background:#0f1115;border:1px solid #333a48;color:#e6e6e6;border-radius:6px;padding:8px;box-sizing:border-box;font:inherit}
.f .hint{font-size:11px;color:#6b7280;margin-top:3px}
.assetbtns{display:flex;gap:6px;flex-wrap:wrap}
.ab{background:#222732;color:#9aa5b1;border:0;padding:6px 10px;border-radius:6px;cursor:pointer;font-size:12px;font-weight:600}
.ab.on{background:#7aa2f7;color:#0f1115}
.rimg2{width:120px;height:150px;object-fit:cover;border-radius:8px;border:1px solid #262b36}
.jrow{border-bottom:1px solid #222732;padding:8px 0}
.jimgs{display:flex;gap:6px;flex-wrap:wrap;margin-top:6px}
.jimgs img{width:70px;height:88px;object-fit:cover;border-radius:6px;border:1px solid #262b36}
.jtxt{font-size:12px;color:#9aa5b1;white-space:pre-wrap;max-height:80px;overflow:auto;background:#0f1115;border-radius:6px;padding:6px;margin-top:6px}
.st{font-size:11px;padding:2px 8px;border-radius:10px;background:#222732;color:#9aa5b1}
.st.succeeded{background:#1f3d2b;color:#7ee2a8}.st.failed{background:#3d1f1f;color:#f7a2a2}
.st.processing,.st.queued{background:#3a3320;color:#f7d67a}
</style>

<script>
const ROOT=(window.ORG_ROOT||'').replace(/\/$/,'');
const SLUG=location.pathname.split('/studio/')[1].split('/')[0];
let TOOLS=[], SCHEMA=null, TOOL=null, POLLING={};

function isAsset(name, p){
  const d=((p&&p.description)||'').toLowerCase();
  return d.includes('asset id')||/(_ref$|_asset$|_assets$|^ref_|^face$|^body$)/.test(name);
}
Promise.all([
  fetch(ROOT+'/api/model/'+SLUG).then(r=>r.json()),
  fetch(ROOT+'/api/zen/tools').then(r=>r.json()),
  fetch(ROOT+'/api/board').then(r=>r.json())
]).then(([m,t,b])=>{
  TOOLS=t.tools||[];
  const opts=b.personas.slice().sort((a,x)=>a.name.localeCompare(x.name))
    .map(p=>`<option value="${p.slug}"${p.slug===SLUG?' selected':''}>${p.name}</option>`).join('');
  document.getElementById('top').innerHTML=`
    <p style="margin:0 0 10px"><a href="${ROOT}/model/${SLUG}">← ${m.name}'s profile</a></p>
    <div class="card" style="display:flex;gap:14px;align-items:center;flex-wrap:wrap">
      <h1 style="margin:0">✦ Studio</h1>
      <select style="max-width:200px" onchange="location.href='${ROOT}/studio/'+this.value">${opts}</select>
      <a href="https://app.zencreator.pro" target="_blank" style="background:#222732;color:#e6e6e6;padding:8px 12px;border-radius:8px;text-decoration:none;font-size:13px;font-weight:600">Open ZenCreator ↗</a>
      <span style="color:#9aa5b1;font-size:13px">Content generates with ${m.name}'s face + body refs and lands in the folder you pick.</span>
    </div>`;
  const refs=m.refs||{};
  window.FACEI=0; window.BODYI=0; window.BACKI=0; window.WAISTI=0; window.XFI=0;
  window.renderRefs=function(){
    let h='';
    for(const which of ['face','body','back','waist','xfanvue']){
      const n=refs[which]||0;
      h+=`<div><div style="font-size:12px;color:#9aa5b1">${which==='face'?'Face':which==='body'?'Body':which==='back'?'Back':which==='waist'?'Waist-up':'NSFW'} refs <span style="color:#6b7280">(click to use)</span></div><div style="display:flex;gap:6px;flex-wrap:wrap">`;
      for(let i=0;i<n;i++){
        const on=(which==='face'?window.FACEI:which==='body'?window.BODYI:which==='back'?window.BACKI:which==='waist'?window.WAISTI:window.XFI)===i;
        h+=`<img class="rimg2" src="${ROOT}/model/${SLUG}/ref/${which}/${i}" onclick="selRef('${which}',${i})" style="cursor:pointer;border:3px solid ${on?'#7aa2f7':'transparent'}">`;
      }
      h+=`<label style="display:flex;align-items:center;justify-content:center;width:46px;min-height:60px;border:1px dashed #333a48;border-radius:8px;cursor:pointer;color:#9aa5b1;font-size:22px;margin:0" title="Add a ${which} reference">+<input type="file" accept="image/*" style="display:none" onchange="refUpload('${which}',this)"></label>`;
      h+=`</div></div>`;
    }
    document.getElementById('refs').innerHTML=h||'<p style="color:#6b7280">No refs on file.</p>';
  };
  window.selRef=function(which,i){
    if(which==='face') window.FACEI=i; else if(which==='body') window.BODYI=i; else if(which==='back') window.BACKI=i; else if(which==='waist') window.WAISTI=i; else window.XFI=i;
    window.renderRefs();
    document.querySelectorAll('[data-asset="1"]').forEach(el=>{
      const k=el.id.slice(3), v=el.dataset.val||'';
      if(which==='face'&&v.startsWith('@face')) setAsset(k,'@face:'+window.FACEI);
      if(which==='body'&&v.startsWith('@body')) setAsset(k,'@body:'+window.BODYI);
      if(which==='back'&&v.startsWith('@back')) setAsset(k,'@back:'+window.BACKI);
      if(which==='waist'&&v.startsWith('@waist')) setAsset(k,'@waist:'+window.WAISTI);
      if(which==='xfanvue'&&v.startsWith('@xfanvue')) setAsset(k,'@xfanvue:'+window.XFI);
    });
  };
  window.refUpload=function(which,inp){
    if(!inp.files.length) return;
    const fd=new FormData(); fd.append('slug',SLUG); fd.append('which',which); fd.append('file',inp.files[0]);
    fetch(ROOT+'/api/ref/upload',{method:'POST',body:fd}).then(r=>r.json()).then(d=>{
      if(d.error){alert(d.error);return;}
      refs[which]=d.count; window.renderRefs();
    });
  };
  window.renderRefs();
  const sel=document.getElementById('toolSel');
  sel.innerHTML=TOOLS.map(t=>`<option value="${t.name}">${t.name} · ${t.price}cr</option>`).join('');
  sel.onchange=()=>loadTool(sel.value);
  const pre=TOOLS.find(t=>t.name==='photoshoot')?'photoshoot':TOOLS[0].name;
  sel.value=pre; loadTool(pre);
  document.getElementById('tplTool').innerHTML='<option value="">All tools</option>'+TOOLS.map(t=>`<option>${t.name}</option>`).join('');
  tplLoad(1);
  refreshJobs(); setInterval(refreshJobs, 6000);
});

let TPLPAGE=1, TPLLIST=[], PENDING_TPL=null;
function tplLoad(p){
  if(p<1)p=1; TPLPAGE=p;
  const q=encodeURIComponent(document.getElementById('tplQ').value||'');
  const tl=encodeURIComponent(document.getElementById('tplTool').value||'');
  fetch(ROOT+'/api/zen/templates?page='+p+'&q='+q+'&tool='+tl).then(r=>r.json()).then(d=>{
    TPLLIST=d.templates||[];
    document.getElementById('tplTotal').textContent='('+(d.total||0)+' presets)';
    document.getElementById('tplPage').textContent='page '+(d.page||1)+' / '+Math.max(1,Math.ceil((d.total||0)/(d.per||24)));
    document.getElementById('tplList').innerHTML=TPLLIST.length?TPLLIST.map((t,i)=>`
      <div style="border:1px solid #262b36;border-radius:8px;padding:10px;display:flex;flex-direction:column">
        <b style="font-size:13px">${t.name}</b>
        <div style="font-size:11px;color:#7aa2f7;margin:3px 0">${t.tool_name}</div>
        <div style="font-size:11px;color:#6b7280;flex:1">${(t.tags||[]).slice(0,5).join(' · ')}</div>
        <button class="ab" style="margin-top:8px" onclick="tplUse(${i})">▶ Load into form</button>
      </div>`).join(''):'<p style="color:#6b7280">No matches.</p>';
  });
}
function tplUse(i){
  const t=TPLLIST[i]; if(!t) return;
  const sel=document.getElementById('toolSel');
  if(![...sel.options].some(o=>o.value===t.tool_name)){ alert('Tool '+t.tool_name+' is not available on this account'); return; }
  PENDING_TPL=t; sel.value=t.tool_name; loadTool(t.tool_name);
  window.scrollTo({top:0,behavior:'smooth'});
}

function loadTool(name){
  TOOL=name;
  const t=TOOLS.find(x=>x.name===name);
  document.getElementById('toolDesc').textContent=(t&&t.description)||'';
  document.getElementById('form').innerHTML='<p style="color:#6b7280">Loading options…</p>';
  fetch(ROOT+'/api/zen/tool/'+name).then(r=>r.json()).then(d=>{
    SCHEMA=d.input_schema||{}; renderForm();
  });
}
function renderForm(){
  const props=SCHEMA.properties||{}, req=SCHEMA.required||[];
  let h='';
  for(const [k,p] of Object.entries(props)){
    const rq=req.includes(k)?'<span class="req">*</span>':'';
    const hint=p.description?`<div class="hint">${String(p.description).slice(0,220)}</div>`:'';
    h+=`<div class="f"><label>${k} ${rq}</label>${fieldHtml(k,p)}${hint}</div>`;
  }
  document.getElementById('form').innerHTML=h||'<p style="color:#6b7280">This tool takes no options.</p>';
  // preselect refs for obvious face/body fields
  for(const k of Object.keys(props)){
    if(/face/.test(k)&&isAsset(k,props[k])) setAsset(k,'@face:'+(window.FACEI||0));
    else if(/body/.test(k)&&isAsset(k,props[k])) setAsset(k,'@body:'+(window.BODYI||0));
  }
  // a template was picked: fill every non-asset field from its preset input
  if(PENDING_TPL&&PENDING_TPL.tool_name===TOOL){
    const inp=PENDING_TPL.input||{};
    for(const [k,v] of Object.entries(inp)){
      const el=document.getElementById('in_'+k); if(!el) continue;
      if(el.dataset&&el.dataset.asset==='1') continue;
      if(el.multiple&&Array.isArray(v)){ [...el.options].forEach(o=>o.selected=v.includes(o.value)); }
      else if(Array.isArray(v)||typeof v==='object'){ el.value=JSON.stringify(v); }
      else{ el.value=String(v); }
    }
    PENDING_TPL=null;
  }
}
function fieldHtml(k,p){
  const t=p.type|| (p.enum?'string':(p.anyOf?'any':'string'));
  if(p.enum) return `<select id="in_${k}">${(p.default===undefined?['<option value="">(default)</option>']:[]).concat(p.enum.map(v=>`<option${v===p.default?' selected':''}>${v}</option>`)).join('')}</select>`;
  if(t==='boolean') return `<select id="in_${k}"><option value="">(default)</option><option value="true"${p.default===true?' selected':''}>true</option><option value="false"${p.default===false?' selected':''}>false</option></select>`;
  if(t==='integer'||t==='number') return `<input id="in_${k}" type="number" ${p.minimum!==undefined?`min="${p.minimum}"`:''} ${p.maximum!==undefined?`max="${p.maximum}"`:''} value="${p.default!==undefined?p.default:''}">`;
  if(t==='array'){
    if(p.items&&p.items.enum) return `<select id="in_${k}" multiple size="4">${p.items.enum.map(v=>`<option>${v}</option>`).join('')}</select>`;
    if(p.items&&isAsset(k,p.items)) return assetPicker(k,true);
    return `<textarea id="in_${k}" placeholder='JSON array e.g. ["a","b"]'></textarea>`;
  }
  if(isAsset(k,p)) return assetPicker(k,false);
  if(k==='prompt'||k==='system_prompt'||(p.description||'').length>120){
    const enh=(/prompt/.test(k)&&!/negative|system/.test(k))?`<button class="ab" style="margin-top:4px" onclick="enhance('${k}');return false">✦ AI-enhance prompt</button>`:'';
    return `<textarea id="in_${k}">${p.default||''}</textarea>${enh}`;
  }
  return `<input id="in_${k}" value="${p.default!==undefined?p.default:''}">`;
}
function assetPicker(k,multi){
  return `<div class="assetbtns" id="in_${k}" data-asset="1" data-multi="${multi?1:0}" data-val="">
    <button class="ab" onclick="setAsset('${k}','@face:'+(window.FACEI||0));return false">Face ref</button>
    <button class="ab" onclick="setAsset('${k}','@body:'+(window.BODYI||0));return false">Body ref</button>
    <button class="ab" onclick="setAsset('${k}','@back:'+(window.BACKI||0));return false">Back ref</button>
    <button class="ab" onclick="setAsset('${k}','@waist:'+(window.WAISTI||0));return false">Waist ref</button>
    <button class="ab" onclick="setAsset('${k}','@xfanvue:'+(window.XFI||0));return false">NSFW ref</button>
    <button class="ab" onclick="pickUpload('${k}');return false">Upload…</button>
    <button class="ab" onclick="setAsset('${k}','');return false">✕ none</button>
    <input type="file" id="up_${k}" style="display:none" accept="image/*" onchange="doUpload('${k}',this)">
    <span id="cur_${k}" style="font-size:12px;color:#7ee2a8;align-self:center"></span></div>`;
}
function setAsset(k,v){
  const el=document.getElementById('in_'+k); if(!el) return;
  el.dataset.val=v;
  document.getElementById('cur_'+k).textContent = v? (v.startsWith('@face')?('✓ face ref '+((+v.split(':')[1]||0)+1)):v.startsWith('@body')?('✓ body ref '+((+v.split(':')[1]||0)+1)):v.startsWith('@back')?('✓ back ref '+((+v.split(':')[1]||0)+1)):v.startsWith('@waist')?('✓ waist ref '+((+v.split(':')[1]||0)+1)):v.startsWith('@xfanvue')?('✓ NSFW ref '+((+v.split(':')[1]||0)+1)):'✓ '+v.slice(0,18)) : '';
  el.querySelectorAll('.ab').forEach(b=>b.classList.remove('on'));
  if(v.startsWith('@face')) el.querySelectorAll('.ab')[0].classList.add('on');
  if(v.startsWith('@body')) el.querySelectorAll('.ab')[1].classList.add('on');
  if(v.startsWith('@back')&&!v.startsWith('@waist')) el.querySelectorAll('.ab')[2].classList.add('on');
  if(v.startsWith('@waist')) el.querySelectorAll('.ab')[3].classList.add('on');
  if(v.startsWith('@xfanvue')) el.querySelectorAll('.ab')[4].classList.add('on');
}
function pickUpload(k){ document.getElementById('up_'+k).click(); }
function enhance(k){
  const el=document.getElementById('in_'+k); if(!el) return;
  const b=event.target; b.textContent='✦ enhancing…'; b.disabled=true;
  fetch(ROOT+'/api/zen/enhance',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({text:el.value,slug:SLUG})})
  .then(r=>r.json()).then(d=>{
    b.textContent='✦ AI-enhance prompt'; b.disabled=false;
    if(d.text) el.value=d.text; else alert(d.error||'enhance failed');
  }).catch(()=>{ b.textContent='✦ AI-enhance prompt'; b.disabled=false; });
}
function retryJob(g){
  fetch(ROOT+'/api/zen/retry',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({gid:g})}).then(r=>r.json()).then(d=>{
    if(d.error) alert(d.error); refreshJobs();
  });
}
function doUpload(k,inp){
  if(!inp.files.length) return;
  const fd=new FormData(); fd.append('file',inp.files[0]);
  document.getElementById('cur_'+k).textContent='uploading…';
  fetch(ROOT+'/api/zen/upload',{method:'POST',body:fd}).then(r=>r.json()).then(d=>{
    if(d.asset_id) setAsset(k,'asset:'+d.asset_id);
    else document.getElementById('cur_'+k).textContent='upload failed';
  });
}
function collect(){
  const props=SCHEMA.properties||{}, req=SCHEMA.required||[], inp={};
  for(const [k,p] of Object.entries(props)){
    const el=document.getElementById('in_'+k); if(!el) continue;
    let v=null;
    if(el.dataset&&el.dataset.asset==='1'){ v=el.dataset.val||null; }
    else if(el.multiple){ v=[...el.selectedOptions].map(o=>o.value); if(!v.length) v=null; }
    else{ v=el.value; if(v==='') v=null; }
    if(v===null){ if(req.includes(k)) throw new Error('Missing required: '+k); continue; }
    const t=p.type;
    if(t==='integer') v=parseInt(v); else if(t==='number') v=parseFloat(v);
    else if(t==='boolean') v=(v==='true');
    else if(t==='array'&&typeof v==='string'){ try{v=JSON.parse(v);}catch(e){throw new Error(k+': bad JSON array');} }
    inp[k]=v;
  }
  return inp;
}
function generate(){
  const msg=document.getElementById('msg'); msg.textContent='';
  let inp; try{ inp=collect(); }catch(e){ msg.textContent=e.message; return; }
  document.getElementById('go').disabled=true;
  fetch(ROOT+'/api/zen/generate',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({slug:SLUG,category:document.getElementById('catSel').value,tool:TOOL,input:inp})})
  .then(r=>r.json()).then(d=>{
    document.getElementById('go').disabled=false;
    if(d.error){ msg.textContent=d.error; return; }
    refreshJobs();
  }).catch(e=>{ document.getElementById('go').disabled=false; msg.textContent='request failed'; });
}
function refreshJobs(){
  fetch(ROOT+'/api/zen/jobs/'+SLUG).then(r=>r.json()).then(d=>{
    const jobs=d.jobs||[];
    if(!jobs.length){ document.getElementById('jobs').innerHTML='<p style="color:#6b7280">No generations yet.</p>'; return; }
    document.getElementById('jobs').innerHTML=jobs.map(j=>{
      const imgs=(j.files||[]).filter(f=>f.idx!==null&&!f.video)
        .map(f=>`<img src="${ROOT}/content_img/${f.idx}" loading="lazy">`).join('');
      const vids=(j.files||[]).filter(f=>f.video)
        .map(f=>`<video controls preload="metadata" style="width:100%;max-height:260px;border-radius:8px;margin-top:6px;background:#000" src="${ROOT}/api/zen/file/${j.gid}/${f.n}"></video>`).join('');
      const rtry=j.status==='failed'?`<button class="ab" style="margin-top:6px" onclick="retryJob('${j.gid}')">↻ Retry</button>`:'';
      return `<div class="jrow">
        <b>${j.tool}</b> → ${j.category.toUpperCase()} <span class="st ${j.status}">${j.status}</span>
        <span style="float:right;font-size:11px;color:#6b7280">${(j.created_at||'').slice(5,16)}</span>
        ${imgs?`<div class="jimgs">${imgs}</div>`:''}${vids}
        ${j.text?`<div class="jtxt">${String(j.text).slice(0,400)}</div>`:''}${rtry}
      </div>`;
    }).join('');
    jobs.filter(j=>['queued','processing','running','unknown'].includes(j.status))
        .forEach(j=>{ if(!POLLING[j.gid]){ POLLING[j.gid]=true; pollJob(j.gid); } });
  });
}
function pollJob(gid){
  fetch(ROOT+'/api/zen/status/'+gid).then(r=>r.json()).then(d=>{
    if(['succeeded','failed'].includes(d.status)){ POLLING[gid]=false; refreshJobs(); }
    else setTimeout(()=>pollJob(gid), 5000);
  }).catch(()=>setTimeout(()=>pollJob(gid), 8000));
}
</script>
'''
