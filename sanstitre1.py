import streamlit as st
from datetime import datetime

# ================= CONFIGURATION =================
st.set_page_config(
    page_title="Miqat Station - Parakou",
    page_icon="🕌",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ================= COULEUR DE FOND SOMBRE =================
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #1a1a2e;
    color: #e0e0e0;
}
[data-testid="stMetricValue"] {
    font-size: 50px;
    color: #f5c542;
}
.time-box {
    background-color: #16213e;
    border-radius: 10px;
    padding: 20px;
    margin: 10px 0;
    text-align: center;
}
.prayer-name {
    font-size: 24px;
    font-weight: bold;
    color: #f5c542;
}
.prayer-time {
    font-size: 32px;
    color: white;
}
.prayer-time-past {
    font-size: 32px;
    color: #666;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ================= HEURES DE PRIÈRE (PARAKOU) =================
# Tu peux modifier directement ici quand les horaires changent.
prayer_times = {
    "Fajr": "05:50",
    "Dhuhr": "12:47",
    "Asr": "16:10",
    "Maghrib": "19:04",
    "Isha": "20:16"
}

# ================= LOGIQUE PRINCIPALE =================
now = datetime.now()

prayer_status = {}
next_prayer = None
next_time = None

for prayer, time_str in prayer_times.items():
    prayer_time = datetime.strptime(time_str, "%H:%M").replace(year=now.year, month=now.month, day=now.day)
    prayer_status[prayer] = {
        "time": prayer_time,
        "is_past": prayer_time <= now
    }
    if prayer_time > now and next_prayer is None:
        next_prayer = prayer
        next_time = prayer_time

# ================= AFFICHAGE =================
st.title("🕌 Miqat Station — Parakou")
st.caption(f"**{now.strftime('%d/%m/%Y')}** — Ta base secrète pour la prière")

# --- COMPTE À REBOURS VERS LA PROCHAINE PRIÈRE ---
if next_prayer:
    time_left = next_time - now
    hours = time_left.seconds // 3600
    minutes = (time_left.seconds // 60) % 60
    
    st.markdown("---")
    st.markdown(f"## ⏳ Prochaine prière : **{next_prayer}**")
    st.metric(label=f"à {next_time.strftime('%H:%M')}", value=f"{hours}h {minutes}m")
    st.markdown("---")

st.markdown("### 📋 Toutes les prières du jour")

# --- TABLEAU COMPLET ---
for prayer, info in prayer_status.items():
    time_str = info["time"].strftime("%H:%M")
    if info["is_past"]:
        st.markdown(f"""
        <div class="time-box" style="opacity: 0.5;">
            <span class="prayer-name">✅ {prayer}</span>
            <span class="prayer-time-past">{time_str}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="time-box" style="border: 2px solid #f5c542;">
            <span class="prayer-name">⏳ {prayer}</span>
            <span class="prayer-time">{time_str}</span>
        </div>
        """, unsafe_allow_html=True)

# ================= CITATION DU JOUR =================
st.markdown("---")
st.markdown("💬 *\"Personne ne viendra te sauver. Tu es ton seul héros.\"*")

# ================= BARRE LATÉRALE =================
with st.sidebar:
    st.header("⚙️ Commandes")
    st.write("**Emplacement :** Parakou, Bénin 🇧🇯")
    st.write("**Fuseau :** UTC+1")
    st.write("**Date :**", now.strftime("%d/%m/%Y"))
    if st.button("🔄 Rafraîchir les horaires"):
        st.rerun()
    st.markdown("---")
    st.caption("Créé par un hacker musulman ☠️")