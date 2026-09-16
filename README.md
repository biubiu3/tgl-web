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
- `scripts/research.py`: the bilingual research narrative, abstract block, glossary, FAQ and interactive worked example.
- `assets/style.css`: responsive layout and styling.
- `assets/app.js`: paired playback, filters, concept walkthrough, citation copy, figure lightbox.
- `assets/videos/`: original MP4s, preserved byte for byte.
- `assets/posters/`: actual video frames; 256 × 256 source videos are not artificially upscaled.
- `assets/figures/`: optimized WebP exports of the author's figures. Figure 1 is a conceptual illustration, not a physical-robot result.
- `assets/paper/teach-and-grow.pdf`: freshly built current 17-page manuscript.
- `content/provenance.json`: paper/figure source hashes and the video-label correction.

The supplied description calls Goal task 07 a bottle-cap task. The local LIBERO task map identifies it as `turn_on_the_stove`, consistent with inspection of both videos; the website uses that name. Paired video playback shares a start time but does not time-align actions or imply a speed comparison. The page presents five qualitative simulation examples, qualitative study descriptions, bounded observations, and clearly identified scaling hypotheses. It does not assert publication acceptance, complete paper reproduction from the public code snapshot, empirical readiness, or an independently replicated benchmark.

Images open in an accessible native dialog (Escape to close). Videos retain native controls, and content remains readable when JavaScript is disabled. All stages of the worked example remain visible without JavaScript. Reduced-motion preferences are respected.

## Search and AI discovery

The build emits a machine-readable layer so that search engines, answer engines and AI agents can read the
project without scraping HTML. All of it is generated from `content/site.json`:

| File | Purpose |
| --- | --- |
| `robots.txt` | Per-crawler rules split by search / user-triggered / training role, plus `Content-Signal` |
| `sitemap.xml` | Index over `sitemap-pages.xml`, `sitemap-images.xml`, `sitemap-videos.xml` |
| `llms.txt` / `llms-full.txt` | LLM index, and the full English + Chinese text as Markdown |
| `index.md` / `zh/index.md` | Markdown mirrors of the two pages |
| `project.json` | Canonical facts, benchmark numbers and identifiers for agents |
| `feed.xml`, `favicon.ico` | Change feed and root icon |

The page carries a JSON-LD `@graph` (WebSite, WebPage, ScholarlyArticle, SoftwareSourceCode, Person,
CollegeOrUniversity, Organization, DefinedTermSet, ImageObject, 10 VideoObject, ItemList, Dataset and
FAQPage) and Google Scholar Highwire `citation_*` tags. `citation_publication_date` must stay in
`YYYY/MM/DD` form or Scholar mis-parses it. `arxiv_id` and `doi` are `null` in `site.json`; when they are
filled in, `scripts/seo.py` emits `citation_arxiv_id` / `citation_doi` and the matching `identifier` and
`sameAs` automatically.

Two rules the build enforces: structured data must describe content that is actually visible on the page
(the `FAQPage` and `DefinedTerm` nodes exist because the FAQ and glossary are rendered), and the sitemaps
discover figures from disk rather than assuming a count.

**This is a technical report. The site does not claim venue acceptance anywhere, and that should not change
without the authors' instruction.**

## Generated visual identity

`assets/brand/tgl-logo-v3.png` and `assets/brand/tgl-cover-v4.png` were created with native ImageGen for this project. The logo expresses robotic manipulation and capability growth. The cover is conceptual artwork, not a physical-robot experiment. Original generated PNGs are preserved. The cover is used in the page and social metadata.
