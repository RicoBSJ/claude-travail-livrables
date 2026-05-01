#!/usr/bin/env node
/**
 * xlsx-to-md.js
 * Convertit un fichier Excel (.xlsx, .xls) ou CSV en Markdown
 *
 * Installation (une seule fois) :
 *   npm install xlsx
 *
 * Usage :
 *   node xlsx-to-md.js fichier.xlsx
 *   node xlsx-to-md.js fichier.xlsx --output ./md/
 *   node xlsx-to-md.js fichier.xlsx --sheet "Feuil1"
 *   node xlsx-to-md.js fichier.xlsx --all-sheets
 */

const XLSX = require('xlsx');
const fs = require('fs');
const path = require('path');

// --- Helpers -----------------------------------------------------------------

function escapeMarkdown(value) {
  if (value === null || value === undefined) return '';
  return String(value)
    .replace(/\|/g, '\\|')      // échappe les pipes
    .replace(/\r?\n/g, '<br>')  // conserve les retours à la ligne
    .trim();
}

function sheetToMarkdown(sheet, sheetName) {
  const data = XLSX.utils.sheet_to_json(sheet, {
    header: 1,
    defval: '',
    blankrows: false,
  });

  if (data.length === 0) {
    return `## ${sheetName}\n\n*(feuille vide)*\n`;
  }

  const headers = data[0].map(escapeMarkdown);
  const rows = data.slice(1);
  const maxCols = Math.max(headers.length, ...rows.map(r => r.length));

  while (headers.length < maxCols) headers.push('');

  let md = `## ${sheetName}\n\n`;
  md += '| ' + headers.join(' | ') + ' |\n';
  md += '|' + headers.map(() => ' --- ').join('|') + '|\n';

  for (const row of rows) {
    const cells = [];
    for (let i = 0; i < maxCols; i++) {
      cells.push(escapeMarkdown(row[i]));
    }
    md += '| ' + cells.join(' | ') + ' |\n';
  }

  return md;
}

// --- Conversion principale ---------------------------------------------------

function convertFile(inputPath, options = {}) {
  const { outputDir, sheetName, allSheets } = options;

  if (!fs.existsSync(inputPath)) {
    console.error(`❌ Fichier introuvable : ${inputPath}`);
    process.exit(1);
  }

  const workbook = XLSX.readFile(inputPath);
  const baseName = path.basename(inputPath, path.extname(inputPath));
  const outDir = outputDir || path.dirname(inputPath);

  if (!fs.existsSync(outDir)) {
    fs.mkdirSync(outDir, { recursive: true });
  }

  let sheetsToProcess;
  if (sheetName) {
    if (!workbook.SheetNames.includes(sheetName)) {
      console.error(
        `❌ Feuille "${sheetName}" introuvable. ` +
        `Feuilles disponibles : ${workbook.SheetNames.join(', ')}`
      );
      process.exit(1);
    }
    sheetsToProcess = [sheetName];
  } else {
    sheetsToProcess = workbook.SheetNames;
  }

  if (allSheets) {
    // Un fichier .md par feuille
    for (const name of sheetsToProcess) {
      const md = sheetToMarkdown(workbook.Sheets[name], name);
      const safeName = name.replace(/[^a-zA-Z0-9_-]/g, '_');
      const outPath = path.join(outDir, `${baseName}_${safeName}.md`);
      fs.writeFileSync(outPath, md, 'utf8');
      console.log(`✅ ${outPath}`);
    }
  } else {
    // Un seul fichier .md regroupant toutes les feuilles
    let md = `# ${baseName}\n\n`;
    for (const name of sheetsToProcess) {
      md += sheetToMarkdown(workbook.Sheets[name], name) + '\n';
    }
    const outPath = path.join(outDir, `${baseName}.md`);
    fs.writeFileSync(outPath, md, 'utf8');
    console.log(`✅ ${outPath}`);
  }
}

// --- CLI ---------------------------------------------------------------------

function parseArgs(argv) {
  const args = { files: [] };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--output' || a === '-o') args.outputDir = argv[++i];
    else if (a === '--sheet' || a === '-s') args.sheetName = argv[++i];
    else if (a === '--all-sheets') args.allSheets = true;
    else if (a === '--help' || a === '-h') args.help = true;
    else args.files.push(a);
  }
  return args;
}

function printHelp() {
  console.log(`
xlsx-to-md — Convertit Excel/CSV en Markdown

Usage :
  node xlsx-to-md.js <fichier> [options]

Options :
  -o, --output <dossier>   Dossier de sortie (défaut : même que l'entrée)
  -s, --sheet <nom>        Convertir une feuille spécifique uniquement
  --all-sheets             Générer un .md séparé par feuille
  -h, --help               Afficher cette aide

Exemples :
  node xlsx-to-md.js donnees.xlsx
  node xlsx-to-md.js donnees.xlsx --output ./md/
  node xlsx-to-md.js donnees.xlsx --sheet "Résultats"
  node xlsx-to-md.js donnees.xlsx --all-sheets
`);
}

const args = parseArgs(process.argv);
if (args.help || args.files.length === 0) {
  printHelp();
  process.exit(args.help ? 0 : 1);
}

for (const file of args.files) {
  convertFile(file, args);
}
