"""Model detail page + Models index. Galleries (SFW/X/Fanvue) with full-size lightbox,
content calendar + post previews (caption/hashtags/platform/time), post composer."""

BODY = r'''
<div id="hdr"></div>
<div id="body"></div>

<div id="lb" onclick="if(event.target.id==='lb')closeLB()">
  <button class="lbnav" id="lbPrev" onclick="navLB(-1)">‹</button>
  <img id="lbImg">
  <button class="lbnav" id="lbNext" onclick="navLB(1)">›</button>
  <div id="lbBar">
    <span id="lbInfo" style="color:#9aa5b1;font-size:13px"></span>
    <button class="libonly" onclick="postFromLB()">➕ Create post / caption</button>
    <button class="ghost libonly" onclick="promoteLB('body')">📌 Use as body ref</button>
    <button class="ghost libonly" onclick="promoteLB('back')">📌 Use as back ref</button>
    <button class="ghost libonly" onclick="promoteLB('waist')">📌 Use as waist ref</button>
    <button class="ghost libonly" onclick="promoteLB('xfanvue')">📌 Use as NSFW ref</button>
    <button class="ghost libonly" onclick="openEditor()">✏️ Edit photo</button>
    <button class="ghost libonly" onclick="openMove()">➡ Move…</button>
    <button class="ghost libonly" onclick="delPhoto()" style="color:#f7a2a2">🗑 Delete</button>
    <button class="ghost refonly" onclick="delRef()" style="color:#f7a2a2;display:none">🗑 Remove this ref</button>
    <button class="ghost" onclick="closeLB()">✕ Close</button>
  </div>
</div>

<div id="ed" style="display:none;position:fixed;inset:0;background:rgba(10,12,16,.94);z-index:70;flex-direction:column;align-items:center;justify-content:center;gap:10px">
  <canvas id="edC" style="max-width:80vw;max-height:58vh;background:#000;cursor:crosshair;border-radius:8px"></canvas>
  <div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:center;align-items:center">
    <button class="mini" onclick="edRot(-90)">&#10226; 90&deg;</button>
    <button class="mini" onclick="edRot(90)">&#10227; 90&deg;</button>
    <button class="mini" onclick="edFlip('h')">&#8651; Flip H</button>
    <button class="mini" onclick="edFlip('v')">&#8645; Flip V</button>
    <button class="mini" id="edCropBtn" onclick="edCropMode()">&#9986; Crop</button>
    <button class="mini" onclick="edReset()">&#8634; Reset</button>
  </div>
  <div style="display:flex;gap:14px;flex-wrap:wrap;justify-content:center;color:#9aa5b1;font-size:12px">
    <label style="margin:0">Brightness <input type="range" id="edB" min="50" max="150" value="100" oninput="edDraw()"></label>
    <label style="margin:0">Contrast <input type="range" id="edK" min="50" max="150" value="100" oninput="edDraw()"></label>
    <label style="margin:0">Saturation <input type="range" id="edS" min="0" max="200" value="100" oninput="edDraw()"></label>
  </div>
  <div style="display:flex;gap:8px">
    <button onclick="edSave('copy')">&#128190; Save as copy</button>
    <button class="ghost" onclick="edSave('overwrite')">Overwrite original</button>
    <button class="ghost" onclick="edClose()">Cancel</button>
  </div>
  <span id="edMsg" style="color:#7ee2a8;font-size:13px"></span>
</div>
<div id="mv" style="display:none;position:fixed;inset:0;background:rgba(10,12,16,.85);z-index:70;align-items:center;justify-content:center">
  <div class="card" style="width:320px">
    <h2 style="margin-top:0">Move photo</h2>
    <label>To model</label><select id="mvSlug"></select>
    <label>Folder</label><select id="mvCat"><option value="sfw">SFW</option><option value="x">X</option><option value="fanvue">Fanvue</option></select>
    <div style="margin-top:12px;display:flex;gap:8px"><button onclick="doMove()">Move</button><button class="ghost" onclick="document.getElementById('mv').style.display='none'">Cancel</button></div>
  </div>
</div>
<div id="cmp" onclick="if(event.target.id==='cmp')closeComposer()">
  <div class="cmpcard">
    <h2 style="margin-top:0" id="cmpTitle">New post</h2>
    <div style="display:flex;gap:14px;flex-wrap:wrap">
      <img id="cmpThumb" style="width:130px;height:165px;object-fit:cover;border-radius:8px;border:1px solid #262b36;background:#0f1115">
      <div style="flex:1;min-width:240px">
        <label>Platform</label><select id="cmpPlat"></select>
        <label>Schedule (date &amp; time)</label><input id="cmpWhen" type="datetime-local">
      </div>
    </div>
    <div id="cmpSlWrap" style="display:none">
      <label>Carousel slides <span style="color:#9aa5b1;font-weight:400;font-size:12px">— click photos to add/remove; the highlighted one is the cover</span></label>
      <div id="cmpSlides" style="display:flex;gap:6px;flex-wrap:wrap;max-height:150px;overflow:auto;padding:4px 0"></div>
    </div>
    <div id="cmpEdWrap" style="display:none">
      <label>Slides <span style="color:#9aa5b1;font-weight:400;font-size:12px">— ★ set cover · ◀ ▶ reorder · ✕ remove</span></label>
      <div id="cmpEdSlides" style="display:flex;gap:8px;flex-wrap:wrap;padding:4px 0"></div>
      <label>Add slides from library <span id="cmpEdTabs"></span></label>
      <div id="cmpEdLib" style="display:flex;gap:6px;flex-wrap:wrap;max-height:130px;overflow:auto;padding:4px 0"></div>
    </div>
    <label>Caption <button class="mini" onclick="aiCaption()">✦ AI caption (3 styles)</button> <span id="cmpMsg" style="color:#9aa5b1;font-size:12px"></span></label>
    <textarea id="cmpCap" style="height:70px"></textarea>
    <div id="capOpts" style="display:none;flex-direction:column;gap:6px;margin:6px 0"></div>
    <label>Hashtags</label>
    <textarea id="cmpTags" style="height:50px" placeholder="#..."></textarea>
    <div style="margin-top:12px;display:flex;gap:8px">
      <button onclick="saveComposer()">Save post</button>
      <button class="ghost" id="cmpDel" onclick="deletePost()" style="display:none">🗑 Delete</button>
      <button class="ghost" onclick="closeComposer()">Cancel</button>
      <span id="cmpErr" style="color:#f7a2a2;font-size:13px;align-self:center"></span>
    </div>
  </div>
</div>

<style>
.mhead{display:flex;gap:20px;align-items:center;flex-wrap:wrap}
.mhead h1{margin:0;font-size:26px}
.geo{color:#9aa5b1;font-size:14px}
.scorebox{margin-left:auto;text-align:right}
.scorebox .s{font-size:30px;font-weight:800;color:#7aa2f7}
.pills span{display:inline-block;background:#222732;color:#9aa5b1;padding:4px 11px;border-radius:14px;font-size:13px;margin:4px 6px 0 0}
.mgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;margin-top:12px}
.mcell{background:#161922;border:1px solid #262b36;border-radius:8px;padding:12px}
.mcell .v{font-size:19px;font-weight:700}
.mcell .k{color:#9aa5b1;font-size:12px;margin-top:2px}
.gtabs{display:flex;gap:8px;margin:14px 0 4px;flex-wrap:wrap}
.gtab{background:#222732;color:#9aa5b1;border:0;padding:7px 15px;border-radius:6px;cursor:pointer;font-weight:600}
.gtab.on{background:#7aa2f7;color:#0f1115}
.gtab.x.on{background:#7ee2a8}
.gtab.fanvue.on{background:#f78ac0}
.gal{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px;margin-top:10px}
.gal img{width:100%;height:180px;object-fit:cover;border-radius:8px;background:#0f1115;border:1px solid #262b36;cursor:zoom-in}
.chnote{border-radius:8px;padding:10px 12px;font-size:13px;margin-top:8px}
.chnote.x{background:#12261d;border:1px solid #285039;color:#7ee2a8}
.chnote.fanvue{background:#2a1b23;border:1px solid #4a2b38;color:#f7a2c0}
.badge{font-size:11px;background:#3a3320;color:#f7d67a;padding:3px 10px;border-radius:12px;margin-left:8px;vertical-align:middle}
.rimg{width:150px;height:190px;object-fit:cover;border-radius:8px;border:1px solid #262b36;background:#0f1115}
.rlbl{font-size:12px;color:#9aa5b1;margin-bottom:4px}
#lb{display:none;position:fixed;inset:0;background:rgba(10,12,16,.94);z-index:50;align-items:center;justify-content:center}
#lb.on{display:flex}
#lbImg{max-width:78vw;max-height:82vh;border-radius:10px;box-shadow:0 8px 40px rgba(0,0,0,.6)}
.lbnav{background:#222732;color:#e6e6e6;border:0;font-size:30px;width:52px;height:52px;border-radius:50%;cursor:pointer;margin:0 18px}
#lbBar{position:fixed;bottom:22px;left:0;right:0;display:flex;gap:12px;justify-content:center;align-items:center}
.ghost{background:#222732;color:#9aa5b1}
#cmp{display:none;position:fixed;inset:0;background:rgba(10,12,16,.8);z-index:60;align-items:center;justify-content:center}
#cmp.on{display:flex}
.cmpcard{background:#161922;border:1px solid #262b36;border-radius:12px;padding:20px;width:560px;max-width:92vw;max-height:88vh;overflow:auto}
.mini{background:#222732;color:#7aa2f7;border:0;padding:2px 9px;border-radius:6px;font-size:12px;cursor:pointer;font-weight:700}
.cal{margin-top:10px}
.calhead{display:flex;align-items:center;gap:12px;margin-bottom:8px}
.calhead b{min-width:150px;text-align:center}
.calgrid{display:grid;grid-template-columns:repeat(7,1fr);gap:4px}
.caldow{color:#6b7280;font-size:11px;text-align:center;padding:2px 0}
.calday{background:#161922;border:1px solid #232836;border-radius:6px;min-height:62px;padding:4px;cursor:pointer;position:relative}
.calday:hover{border-color:#7aa2f7}
.calday.other{opacity:.35}
.calday.today{border-color:#f7c97a}
.calday .dn{font-size:11px;color:#9aa5b1}
.calday .cimgs{display:flex;gap:2px;margin-top:3px;flex-wrap:wrap}
.calday .cimgs img{width:20px;height:24px;object-fit:cover;border-radius:3px}
.calday .more{font-size:10px;color:#7aa2f7}
.pcard{display:flex;gap:12px;background:#161922;border:1px solid #262b36;border-radius:10px;padding:12px;margin-top:10px}
.pcard img{width:86px;height:108px;object-fit:cover;border-radius:8px;cursor:zoom-in}
.pplat{font-size:11px;padding:2px 9px;border-radius:10px;font-weight:700}
.pst{font-size:11px;padding:2px 9px;border-radius:10px;background:#222732;color:#9aa5b1}
.pst.pending_review{background:#3a3320;color:#f7d67a}.pst.approved{background:#1f3d2b;color:#7ee2a8}
.pst.rejected{background:#3d1f1f;color:#f7a2a2}.pst.posted{background:#1f2d3d;color:#7aa2f7}
.pcap{font-size:13px;margin-top:4px;white-space:pre-wrap}
.ptags{font-size:12px;color:#7aa2f7;margin-top:3px;word-break:break-all}
</style>

<script>
const ROOT=(window.ORG_ROOT||'').replace(/\/$/,'');
const SLUG=location.pathname.split('/model/')[1].split('/')[0];
const CATS=[['sfw','SFW'],['x','X'],['fanvue','Fanvue']];
const PLATFORMS=['instagram','tiktok','x','youtube','facebook','reddit','fanvue'];
const PLATC={instagram:'#f7a2c0',tiktok:'#7ae2e2',x:'#7aa2f7',youtube:'#f7a2a2',facebook:'#7aa5f7',reddit:'#f7c97a',fanvue:'#f78ac0'};
const MLABEL={avg_post_views:'Avg post views',profile_views:'Profile views',avg_post_likes:'Avg post likes',
 total_likes:'Profile likes',avg_comments:'Avg comments',followers:'Followers',x_subs:'X subs',
 fanvue_subs:'Fanvue subs',revenue:'Revenue',engagement_rate:'Engagement'};
const MORDER=['revenue','fanvue_subs','x_subs','followers','avg_post_views','profile_views','avg_post_likes','total_likes','avg_comments','engagement_rate'];
function fmt(k,v){ if(v===undefined||v===null) return '—';
  if(k==='revenue') return '$'+Math.round(v).toLocaleString();
  if(k==='engagement_rate') return (+v).toFixed(1)+'%';
  return Math.round(v).toLocaleString(); }

let D=null, GCAT='sfw', POSTS=[], CAL=new Date(), LBCAT='sfw', LBI=0, LBREF=null, EDITID=null, CMPIMG=null, CMPEXTRA=[];

fetch(ROOT+'/api/model/'+SLUG).then(r=>r.json()).then(d=>{
  if(!d||d.error){document.getElementById('hdr').innerHTML='<p style="color:#f7a2a2">Model not found.</p>';return;}
  D=d; renderHead(); renderBody(); loadPosts();
});

function renderHead(){
  const partner=D.partner_name?`<a href="${ROOT}/model/${D.partner_slug}" style="color:#f7a2c0">❤ ${D.partner_name}</a>`:'';
  document.getElementById('hdr').innerHTML=`
   <p style="margin:0 0 10px"><a href="${ROOT}/models">← All models</a></p>
   <div class="card"><div class="mhead">
     <div>
       <h1>${D.name}${D.rank?`<span class="badge">Rank #${D.rank}</span>`:''}</h1>
       <div class="geo">${D.geo||''} ${D.team?('· '+D.team):''} ${partner}</div>
       <div class="pills" style="margin-top:8px">
         ${D.handles.tiktok?`<span>TikTok @${D.handles.tiktok}</span>`:''}
         ${D.handles.instagram?`<span>IG @${D.handles.instagram}</span>`:''}
         ${D.handles.x?`<span>X @${D.handles.x}</span>`:''}
         ${D.handles.fanvue?`<span>Fanvue @${D.handles.fanvue}</span>`:''}
       </div>
     </div>
     <div class="scorebox">
       <div class="s">${(D.score||0).toFixed(1)}</div>
       <div class="geo">overall score</div>
       ${D.agent_id?`<div style="margin-top:8px"><a href="${ROOT}/org">Open agent →</a></div>`:''}
     </div>
   </div></div>`;
}

function renderBody(){
  const m=D.metrics||{};
  const cells=MORDER.filter(k=>k in m).map(k=>
    `<div class="mcell"><div class="v">${fmt(k,m[k])}</div><div class="k">${MLABEL[k]||k}</div></div>`).join('')
    || '<p style="color:#6b7280">No metrics yet.</p>';
  const c=D.counts||{};
  const tabs=CATS.map(([k,lbl])=>
    `<button class="gtab ${k}${k==='sfw'?' on':''}" id="t_${k}" onclick="setG('${k}')">${lbl} · ${c[k]||0}</button>`).join('');
  const refs=D.refs||{};
  const refHtml=(refs.face||refs.body)?`
    <div style="display:flex;gap:12px;flex-wrap:wrap">
      ${Array.from({length:refs.face||0},(_,i)=>`<div><div class="rlbl">Face${i?' '+(i+1):''}</div><img class="rimg" style="cursor:zoom-in" onclick="openRefLB('face',${i})" src="${ROOT}/model/${SLUG}/ref/face/${i}"></div>`).join('')}
      ${Array.from({length:refs.body||0},(_,i)=>`<div><div class="rlbl">Body${i?' '+(i+1):''}</div><img class="rimg" style="cursor:zoom-in" onclick="openRefLB('body',${i})" src="${ROOT}/model/${SLUG}/ref/body/${i}"></div>`).join('')}
      ${Array.from({length:refs.back||0},(_,i)=>`<div><div class="rlbl">Back${i?' '+(i+1):''}</div><img class="rimg" style="cursor:zoom-in" onclick="openRefLB('back',${i})" src="${ROOT}/model/${SLUG}/ref/back/${i}"></div>`).join('')}
      ${Array.from({length:refs.waist||0},(_,i)=>`<div><div class="rlbl">Waist-up${i?' '+(i+1):''}</div><img class="rimg" style="cursor:zoom-in" onclick="openRefLB('waist',${i})" src="${ROOT}/model/${SLUG}/ref/waist/${i}"></div>`).join('')}
      <div style="display:flex;flex-direction:column;gap:6px;justify-content:center">
        <button class="mini" onclick="refUpl('face')">+ face ref</button>
        <button class="mini" onclick="refUpl('body')">+ body ref</button>
        <button class="mini" onclick="refUpl('back')">+ back ref</button>
        <button class="mini" onclick="refUpl('waist')">+ waist ref</button>
        <input type="file" id="refFile" accept="image/*" style="display:none" onchange="refUplGo(this)">
      </div>
    </div>`:'<p style="color:#6b7280">No reference photos on file.</p>';
  const nsfwHtml=`
    <div style="display:flex;gap:12px;flex-wrap:wrap;align-items:flex-start">
      ${Array.from({length:refs.xfanvue||0},(_,i)=>`<div><div class="rlbl">NSFW${i?' '+(i+1):''}</div><img class="rimg" style="cursor:zoom-in" onclick="openRefLB('xfanvue',${i})" src="${ROOT}/model/${SLUG}/ref/xfanvue/${i}"></div>`).join('')||'<p style="color:#6b7280;margin:4px 0">No NSFW reference photos yet — upload the ones you generate (e.g. with Grok).</p>'}
      <div style="display:flex;align-items:center"><button class="mini" style="background:#4a2b38;color:#f78ac0" onclick="refUpl('xfanvue')">+ NSFW ref</button></div>
    </div>`;
  document.getElementById('body').innerHTML=`
    <h2>Metrics ${D.sample===false?'<span style="font-size:11px;background:#1f3d2b;color:#7ee2a8;padding:3px 10px;border-radius:12px;margin-left:8px;vertical-align:middle">live</span>':'<span class="badge">sample</span>'}</h2>
    <div class="mgrid">${cells}</div>
    <h2>Reference photos <span style="font-size:12px;color:#6b7280;font-weight:400">— identity refs ZenCreator uses to keep ${D.name} consistent</span></h2>
    <div class="card">${refHtml}
      <div style="margin-top:12px"><a href="${ROOT}/studio/${SLUG}"><button>✦ Create content with ZenCreator</button></a></div>
    </div>
    <h2 style="color:#f78ac0">NSFW reference photos <span style="font-size:12px;color:#6b7280;font-weight:400">— identity refs for X subscriber &amp; Fanvue content only, never IG/TikTok</span></h2>
    <div class="card" style="border:1px solid #4a2b38">${nsfwHtml}</div>
    <h2>Content library <span style="font-size:12px;color:#6b7280;font-weight:400">— click a photo to view full size</span></h2>
    <div class="gtabs">${tabs}
      <button class="gtab" style="margin-left:auto;background:#1f3d2b;color:#7ee2a8" onclick="photoUpl()">⬆ Add photos to this folder</button>
      <input type="file" id="phFile" accept="image/*" multiple style="display:none" onchange="photoUplGo(this)">
    </div>
    <div id="gal"></div>
    <h2>Content calendar</h2>
    <div class="card cal">
      <div class="calhead">
        <button class="ghost" onclick="calNav(-1)">‹</button><b id="calTitle"></b><button class="ghost" onclick="calNav(1)">›</button>
        <span style="color:#6b7280;font-size:12px">click a day to schedule a post</span>
      </div>
      <div class="calgrid" id="calGrid"></div>
    </div>
    <h2>Scheduled &amp; drafted posts <span id="pcount" class="badge"></span></h2>
    <div id="plist"><p style="color:#6b7280">No posts yet — click a day on the calendar or a photo in the library to create one.</p></div>`;
  setG('sfw');
}

function setG(which){
  GCAT=which;
  CATS.forEach(([k])=>document.getElementById('t_'+k).classList.toggle('on',k===which));
  const box=document.getElementById('gal');
  const n=(D.counts||{})[which]||0;
  if(!n){ box.innerHTML='<p style="color:#6b7280">No '+which.toUpperCase()+' images tagged yet. Use the <a href="'+ROOT+'/tag">Tag</a> page or the <a href="'+ROOT+'/studio/'+SLUG+'">Studio</a>.</p>'; return; }
  let note='';
  if(which==='x') note='<div class="chnote x">X subscriber content.</div>';
  if(which==='fanvue') note='<div class="chnote fanvue">Adult content — for Fanvue. Publishing is handled on your side, not from here.</div>';
  let imgs='';
  for(let i=0;i<n;i++){
    imgs+=`<img loading="lazy" src="${ROOT}/model/${SLUG}/${which}/${i}" onclick="openLB('${which}',${i})" onerror="this.style.display='none'">`;
  }
  box.innerHTML=note+'<div class="gal">'+imgs+'</div>';
}

/* ---------- lightbox ---------- */
function openLB(cat,i){ LBREF=null; LBCAT=cat; LBI=i; updLB(); document.getElementById('lb').classList.add('on'); }
function openRefLB(w,i){ LBREF={w:w,i:i}; updLB(); document.getElementById('lb').classList.add('on'); }
function updLB(){
  const ref=!!LBREF;
  document.querySelectorAll('#lbBar .libonly').forEach(b=>b.style.display=ref?'none':'');
  document.querySelectorAll('#lbBar .refonly').forEach(b=>b.style.display=ref?'':'none');
  if(ref){
    const labels={face:'Face',body:'Body',back:'Back',waist:'Waist-up',xfanvue:'NSFW'};
    const n=(D.refs||{})[LBREF.w]||0;
    document.getElementById('lbImg').src=ROOT+'/model/'+SLUG+'/ref/'+LBREF.w+'/'+LBREF.i;
    document.getElementById('lbInfo').textContent=D.name+' · '+(labels[LBREF.w]||LBREF.w)+' ref · '+(LBREF.i+1)+' / '+n;
    document.getElementById('lbPrev').style.visibility=LBREF.i>0?'visible':'hidden';
    document.getElementById('lbNext').style.visibility=LBREF.i<n-1?'visible':'hidden';
    return;
  }
  const n=(D.counts||{})[LBCAT]||0;
  document.getElementById('lbImg').src=ROOT+'/model/'+SLUG+'/'+LBCAT+'/'+LBI;
  document.getElementById('lbInfo').textContent=D.name+' · '+LBCAT.toUpperCase()+' · '+(LBI+1)+' / '+n;
  document.getElementById('lbPrev').style.visibility=LBI>0?'visible':'hidden';
  document.getElementById('lbNext').style.visibility=LBI<n-1?'visible':'hidden';
}
function navLB(d){
  if(LBREF){ const n=(D.refs||{})[LBREF.w]||0; LBREF.i=Math.min(n-1,Math.max(0,LBREF.i+d)); updLB(); return; }
  const n=(D.counts||{})[LBCAT]||0; LBI=Math.min(n-1,Math.max(0,LBI+d)); updLB(); }
function closeLB(){ LBREF=null; document.getElementById('lb').classList.remove('on'); }
function delRef(){
  if(!LBREF) return;
  if(!confirm('Remove this reference photo? ZenCreator will stop using it for '+D.name+'.')) return;
  fetch(ROOT+'/api/ref/delete',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({slug:SLUG,which:LBREF.w,i:LBREF.i})})
    .then(r=>r.json()).then(d=>{ if(d.error){alert(d.error);return;} location.reload(); });
}
document.addEventListener('keydown',e=>{
  if(document.getElementById('lb').classList.contains('on')){
    if(e.key==='Escape')closeLB(); if(e.key==='ArrowLeft')navLB(-1); if(e.key==='ArrowRight')navLB(1);
  } else if(document.getElementById('cmp').classList.contains('on')&&e.key==='Escape') closeComposer();
});
function postFromLB(){ closeLB(); openComposer(null,{category:LBCAT,idx:LBI}); }
function photoUpl(){ document.getElementById('phFile').click(); }
function photoUplGo(inp){
  if(!inp.files.length) return;
  const fd=new FormData(); fd.append('slug',SLUG); fd.append('category',GCAT);
  [...inp.files].forEach(f=>fd.append('file',f));
  fetch(ROOT+'/api/photo/upload',{method:'POST',body:fd}).then(r=>r.json()).then(d=>{
    if(d.error){alert(d.error);return;} location.reload();
  });
}
let REFW='body';
function refUpl(w){ REFW=w; document.getElementById('refFile').click(); }
function refUplGo(inp){
  if(!inp.files.length) return;
  const fd=new FormData(); fd.append('slug',SLUG); fd.append('which',REFW); fd.append('file',inp.files[0]);
  fetch(ROOT+'/api/ref/upload',{method:'POST',body:fd}).then(r=>r.json()).then(d=>{
    if(d.error){alert(d.error);return;} location.reload();
  });
}
function promoteLB(w){
  w=w||'body';
  fetch(ROOT+'/api/ref/promote',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({slug:SLUG,which:w,category:LBCAT,idx:LBI})})
    .then(r=>r.json()).then(d=>{ alert(d.error?('Failed: '+d.error):('Added as '+w+' ref #'+d.count+' — it will show in the Studio ref picker.')); });
}
/* ---------- photo editor ---------- */
let EDimg=null, EDrot=0, EDfh=1, EDfv=1, EDcrop=null, EDcropping=false, EDdrag=null;
function edV(id){return document.getElementById(id).value;}
function openEditor(){
  EDimg=new Image();
  EDimg.onload=()=>{ EDrot=0;EDfh=1;EDfv=1;EDcrop=null;EDcropping=false;EDdrag=null;
    ['edB','edK','edS'].forEach(i=>document.getElementById(i).value=100);
    document.getElementById('edCropBtn').textContent='✂ Crop';
    document.getElementById('edMsg').textContent='';
    edDraw(); document.getElementById('ed').style.display='flex'; };
  EDimg.src=ROOT+'/model/'+SLUG+'/'+LBCAT+'/'+LBI+'?e='+Date.now();
}
function edDraw(){
  const c=document.getElementById('edC'),x=c.getContext('2d');
  const src=EDcrop||{x:0,y:0,w:EDimg.width,h:EDimg.height};
  const r=((EDrot%360)+360)%360, rot90=(r===90||r===270);
  c.width=rot90?src.h:src.w; c.height=rot90?src.w:src.h;
  x.save();
  x.filter='brightness('+edV('edB')+'%) contrast('+edV('edK')+'%) saturate('+edV('edS')+'%)';
  x.translate(c.width/2,c.height/2); x.rotate(r*Math.PI/180); x.scale(EDfh,EDfv);
  x.drawImage(EDimg,src.x,src.y,src.w,src.h,-src.w/2,-src.h/2,src.w,src.h);
  x.restore();
  if(EDdrag){ x.strokeStyle='#7aa2f7'; x.lineWidth=Math.max(2,c.width/300); x.setLineDash([8,6]);
    x.strokeRect(EDdrag.x,EDdrag.y,EDdrag.w,EDdrag.h); x.setLineDash([]); }
}
function edRot(d){ if(EDcropping)return; EDrot+=d; edDraw(); }
function edFlip(w){ if(EDcropping)return; if(w==='h')EDfh*=-1; else EDfv*=-1; edDraw(); }
function edReset(){ EDrot=0;EDfh=1;EDfv=1;EDcrop=null;EDcropping=false;EDdrag=null;
  ['edB','edK','edS'].forEach(i=>document.getElementById(i).value=100);
  document.getElementById('edCropBtn').textContent='✂ Crop'; edDraw(); }
function edCropMode(){
  if(EDcropping){
    if(EDdrag&&Math.abs(EDdrag.w)>10&&Math.abs(EDdrag.h)>10){
      const base=EDcrop||{x:0,y:0};
      EDcrop={x:base.x+Math.min(EDdrag.x,EDdrag.x+EDdrag.w),y:base.y+Math.min(EDdrag.y,EDdrag.y+EDdrag.h),
              w:Math.abs(EDdrag.w),h:Math.abs(EDdrag.h)};
    }
    EDcropping=false; EDdrag=null; document.getElementById('edCropBtn').textContent='✂ Crop'; edDraw(); return;
  }
  EDrot=0;EDfh=1;EDfv=1; EDcropping=true; EDdrag=null;
  document.getElementById('edCropBtn').textContent='✔ Apply crop'; edDraw();
}
(function(){
  const c=document.getElementById('edC'); let down=false;
  function pos(e){ const r=c.getBoundingClientRect();
    return [(e.clientX-r.left)*c.width/r.width,(e.clientY-r.top)*c.height/r.height]; }
  c.addEventListener('mousedown',e=>{ if(!EDcropping)return; down=true; const p=pos(e); EDdrag={x:p[0],y:p[1],w:0,h:0}; e.preventDefault(); });
  c.addEventListener('mousemove',e=>{ if(!EDcropping||!down)return; const p=pos(e); EDdrag.w=p[0]-EDdrag.x; EDdrag.h=p[1]-EDdrag.y; edDraw(); });
  window.addEventListener('mouseup',()=>{ down=false; });
})();
function edClose(){ document.getElementById('ed').style.display='none'; }
function edSave(mode){
  document.getElementById('edMsg').textContent='saving…';
  EDdrag=null; edDraw();
  document.getElementById('edC').toBlob(b=>{
    const fd=new FormData(); fd.append('slug',SLUG); fd.append('category',LBCAT); fd.append('idx',LBI);
    fd.append('mode',mode); fd.append('file',b,'edit.png');
    fetch(ROOT+'/api/photo/save_edit',{method:'POST',body:fd}).then(r=>r.json()).then(d2=>{
      if(d2.error){document.getElementById('edMsg').textContent='failed: '+d2.error;return;}
      location.reload();
    });
  },'image/png');
}
function openMove(){
  fetch(ROOT+'/api/board').then(r=>r.json()).then(d=>{
    document.getElementById('mvSlug').innerHTML=d.personas.map(p=>'<option value="'+p.slug+'"'+(p.slug===SLUG?' selected':'')+'>'+p.name+'</option>').join('');
    document.getElementById('mvCat').value=LBCAT;
    document.getElementById('mv').style.display='flex';
  });
}
function doMove(){
  fetch(ROOT+'/api/photo/move',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({slug:SLUG,category:LBCAT,idx:LBI,to_slug:document.getElementById('mvSlug').value,to_category:document.getElementById('mvCat').value})})
    .then(r=>r.json()).then(d=>{ if(d.error){alert(d.error);return;} location.reload(); });
}
function delPhoto(){
  if(!confirm('Delete this photo permanently? It will be removed from the library and from disk.')) return;
  fetch(ROOT+'/api/photo/delete',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({slug:SLUG,category:LBCAT,idx:LBI})})
    .then(r=>r.json()).then(d=>{ if(d.error){alert(d.error);return;} location.reload(); });
}

/* ---------- posts ---------- */
function loadPosts(){
  fetch(ROOT+'/api/posts/'+SLUG).then(r=>r.json()).then(d=>{
    POSTS=d.posts||[]; renderCal(); renderPosts();
  });
}
function renderPosts(){
  document.getElementById('pcount').textContent=POSTS.length+' total';
  if(!POSTS.length){ document.getElementById('plist').innerHTML='<p style="color:#6b7280">No posts yet — click a day on the calendar or a photo in the library to create one.</p>'; return; }
  document.getElementById('plist').innerHTML=POSTS.map(p=>{
    const c=PLATC[p.platform]||'#9aa5b1';
    const idxs=(p.img_idxs&&p.img_idxs.length)?p.img_idxs:(p.img_idx!==null?[p.img_idx]:[]);
    const img=idxs.length?`<div style="display:flex;flex-direction:column;gap:3px"><img src="${ROOT}/content_img/${idxs[0]}" onclick="lbFromPost(${idxs[0]})">${idxs.length>1?`<span style="font-size:11px;color:#7aa2f7;text-align:center">🖼 ${idxs.length} slides</span>`:''}</div>`:'';
    return `<div class="pcard">
      ${img}
      <div style="flex:1">
        <span class="pplat" style="background:${c}22;color:${c}">${p.platform}</span>
        <span class="pst ${p.status}">${p.status.replace('_',' ')}</span>
        <span style="color:#9aa5b1;font-size:12px;margin-left:6px">${p.slot_time?('📅 '+p.slot_time):'unscheduled'}</span>
        <button class="mini" style="float:right" onclick='editPost(${JSON.stringify(p).replace(/'/g,"&#39;")})'>✎ Edit</button>
        <div class="pcap">${(p.caption||'<span style=color:#6b7280>no caption yet</span>')}</div>
        <div class="ptags">${p.hashtags||''}</div>
        ${p.review_notes?`<div style="font-size:12px;color:#f7c97a;margin-top:3px">📝 ${p.review_notes}</div>`:''}
      </div>
    </div>`;
  }).join('');
}
function lbFromPost(idx){ window.open(ROOT+'/content_img/'+idx,'_blank'); }

/* ---------- calendar ---------- */
function calNav(d){ CAL=new Date(CAL.getFullYear(),CAL.getMonth()+d,1); renderCal(); }
function renderCal(){
  const y=CAL.getFullYear(),m=CAL.getMonth();
  document.getElementById('calTitle').textContent=CAL.toLocaleString('en',{month:'long',year:'numeric'});
  const first=new Date(y,m,1), startDow=(first.getDay()+6)%7;
  const dim=new Date(y,m+1,0).getDate();
  const today=new Date(); const tstr=today.toISOString().slice(0,10);
  const byDay={};
  POSTS.forEach(p=>{ const d=(p.slot_time||'').slice(0,10); if(d){ (byDay[d]=byDay[d]||[]).push(p); } });
  let h=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'].map(d=>`<div class="caldow">${d}</div>`).join('');
  for(let i=0;i<startDow;i++) h+='<div class="calday other"></div>';
  for(let d=1;d<=dim;d++){
    const ds=`${y}-${String(m+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
    const list=byDay[ds]||[];
    const thumbs=list.slice(0,3).map(p=>p.img_idx!==null?`<img src="${ROOT}/content_img/${p.img_idx}">`:'').join('');
    const more=list.length>3?`<span class="more">+${list.length-3}</span>`:'';
    h+=`<div class="calday${ds===tstr?' today':''}" onclick="openComposer(null,null,'${ds}')">
      <div class="dn">${d}</div><div class="cimgs">${thumbs}${more}</div></div>`;
  }
  document.getElementById('calGrid').innerHTML=h;
}

/* ---------- composer ---------- */
function openComposer(post,img,dateStr){
  EDITID=post?post.id:null; CMPIMG=img||null;
  document.getElementById('cmpTitle').textContent=post?'Edit post':'New post';
  document.getElementById('cmpDel').style.display=post?'inline-block':'none';
  document.getElementById('cmpPlat').innerHTML=PLATFORMS.map(p=>`<option${post&&post.platform===p?' selected':''}>${p}</option>`).join('');
  document.getElementById('cmpCap').value=post?post.caption:'';
  document.getElementById('cmpTags').value=post?post.hashtags:'';
  document.getElementById('cmpErr').textContent=''; document.getElementById('cmpMsg').textContent='';
  let when=post?(post.slot_time||''):(dateStr?dateStr+' 18:00':'');
  document.getElementById('cmpWhen').value=when?when.replace(' ','T'):'';
  const th=document.getElementById('cmpThumb');
  if(post&&post.img_idx!==null) th.src=ROOT+'/content_img/'+post.img_idx;
  else if(img) th.src=ROOT+'/model/'+SLUG+'/'+img.category+'/'+img.idx;
  else th.removeAttribute('src');
  if(!post&&!img){ document.getElementById('cmpMsg').textContent='pick photos below ⬇'; }
  document.getElementById('capOpts').style.display='none';
  document.getElementById('capOpts').innerHTML='';
  const needPicker=!!post||(!post&&!img);
  document.getElementById('cmpEdWrap').style.display=needPicker?'block':'none';
  if(needPicker){
    EDITSLIDES=post?((post.img_idxs&&post.img_idxs.length)?post.img_idxs.slice():(post.img_idx!==null&&post.img_idx!==undefined?[post.img_idx]:[])):[];
    renderEdSlides(); loadEdLib('sfw');
  }
  buildSlides(post,img);
  document.getElementById('cmp').classList.add('on');
}
let EDITSLIDES=[], EDLIBCAT='sfw';
function renderEdSlides(){
  const g=document.getElementById('cmpEdSlides');
  g.innerHTML=EDITSLIDES.map((gi,n)=>`
    <div style="display:flex;flex-direction:column;align-items:center;gap:2px">
      <img src="${ROOT}/content_img/${gi}" style="width:60px;height:76px;object-fit:cover;border-radius:6px;border:2px solid ${n===0?'#7aa2f7':'#262b36'}">
      <div style="font-size:10px;color:${n===0?'#7aa2f7':'#6b7280'}">${n===0?'cover':'slide '+(n+1)}</div>
      <div style="display:flex;gap:2px">
        ${n>0?`<button class="mini" onclick="edSlMove(${n},-1)">◀</button>`:''}
        ${n<EDITSLIDES.length-1?`<button class="mini" onclick="edSlMove(${n},1)">▶</button>`:''}
        ${n>0?`<button class="mini" title="make cover" onclick="edSlCover(${n})">★</button>`:''}
        ${EDITSLIDES.length>1?`<button class="mini" style="color:#f7a2a2" onclick="edSlDel(${n})">✕</button>`:''}
      </div>
    </div>`).join('')||'<span style="color:#f7a2a2;font-size:12px">no photos — add one below</span>';
  const th=document.getElementById('cmpThumb');
  if(EDITSLIDES.length) th.src=ROOT+'/content_img/'+EDITSLIDES[0];
}
function edSlMove(n,d){ const t=EDITSLIDES[n]; EDITSLIDES[n]=EDITSLIDES[n+d]; EDITSLIDES[n+d]=t; renderEdSlides(); }
function edSlCover(n){ const t=EDITSLIDES.splice(n,1)[0]; EDITSLIDES.unshift(t); renderEdSlides(); }
function edSlDel(n){ EDITSLIDES.splice(n,1); renderEdSlides(); loadEdLib(EDLIBCAT); }
function loadEdLib(cat){
  EDLIBCAT=cat;
  document.getElementById('cmpEdTabs').innerHTML=CATS.map(([k,l])=>`<button class="mini" style="margin-left:6px;${k===cat?'background:#7aa2f7;color:#0f1115':''}" onclick="loadEdLib('${k}')">${l}</button>`).join('');
  fetch(ROOT+'/api/lib_idxs/'+SLUG+'/'+cat).then(r=>r.json()).then(d=>{
    const idxs=(d.idxs||[]).filter(i=>i!==null&&i!==undefined);
    document.getElementById('cmpEdLib').innerHTML=idxs.length?idxs.map(gi=>`<img src="${ROOT}/content_img/${gi}" style="width:46px;height:58px;object-fit:cover;border-radius:5px;cursor:pointer;border:2px solid ${EDITSLIDES.includes(gi)?'#7ee2a8':'#262b36'}" onclick="edSlAdd(${gi})">`).join(''):'<span style="color:#6b7280;font-size:12px">no photos in this folder</span>';
  });
}
function edSlAdd(gi){
  const at=EDITSLIDES.indexOf(gi);
  if(at>=0){ if(EDITSLIDES.length>1) EDITSLIDES.splice(at,1); }
  else EDITSLIDES.push(gi);
  renderEdSlides(); loadEdLib(EDLIBCAT);
}
function buildSlides(post,img){
  CMPEXTRA=[];
  const wrap=document.getElementById('cmpSlWrap'), grid=document.getElementById('cmpSlides');
  grid.innerHTML='';
  if(post){ wrap.style.display='none'; return; }
  if(!img){ wrap.style.display='none'; return; }
  const n=(D.counts||{})[img.category]||0;
  if(n<2){ wrap.style.display='none'; return; }
  wrap.style.display='block';
  for(let i=0;i<n;i++){
    const el=document.createElement('img');
    el.src=ROOT+'/model/'+SLUG+'/'+img.category+'/'+i;
    el.style.cssText='width:52px;height:66px;object-fit:cover;border-radius:6px;cursor:pointer;border:2px solid '+(i===img.idx?'#7aa2f7':'#262b36');
    if(i===img.idx){ el.title='cover photo'; }
    else{
      el.onclick=()=>{
        const at=CMPEXTRA.indexOf(i);
        if(at>=0){ CMPEXTRA.splice(at,1); el.style.borderColor='#262b36'; }
        else{ CMPEXTRA.push(i); el.style.borderColor='#7ee2a8'; }
        document.getElementById('cmpMsg').textContent=CMPEXTRA.length?('carousel: '+(CMPEXTRA.length+1)+' slides'):'';
      };
    }
    grid.appendChild(el);
  }
}
function editPost(p){ openComposer(p,null); }
function closeComposer(){ document.getElementById('cmp').classList.remove('on'); }
function saveComposer(){
  const when=(document.getElementById('cmpWhen').value||'').replace('T',' ');
  const body={platform:document.getElementById('cmpPlat').value,
    caption:document.getElementById('cmpCap').value, hashtags:document.getElementById('cmpTags').value,
    slot_time:when};
  if(EDITID){
    body.id=EDITID;
    const doUpdate=()=>fetch(ROOT+'/api/post/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})
      .then(r=>r.json()).then(d=>{
        if(d.error){ document.getElementById('cmpErr').textContent=d.error; return; }
        closeComposer(); loadPosts();
      });
    if(EDITSLIDES.length){
      fetch(ROOT+'/api/post/set_slides',{method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({id:EDITID,idxs:EDITSLIDES})})
        .then(r=>r.json()).then(d=>{
          if(d.error){ document.getElementById('cmpErr').textContent=d.error; return; }
          doUpdate();
        });
    } else doUpdate();
    return;
  }
  if(!CMPIMG){
    if(!EDITSLIDES.length){ document.getElementById('cmpErr').textContent='Add at least one photo below.'; return; }
    body.slug=SLUG; body.idxs=EDITSLIDES;
    fetch(ROOT+'/api/post/create_global',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})
      .then(r=>r.json()).then(d=>{
        if(d.error){ document.getElementById('cmpErr').textContent=d.error; return; }
        closeComposer(); loadPosts();
      });
    return;
  }
  body.slug=SLUG; body.category=CMPIMG.category; body.idx=CMPIMG.idx; body.extra_idxs=CMPEXTRA;
  fetch(ROOT+'/api/post/create',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})
    .then(r=>r.json()).then(d=>{
      if(d.error){ document.getElementById('cmpErr').textContent=d.error; return; }
      closeComposer(); loadPosts();
    });
}
function deletePost(){
  if(!EDITID) return;
  if(!confirm('Delete this post?')) return;
  fetch(ROOT+'/api/post/delete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:EDITID})})
    .then(r=>r.json()).then(()=>{ closeComposer(); loadPosts(); });
}
function aiCaption(){
  document.getElementById('cmpMsg').textContent='writing 3 styles…';
  const esc=s=>String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;');
  const opts=document.getElementById('capOpts'); opts.style.display='none'; opts.innerHTML='';
  fetch(ROOT+'/api/post/gen_captions3',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({slug:SLUG,platform:document.getElementById('cmpPlat').value,
      hint:document.getElementById('cmpCap').value})})
    .then(r=>r.json()).then(d=>{
      if(d.error||!(d.options||[]).length){ document.getElementById('cmpMsg').textContent='failed: '+(d.error||'no output'); return; }
      document.getElementById('cmpMsg').textContent='✓ pick a style';
      window.CAPOPTS=d.options;
      opts.style.display='flex';
      opts.innerHTML=d.options.map((o,i)=>`
        <div onclick="useCap(${i})" style="border:1px solid #333a48;border-radius:8px;padding:8px 10px;cursor:pointer" onmouseover="this.style.borderColor='#7aa2f7'" onmouseout="this.style.borderColor='#333a48'">
          <b style="font-size:12px;color:#7aa2f7">${esc(o.style)}</b>
          <div style="font-size:13px;margin-top:2px">${esc(o.caption)}</div>
          <div style="font-size:11px;color:#6b7280;margin-top:2px">${esc((o.hashtags||'').slice(0,140))}</div>
        </div>`).join('');
    }).catch(()=>{ document.getElementById('cmpMsg').textContent='request failed'; });
}
function useCap(i){
  const o=(window.CAPOPTS||[])[i]; if(!o) return;
  document.getElementById('cmpCap').value=o.caption;
  if(o.hashtags) document.getElementById('cmpTags').value=o.hashtags;
  document.getElementById('capOpts').style.display='none';
  document.getElementById('cmpMsg').textContent='✓ '+o.style+' style';
}
</script>
'''


INDEX = r'''
<h1>Models</h1>
<p style="color:#9aa5b1;margin-top:-4px">Every persona in the roster. Click a card to open that model's full profile — bio, handles, metrics, and content library.</p>
<div id="grid" class="mgrid2"></div>
<style>
.mgrid2{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px;margin-top:14px}
.mcard{background:#161922;border:1px solid #262b36;border-radius:12px;overflow:hidden;cursor:pointer;transition:border-color .15s}
.mcard:hover{border-color:#7aa2f7}
.mcard .thumb{height:180px;background:#0f1115 center/cover no-repeat;display:flex;align-items:center;justify-content:center;color:#3b414d;font-size:13px}
.mcard .body{padding:12px 14px}
.mcard .nm{font-size:17px;font-weight:700}
.mcard .sub{color:#9aa5b1;font-size:12px;margin-top:2px}
.mcard .row{display:flex;justify-content:space-between;align-items:center;margin-top:10px}
.mcard .sc{font-size:20px;font-weight:800;color:#7aa2f7}
.rk{font-size:11px;background:#222732;color:#f7d67a;padding:2px 9px;border-radius:10px}
.hb{color:#f7a2c0;font-size:12px}
</style>
<script>
const ROOT = (window.ORG_ROOT||'').replace(/\/$/,'');
fetch(ROOT+'/api/board').then(r=>r.json()).then(d=>{
  const grid=document.getElementById('grid'); grid.innerHTML='';
  const rows=d.personas.slice().sort((a,b)=>a.rank-b.rank);
  rows.forEach(p=>{
    const thumb=ROOT+'/model/'+p.slug+'/sfw/0';
    const el=document.createElement('div'); el.className='mcard';
    el.onclick=()=>location.href=ROOT+'/model/'+p.slug;
    el.innerHTML=`
      <div class="thumb" style="background-image:url('${thumb}')" data-slug="${p.slug}">no photo tagged</div>
      <div class="body">
        <div style="display:flex;justify-content:space-between;align-items:flex-start">
          <div><div class="nm">${p.name}</div><div class="sub">${p.geo||''} · ${p.team||''}</div></div>
          <span class="rk">#${p.rank}</span>
        </div>
        <div class="row"><span class="hb">${p.partner_name?('❤ '+p.partner_name):''}</span><span class="sc">${p.score.toFixed(1)}</span></div>
      </div>`;
    grid.appendChild(el);
    const img=new Image();
    img.onload=()=>{const t=el.querySelector('.thumb'); if(t)t.textContent='';};
    img.src=thumb;
  });
});
</script>
'''
