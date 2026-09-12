/** @type {import('tailwindcss').Config} */
 // Design System: Food Tracker — Wellness Calm (Variant A, Lora + Raleway)
 // Source: design-system/food-tracker/MASTER.md + DESIGN_GUIDELINES.md
 // Stack: React + Tailwind, mobile-first 375px
module.exports = {
  content: ["./src/**/*.{js,ts,jsx,tsx}", "./index.html"],
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: "#7C3AED", foreground: "#FFFFFF" },
        secondary: { DEFAULT: "#8B5CF6", foreground: "#000000" },
        accent: { DEFAULT: "#059669", foreground: "#000000" },
        background: "#FAF5FF",
        foreground: "#0F172A",
        card: { DEFAULT: "#FFFFFF", foreground: "#0F172A" },
        muted: { DEFAULT: "#F7F3FD", foreground: "#475569" },
        border: "#EFE7FC",
        destructive: { DEFAULT: "#DC2626", foreground: "#FFFFFF" },
        ring: "#7C3AED",
      },
      fontFamily: {
        serif: ["Lora", "serif"],
        sans: ["Raleway", "sans-serif"],
        heading: ["Lora", "serif"],
        body: ["Raleway", "sans-serif"],
      },
      spacing: {
        xs: "4px",
        sm: "8px",
        md: "16px",
        lg: "24px",
        xl: "32px",
        "2xl": "48px",
        "3xl": "64px",
      },
      borderRadius: {
        sm: "8px",
        md: "12px",
        lg: "16px",
      },
      boxShadow: {
        sm: "0 1px 2px rgba(0,0,0,0.05)",
        md: "0 4px 6px rgba(0,0,0,0.1)",
        lg: "0 10px 15px rgba(0,0,0,0.1)",
        xl: "0 20px 25px rgba(0,0,0,0.15)",
      },
      minHeight: {
        tap: "44px",
      },
      minWidth: {
        tap: "44px",
      },
    },
  },
  plugins: [],
};
