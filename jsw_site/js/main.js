// Brand name: change here to rename the site everywhere.
const BRAND = "JSW AI";
document.querySelectorAll("[data-brand]").forEach(e=>e.textContent=BRAND);
document.title = document.title.replace(/^JSW( AI)?/, BRAND);
document.getElementById("year").textContent = new Date().getFullYear();
const t=document.querySelector(".menu-toggle"),l=document.querySelector(".links");
t.addEventListener("click",()=>l.classList.toggle("open"));
l.querySelectorAll("a").forEach(a=>a.addEventListener("click",()=>l.classList.remove("open")));
// Contact form: opens the visitor's email client (no backend needed).
const f=document.getElementById("contact-form");
f.addEventListener("submit",e=>{e.preventDefault();const d=new FormData(f),v=k=>(d.get(k)||"").toString().trim();
const subject="Website inquiry - "+v("service");
const body="Name: "+v("name")+"\nEmail: "+v("email")+"\nCompany: "+v("company")+"\nService: "+v("service")+"\n\nMessage:\n"+v("message");
window.location.href="mailto:sam@jsw-ai.com?subject="+encodeURIComponent(subject)+"&body="+encodeURIComponent(body);
document.getElementById("form-note").textContent="Opening your email app… If nothing happens, please try again.";});
