// Keys are also read by the inline script in PageFrame.astro, which applies them before first paint.
const STATE_KEY = "ultmos-window"
const MAXIMIZED_KEY = "ultmos-maximized"

const root = document.documentElement
const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)")

type WindowState = "closed" | "minimized"

function store(write: () => void) {
  try {
    write()
  } catch {}
}

function setWindowState(state: WindowState | null) {
  if (state) root.dataset.windowState = state
  else delete root.dataset.windowState
  store(() =>
    state
      ? sessionStorage.setItem(
          STATE_KEY,
          JSON.stringify({ state, path: location.pathname }),
        )
      : sessionStorage.removeItem(STATE_KEY),
  )
}

// offsetLeft/Top ignore transforms and `translate`, so this measures where the window and dock rest,
// even while the window is scaled down or the dock is slid off-screen by the maximized window.
function aimAtDock() {
  const page = document.querySelector<HTMLElement>(".page")
  const dock = document.querySelector<HTMLElement>(".dock")
  const icon = document.getElementById("dock-ultmos")
  if (!page || !dock || !icon || icon.offsetParent !== dock) return
  const x = dock.offsetLeft - dock.offsetWidth / 2 + icon.offsetLeft + icon.offsetWidth / 2
  const y = dock.offsetTop + icon.offsetTop + icon.offsetHeight / 2
  page.style.transformOrigin = `${x - page.offsetLeft}px ${y - page.offsetTop}px`
}

// The window's controls disappear with it, so focus moves to the icon that reopens it.
const focusDesktopIcon = () => document.querySelector<HTMLElement>(".desktop-icon")?.focus()

export function closeWindow() {
  setWindowState("closed")
  focusDesktopIcon()
}

export function minimizeWindow() {
  aimAtDock()
  setWindowState("minimized")
  focusDesktopIcon()
}

export function toggleMaximized() {
  const on = !root.hasAttribute("data-window-maximized")
  root.toggleAttribute("data-window-maximized", on)
  store(() =>
    on
      ? localStorage.setItem(MAXIMIZED_KEY, "1")
      : localStorage.removeItem(MAXIMIZED_KEY),
  )
}

export async function activateApp(startHref: string) {
  if (root.dataset.windowState === "minimized") {
    aimAtDock()
    return setWindowState(null)
  }
  if (root.dataset.windowState !== "closed") return

  const icon = document.querySelector("#dock-ultmos .dock-icon")
  if (icon && !reducedMotion.matches) {
    await icon.animate(
      [
        { translate: "0 0", easing: "cubic-bezier(.3,.7,.4,1)" },
        { translate: "0 -45%", easing: "cubic-bezier(.6,0,.7,.3)" },
        { translate: "0 0" },
      ],
      { duration: 600 },
    ).finished
  }

  if (new URL(startHref, location.href).pathname === location.pathname) {
    setWindowState(null)
  } else {
    store(() => {
      sessionStorage.removeItem(STATE_KEY)
      sessionStorage.setItem("ultmos-launch", "1")
    })
    location.assign(startHref)
  }
}

const syncFocus = () =>
  root.toggleAttribute("data-window-inactive", !document.hasFocus())
addEventListener("focus", syncFocus)
addEventListener("blur", syncFocus)
syncFocus()
