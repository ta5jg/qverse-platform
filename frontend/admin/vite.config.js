import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  root: ".",
  base: "/admin/forge/",
  build: {
    outDir: "dist",
    emptyOutDir: true,
  },
});
