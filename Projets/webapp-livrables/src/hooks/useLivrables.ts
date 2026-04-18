"use client";

import { useEffect, useState } from "react";

export interface Livrable {
  id: string;
  name: string;
  path: string;
  size: number;
  date: string;
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

export type LivrablesCategory = keyof Omit<LivrablesResponse, "_meta">;

interface UseLivrablesResult {
  data: LivrablesResponse | null;
  loading: boolean;
  error: string | null;
  refetch: () => void;
}

/**
 * Hook React pour consommer /api/livrables.
 * Utilisable dans n'importe quel composant client pour accéder
 * aux livrables scannés par l'API Route Next.js.
 *
 * @example
 * const { data, loading, error } = useLivrables();
 * if (data) console.log(data.quiz.length, "quiz trouvés");
 */
export function useLivrables(): UseLivrablesResult {
  const [data, setData] = useState<LivrablesResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [tick, setTick] = useState(0);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);

    fetch("/api/livrables")
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status} — ${res.statusText}`);
        return res.json() as Promise<LivrablesResponse>;
      })
      .then((json) => {
        if (!cancelled) {
          setData(json);
          setLoading(false);
        }
      })
      .catch((err: unknown) => {
        if (!cancelled) {
          const msg = err instanceof Error ? err.message : String(err);
          setError(msg);
          setLoading(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [tick]);

  const refetch = () => setTick((t) => t + 1);

  return { data, loading, error, refetch };
}

/**
 * Formate la taille d'un fichier en chaîne lisible.
 * @example formatSize(102400) // "100,0 Ko"
 */
export function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} o`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} Ko`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} Mo`;
}

/**
 * Formate une date ISO en date courte française.
 * @example formatDate("2026-04-16T08:20:00Z") // "16 avr. 2026"
 */
export function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString("fr-FR", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}
