import streamlit as st
import time

# --- Configuration de la page ---
st.set_page_config(
    page_title="Tender Sniper",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS Personnalisé (Mobile Native) ---
st.markdown("""
<style>
    /* Masquer le menu hamburger (3 points) et le footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* On garde le Header visible pour le bouton Sidebar (Top Left), 
       mais on le rend transparent ou discret si besoin. 
       Si on le cache, on ne peut plus ouvrir le menu sur mobile. */
    /* header {visibility: hidden;}  <-- SUPPRIMÉ pour accès Sidebar */

    /* Meta-viewport simulation pour mobile */
    @viewport {
        width: device-width;
        zoom: 1.0;
    }

    /* Style global "Mobile Native" */
    .stApp {
        background-color: #f2f2f7; /* Gris clair iOS */
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* Réduire le padding pour utiliser tout l'écran */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }
    
    /* Force text color to black for all text elements */
    .stApp, .stMarkdown, p, h1, h2, h3, h4, span, div, label {
        color: #1c1c1e !important; /* Noir doux iOS */
    }

    /* Cards - Style iOS */
    .tender-card {
        background-color: white;
        padding: 16px;
        border-radius: 16px; 
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 16px;
        border-left: none;
    }

    /* Boutons style iOS "Primary" */
    .stButton > button {
        width: 100%;
        background-color: #007AFF !important;
        color: white !important;
        border: none;
        border-radius: 12px;
        font-weight: 600;
        font-size: 17px;
        padding: 14px 20px;
        margin-top: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.1s ease;
    }
    .stButton > button:hover {
        background-color: #006ede !important;
        transform: scale(0.98);
    }
    .stButton > button:active {
        transform: scale(0.96);
    }

    /* Alerte Rouge Clignotante style iOS */
    @keyframes blink {
        0% { opacity: 1; }
        50% { opacity: 0.6; }
        100% { opacity: 1; }
    }
    .alert-urgent {
        color: #ff3b30; /* Rouge iOS */
        font-weight: 700;
        animation: blink 2s infinite;
        background-color: rgba(255, 59, 48, 0.1);
        padding: 12px;
        border-radius: 10px;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 15px;
        border: 1px solid rgba(255, 59, 48, 0.2);
    }

    /* Budget */
    .budget-tag {
        color: #34c759; /* Vert iOS */
        font-weight: 700;
        font-size: 1.1em;
    }
    
    /* Titres Card */
    .tender-card h3 {
        font-size: 1.2rem;
        margin-bottom: 8px;
        font-weight: 700;
    }
    
    /* Sidebar styling adjustment */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# --- État de session pour le Login ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- Écran de Login ---
if not st.session_state['logged_in']:
    st.markdown("<h1 style='text-align: center;'>🎯 Tender Sniper</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #8e8e93 !important;'>Intelligence d'Appels d'Offres</h4>", unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    
    password = st.text_input("Mot de passe", type="password", placeholder="Entrez le code d'accès")
    
    if st.button("SE CONNECTER"):
        if password == "DEMO":
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Mot de passe incorrect")

# --- Application Principale avec Navigation ---
else:
    # --- Sidebar Navigation ---
    st.sidebar.title("⚙️ Menu")
    
    navigation = st.sidebar.radio(
        "Navigation",
        ["📊 Mes Opportunités", "🎯 Configurer ma Veille"],
        label_visibility="collapsed"
    )

    # --- PAGE 1 : Configurer ma Veille ---
    if navigation == "🎯 Configurer ma Veille":
        st.markdown("## 🎯 Configurer ma Veille")
        st.markdown("Définissez vos critères pour que l'IA chasse les meilleurs marchés pour vous.")
        
        with st.form("config_form"):
            st.markdown("### 🔍 Critères de Recherche")
            
            # Champ 1 : Mots-clés
            keywords = st.multiselect(
                "Mots-clés ciblés",
                options=["Nettoyage", "Vitrerie", "Gros Oeuvre", "Gardiennage", "Électricité"],
                default=["Nettoyage", "Vitrerie"]
            )
            
            # Champ 2 : Zones
            zones = st.multiselect(
                "Zone Géographique",
                options=["75 - Paris", "92 - Hauts-de-Seine", "93 - Seine-Saint-Denis", "94 - Val-de-Marne"],
                default=["75 - Paris"]
            )
            
            # Champ 3 : Budget
            budget = st.slider(
                "Budget Minimum du marché (€)",
                min_value=10000,
                max_value=1000000,
                value=50000,
                step=10000
            )
            
            st.write("")
            submitted = st.form_submit_button("💾 Sauvegarder mes critères")
            
            if submitted:
                st.balloons()
                st.success("✅ Le robot a bien reçu vos ordres. La recherche commence...")
                time.sleep(2)

    # --- PAGE 2 : Mes Opportunités (Dashboard Existant) ---
    elif navigation == "📊 Mes Opportunités":
        # Header Salutation
        st.markdown("### Bonjour M. Essid 👋")
        st.caption("Espace Client : **YesClean**")
        
        # KPIs
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Opportunités", "3", "+1 aujourd'hui")
        with col2:
            st.metric("Potentiel", "6.8 M€")
        st.markdown("---")

        # --- CARTE 1 : Centre Pompidou ---
        st.markdown("""
        <div class="tender-card">
            <h3>🏛️ Centre Pompidou (Nettoyage)</h3>
            <p>📍 <b>Lieu :</b> Paris (75)</p>
            <p>💶 <b>Budget Estimé :</b> <span class="budget-tag">6,6 M€</span></p>
            <div class="alert-urgent">⚠️ Visite Obligatoire : J-1</div>
        </div>
        """, unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🧠 Synthèse IA", key="btn1"):
                st.info("Résumé : Marché global de performance pour le nettoyage des espaces d'exposition et des bureaux. Critère RSE prépondérant (30%). Attention : visite sur site demain à 10h impérative pour valider la candidature.")
        with col_b:
            if st.button("📂 Télécharger DCE", key="btn2"):
                with st.spinner('Récupération sécurisée du DCE...'):
                    time.sleep(1.5)
                st.success("DCE téléchargé dans 'Mes Documents' !")

        st.write("") # Spacer

        # --- CARTE 2 : Campus Audencia ---
        st.markdown("""
        <div class="tender-card" style="border-left-color: #6c757d;">
            <h3>🎓 Campus Audencia (Entretien)</h3>
            <p>📍 <b>Lieu :</b> Saint-Ouen (93)</p>
            <p>💶 <b>Budget Estimé :</b> <span class="budget-tag">250 K€</span></p>
            <p style="color: orange; font-weight: bold;">⏳ Date limite : 15 jours</p>
        </div>
        """, unsafe_allow_html=True)

        col_c, col_d = st.columns(2)
        with col_c:
            st.button("🧠 Synthèse IA", key="btn3")
        with col_d:
            st.button("📂 Télécharger DCE", key="btn4")
