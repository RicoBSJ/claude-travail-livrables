"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function Header() {
  const router = useRouter();
  const [query, setQuery] = useState("");

  function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    if (query.trim()) {
      router.push(`/recherche?q=${encodeURIComponent(query.trim())}`);
    }
  }

  return (
    <header className="h-14 bg-white border-b border-gray-200 flex items-center px-6 gap-4 shadow-sm flex-shrink-0">
      {/* Titre page courante — sera affiché dynamiquement via le breadcrumb plus tard */}
      <div className="flex-1">
        <Link href="/" className="text-[#1B3A6B] font-semibold text-sm hover:underline">
          Portail Livrables
        </Link>
      </div>

      {/* Barre de recherche */}
      <form onSubmit={handleSearch} className="flex items-center gap-2">
        <div className="relative">
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-4.35-4.35M17 11A6 6 0 115 11a6 6 0 0112 0z" />
            </svg>
          </span>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Rechercher un livrable…"
            className="pl-9 pr-4 py-1.5 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#1B3A6B]/40 focus:border-[#1B3A6B] w-64 bg-gray-50"
          />
        </div>
        <button
          type="submit"
          className="px-3 py-1.5 text-sm bg-[#1B3A6B] text-white rounded-lg hover:bg-[#2a5298] transition-colors"
        >
          OK
        </button>
      </form>
    </header>
  );
}
