// Images pasted in GitHub's web editor are hosted by GitHub and can disappear; this keeps a copy in docs/images.
import { existsSync, mkdirSync, readdirSync, readFileSync, unlinkSync, writeFileSync } from "node:fs"
import { dirname, extname, join, relative } from "node:path"
import sharp from "sharp"

const docs = join(import.meta.dirname, "../../docs")
const images = join(docs, "images")
const githubImage = /https:\/\/github\.com\/(?:[\w.-]+\/[\w.-]+\/assets\/\d+|user-attachments\/assets)\/([0-9a-f-]{36})/g
const extensions: Record<string, string> = { "image/png": "png", "image/jpeg": "jpg", "image/gif": "gif", "image/webp": "webp" }
const defaultMaxSide = 1600

async function download(url: string, id: string, source: string) {
  const response = await fetch(url)
  const extension = extensions[response.headers.get("content-type")?.split(";")[0] ?? ""]
  if (!response.ok || !extension) throw new Error(`${response.status} ${response.headers.get("content-type")}`)
  const name = `${id.slice(0, 8)}.${extension}`
  const path = join(images, name)
  if (existsSync(path)) return name
  const data = Buffer.from(await response.arrayBuffer())
  // The page never needs more than 4× the size the <img> asks for; resizing would drop a GIF's animation.
  const tag = source.match(new RegExp(`<img\\b[^>]*${url}[^>]*>`))?.[0] ?? ""
  const pixels = [...tag.matchAll(/\b(?:width|height)\s*=\s*["']?(\d+)(?![\d%])/g)].map((m) => Number(m[1]))
  const maxSide = pixels.length ? Math.max(...pixels) * 4 : defaultMaxSide
  const image = sharp(data).resize({ width: maxSide, height: maxSide, fit: "inside", withoutEnlargement: true })
  const out = extension === "gif" ? data : await (extension === "png" ? image.png({ compressionLevel: 9 }) : image).toBuffer()
  mkdirSync(images, { recursive: true })
  writeFileSync(path, out)
  return name
}

let changed = 0
let allSources = ""
for (const file of readdirSync(docs, { recursive: true, encoding: "utf8" })) {
  if (!file.endsWith(".md")) continue
  const path = join(docs, file)
  let source = readFileSync(path, "utf8")
  for (const [url, id] of new Map([...source.matchAll(githubImage)].map((m) => [m[0], m[1]]))) {
    try {
      const name = await download(url, id, source)
      source = source.replaceAll(url, relative(dirname(path), join(images, name)))
      changed++
    } catch (error) {
      // A dead link stays remote: the site still renders it, and the build skips remote images.
      console.log(`::warning file=docs/${file}::Could not download ${url}: ${error instanceof Error ? error.message : error}`)
    }
  }
  writeFileSync(path, source)
  allSources += source
}
console.log(`${changed} image link(s) localized`)

// Git history keeps every pruned file.
const unused = existsSync(images) ? readdirSync(images).filter((name) => Object.values(extensions).includes(extname(name).slice(1)) && !allSources.includes(`images/${name}`)) : []
for (const name of unused) unlinkSync(join(images, name))
console.log(`${unused.length} unreferenced image(s) pruned${unused.length ? `: ${unused.join(", ")}` : ""}`)
