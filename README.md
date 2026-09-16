# Teach and Grow — project website

Bilingual project page for **Teach and Grow: An Agent-Centered Architecture for General Robot Learning**, by Chang Nie, Zhe Liu, and Hesheng Wang (Shanghai Jiao Tong University).

Review URL: **https://biubiu3.github.io/tgl-web/**  
Chinese: **https://biubiu3.github.io/tgl-web/zh/**

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
4. Wait for both `build` and `deploy` to succeed. Visit the review URL above.

Every subsequent push to `main` rebuilds, checks links and benchmark arithmetic, and deploys the static artifact. GitHub Pages ties the first path component to the repository name. An exact `biubiu3.github.io/tgl/` URL requires a repository named `tgl` or a route in the owner's `biubiu3.github.io` site.

## Future custom domain: tgl.changnie.top

Do this after accepting the review site. DNS has not been changed by this repository.

1. In this repository's **Settings → Pages → Custom domain**, enter `tgl.changnie.top` and save.
2. In the Cloudflare zone for `changnie.top`, create a DNS record: **CNAME**, name **tgl**, target **biubiu3.github.io**, **DNS only** (gray cloud), TTL **Auto**. The target is a hostname, with no scheme or path. Replace an existing record at `tgl` only after confirming it is no longer needed.
3. Update `deployment.json` to:
   ```json
   {
     "url": "https://tgl.changnie.top/",
     "custom_domain": "tgl.changnie.top"
   }
   ```
4. Commit and push. The build places the site at the domain root, updates canonical/hreflang/social/PDF/BibTeX URLs, sitemap and robots.txt, and emits `CNAME`. Chinese becomes `/zh/`.
5. Wait for GitHub's DNS check and certificate provisioning, then enable **Enforce HTTPS**. Check the English/Chinese pages, PDF, figures, and video playback over HTTPS. GitHub may need time to issue the certificate.
6. If GitHub requests ownership verification, use its exact TXT hostname and value in Cloudflare. No account password or Cloudflare global API key is needed.

The future configuration can be tested without altering the current review deployment:

```bash
python3 scripts/build.py --url https://tgl.changnie.top/ --custom-domain tgl.changnie.top --out dist-custom
python3 -m http.server 8001 --directory dist-custom
```

## Editing

- `content/site.json`: authors, exact benchmark values, paired-video descriptions in English and Chinese.
- `scripts/build.py`: bilingual page shell, videos, figures, metadata, and BibTeX.
- `scripts/research.py`: the bilingual research narrative and interactive worked example.
- `assets/style.css`: responsive layout and styling.
- `assets/app.js`: paired playback, filters, concept walkthrough, citation copy, figure lightbox.
- `assets/videos/`: original MP4s, preserved byte for byte.
- `assets/posters/`: actual video frames; 256 × 256 source videos are not artificially upscaled.
- `assets/figures/`: optimized WebP exports of the author's figures. Figure 1 is a conceptual illustration, not a physical-robot result.
- `assets/paper/teach-and-grow.pdf`: freshly built current 17-page manuscript.
- `content/provenance.json`: paper/figure source hashes and the video-label correction.

The supplied description calls Goal task 07 a bottle-cap task. The local LIBERO task map identifies it as `turn_on_the_stove`, consistent with inspection of both videos; the website uses that name. Paired video playback shares a start time but does not time-align actions or imply a speed comparison. The page presents five qualitative simulation examples, qualitative study descriptions, bounded observations, and clearly identified scaling hypotheses. It does not assert publication acceptance, a released robot codebase, empirical readiness, or an independently replicated benchmark.

Images open in an accessible native dialog (Escape to close). Videos retain native controls, and content remains readable when JavaScript is disabled. All stages of the worked example remain visible without JavaScript. Reduced-motion preferences are respected.

## Generated visual identity

`assets/brand/tgl-logo.png` and `assets/brand/tgl-cover.png` were created with native ImageGen for this project. The logo expresses robotic manipulation and capability growth. The cover is conceptual artwork, not a physical-robot experiment. Original generated PNGs are preserved. The cover is used in the page and social metadata.
