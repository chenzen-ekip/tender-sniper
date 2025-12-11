
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import csv

# URL cible demandée
URL = "https://www.marchesonline.com/appels-offres/top-recherches/nettoyage"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://www.marchesonline.com/"
}

def clean_text(text):
    if text:
        return re.sub(r'\s+', ' ', text).strip()
    return "N/A"

def main():
    print(f"Scraping : {URL}")
    
    try:
        response = requests.get(URL, headers=HEADERS, timeout=15)
        response.raise_for_status() # Lève une exception si erreur HTTP

        soup = BeautifulSoup(response.text, "html.parser")
        
        # Trouver les liens d'annonces
        # On garde la logique qui a fonctionné: recherche des liens contenant "/appels-offres/avis/"
        ad_links = soup.find_all("a", href=lambda h: h and "/appels-offres/avis/" in h)
        
        print(f"Nombre de liens potentiels trouvés : {len(ad_links)}")

        leads = []
        seen_urls = set()

        for link in ad_links:
            href = link.get('href')
            full_url = urljoin("https://www.marchesonline.com", href) # Reconstruire le lien complet
            
            # Déduplication
            if full_url in seen_urls:
                continue
            
            title = link.get_text(strip=True)
            # Filtrage des liens non pertinents (trop courts)
            if len(title) < 5:
                continue
                
            seen_urls.add(full_url)
            
            # Extraction de la date (remontée dans le parent comme validé précédemment)
            date_pub = "Non trouvée"
            current_elem = link
            # On remonte jusqu'à 4 niveaux parents pour trouver une date
            for _ in range(4):
                if not current_elem: break
                text_content = current_elem.get_text(" ", strip=True)
                match = re.search(r"(\d{2}/\d{2}/\d{4})", text_content)
                if match:
                    date_pub = match.group(1)
                    break
                current_elem = current_elem.parent

            leads.append({
                "Titre": title,
                "Date": date_pub,
                "Lien": full_url
            })

        # Sauvegarde CSV
        csv_filename = 'leads_nettoyage.csv'
        if leads:
            with open(csv_filename, mode='w', newline='', encoding='utf-8-sig') as csvfile:
                fieldnames = ['Titre', 'Date', 'Lien']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for lead in leads:
                    writer.writerow(lead)
            
            print(f"Succès ! {len(leads)} leads sauvegardés dans '{csv_filename}'.")
        else:
            print("Aucune lead trouvée. Vérifiez la structure de la page ou les sélecteurs.")

    except requests.RequestException as e:
        print(f"Erreur de réseau ou HTTP : {e}")
    except Exception as e:
        print(f"Une erreur inattendue est survenue : {e}")

if __name__ == "__main__":
    main()
