
import os
import pandas as pd
from openai import OpenAI

# Configuration
# Note: Security best practice would be environment variable, but user explicitly asked to put it in script for this exercise.
API_KEY = "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"

client = OpenAI(api_key=API_KEY)

INPUT_FILE = 'leads_complets.csv'
OUTPUT_FILE = 'leads_ready.csv'
MODEL = "gpt-4o-mini"

def generate_email(title, description):
    prompt = f"""Tu es un apporteur d'affaires B2B. Analyse cet appel d'offres de nettoyage. Rédige un email de prospection ULTRA COURT (4 lignes max) à destination du patron d'une entreprise de nettoyage locale. L'email doit dire : 'J'ai détecté ce marché [Titre], voici pourquoi vous pouvez le gagner [Argument clé extrait du texte]. Je vous ai préparé le dossier technique, je vous l'envoie ?'. Ton ton doit être direct et professionnel.

    Titre du marché : {title}
    Description du marché : {description[:2000]} (tronqué si trop long)"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "Tu es un expert en vente B2B direct et efficace."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Erreur IA: {str(e)}"

def main():
    print("Démarrage du Cerveau 🧠...")
    
    try:
        df = pd.read_csv(INPUT_FILE)
        print(f"Fichier chargé. {len(df)} leads trouvés.")
    except FileNotFoundError:
        print(f"Erreur: Impossible de trouver {INPUT_FILE}")
        return

    # Mode test : 3 premières lignes seulement
    # df_subset = df.head(3).copy() # User asked for Loop on first 3 generally, but saving all usually makes sense. 
    # The requirement was "Pour les 3 premières lignes SEULEMENT (mode test pour économiser des crédits)"
    # So I will effectively only process 3 and leave the rest blank or just create a small file.
    # To produce a valid CSV with columns aligned, I'll copy the whole DF but only fill the first 3.
    
    df['Email_Genere'] = ""
    
    limit = 3
    print(f"Traitement des {limit} premiers leads pour test...")

    for index, row in df.iterrows():
        if index >= limit:
            break
        
        print(f"[{index+1}/{limit}] Analyse de : {row['Titre'][:30]}...")
        
        email = generate_email(row['Titre'], row['Description_Texte'])
        df.at[index, 'Email_Genere'] = email
        print("  -> Email généré.")

    # Save to new file
    # We might want to save only the processed ones or all. 
    # Usually "leads_ready.csv" implies the output. The user said "leads_ready.csv avec les colonnes originales + une nouvelle colonne".
    # I will save the whole dataframe, with the rest having empty strings, or just the top 3.
    # Let's save the whole thing, so the user sees the structure, but populated only for top 3.
    
    df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
    print(f"\nTerminé ! Résultats sauvegardés dans '{OUTPUT_FILE}'.")
    print("Vérifiez la colonne 'Email_Genere' pour les 3 premières lignes.")

if __name__ == "__main__":
    main()
