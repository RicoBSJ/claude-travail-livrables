import Link from "next/link";
import LivrablesStats from "@/components/LivrablesStats";

const categories = [
  {
    href: "/quiz",
    label: "Quiz",
    icon: "🧠",
    description: "QCM PowerPoint sur les RBPP, bientraitance et pratiques professionnelles",
    color: "bg-blue-50 border-blue-200 hover:bg-blue-100",
    iconBg: "bg-blue-100",
  },
  {
    href: "/infographies",
    label: "Infographies",
    icon: "🌸",
    description: "Infographies format pétale et cartes visuelles sur les thématiques médico-sociales",
    color: "bg-purple-50 border-purple-200 hover:bg-purple-100",
    iconBg: "bg-purple-100",
  },
  {
    href: "/lecons",
    label: "Leçons",
    icon: "📖",
    description: "Leçons hebdomadaires Claude Code et NO-CODE+IA pour la montée en compétences",
    color: "bg-green-50 border-green-200 hover:bg-green-100",
    iconBg: "bg-green-100",
  },
  {
    href: "/veilles",
    label: "Veilles",
    icon: "📡",
    description: "Veilles HAS/ANESM, SERAFIN-PH et actualités sectorielles",
    color: "bg-orange-50 border-orange-200 hover:bg-orange-100",
    iconBg: "bg-orange-100",
  },
  {
    href: "/projets",
    label: "Projets",
    icon: "🚀",
    description: "Guides et livrables des projets en cours (Web App, Agents Claude, MCP)",
    color: "bg-red-50 border-red-200 hover:bg-red-100",
    iconBg: "bg-red-100",
  },
];

export default function Home() {
  return (
    <div className="max-w-5xl mx-auto px-6 py-10">
      {/* Intro */}
      <div className="mb-8 bg-white rounded-xl border border-gray-200 shadow-sm p-6">
        <h2 className="text-xl font-semibold text-[#1B3A6B] mb-2">
          Bienvenue sur le portail
        </h2>
        <p className="text-gray-600 leading-relaxed">
          Ce portail centralise tous les livrables produits dans le cadre du projet Claude_Travail :
          formations, quiz RBPP, infographies, veilles HAS/ANESM et supports pédagogiques.
          Il est destiné aux professionnels du secteur médico-social (ESSMS).
        </p>
      </div>

      {/* Categories grid */}
      <h2 className="text-lg font-semibold text-gray-700 mb-4">
        Accéder aux livrables par catégorie
      </h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        {categories.map((cat) => (
          <Link
            key={cat.href}
            href={cat.href}
            className={`flex flex-col rounded-xl border p-5 transition-colors ${cat.color} shadow-sm`}
          >
            <div className={`inline-flex items-center justify-center w-11 h-11 rounded-full ${cat.iconBg} text-2xl mb-3`}>
              {cat.icon}
            </div>
            <h3 className="text-base font-semibold text-[#1B3A6B] mb-1">
              {cat.label}
            </h3>
            <p className="text-sm text-gray-600 leading-relaxed">
              {cat.description}
            </p>
          </Link>
        ))}
      </div>

      {/* Tableau de bord API — Session 03 */}
      <div className="mt-10">
        <h2 className="text-lg font-semibold text-gray-700 mb-3">
          Tableau de bord des livrables
        </h2>
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-5">
          <LivrablesStats />
        </div>
      </div>

      {/* Statut du projet */}
      <div className="mt-6 bg-[#1B3A6B] text-white rounded-xl p-5 text-center">
        <p className="text-blue-200 text-sm">
          Session 03/10 — API Route /api/livrables · Prochaine étape : Catalogue &amp; Filtres
        </p>
      </div>
    </div>
  );
}
