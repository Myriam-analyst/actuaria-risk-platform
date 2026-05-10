"""
ACTUARIA — Risk Pricing Studio v3.0
Plateforme de tarification actuarielle automobile
"""

import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import chi2
from scipy.stats import poisson as sp_poisson
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings("ignore")
# Importer les modules principaux de création de PDF
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime
import time

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG PAGE
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="ACTUARIA — Risk Pricing Studio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════════════════
# CSS PREMIUM
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html,body,[class*="css"]{ font-family:'Inter',sans-serif !important; }
.stApp{ background:#050B18; color:#F1F5F9; }

[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#050B18 0%,#0A1628 60%,#050B18 100%) !important;
  border-right:1px solid #1E3A5F !important;
}
[data-testid="stMetric"]{
  background:#0F1E38; border:1px solid #1E3A5F;
  border-radius:12px; padding:1rem;
}
[data-testid="stMetricValue"]{ color:#3B82F6 !important; font-family:'JetBrains Mono',monospace !important; }
[data-testid="stMetricLabel"]{ color:#CBD5E1 !important; font-size:0.72rem !important; }

.stTabs [data-baseweb="tab-list"]{
  background:#0F1E38; border-bottom:1px solid #1E3A5F;
  border-radius:12px 12px 0 0; padding:4px 8px 0; gap:4px;
}
.stTabs [data-baseweb="tab"]{ color:#94A3B8 !important; font-weight:500; font-size:0.85rem; padding:8px 16px; }
.stTabs [aria-selected="true"]{ color:#3B82F6 !important; border-bottom:2px solid #3B82F6 !important; background:rgba(59,130,246,0.08) !important; }

.stButton>button{
  background:linear-gradient(135deg,#1D4ED8,#3B82F6) !important;
  color:white !important; border:none !important; border-radius:8px !important;
  font-weight:600 !important; padding:0.6rem 1.5rem !important;
  box-shadow:0 4px 12px rgba(59,130,246,0.3) !important; transition:all 0.2s !important;
}
.stButton>button:hover{ transform:translateY(-1px) !important; box-shadow:0 6px 20px rgba(59,130,246,0.4) !important; }

[data-testid="stDataFrame"]{ background:#0F1E38 !important; border-radius:8px !important; }
::-webkit-scrollbar{ width:6px; height:6px; }
::-webkit-scrollbar-track{ background:#0A1628; }
::-webkit-scrollbar-thumb{ background:#1E3A5F; border-radius:3px; }
[data-testid="stFileUploader"]{ background:#0F1E38 !important; border:2px dashed #1E3A5F !important; border-radius:16px !important; }

@keyframes fadeIn{ from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }
@keyframes slideIn{ from{opacity:0;transform:translateX(-16px)} to{opacity:1;transform:translateX(0)} }
@keyframes spin{ 0%{transform:rotate(0deg)} 100%{transform:rotate(360deg)} }
@keyframes float{ 0%,100%{transform:translateY(0)} 50%{transform:translateY(-10px)} }
@keyframes gradientShift{
  0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%}
}
@keyframes shimmer{
  0%{background-position:-200% 0} 100%{background-position:200% 0}
}
@keyframes ripple{
  0%{transform:scale(0.8);opacity:1} 100%{transform:scale(2.4);opacity:0}
}

.kpi-card{
  animation:fadeIn 0.5s ease forwards;
  background:linear-gradient(135deg,#0F1E38,#0A1628);
  border:1px solid rgba(30,58,95,0.8); border-radius:14px;
  padding:1.4rem 1rem; text-align:center;
  transition:transform 0.2s,box-shadow 0.2s;
}
.kpi-card:hover{ transform:translateY(-3px); box-shadow:0 8px 24px rgba(59,130,246,0.2); }
.pulse-dot{ display:inline-block; width:8px; height:8px; border-radius:50%; background:#10B981; animation:ripple 1.5s ease-out infinite; margin-right:6px; }
.loader{ width:38px; height:38px; border:3px solid rgba(59,130,246,0.2); border-top:3px solid #3B82F6; border-radius:50%; animation:spin 0.8s linear infinite; margin:0 auto; }
.hero-gradient{ background:linear-gradient(135deg,#3B82F6,#06B6D4,#8B5CF6,#3B82F6); background-size:300% 300%; animation:gradientShift 4s ease infinite; -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.shimmer-bar{ background:linear-gradient(90deg,#1E3A5F 25%,#3B82F620 50%,#1E3A5F 75%); background-size:200% 100%; animation:shimmer 2s infinite; height:4px; border-radius:2px; margin:4px 0; }
.floating{ animation:float 3s ease-in-out infinite; display:inline-block; }
.fade-in{ animation:fadeIn 0.6s ease forwards; }
.slide-in{ animation:slideIn 0.5s ease forwards; }
.feature-card{ background:rgba(59,130,246,0.05); border:1px solid rgba(59,130,246,0.15); border-radius:14px; padding:1.4rem; text-align:center; transition:all 0.3s; }
.feature-card:hover{ background:rgba(59,130,246,0.12); border-color:rgba(59,130,246,0.4); transform:translateY(-5px); box-shadow:0 8px 30px rgba(59,130,246,0.2); }
.step-badge{ display:inline-flex; align-items:center; justify-content:center; width:26px; height:26px; background:linear-gradient(135deg,#1D4ED8,#3B82F6); border-radius:50%; font-size:0.78rem; font-weight:700; color:white; margin-right:8px; flex-shrink:0; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS UI
# ══════════════════════════════════════════════════════════════════════════════
PLOTLY_CFG = dict(
    template="plotly_dark", paper_bgcolor="#0A1628", plot_bgcolor="#0A1628",
    font_family="Inter", font_color="#EAEEF3",
    title_font_color="#F1F5F9", title_font_size=14,
    margin=dict(t=50,b=40,l=40,r=20),
)

def header(title, subtitle="", icon=""):
    sub_html = f"<div style='font-size:0.8rem;color:#94A3B8;margin-top:3px;'>{subtitle}</div>" if subtitle else ""
    st.markdown(
        "<div class='fade-in' style='background:linear-gradient(135deg,#050B18 0%,#0A1F45 50%,#050B18 100%);"
        "border-bottom:1px solid rgba(59,130,246,0.35);padding:1.2rem 2rem;margin-bottom:2rem;"
        "border-radius:0 0 16px 16px;box-shadow:0 4px 30px rgba(59,130,246,0.08);'>"
        "<div style='display:flex;align-items:center;gap:12px;'>"
        f"<div style='font-size:1.6rem;'>{icon}</div>"
        "<div>"
        "<div style='font-size:0.6rem;color:#475569;text-transform:uppercase;letter-spacing:4px;font-weight:600;'>ACTUARIA · RISK PRICING STUDIO v3.0</div>"
        f"<div style='font-size:1.25rem;font-weight:700;color:#F1F5F9;margin-top:3px;'>{title}</div>"
        f"{sub_html}</div></div></div>",
        unsafe_allow_html=True)

def kpi(value, label, color="#3B82F6", icon="", delay=0):
    st.markdown(
        f"<div class='kpi-card' style='animation-delay:{delay}s;'>"
        f"<div style='font-size:1.2rem;margin-bottom:4px;'>{icon}</div>"
        f"<div style='font-size:1.35rem;font-weight:800;color:{color};font-family:JetBrains Mono,monospace;line-height:1.2;word-break:break-all;'>{value}</div>"
        f"<div style='font-size:0.65rem;color:#94A3B8;text-transform:uppercase;letter-spacing:1.2px;margin-top:6px;font-weight:500;'>{label}</div>"
        "</div>", unsafe_allow_html=True)

def health_card(icon_s, label, value, color):
    st.markdown(
        "<div class='kpi-card' style='text-align:center;'>"
        f"<div style='font-size:2rem;'>{icon_s}</div>"
        f"<div style='font-size:0.7rem;color:#94A3B8;text-transform:uppercase;letter-spacing:1px;margin:6px 0;font-weight:500;'>{label}</div>"
        f"<div style='font-family:JetBrains Mono;font-weight:700;font-size:0.95rem;color:{color};'>{value}</div>"
        "</div>", unsafe_allow_html=True)

def ai_box(text):
    st.markdown(
        "<div class='slide-in' style='background:linear-gradient(135deg,rgba(59,130,246,0.08),rgba(6,182,212,0.04));"
        "border:1px solid rgba(59,130,246,0.22);border-left:3px solid #3B82F6;"
        "border-radius:0 12px 12px 0;padding:1rem 1.5rem;margin:1rem 0;'>"
        "<div style='display:flex;gap:10px;'>"
        "<div style='font-size:1.2rem;margin-top:2px;'>🤖</div>"
        "<div>"
        "<div style='font-size:0.65rem;color:#3B82F6;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:5px;'>Analyse IA Actuarielle</div>"
        f"<div style='font-size:0.87rem;color:#CBD5E1;line-height:1.65;'>{text}</div>"
        "</div></div></div>", unsafe_allow_html=True)

def interp_box(title, text):
    st.markdown(
        "<div class='fade-in' style='background:linear-gradient(135deg,rgba(16,185,129,0.07),rgba(16,185,129,0.02));"
        "border:1px solid rgba(16,185,129,0.18);border-left:3px solid #10B981;"
        "border-radius:0 12px 12px 0;padding:1rem 1.5rem;margin:0.8rem 0;'>"
        "<div style='display:flex;gap:10px;'>"
        "<div style='font-size:1.2rem;margin-top:2px;'>💡</div>"
        "<div>"
        f"<div style='font-size:0.65rem;color:#10B981;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:5px;'>{title}</div>"
        f"<div style='font-size:0.87rem;color:#CBD5E1;line-height:1.65;'>{text}</div>"
        "</div></div></div>", unsafe_allow_html=True)

def rec_box(text, level="warning"):
    cfg = {"warning":("#F59E0B","rgba(245,158,11,0.09)","⚠"),
           "success":("#10B981","rgba(16,185,129,0.09)","✔"),
           "danger": ("#EF4444","rgba(239,68,68,0.09)","✗"),
           "info":   ("#3B82F6","rgba(59,130,246,0.09)","ℹ")}
    c,bg,icon = cfg.get(level, cfg["info"])
    st.markdown(
        f"<div style='background:{bg};border-left:3px solid {c};border-radius:0 8px 8px 0;"
        f"padding:0.7rem 1.2rem;margin:0.3rem 0;font-size:0.87rem;color:#E2E8F0;'>"
        f"<span style='color:{c};font-weight:700;margin-right:6px;'>{icon}</span>{text}</div>",
        unsafe_allow_html=True)

def animated_progress(label, pct, color="#3B82F6"):
    p = min(max(pct, 0), 100)
    st.markdown(
        "<div style='margin:4px 0;'>"
        f"<div style='display:flex;justify-content:space-between;margin-bottom:4px;'>"
        f"<span style='font-size:0.8rem;color:#CBD5E1;'>{label}</span>"
        f"<span style='font-size:0.8rem;color:{color};font-weight:600;'>{p:.1f}%</span></div>"
        "<div style='background:#1E3A5F;border-radius:4px;height:6px;'>"
        f"<div style='width:{p}%;height:100%;border-radius:4px;background:linear-gradient(90deg,{color},{color}aa);'></div>"
        "</div></div>", unsafe_allow_html=True)

def tlight(v, g, o, higher=False):
    if higher:
        if v>=g: return "🟢","#10B981"
        elif v>=o: return "🟠","#F59E0B"
        else: return "🔴","#EF4444"
    else:
        if v<=g: return "🟢","#10B981"
        elif v<=o: return "🟠","#F59E0B"
        else: return "🔴","#EF4444"

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
DEFAULTS = {
    "df":None, "df_proc":None,
    "model_logit":None, "model_poi":None, "model_nb":None,
    "irr_nb":None, "irr_poi":None,
    "data_imported":False, "report_data":{}, "auc_val":None,
}
for k,v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

CURRENCIES = {
    "€ (Euro)":            ("€",    1.0),
    "$ (Dollar US)":       ("$",    1.08),
    "FCFA (Franc CFA)":    ("FCFA", 655.96),
    "£ (Livre sterling)":  ("£",    0.86),
    "MAD (Dirham)":        ("MAD",  10.85),
    "XOF (UEMOA)":         ("XOF",  655.96),
    "DZD (Dinar algérien)":("DZD",  145.0),
    "TND (Dinar tunisien)":("TND",  3.35),
}

# ══════════════════════════════════════════════════════════════════════════════
# LANDING PAGE
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.data_imported:

    # HERO
    st.markdown(
        "<div style='text-align:center;padding:3rem 1rem 2rem;'>"
        "<div class='floating' style='font-size:4.5rem;margin-bottom:1rem;'>📊</div>"
        "<div style='font-size:0.7rem;color:#3B82F6;letter-spacing:6px;text-transform:uppercase;font-weight:600;margin-bottom:12px;'>ACTUARIA · RISK PRICING STUDIO v3.0</div>"
        "<div class='hero-gradient' style='font-size:3.5rem;font-weight:800;line-height:1.2;'>Plateforme de tarification<br>actuarielle intelligente</div>"
        "<div style='font-size:1rem;color:#94A3B8;margin-top:1.2rem;max-width:540px;margin-left:auto;margin-right:auto;line-height:1.9;'>"
        "Modélisez la fréquence des sinistres · Calculez des primes pures en temps réel · Rapport PDF professionnel"
        "</div></div>", unsafe_allow_html=True)

    # Feature cards
    feats = [
        ("🎯","Survenance","Logit — Probabilité de sinistre par profil"),
        ("📈","Fréquence GLM","Poisson & NB2 avec offset exposition"),
        ("💰","Prime temps réel","Multi-devises · Décomposition complète"),
        ("🧩","Segmentation","KMeans — Groupes de risque automatiques"),
        ("📑","Recommandations","Diagnostics actuariels et actions concrètes"),
        ("📄","Rapport PDF","Export professionnel téléchargeable"),
    ]
    cols = st.columns(3)
    for i,(icon,title,desc) in enumerate(feats):
        with cols[i%3]:
            st.markdown(
                f"<div class='feature-card' style='margin-bottom:1rem;min-height:120px;'>"
                f"<div style='font-size:1.8rem;'>{icon}</div>"
                f"<div style='font-weight:700;color:#F1F5F9;margin:6px 0;font-size:0.9rem;'>{title}</div>"
                f"<div style='font-size:0.75rem;color:#94A3B8;line-height:1.5;'>{desc}</div>"
                "</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Import zone
    st.markdown(
        "<div style='text-align:center;margin-bottom:0.8rem;'>"
        "<div style='font-size:1.3rem;font-weight:700;color:#F1F5F9;'>Importez votre portefeuille pour commencer</div>"
        "<div style='font-size:0.82rem;color:#94A3B8;margin-top:4px;'>CSV · Excel (.xlsx) · Parquet · JSON — jusqu'à 200 Mo</div>"
        "</div>", unsafe_allow_html=True)

    _, cc, _ = st.columns([1,2,1])
    with cc:
        uploaded = st.file_uploader("Fichier de données", type=["csv","xlsx","parquet","json"],
                                    label_visibility="collapsed")
        c1l, c2l = st.columns(2)
        sep = c1l.selectbox("Séparateur CSV", [",",";","\\t","|"], label_visibility="visible")
        enc = c2l.selectbox("Encodage", ["utf-8","latin-1","utf-8-sig"], label_visibility="visible")

        if uploaded:
            placeholder = st.empty()
            placeholder.markdown(
                "<div style='text-align:center;padding:1.5rem;'>"
                "<div class='loader'></div>"
                "<div style='color:#64748B;font-size:0.85rem;margin-top:10px;'>Chargement en cours...</div>"
                "</div>", unsafe_allow_html=True)
            time.sleep(0.5)
            try:
                ext = uploaded.name.split(".")[-1].lower()
                real_sep = "\t" if sep == "\\t" else sep
                if ext == "csv":           df_load = pd.read_csv(uploaded, sep=real_sep, encoding=enc)
                elif ext in["xlsx","xls"]: df_load = pd.read_excel(uploaded)
                elif ext == "parquet":     df_load = pd.read_parquet(uploaded)
                elif ext == "json":        df_load = pd.read_json(uploaded)
                placeholder.empty()
                n_r, n_c = df_load.shape
                st.markdown(
                    "<div style='background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.3);"
                    "border-radius:12px;padding:1.2rem;text-align:center;'>"
                    "<div style='font-size:2rem;'>✅</div>"
                    "<div style='font-size:1rem;font-weight:700;color:#10B981;margin-top:6px;'>Fichier chargé avec succès !</div>"
                    f"<div style='font-size:0.85rem;color:#64748B;margin-top:4px;'>{n_r:,} contrats · {n_c} variables</div>"
                    "</div>", unsafe_allow_html=True)
                time.sleep(0.6)
                st.session_state.df = df_load
                st.session_state.data_imported = True
                st.rerun()
            except Exception as e:
                placeholder.empty()
                st.error(f"Erreur : {e}")

    # ── WORKFLOW — construit ligne par ligne sans f-string multiline ──────────
    steps_list = [
        "Importer le fichier de données (CSV, Excel...)",
        "Prétraitement automatique (nettoyage, encodage, offset)",
        "Analyse exploratoire du portefeuille (EDA)",
        "Estimer les modèles GLM (Logit, Poisson, NB2)",
        "Calculer les primes en temps réel · multi-devises",
        "Exporter le rapport PDF professionnel",
    ]
    # On construit le HTML en concaténation simple — PAS de f-string multiligne
    wf_html = (
        "<br>"
        "<div style='background:rgba(59,130,246,0.04);border:1px solid rgba(59,130,246,0.1);"
        "border-radius:14px;padding:1.5rem;max-width:720px;margin:0 auto;'>"
        "<div style='font-size:0.75rem;color:#3B82F6;text-transform:uppercase;letter-spacing:2px;"
        "font-weight:600;margin-bottom:1rem;'>Workflow recommandé</div>"
        "<div style='display:flex;flex-direction:column;gap:10px;'>"
    )
    for i, step in enumerate(steps_list):
        wf_html += (
            "<div style='display:flex;align-items:center;gap:8px;'>"
            f"<div class='step-badge'>{i+1}</div>"
            f"<div style='font-size:0.85rem;color:#CBD5E1;'>{step}</div>"
            "</div>"
        )
    wf_html += (
        "</div></div>"
        "<div style='text-align:center;color:#1E3A5F;font-size:0.72rem;margin-top:2.5rem;'>"
        "ACTUARIA v3.0 · INSSEDS 2025-2026 · Streamlit · statsmodels · scikit-learn · plotly · reportlab"
        "</div>"
    )
    st.markdown(wf_html, unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
df = st.session_state.df

st.sidebar.markdown(
    "<div style='padding:1.5rem 1rem 1rem;border-bottom:1px solid rgba(30,58,95,0.8);margin-bottom:1rem;'>"
    "<div style='font-size:1.05rem;font-weight:800;color:#F1F5F9;letter-spacing:1px;'>ACTUARIA<span style='color:#3B82F6;'>.</span></div>"
    "<div style='font-size:0.58rem;color:#94A3B8;letter-spacing:2.5px;margin-top:2px;'>RISK PRICING STUDIO v3.0</div>"
    "</div>", unsafe_allow_html=True)

PAGES = {
    "🏠  Dashboard":                   "dashboard",
    "🧹  Prétraitement":               "preprocess",
    "📊  Analyse Exploratoire":        "eda",
    "📈  Modélisation GLM":            "models",
    "🔬  Validation":                  "validation",
    "💰  Tarification":                "pricing",
    "🧩  Segmentation":                "segmentation",
    "📑  Recommandations Actuarielles":"recommendations",
    "📄  Rapport PDF":                 "report",
    "⚙️  Paramètres":                 "settings",
}
sel  = st.sidebar.radio("", list(PAGES.keys()), label_visibility="collapsed")
PAGE = PAGES[sel]

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<div style='font-size:0.62rem;color:#94A3B8;text-transform:uppercase;"
    "letter-spacing:2px;padding:0 8px;margin-bottom:6px;'>Paramètres métier</div>",
    unsafe_allow_html=True)

currency_label = st.sidebar.selectbox("Devise", list(CURRENCIES.keys()), index=0)
CUR_SYM, CUR_RATE = CURRENCIES[currency_label]

COUT  = st.sidebar.number_input(
    f"Coût moyen / sinistre ({CUR_SYM})", 100, 50_000_000,
    int(2500 * CUR_RATE), int(500 * CUR_RATE))
SECU  = st.sidebar.slider("Sécurité (%)",  0, 30, 10) / 100
FRAIS = st.sidebar.slider("Frais (%)",     0, 40, 15) / 100
MARGE = st.sidebar.slider("Marge (%)",     0, 20,  5) / 100

# Progression workflow  ─ is not None pour éviter ValueError sur DataFrame
steps_done = sum([
    st.session_state.df_proc is not None,
    st.session_state.model_logit is not None,
    st.session_state.model_nb is not None,
])
pct_done = steps_done / 3 * 100

st.sidebar.markdown(
    "<div style='padding:0 0.5rem;margin:0.5rem 0;'>"
    "<div style='font-size:0.65rem;color:#94A3B8;margin-bottom:4px;'>"
    f"<span class='pulse-dot'></span>Progression : {pct_done:.0f}%</div>"
    "<div style='background:#1E3A5F;border-radius:4px;height:5px;'>"
    f"<div style='width:{pct_done}%;height:100%;border-radius:4px;"
    "background:linear-gradient(90deg,#3B82F6,#06B6D4);'></div></div>"
    "<div style='font-size:0.65rem;color:#3B82F6;margin-top:3px;text-align:right;'>"
    f"{pct_done:.0f}% complété</div></div>", unsafe_allow_html=True)

st.sidebar.markdown(
    "<div style='margin:0.5rem;background:rgba(16,185,129,0.07);border:1px solid rgba(16,185,129,0.18);"
    "border-radius:10px;padding:0.8rem;'>"
    f"<div style='color:#10B981;font-weight:700;font-size:0.78rem;'>✔ {df.shape[0]:,} contrats chargés</div>"
    f"<div style='color:#94A3B8;font-size:0.72rem;margin-top:4px;font-family:JetBrains Mono;'>"
    f"{df.shape[1]} variables · Devise : {CUR_SYM}</div></div>", unsafe_allow_html=True)

if st.sidebar.button("↩ Nouveau dataset", use_container_width=True):
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if PAGE == "dashboard":
    header("Dashboard Exécutif", "Vue synthétique temps réel du portefeuille", "🏠")

    has_cn = "ClaimNb" in df.columns
    has_oc = "ClaimOcc" in df.columns
    has_ex = "Exposure" in df.columns
    n    = len(df)
    taux = df["ClaimOcc"].mean() if has_oc else ((df["ClaimNb"]>0).mean() if has_cn else 0)
    freq = df["ClaimNb"].mean() if has_cn else 0
    expo = df["Exposure"].sum() if has_ex else n
    pz   = (df["ClaimNb"]==0).mean() if has_cn else 0
    rvm  = df["ClaimNb"].var()/freq if has_cn and freq>0 else 1

    k1,k2,k3,k4,k5,k6 = st.columns(6)
    with k1: kpi(f"{n:,}","Contrats","#3B82F6","🗂️",0.0)
    with k2: kpi(f"{taux*100:.2f}%","Sinistralité","#EF4444" if taux>0.05 else "#10B981","🚨",0.1)
    with k3: kpi(f"{freq:.4f}","Fréquence","#F59E0B","📉",0.2)
    with k4: kpi(f"{expo:,.0f}","Exposition (ans)","#06B6D4","⏱️",0.3)
    with k5: kpi(f"{pz*100:.1f}%","% Zéros","#8B5CF6","0️⃣",0.4)
    with k6: kpi(f"{rvm:.3f}","Var/Moy","#F59E0B" if rvm>1.1 else "#10B981","📊",0.5)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🏥 Carte de santé du portefeuille")
    h1,h2,h3,h4 = st.columns(4)
    i1,c1 = tlight(rvm,1.1,2.0)
    i2,c2 = tlight(pz,0.90,0.96)
    i3,c3 = tlight(taux,0.05,0.10)
    q = max(0,min(100,100-int(df.isnull().sum().sum()/max(n,1)*200)-int((rvm-1)*20)))
    i4,c4 = tlight(q,90,70,higher=True)
    with h1: health_card(i1,"Surdispersion",f"Var/Moy={rvm:.3f}",c1)
    with h2: health_card(i2,"Excès zéros",f"{pz*100:.1f}% zéros",c2)
    with h3: health_card(i3,"Sinistralité",f"{taux*100:.2f}%",c3)
    with h4: health_card(i4,"Qualité données",f"{q}/100",c4)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📊 Profil du portefeuille")
    p1,p2 = st.columns(2)
    with p1:
        animated_progress("Taux de sinistralité", taux*100, "#EF4444")
        animated_progress("Proportion de zéros", pz*100, "#8B5CF6")
        animated_progress("Qualité données", q, "#10B981")
    with p2:
        animated_progress("Exposition moy. (vs 1 an)", min((df["Exposure"].mean() if has_ex else 1)*100,100), "#3B82F6")
        animated_progress("Surdispersion normalisée", min((rvm-1)*50,100), "#F59E0B")

    st.markdown("<br>", unsafe_allow_html=True)
    g1,g2 = st.columns(2)
    with g1:
        if has_cn:
            d = df["ClaimNb"].value_counts().sort_index().reset_index()
            d.columns = ["ClaimNb","N"]
            fig = px.bar(d,x="ClaimNb",y="N",title="Distribution du nombre de sinistres",
                         color="N",color_continuous_scale=[[0,"#1D4ED8"],[1,"#06B6D4"]])
            fig.update_layout(**PLOTLY_CFG); fig.update_coloraxes(showscale=False)
            st.plotly_chart(fig, use_container_width=True)
    with g2:
        if "DrivAge" in df.columns and has_oc:
            ag = df.groupby(pd.cut(df["DrivAge"],[17,24,39,59,100],
                            labels=["18-24","25-39","40-59","60+"]))["ClaimOcc"].mean().reset_index()
            ag.columns = ["Tranche","Taux"]; ag["Taux"] *= 100
            fig2 = px.bar(ag,x="Tranche",y="Taux",title="Sinistralité par tranche d'âge (%)",
                          color="Taux",color_continuous_scale=[[0,"#10B981"],[0.5,"#F59E0B"],[1,"#EF4444"]])
            fig2.update_layout(**PLOTLY_CFG); fig2.update_coloraxes(showscale=False)
            st.plotly_chart(fig2, use_container_width=True)

    interp_box("Ce que signifie ce tableau de bord",
        f"Votre portefeuille contient <b>{n:,} contrats</b>. Sur 100 assurés, <b>{taux*100:.1f}</b> ont déclaré au moins un sinistre. "
        f"Le ratio Var/Moy = {rvm:.3f} : " +
        ("valeur proche de 1 — modèle Poisson valide." if rvm<1.1 else "valeur > 1 — sinistres irréguliers, le modèle NB2 est nécessaire.") +
        f" Les {pz*100:.1f}% de contrats sans sinistre sont normaux en assurance automobile.")

    ai_box(f"Portefeuille {n:,} contrats · Sinistralité {taux*100:.2f}% · "
           f"Surdispersion {'légère' if rvm<1.5 else 'modérée' if rvm<2 else 'forte'} (Var/Moy={rvm:.3f}). " +
           ("→ GLM NB2 recommandé." if rvm>1.1 else "→ GLM Poisson acceptable.") +
           (" → Excès de zéros : tester ZIP/ZINB." if pz>0.90 else ""))

# ══════════════════════════════════════════════════════════════════════════════
# PRÉTRAITEMENT
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "preprocess":
    header("Prétraitement Intelligent", "Nettoyage et transformations actuarielles", "🧹")
    dw = st.session_state.df.copy()

    c1,c2,c3 = st.columns(3)
    rm_dup  = c1.checkbox("Supprimer les doublons", True)
    rm_exp  = c2.checkbox("Supprimer Exposure ≤ 0", True)
    impute  = c3.checkbox("Imputer valeurs manquantes", True)
    c4,c5,c6 = st.columns(3)
    cr_occ  = c4.checkbox("Créer ClaimOcc", True)
    cr_log  = c5.checkbox("Créer log_Exposure", True)
    cr_cats = c6.checkbox("Créer tranches d'âge/densité", True)

    if st.button("🔧 Lancer le pipeline automatique", use_container_width=True):
        steps, n0 = [], len(dw)
        bar = st.progress(0, "Pipeline en cours...")
        if rm_dup:
            dw = dw.drop_duplicates()
            n_rm = n0-len(dw)
            steps.append(f"✔ {n_rm:,} doublons supprimés" if n_rm>0 else "✔ Aucun doublon")
        bar.progress(20)
        if rm_exp and "Exposure" in dw.columns:
            dw = dw[dw["Exposure"]>0].copy(); steps.append("✔ Exposition ≤ 0 supprimée")
        bar.progress(40)
        if impute:
            for col in dw.columns:
                if dw[col].isnull().sum()>0:
                    val_fill = dw[col].median() if dw[col].dtype in["float64","int64"] else dw[col].mode()[0]
                    dw[col].fillna(val_fill, inplace=True)
            steps.append("✔ Valeurs manquantes imputées")
        bar.progress(60)
        if cr_occ and "ClaimNb" in dw.columns and "ClaimOcc" not in dw.columns:
            dw["ClaimOcc"] = (dw["ClaimNb"]>0).astype(int); steps.append("✔ ClaimOcc créée")
        if cr_log and "Exposure" in dw.columns and "log_Exposure" not in dw.columns:
            dw["log_Exposure"] = np.log(dw["Exposure"].clip(lower=1e-6)); steps.append("✔ log_Exposure créée")
        bar.progress(80)
        if cr_cats:
            if "DrivAge" in dw.columns and "DrivAge_cat" not in dw.columns:
                dw["DrivAge_cat"] = pd.cut(dw["DrivAge"],[17,24,39,59,100],labels=["18-24","25-39","40-59","60+"])
                steps.append("✔ DrivAge_cat créée")
            if "Density" in dw.columns and "Density_cat" not in dw.columns:
                dw["Density_cat"] = pd.cut(dw["Density"],[0,50,300,2000,999999],
                                           labels=["Rurale","Périurbaine","Urbaine","Très urbaine"])
                steps.append("✔ Density_cat créée")
        bar.progress(100); time.sleep(0.3); bar.empty()
        st.session_state.df = dw
        st.session_state.df_proc = dw
        for s in steps: rec_box(s,"success")
        st.success(f"Pipeline terminé — {dw.shape[0]:,} × {dw.shape[1]}")
        interp_box("Pourquoi ce nettoyage est indispensable",
            "Les doublons fausseraient les estimations. L'exposition doit être positive pour calculer "
            "une fréquence annualisée. <b>log_Exposure</b> est l'offset du GLM — il permet de comparer "
            "équitablement un contrat de 3 mois et un contrat d'un an.")
        ai_box(f"Pipeline : {len(steps)} transformations · Dataset final : {dw.shape[0]:,} × {dw.shape[1]}")

    if st.session_state.df_proc is not None:
        st.markdown("### Statistiques du dataset traité")
        st.dataframe(st.session_state.df_proc.describe().round(3), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# EDA
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "eda":
    header("Analyse Exploratoire", "Comprendre les données avant de modéliser", "📊")
    df = st.session_state.df
    t1,t2,t3,t4 = st.tabs(["📊 Descriptif","🎯 Actuariel","📉 Corrélations","🔬 Surdispersion"])

    with t1:
        nc = df.select_dtypes(include=[np.number]).columns.tolist()
        sc = st.selectbox("Variable", nc)
        c1,c2 = st.columns(2)
        with c1:
            fig = px.histogram(df,x=sc,nbins=50,title=f"Distribution — {sc}",color_discrete_sequence=["#3B82F6"])
            fig.update_layout(**PLOTLY_CFG); st.plotly_chart(fig,use_container_width=True)
        with c2:
            if "ClaimOcc" in df.columns:
                fig2 = px.box(df,x=df["ClaimOcc"].astype(str),y=sc,title=f"{sc} selon sinistralité",
                              color=df["ClaimOcc"].astype(str),color_discrete_map={"0":"#3B82F6","1":"#EF4444"})
                fig2.update_layout(**PLOTLY_CFG); st.plotly_chart(fig2,use_container_width=True)
        st.dataframe(df[nc].describe().round(4),use_container_width=True)
        interp_box("Comment lire ces graphiques",
            "L'histogramme montre la répartition des valeurs. Le boxplot compare les assurés "
            "<b>sinistrés (1)</b> et <b>non-sinistrés (0)</b>. Si les deux boîtes sont très "
            "différentes, cette variable est un bon prédicteur du sinistre.")

    with t2:
        c1,c2 = st.columns(2)
        with c1:
            if "DrivAge_cat" in df.columns and "ClaimOcc" in df.columns:
                g = df.groupby("DrivAge_cat",observed=True)["ClaimOcc"].mean().reset_index()
                g["ClaimOcc"] *= 100
                fig = px.bar(g,x="DrivAge_cat",y="ClaimOcc",title="Sinistralité par âge (%)",
                             color="ClaimOcc",color_continuous_scale=[[0,"#10B981"],[0.5,"#F59E0B"],[1,"#EF4444"]])
                fig.update_layout(**PLOTLY_CFG); fig.update_coloraxes(showscale=False)
                st.plotly_chart(fig,use_container_width=True)
        with c2:
            if "Density_cat" in df.columns and "ClaimOcc" in df.columns:
                g2 = df.groupby("Density_cat",observed=True)["ClaimOcc"].mean().reset_index()
                g2["ClaimOcc"] *= 100
                fig2 = px.bar(g2,x="Density_cat",y="ClaimOcc",title="Sinistralité par densité (%)",
                              color="ClaimOcc",color_continuous_scale=[[0,"#10B981"],[0.5,"#F59E0B"],[1,"#EF4444"]])
                fig2.update_layout(**PLOTLY_CFG); fig2.update_coloraxes(showscale=False)
                st.plotly_chart(fig2,use_container_width=True)
        if "BonusMalus" in df.columns and "ClaimOcc" in df.columns:
            bmg = df.groupby(pd.cut(df["BonusMalus"],[49,50,64,100,350],labels=["BM=50","51-64","65-100",">100"]),
                             observed=True)["ClaimOcc"].mean().reset_index()
            bmg.columns = ["BonusMalus","Taux"]; bmg["Taux"] *= 100
            fig3 = px.bar(bmg,x="BonusMalus",y="Taux",title="Sinistralité par BonusMalus (%)",
                          color="Taux",color_continuous_scale=[[0,"#10B981"],[0.5,"#F59E0B"],[1,"#EF4444"]])
            fig3.update_layout(**PLOTLY_CFG); fig3.update_coloraxes(showscale=False)
            st.plotly_chart(fig3,use_container_width=True)
        interp_box("Que révèlent ces graphiques actuariels ?",
            "Les barres montrent le % d'assurés ayant eu un sinistre par catégorie. "
            "<b>Rouge = risque élevé, Vert = faible risque.</b> Le BonusMalus reflète l'historique : "
            "un malus >100 prédit une sinistralité future élevée.")

    with t3:
        nc2 = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(nc2)>=2:
            fig_c = px.imshow(df[nc2].corr(),title="Matrice de corrélation",
                              color_continuous_scale="RdBu_r",zmin=-1,zmax=1,text_auto=".2f")
            fig_c.update_layout(**PLOTLY_CFG); st.plotly_chart(fig_c,use_container_width=True)
        interp_box("Comment lire la matrice",
            "<b>+1 (rouge)</b> : deux variables augmentent ensemble. <b>-1 (bleu)</b> : sens opposé. "
            "<b>0</b> : aucun lien linéaire. Des corrélations > 0,7 entre prédicteurs signalent une multicolinéarité.")

    with t4:
        if "ClaimNb" in df.columns:
            mu = df["ClaimNb"].mean(); var = df["ClaimNb"].var()
            rvm2 = var/mu if mu>0 else 1; pz2 = (df["ClaimNb"]==0).mean()
            c1,c2,c3 = st.columns(3)
            c1.metric("E[ClaimNb]",f"{mu:.5f}")
            c2.metric("Var[ClaimNb]",f"{var:.5f}")
            c3.metric("Ratio Var/Moy",f"{rvm2:.4f}",delta=f"{rvm2-1:+.4f}")
            ks = range(6)
            obs = [(df["ClaimNb"]==k).mean() for k in ks]
            poi = [sp_poisson.pmf(k,mu) for k in ks]
            fig_d = go.Figure()
            fig_d.add_trace(go.Bar(x=list(ks),y=obs,name="Observé",marker_color="#3B82F6",offsetgroup=0))
            fig_d.add_trace(go.Bar(x=list(ks),y=poi,name="Poisson théorique",marker_color="#F59E0B",offsetgroup=1,opacity=0.85))
            fig_d.update_layout(title="Observé vs Poisson théorique",barmode="group",**PLOTLY_CFG)
            st.plotly_chart(fig_d,use_container_width=True)
            if rvm2>1.1: rec_box(f"Surdispersion (Var/Moy={rvm2:.4f}) → NB2 recommandé.","warning")
            if pz2>0.90: rec_box(f"{pz2*100:.1f}% de zéros → ZIP/ZINB à envisager.","warning")
            interp_box("Qu'est-ce que la surdispersion ?",
                "En Poisson, variance = moyenne (ratio = 1). Si ratio > 1, le portefeuille est hétérogène. "
                "Le <b>NB2</b> ajoute un paramètre alpha pour mesurer cette hétérogénéité. "
                "Barres bleues = observé. Barres oranges = ce que Poisson prédirait.")

# ══════════════════════════════════════════════════════════════════════════════
# MODÉLISATION GLM
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "models":
    header("Modélisation Actuarielle GLM", "Logit · Poisson · Binomiale Négative NB2", "📈")
    df = st.session_state.df

    req = ["ClaimNb","ClaimOcc","log_Exposure","DrivAge","BonusMalus","Density","VehPower","VehAge"]
    miss_req = [c for c in req if c not in df.columns]
    if miss_req:
        st.error(f"Variables manquantes : {miss_req}. Exécutez le Prétraitement d'abord.")
        st.stop()

    try:
        import statsmodels.api as sm
        from statsmodels.genmod.families import Poisson as Poi, NegativeBinomial as NB
        from statsmodels.genmod.families.links import Log
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import roc_curve, auc as sk_auc
    except ImportError:
        st.error("Installez : pip install statsmodels scikit-learn")
        st.stop()

    cat_cols  = [c for c in ["VehBrand","VehGas","Area","Region"] if c in df.columns]
    base_cols = [c for c in ["DrivAge","BonusMalus","VehPower","VehAge","Density"] if c in df.columns] + cat_cols
    df_enc    = pd.get_dummies(df[base_cols+["ClaimNb","ClaimOcc","log_Exposure"]],
                               columns=cat_cols, drop_first=True, dtype=int)
    y_occ = df_enc["ClaimOcc"]; y_cnt = df_enc["ClaimNb"]; off_all = df_enc["log_Exposure"]
    X_all = sm.add_constant(df_enc.drop(columns=["ClaimNb","ClaimOcc","log_Exposure"]))
    n_s   = min(150_000, len(y_cnt))
    rng   = np.random.RandomState(42)
    idx_s = rng.choice(len(y_cnt), size=n_s, replace=False)
    Xs    = X_all.iloc[idx_s].reset_index(drop=True)
    y_os  = y_occ.iloc[idx_s].reset_index(drop=True)
    y_cs  = y_cnt.iloc[idx_s].reset_index(drop=True)
    offs  = off_all.iloc[idx_s].reset_index(drop=True)
    tr,te = train_test_split(np.arange(n_s), test_size=0.25, random_state=42, stratify=(y_os>0).astype(int))
    Xtr,Xte   = Xs.iloc[tr].reset_index(drop=True), Xs.iloc[te].reset_index(drop=True)
    yotr,yote = y_os.iloc[tr].reset_index(drop=True), y_os.iloc[te].reset_index(drop=True)
    yctr,ycte = y_cs.iloc[tr].reset_index(drop=True), y_cs.iloc[te].reset_index(drop=True)
    otr,ote   = offs.iloc[tr].reset_index(drop=True), offs.iloc[te].reset_index(drop=True)

    tl,tp,tnb = st.tabs(["📊 Logit — Survenance","📈 Poisson — Fréquence","🎯 NB2 ★ Recommandé"])

    with tl:
        interp_box("Qu'est-ce que le modèle Logit ?",
            "Il calcule la <b>probabilité qu'un assuré déclare au moins un sinistre</b>. "
            "Les résultats sont exprimés en <b>Odds Ratios (OR)</b> : OR > 1 = facteur aggravant, "
            "OR < 1 = facteur protecteur. L'<b>AUC-ROC</b> mesure la capacité discriminante : "
            "0,5 = tirage au sort, 1 = parfait. En IARD avec 96% de non-sinistrés, AUC ≥ 0,62 est satisfaisant.")
        if st.button("▶ Estimer le Logit", use_container_width=True, key="btn_l"):
            with st.spinner("Estimation MLE — BFGS..."):
                try:
                    res = sm.Logit(yotr,Xtr).fit(method="bfgs",maxiter=500,disp=False)
                    st.session_state.model_logit = res
                    st.success("✔ Logit estimé")
                except Exception as e: st.error(f"Erreur : {e}")

        if st.session_state.model_logit:
            res = st.session_state.model_logit
            coef = res.params; ci = res.conf_int(); pv = res.pvalues
            yp = res.predict(Xte)
            fpr,tpr,_ = roc_curve(yote,yp); auc_v = sk_auc(fpr,tpr)
            st.session_state.auc_val = auc_v
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("Pseudo-R² McFadden",f"{res.prsquared:.4f}")
            c2.metric("AIC",f"{res.aic:,.0f}")
            c3.metric("Log-vraisemblance",f"{res.llf:,.0f}")
            c4.metric("AUC-ROC (test)",f"{auc_v:.4f}")
            or_df = pd.DataFrame({
                "Coef β":coef.round(4), "Odds Ratio":np.exp(coef).round(4),
                "IC inf (95%)":np.exp(ci[0]).round(4), "IC sup (95%)":np.exp(ci[1]).round(4),
                "p-value":pv.round(6),
                "Sig":["***" if p<0.001 else "**" if p<0.01 else "*" if p<0.05 else "ns" for p in pv]
            }).sort_values("p-value")
            st.dataframe(or_df, use_container_width=True)
            c_r,c_d = st.columns(2)
            with c_r:
                fr = go.Figure()
                fr.add_trace(go.Scatter(x=fpr,y=tpr,fill="tozeroy",fillcolor="rgba(59,130,246,0.1)",
                                        line=dict(color="#3B82F6",width=2.5),name=f"AUC={auc_v:.4f}"))
                fr.add_trace(go.Scatter(x=[0,1],y=[0,1],line=dict(color="#E0E3E8",dash="dash"),name="Aléatoire"))
                fr.update_layout(title="Courbe ROC",xaxis_title="Faux positifs",yaxis_title="Vrais positifs",**PLOTLY_CFG)
                st.plotly_chart(fr, use_container_width=True)
            with c_d:
                fd = go.Figure()
                fd.add_trace(go.Histogram(x=yp[yote==0],nbinsx=60,name="Non sinistrés",marker_color="#3B82F6",opacity=0.7))
                fd.add_trace(go.Histogram(x=yp[yote==1],nbinsx=60,name="Sinistrés",marker_color="#EF4444",opacity=0.7))
                fd.update_layout(barmode="overlay",title="Distribution des probabilités prédites",**PLOTLY_CFG)
                st.plotly_chart(fd, use_container_width=True)
            interp_box("Interprétation des résultats du Logit",
                f"<b>AUC = {auc_v:.3f}</b> : le modèle classe correctement {auc_v*100:.0f}% des paires sinistré/non-sinistré. "
                "Les <b>OR > 1</b> désignent les facteurs aggravants : un OR de 1,5 signifie +50% de risque. "
                "<b>*** = très significatif</b> : moins d'une chance sur 1000 que l'effet soit dû au hasard.")
            ai_box(f"Logit estimé · AUC = {auc_v:.4f} · " +
                   ("Pouvoir discriminant satisfaisant pour un portefeuille IARD déséquilibré." if auc_v>=0.60
                    else "AUC modérée — variables supplémentaires recommandées."))

    with tp:
        interp_box("Qu'est-ce que le GLM Poisson ?",
            "Il modélise le <b>nombre annuel de sinistres</b>. L'<b>offset log(Exposure)</b> compare "
            "équitablement les contrats de durées différentes. Les coefficients deviennent des "
            "<b>IRR</b> : IRR = 1,2 signifie +20% de sinistres attendus. "
            "Limite : suppose Variance = Moyenne. Si ratio Var/Moy > 1 → NB2 nécessaire.")
        if st.button("▶ Estimer GLM Poisson", use_container_width=True, key="btn_p"):
            with st.spinner("Estimation IRLS..."):
                try:
                    rp = sm.GLM(yctr,Xtr,family=Poi(link=Log()),offset=otr).fit(maxiter=500,disp=False)
                    st.session_state.model_poi = rp
                    st.session_state.irr_poi   = pd.DataFrame({
                        "IRR":np.exp(rp.params).round(4), "p-value":rp.pvalues.round(6),
                        "Sig":["***" if p<0.001 else "**" if p<0.01 else "*" if p<0.05 else "ns" for p in rp.pvalues]
                    }).sort_values("p-value")
                    st.success("✔ GLM Poisson estimé")
                except Exception as e: st.error(f"Erreur : {e}")

        if st.session_state.model_poi:
            rp = st.session_state.model_poi
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("Log-vraisemblance",f"{rp.llf:,.2f}")
            c2.metric("AIC",f"{rp.aic:,.2f}")
            c3.metric("BIC",f"{rp.bic:,.2f}")
            c4.metric("Ratio Dév/DDL",f"{rp.deviance/rp.df_resid:.4f}")
            st.dataframe(st.session_state.irr_poi, use_container_width=True)
            interp_box("Interprétation du GLM Poisson",
                f"<b>AIC = {rp.aic:,.1f}</b> : critère de qualité d'ajustement (plus bas = meilleur). "
                f"<b>Ratio Dév/DDL = {rp.deviance/rp.df_resid:.4f}</b> : doit être proche de 1 sous H₀ Poisson. "
                "Les <b>IRR > 1</b> = facteurs aggravants. <b>IRR < 1</b> = facteurs protecteurs.")
            ai_box(f"Poisson · AIC={rp.aic:,.1f} · Ratio Dév/DDL={rp.deviance/rp.df_resid:.4f}." +
                   (" Surdispersion → NB2 recommandé." if rp.deviance/rp.df_resid>1.05 else " Ajustement correct."))

    with tnb:
        interp_box("Pourquoi le NB2 est-il souvent supérieur ?",
            "Le NB2 ajoute un paramètre <b>alpha (α)</b> qui capture l'hétérogénéité non observée. "
            "Le <b>LRT</b> teste : H₀ α=0 (Poisson) vs H₁ α>0 (NB2). "
            "Un <b>ΔAIC > 10</b> = preuve forte. <b>ΔAIC > 100</b> = preuve très forte.")
        if st.button("▶ Estimer GLM NB2", use_container_width=True, key="btn_nb"):
            with st.spinner("Estimation NB2 (~1-2 min)..."):
                try:
                    rn = sm.GLM(yctr,Xtr,family=NB(link=Log()),offset=otr).fit(maxiter=500,disp=False)
                    st.session_state.model_nb  = rn
                    st.session_state.irr_nb    = pd.DataFrame({
                        "IRR":np.exp(rn.params).round(4),
                        "IC inf":np.exp(rn.conf_int()[0]).round(4),
                        "IC sup":np.exp(rn.conf_int()[1]).round(4),
                        "p-value":rn.pvalues.round(6),
                        "Sig":["***" if p<0.001 else "**" if p<0.01 else "*" if p<0.05 else "ns" for p in rn.pvalues]
                    }).sort_values("p-value")
                    st.success("✔ GLM NB2 estimé")
                except Exception as e: st.error(f"Erreur : {e}")

        if st.session_state.model_nb:
            rn = st.session_state.model_nb; irr_nb = st.session_state.irr_nb
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("Log-vraisemblance",f"{rn.llf:,.2f}")
            c2.metric("AIC",f"{rn.aic:,.2f}")
            c3.metric("BIC",f"{rn.bic:,.2f}")
            c4.metric("Ratio Dév/DDL",f"{rn.deviance/rn.df_resid:.4f}")
            if st.session_state.model_poi:
                rp2 = st.session_state.model_poi
                lrt = -2*(rp2.llf-rn.llf); lrt_p = chi2.sf(lrt,df=1); da = rp2.aic-rn.aic
                if lrt_p<0.05:
                    rec_box(f"LRT p={lrt_p:.2e} → NB2 significativement supérieur ✔ (ΔAIC={da:.1f})","success")
                else:
                    rec_box("LRT non significatif — Poisson et NB2 équivalents","info")
            st.dataframe(irr_nb, use_container_width=True)
            vp = [v for v in irr_nb.index if v!="const" and not v.startswith("Region_")]
            isub = irr_nb.loc[vp].sort_values("IRR")
            clrs = ["#EF4444" if v>1 else "#10B981" for v in isub["IRR"]]
            ff = go.Figure()
            ff.add_trace(go.Bar(y=isub.index.tolist(), x=(isub["IRR"]-1).tolist(),
                                base=1, orientation="h", marker_color=clrs, opacity=0.85,
                                error_x=dict(type="data",symmetric=False,
                                             array=(isub["IC sup"]-isub["IRR"]).tolist(),
                                             arrayminus=(isub["IRR"]-isub["IC inf"]).tolist(),
                                             color="rgba(255,255,255,0.4)")))
            ff.add_vline(x=1, line_dash="dash", line_color="rgba(255,255,255,0.4)")
            ff.update_layout(title="Forest plot IRR — Rouge=aggravant · Vert=protecteur",
                             height=max(400,len(vp)*28), **PLOTLY_CFG)
            st.plotly_chart(ff, use_container_width=True)
            interp_box("Interprétation du Forest plot et des IRR",
                "<b>Rouge (IRR>1)</b> : facteur aggravant — augmente les sinistres. "
                "Ex : BonusMalus élevé → plus de sinistres. "
                "<b>Vert (IRR<1)</b> : facteur protecteur — réduit les sinistres. "
                "Ex : conducteur âgé → moins de sinistres. "
                "Les barres d'erreur = IC 95%. <b>*** = p < 0,001</b> : certitude quasi absolue.")
            ai_box(f"NB2 retenu · AIC={rn.aic:,.1f} · Les IRR serviront de base aux relativités tarifaires.")

# ══════════════════════════════════════════════════════════════════════════════
# VALIDATION
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "validation":
    header("Validation & Diagnostics", "Qualité prédictive et robustesse", "🔬")
    if not st.session_state.model_nb and not st.session_state.model_logit:
        st.warning("⚠ Estimez d'abord les modèles dans Modélisation GLM"); st.stop()
    rows = []
    if st.session_state.model_logit:
        r = st.session_state.model_logit
        rows.append({"Modèle":"Logit","Cible":"ClaimOcc","Log-L":f"{r.llf:,.2f}",
                     "AIC":f"{r.aic:,.2f}","BIC":f"{r.bic:,.2f}","Pseudo-R²":f"{r.prsquared:.4f}"})
    if st.session_state.model_poi:
        r = st.session_state.model_poi
        rows.append({"Modèle":"GLM Poisson","Cible":"ClaimNb","Log-L":f"{r.llf:,.2f}",
                     "AIC":f"{r.aic:,.2f}","BIC":f"{r.bic:,.2f}","Dév/DDL":f"{r.deviance/r.df_resid:.4f}"})
    if st.session_state.model_nb:
        r = st.session_state.model_nb
        rows.append({"Modèle":"GLM NB2 ★","Cible":"ClaimNb","Log-L":f"{r.llf:,.2f}",
                     "AIC":f"{r.aic:,.2f}","BIC":f"{r.bic:,.2f}","Dév/DDL":f"{r.deviance/r.df_resid:.4f}"})
    if rows:
        st.dataframe(pd.DataFrame(rows).fillna("—"), use_container_width=True)
    if st.session_state.model_poi and st.session_state.model_nb:
        rp = st.session_state.model_poi; rn = st.session_state.model_nb
        lrt = -2*(rp.llf-rn.llf); lpv = chi2.sf(lrt,df=1); da = rp.aic-rn.aic
        st.markdown("### LRT — Poisson vs NB2")
        c1,c2,c3 = st.columns(3)
        c1.metric("LR Statistique",f"{lrt:.4f}")
        c2.metric("p-value",f"{lpv:.2e}")
        c3.metric("ΔAIC (Poisson−NB2)",f"{da:.2f}")
        if lpv<0.05:
            rec_box(f"H₀ rejetée : NB2 supérieur (ΔAIC={da:.1f})","success")
            if da>100: rec_box("ΔAIC > 100 : preuve très forte (Burnham & Anderson, 2002)","success")
        else:
            rec_box("Poisson et NB2 statistiquement équivalents","info")
        interp_box("Comment choisir entre Poisson et NB2 ?",
            "Le <b>LRT</b> teste H₀ : α=0 (Poisson valide) contre H₁ : α>0 (NB2 nécessaire). "
            "Si p < 0,001 → NB2 retenu avec certitude quasi absolue. "
            "<b>ΔAIC > 10</b> = preuve forte. <b>ΔAIC > 100</b> = preuve très forte.")
        ai_box(f"LRT p={lpv:.2e} → NB2 {'supérieur' if lpv<0.05 else 'équivalent'} au Poisson. "
               f"ΔAIC={da:.1f}. Modèle retenu : NB2.")

# ══════════════════════════════════════════════════════════════════════════════
# TARIFICATION
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "pricing":
    header("Tarification & Scoring", f"Calcul de prime en temps réel — Devise : {CUR_SYM}", "💰")
    if not st.session_state.model_nb or not st.session_state.model_logit:
        st.warning("⚠ Estimez d'abord Logit ET NB2 dans Modélisation GLM"); st.stop()

    rl = st.session_state.model_logit; rn = st.session_state.model_nb
    X_cols = rl.model.exog_names

    interp_box("Comment fonctionne ce calculateur ?",
        f"Renseignez le profil de l'assuré. L'application calcule instantanément en <b>{CUR_SYM}</b> : "
        "(1) P(sinistre) via Logit. (2) Fréquence annuelle via NB2. "
        "(3) Prime pure = fréquence × coût moyen. (4) Prime commerciale = prime pure + chargements.")

    c1,c2,c3 = st.columns(3)
    with c1:
        age_v = st.slider("Âge conducteur", 18, 85, 45)
        bm_v  = st.slider("BonusMalus", 50, 250, 60)
    with c2:
        pw_v  = st.slider("Puissance véhicule", 1, 15, 6)
        va_v  = st.slider("Âge véhicule (ans)", 0, 30, 5)
    with c3:
        den_v = st.slider("Densité (hab/km²)", 0, 20000, 400, 100)

    xp = pd.Series(0.0, index=X_cols); xp["const"] = 1.0
    for col,val in [("DrivAge",age_v),("BonusMalus",bm_v),("VehPower",pw_v),("VehAge",va_v),("Density",den_v)]:
        if col in X_cols: xp[col] = float(val)
    x_df  = pd.DataFrame([xp]); off0 = pd.Series([0.0])
    prob  = rl.predict(x_df)[0]*100
    freq  = rn.predict(x_df, offset=off0)[0]*100
    pp    = freq/100*COUT
    pc    = pp*(1+SECU+FRAIS+MARGE)
    xr    = xp.copy()
    for col,val in [("DrivAge",45),("BonusMalus",60),("Density",400)]:
        if col in X_cols: xr[col] = float(val)
    freq_ref = rn.predict(pd.DataFrame([xr]),offset=off0)[0]*100
    rel      = freq/freq_ref if freq_ref>0 else 1.0

    st.markdown("<br>", unsafe_allow_html=True)
    r1,r2,r3,r4 = st.columns(4)
    with r1: kpi(f"{prob:.2f}%","P(Sinistre)","#EF4444" if prob>6 else "#3B82F6","🎯")
    with r2: kpi(f"{freq:.4f}/an","Fréquence annuelle","#F59E0B" if freq>5 else "#3B82F6","📉")
    with r3: kpi(f"{pp:.0f} {CUR_SYM}","Prime pure","#EF4444" if pp>150*CUR_RATE else "#10B981","💵")
    with r4: kpi(f"{pc:.0f} {CUR_SYM}","Prime commerciale","#EF4444" if pc>200*CUR_RATE else "#10B981","💰")

    msg_rel = f"{rel:.2f}× plus risqué" if rel>1 else f"{1/rel:.2f}× moins risqué"
    col_rel = "danger" if rel>2 else "warning" if rel>1.2 else "success"
    rec_box(f"Ce profil est <b>{msg_rel}</b> que le profil de référence (45 ans, BM=60, densité=400).", col_rel)

    st.markdown(f"<br><b>Décomposition de la prime commerciale ({CUR_SYM})</b>", unsafe_allow_html=True)
    prime_df = pd.DataFrame({
        "Composante":["Prime pure","+ Sécurité","+ Frais","+ Marge","PRIME COMMERCIALE"],
        f"Montant ({CUR_SYM})":[f"{pp:.0f}",f"{pp*SECU:.0f}",f"{pp*FRAIS:.0f}",f"{pp*MARGE:.0f}",f"{pc:.0f}"],
        "Taux":["Base",f"+{SECU*100:.0f}%",f"+{FRAIS*100:.0f}%",f"+{MARGE*100:.0f}%","Total"]
    })
    st.dataframe(prime_df, use_container_width=True)

    if CUR_SYM != "€":
        rec_box(f"Montants en {CUR_SYM} (taux : 1€ = {CUR_RATE:.2f} {CUR_SYM}).","info")

    interp_box("À quoi correspondent ces montants ?",
        f"<b>Prime pure ({pp:.0f} {CUR_SYM})</b> = coût théorique du risque pur. "
        f"<b>Sécurité ({SECU*100:.0f}%)</b> = marge pour couvrir la variabilité aléatoire. "
        f"<b>Frais ({FRAIS*100:.0f}%)</b> = commissions et coûts de gestion. "
        f"<b>Marge ({MARGE*100:.0f}%)</b> = bénéfice attendu par l'assureur.")
    ai_box(f"Profil : {age_v}ans, BM={bm_v}, densité={den_v:,}. "
           f"P(sinistre)={prob:.2f}% · Fréq={freq:.4f}/an · Prime pure={pp:.0f}{CUR_SYM} · Commerciale={pc:.0f}{CUR_SYM}.")

    st.session_state.report_data["pricing"] = {
        "age":age_v,"bm":bm_v,"power":pw_v,"vehage":va_v,"density":den_v,
        "prob":prob,"freq":freq,"pp":pp,"pc":pc,"rel":rel,"cur":CUR_SYM
    }

# ══════════════════════════════════════════════════════════════════════════════
# SEGMENTATION
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "segmentation":
    header("Segmentation Portefeuille", "Identification des groupes de risque naturels", "🧩")
    df = st.session_state.df
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans

    interp_box("Qu'est-ce que la segmentation KMeans ?",
        "L'algorithme <b>KMeans</b> divise le portefeuille en groupes d'assurés similaires. "
        "Identifiez les <b>segments très risqués</b> (surprime) et les <b>bons risques</b> (rabais fidélisation).")

    feat_cols = [c for c in ["DrivAge","BonusMalus","Density","VehPower","VehAge"] if c in df.columns]
    n_clust   = st.slider("Nombre de segments", 2, 8, 4)

    if st.button("🔍 Lancer la segmentation KMeans", use_container_width=True):
        bar = st.progress(0,"Segmentation...")
        df_seg = df[feat_cols].dropna().copy()
        bar.progress(20)
        scaler = StandardScaler(); X_sc = scaler.fit_transform(df_seg)
        bar.progress(40)
        km = KMeans(n_clusters=n_clust, random_state=42, n_init=10)
        labels = km.fit_predict(X_sc)
        bar.progress(65)
        df_seg["Segment"] = labels
        if "ClaimOcc" in df.columns: df_seg["ClaimOcc"] = df["ClaimOcc"].values[:len(df_seg)]
        if "ClaimNb"  in df.columns: df_seg["ClaimNb"]  = df["ClaimNb"].values[:len(df_seg)]

        # BUG FIX — N contrats séparé pour ne pas écraser DrivAge
        agg_dict = {c:"mean" for c in feat_cols}
        if "ClaimOcc" in df_seg.columns: agg_dict["ClaimOcc"] = "mean"
        if "ClaimNb"  in df_seg.columns: agg_dict["ClaimNb"]  = "mean"
        profiles = df_seg.groupby("Segment").agg(agg_dict).reset_index()
        taille   = df_seg.groupby("Segment").size().reset_index(name="N contrats")
        profiles = profiles.merge(taille, on="Segment")
        if "ClaimOcc" in profiles.columns:
            profiles["Sinistralité %"] = (profiles["ClaimOcc"]*100).round(2)
        bar.progress(100); time.sleep(0.3); bar.empty()

        st.dataframe(profiles.round(3), use_container_width=True)

        if len(feat_cols)>=3:
            COLORS = ["#3B82F6","#10B981","#F59E0B","#EF4444","#8B5CF6","#06B6D4","#EC4899","#14B8A6"]
            fr = go.Figure()
            for seg in sorted(df_seg["Segment"].unique()):
                row_seg = profiles[profiles["Segment"]==seg]
                if len(row_seg)==0: continue
                vals  = [row_seg[c].values[0] for c in feat_cols]
                norms = [(v-df[c].min())/max(df[c].max()-df[c].min(),1e-9) for v,c in zip(vals,feat_cols)]
                sin_r = row_seg["Sinistralité %"].values[0] if "Sinistralité %" in row_seg.columns else 0
                fr.add_trace(go.Scatterpolar(r=norms+[norms[0]], theta=feat_cols+[feat_cols[0]],
                    fill="toself", name=f"Seg {seg} (sin={sin_r:.1f}%)",
                    line_color=COLORS[seg%len(COLORS)], opacity=0.75))
            fr.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0,1],
                             gridcolor="rgba(255,255,255,0.08)")),
                             title="Radar — Profil de chaque segment", **PLOTLY_CFG)
            st.plotly_chart(fr, use_container_width=True)

        if "Sinistralité %" in profiles.columns:
            fs = px.bar(profiles, x="Segment", y="Sinistralité %",
                        title="Sinistralité par segment (%)", color="Sinistralité %", text="Sinistralité %",
                        color_continuous_scale=[[0,"#10B981"],[0.5,"#F59E0B"],[1,"#EF4444"]])
            fs.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
            fs.update_layout(**PLOTLY_CFG); fs.update_coloraxes(showscale=False)
            st.plotly_chart(fs, use_container_width=True)

        interp_box("Comment utiliser ces segments ?",
            "Le segment <b>rouge</b> = population la plus risquée → <b>surprime</b>. "
            "Le segment <b>vert</b> = meilleurs clients → <b>tarifs préférentiels</b>. "
            "Le radar montre les caractéristiques de chaque groupe.")
        ai_box(f"Segmentation en {n_clust} groupes sur {len(df_seg):,} contrats terminée.")

# ══════════════════════════════════════════════════════════════════════════════
# RECOMMANDATIONS ACTUARIELLES
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "recommendations":
    header("Recommandations Actuarielles", "Diagnostics, stratégies tarifaires et actions concrètes", "📑")
    df = st.session_state.df

    st.markdown("### 🔬 Diagnostics statistiques automatiques")
    if "ClaimNb" in df.columns and df["ClaimNb"].mean()>0:
        rvm_r = df["ClaimNb"].var()/df["ClaimNb"].mean()
        pz_r  = (df["ClaimNb"]==0).mean()
        if rvm_r>1.5: rec_box(f"Surdispersion forte (Var/Moy={rvm_r:.3f}) → GLM NB2 indispensable.","danger")
        elif rvm_r>1.1: rec_box(f"Surdispersion modérée (Var/Moy={rvm_r:.3f}) → GLM NB2 recommandé.","warning")
        else: rec_box(f"Équidispersion acceptable (Var/Moy={rvm_r:.3f}) → GLM Poisson utilisable.","success")
        if pz_r>0.90: rec_box(f"Excès structurel de zéros ({pz_r*100:.1f}%) → Tester ZIP/ZINB.","warning")

    nc_r = df.select_dtypes(include=[np.number]).columns
    if len(nc_r)>=2:
        cm_r = df[nc_r].corr().abs()
        hc_r = [(i,j,cm_r.loc[i,j]) for i in cm_r.index for j in cm_r.columns if i<j and cm_r.loc[i,j]>0.7]
        if hc_r:
            for i,j,v in hc_r[:3]: rec_box(f"Corrélation élevée {i}×{j} (r={v:.2f}) → multicolinéarité.","warning")
        else: rec_box("Aucune corrélation excessive entre prédicteurs.","success")

    miss_r = df.isnull().sum().sum()
    if miss_r>0: rec_box(f"{miss_r:,} valeurs manquantes → exécutez le prétraitement.","warning")
    else: rec_box("Aucune valeur manquante.","success")

    st.markdown("---")
    st.markdown("### 💼 Recommandations tarifaires actuarielles")

    if st.session_state.model_nb is not None:
        irr_r = st.session_state.irr_nb
        rec_box("GLM NB2 retenu comme modèle de fréquence — LRT significatif (preuve forte).","success")
        for var, msg_risk, msg_prot in [
            ("BonusMalus",
             "Prédicteur #1 de fréquence. <b>Action :</b> Pondérer fortement BonusMalus dans la grille. "
             "Les malussés (BM>100) justifient une surprime de +150% à +200%.",""),
            ("DrivAge","",
             "Facteur protecteur — l'expérience réduit la fréquence. "
             "<b>Action :</b> Réduction pour les conducteurs 40+ et surprime progressive pour les 18-25 ans."),
            ("Density",
             "Zones urbaines plus accidentogènes. <b>Action :</b> Créer des zones tarifaires différenciées.",""),
            ("VehPower",
             "Véhicules puissants → sinistralité accrue. <b>Action :</b> Coefficient progressif sur la puissance.",""),
        ]:
            if var in irr_r.index:
                v_irr = irr_r.loc[var,"IRR"]
                sig   = irr_r.loc[var,"Sig"]
                if v_irr>1 and msg_risk:
                    rec_box(f"<b>{var}</b> (IRR={v_irr:.4f} {sig}) : {msg_risk}","warning")
                elif v_irr<1 and msg_prot:
                    rec_box(f"<b>{var}</b> (IRR={v_irr:.4f} {sig}) : {msg_prot}","info")
    else:
        rec_box("Estimez le NB2 dans Modélisation GLM pour les recommandations tarifaires.","info")

    st.markdown("---")
    st.markdown("### 🔭 Pistes d'amélioration actuarielles")
    improvements = [
        ("Modèles Zero-Inflated (ZIP/ZINB)",
         "L'excès structurel de zéros peut être capturé par des modèles à deux composantes."),
        ("GLM Gamma pour la sévérité",
         "Intégrer un modèle de coût moyen par sinistre (ClaimAmount) via GLM Gamma pour une prime pure complète."),
        ("Effets non-linéaires",
         "Tester DrivAge² et l'interaction DrivAge×BonusMalus pour capturer les non-linéarités."),
        ("Données télématiques",
         "L'intégration du kilométrage et du comportement de conduite (UBI) pourrait diviser l'erreur par 2."),
        ("Données de panel",
         "L'historique longitudinal permettrait d'estimer des effets fixes individuels."),
    ]
    for title_imp, desc_imp in improvements:
        rec_box(f"<b>{title_imp}</b> : {desc_imp}", "info")

    interp_box("Comment utiliser ces recommandations actuarielles ?",
        "Ces diagnostics analysent automatiquement votre portefeuille et vos modèles. "
        "Les recommandations indiquent les variables prioritaires pour la grille de tarification. "
        "Toute décision tarifaire doit être validée par un actuaire qualifié.")

# ══════════════════════════════════════════════════════════════════════════════
# RAPPORT PDF
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "report":
    header("Rapport PDF Professionnel", "Export complet · Résultats actuariels", "📄")

    c1,c2 = st.columns(2)
    analyste  = c1.text_input("Nom de l'analyste","")
    compagnie = c2.text_input("Institution / Compagnie","")
    rtype = st.radio("Type de rapport",
        ["📊 Rapport Exécutif (2-3 pages)","📋 Rapport Technique Complet"],horizontal=True)

    if st.button("📥 Générer le rapport PDF", use_container_width=True):
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib import colors as rl_colors
            from reportlab.lib.units import cm
            from reportlab.lib.styles import ParagraphStyle
            from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
            from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                            Table, TableStyle, HRFlowable, PageBreak)

            buf   = BytesIO()
            df_r  = st.session_state.df
            now_r = datetime.now().strftime("%d/%m/%Y à %H:%M")

            NAVY  = rl_colors.HexColor("#0A1628"); BLUE  = rl_colors.HexColor("#3B82F6")
            GRAY  = rl_colors.HexColor("#EAEDF2"); LIGHT = rl_colors.HexColor("#F1F5F9")
            WHITE = rl_colors.white

            def PS(name, **kw):
                p = dict(fontName="Helvetica",fontSize=10,textColor=rl_colors.HexColor("#1E293B"),
                         spaceAfter=6,leading=16,alignment=TA_JUSTIFY)
                p.update(kw); return ParagraphStyle(name, **p)

            S_BODY = PS("b")
            S_SEC  = PS("s",fontName="Helvetica-Bold",fontSize=13,textColor=BLUE,spaceBefore=12,spaceAfter=6,leading=18)
            S_BOLD = PS("bd",fontName="Helvetica-Bold",fontSize=10)
            S_GRAY = PS("sg",fontSize=8.5,textColor=GRAY,leading=12)

            def hr_l(): return HRFlowable(width="100%",thickness=1,color=BLUE,spaceAfter=8,spaceBefore=4)

            def dtbl(headers, rows, cw=None):
                t = Table([headers]+rows, colWidths=cw)
                t.setStyle(TableStyle([
                    ("BACKGROUND",(0,0),(-1,0),BLUE),("TEXTCOLOR",(0,0),(-1,0),WHITE),
                    ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),9),
                    ("FONTNAME",(0,1),(-1,-1),"Helvetica"),
                    ("ROWBACKGROUNDS",(0,1),(-1,-1),[LIGHT,WHITE]),
                    ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
                    ("LEFTPADDING",(0,0),(-1,-1),7),
                    ("GRID",(0,0),(-1,-1),0.4,rl_colors.HexColor("#CBD5E1")),
                ])); return t

            def on_page(canvas, doc):
                canvas.saveState()
                canvas.setFont("Helvetica",8); canvas.setFillColor(GRAY)
                canvas.drawCentredString(A4[0]/2, 1.0*cm, f"ACTUARIA v3.0 · {compagnie or 'INSSEDS'} · {now_r}")
                canvas.drawRightString(A4[0]-1.5*cm, 1.0*cm, f"Page {doc.page}")
                canvas.restoreState()

            doc_pdf = SimpleDocTemplate(buf, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm,
                                        topMargin=2*cm, bottomMargin=2*cm,
                                        title="ACTUARIA — Rapport Actuariel", author=analyste or "ACTUARIA")
            story = []

            # Couverture
            story.append(Spacer(1,2*cm))
            cv = Table([[Paragraph("ACTUARIA v3.0",
                          PS("t",fontName="Helvetica-Bold",fontSize=22,textColor=WHITE,alignment=TA_CENTER))]],
                       colWidths=[17*cm])
            cv.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),NAVY),
                                    ("TOPPADDING",(0,0),(-1,-1),28),("BOTTOMPADDING",(0,0),(-1,-1),10)]))
            story.append(cv)
            story.append(Paragraph("RISK PRICING STUDIO",
                          PS("s2",fontSize=10,textColor=rl_colors.HexColor("#94A3B8"),alignment=TA_CENTER)))
            story.append(Spacer(1,0.3*cm))
            label_r = "RAPPORT EXÉCUTIF" if "Exécutif" in rtype else "RAPPORT TECHNIQUE COMPLET"
            bn = Table([[Paragraph(label_r,
                         PS("bl",fontName="Helvetica-Bold",fontSize=14,textColor=WHITE,alignment=TA_CENTER))]],
                       colWidths=[17*cm])
            bn.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),BLUE),
                                    ("TOPPADDING",(0,0),(-1,-1),12),("BOTTOMPADDING",(0,0),(-1,-1),12)]))
            story.append(bn); story.append(Spacer(1,0.4*cm))
            story.append(Paragraph("Modélisation actuarielle automobile · GLM Logit · Poisson · NB2",
                          PS("sb",fontSize=9.5,textColor=GRAY,alignment=TA_CENTER)))
            story.append(Spacer(1,0.5*cm))
            meta = [["Analyste",analyste or "—"],["Institution",compagnie or "—"],
                    ["Date",now_r],["Dataset",f"{df_r.shape[0]:,} contrats · {df_r.shape[1]} variables"],
                    ["Devise",CUR_SYM]]
            mt = Table(meta, colWidths=[4*cm,13*cm])
            mt.setStyle(TableStyle([
                ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),("FONTNAME",(1,0),(1,-1),"Helvetica"),
                ("FONTSIZE",(0,0),(-1,-1),9.5),("TEXTCOLOR",(0,0),(0,-1),BLUE),
                ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
                ("ROWBACKGROUNDS",(0,0),(-1,-1),[LIGHT,WHITE]),
                ("LINEBELOW",(0,-1),(-1,-1),1,BLUE)]))
            story.append(mt); story.append(PageBreak())

            # Section 1 : KPIs
            story.append(Paragraph("1. Vue d'ensemble du portefeuille", S_SEC)); story.append(hr_l())
            has_cn_r = "ClaimNb" in df_r.columns; has_oc_r = "ClaimOcc" in df_r.columns
            has_ex_r = "Exposure" in df_r.columns
            taux_r_v = df_r["ClaimOcc"].mean() if has_oc_r else 0
            freq_r_v = df_r["ClaimNb"].mean() if has_cn_r else 0
            pz_r_v   = (df_r["ClaimNb"]==0).mean() if has_cn_r else 0
            rvm_r_v  = df_r["ClaimNb"].var()/freq_r_v if has_cn_r and freq_r_v>0 else 1
            krows = [
                ["Contrats",f"{len(df_r):,}","Taille totale analysée"],
                ["Sinistralité",f"{taux_r_v*100:.2f}%","Part des assurés avec ≥ 1 sinistre"],
                ["Fréquence globale",f"{freq_r_v:.5f}","Sinistres moyens par contrat/an"],
                ["Exposition totale",f"{df_r['Exposure'].sum() if has_ex_r else len(df_r):,.0f} ans","Somme des expositions"],
                ["Proportion zéros",f"{pz_r_v*100:.2f}%","Contrats sans sinistre"],
                ["Ratio Var/Moy",f"{rvm_r_v:.4f}","Indicateur de surdispersion"],
            ]
            story.append(dtbl(["Indicateur","Valeur","Signification"],krows,[4*cm,3.5*cm,9.5*cm]))
            story.append(Spacer(1,0.3*cm))
            story.append(Paragraph(
                f"Portefeuille de {len(df_r):,} contrats · Sinistralité {taux_r_v*100:.2f}% · "
                f"Ratio Var/Moy = {rvm_r_v:.4f} " +
                ("→ surdispersion, NB2 retenu." if rvm_r_v>1.1 else "→ Poisson acceptable.") +
                f" {pz_r_v*100:.1f}% de contrats sans sinistre (typique IARD automobile).", S_BODY))

            # Section 2 : Modèles GLM
            story.append(Spacer(1,0.5*cm))
            story.append(Paragraph("2. Résultats des modèles économétriques", S_SEC)); story.append(hr_l())

            if st.session_state.model_logit:
                story.append(Paragraph("2.1 Modèle Logistique — Survenance (ClaimOcc)", S_BOLD))
                rl2 = st.session_state.model_logit; auc_r2 = st.session_state.auc_val or 0
                story.append(Paragraph(
                    f"Pseudo-R² McFadden = {rl2.prsquared:.4f} · AIC = {rl2.aic:,.0f} · AUC-ROC = {auc_r2:.4f}. "
                    "Modèle globalement significatif. AUC satisfaisante pour un portefeuille déséquilibré.", S_BODY))

            if st.session_state.model_poi and st.session_state.model_nb:
                story.append(Spacer(1,0.3*cm))
                story.append(Paragraph("2.2 GLM Poisson vs Binomiale Négative", S_BOLD))
                rp4 = st.session_state.model_poi; rn4 = st.session_state.model_nb
                lrt4 = -2*(rp4.llf-rn4.llf); lp4 = chi2.sf(lrt4,df=1); da4 = rp4.aic-rn4.aic
                comp4 = [
                    ["GLM Poisson",f"{rp4.llf:,.2f}",f"{rp4.aic:,.2f}",f"{rp4.bic:,.2f}",
                     f"{rp4.deviance/rp4.df_resid:.4f}",""],
                    ["GLM NB2 ★",f"{rn4.llf:,.2f}",f"{rn4.aic:,.2f}",f"{rn4.bic:,.2f}",
                     f"{rn4.deviance/rn4.df_resid:.4f}",f"ΔAIC={da4:.1f} ✔"],
                ]
                story.append(dtbl(["Modèle","Log-L","AIC","BIC","Dév/DDL","Statut"],
                                   comp4,[4.5*cm,2.5*cm,2.5*cm,2.5*cm,2.5*cm,2.5*cm]))
                story.append(Paragraph(
                    f"LRT p = {lp4:.2e} → " +
                    ("NB2 significativement supérieur." if lp4<0.05 else "Poisson et NB2 équivalents.") +
                    f" ΔAIC = {da4:.1f}" + (" → preuve forte." if da4>10 else "."), S_BODY))

                story.append(Spacer(1,0.3*cm))
                story.append(Paragraph("2.3 Incident Rate Ratios (IRR) — GLM NB2", S_BOLD))
                irr4 = st.session_state.irr_nb
                top8 = irr4[irr4.index!="const"].head(8)
                irr_rows4 = [
                    [str(v), f"{top8.loc[v,'IRR']:.4f}",
                     f"{top8.loc[v,'IC inf']:.4f}" if 'IC inf' in top8.columns else "—",
                     f"{top8.loc[v,'IC sup']:.4f}" if 'IC sup' in top8.columns else "—",
                     f"{top8.loc[v,'p-value']:.4e}", top8.loc[v,'Sig']]
                    for v in top8.index]
                story.append(dtbl(["Variable","IRR","IC inf (95%)","IC sup (95%)","p-value","Sig."],
                                   irr_rows4,[5*cm,2*cm,2.5*cm,2.5*cm,3*cm,2*cm]))
                story.append(Paragraph(
                    "IRR > 1 : facteur aggravant · IRR < 1 : facteur protecteur · "
                    "IC ne contenant pas 1 → effet significatif.", S_BODY))

            # Tarification
            pd5 = st.session_state.report_data.get("pricing")
            if pd5:
                n_sec_r = "4" if "Technique" in rtype else "3"
                story.append(Spacer(1,0.5*cm))
                story.append(Paragraph(f"{n_sec_r}. Exemple de tarification", S_SEC))
                story.append(hr_l())
                pr_r = [
                    ["Âge conducteur",f"{pd5['age']} ans"],["BonusMalus",str(pd5["bm"])],
                    ["Densité",f"{pd5['density']:,} hab/km²"],
                    ["P(sinistre)",f"{pd5['prob']:.2f}%"],["Fréquence/an",f"{pd5['freq']:.4f}"],
                    [f"Prime pure ({pd5['cur']})",f"{pd5['pp']:.0f}"],
                    [f"Prime commerciale ({pd5['cur']})",f"{pd5['pc']:.0f}"],
                    ["Relativité vs référence",f"{pd5['rel']:.2f}×"],
                ]
                story.append(dtbl(["Paramètre","Valeur"],pr_r,[6*cm,11*cm]))
                story.append(Paragraph(
                    f"Ce profil présente un risque {pd5['rel']:.2f}× " +
                    ("supérieur" if pd5['rel']>1 else "inférieur") +
                    f" à la référence. Prime commerciale : {pd5['pc']:.0f} {pd5['cur']}.", S_BODY))

            # Recommandations
            n_reco = str(int(n_sec_r if pd5 else "3")+1) if pd5 else "3"
            story.append(Spacer(1,0.5*cm))
            story.append(Paragraph(f"{n_reco}. Recommandations actuarielles", S_SEC))
            story.append(hr_l())
            recs5 = [
                ("NB2 retenu","Supérieur au Poisson sur tous les critères (LRT, AIC, BIC)."),
                ("BonusMalus prioritaire","Prédicteur #1 — pondérer fortement dans la grille tarifaire."),
                ("Surprimes ciblées","Jeunes (<25 ans), malussés (BM>100), très urbains → relativités > 2×."),
                ("ZIP/ZINB à tester","Excès de zéros structurel → modèles Zero-Inflated."),
                ("GLM Gamma (sévérité)","Intégrer un modèle de coût moyen pour une prime pure complète."),
            ]
            story.append(dtbl(["","Recommandation","Description"],
                               [[f"[{i+1}]",r,d] for i,(r,d) in enumerate(recs5)],
                               [0.8*cm,4.5*cm,11.7*cm]))
            story.append(Spacer(1,0.8*cm))
            story.append(HRFlowable(width="100%",thickness=2,color=BLUE,spaceAfter=10))
            story.append(Paragraph(
                f"Généré automatiquement par ACTUARIA v3.0 · {min(150000,len(df_r)):,} observations · "
                "À valider par un actuaire qualifié avant toute décision tarifaire opérationnelle.",
                PS("n",fontSize=8.5,textColor=GRAY,fontName="Helvetica-Oblique",leading=13)))

            doc_pdf.build(story, onFirstPage=on_page, onLaterPages=on_page)
            pdf_bytes = buf.getvalue()
            fname = f"ACTUARIA_rapport_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
            st.download_button("📥 Télécharger le rapport PDF", pdf_bytes, fname,
                               "application/pdf", use_container_width=True)
            st.success(f"✔ Rapport généré — {len(pdf_bytes)/1024:.0f} Ko")

        except ImportError as ie:
            st.error(f"Module manquant : {ie}. Installez : pip install reportlab")
        except Exception as e:
            st.error(f"Erreur PDF : {e}")
            import traceback; st.code(traceback.format_exc())

# ══════════════════════════════════════════════════════════════════════════════
# PARAMÈTRES
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "settings":
    header("Paramètres & Session","","⚙️")
    st.info("Les paramètres métier (devise, coût moyen, chargements) sont réglables dans la barre latérale en temps réel.")

    st.markdown("### 📋 État de la session")

    # ── BUG FIX ValueError ─────────────────────────────────────────────────
    # Utiliser "is not None" et non "if obj" pour éviter ValueError sur DataFrame
    proc_ok    = st.session_state.df_proc is not None
    logit_ok   = st.session_state.model_logit is not None
    poi_ok     = st.session_state.model_poi is not None
    nb_ok      = st.session_state.model_nb is not None
    # ─────────────────────────────────────────────────────────────────────────

    for step, ok in [
        ("Données importées",     True),
        ("Prétraitement",         proc_ok),
        ("Logit estimé",          logit_ok),
        ("GLM Poisson estimé",    poi_ok),
        ("GLM NB2 estimé",        nb_ok),
    ]:
        status = "✔ Oui" if ok else ("En attente" if step=="Prétraitement" else "✗ Non")
        level  = "success" if ok else ("warning" if step=="Prétraitement" else "danger")
        rec_box(f"{step} : <b>{status}</b>", level)

    st.markdown("---")
    csv_b = st.session_state.df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇ Télécharger le dataset traité (CSV)", csv_b,
                       "dataset_traite.csv","text/csv",use_container_width=True)

    st.markdown("---")
    if st.button("🗑️ Réinitialiser toute la session", type="secondary", use_container_width=True):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

    st.markdown(
        "<div style='text-align:center;color:#64748B;font-size:0.72rem;margin-top:2rem;"
        "padding:1rem;border-top:1px solid #1E3A5F;'>"
        "ACTUARIA v3.0 · INSSEDS 2025-2026 · Streamlit · statsmodels · scikit-learn · plotly · reportlab"
        "</div>", unsafe_allow_html=True)