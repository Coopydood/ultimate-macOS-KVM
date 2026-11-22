// @ts-check
import { defineConfig } from "astro/config"
import fs from "node:fs"
import semver from "semver"
import { satteri } from "@astrojs/markdown-satteri"
import { defineMdastPlugin } from "satteri"
import { admonitionsToDirectives } from "@nullpinter/satteri-admonitions-to-directives"
import starlight from "@astrojs/starlight"
import tailwindcss from "@tailwindcss/vite"

const changelogSlugs = fs
  .readdirSync("../changelogs/", { withFileTypes: true })
  .filter((entry) => entry.isFile())
  .map((entry) => entry.name.split(".").slice(0, -1).join("."))
  .sort((a, b) => {
    const aVersion = a.replaceAll("-", ".")
    const bVersion = b.replaceAll("-", ".")

    return semver.compare(bVersion, aVersion)
  })
  .map((slug) => `changelogs/${slug}`)

// The leading `# Heading` is the page title (see content.config.ts), which Starlight already renders.
const removeTitleHeading = defineMdastPlugin({
  name: "remove-title-heading",
  before(root, ctx) {
    const first = root.children[0]
    if (first?.type === "heading" && first.depth === 1) ctx.removeChildAt(root, 0)
  },
})

// https://astro.build/config
export default defineConfig({
  site: "https://coopydood.github.io",
  base: "ultimate-macOS-KVM",
  redirects: { "/": "/ultimate-macOS-KVM/gettingstarted/" },
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
        { label: "Getting started", items: ["gettingstarted", "supportedhosts", "supportedguests", "kernel"] },
        { label: "Guide", items: ["mainmenu", "autopilot", "passthroughassistant", "xmlconverter", "extras", "remotedesktop", "opencore"] },
        { label: "Help", items: ["faqs", "issues", "usefullinks", "credits"] },
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
