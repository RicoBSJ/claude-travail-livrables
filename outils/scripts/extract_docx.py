import zipfile
import xml.etree.ElementTree as ET
import sys
import os
import re

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
R = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'

def extract_links(z):
    """Chaque lien du corps avec son LIBELLÉ visible et sa CIBLE : (libellé, url), dans l'ordre du document.
    Ajouté le 12/09/2026 : un contrôle qui ne lit que le texte ne sait pas qu'un libellé « Nexem » est un
    lien vers nexem.fr — il le traitait comme un nom sans adresse (passe A4)."""
    liens = []
    if 'word/document.xml' not in z.namelist() or 'word/_rels/document.xml.rels' not in z.namelist():
        return liens
    cibles = {}
    with z.open('word/_rels/document.xml.rels') as f:
        for rel in ET.parse(f).getroot().iter('{http://schemas.openxmlformats.org/package/2006/relationships}Relationship'):
            if 'hyperlink' in rel.get('Type', '').lower():
                cibles[rel.get('Id')] = rel.get('Target', '')
    with z.open('word/document.xml') as f:
        for h in ET.parse(f).getroot().iter(W + 'hyperlink'):
            rid = h.get(R + 'id')
            if rid in cibles and cibles[rid].startswith('http'):
                libelle = ''.join(t.text or '' for t in h.iter(W + 't')).strip()
                if libelle:
                    liens.append((libelle, cibles[rid]))
    return liens

def extract_text_and_urls(filepath):
    urls = []
    text_parts = []
    
    try:
        with zipfile.ZipFile(filepath, 'r') as z:
            # Extract text from document.xml
            if 'word/document.xml' in z.namelist():
                with z.open('word/document.xml') as f:
                    tree = ET.parse(f)
                    root = tree.getroot()
                    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                    for elem in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'):
                        if elem.text:
                            text_parts.append(elem.text)
            
            liens = []
            # Extract URLs from relationships
            rels_files = [n for n in z.namelist() if n.endswith('.rels')]
            for rels_file in rels_files:
                with z.open(rels_file) as f:
                    try:
                        tree = ET.parse(f)
                        root = tree.getroot()
                        for rel in root.iter('{http://schemas.openxmlformats.org/package/2006/relationships}Relationship'):
                            target = rel.get('Target', '')
                            rtype = rel.get('Type', '')
                            if 'hyperlink' in rtype.lower() and target.startswith('http'):
                                if target not in urls:
                                    urls.append(target)
                    except:
                        pass
            liens = extract_links(z)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        liens = []

    return '\n'.join(text_parts), urls, liens

USAGE = """Usage : python3 extract_docx.py <fichier.docx> [--extrait[=N]]

  (sans option)   affiche la TOTALITÉ du texte
  --extrait       affiche les 3000 premiers caractères
  --extrait=N     affiche les N premiers caractères
"""

if __name__ == '__main__':
    args = sys.argv[1:]
    if not args or args[0] in ('-h', '--help'):
        print(USAGE)
        sys.exit(0 if args else 1)

    filepath = args[0]
    if not os.path.isfile(filepath):
        print(f"ERREUR : fichier introuvable — {filepath}", file=sys.stderr)
        sys.exit(1)

    # Longueur à afficher : tout par défaut, tronqué seulement si --extrait est demandé
    limite = None
    for a in args[1:]:
        if a == '--extrait':
            limite = 3000
        elif a.startswith('--extrait='):
            try:
                limite = int(a.split('=', 1)[1])
            except ValueError:
                print(f"ERREUR : valeur invalide pour --extrait — {a}", file=sys.stderr)
                sys.exit(1)

    text, urls, liens = extract_text_and_urls(filepath)

    print(f"=== URLS ({len(urls)}) ===")
    for url in urls:
        print(url)

    # les liens du corps, libellé → cible (une ligne par lien, dans l'ordre du document)
    print(f"\n=== LIENS ({len(liens)}) ===")
    for libelle, url in liens:
        print(f"{libelle} → {url}")

    if limite is None:
        print(f"\n=== TEXTE COMPLET ({len(text)} caractères) ===")
        print(text)
    else:
        print(f"\n=== TEXTE — extrait de {min(limite, len(text))} sur {len(text)} caractères ===")
        print(text[:limite])
        if len(text) > limite:
            print(f"\n[... {len(text) - limite} caractères non affichés — relancer sans --extrait pour tout voir]")
