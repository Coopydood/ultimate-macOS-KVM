import sharp from "sharp"

const cache = new Map<string, Promise<string>>()

// The path is relative to the project root, which is Astro's working directory.
function inlineWallpaper(file: string, width: number, blur?: number) {
  const key = `${file} ${width} ${blur}`
  let url = cache.get(key)
  if (!url) {
    let image = sharp(`src/assets/${file}`).resize(width)
    if (blur) image = image.blur(blur)
    url = image
      .jpeg({ quality: 85 })
      .toBuffer()
      .then((data) => `url("data:image/jpeg;base64,${data.toString("base64")}")`)
    cache.set(key, url)
  }
  return url
}

// Stands in for a backdrop blur, which drops frames while the window animates.
export const blurredWallpaper = (file: string) => inlineWallpaper(file, 192, 20)

export const wallpaperPlaceholder = (file: string) => inlineWallpaper(file, 64)
