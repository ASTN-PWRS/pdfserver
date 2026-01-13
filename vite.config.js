import { defineConfig } from "vite";
import { viteStaticCopy } from "vite-plugin-static-copy";

export default defineConfig({
  publicDir: "dummy",
  build: {
    outDir: "app/public/shoelace",
    emptyOutDir: false,
    rollupOptions: {
      input: "./resources/main.js",
      output: {
        entryFileNames: "shoelace.js",
        assetFileNames: "shoelace[extname]",
      },
    },
  },
  plugins: [
    viteStaticCopy({
      targets: [
        {
          src: "node_modules/@shoelace-style/shoelace/dist/assets",
          dest: "",
        },
        {
          src: "node_modules/@panzoom/panzoom/dist/panzoom.min.js",
          dest: "../js",
        },
        {
          src: "node_modules/markdown-it/dist/markdown-it.min.js",
          dest: "../js",
        },
      ],
    }),
  ],
});
