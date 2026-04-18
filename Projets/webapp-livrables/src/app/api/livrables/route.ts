import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

// Chemin racine des livrables sur le système de fichiers local
const LIVRABLES_ROOT = process.env.LIVRABLES_PATH ||
  "/Users/utilisateur/kDrive/Claude_Travail/Livrables";

const VEILLE_ROOT = process.env.VEILLE_PATH ||
  "/Users/utilisateur/kDrive/Claude_Travail/Sources/Veille";

export interface Livrable {
  id: string;
  name: string;
  path: string;
  size: number;       // en octets
  date: string;       // ISO 8601
  category: string;
  extension: string;
}

export interface LivrablesResponse {
  quiz: Livrable[];
  infographies: Livrable[];
  lecons: Livrable[];
  veilles: Livrable[];
  projets: Livrable[];
  _meta: {
    generated_at: string;
    total: number;
    livrables_root: string;
  };
}

/**
 * Scanne un répertoire et retourne les fichiers avec leurs métadonnées.
 * @param dir       Chemin absolu du répertoire à scanner
 * @param category  Nom de la catégorie (pour le champ `category`)
 * @param recursive Si true, scanne récursivement les sous-dossiers
 */
function scanDirectory(
  dir: string,
  category: string,
  recursive = false
): Livrable[] {
  const results: Livrable[] = [];

  if (!fs.existsSync(dir)) {
    return results;
  }

  const entries = fs.readdirSync(dir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);

    if (entry.isDirectory() && recursive) {
      const sub = scanDirectory(fullPath, category, true);
      results.push(...sub);
    } else if (entry.isFile()) {
      const ext = path.extname(entry.name).toLowerCase();
      // On ne retient que les extensions documentaires
      if (![".docx", ".pptx", ".pdf", ".md", ".xlsx"].includes(ext)) {
        continue;
      }

      let stat: fs.Stats;
      try {
        stat = fs.statSync(fullPath);
      } catch {
        continue;
      }

      results.push({
        id: Buffer.from(fullPath).toString("base64url"),
        name: entry.name,
        path: fullPath,
        size: stat.size,
        date: stat.mtime.toISOString(),
        category,
        extension: ext,
      });
    }
  }

  // Tri : plus récent en premier (par date de modification)
  results.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());

  return results;
}

export async function GET(): Promise<NextResponse<LivrablesResponse>> {
  try {
    const quiz = scanDirectory(
      path.join(LIVRABLES_ROOT, "Quiz"),
      "quiz"
    );

    const infographies = scanDirectory(
      path.join(LIVRABLES_ROOT, "Infographies"),
      "infographies"
    );

    const lecons = scanDirectory(
      path.join(LIVRABLES_ROOT, "Leçons"),
      "lecons"
    );

    // Les veilles sont dans Sources/Veille/, pas dans Livrables/
    const veilles = scanDirectory(
      VEILLE_ROOT,
      "veilles"
    );

    // Les projets sont dans Livrables/Projets/ (arborescence récursive)
    const projets = scanDirectory(
      path.join(LIVRABLES_ROOT, "Projets"),
      "projets",
      true  // récursif pour webb-livrables/, claude-agents/, mcp-integrations/
    );

    const total = quiz.length + infographies.length + lecons.length + veilles.length + projets.length;

    const response: LivrablesResponse = {
      quiz,
      infographies,
      lecons,
      veilles,
      projets,
      _meta: {
        generated_at: new Date().toISOString(),
        total,
        livrables_root: LIVRABLES_ROOT,
      },
    };

    return NextResponse.json(response);
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : "Erreur inconnue";
    return NextResponse.json(
      {
        quiz: [],
        infographies: [],
        lecons: [],
        veilles: [],
        projets: [],
        _meta: {
          generated_at: new Date().toISOString(),
          total: 0,
          livrables_root: LIVRABLES_ROOT,
        },
        error: `Impossible de scanner les livrables : ${message}`,
      } as LivrablesResponse & { error: string },
      { status: 500 }
    );
  }
}
