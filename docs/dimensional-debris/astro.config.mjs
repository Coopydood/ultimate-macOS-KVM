// @ts-check
import { defineConfig } from "astro/config"
import fs from "node:fs"
import { satteri } from "@astrojs/markdown-satteri"
import { defineMdastPlugin } from "satteri"
import { admonitionsToDirectives } from "@nullpinter/satteri-admonitions-to-directives"
import starlight from "@astrojs/starlight"
import tailwindcss from "@tailwindcss/vite"

// Sidebar position of a doc page: an `<!-- order: N -->` comment on its first line, hidden on GitHub.
/** @param {string} directory */
function sidebarSlugs(directory) {
  return fs
    .readdirSync(`../${directory}`)
    .filter((file) => file.endsWith(".md"))
    .map((file) => {
      const order = fs.readFileSync(`../${directory}/${file}`, "utf8").match(/^\s*<!--\s*order:\s*(-?\d+)\s*-->/)?.[1]
      if (order === undefined) throw new Error(`docs/${directory}/${file} needs an <!-- order: N --> comment on its first line`)
      return { slug: `${directory}/${file.slice(0, -3).toLowerCase()}`, order: Number(order) }
    })
    .sort((a, b) => a.order - b.order)
    .map(({ slug }) => slug)
}

// Newest first; file names are versions like v0-14-1.
const changelogSlugs = fs
  .readdirSync("../changelogs")
  .map((file) => file.slice(0, -3))
  .sort((a, b) => {
    const [x, y] = [a, b].map((name) => name.slice(1).split("-").map(Number))
    return y[0] - x[0] || y[1] - x[1] || y[2] - x[2]
  })
  .map((name) => `changelogs/${name}`)

// The leading `# Heading` is the page title (see content.config.ts), which Starlight already renders.
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
      markdown: { processedDirs: [".."] },
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
        {
          label: "Changelogs",
          items: changelogSlugs,
          collapsed: true,
        },
      ],
    }),
  ],
  vite: {
    plugins: [tailwindcss()],
  },
})
