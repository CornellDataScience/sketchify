/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    /*colors: {
      'blue': '#1fb6ff',
      'beige': '#f5f5dc',
      'gray': '#8492a6',
    },
    backgroundColor: {
      'blue': '#1fb6ff',
      'beige': '#f5f5dc',
      'gray': '#8492a6',
    },
    */
    extend: {},
  },
  plugins: [require("flowbite/plugin")],
};
