"""Approvals queue — cross-model review of planned posts before they go out.

Views: list, day, week, month calendar. Filters by model, platform, and content
section (Social / X / Fanvue). Managers can fully edit a post inline: caption
(incl. 3-style AI rewrite), hashtags, platform, schedule, and the photos
themselves (swap from the library or generate new ones in ZenCreator)."""

BODY = r'''
<h1>Approvals</h1>
<p style="color:#9aa5b1">Every planned post lands here as <b>pending review</b>. Nothing publishes
until it is approved here &mdash; and live posting stays off until go-live.</p>

<div class="card" style="display:flex;gap:14px;align-items:center;flex-wrap:wrap">
  <b>Live posting</b>
  <span id="glState" class="stb" style="background:#2a2f3a;color:#9aa5b1">checking…</span>
  <button id="glBtn" onclick="toggleGL()" style="display:none"></button>
  <span style="color:#6b7280;font-size:12px">When ON, approved posts publish at their scheduled time. Fanvue publishes through its own service.</span>
</div>

<div class="sectabs" id="sectabs"></div>

<div class="card" style="display:flex;gap:16px;align-items:center;flex-wrap:wrap;padding:12px 16px">
  <div><label class="flbl">Model</label><select id="fModel" onchange="render()"></select></div>
  <div><label class="flbl">Platform</label><select id="fPlat" onchange="render()"></select></div>
  <div><label class="flbl">Status</label><select id="fStat" onchange="render()">
    <option value="pending_review">Pending review</option>
    <option value="upcoming">Pending + approved</option>
    <option value="all">Everything</option>
  </select></div>
  <div><label class="flbl">View</label>
    <div class="viewbtns" id="viewbtns"></div>
  </div>
  <div id="datenav" style="display:none;align-items:center;gap:8px">
    <button class="bU" onclick="navDate(-1)">&#8249;</button>
    <b id="dateLabel" style="min-width:190px;text-align:center;display:inline-block"></b>
    <button class="bU" onclick="navDate(1)">&#8250;</button>
    <button class="bU" onclick="goToday()">Today</button>
  </div>
  <div style="margin-left:auto;display:flex;gap:8px;align-items:center">
    <span id="shownCount" style="color:#6b7280;font-size:12px"></span>
    <button class="bA" id="bulkBtn" onclick="approveAllShown()" style="display:none">&#10003; Approve all shown</button>
  </div>
</div>

<div id="calWrap" style="display:none"></div>

<div id="listWrap">
  <h2 style="margin-top:18px">Pending review <span id="pcount" class="cnt"></span></h2>
  <div id="pending" class="apgrid"></div>
  <h2 style="margin-top:26px">Recently decided</h2>
  <div id="decided" class="apgrid"></div>
</div>

<div id="ed" onclick="if(event.target.id==='ed')closeEd()">
  <div class="edcard">
    <h2 style="margin-top:0" id="edTitle">Edit post</h2>
    <div style="display:flex;gap:14px;flex-wrap:wrap">
      <div style="flex:1;min-width:230px">
        <label>Platform</label><select id="edPlat"></select>
      </div>
      <div style="flex:1;min-width:230px">
        <label>Schedule (date &amp; time)</label><input id="edWhen" type="datetime-local">
      </div>
    </div>

    <label style="margin-top:12px;display:block">Photos <span class="hint">&mdash; &#9733; cover &middot; &#9664; &#9654; reorder &middot; &#10005; remove</span></label>
    <div id="edSlides" class="slrow"></div>

    <label style="margin-top:10px;display:block">Swap in a photo from the library <span id="edTabs"></span></label>
    <div id="edLib" class="librow"></div>

    <details style="margin-top:12px;background:#0f1115;border:1px solid #262b36;border-radius:8px;padding:10px">
      <summary style="cursor:pointer;color:#7aa2f7;font-weight:600">&#10022; Need a different photo? Generate one with ZenCreator</summary>
      <p class="hint" style="margin:8px 0">Describe the scene only &mdash; <b id="edWho">the model</b>'s face &amp; body references are applied automatically. New photos land in the folder tab selected above.</p>
      <textarea id="edPrompt" placeholder="e.g. sitting at a sunny cafe table with an iced coffee, candid, natural light"></textarea>
      <div style="display:flex;gap:8px;align-items:center;margin-top:6px;flex-wrap:wrap">
        <button class="mini" onclick="genPhoto()">&#10022; Generate photo</button>
        <span id="edGenMsg" class="hint"></span>
      </div>
    </details>

    <label style="margin-top:12px;display:block">Caption
      <button class="mini" onclick="aiCap()">&#10022; AI caption (3 styles)</button>
      <span id="edCapMsg" class="hint"></span></label>
    <textarea id="edCap" style="height:78px"></textarea>
    <div id="edCapOpts" style="display:none;flex-direction:column;gap:6px;margin:6px 0"></div>

    <label>Hashtags</label>
    <textarea id="edTags" style="height:52px" placeholder="#..."></textarea>

    <div style="margin-top:14px;display:flex;gap:8px;flex-wrap:wrap">
      <button onclick="saveEd(null)">Save changes</button>
      <button class="bA" onclick="saveEd('approved')">&#10003; Save &amp; approve</button>
      <button class="bU" onclick="closeEd()">Cancel</button>
      <span id="edErr" style="color:#f7a2a2;font-size:13px;align-self:center"></span>
    </div>
  </div>
</div>

<style>
.cnt{font-size:12px;background:#3d2f1f;color:#f7d67a;padding:2px 10px;border-radius:10px;vertical-align:middle}
.flbl{display:block;font-size:11px;color:#6b7280;margin-bottom:3px}
.sectabs{display:flex;gap:8px;flex-wrap:wrap;margin:16px 0 12px}
.sectab{background:#222732;color:#9aa5b1;border:0;padding:9px 18px;border-radius:8px;cursor:pointer;font-weight:700;font-size:14px}
.sectab.on{background:#7aa2f7;color:#0f1115}
.sectab.x.on{background:#e6e6e6;color:#0f1115}
.sectab.fanvue.on{background:#c67af7;color:#0f1115}
.viewbtns{display:flex;gap:4px}
.vb{background:#222732;color:#9aa5b1;border:0;padding:7px 13px;border-radius:6px;cursor:pointer;font-weight:600;font-size:13px}
.vb.on{background:#7aa2f7;color:#0f1115}
.apgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:14px;margin-top:12px}
.apc{background:#161922;border:1px solid #262b36;border-radius:12px;overflow:hidden;display:flex;flex-direction:column}
.apc .top{display:flex;gap:12px;padding:12px}
.apc .th{width:96px;height:96px;border-radius:8px;background:#0f1115 center/cover no-repeat;flex:none;cursor:pointer}
.apc .meta{min-width:0;flex:1}
.apc .who{font-weight:700;font-size:15px}
.apc .who a{color:#e6e6e6}
.plat{display:inline-block;font-size:11px;font-weight:700;padding:2px 9px;border-radius:10px;margin-left:6px;vertical-align:middle}
.when{color:#9aa5b1;font-size:12px;margin-top:3px}
.cap{padding:0 12px;font-size:13px;line-height:1.45;white-space:pre-wrap;word-break:break-word}
.tags{padding:6px 12px 0;font-size:12px;color:#7aa2f7;word-break:break-word}
.notes{padding:6px 12px 0;font-size:12px;color:#f7a2a2}
.acts{display:flex;gap:8px;padding:12px;margin-top:auto;flex-wrap:wrap}
.acts button{flex:1;padding:8px 0;font-size:13px;min-width:88px}
.bA{background:#1f3d2b!important;color:#7ee2a8!important}
.bR{background:#3d1f1f!important;color:#f7a2a2!important}
.bU{background:#2a2f3a!important;color:#9aa5b1!important}
.bE{background:#222732!important;color:#7aa2f7!important}
.stb{font-size:11px;font-weight:700;padding:2px 9px;border-radius:10px}
.st-approved{background:#1f3d2b;color:#7ee2a8}.st-rejected{background:#3d1f1f;color:#f7a2a2}
.st-posted{background:#1f2f3d;color:#7ac6f7}.st-failed{background:#3d1f1f;color:#f7a2a2}
.st-pending_review{background:#3d2f1f;color:#f7d67a}
.empty{color:#3b414d;padding:18px;border:1px dashed #262b36;border-radius:12px;grid-column:1/-1;text-align:center}
.calgrid{display:grid;grid-template-columns:repeat(7,1fr);gap:6px;margin-top:12px}
.cdow{color:#6b7280;font-size:11px;text-align:center;padding:2px 0;font-weight:700}
.cday{background:#161922;border:1px solid #232836;border-radius:8px;min-height:104px;padding:5px;position:relative}
.cday.other{opacity:.3}
.cday.today{border-color:#f7c97a}
.cday .dn{font-size:11px;color:#9aa5b1;margin-bottom:3px;cursor:pointer}
.cday .dn:hover{color:#7aa2f7}
.cev{display:flex;gap:4px;align-items:center;background:#1b1f29;border-left:3px solid #f7d67a;border-radius:4px;padding:3px 4px;margin-bottom:3px;cursor:pointer;font-size:11px}
.cev:hover{background:#222a38}
.cev img{width:20px;height:24px;object-fit:cover;border-radius:3px;flex:none}
.cev .cnm{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:#e6e6e6}
.cev.approved{border-left-color:#7ee2a8}.cev.posted{border-left-color:#7ac6f7}
.cev.rejected{border-left-color:#f7a2a2;opacity:.6}.cev.failed{border-left-color:#f7a2a2}
.wkcol{background:#161922;border:1px solid #232836;border-radius:8px;padding:6px;min-height:200px}
.wkhd{font-size:12px;color:#9aa5b1;font-weight:700;margin-bottom:6px;text-align:center}
.wkhd.today{color:#f7c97a}
.dayrow{display:flex;gap:12px;background:#161922;border:1px solid #262b36;border-left:4px solid #f7d67a;border-radius:10px;padding:12px;margin-bottom:10px}
.dayrow.approved{border-left-color:#7ee2a8}.dayrow.posted{border-left-color:#7ac6f7}
.dayrow.rejected{border-left-color:#f7a2a2}.dayrow.failed{border-left-color:#f7a2a2}
.dayrow img{width:72px;height:90px;object-fit:cover;border-radius:8px;flex:none;cursor:pointer}
.dayrow .tm{font-size:19px;font-weight:800;color:#7aa2f7;min-width:64px}
#ed{display:none;position:fixed;inset:0;background:rgba(10,12,16,.85);z-index:60;align-items:center;justify-content:center}
#ed.on{display:flex}
.edcard{background:#161922;border:1px solid #262b36;border-radius:12px;padding:20px;width:640px;max-width:94vw;max-height:92vh;overflow:auto}
.edcard label{display:block;font-size:13px;color:#9aa5b1;margin:8px 0 4px}
.edcard textarea,.edcard input,.edcard select{width:100%;background:#0f1115;border:1px solid #333a48;color:#e6e6e6;border-radius:6px;padding:8px;box-sizing:border-box;font:inherit}
.edcard textarea{height:64px}
.hint{font-size:12px;color:#6b7280;font-weight:400}
.mini{background:#222732;color:#7aa2f7;border:0;padding:3px 10px;border-radius:6px;font-size:12px;cursor:pointer;font-weight:700;width:auto}
.slrow{display:flex;gap:8px;flex-wrap:wrap;padding:4px 0}
.librow{display:flex;gap:6px;flex-wrap:wrap;max-height:132px;overflow:auto;padding:4px 0}
.librow img{width:46px;height:58px;object-fit:cover;border-radius:5px;cursor:pointer;border:2px solid #262b36}
</style>
<script>
const ROOT=(window.ORG_ROOT||'').replace(/\/$/,'');
const PLATFORMS=['instagram','tiktok','x','youtube','facebook','reddit','fanvue'];
const SOCIAL=['instagram','tiktok','youtube','facebook','reddit'];
const CATS=[['sfw','SFW'],['x','X'],['fanvue','Fanvue']];
const SECTIONS=[['all','All'],['social','Social'],['x','X'],['fanvue','Fanvue']];
const CATC={social:'sfw',x:'x',fanvue:'fanvue',all:'sfw'};
const PLATC={instagram:['#3d1f33','#f7a2c0'],tiktok:['#1f333d','#7ac6f7'],x:['#2a2f3a','#e6e6e6'],
  youtube:['#3d1f1f','#f7a2a2'],facebook:['#1f2a3d','#7aa2f7'],reddit:['#3d2a1f','#f7c67a'],
  fanvue:['#331f3d','#c67af7']};
const DOW=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
const MONTHS=['January','February','March','April','May','June','July','August','September','October','November','December'];
let POSTS=[], MODELS=[], EDPOST=null, EDSLIDES=[], EDCAT='sfw';
let SECTION='all', VIEW='list', CUR=new Date();

function esc(s){return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function pill(p){const c=PLATC[p]||['#2a2f3a','#9aa5b1'];
  return `<span class="plat" style="background:${c[0]};color:${c[1]}">${esc(p)}</span>`;}
function ymd(d){return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');}
function dpart(p){return (p.slot_time||'').slice(0,10);}
function tpart(p){return (p.slot_time||'').slice(11,16);}

/* ---------- filtering ---------- */
function inSection(p){
  if(SECTION==='all') return true;
  if(SECTION==='x') return p.platform==='x';
  if(SECTION==='fanvue') return p.platform==='fanvue';
  return SOCIAL.indexOf(p.platform)>=0;
}
function filtered(){
  const m=document.getElementById('fModel').value;
  const pl=document.getElementById('fPlat').value;
  const st=document.getElementById('fStat').value;
  return POSTS.filter(p=>{
    if(!inSection(p)) return false;
    if(m!=='all'&&p.pslug!==m) return false;
    if(pl!=='all'&&p.platform!==pl) return false;
    if(st==='pending_review'&&p.status!=='pending_review') return false;
    if(st==='upcoming'&&['pending_review','approved'].indexOf(p.status)<0) return false;
    if(st==='all'&&p.status==='draft') return false;
    return true;
  });
}

/* ---------- media (big preview: video or image, click to enlarge) ---------- */
function mediaBlock(po){
  const base=`${ROOT}/api/post_media/${po.id}/`;
  if(po.is_video){
    return `<div style="padding:8px 12px 0"><video src="${base}0" controls preload="metadata" playsinline style="width:100%;max-height:560px;border-radius:8px;background:#000"></video><div style="font-size:11px;color:#7aa2f7;padding-top:4px">video · tap play</div></div>`;
  }
  const n=po.nmedia||1;
  if(n<=1){
    return `<div style="padding:8px 12px 0"><img src="${base}0" onclick="lightbox('${base}0',0)" style="width:100%;max-height:560px;object-fit:contain;border-radius:8px;background:#0b0d11;cursor:zoom-in"></div>`;
  }
  let strip='';
  for(let i=0;i<n;i++) strip+=`<img src="${base}${i}" onclick="lightbox('${base}${i}',0)" style="flex:1 1 30%;max-width:32%;height:230px;object-fit:cover;border-radius:6px;border:2px solid ${i===0?'#7aa2f7':'#262b36'};cursor:zoom-in">`;
  return `<div style="padding:8px 12px 0"><div style="display:flex;gap:6px;flex-wrap:wrap">${strip}</div><div style="font-size:11px;color:#7aa2f7;padding-top:4px">${n}-slide carousel · tap any to enlarge</div></div>`;
}
function lightbox(src,isVid){
  let o=document.getElementById('lbx');
  if(!o){o=document.createElement('div');o.id='lbx';o.style.cssText='position:fixed;inset:0;background:rgba(0,0,0,.92);z-index:99999;display:flex;align-items:center;justify-content:center;cursor:zoom-out';o.onclick=()=>{o.style.display='none';o.innerHTML='';};document.body.appendChild(o);}
  o.innerHTML = isVid ? `<video src="${src}" controls autoplay style="max-width:96vw;max-height:96vh"></video>` : `<img src="${src}" style="max-width:96vw;max-height:96vh;object-fit:contain">`;
  o.style.display='flex';
}
/* ---------- cards ---------- */
function card(po,pending){
  const idxs=(po.img_idxs&&po.img_idxs.length)?po.img_idxs:(po.img_idx!=null?[po.img_idx]:[]);
  const th=idxs.length?`style="background-image:url('${ROOT}/content_img/${idxs[0]}')"`:(po.is_video?'style="background:#11141a"':'');
  const slides=idxs.length>1?`<div style="display:flex;gap:4px;padding:6px 12px 0;flex-wrap:wrap">${idxs.map((gi,n)=>`<img src="${ROOT}/content_img/${gi}" style="width:44px;height:56px;object-fit:cover;border-radius:5px;border:2px solid ${n===0?'#7aa2f7':'#262b36'}">`).join('')}<span style="font-size:11px;color:#7aa2f7;align-self:center;margin-left:4px">${idxs.length}-slide carousel</span></div>`:'';
  const when=po.slot_time?('&#128197; '+esc(po.slot_time.replace('T',' ')) ):'no time set';
  let acts='';
  if(pending){
    acts=`<div class="acts">
      <button class="bA" onclick="decide(${po.id},'approved')">&#10003; Approve</button>
      <button class="bE" onclick="openEd(${po.id})">&#9998; Edit</button>
      <button class="bR" onclick="rejectPost(${po.id})">&#10005; Reject</button></div>`;
  }else{
    acts=`<div class="acts"><span class="stb st-${esc(po.status)}" style="align-self:center">${esc(po.status)}</span>
      <button class="bE" onclick="openEd(${po.id})">&#9998; Edit</button>
      <button class="bU" onclick="decide(${po.id},'pending_review')">&#8630; Back to queue</button></div>`;
  }
  return `<div class="apc">
    <div class="top">
      <div class="th" ${th} onclick="location.href='${ROOT}/model/${po.pslug}'"></div>
      <div class="meta">
        <div class="who"><a href="${ROOT}/model/${po.pslug}">${esc(po.pname)}</a>${pill(po.platform)}</div>
        <div class="when">${when}</div>
        <div class="when">created ${esc((po.created_at||'').slice(0,16).replace('T',' '))}</div>
      </div>
    </div>
    ${mediaBlock(po)}
    <div class="cap">${esc(po.caption)}</div>
    ${po.hashtags?`<div class="tags">${esc(po.hashtags)}</div>`:''}
    ${po.review_notes?`<div class="notes">Note: ${esc(po.review_notes)}</div>`:''}
    ${acts}</div>`;
}

/* ---------- views ---------- */
function render(){
  const list=filtered();
  document.getElementById('shownCount').textContent=list.length+' post'+(list.length===1?'':'s')+' shown';
  const pend=list.filter(p=>p.status==='pending_review');
  document.getElementById('bulkBtn').style.display=pend.length>1?'inline-block':'none';
  document.getElementById('bulkBtn').textContent='✓ Approve all shown ('+pend.length+')';
  document.getElementById('sectabs').innerHTML=SECTIONS.map(([k,l])=>{
    const n=POSTS.filter(p=>{const s=SECTION;SECTION=k;const r=inSection(p);SECTION=s;return r&&p.status==='pending_review';}).length;
    return `<button class="sectab ${k} ${k===SECTION?'on':''}" onclick="setSection('${k}')">${l}${n?' · '+n:''}</button>`;
  }).join('');
  document.getElementById('viewbtns').innerHTML=[['list','List'],['day','Day'],['week','Week'],['month','Month']]
    .map(([k,l])=>`<button class="vb ${k===VIEW?'on':''}" onclick="setView('${k}')">${l}</button>`).join('');
  document.getElementById('datenav').style.display=VIEW==='list'?'none':'flex';
  document.getElementById('listWrap').style.display=VIEW==='list'?'block':'none';
  document.getElementById('calWrap').style.display=VIEW==='list'?'none':'block';
  if(VIEW==='list') renderList(list); else renderCal(list);
}
function renderList(list){
  const pend=list.filter(p=>p.status==='pending_review');
  const done=list.filter(p=>p.status!=='pending_review').slice(0,24);
  document.getElementById('pcount').textContent=pend.length+' waiting';
  document.getElementById('pending').innerHTML=
    pend.length?pend.map(p=>card(p,true)).join(''):'<div class="empty">Nothing waiting for review in this view.</div>';
  document.getElementById('decided').innerHTML=
    done.length?done.map(p=>card(p,false)).join(''):'<div class="empty">No decisions yet.</div>';
}
function evChip(p){
  const idxs=(p.img_idxs&&p.img_idxs.length)?p.img_idxs:(p.img_idx!=null?[p.img_idx]:[]);
  const im=p.is_video?`<span style="display:inline-block;width:18px;height:18px;border-radius:3px;background:#11141a;color:#7aa2f7;text-align:center;line-height:18px;font-size:10px">&#9654;</span>`:(idxs.length?`<img src="${ROOT}/content_img/${idxs[0]}">`:'');
  const c=PLATC[p.platform]||['#2a2f3a','#9aa5b1'];
  return `<div class="cev ${esc(p.status)}" onclick="openEd(${p.id})" title="${esc(p.pname)} · ${esc(p.platform)} · ${esc(p.status)}">
    ${im}<span class="cnm">${tpart(p)} ${esc(p.pname.split(' ')[0])}</span>
    <span style="width:7px;height:7px;border-radius:50%;background:${c[1]};flex:none"></span></div>`;
}
function renderCal(list){
  const byDay={};
  list.forEach(p=>{const d=dpart(p); if(d)(byDay[d]=byDay[d]||[]).push(p);});
  Object.values(byDay).forEach(a=>a.sort((x,y)=>tpart(x).localeCompare(tpart(y))));
  const today=ymd(new Date());
  const w=document.getElementById('calWrap');
  if(VIEW==='month'){
    const y=CUR.getFullYear(), m=CUR.getMonth();
    document.getElementById('dateLabel').textContent=MONTHS[m]+' '+y;
    const first=new Date(y,m,1), start=(first.getDay()+6)%7, dim=new Date(y,m+1,0).getDate();
    let h=DOW.map(d=>`<div class="cdow">${d}</div>`).join('');
    for(let i=0;i<start;i++) h+='<div class="cday other"></div>';
    for(let d=1;d<=dim;d++){
      const ds=`${y}-${String(m+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
      const evs=(byDay[ds]||[]);
      h+=`<div class="cday${ds===today?' today':''}">
        <div class="dn" onclick="jumpDay('${ds}')">${d}${evs.length?` <span style="color:#7aa2f7">· ${evs.length}</span>`:''}</div>
        ${evs.slice(0,4).map(evChip).join('')}
        ${evs.length>4?`<div style="font-size:10px;color:#7aa2f7;cursor:pointer" onclick="jumpDay('${ds}')">+${evs.length-4} more</div>`:''}</div>`;
    }
    w.innerHTML='<div class="calgrid">'+h+'</div>'+legend();
  }else if(VIEW==='week'){
    const base=new Date(CUR); base.setDate(base.getDate()-((base.getDay()+6)%7));
    const end=new Date(base); end.setDate(end.getDate()+6);
    document.getElementById('dateLabel').textContent=MONTHS[base.getMonth()].slice(0,3)+' '+base.getDate()+' – '+MONTHS[end.getMonth()].slice(0,3)+' '+end.getDate();
    let h='';
    for(let i=0;i<7;i++){
      const d=new Date(base); d.setDate(d.getDate()+i); const ds=ymd(d);
      const evs=byDay[ds]||[];
      h+=`<div class="wkcol"><div class="wkhd${ds===today?' today':''}">${DOW[i]} ${d.getDate()}</div>
        ${evs.length?evs.map(evChip).join(''):'<div style="color:#3b414d;font-size:11px;text-align:center;padding-top:8px">&mdash;</div>'}</div>`;
    }
    w.innerHTML='<div class="calgrid">'+h+'</div>'+legend();
  }else{
    const ds=ymd(CUR);
    document.getElementById('dateLabel').textContent=DOW[(CUR.getDay()+6)%7]+' '+MONTHS[CUR.getMonth()]+' '+CUR.getDate()+', '+CUR.getFullYear();
    const evs=byDay[ds]||[];
    w.innerHTML=(evs.length?evs.map(p=>{
      const idxs=(p.img_idxs&&p.img_idxs.length)?p.img_idxs:(p.img_idx!=null?[p.img_idx]:[]);
      return `<div class="dayrow ${esc(p.status)}">
        <div class="tm">${tpart(p)||'--:--'}</div>
        ${p.is_video?`<video src="${ROOT}/api/post_media/${p.id}/0" muted preload="metadata" onclick="openEd(${p.id})" style="width:70px;height:90px;object-fit:cover;border-radius:6px;background:#000;cursor:pointer"></video>`:(idxs.length?`<img src="${ROOT}/content_img/${idxs[0]}" onclick="openEd(${p.id})">`:'')}
        <div style="flex:1;min-width:0">
          <div><b>${esc(p.pname)}</b>${pill(p.platform)}<span class="stb st-${esc(p.status)}" style="margin-left:6px">${esc(p.status).replace('_',' ')}</span>${idxs.length>1?`<span style="font-size:11px;color:#7aa2f7;margin-left:6px">${idxs.length} slides</span>`:''}</div>
          <div class="cap" style="padding:6px 0 0">${esc(p.caption)}</div>
          <div class="tags" style="padding:4px 0 0">${esc(p.hashtags||'')}</div>
        </div>
        <div style="display:flex;flex-direction:column;gap:6px;justify-content:center">
          ${p.status==='pending_review'?`<button class="bA" onclick="decide(${p.id},'approved')">&#10003; Approve</button>`:''}
          <button class="bE" onclick="openEd(${p.id})">&#9998; Edit</button>
        </div></div>`;
    }).join(''):'<div class="empty" style="margin-top:12px">Nothing scheduled this day.</div>')+legend();
  }
}
function legend(){
  return `<div style="display:flex;gap:16px;flex-wrap:wrap;margin-top:12px;font-size:11px;color:#6b7280">
    <span><span style="display:inline-block;width:10px;height:10px;background:#f7d67a;border-radius:2px"></span> pending</span>
    <span><span style="display:inline-block;width:10px;height:10px;background:#7ee2a8;border-radius:2px"></span> approved</span>
    <span><span style="display:inline-block;width:10px;height:10px;background:#7ac6f7;border-radius:2px"></span> posted</span>
    <span><span style="display:inline-block;width:10px;height:10px;background:#f7a2a2;border-radius:2px"></span> rejected / failed</span>
    <span style="margin-left:auto">click any post to edit it</span></div>`;
}
function setSection(k){ SECTION=k; render(); }
function setView(v){ VIEW=v; render(); }
function jumpDay(ds){ CUR=new Date(ds+'T12:00:00'); VIEW='day'; render(); }
function goToday(){ CUR=new Date(); render(); }
function navDate(d){
  if(VIEW==='month') CUR=new Date(CUR.getFullYear(),CUR.getMonth()+d,1);
  else if(VIEW==='week'){ CUR=new Date(CUR); CUR.setDate(CUR.getDate()+7*d); }
  else { CUR=new Date(CUR); CUR.setDate(CUR.getDate()+d); }
  render();
}
function approveAllShown(){
  const pend=filtered().filter(p=>p.status==='pending_review');
  if(!pend.length) return;
  if(!confirm('Approve all '+pend.length+' posts currently shown?\n\nThey will publish at their scheduled times once live posting is ON.')) return;
  Promise.all(pend.map(p=>fetch(ROOT+'/api/post/update',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({id:p.id,status:'approved'})}))).then(()=>load().then(render));
}

/* ---------- data ---------- */
function load(){
  return fetch(ROOT+'/api/approvals').then(r=>r.json()).then(d=>{ POSTS=d.posts||[]; });
}
function decide(id,status){
  fetch(ROOT+'/api/post/update',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({id:id,status:status})}).then(()=>load().then(render));
}
function rejectPost(id){
  const note=prompt('Why is this rejected? (note goes back to the composer)')||'';
  fetch(ROOT+'/api/post/update',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({id:id,status:'rejected',review_notes:note})}).then(()=>load().then(render));
}

/* ---------- editor ---------- */
function openEd(id){
  const po=POSTS.find(p=>p.id===id); if(!po) return;
  EDPOST=po;
  EDSLIDES=(po.img_idxs&&po.img_idxs.length)?po.img_idxs.slice():(po.img_idx!=null?[po.img_idx]:[]);
  document.getElementById('edTitle').innerHTML='Edit post &mdash; '+esc(po.pname);
  document.getElementById('edWho').textContent=po.pname;
  document.getElementById('edPlat').innerHTML=PLATFORMS.map(p=>`<option${p===po.platform?' selected':''}>${p}</option>`).join('');
  document.getElementById('edWhen').value=(po.slot_time||'').replace(' ','T').slice(0,16);
  document.getElementById('edCap').value=po.caption||'';
  document.getElementById('edTags').value=po.hashtags||'';
  document.getElementById('edErr').textContent='';
  document.getElementById('edCapMsg').textContent='';
  document.getElementById('edGenMsg').textContent='';
  document.getElementById('edCapOpts').style.display='none';
  document.getElementById('edPrompt').value='';
  renderSlides();
  loadLib(po.platform==='fanvue'?'fanvue':(po.platform==='x'?'x':'sfw'));
  document.getElementById('ed').classList.add('on');
}
function closeEd(){ document.getElementById('ed').classList.remove('on'); }
function renderSlides(){
  document.getElementById('edSlides').innerHTML=EDSLIDES.map((gi,n)=>`
    <div style="display:flex;flex-direction:column;align-items:center;gap:2px">
      <img src="${ROOT}/content_img/${gi}" style="width:62px;height:78px;object-fit:cover;border-radius:6px;border:2px solid ${n===0?'#7aa2f7':'#262b36'}">
      <div style="font-size:10px;color:${n===0?'#7aa2f7':'#6b7280'}">${n===0?'cover':'slide '+(n+1)}</div>
      <div style="display:flex;gap:2px">
        ${n>0?`<button class="mini" onclick="slMove(${n},-1)">&#9664;</button>`:''}
        ${n<EDSLIDES.length-1?`<button class="mini" onclick="slMove(${n},1)">&#9654;</button>`:''}
        ${n>0?`<button class="mini" title="make cover" onclick="slCover(${n})">&#9733;</button>`:''}
        ${EDSLIDES.length>1?`<button class="mini" style="color:#f7a2a2" onclick="slDel(${n})">&#10005;</button>`:''}
      </div>
    </div>`).join('')||'<span style="color:#f7a2a2;font-size:12px">no photos &mdash; pick one below</span>';
}
function slMove(n,d){const t=EDSLIDES[n];EDSLIDES[n]=EDSLIDES[n+d];EDSLIDES[n+d]=t;renderSlides();}
function slCover(n){const t=EDSLIDES.splice(n,1)[0];EDSLIDES.unshift(t);renderSlides();}
function slDel(n){EDSLIDES.splice(n,1);renderSlides();loadLib(EDCAT);}
function loadLib(cat){
  EDCAT=cat;
  document.getElementById('edTabs').innerHTML=CATS.map(([k,l])=>`<button class="mini" style="margin-left:6px;${k===cat?'background:#7aa2f7;color:#0f1115':''}" onclick="loadLib('${k}')">${l}</button>`).join('');
  fetch(ROOT+'/api/lib_idxs/'+EDPOST.pslug+'/'+cat).then(r=>r.json()).then(d=>{
    const idxs=(d.idxs||[]).filter(i=>i!=null);
    document.getElementById('edLib').innerHTML=idxs.length
      ? idxs.map(gi=>`<img src="${ROOT}/content_img/${gi}" style="border-color:${EDSLIDES.includes(gi)?'#7ee2a8':'#262b36'}" onclick="slAdd(${gi})">`).join('')
      : '<span class="hint">No photos in this folder yet &mdash; upload on the model page or generate one below.</span>';
  });
}
function slAdd(gi){
  const at=EDSLIDES.indexOf(gi);
  if(at>=0){ if(EDSLIDES.length>1) EDSLIDES.splice(at,1); }
  else EDSLIDES.push(gi);
  renderSlides(); loadLib(EDCAT);
}
function genPhoto(){
  const prompt=document.getElementById('edPrompt').value.trim();
  if(!prompt){ document.getElementById('edGenMsg').textContent='describe the scene first'; return; }
  const msg=document.getElementById('edGenMsg');
  msg.textContent='generating… (about a minute)';
  fetch(ROOT+'/api/zen/generate',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({slug:EDPOST.pslug,category:EDCAT,tool:'photoshoot',
      input:{face_ref:'@face',body_ref:'@body',prompt:prompt,image_count:2}})})
  .then(r=>r.json()).then(d=>{
    if(d.error){ msg.textContent='failed: '+d.error; return; }
    pollGen(d.id,msg);
  }).catch(()=>{ msg.textContent='request failed'; });
}
function pollGen(gid,msg){
  fetch(ROOT+'/api/zen/status/'+gid).then(r=>r.json()).then(d=>{
    if(d.status==='succeeded'){ msg.textContent='✓ new photos added below — click one to use it'; loadLib(EDCAT); }
    else if(d.status==='failed'){ msg.textContent='generation failed — try a different description'; }
    else{ msg.textContent='generating… '+(d.status||'working'); setTimeout(()=>pollGen(gid,msg),6000); }
  }).catch(()=>setTimeout(()=>pollGen(gid,msg),8000));
}
function aiCap(){
  const msg=document.getElementById('edCapMsg'), box=document.getElementById('edCapOpts');
  msg.textContent='writing 3 styles…'; box.style.display='none'; box.innerHTML='';
  fetch(ROOT+'/api/post/gen_captions3',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({slug:EDPOST.pslug,platform:document.getElementById('edPlat').value,
      hint:document.getElementById('edCap').value})})
  .then(r=>r.json()).then(d=>{
    if(d.error||!(d.options||[]).length){ msg.textContent='failed: '+(d.error||'no output'); return; }
    msg.textContent='pick a style';
    window.CAPO=d.options;
    box.style.display='flex';
    box.innerHTML=d.options.map((o,i)=>`
      <div onclick="useCap(${i})" style="border:1px solid #333a48;border-radius:8px;padding:8px 10px;cursor:pointer">
        <b style="font-size:12px;color:#7aa2f7">${esc(o.style)}</b>
        <div style="font-size:13px;margin-top:2px">${esc(o.caption)}</div>
        <div style="font-size:11px;color:#6b7280;margin-top:2px">${esc((o.hashtags||'').slice(0,140))}</div>
      </div>`).join('');
  }).catch(()=>{ msg.textContent='request failed'; });
}
function useCap(i){
  const o=(window.CAPO||[])[i]; if(!o) return;
  document.getElementById('edCap').value=o.caption;
  if(o.hashtags) document.getElementById('edTags').value=o.hashtags;
  document.getElementById('edCapOpts').style.display='none';
  document.getElementById('edCapMsg').textContent='✓ '+o.style;
}
function saveEd(newStatus){
  if(!EDSLIDES.length){ document.getElementById('edErr').textContent='Add at least one photo.'; return; }
  const body={id:EDPOST.id,platform:document.getElementById('edPlat').value,
    caption:document.getElementById('edCap').value,hashtags:document.getElementById('edTags').value,
    slot_time:(document.getElementById('edWhen').value||'').replace('T',' ')};
  if(newStatus) body.status=newStatus;
  fetch(ROOT+'/api/post/set_slides',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({id:EDPOST.id,idxs:EDSLIDES})})
  .then(r=>r.json()).then(d=>{
    if(d.error){ document.getElementById('edErr').textContent=d.error; return; }
    return fetch(ROOT+'/api/post/update',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify(body)}).then(r=>r.json()).then(d2=>{
        if(d2.error){ document.getElementById('edErr').textContent=d2.error; return; }
        closeEd(); load().then(render);
      });
  });
}
document.addEventListener('keydown',e=>{
  if(e.key==='Escape'){ closeEd(); return; }
  if(document.getElementById('ed').classList.contains('on')) return;
  if(VIEW!=='list'&&e.key==='ArrowLeft') navDate(-1);
  if(VIEW!=='list'&&e.key==='ArrowRight') navDate(1);
});

/* ---------- go-live ---------- */
function loadGL(){
  fetch(ROOT+'/api/golive').then(r=>r.json()).then(d=>{
    const st=document.getElementById('glState'), b=document.getElementById('glBtn');
    if(d.on){ st.textContent='ON — publishing approved posts'; st.style.background='#1f3d2b'; st.style.color='#7ee2a8';
      b.textContent='Turn OFF'; b.className='bR'; }
    else{ st.textContent='OFF — holding (safety gate)'; st.style.background='#3d2f1f'; st.style.color='#f7d67a';
      b.textContent='Turn ON live posting'; b.className='bA'; }
    b.style.display='inline-block'; window.GLON=!!d.on;
  });
}
function toggleGL(){
  const turningOn=!window.GLON;
  if(turningOn&&!confirm('Turn ON live posting? Approved posts with a due time will publish to the real platforms.')) return;
  fetch(ROOT+'/api/golive',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({on:turningOn})}).then(r=>r.json()).then(()=>loadGL());
}

/* ---------- boot ---------- */
fetch(ROOT+'/api/board').then(r=>r.json()).then(b=>{
  MODELS=(b.personas||[]).slice().sort((a,x)=>a.name.localeCompare(x.name));
  document.getElementById('fModel').innerHTML='<option value="all">All models</option>'+
    MODELS.map(m=>`<option value="${m.slug}">${esc(m.name)}</option>`).join('');
  document.getElementById('fPlat').innerHTML='<option value="all">All platforms</option>'+
    PLATFORMS.map(p=>`<option value="${p}">${p}</option>`).join('');
  return load();
}).then(render);
loadGL();
setInterval(()=>{ if(!document.getElementById('ed').classList.contains('on')) load().then(render); },30000);
</script>
'''
