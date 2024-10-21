// @ts-check
import { defineConfig } from "astro/config"
import remarkGithubAlerts from "remark-github-alerts"
import starlight from "@astrojs/starlight"
import tailwind from "@astrojs/tailwind"

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
      logo: {
        src: "./src/assets/ULTMOS.png",
      },
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
        Sidebar: "./src/components/Sidebar.astro",
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
          autogenerate: { directory: "changelogs" },
          collapsed: true,
        },
      ],
    }),
    tailwind({
      applyBaseStyles: false,
    }),
  ],
})
