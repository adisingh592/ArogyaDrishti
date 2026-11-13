/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        themeDark: "#171e19",
        themeCharcoal: "#272727",
        themeYellow: "#ffe17c",
        themeSage: "#b7c6c2",
        themeSoft: "#f8f9fa",
        border: "hsl(var(--border, 214.3 31.8% 91.4%))",
        input: "hsl(var(--input, 214.3 31.8% 91.4%))",
        ring: "hsl(var(--ring, 168 57% 24%))",
        background: "hsl(var(--background, 0 0% 100%))",
        foreground: "hsl(var(--foreground, 222.2 84% 4.9%))",
        card: {
          DEFAULT: "hsl(var(--card, 0 0% 100%))",
          foreground: "hsl(var(--card-foreground, 222.2 84% 4.9%))",
        },
        primary: {
          DEFAULT: "hsl(var(--primary, 168 57% 24%))",
          foreground: "hsl(var(--primary-foreground, 210 40% 98%))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary, 210 40% 96.1%))",
          foreground: "hsl(var(--secondary-foreground, 222.2 47.4% 11.2%))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive, 0 84.2% 60.2%))",
          foreground: "hsl(var(--destructive-foreground, 210 40% 98%))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted, 210 40% 96.1%))",
          foreground: "hsl(var(--muted-foreground, 215.4 16.3% 46.9%))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent, 160 30% 95%))",
          foreground: "hsl(var(--accent-foreground, 168 57% 24%))",
        },
        teal: {
          primary: '#1a5e52',
          light: '#0d9488',
          bg: '#f0f4f2',
        },
        brand: {
          dark: '#1a5e52',
          mid: '#0d9488',
          bg: '#f0f4f2',
          orange: '#f97316',
          amber: '#fef3c7',
        }
      },
      fontFamily: {
        disp: ["'Anton'", "'Impact'", "'Arial Narrow'", "sans-serif"],
        body: ["'DM Sans'", "'Helvetica Neue'", "sans-serif"],
        serif: ['Georgia', 'Cambria', 'serif'],
        sans: ["'DM Sans'", 'Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
