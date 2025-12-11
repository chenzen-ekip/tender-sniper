
import pandas as pd
import re

INPUT_FILE = 'leads_ready.csv'
OUTPUT_FILE = 'leads_filtered.csv'

# Critères de filtrage
KEYWORDS_KEEP = ["Nettoyage", "Entretien", "Vitrerie", "Ménage", "Hygiène", "Déchets"]
KEYWORDS_EXCLUDE = ["Enquête", "Données", "Curage", "Espaces Verts", "Jardin", "Elagage", "Étude", "Sondage"]
LOCATIONS_EXCLUDE = ["Guyane", "Réunion", "Guadeloupe", "Martinique", "Mayotte", "971", "972", "973", "974", "976"]

def is_relevant(row):
    title = str(row['Titre'])
    desc = str(row['Description_Texte'])
    combined_text = (title + " " + desc).lower()
    
    # 1. Check Geography (Exclude DOM-TOM)
    for loc in LOCATIONS_EXCLUDE:
        if loc.lower() in combined_text:
            return False, f"Exclu (Lieu : {loc})"

    # 2. Check Exclusions (Wrong Activity)
    for kw in KEYWORDS_EXCLUDE:
        if kw.lower() in combined_text:
            return False, f"Exclu (Moché : {kw})"

    # 3. Check Inclusions (Right Activity)
    # At least one positive keyword must be in the Title (stronger signal) or Description
    # User said "Si le titre contient...", let's be strict on Title for relevance?
    # Or strict on the combined text. User said "Regarde la ligne 2... Ce n'est PAS du nettoyage".
    # Let's check Title primarily for the "Cleaning" aspect as Description might mention "nettoyage" in a different context.
    
    match_found = False
    for kw in KEYWORDS_KEEP:
        if kw.lower() in title.lower():
            match_found = True
            break
    
    if not match_found:
        # Fallback check in description but stronger
        for kw in KEYWORDS_KEEP:
            if kw.lower() in desc.lower():
                 # Maybe okay, but verify it's not buried
                 match_found = True
                 break
    
    if match_found:
        return True, "Validé"
    
    return False, "Exclu (Pas de mot clé pertinent)"

def main():
    print("🧹 Démarrage du Grand Nettoyage des Leads...")
    
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"Fichier {INPUT_FILE} introuvable.")
        return

    filtered_leads = []
    
    print(f"Total leads avant filtrage : {len(df)}")
    
    for index, row in df.iterrows():
        relevant, reason = is_relevant(row)
        if relevant:
            filtered_leads.append(row)
        # else:
            # print(f"  ❌ {row['Titre'][:40]}... -> {reason}")

    df_filtered = pd.DataFrame(filtered_leads)
    
    if not df_filtered.empty:
        df_filtered.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
        print(f"\n✅ Terminé ! {len(df_filtered)} leads qualifiés sauvegardés dans '{OUTPUT_FILE}'.")
        
        # Afficher la 'Pépite' potentielle (la première du fichier filtré)
        best_lead = df_filtered.iloc[0]
        print("\n💎 CANDIDAT PÉPITE IDENTIFIÉ :")
        print(f"Titre : {best_lead['Titre']}")
        print(f"Lien : {best_lead['Lien']}")
        print(f"Date : {best_lead['Date']}")
        print("-" * 20)
        print(f"Début Email Généré (si dispo) :\n{str(best_lead.get('Email_Genere', 'N/A'))[:200]}...")
        
    else:
        print("\n⚠️ Aucun lead n'a survécu au filtrage. Vérifiez les critères.")

if __name__ == "__main__":
    main()
