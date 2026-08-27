"""Playbooks page: shared, editable knowledge base the agents read + research agents update."""

BODY = r'''
<h1>Playbooks</h1>
<p style="color:#9aa5b1;margin-top:-4px">The shared knowledge base every model agent reads before planning content. Platform &amp; function specialists keep these current; you can edit any of them.</p>
<div id="pb"></div>
<style>
.pbcard{background:#161922;border:1px solid #262b36;border-radius:10px;padding:16px;margin-top:12px}
.pbcard h3{margin:0 0 8px;text-transform:capitalize}
.pbcard textarea{width:100%;height:110px;background:#0f1115;border:1px solid #333a48;color:#e6e6e6;border-radius:6px;padding:10px;box-sizing:border-box;font:inherit}
.pbmsg{color:#7ee2a8;font-size:12px;margin-left:10px}
</style>
<script>
const SCOPECOLOR={global:'#c0a2f7',tiktok:'#7ae2e2',instagram:'#f7a2c0',x:'#7aa2f7',youtube:'#f7a2a2',facebook:'#7aa5f7',reddit:'#f7c97a',fanvue:'#f78ac0'};
fetch('api/playbook').then(r=>r.json()).then(list=>{
  const box=document.getElementById('pb'); box.innerHTML='';
  list.forEach(p=>{
    const c=SCOPECOLOR[p.scope]||'#9aa5b1';
    const d=document.createElement('div'); d.className='pbcard'; d.style.borderTop='3px solid '+c;
    d.innerHTML=`<h3 style="color:${c}">${p.scope}</h3>
      <textarea id="pb_${p.scope}">${(p.body||'').replace(/</g,'&lt;')}</textarea>
      <div style="margin-top:10px"><button onclick="savePb('${p.scope}')">Save</button><span class="pbmsg" id="msg_${p.scope}"></span></div>`;
    box.appendChild(d);
  });
});
function savePb(scope){
  const body=document.getElementById('pb_'+scope).value;
  fetch('api/playbook/set',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({scope,body})})
    .then(r=>r.json()).then(()=>{document.getElementById('msg_'+scope).textContent='Saved ✓';
      setTimeout(()=>document.getElementById('msg_'+scope).textContent='',2000);});
}
</script>
'''
