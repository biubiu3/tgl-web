# Teach and Grow — project website

Bilingual project page for **Teach and Grow: An Agent-Centered Architecture for General Robot Learning**, by Chang Nie, Zhe Liu, and Hesheng Wang (Shanghai Jiao Tong University).

Production URL: **https://tgl.changnie.top/**<br>
Chinese: **https://tgl.changnie.top/zh/**

GitHub review URL: https://biubiu3.github.io/tgl-web/ (redirects after the custom domain is bound).

This repository contains the website, paper PDF, figure exports, and ten author-supplied videos. The robot implementation is maintained separately at https://github.com/IRMVLab/TGL. A problem-led research narrative, method explanations, and paired demonstrations are inspired by https://hear.irmv.top/; the implementation, typography, color palette, and interactions are original. The research edition uses a restrained dark-blue technical masthead with light reading sections. It traces the problem, early agent experiments, sparse teaching, Skill Blocks, physical feedback, retained experience, and the longer-term research direction. Numerical scoreboards are intentionally left in the paper.

## Local preview

Requires Python 3.10+; no npm dependencies or external services.

```bash
python3 scripts/build.py
python3 scripts/check_site.py
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000/ (Chinese: `/zh/`). Local preview omits GitHub's repository prefix. No runtime third-party fonts, scripts, analytics, or embeds are loaded.

## GitHub Pages setup

1. Open https://github.com/biubiu3/tgl-web/settings/pages.
2. Under **Build and deployment**, set **Source** to **GitHub Actions**.
3. Open **Actions → Build and deploy TGL website** and rerun the latest workflow, or use **Run workflow** on `main`.
4. Wait for both `build` and `deploy` to succeed. Visit the configured site URL above.

Every subsequent push to `main` rebuilds, checks links and benchmark arithmetic, and deploys the static artifact. GitHub Pages ties the first path component to the repository name. An exact `biubiu3.github.io/tgl/` URL requires a repository named `tgl` or a route in the owner's `biubiu3.github.io` site.

## Production domain: tgl.changnie.top

`deployment.json` is configured for the production domain. Account-side setup is still required:

1. Open https://github.com/biubiu3/tgl-web/settings/pages. Keep Source as **GitHub Actions**. Set **Custom domain** to `tgl.changnie.top` and save.
2. In Cloudflare, select `changnie.top` → **DNS → Records**. Add **CNAME**, name **tgl**, target **biubiu3.github.io**, proxy **DNS only** (gray cloud), TTL **Auto**. Do not include `https://` or a repository path in the target. Leave the apex and other subdomains unchanged.
3. Wait for GitHub's DNS check and TLS certificate, then enable **Enforce HTTPS**. This option can take up to 24 hours to become available.
4. Verify `/`, `/zh/`, the paper PDF, images, and video playback on the production domain. Update external project links after HTTPS is live.

The build updates canonical, hreflang, social, PDF, BibTeX, sitemap, and robots URLs. It also emits `CNAME` for portability, but **GitHub Actions deployments ignore that file for domain binding**: the Pages setting in step 1 is required.

References: [GitHub custom domains](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site), [Cloudflare proxy status](https://developers.cloudflare.com/dns/proxy-status/).

## Editing

- `content/site.json`: authors, exact benchmark values, paired-video descriptions in English and Chinese, and the `seo` block (paper date, abstract, keywords, glossary terms, FAQ). Every number and identifier used for metadata comes from here — do not hard-code a figure elsewhere.
- `scripts/build.py`: bilingual page shell, videos, figures, and BibTeX.
- `scripts/seo.py`: `<head>` metadata, the JSON-LD `@graph`, and every machine-readable file (robots.txt, sitemaps, llms.txt, llms-full.txt, Markdown mirrors, project.json, feed.xml).
- `scripts/research.py`: the bilingual research narrative, abstract block, glossary, FAQ and worked example. The FAQ and the cost deep-dive render expanded (no accordions), so every text block is readable without interaction; only the four-stage worked example keeps its tab switch, and all four stages remain visible without JavaScript.
- `assets/style.css`: responsive layout and styling.
- `assets/app.js`: paired playback, filters, concept walkthrough, citation copy, figure lightbox.
- `assets/videos/`: original MP4s, preserved byte for byte.
- `assets/posters/`: actual video frames; 256 × 256 source videos are not artificially upscaled.
- `assets/figures/`: optimized WebP exports of the author's figures. Figure 1 is a conceptual illustration, not a physical-robot result.
- `assets/paper/teach-and-grow.pdf`: freshly built current 17-page manuscript.
- `content/provenance.json`: paper/figure source hashes and the video-label correction.

The supplied description calls Goal task 07 a bottle-cap task. The local LIBERO task map identifies it as `turn_on_the_stove`, consistent with inspection of both videos; the website uses that name. Paired video playback shares a start time but does not time-align actions or imply a speed comparison. The page presents five qualitative simulation examples, the controlled-study counts reported in the paper's appendix (stage accuracy, effect confirmations, the 3/3 and 0/6-to-4/6 studies), bounded observations, and clearly identified scaling hypotheses. The full benchmark tables stay in the paper. It does not assert publication acceptance, complete paper reproduction from the public code snapshot, empirical readiness, or an independently replicated benchmark.

Images open in an accessible native dialog (Escape to close). Videos retain native controls, and content remains readable when JavaScript is disabled. All stages of the worked example remain visible without JavaScript. Reduced-motion preferences are respected.

## Publication identity

The paper is on arXiv as **2608.17209** (DOI `10.48550/arXiv.2608.17209`), first posted **17 August 2026**. These
live in `content/site.json` under `seo` and are written into the citation tags, JSON-LD `identifier`/`sameAs`,
`cite.bib`, `CITATION.cff`, `codemeta.json`, `project.json` and `/paper/` automatically. `arxiv_id` and `doi`
were verified against the arXiv record on 2026-09-16; re-verify before changing them.

Two dates are tracked separately and must not be conflated:

- `paper_date` (`2026/08/17`) — the publication date. Feeds `citation_publication_date` and JSON-LD
  `datePublished`. **Must stay `YYYY/MM/DD`** or Google Scholar mis-parses it.
- `updated_iso` (`2026-09-16`) — last content change. Feeds sitemap `lastmod` and JSON-LD `dateModified`.

The site's own abstract comes from the current manuscript PDF, which is newer than the arXiv posting; the two
abstracts are worded differently. The site keeps its own and links out to arXiv rather than overwriting either.

## Generated sub-pages

Beyond the two main pages, the build emits **16 supplementary pages** from `scripts/pages.py` — English and
Chinese for each, cross-linked by `hreflang` and by hand-written `related` lists:

| Path | Purpose |
| --- | --- |
| `/paper/` | Publication record: abstract, authors, keywords, BibTeX, links. Carries the Google Scholar metadata. |
| `/research-context/` | How TGL sits among VLA models, world-action models, robot foundation models and agentic robotics. |
| `/concepts/teach-and-grow-learning/` | The paradigm itself. |
| `/concepts/training-free-robot-learning/` | The category, and what the term does and does not mean. |
| `/concepts/skill-block/` | The unit of reusable behaviour and its contract. |
| `/concepts/skill-library/` | The persistent validated-behaviour store. |
| `/concepts/experience-memory/` | The contextual store of outcomes, diagnoses and repairs. |
| `/concepts/retraining-tax/` | The named cost problem the paper frames. |
| `/concepts/agentic-robotics/` | What it means for a robot to be agent-centered. |
| `/concepts/general-robot-learning/` | Two routes to generality and what each costs. |
| `/concepts/lifelong-robot-learning/` | The forgetting problem, and a mechanism that avoids it. |
| `/concepts/vla-without-retraining/` | Adapting a VLA model with frozen weights. |
| `/concepts/physical-ai/` | Physical AI and embodied AI, for manipulation. |
| `/concepts/llm-robotics/` | What a large language model adds to a robot stack. |
| `/concepts/gpt-robotic-arm/` | GPT-class models and robot arms. |
| `/concepts/ai-agent-robotic-arm/` | The agent loop paired with a physical arm. |
| `/research/agentic-robotics-2026/` | Research map of the 2026 agentic-robotics landscape. |
| `/concepts/gpt-6-robotic-arm/` | GPT-6-class models driving a robot arm. |
| `/concepts/agent-as-policy/` | Agent as Policy (AGP), with current examples and a comparison against TGL. |
| `/concepts/coding-agent-robotics/` | Models that write and run robot programs. |
| `/concepts/physical-in-context-learning/` | Adapting a robot from context without updating weights. |
| `/concepts/general-purpose-agent-robot/` | One agent across many tasks, and what it does not retain. |
| `/concepts/no-retraining-robot-learning/` | Acquiring tasks with frozen weights. |
| `/concepts/robot-agent-memory/` | What a robot should keep from an interaction. |
| `/concepts/runtime-reasoning-robotics/` | Deciding while the task is running. |
| `/concepts/tool-use-robotics/` | Perception, grasping and motion as callable tools. |
| `/concepts/` | Hub listing every concept page. |
| `/glossary/` | Every term defined, aggregated from site.json. |
| `/faq/` | Every question and answer, aggregated from site.json and the concept pages. |

That is 29 pages per language, 61 HTML pages in total. Pages declare their own `parent` folder;
`_page_dirs()` in `seo.py` reads it rather than inferring a path from the slug. The 2026 pages live in
`scripts/pages_hot.py`, which is wired into `build.py` the same way as `pages.py` and `pages_extra.py`;
its module docstring records the sourcing rule — identifiers are resolved against the arXiv API, never
inferred from a title search.

Each page is written to stand alone — a definition, the mechanism, its relation to TGL, an FAQ where useful —
so it can be quoted by a reader or an AI assistant without the surrounding page. `{home}`, `{cite}`,
`{abstract}`, `{keywords}` and `{bibtex_key}` are placeholders resolved from `content/site.json` at build time,
so no page hard-codes a path or a fact. The Chinese concept pages live under `/zh/concepts/`.

## Search and AI discovery

The build emits a machine-readable layer so that search engines, answer engines and AI agents can read the
project without scraping HTML. All of it is generated from `content/site.json`:

| File | Purpose |
| --- | --- |
| `robots.txt` | Per-crawler rules split by search / user-triggered / training role, plus `Content-Signal` |
| `sitemap.xml` | Index over `sitemap-pages.xml`, `sitemap-images.xml`, `sitemap-videos.xml` |
| `llms.txt` / `llms-full.txt` | LLM index, and the full text of every page in both languages |
| `cite.bib` / `CITATION.cff` / `codemeta.json` | Citation and software metadata |
| `results.json` / `results.csv` | The benchmark tables, so nothing has to be scraped from HTML |
| `page-index.json` | Machine-readable inventory of every page |
| `related-work.json` | Neighbouring directions under eight 2026 categories, each naming its page |
| `data/agentic-robotics-2026.json` | The 2026 reading list; arXiv identifiers resolved against the API |
| `data/search-targets.json` | Query to landing page, for assistants that start from a question |
| `index.md` / `zh/index.md` | Markdown mirrors of the two main pages, with YAML frontmatter (sub-pages get their own) |
| `project.json` | Canonical facts, benchmark numbers and identifiers for agents |
| `positioning.json` / `positioning.md` | Positioning and precedence: what TGL claims about itself, what it explicitly does not claim, the terms it introduced, and the dated record behind those statements |
| `feed.xml`, `favicon.ico` | Change feed and root icon |

The page carries a JSON-LD `@graph` (WebSite, WebPage, ScholarlyArticle, SoftwareSourceCode, Person,
CollegeOrUniversity, Organization, DefinedTermSet, ImageObject, 10 VideoObject, ItemList, Dataset and
FAQPage) and Google Scholar Highwire `citation_*` tags. `citation_publication_date` must stay in
`YYYY/MM/DD` form or Scholar mis-parses it.

Highwire `citation_*` tags appear on the two canonical pages — `/` and `/paper/` — and deliberately **not** on
the concept or research-context pages. Both carry the same `citation_title`, authors and `citation_pdf_url`, so
Scholar resolves them to one work with one PDF; the other pages would only add near-duplicate records. If that
ever needs to change, `_citation_tags()` in `scripts/seo.py` is the single place that emits them. `arxiv_id` and `doi` are `null` in `site.json`; when they are
filled in, `scripts/seo.py` emits `citation_arxiv_id` / `citation_doi` and the matching `identifier` and
`sameAs` automatically.

Three rules the build enforces: structured data must describe content that is actually visible on the page
(the `FAQPage` and `DefinedTerm` nodes exist because the FAQ and glossary are rendered); the sitemaps
discover figures from disk rather than assuming a count; and the positioning statement is machine-layer
only. Every claim in `positioning.json`/`positioning.md` is already asserted in the visible FAQ and the
research narrative — the statement adds structure, an explicit scope and a stable URL, not new facts — so
`check_site.py` fails if either filename is ever rendered into HTML.

**This is a technical report. The site does not claim venue acceptance anywhere, and that should not change
without the authors' instruction.**

## AI crawler access: two layers, currently disagreeing

`robots.txt` states intent; Cloudflare enforces. **As of 2026-09-16 the two do not match**, and this is the
single most consequential setting for AI discoverability:

| Layer | Training crawlers (GPTBot, ClaudeBot, CCBot, Bytespider, Amazonbot) | Search crawlers (OAI-SearchBot, Claude-SearchBot, PerplexityBot, Kimi-SearchBot, bingbot, Googlebot, Baiduspider) |
| --- | --- | --- |
| `robots.txt` section 3 | `Allow: /` | `Allow: /` |
| Cloudflare edge | **HTTP 403, "Your request was blocked."** | HTTP 200 with real content |

Blocking a *training* crawler does not affect whether the site appears in that product's answers — ChatGPT
search reads `OAI-SearchBot`, which is not blocked. So this does not harm AI-search visibility. It does
decide whether the work enters model training corpora.

To resolve it, change one side only:

- **To permit training**, open the Cloudflare dashboard → **AI Crawl Control** → **Crawlers** tab and set each of
  those agents to **Allow**. (Blocking is implemented as a zone-level WAF rule, so the change takes effect
  immediately.)
- **To reserve training rights**, edit `ROBOTS` in `scripts/seo.py` and change the section 3 `Allow:` lines to
  `Disallow:`.

Verify with a real user-agent probe after any change:

```bash
for ua in "GPTBot/1.4" "OAI-SearchBot/1.4" "ClaudeBot/1.0" "Claude-SearchBot/1.0" "CCBot/2.0"; do
  printf '%s  %s\n' "$(curl -s -o /dev/null -w '%{http_code}' -A "$ua" https://tgl.changnie.top/)" "$ua"
done
```

## Generated visual identity

`assets/brand/tgl-logo-v3.png` and `assets/brand/tgl-cover-v4.png` were created with native ImageGen for this project. The logo expresses robotic manipulation and capability growth. The cover is conceptual artwork, not a physical-robot experiment. Original generated PNGs are preserved. The cover is used in the page and social metadata.
