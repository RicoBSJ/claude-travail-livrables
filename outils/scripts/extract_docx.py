import zipfile
import xml.etree.ElementTree as ET
import sys
import os
import re

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
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
    
    return '\n'.join(text_parts), urls

if __name__ == '__main__':
    filepath = sys.argv[1]
    text, urls = extract_text_and_urls(filepath)
    print(f"=== URLS ({len(urls)}) ===")
    for url in urls:
        print(url)
    print(f"\n=== TEXT (excerpt) ===")
    # Print first 3000 chars
    print(text[:3000])
