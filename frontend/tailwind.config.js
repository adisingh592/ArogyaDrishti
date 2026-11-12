/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
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
        serif: ['Georgia', 'Cambria', 'serif'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
