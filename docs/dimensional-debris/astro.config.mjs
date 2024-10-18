// @ts-check
import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";

// https://astro.build/config
export default defineConfig({
  integrations: [
    starlight({
      title: "ULTMOS",
      logo: {
        src: "./src/assets/ULTMOS.png",
      },
      customCss: ["./src/styles/custom.css"],
      social: {
        github: "https://github.com/Coopydood/ultimate-macOS-KVM",
        discord: "https://discord.gg/WzWkSsT",
      },
      components: {
        Sidebar: "./src/components/Sidebar.astro",
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
          label: "Changelogs",
          autogenerate: { directory: "changelogs" },
          collapsed: true,
        },
        {
          label: "Reference",
          autogenerate: { directory: "reference" },
        },
      ],
    }),
  ],
});
