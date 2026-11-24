import streamlit as st
import html, os, urllib.request, json

st.set_page_config(page_title="Haki AI — Haki za Binadamu Kenya", page_icon="✊", layout="centered")
st.markdown("""<style>
.stApp{background:#0a0808;color:#f3e5f5}
.haki-card{background:#1a0a0a;border:1px solid #880e4f;border-radius:10px;padding:14px 18px;margin:8px 0}
.emergency{background:#1a0000;border:2px solid #ff0000;border-radius:8px;padding:10px;margin:8px 0}
.stButton>button{background:#880e4f;color:#fff;border:none;border-radius:8px;padding:10px 24px;font-weight:700;width:100%}
</style>""", unsafe_allow_html=True)

def _secret(name):
    """Read a Streamlit secret, falling back to the environment; never crash when no secrets file exists."""
    try:
        v = st.secrets.get(name)
    except Exception:
        v = None
    return v or os.environ.get(name, "")

API_KEY = _secret("GOOGLE_API_KEY") or _secret("GEMINI_API_KEY")
MODEL = _secret("GEMINI_MODEL") or "gemini-3.5-flash-lite"  # the 1.5 Flash model this app used was retired by Google
SYSTEM = "Wewe ni mshauri wa haki za binadamu Kenya. Jibu kwa Kiswahili. Toa habari za haki kulingana na Katiba ya Kenya 2010 na sheria za kimataifa. Elekeza kwa mashirika yanayotoa msaada wa kisheria bure. Sisitiza haki za watu wenye ulemavu."

def ask(q):
    if not API_KEY: return "❌ API key not configured."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
    body = {"contents":[{"role":"user","parts":[{"text":q}]}],
            "systemInstruction":{"parts":[{"text":SYSTEM}]},
            "generationConfig":{"temperature":0.2,"maxOutputTokens":700}}
    try:
        req = urllib.request.Request(url,data=json.dumps(body).encode(),headers={"Content-Type":"application/json","x-goog-api-key":API_KEY},method="POST")
        with urllib.request.urlopen(req,timeout=30) as r:
            return html.escape(json.loads(r.read())["candidates"][0]["content"]["parts"][0]["text"])
    except Exception as e: return html.escape(f"❌ {e}")

st.markdown('<div class="emergency">🆘 DHARURA: Dharura: 999 / 112 | IPOA (malalamiko dhidi ya polisi): 1559 | KNCHR: 0800 720 627 (SMS 22359) | LSK: 0800 720 434</div>', unsafe_allow_html=True)

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
        ("KNCHR","Kenya National Commission on Human Rights","0800 720 627 (bure) · SMS 22359","knchr.org"),
        ("LSK Legal Aid","Law Society of Kenya","0800 720 434 (bure)","lsk.or.ke"),
        ("FIDA Kenya","Msaada wa wanawake","0800 720 501 (bure)","fidakenya.org"),
        ("Childline Kenya","Haki na usalama wa watoto","116 (bure, saa 24)","piga 116"),
        ("IPOA","Malalamiko dhidi ya polisi","1559 (bure)","ipoa.go.ke"),
        ("NCPWD","Haki za ulemavu","Angalia ncpwd.go.ke","ncpwd.go.ke"),
    ]
    for name, desc, phone, web in orgs:
        st.markdown(f'<div class="haki-card"><b>{name}</b> — {desc}<br>📞 {phone} | 🌐 {web}</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("✊ Haki AI v1.0 | KNCHR: knchr.org | Si ushauri wa kisheria rasmi | CC BY-NC-ND 4.0")
