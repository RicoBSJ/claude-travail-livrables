"use client";

import { useEffect, useState } from "react";

interface LivrableMeta {
  generated_at: string;
  total: number;
  livrables_root: string;
}

interface LivrablesData {
  quiz: unknown[];
  infographies: unknown[];
  lecons: unknown[];
  veilles: unknown[];
  projets: unknown[];
  _meta: LivrableMeta;
}

/**
 * LivrablesStats — Composant client qui interroge /api/livrables
 * et affiche un tableau de bord des compteurs par catégorie.
 * Utilisé en session 03 pour démontrer le fonctionnement de l'API Route.
 */
export default function LivrablesStats() {
  const [data, setData] = useState<LivrablesData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/livrables")
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json() as Promise<LivrablesData>;
      })
      .then((json) => {
        setData(json);
        setLoading(false);
      })
      .catch((err: unknown) => {
        const msg = err instanceof Error ? err.message : String(err);
        setError(msg);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="animate-pulse bg-gray-100 rounded-xl h-28 flex items-center justify-center text-gray-400 text-sm">
        Chargement des statistiques…
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-sm text-red-700">
        Impossible de contacter <code>/api/livrables</code> : {error}
      </div>
    );
  }

  const categories = [
    { key: "quiz",         label: "Quiz",        icon: "🧠", color: "bg-blue-50 text-blue-700" },
    { key: "infographies", label: "Infographies", icon: "🌸", color: "bg-purple-50 text-purple-700" },
    { key: "lecons",       label: "Leçons",       icon: "📖", color: "bg-green-50 text-green-700" },
    { key: "veilles",      label: "Veilles",      icon: "📡", color: "bg-orange-50 text-orange-700" },
    { key: "projets",      label: "Projets",      icon: "🚀", color: "bg-red-50 text-red-700" },
  ] as const;

  return (
    <div className="space-y-4">
      {/* Compteurs par catégorie */}
      <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
        {categories.map((cat) => {
          const count = (data[cat.key] as unknown[]).length;
          return (
            <div
              key={cat.key}
              className={`rounded-xl p-3 text-center ${cat.color} border border-current/10`}
            >
              <div className="text-2xl mb-1">{cat.icon}</div>
              <div className="text-2xl font-bold">{count}</div>
              <div className="text-xs font-medium opacity-80">{cat.label}</div>
            </div>
          );
        })}
      </div>

      {/* Métadonnées */}
      <div className="bg-gray-50 border border-gray-200 rounded-lg px-4 py-2 flex flex-wrap gap-x-6 gap-y-1 text-xs text-gray-500">
        <span>
          <strong className="text-gray-700">Total :</strong> {data._meta.total} livrables
        </span>
        <span>
          <strong className="text-gray-700">Généré le :</strong>{" "}
          {new Date(data._meta.generated_at).toLocaleString("fr-FR")}
        </span>
        <span className="hidden sm:inline truncate max-w-xs">
          <strong className="text-gray-700">Racine :</strong> {data._meta.livrables_root}
        </span>
      </div>
    </div>
  );
}
