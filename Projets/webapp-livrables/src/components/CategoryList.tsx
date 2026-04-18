"use client";

import { useLivrables, formatSize, formatDate, LivrablesCategory } from "@/hooks/useLivrables";

interface CategoryConfig {
  key: LivrablesCategory;
  icon: string;
  color: {
    border: string;
    iconBg: string;
    badge: string;
    emptyBorder: string;
  };
  emptyText: string;
  emptyPath: string;
}

interface CategoryListProps {
  config: CategoryConfig;
}

/**
 * CategoryList — Composant générique pour afficher la liste des livrables
 * d'une catégorie donnée, en consommant /api/livrables via le hook useLivrables.
 *
 * Préfigure la session 04 (grille de cards avec filtres) en affichant
 * dès maintenant la liste brute issue de l'API.
 */
export default function CategoryList({ config }: CategoryListProps) {
  const { data, loading, error } = useLivrables();

  if (loading) {
    return (
      <div className="animate-pulse space-y-3">
        {[1, 2, 3].map((i) => (
          <div key={i} className="h-16 bg-gray-100 rounded-xl" />
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-sm text-red-700">
        Erreur lors du chargement : {error}
      </div>
    );
  }

  const items = data ? data[config.key] : [];

  if (!items || items.length === 0) {
    return (
      <div
        className={`bg-white rounded-xl border ${config.color.emptyBorder} shadow-sm p-8 text-center`}
      >
        <div
          className={`inline-flex items-center justify-center w-16 h-16 rounded-full ${config.color.iconBg} text-3xl mb-4`}
        >
          {config.icon}
        </div>
        <h2 className="text-lg font-semibold text-[#1B3A6B] mb-2">
          Aucun fichier disponible
        </h2>
        <p className="text-gray-500 text-sm max-w-md mx-auto">
          Les fichiers seront affichés ici dès qu&apos;ils seront présents dans{" "}
          <code className="bg-gray-100 px-1 rounded text-xs">{config.emptyPath}</code>.
        </p>
        <p className="text-gray-400 text-xs mt-3">
          {config.emptyText}
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <p className="text-sm text-gray-500 mb-4">
        {items.length} fichier{items.length > 1 ? "s" : ""} trouvé{items.length > 1 ? "s" : ""}
        {" "}— tri par date de modification (plus récent en premier)
      </p>
      {items.map((item) => (
        <div
          key={item.id}
          className={`bg-white rounded-xl border ${config.color.border} shadow-sm p-4 flex items-center gap-4 hover:shadow-md transition-shadow`}
        >
          <div
            className={`inline-flex items-center justify-center w-10 h-10 rounded-full ${config.color.iconBg} text-xl flex-shrink-0`}
          >
            {config.icon}
          </div>
          <div className="flex-1 min-w-0">
            <p className="font-medium text-[#1B3A6B] truncate text-sm">{item.name}</p>
            <p className="text-xs text-gray-400 mt-0.5">
              {formatDate(item.date)} &middot; {formatSize(item.size)}
            </p>
          </div>
          <span
            className={`text-xs ${config.color.badge} font-medium px-2.5 py-1 rounded-full flex-shrink-0`}
          >
            {item.extension.replace(".", "").toUpperCase()}
          </span>
        </div>
      ))}
    </div>
  );
}
