// @ts-check
import { defineConfig } from "astro/config"
import fs from "node:fs"
import remarkGithubAlerts from "remark-github-alerts"
import semver from "semver"
import starlight from "@astrojs/starlight"
import tailwind from "@astrojs/tailwind"

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
    remarkPlugins: [remarkGithubAlerts],
  },
  integrations: [
    starlight({
      title: "ULTMOS",
      customCss: [
        "./src/styles/custom.css",
        "./src/tailwind.css",
        "remark-github-alerts/styles/github-colors-light.css",
        "remark-github-alerts/styles/github-base.css",
      ],
      social: {
        github: "https://github.com/Coopydood/ultimate-macOS-KVM",
        discord: "https://discord.gg/WzWkSsT",
      },
      components: {
        PageFrame: "./src/components/PageFrame.astro",
        TwoColumnContent: "./src/components/TwoColumnContent.astro",
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
          autogenerate: { directory: "reference" },
        },
        {
          label: "Changelogs",
          items: changelogSlugs,
          collapsed: true,
        },
      ],
    }),
    tailwind({
      applyBaseStyles: false,
    }),
  ],
})
