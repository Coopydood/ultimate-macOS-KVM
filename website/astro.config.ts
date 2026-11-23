import { defineConfig } from "astro/config"
import { satteri } from "@astrojs/markdown-satteri"
import { defineHastPlugin, defineMdastPlugin, type HastNode } from "satteri"
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

// Astro only optimizes Markdown `![]()` images; the docs use HTML <img> for GitHub's sizing attributes.
// Satteri keeps HTML as raw text, so each local <img> is cut out of it as an element for Astro's image pass.
const optimizeHtmlImages = defineHastPlugin({
  name: "optimize-html-images",
  raw(node, ctx) {
    const parts = node.value.split(/(<img\b(?:[^>"']|"[^"]*"|'[^']*')*>)/i)
    if (parts.length === 1) return
    let changed = false
    const nodes: HastNode[] = parts.map((part, i) => {
      const attrs = Object.fromEntries(
        [...part.matchAll(/([\w-]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'>]+?)(?=\s|\/?>|$)))?/g)]
          .slice(1)
          .map(([, k, ...v]) => [k.toLowerCase(), v.find((x) => x != null) ?? ""]),
      )
      const src = attrs.src
      let path: string | undefined
      try {
        path = decodeURI(src)
      } catch {}
      if (i % 2 === 0 || !path || URL.canParse(src) || src.startsWith("/")) return { type: "raw", value: part }
      changed = true
      ctx.data.astro?.localImagePaths.add(path)
      const { width, height, ...rest } = attrs
      const px = (v?: string) => v == null || /^\d+$/.test(v)
      if (px(width) && px(height))
        return { type: "element", tagName: "img", properties: { ...rest, ...(width && { width: +width }), ...(height && { height: +height }), densities: [1, 2] }, children: [] }
      // getImage takes pixel sizes and writes the file's own size into width/height, so the sizes move to CSS with auto for an unset side
      const style = Object.entries({ width, height })
        .map(([k, v]) => `${k}: ${v == null ? "auto" : px(v) ? `${v}px` : v}`)
        .join("; ")
      return { type: "element", tagName: "img", properties: { ...rest, style }, children: [] }
    })
    if (changed) ctx.replaceNode(node, nodes)
  },
})

// https://astro.build/config
export default defineConfig({
  site: "https://coopydood.github.io",
  base: "ultimate-macOS-KVM",
  devToolbar: { enabled: true, placement: "bottom-left" },
  markdown: {
    processor: satteri({
      hastPlugins: [optimizeHtmlImages],
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
        { label: "Home", link: "/" },
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
