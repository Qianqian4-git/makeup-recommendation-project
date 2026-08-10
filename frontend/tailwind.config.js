/** @type {import('tailwindcss').Config} */
export default {
    content: [
      "./index.html",
      "./src/**/*.{vue,js,ts,jsx,tsx}",
    ],
    theme: {
      extend: {
        fontFamily: {
          sans: ['-apple-system', 'BlinkMacSystemFont', '"SF Pro Display"', '"Helvetica Neue"', 'Arial', 'sans-serif'],
        },
        colors: {
          apple: {
            blue: '#007AFF',        // 系统蓝（主色）
            blueLight: '#E5F2FF',   // 浅蓝背景
            gray: '#8E8E93',
            lightGray: '#F5F5F7',
            border: '#E5E5EA',
            darkText: '#1C1C1E',
            secondaryText: '#6C6C70',
          }
        },
        boxShadow: {
          'apple': '0 4px 20px rgba(0, 0, 0, 0.04), 0 1px 3px rgba(0, 0, 0, 0.02)',
          'apple-lg': '0 20px 60px rgba(0, 0, 0, 0.06), 0 2px 10px rgba(0, 0, 0, 0.02)',
        },
        backdropBlur: {
          'xl': '20px',
        }
      },
    },
    plugins: [],
  }