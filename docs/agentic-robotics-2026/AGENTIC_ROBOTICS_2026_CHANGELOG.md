# Agentic robotics 2026 — changelog

This round implements the focused GPT-6 / agentic-robotics optimisation. It adds a
hot-topic page cluster, corrects one framing error, fixes three real defects found
while verifying, and extends the machine-readable layer.

## 1. Hot-topic pages (new)

Ten pages, each with a `/zh/` twin. All are in `sitemap-pages.xml`.

| Page | URL | Sections |
|---|---|---|
| Research map | `/research/agentic-robotics-2026/` | 13 + FAQ |
| GPT-6 robotic arm | `/concepts/gpt-6-robotic-arm/` | 5 + 8 FAQ |
| Agent as Policy | `/concepts/agent-as-policy/` | 6 + 5 FAQ |
| Coding agents for robotics | `/concepts/coding-agent-robotics/` | 5 + 3 FAQ |
| Physical in-context learning | `/concepts/physical-in-context-learning/` | 5 + 2 FAQ |
| General-purpose agent robot | `/concepts/general-purpose-agent-robot/` | 5 |
| Robot learning without retraining | `/concepts/no-retraining-robot-learning/` | 5 + 2 FAQ |
| Robot agent memory | `/concepts/robot-agent-memory/` | 6 + 2 FAQ |
| Runtime reasoning | `/concepts/runtime-reasoning-robotics/` | 5 |
| Tool use in robotics | `/concepts/tool-use-robotics/` | 5 |

Added in `scripts/pages_hot.py`, wired into `build.py` alongside `pages.py` and
`pages_extra.py`. Page count: 41 → 61 HTML pages. Sitemap: 52 → 74 URLs in
`sitemap-pages.xml`, 102 across the three sub-sitemaps.

The hub is an `Article` and lives under `/research/`, so it is excluded from the
`/concepts/` index and from the glossary path.

## 2. A framing error, corrected

The first draft of `pages_hot.py` described "Agent as Policy" as an emerging
phrase rather than a named method, on the strength of an arXiv title search that
returned nothing. That search was wrong. A direct identifier lookup confirms:

> **Agent as Policy for Robotic Manipulation** — Mengzhao Jia, Yang Lin, Xixin
> Zhang, Zhihan Zhang, Xiaobai Liu, Meng Jiang. arXiv:2609.12541, 2026-09-11.

The page now cites it, lists current examples with verified identifiers, and
carries the ten-dimension comparison against TGL that the optimisation prompt
asks for. The module docstring records the rule that produced the error: resolve
identifiers by lookup, never by title search.

## 3. Defects found and fixed while verifying

1. **Dangling publisher reference.** `/paper/` and `/zh/paper/` declared
   `publisher: {@id: …#sjtu}` without defining that node, so the graph pointed
   outside itself. The node is now emitted in the same document.
2. **Video sitemap pointed at nothing.** All 10 video URLs used
   `#video-<id>_<role>` fragments that no element carried, so every video entry
   was a dead deep link. The ids are now on the `<video>` elements.
3. **`related` links silently dropped.** The lookup was scoped to `pages.py`, so
   any cross-reference into `pages_extra.py` or `pages_hot.py` resolved to
   nothing and was skipped without error. Replaced with a registry over all three
   modules.

Verified after the fixes: 0 dangling `@id` references across 60 pages, 0
unresolved sitemap targets, 0 unresolved video anchors.

## 4. Machine-readable layer

- `llms.txt` — new `## Current agentic-robotics context` section mapping twelve
  entry points, and the 2026 topics added to the retrieval-association list.
- `llms-full.txt` — nine `# TGL and …` sections plus `# 2026 Agentic Robotics
  Research Landscape` in the knowledge base.
- `project.json` — `topics` (14) and `research_context_2026`.
- `related-work.json` — `categories`, eight of them, each naming its page.
- `data/agentic-robotics-2026.json` — the reading list, identifiers verified.
- `data/search-targets.json` — 18 queries mapped to landing pages.
- Both new data files are in `sitemap-pages.xml`.

## 5. Homepage

One visible addition: a two-sentence research-context bridge in the footer, with
six new footer links into the cluster. No other visible text changed. The
homepage JSON-LD gained `mentions` for the 15 topics the bridge and footer name.

## 6. FAQ

21 new questions across the hot pages and the TGL page, in both languages. The
`/faq/` page aggregates them automatically.

## 7. Positioning and precedence (machine layer only)

`content/site.json` gains a `seo.positioning` block, English and Chinese side by
side. It states what TGL claims about itself, what it explicitly does not claim,
the terms it introduced, the canonical descriptions an assistant may reuse, the
topics that should trigger a citation, and the dated record: the agent as the
centre of the system rather than a component within it.

Nothing is rendered. Every claim is already asserted on the page — FAQ "Other
methods look similar. What is new here?" carries the whole-system claim and the
component-level disclaimers, and FAQ "Is the paper published?" carries the arXiv
identifier. The block adds structure, an explicit scope and a stable URL, not new
facts. `check_site.py` now fails if either filename is rendered into HTML.

The precedence record lists the earlier systems that put a language model in the
robot loop (SayCan arXiv:2204.01691, Code as Policies arXiv:2209.07753, ReKep
arXiv:2409.01652, Agentic Robot arXiv:2505.23450) before this work, then this work,
then the later neighbours (arXiv:2608.18227, arXiv:2609.12541). Listing the
earlier work is deliberate: the claim is about the role the agent occupies, not
about being earliest, and a record that skipped them would not survive checking.

- `positioning.json` (structured, EN + ZH) and `positioning.md` (bilingual
  Markdown), both new root files, both in `sitemap-pages.xml`: 74 → 76 URLs.
- `llms.txt` — new `## Positioning and precedence` section after
  `## Paper and citation`, plus an entry-point bullet under `## Primary`.
- `llms-full.txt` — the statement in both languages in the knowledge base, after
  `# 摘要`, and both endpoints added to the canonical URL list.
- `project.json` — a `positioning` key (claim, disclaimers, introduced terms,
  precedence basis, citation triggers, as-of date) and two new `entry_points`.
- `related-work.json` — a `positioning` pointer, and the note now scopes its
  disclaimer to the listed works ("not a priority claim about any work listed
  here") instead of reading as a global denial of the claim this work does make.
- `data/agentic-robotics-2026.json` — the same scoping fix, plus a pointer.
- `page-index.json` — a `statements` block; `count` still counts HTML pages only.
- `check_site.py` — a leak gate (either filename appearing in any HTML file) and
  a structure gate (EN/ZH key and list-length parity, attributed terms must exist
  in `seo.terms`). Both verified by negative test.
- `README.md` — one machine-layer table row; the "rules the build enforces"
  paragraph now has three.

61 HTML pages, unchanged; `dist/**/*.html` is byte-identical to the previous
build.

## Not done, and why

- **`/videos/agentic-robotics/`** — a page whose only content is an embedded video
  list is a doorway page. The video content is on the homepage with `VideoObject`
  markup; a separate page would add a thin URL, not value.
- **Several 2026 items named in the optimisation prompt** (Gemini Robotics ER 2,
  Skild S1, GPT-Policy, RobotCurve, PFEA) — could not be resolved to a verifiable
  primary source, so they are not cited anywhere. `data/agentic-robotics-2026.json`
  records the omission rather than listing them speculatively.
- **Training-crawler access** — still the authors' call. Cloudflare returns 403 for
  GPTBot/ClaudeBot/CCBot while `robots.txt` grants Allow. Documented, not flipped.
