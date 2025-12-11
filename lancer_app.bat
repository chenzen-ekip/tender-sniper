@echo off
:: Se placer dans le répertoire du script
cd /d "%~dp0"

:: Activer l'environnement virtuel et installer streamlit si nécessaire (rapide check)
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else (
    echo Attention: Dossier .venv non trouvé. On essaie avec le python global...
)

:: Vérifier si streamlit est installé via une commande pip simple (optionnel mais utile)
pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo Installation de Streamlit...
    pip install streamlit
)

:: Lancer l'application
echo Lancement de Tender Sniper...
streamlit run app.py

:: Laisser la fenêtre ouverte en cas d'erreur
pause
