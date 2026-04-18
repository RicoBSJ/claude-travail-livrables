import { Suspense } from "react";

function RechercheContent() {
  return (
    <div className="max-w-5xl mx-auto px-6 py-10">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-[#1B3A6B]">Recherche</h1>
        <p className="text-gray-500 text-sm mt-1">Recherche plein texte dans tous les livrables</p>
      </div>
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-8 text-center">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gray-50 text-3xl mb-4">
          🔍
        </div>
        <h2 className="text-lg font-semibold text-[#1B3A6B] mb-2">Recherche fulltext à venir</h2>
        <p className="text-gray-500 text-sm max-w-md mx-auto">
          La recherche plein texte avec debounce et résultats live sera disponible à la session 07.
        </p>
        <div className="mt-6 inline-block bg-gray-100 text-gray-600 text-xs font-medium px-3 py-1.5 rounded-full">
          Session 07 — Recherche Fulltext
        </div>
      </div>
    </div>
  );
}

export default function RecherchePage() {
  return (
    <Suspense fallback={<div className="p-10 text-gray-400">Chargement…</div>}>
      <RechercheContent />
    </Suspense>
  );
}
