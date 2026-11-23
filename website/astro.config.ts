import { defineConfig } from "astro/config"
import { satteri } from "@astrojs/markdown-satteri"
import { defineMdastPlugin } from "satteri"
import { admonitionsToDirectives } from "@nullpinter/satteri-admonitions-to-directives"
import starlight from "@astrojs/starlight"
import tailwindcss from "@tailwindcss/vite"
import { changelogSlugs, docsDir, sidebarSlugs } from "./src/docs"

// The leading `# Heading` is the page title (see src/docs.ts), which Starlight already renders.
const removeTitleHeading = defineMdastPlugin({
  name: "remove-title-heading",
  before(root, ctx) {
    const index = root.children.findIndex((node) => node.type !== "html")
    const first = root.children[index]
    if (first?.type === "heading" && first.depth === 1) ctx.removeChildAt(root, index)
  },
})

// https://astro.build/config
export default defineConfig({
  site: "https://coopydood.github.io",
  base: "ultimate-macOS-KVM",
  redirects: { "/": "/ultimate-macOS-KVM/start/gettingstarted/" },
  devToolbar: { enabled: true, placement: "bottom-left" },
  markdown: {
    processor: satteri({
      mdastPlugins: [
        removeTitleHeading,
        // Targets must be Starlight aside variants; any other name renders as a plain <div>.
        admonitionsToDirectives({
          mapping: {
            NOTE: "note",
            TIP: "tip",
            IMPORTANT: "note",
            WARNING: "caution",
            CAUTION: "danger",
          },
        }),
      ],
    }),
  },
  integrations: [
    starlight({
      title: "ULTMOS",
      markdown: { processedDirs: [docsDir] },
      customCss: ["./src/tailwind.css", "./src/styles/custom.css"],
      social: [
        { icon: "github", label: "GitHub", href: "https://github.com/Coopydood/ultimate-macOS-KVM" },
        { icon: "discord", label: "Discord", href: "https://discord.gg/WzWkSsT" },
      ],
      components: {
        PageFrame: "./src/components/PageFrame.astro",
        SiteTitle: "./src/components/SiteTitle.astro",
      },
      sidebar: [
        { label: "Getting started", items: sidebarSlugs("start") },
        { label: "Guide", items: sidebarSlugs("guide") },
        { label: "Help", items: sidebarSlugs("help") },
        { label: "Changelogs", items: changelogSlugs(), collapsed: true },
      ],
    }),
  ],
  vite: {
    plugins: [tailwindcss()],
  },
})
