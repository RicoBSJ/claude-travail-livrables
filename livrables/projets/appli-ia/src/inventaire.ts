// src/inventaire.ts — Inventaire typé des livrables (TypeScript)
// Mis à jour leçon 04 (21/08/2026) :
//   - fs.promises (async/await) remplace fs synchrone
//   - date et slug extraits du NOM (écart n°3 résolu)
//   - Livrable aligné sur la nouvelle interface de types.ts
//
// Lance (après compilation) : npm run build && npm run inventaire:ts

import * as fs   from 'node:fs/promises';
import * as path from 'node:path';
import type { Livrable, DossierConfig } from './types';

// Le script compilé vit dans livrables/projets/appli-ia/dist/
// On remonte de 4 niveaux pour atteindre la racine Claude_Travail/
const RACINE: string = path.resolve(__dirname, '..', '..', '..', '..');

const CATEGORIES: Record<string, DossierConfig> = {
  lecons:       { chemin: path.join(RACINE, 'livrables', 'lecons'),       extensions: ['.docx', '.md'] },
  quiz:         { chemin: path.join(RACINE, 'livrables', 'quiz'),         extensions: ['.pptx'] },
  infographies: { chemin: path.join(RACINE, 'livrables', 'infographies'), extensions: ['.pptx'] },
  veilles:      { chemin: path.join(RACINE, 'sources',   'veille'),       extensions: ['.docx', '.md'] },
  documents:    { chemin: path.join(RACINE, 'livrables', 'documents'),    extensions: ['.docx', '.pdf'] },
  controles:    { chemin: path.join(RACINE, 'livrables', 'controles'),    extensions: ['.md', '.docx'] },
};

const DOCS_DE_DOSSIER: string[] = ['readme.md'];

// ── Helpers ────────────────────────────────────────────────────────────────

function extracterDate(nom: string): string | null {
  const match = nom.match(/^(\d{4}-\d{2}-\d{2})/);
  return match ? match[1] : null;
}

function extraerSlug(nom: string): string {
  const { name } = path.parse(nom);
  const match = name.match(/^\d{4}-\d{2}-\d{2}_(.+)$/);
  return match ? match[1] : name;
}

function estLivrable(nom: string, extensions: string[]): boolean {
  if (nom.startsWith('~$')) return false;
  if (DOCS_DE_DOSSIER.includes(nom.toLowerCase())) return false;
  return extensions.includes(path.extname(nom).toLowerCase());
}

// ── Inventaire async ───────────────────────────────────────────────────────

async function inventorierDossier(
  dossierPath: string,
  extensions: string[],
  recursif: boolean
): Promise<Livrable[]> {
  const livrables: Livrable[] = [];
  let entrees;
  try {
    entrees = await fs.readdir(dossierPath, { withFileTypes: true });
  } catch {
    return livrables;
  }
  for (const entree of entrees) {
    if (entree.isDirectory() && recursif) {
      const sous = await inventorierDossier(
        path.join(dossierPath, entree.name),
        extensions,
        true
      );
      livrables.push(...sous);
    } else if (entree.isFile() && estLivrable(entree.name, extensions)) {
      const fichierPath = path.join(dossierPath, entree.name);
      let taille = 0;
      try {
        const stats = await fs.stat(fichierPath);
        taille = stats.size;
      } catch { /* inaccessible */ }
      livrables.push({
        nom:       entree.name,
        date:      extracterDate(entree.name),
        slug:      extraerSlug(entree.name),
        taille,
        extension: path.extname(entree.name).toLowerCase(),
      });
    }
  }
  return livrables;
}

// ── Affichage terminal ─────────────────────────────────────────────────────

async function main(): Promise<void> {
  console.log('Portail Livrables — inventaire TypeScript (leçon 04)\n');

  let totalFichiers = 0;
  let totalOctets   = 0;

  for (const [cle, config] of Object.entries(CATEGORIES)) {
    const estRecursif = cle === 'veilles';
    const livrables   = await inventorierDossier(config.chemin, config.extensions, estRecursif);
    const octets      = livrables.reduce((s, l) => s + l.taille, 0);
    const ko          = Math.round(octets / 1024);

    totalFichiers += livrables.length;
    totalOctets   += octets;

    console.log(`${cle.padEnd(14)} ${String(livrables.length).padStart(4)} fichier(s)   ${String(ko).padStart(7)} Ko`);

    // Afficher les 3 premiers avec date + slug
    const triés = [...livrables].sort((a, b) => {
      if (a.date === null && b.date === null) return 0;
      if (a.date === null) return 1;
      if (b.date === null) return -1;
      return b.date.localeCompare(a.date);
    });
    triés.slice(0, 3).forEach(l => {
      const d = (l.date ?? '(sans date)').padEnd(12);
      console.log(`   ${d}  ${l.slug}`);
    });
    if (livrables.length > 3) {
      console.log(`   … et ${livrables.length - 3} autre(s)`);
    }
    console.log();
  }

  const totalMo = (totalOctets / 1024 / 1024).toFixed(2);
  console.log('─'.repeat(52));
  console.log(`Total : ${totalFichiers} fichiers — ${totalMo} Mo`);
}

main().catch(console.error);
