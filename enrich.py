
import requests
from bs4 import BeautifulSoup
import csv
import time
import random

INPUT_CSV = "leads_nettoyage.csv"
OUTPUT_CSV = "leads_complets.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_description(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return "Erreur HTTP"
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Strategies to find description
        # 1. Look for a large block of text containing "Descriptif"
        # 2. Look for specific classes found in previous analysis or common patterns
        
        # Based on typical Marchesonline structure:
        content_div = soup.find("div", class_="avis-detail")
        if not content_div:
            content_div = soup.find("div", itemprop="description")
        
        if content_div:
            return content_div.get_text(separator="\n", strip=True)
            
        # Fallback: Find the div with the most text
        divs = soup.find_all("div")
        largest_div = None
        max_len = 0
        for d in divs:
            txt = d.get_text(strip=True)
            if len(txt) > max_len:
                # heuristic to ignore navbar/footer: check text density or keywords
                if "Mentions légales" in txt: continue 
                max_len = len(txt)
                largest_div = d
        
        if largest_div and max_len > 500:
             # Refine: try to get the text that is NOT in menu
             return largest_div.get_text(separator="\n", strip=True) # A bit crude but better than nothing

        return "Description non trouvée automatiquement."

    except Exception as e:
        return f"Erreur: {str(e)}"

def main():
    print("Démarrage de l'enrichissement...")
    
    leads = []
    with open(INPUT_CSV, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        leads = list(reader)
    
    total = len(leads)
    enriched_leads = []
    
    for i, lead in enumerate(leads, 1):
        url = lead.get("Lien")
        print(f"[{i}/{total}] Traitement : {lead.get('Titre')[:30]}...")
        
        if url and url.startswith("http"):
            desc = get_description(url)
            # Truncate slightly for CSV cell sanity if massive, but keep most
            if len(desc) > 30000: desc = desc[:30000] + "..."
            lead["Description_Texte"] = desc
        else:
            lead["Description_Texte"] = "URL invalide"
        
        enriched_leads.append(lead)
        
        # Pause to be polite
        time.sleep(1.0 + random.random() * 0.5)

    # Save to new CSV
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        fieldnames = ["Titre", "Date", "Lien", "Description_Texte"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(enriched_leads)
        
    print(f"\nTerminé ! Résultats dans {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
