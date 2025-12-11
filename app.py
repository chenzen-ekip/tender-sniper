import streamlit as st
import time

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Tender Sniper",
    page_icon="🎯",
    layout="wide", # Utilise tout l'écran
    initial_sidebar_state="collapsed"
)

# --- CSS POUR FAIRE APP MOBILE (ET CACHER LA BANDE NOIRE) ---
st.markdown("""
    <style>
    /* Cacher le menu hamburger, le footer et le header (la bande noire) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Supprimer les marges en haut pour coller au bord du téléphone */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    /* Style des boutons "App Mobile" */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        background-color: #0068C9;
        color: white;
        font-weight: bold;
        border: none;
    }
    
    /* Style des alertes */
    .urgent-box {
        background-color: #FFF2F2;
        border: 1px solid #FF4B4B;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- GESTION DES ÉTAPES (LOGIN -> ONBOARDING -> DASHBOARD) ---
if 'step' not in st.session_state:
    st.session_state.step = 'login'

# ==========================================
# ÉTAPE 1 : ÉCRAN DE CONNEXION
# ==========================================
if st.session_state.step == 'login':
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.title("🎯 Tender Sniper")
    st.caption("Intelligence d'Appels d'Offres")
    
    with st.form("login_form"):
        st.write("### Connexion")
        password = st.text_input("Code d'accès", type="password")
        submitted = st.form_submit_button("SE CONNECTER")
        
        if submitted:
            if password == "YESCLEAN" or password == "DEMO": # Mot de passe simple
                st.session_state.step = 'onboarding'
                st.rerun()
            else:
                st.error("Code incorrect.")

# ==========================================
# ÉTAPE 2 : ONBOARDING (CONFIGURATION)
# ==========================================
elif st.session_state.step == 'onboarding':
    st.title("⚙️ Configuration")
    st.write("Bienvenue M. Essid. Configurez votre robot pour lancer la recherche.")
    
    with st.form("onboarding_form"):
        st.subheader("1. Vos Cibles")
        keywords = st.multiselect(
            "Quels types de marchés ?",
            ["Nettoyage", "Vitrerie", "Remise en état", "Espaces Verts"],
            default=["Nettoyage", "Vitrerie"]
        )
        
        st.subheader("2. Votre Zone")
        col1, col2 = st.columns(2)
        with col1:
            depts = st.multiselect(
                "Départements",
                ["75", "92", "93", "94", "77"],
                default=["75", "93"]
            )
        with col2:
            budget = st.slider("Budget Min.", 10000, 500000, 50000)
            
        st.markdown("---")
        submitted = st.form_submit_button("🚀 LANCER L'ANALYSE")
        
        if submitted:
            with st.spinner("Le robot scanne les bases de données..."):
                time.sleep(2) # Faux temps de chargement pour l'effet "Waouh"
            st.session_state.step = 'dashboard'
            st.rerun()

# ==========================================
# ÉTAPE 3 : LE DASHBOARD (RÉSULTATS)
# ==========================================
elif st.session_state.step == 'dashboard':
    # En-tête Client
    st.write("👋 **Bonjour YesClean**")
    
    # KPIs
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Opportunités", "3", "+2 ce matin")
    with col2:
        st.metric("Potentiel", "6.8 M€", "High Ticket")
        
    st.markdown("---")
    st.subheader("🔥 Alertes Urgentes")

    # CARTE 1 : POMPIDOU (URGENT)
    with st.container():
        st.markdown("""
        <div class="urgent-box">
            <h3 style="margin:0; color:#333;">🏛️ Centre Pompidou (Nettoyage)</h3>
            <p style="color: grey; margin-bottom:5px;">📍 Paris (75) | 💰 <b>6,6 M€</b></p>
            <p style="color: #FF4B4B; font-weight:bold;">⚠️ VISITE OBLIGATOIRE : J-1</p>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.button("📄 Synthèse IA", key="btn_syn_1")
        with c2:
            st.button("📥 Dossier (DCE)", key="btn_dce_1")

    # CARTE 2 : AUDENCIA
    with st.expander("🎓 Campus Audencia (St Ouen)", expanded=True):
        st.write("**Budget :** 250 000 € / an")
        st.write("**Date limite :** 15 Janvier")
        st.info("💡 **Avis IA :** Marché parfait pour compléter vos tournées dans le 93.")
        st.button("Voir le dossier", key="btn_2")

    # Bouton de retour aux réglages (discret en bas)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Modifier mes filtres"):
        st.session_state.step = 'onboarding'
        st.rerun()
