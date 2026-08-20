import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#F4FCFF',
          100: '#EAF7FD',
          400: '#20C4F4',
          500: '#00B8F0',
          700: '#0878C9',
          800: '#073B82',
          900: '#063B73',
        },
        bg: {
          page: '#F7FAFC',
          surface: '#FFFFFF',
        },
        border: '#E3EAF0',
        text: {
          primary: '#102A43',
          secondary: '#52606D',
          muted: '#7B8794',
        },
        status: {
          success: '#16A34A',
          warning: '#F59E0B',
          danger: '#DC3545',
          info: '#0878C9',
        },
      },
      fontFamily: {
        sans: ['Open Sans', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        base: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
        md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
      },
      transitionDuration: {
        150: '150ms',
        200: '200ms',
        300: '300ms',
      },
    },
  },
  plugins: [],
}

export default config
