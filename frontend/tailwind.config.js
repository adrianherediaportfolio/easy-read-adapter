/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#19342f',
        moss: '#527b68',
        cream: '#f6f4ed',
        coral: '#dc755c',
      },
      fontFamily: {
        sans: ['Atkinson Hyperlegible', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
