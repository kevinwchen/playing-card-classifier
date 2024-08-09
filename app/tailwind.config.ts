import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          // stone
          100: "#f5f5f4",
          300: "#d6d3d1",
          500: "#737373",
          700: "#44403c",
          800: "#292524",
        },
        secondary: {
          100: "#f7efdc",
          200: "#eee0b9",
          300: "#e6d097",
          400: "#ddc174",
          500: "#d5b151",
          600: "#aa8e41",
          700: "#806a31",
          800: "#554720",
          900: "#2b2310",
        },
      },
    },
  },
  plugins: [],
};
export default config;
