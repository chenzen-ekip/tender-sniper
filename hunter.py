
import time
import re
import requests
import csv
from googlesearch import search
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

# Configuration
QUERIES = [
    "Entreprise assainissement 78", 
    "Entreprise hydrocurage 92", 
    "Société curage canalisation 91", 
    "Vidange fosse septique 95"
]

OUTPUT_FILE = "prospects.csv"
BLACKLIST_DOMAINS = ["wix.com", "sentry.io", "jpg", "png", "facebook.com", "linkedin.com", "instagram.com", "twitter.com", "societe.com", "pagesjaunes.fr", "mappy.com"]
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def extract_emails_from_text(text):
    # Regex standard pour email
    # On exclut les extensions images pour réduire le bruit
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    raw_emails = re.findall(email_pattern, text)
    
    clean_emails = set()
    for email in raw_emails:
        email = email.lower()
        if any(bad in email for bad in BLACKLIST_DOMAINS):
            continue
        if email.endswith(('png', 'jpg', 'jpeg', 'gif', 'svg', 'webp')):
            continue
        clean_emails.add(email)
    return list(clean_emails)

def scrape_site_emails(url):
    print(f"  --> Visite de {url}...")
    emails_found = set()
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            emails_found.update(extract_emails_from_text(response.text))
            
            # Essayer la page contact si possible
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                href = link['href']
                if 'contact' in href.lower():
                    contact_url = urljoin(url, href)
                    try:
                        print(f"    --> Visite Contact : {contact_url}")
                        resp_contact = requests.get(contact_url, headers=HEADERS, timeout=5)
                        if resp_contact.status_code == 200:
                            emails_found.update(extract_emails_from_text(resp_contact.text))
                    except:
                        pass
                    break # On en teste juste une pour pas spammer
                    
    except Exception as e:
        print(f"    Erreur visite : {e}")
    
    return list(emails_found)

def main():
    print("🚀 Lancement du Hunter...")
    
    results = []
    processed_urls = set()

    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(["Recherche", "Site_Web", "Email_Trouvé"])
        
        for query in QUERIES:
            print(f"\n🔍 Recherche : {query}")
            try:
                # Récupère 10 résultats, pause de 2s gérée par la lib ou manuellement
                search_results = search(query, num_results=10)
                
                for url in search_results:
                    # Filtrer les sites annuaires/inutiles si possible via domaine
                    domain = urlparse(url).netloc
                    if any(bad in domain for bad in BLACKLIST_DOMAINS):
                        continue
                        
                    if url in processed_urls:
                        continue
                    processed_urls.add(url)
                    
                    # Scrape
                    emails = scrape_site_emails(url)
                    time.sleep(2) # Politeness
                    
                    if emails:
                        print(f"    ✅ Emails trouvés : {emails}")
                        for email in emails:
                            writer.writerow([query, url, email])
                            f.flush() # Ecriture immédiate
                    else:
                        print("    ❌ Pas d'email trouvé.")
                        
            except Exception as e:
                print(f"Erreur recherche Google : {e}")

    print(f"\nTerminé ! Résultats dans {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
