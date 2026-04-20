import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

const LIVRABLES_ROOT =
  process.env.LIVRABLES_PATH ||
  "/Users/utilisateur/kDrive/Claude_Travail/Livrables";

const VEILLE_ROOT =
  process.env.VEILLE_PATH ||
  "/Users/utilisateur/kDrive/Claude_Travail/Sources/Veille";

const VALID_EXTS = [".docx", ".pptx", ".pdf", ".md", ".xlsx"];

interface CategoryStats {
  count: number;
  total_size_bytes: number;
  latest_date: string | null;
  extensions: Record<string, number>;
}

interface StatsResponse {
  generated_at: string;
  total_files: number;
  total_size_bytes: number;
  categories: {
    quiz: CategoryStats;
    infographies: CategoryStats;
    lecons: CategoryStats;
    veilles: CategoryStats;
    projets: CategoryStats;
  };
  /** Livrables créés dans les 7 derniers jours */
  recent_count: number;
  /** Livrables créés dans les 30 derniers jours */
  monthly_count: number;
}

function scanStats(dir: string, recursive = false): CategoryStats {
  const stats: CategoryStats = {
    count: 0,
    total_size_bytes: 0,
    latest_date: null,
    extensions: {},
  };

  if (!fs.existsSync(dir)) return stats;

  const entries = fs.readdirSync(dir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory() && recursive) {
      const sub = scanStats(fullPath, true);
      stats.count += sub.count;
      stats.total_size_bytes += sub.total_size_bytes;
      for (const [ext, n] of Object.entries(sub.extensions)) {
        stats.extensions[ext] = (stats.extensions[ext] ?? 0) + n;
      }
      if (
        sub.latest_date &&
        (!stats.latest_date || sub.latest_date > stats.latest_date)
      ) {
        stats.latest_date = sub.latest_date;
      }
    } else if (entry.isFile()) {
      const ext = path.extname(entry.name).toLowerCase();
      if (!VALID_EXTS.includes(ext)) continue;
      try {
        const s = fs.statSync(fullPath);
        stats.count++;
        stats.total_size_bytes += s.size;
        stats.extensions[ext] = (stats.extensions[ext] ?? 0) + 1;
        const iso = s.mtime.toISOString();
        if (!stats.latest_date || iso > stats.latest_date) {
          stats.latest_date = iso;
        }
      } catch {
        /* skip */
      }
    }
  }

  return stats;
}

function countRecent(catStats: CategoryStats[], cutoffMs: number): number {
  // On ne peut pas connaître les dates individuelles ici — on relit le FS
  // Cette fonction est appelée en dehors du scan pour les stats agrégées
  return catStats.reduce((acc) => acc, 0); // placeholder
}

export async function GET(): Promise<NextResponse<StatsResponse>> {
  try {
    const now = Date.now();
    const week = now - 7 * 24 * 60 * 60 * 1000;
    const month = now - 30 * 24 * 60 * 60 * 1000;

    const categories = {
      quiz:          scanStats(path.join(LIVRABLES_ROOT, "Quiz")),
      infographies:  scanStats(path.join(LIVRABLES_ROOT, "Infographies")),
      lecons:        scanStats(path.join(LIVRABLES_ROOT, "Leçons")),
      veilles:       scanStats(VEILLE_ROOT),
      projets:       scanStats(path.join(LIVRABLES_ROOT, "Projets"), true),
    };

    const allCats = Object.values(categories);
    const total_files = allCats.reduce((s, c) => s + c.count, 0);
    const total_size_bytes = allCats.reduce((s, c) => s + c.total_size_bytes, 0);

    // Pour recent/monthly on recompte depuis le FS directement
    function countRecentInDir(dir: string, cutoffMs: number, recursive = false): number {
      if (!fs.existsSync(dir)) return 0;
      let n = 0;
      for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
        const fp = path.join(dir, entry.name);
        if (entry.isDirectory() && recursive) {
          n += countRecentInDir(fp, cutoffMs, true);
        } else if (entry.isFile() && VALID_EXTS.includes(path.extname(entry.name).toLowerCase())) {
          try {
            if (fs.statSync(fp).mtime.getTime() >= cutoffMs) n++;
          } catch { /* skip */ }
        }
      }
      return n;
    }

    const dirs = [
      { dir: path.join(LIVRABLES_ROOT, "Quiz"),          rec: false },
      { dir: path.join(LIVRABLES_ROOT, "Infographies"),   rec: false },
      { dir: path.join(LIVRABLES_ROOT, "Leçons"),         rec: false },
      { dir: VEILLE_ROOT,                                  rec: false },
      { dir: path.join(LIVRABLES_ROOT, "Projets"),         rec: true  },
    ];

    const recent_count  = dirs.reduce((s, d) => s + countRecentInDir(d.dir, week,  d.rec), 0);
    const monthly_count = dirs.reduce((s, d) => s + countRecentInDir(d.dir, month, d.rec), 0);

    return NextResponse.json({
      generated_at: new Date().toISOString(),
      total_files,
      total_size_bytes,
      categories,
      recent_count,
      monthly_count,
    });
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : "Erreur inconnue";
    console.error("[/api/livrables/stats]", message);
    return NextResponse.json(
      { error: message } as unknown as StatsResponse,
      { status: 500 }
    );
  }
}
