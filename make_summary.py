
import os
from openai import OpenAI
from fpdf import FPDF
import unidecode

# Configuration
API_KEY = "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"

client = OpenAI(api_key=API_KEY)
MODEL = "gpt-4o-mini"
INPUT_FILE = "raw_tender.txt"
OUTPUT_PDF = "Synthese_Marche_CD92.pdf"
OUTPUT_MD = "Synthese_Marche_CD92.md"

def get_summary(text):
    prompt = """Agis comme un expert en appels d'offres. Voici le texte brut d'une annonce de marché public pour de l'assainissement.

    Fais-moi une Fiche de Synthèse d'une page (Executive Summary) pour le dirigeant de l'entreprise qui souhaite répondre.

    Structure la fiche exactement comme ça :

    TITRE: [Titre du Marché & Lieu]
    DATE_LIMITE: [Date Limite]
    CHIFFRES_CLES: [Durée, montant estimé, volume...]
    MATERIEL: [Matériel Requis / Contraintes Techniques]
    CRITERES: [Critères de sélection]

    Le ton doit être ultra-pro et direct. Pas de bla-bla.
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Tu es un expert en synthèse de marchés publics."},
            {"role": "user", "content": f"{prompt}\n\nTEXTE:\n{text}"}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

def create_pdf(text, filename):
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Fiche de Synthèse - Marché Public", ln=True, align='C')
    pdf.ln(10)

    # Content
    pdf.set_font("Arial", size=11)
    
    lines = text.split('\n')
    for line in lines:
        # Handling basic encoding for FPDF (latin-1 limitation)
        # Using unidecode to be safe or explicit replacement
        # FPDF standard font doesn't support full unicode (like emoji or some symbols), so we replace roughly.
        try:
            line_encoded = line.encode('latin-1', 'replace').decode('latin-1')
        except:
            line_encoded = unidecode.unidecode(line)

        if "TITRE:" in line:
            pdf.set_font("Arial", 'B', 12)
            pdf.multi_cell(0, 10, line.replace("TITRE:", "").strip())
            pdf.ln(2)
        elif "DATE_LIMITE:" in line:
            pdf.set_font("Arial", 'B', 12)
            pdf.set_text_color(220, 50, 50) # Red
            pdf.cell(0, 10, clean_text(line), ln=True)
            pdf.set_text_color(0, 0, 0) # Reset
            pdf.ln(2)
        elif any(x in line for x in ["CHIFFRES_CLES:", "MATERIEL:", "CRITERES:"]):
             pdf.set_font("Arial", 'B', 11)
             pdf.cell(0, 10, clean_text(line), ln=True)
             pdf.set_font("Arial", size=11)
        else:
             pdf.set_font("Arial", size=11)
             pdf.multi_cell(0, 6, clean_text(line))
             
    pdf.output(filename)

def clean_text(text):
    # Helper to clean up text for FPDF latin-1
    text = text.replace("’", "'").replace("–", "-").replace("€", "Euros")
    try:
        return text.encode('latin-1', 'replace').decode('latin-1')
    except:
        return unidecode.unidecode(text)

def main():
    print("lecture du texte...")
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            raw_text = f.read()
    except FileNotFoundError:
        print("Erreur: raw_tender.txt introuvable.")
        return

    print("Génération du résumé IA...")
    summary = get_summary(raw_text)
    
    print("Sauvegarde Markdown...")
    with open(OUTPUT_MD, 'w', encoding='utf-8') as f:
        f.write("# Fiche de Synthèse\n\n" + summary)
        
    print("Génération PDF...")
    try:
        create_pdf(summary, OUTPUT_PDF)
        print(f"PDF créé : {OUTPUT_PDF}")
    except Exception as e:
        print(f"Erreur PDF: {e}")
        # Fallback if FPDF fails
        pass

if __name__ == "__main__":
    main()
