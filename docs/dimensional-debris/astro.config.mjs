// @ts-check
import { defineConfig } from "astro/config"
import fs from "node:fs"
import semver from "semver"
import { satteri } from "@astrojs/markdown-satteri"
import { admonitionsToDirectives } from "@nullpinter/satteri-admonitions-to-directives"
import starlight from "@astrojs/starlight"
import tailwindcss from "@tailwindcss/vite"

const changelogSlugs = fs
  .readdirSync("./src/content/docs/changelogs/", { withFileTypes: true })
  .filter((entry) => entry.isFile())
  .map((entry) => entry.name.split(".").slice(0, -1).join("."))
  .sort((a, b) => {
    const aVersion = a.replaceAll("-", ".")
    const bVersion = b.replaceAll("-", ".")

    return semver.compare(bVersion, aVersion)
  })
  .map((slug) => `changelogs/${slug}`)

// https://astro.build/config
export default defineConfig({
  site: "https://coopydood.github.io",
  base: "ultimate-macOS-KVM",
  markdown: {
    processor: satteri({
      mdastPlugins: [
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
        {
          label: "Guides",
          items: [
            // Each item here is one entry in the navigation menu.
            { label: "Example Guide", slug: "guides/example" },
          ],
        },
        {
          label: "Reference",
          items: [{ autogenerate: { directory: "reference" } }],
        },
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
