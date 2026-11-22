import { readFileSync } from "node:fs"
import { defineCollection } from "astro:content"
import type { Loader } from "astro/loaders"
import { glob } from "astro/loaders"
import { docsSchema } from "@astrojs/starlight/schema"
import { docTitle, docsDir } from "./docs"

function withTitles(loader: Loader): Loader {
  return {
    ...loader,
    load: (context) =>
      loader.load({
        ...context,
        parseData: (props) =>
          context.parseData({
            ...props,
            data: { title: docTitle(readFileSync(new URL(props.filePath!, context.config.root), "utf8")), ...props.data },
          }),
      }),
  }
}

export const collections = {
  docs: defineCollection({
    loader: withTitles(glob({ base: docsDir, pattern: "{start,guide,help,changelogs}/*.md" })),
    schema: docsSchema(),
  }),
}
