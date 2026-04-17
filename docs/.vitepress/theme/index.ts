import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import { nextTick } from 'vue'
import './custom.css'

const STORAGE_KEY = 'preferred-code-lang'

function getPreferredLang(): string | null {
  try {
    return localStorage.getItem(STORAGE_KEY)
  } catch {
    return null
  }
}

function setPreferredLang(lang: string): void {
  try {
    localStorage.setItem(STORAGE_KEY, lang)
  } catch {
    /* ignore */
  }
}

function labelText(label: HTMLLabelElement): string {
  return (label.textContent ?? '').trim()
}

function applyLangToGroup(group: HTMLElement, lang: string): boolean {
  const inputs = Array.from(
    group.querySelectorAll<HTMLInputElement>('.tabs input')
  )
  const labels = Array.from(
    group.querySelectorAll<HTMLLabelElement>('.tabs label')
  )
  const idx = labels.findIndex((l) => labelText(l) === lang)
  if (idx < 0) return false
  const target = inputs[idx]
  if (!target) return false
  if (!target.checked) target.checked = true
  const blocks = group.querySelector<HTMLElement>(':scope > .blocks')
  if (blocks) {
    const children = Array.from(blocks.children)
    children.forEach((child) => child.classList.remove('active'))
    children[idx]?.classList.add('active')
  }
  return true
}

function applyLangEverywhere(lang: string, skip?: HTMLElement | null): void {
  document
    .querySelectorAll<HTMLElement>('.vp-code-group')
    .forEach((group) => {
      if (group === skip) return
      applyLangToGroup(group, lang)
    })
}

function applyStoredLang(): void {
  const lang = getPreferredLang()
  if (lang) applyLangEverywhere(lang)
}

const theme: Theme = {
  extends: DefaultTheme,
  enhanceApp({ router }) {
    if (typeof window === 'undefined') return

    document.addEventListener(
      'click',
      (event) => {
        const target = event.target
        if (!(target instanceof HTMLInputElement)) return
        if (!target.matches('.vp-code-group .tabs input')) return
        const group = target.closest<HTMLElement>('.vp-code-group')
        if (!group) return
        const label = group.querySelector<HTMLLabelElement>(
          `label[for="${CSS.escape(target.id)}"]`
        )
        const lang = label ? labelText(label) : ''
        if (!lang) return
        setPreferredLang(lang)
        applyLangEverywhere(lang, group)
      },
      true
    )

    const schedule = () => {
      nextTick(() => {
        requestAnimationFrame(applyStoredLang)
      })
    }

    if (document.readyState === 'loading') {
      window.addEventListener('DOMContentLoaded', schedule, { once: true })
    } else {
      schedule()
    }

    const prev = router.onAfterRouteChanged
    router.onAfterRouteChanged = (to) => {
      prev?.(to)
      schedule()
    }
  }
}

export default theme
