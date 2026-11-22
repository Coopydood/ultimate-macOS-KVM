import { readFileSync } from "node:fs"
import { defineCollection } from "astro:content"
import type { Loader } from "astro/loaders"
import { glob } from "astro/loaders"
import { docsSchema } from "@astrojs/starlight/schema"

// The docs are also read on GitHub, which renders frontmatter, so the title is the leading `# Heading`.
const titleHeading = /^\s*# +([^\r\n]+?)[ #]*\r?(?:\n|$)/

function titleFor(id: string, file: URL) {
  const changelog = id.match(/^changelogs\/(v[\d-]+)$/)
  if (changelog) return changelog[1].replaceAll("-", ".")
  return readFileSync(file, "utf8").match(titleHeading)?.[1]
}

function withTitles(loader: Loader): Loader {
  return {
    ...loader,
    load: (context) =>
      loader.load({
        ...context,
        parseData: (props) =>
          context.parseData({
            ...props,
            data: { title: titleFor(props.id, new URL(props.filePath!, context.config.root)), ...props.data },
          }),
      }),
  }
}

export const collections = {
  docs: defineCollection({
    loader: withTitles(glob({ base: "..", pattern: "{start,guide,help,changelogs}/*.md" })),
    schema: docsSchema(),
  }),
}
