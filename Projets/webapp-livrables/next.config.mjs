import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Modules serveur externes (pour sessions futures)
  experimental: {
    serverComponentsExternalPackages: ["mammoth", "officeparser"],
  },

  // Alias pour le chemin vers les livrables
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      "@livrables": path.resolve(
        process.env.LIVRABLES_PATH ||
          "/Users/utilisateur/kDrive/Claude_Travail/Livrables"
      ),
    };
    return config;
  },
};

export default nextConfig;
