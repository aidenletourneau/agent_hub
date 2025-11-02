// tailwind.config.js
module.exports = {
    content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    // Make sure to include your shadcn/ui components path
    "./@/components/**/*.{js,ts,jsx,tsx}", 
    ],
    theme: {
    extend: {},
    },
    plugins: [],
};