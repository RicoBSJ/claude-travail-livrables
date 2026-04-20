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

/** Filtre une liste de livrables selon les critères de la requête */
function applyFilters(
  items: Livrable[],
  opts: { category?: string; ext?: string; days?: number; q?: string }
): Livrable[] {
  let result = items;

  // Filtre catégorie
  if (opts.category) {
    result = result.filter((l) => l.category === opts.category);
  }

  // Filtre extension (ex: .pptx, .docx)
  if (opts.ext) {
    const ext = opts.ext.startsWith(".") ? opts.ext : `.${opts.ext}`;
    result = result.filter((l) => l.extension === ext.toLowerCase());
  }

  // Filtre temporel (N derniers jours)
  if (opts.days && opts.days > 0) {
    const cutoff = Date.now() - opts.days * 24 * 60 * 60 * 1000;
    result = result.filter((l) => new Date(l.date).getTime() >= cutoff);
  }

  // Recherche textuelle sur le nom de fichier
  if (opts.q) {
    const query = opts.q.toLowerCase();
    result = result.filter((l) => l.name.toLowerCase().includes(query));
  }

  return result;
}

export async function GET(request: Request): Promise<NextResponse<LivrablesResponse>> {
  try {
    // Paramètres de filtrage depuis l'URL
    const { searchParams } = new URL(request.url);
    const category = searchParams.get("category") ?? undefined;
    const ext      = searchParams.get("ext") ?? undefined;
    const days     = searchParams.get("days") ? Number(searchParams.get("days")) : undefined;
    const q        = searchParams.get("q") ?? undefined;

    const filters = { category, ext, days, q };

    const quiz = applyFilters(
      scanDirectory(path.join(LIVRABLES_ROOT, "Quiz"), "quiz"),
      filters
    );

    const infographies = applyFilters(
      scanDirectory(path.join(LIVRABLES_ROOT, "Infographies"), "infographies"),
      filters
    );

    const lecons = applyFilters(
      scanDirectory(path.join(LIVRABLES_ROOT, "Leçons"), "lecons"),
      filters
    );

    const veilles = applyFilters(
      scanDirectory(VEILLE_ROOT, "veilles"),
      filters
    );

    const projets = applyFilters(
      scanDirectory(path.join(LIVRABLES_ROOT, "Projets"), "projets", true),
      filters
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
