import streamlit as st
import urllib.request, json

st.set_page_config(page_title="Haki AI — Haki za Binadamu Kenya", page_icon="✊", layout="centered")
st.markdown("""<style>
.stApp{background:#0a0808;color:#f3e5f5}
.haki-card{background:#1a0a0a;border:1px solid #880e4f;border-radius:10px;padding:14px 18px;margin:8px 0}
.emergency{background:#1a0000;border:2px solid #ff0000;border-radius:8px;padding:10px;margin:8px 0}
.stButton>button{background:#880e4f;color:#fff;border:none;border-radius:8px;padding:10px 24px;font-weight:700;width:100%}
</style>""", unsafe_allow_html=True)

API_KEY = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY","")
SYSTEM = "Wewe ni mshauri wa haki za binadamu Kenya. Jibu kwa Kiswahili. Toa habari za haki kulingana na Katiba ya Kenya 2010 na sheria za kimataifa. Elekeza kwa mashirika yanayotoa msaada wa kisheria bure. Sisitiza haki za watu wenye ulemavu."

def ask(q):
    if not API_KEY: return "❌ API key not configured."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    body = {"contents":[{"role":"user","parts":[{"text":q}]}],
            "systemInstruction":{"parts":[{"text":SYSTEM}]},
            "generationConfig":{"temperature":0.2,"maxOutputTokens":700}}
    try:
        req = urllib.request.Request(url,data=json.dumps(body).encode(),headers={"Content-Type":"application/json"},method="POST")
        with urllib.request.urlopen(req,timeout=30) as r:
            return json.loads(r.read())["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e: return f"❌ {e}"

st.markdown('<div class="emergency">🆘 DHARURA: DPP: 020 423 0000 | IPOA (Polisi): 0800 720 471 | KNCHR: 020 271 2722</div>', unsafe_allow_html=True)

st.markdown("# ✊ Haki AI")
st.markdown("**Haki za Binadamu na Ulemavu — Katiba ya Kenya**")

tab1,tab2,tab3 = st.tabs(["📖 Haki za Kimsingi","♿ Ulemavu","🏛️ Msaada wa Kisheria Bure"])

with tab1:
    rights_q = st.selectbox("Swali lako:", [
        "Haki zangu kama ninakamatwa na polisi",
        "Haki zangu dhidi ya unyanyasaji wa polisi",
        "Haki za mkutano na maandamano Kenya",
        "Haki za wafungwa Kenya",
        "Haki zangu ikiwa nimefukuzwa kazi vibaya",
        "Haki zangu kama mkimbizi Kenya",
        "Jinsi ya kulinda haki yangu ya faragha",
        "Ubaguzi — nini unastahili kisheria",
    ])
    if st.button("📖 Niambie Haki Zangu", key="rights_btn"):
        with st.spinner("..."): result = ask(rights_q + " chini ya Katiba ya Kenya 2010 na sheria husika. Toa hatua sahihi za kisheria.")
        st.markdown(f'<div class="haki-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

with tab2:
    dis_q = st.selectbox("Swali la ulemavu:", [
        "Haki za mtu mwenye ulemavu Kenya — orodha kamili",
        "Jinsi ya kupata kitambulisho cha ulemavu (NCPWD)",
        "Punguzo la kodi kwa watu wenye ulemavu Kenya",
        "Elimu ya watoto wenye ulemavu — haki na masharti",
        "Mahali pa kazi — wajibika wa mwajiri kwa mfanyakazi mwenye ulemavu",
        "Huduma za bure za serikali kwa watu wenye ulemavu",
    ])
    if st.button("♿ Niambie", key="dis_btn"):
        with st.spinner("..."): result = ask(dis_q + " Kenya Persons with Disabilities Act na NCPWD. Toa hatua za vitendo na viungo rasmi.")
        st.markdown(f'<div class="haki-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

with tab3:
    st.markdown("### Msaada wa Kisheria Bure Kenya")
    orgs = [
        ("KNCHR","Kenya National Commission on Human Rights","020 271 2722","knchr.org"),
        ("LSK Legal Aid","Law Society of Kenya","020 271 7061","lsk.or.ke"),
        ("FIDA Kenya","Msaada wa wanawake","020 271 0680","fidakenya.org"),
        ("CRADLE","Haki za watoto","020 375 6497","thecradle.or.ke"),
        ("IPOA","Malalamiko dhidi ya polisi","0800 720 471","ipoa.go.ke"),
        ("NCPWD","Haki za ulemavu","020 271 5955","ncpwd.go.ke"),
    ]
    for name, desc, phone, web in orgs:
        st.markdown(f'<div class="haki-card"><b>{name}</b> — {desc}<br>📞 {phone} | 🌐 {web}</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("✊ Haki AI v1.0 | KNCHR: knchr.org | Si ushauri wa kisheria rasmi | CC BY-NC-ND 4.0")
