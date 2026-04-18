export default function VeillesPage() {
  return (
    <div className="max-w-5xl mx-auto px-6 py-10">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-[#1B3A6B]">Veilles</h1>
        <p className="text-gray-500 text-sm mt-1">Veilles HAS/ANESM, SERAFIN-PH et actualités sectorielles</p>
      </div>
      <div className="bg-white rounded-xl border border-orange-100 shadow-sm p-8 text-center">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-orange-50 text-3xl mb-4">📡</div>
        <h2 className="text-lg font-semibold text-[#1B3A6B] mb-2">Catalogue des veilles à venir</h2>
        <p className="text-gray-500 text-sm max-w-md mx-auto">
          La liste des veilles sera disponible à la session 04 (API Route + catalogue avec filtres).
        </p>
        <div className="mt-6 inline-block bg-orange-50 text-orange-700 text-xs font-medium px-3 py-1.5 rounded-full">
          Session 04 — Catalogue &amp; Filtres
        </div>
      </div>
    </div>
  );
}
