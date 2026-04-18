"use client";

import { useLivrables, formatSize, formatDate } from "@/hooks/useLivrables";

export default function QuizPage() {
  const { data, loading, error } = useLivrables();

  return (
    <div className="max-w-5xl mx-auto px-6 py-10">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-[#1B3A6B]">Quiz</h1>
        <p className="text-gray-500 text-sm mt-1">
          QCM PowerPoint sur les RBPP, bientraitance et pratiques professionnelles
        </p>
      </div>

      {loading && (
        <div className="animate-pulse space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-16 bg-gray-100 rounded-xl" />
          ))}
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-sm text-red-700">
          Erreur lors du chargement : {error}
        </div>
      )}

      {data && data.quiz.length === 0 && (
        <div className="bg-white rounded-xl border border-blue-100 shadow-sm p-8 text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-blue-50 text-3xl mb-4">
            🧠
          </div>
          <h2 className="text-lg font-semibold text-[#1B3A6B] mb-2">
            Aucun quiz disponible pour l&apos;instant
          </h2>
          <p className="text-gray-500 text-sm max-w-md mx-auto">
            Les quiz seront affichés ici dès qu&apos;ils seront générés dans{" "}
            <code className="bg-gray-100 px-1 rounded text-xs">Livrables/Quiz/</code>.
          </p>
        </div>
      )}

      {data && data.quiz.length > 0 && (
        <div className="space-y-3">
          {data.quiz.map((item) => (
            <div
              key={item.id}
              className="bg-white rounded-xl border border-blue-100 shadow-sm p-4 flex items-center gap-4 hover:border-blue-300 transition-colors"
            >
              <div className="inline-flex items-center justify-center w-10 h-10 rounded-full bg-blue-50 text-xl flex-shrink-0">
                🧠
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-medium text-[#1B3A6B] truncate text-sm">{item.name}</p>
                <p className="text-xs text-gray-400 mt-0.5">
                  {formatDate(item.date)} &middot; {formatSize(item.size)}
                </p>
              </div>
              <span className="text-xs bg-blue-50 text-blue-700 font-medium px-2.5 py-1 rounded-full flex-shrink-0">
                {item.extension.replace(".", "").toUpperCase()}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
