import type { Config } from "tailwindcss";

export default {
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./app.vue",
  ],
  theme: {
    extend: {
      colors: {
        "water-soft": "#3B82F6",
        "water-medium": "#22C55E",
        "water-hard": "#EAB308",
        "water-very-hard": "#EF4444",
      },
    },
  },
} satisfies Config;
