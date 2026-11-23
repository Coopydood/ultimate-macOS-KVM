import { readdirSync, readFileSync } from "node:fs"

// The docs are also read on GitHub, which renders frontmatter, so page data lives in the Markdown itself:
// an `<!-- order: N -->` comment on the first line, then the `# Title` heading.
export const docsDir = "../docs"

const orderComment = /^\s*<!--\s*order:\s*(-?\d+)\s*-->/
const titleHeading = /^(?:\s*<!--[\s\S]*?-->)*\s*# +([^\r\n]+?)[ #]*\r?(?:\n|$)/

export function docTitle(source: string) {
  return source.match(titleHeading)?.[1]
}

export function sidebarSlugs(directory: string) {
  const pages = readdirSync(`${docsDir}/${directory}`)
    .filter((file) => file.endsWith(".md"))
    .map((file) => {
      const order = readFileSync(`${docsDir}/${directory}/${file}`, "utf8").match(orderComment)?.[1]
      if (order === undefined) throw new Error(`docs/${directory}/${file} needs an <!-- order: N --> comment on its first line`)
      return { file, slug: `${directory}/${file.slice(0, -3).toLowerCase()}`, order: Number(order) }
    })
    .sort((a, b) => a.order - b.order)
  pages.forEach((page, i) => {
    const next = pages[i + 1]
    if (next?.order === page.order)
      throw new Error(`docs/${directory}/${page.file} and ${next.file} have the same <!-- order: ${page.order} -->`)
  })
  return pages.map(({ slug }) => slug)
}

// Newest first; file names are versions like v0-14-1.
export function changelogSlugs() {
  return readdirSync(`${docsDir}/changelogs`)
    .map((file) => file.slice(0, -3))
    .sort((a, b) => {
      const [x, y] = [a, b].map((name) => name.slice(1).split("-").map(Number))
      return y[0] - x[0] || y[1] - x[1] || y[2] - x[2]
    })
    .map((name) => `changelogs/${name}`)
}
