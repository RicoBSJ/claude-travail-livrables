export default function ProjetsPage() {
  return (
    <div className="max-w-5xl mx-auto px-6 py-10">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-[#1B3A6B]">Projets</h1>
        <p className="text-gray-500 text-sm mt-1">Guides et livrables des projets en cours (Web App, Agents Claude, MCP)</p>
      </div>
      <div className="bg-white rounded-xl border border-red-100 shadow-sm p-8 text-center">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-red-50 text-3xl mb-4">🚀</div>
        <h2 className="text-lg font-semibold text-[#1B3A6B] mb-2">Catalogue des projets à venir</h2>
        <p className="text-gray-500 text-sm max-w-md mx-auto">
          La liste des projets sera disponible à la session 04 (API Route + catalogue avec filtres).
        </p>
        <div className="mt-6 inline-block bg-red-50 text-red-700 text-xs font-medium px-3 py-1.5 rounded-full">
          Session 04 — Catalogue &amp; Filtres
        </div>
      </div>
    </div>
  );
}
