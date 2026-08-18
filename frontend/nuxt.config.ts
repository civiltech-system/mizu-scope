export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ["@nuxtjs/tailwindcss", "@pinia/nuxt"],
  css: ["maplibre-gl/dist/maplibre-gl.css"],
  vite: {
    optimizeDeps: {
      include: ["maplibre-gl"],
    },
    ssr: {
      noExternal: ["maplibre-gl"],
    },
  },
  runtimeConfig: {
    apiBase: process.env.NUXT_API_BASE || "http://backend:8000",
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || "http://localhost:8000",
    },
  },
  app: {
    head: {
      charset: "utf-8",
      viewport: "width=device-width, initial-scale=1",
      titleTemplate: "%s | MizuMap",
      meta: [
        { name: "theme-color", content: "#1d4ed8" },
        { name: "apple-mobile-web-app-capable", content: "yes" },
        { name: "apple-mobile-web-app-status-bar-style", content: "default" },
        { name: "apple-mobile-web-app-title", content: "MizuScope" },
      ],
      link: [
        { rel: "icon", type: "image/png", sizes: "32x32", href: "/favicon-32x32.png" },
        { rel: "apple-touch-icon", sizes: "180x180", href: "/apple-touch-icon.png" },
        { rel: "manifest", href: "/site.webmanifest" },
      ],
    },
  },
});
