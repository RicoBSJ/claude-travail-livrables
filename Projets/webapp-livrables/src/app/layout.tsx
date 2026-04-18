import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "Portail Livrables — Claude_Travail",
  description:
    "Portail de consultation des livrables du projet Claude_Travail : quiz, infographies, leçons, veilles et projets.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr" className={`${inter.variable} h-full antialiased`}>
      <body className="min-h-full flex flex-row bg-gray-50 text-gray-900">
        {/* Sidebar fixe à gauche */}
        <Sidebar />

        {/* Zone principale : header + contenu */}
        <div className="flex flex-col flex-1 min-h-screen overflow-hidden">
          <Header />
          <main className="flex-1 overflow-y-auto">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
