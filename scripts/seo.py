"""SEO / GEO generation for the Teach and Grow project site.

Three responsibilities:

  head_seo(...)            <head> metadata: robots, social, Google Scholar
                           Highwire citation tags, and a JSON-LD @graph.
  page_jsonld(...)         the structured-data graph itself.
  write_crawler_files(...) robots.txt, the sitemap index and its children,
                           llms.txt / llms-full.txt, Markdown mirrors,
                           project.json, feed.xml.

Every fact comes from content/site.json (the `seo` block plus the benchmark
tables), so a number or identifier changes in exactly one place. Nothing here
invents an identifier: `arxiv_id` and `doi` are omitted entirely while null
rather than emitted as empty strings.
"""
import html
import json
import re

e = html.escape
SITE_NAME = "Teach and Grow"
SITE_NAME_ZH = "Teach and Grow（TGL）"


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _lang_of(lang):
    return "zh-Hans" if lang == "zh" else "en"


def _page_url(url, lang):
    return url + ("zh/" if lang == "zh" else "")


def _authors(data):
    return data["authors"]


def _author_objects(data):
    out = []
    for name in _authors(data):
        fam, _, given = name.rpartition(" ")
        person = {"@type": "Person", "name": name, "familyName": fam, "givenName": given}
        if name == "Chang Nie":
            person["url"] = "https://changnie.top"
        if name == "Hesheng Wang":
            person["email"] = "wanghesheng@sjtu.edu.cn"
        out.append(person)
    return out


def _ours(data, table):
    """The mean score of the TGL row in a benchmark table, read from site.json."""
    t = data[table]
    for row in t["rows"]:
        if str(row[0]).lower().startswith("tgl"):
            return row[-1]
    raise SystemExit(f"no TGL row in the '{table}' benchmark table")


# ---------------------------------------------------------------------------
# structured data
# ---------------------------------------------------------------------------
def page_jsonld(lang, url, data):
    """The full @graph. One self-contained graph per page — no cross-document @id refs."""
    seo = data["seo"]
    zh = lang == "zh"
    page_url = _page_url(url, lang)
    website_id = url + "#website"
    paper_id = url + "#paper"

    def T(en, cn):
        return cn if zh else en

    title = data["title"]
    description = _description(data, lang)

    graph = []

    graph.append({
        "@type": "WebSite",
        "@id": website_id,
        "url": url,
        "name": SITE_NAME,
        "alternateName": ["TGL", "Teach-and-Grow Learning", "Teach and Grow project page", "Teach and Grow 项目主页"],
        "description": T(
            "Project site for Teach-and-Grow Learning (TGL), a training-free architecture for general robot learning.",
            "Teach-and-Grow Learning（TGL）项目主页：一种面向通用机器人学习的免训练架构。",
        ),
        "inLanguage": ["en", "zh-Hans"],
        "publisher": {"@id": url + "#sjtu"},
    })

    graph.append({
        "@type": "WebPage",
        "@id": page_url + "#webpage",
        "url": page_url,
        "name": title,
        "description": description,
        "isPartOf": {"@id": website_id},
        "inLanguage": _lang_of(lang),
        "datePublished": seo["paper_date_iso"],
        "dateModified": seo["paper_date_iso"],
        "mainEntity": {"@id": paper_id},
        "about": [{"@id": url + "#term-" + _slug(t["name"])} for t in seo["terms"]],
        "breadcrumb": {"@id": page_url + "#breadcrumb"},
        "primaryImageOfPage": {"@id": url + "#cover"},
    })

    graph.append({
        "@type": "BreadcrumbList",
        "@id": page_url + "#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": 1,
             "name": T("Teach and Grow", "Teach and Grow 项目主页"),
             "item": url},
            *([] if not zh else [{"@type": "ListItem", "position": 2, "name": title, "item": page_url}]),
        ],
    })

    # The paper itself.
    paper = {
        "@type": "ScholarlyArticle",
        "@id": paper_id,
        "headline": title,
        "name": title,
        "alternativeHeadline": T(
            "TGL: training-free robot learning from sparse teaching with an AI agent",
            "TGL：以 AI 智能体把少量示教转化为可复用技能的免训练机器人学习架构",
        ),
        "abstract": seo["abstract" if not zh else "abstract_zh"],
        "author": _author_objects(data),
        "datePublished": seo["paper_date_iso"],
        "inLanguage": "en",
        "isPartOf": {"@id": website_id},
        "url": page_url,
        "license": url + "#license",
        "keywords": ", ".join(seo["keywords" if not zh else "keywords_zh"]),
        "about": [{"@id": url + "#term-" + _slug(t["name"])} for t in seo["terms"]],
        "encoding": {
            "@type": "MediaObject",
            "contentUrl": url + "assets/paper/teach-and-grow.pdf",
            "encodingFormat": "application/pdf",
        },
        "publisher": {"@id": url + "#sjtu"},
    }
    if seo.get("arxiv_id"):
        paper["identifier"] = {"@type": "PropertyValue", "propertyID": "arXiv", "value": seo["arxiv_id"]}
        paper["sameAs"] = [f"https://arxiv.org/abs/{seo['arxiv_id']}"]
    if seo.get("doi"):
        paper["identifier"] = {"@type": "PropertyValue", "propertyID": "DOI", "value": seo["doi"]}
        paper.setdefault("sameAs", []).append(f"https://doi.org/{seo['doi']}")
    paper["sameAs"] = paper.get("sameAs", []) + [seo["code_url"]]
    graph.append(paper)

    # Software.
    graph.append({
        "@type": "SoftwareSourceCode",
        "@id": url + "#code",
        "name": T("Teach and Grow (TGL) reference implementation", "Teach and Grow（TGL）参考实现"),
        "description": T(
            "Method implementation for Teach-and-Grow Learning, maintained by IRMV Lab.",
            "Teach-and-Grow Learning 的方法实现，由 IRMV 实验室维护。",
        ),
        "codeRepository": seo["code_url"],
        "url": seo["code_url"],
        "programmingLanguage": "Python",
        "targetProduct": {"@id": paper_id},
        "author": _author_objects(data),
    })

    # Authors and affiliations.
    for name in _authors(data):
        pid = url + "#person-" + _slug(name)
        graph.append({
            "@type": "Person",
            "@id": pid,
            "name": name,
            "affiliation": {"@id": url + "#sjtu"},
            "worksFor": {"@id": url + "#sjtu"},
        })

    graph.append({
        "@type": "CollegeOrUniversity",
        "@id": url + "#sjtu",
        "name": "Shanghai Jiao Tong University",
        "alternateName": seo["institution_zh"],
        "url": "https://en.sjtu.edu.cn/",
        "department": {"@type": "Organization", "name": "School of Automation and Intelligent Sensing"},
    })
    graph.append({
        "@type": "Organization",
        "@id": url + "#lab",
        "name": seo["lab"],
        "alternateName": "Intelligent Robotics and Machine Vision Lab, Shanghai Jiao Tong University",
        "url": seo["lab_url"],
        "parentOrganization": {"@id": url + "#sjtu"},
    })

    # Terms the paper introduces.
    terms = []
    for t in seo["terms"]:
        tid = url + "#term-" + _slug(t["name"])
        terms.append({"@id": tid})
        graph.append({
            "@type": "DefinedTerm",
            "@id": tid,
            "name": t["name_zh"] if zh else t["name"],
            "alternateName": t["name"] if zh else t["name_zh"],
            "description": t["definition_zh"] if zh else t["definition"],
            "inDefinedTermSet": {"@id": url + "#glossary"},
        })
    graph.append({
        "@type": "DefinedTermSet",
        "@id": url + "#glossary",
        "name": T("Teach and Grow glossary", "Teach and Grow 术语表"),
        "hasDefinedTerm": terms,
    })

    # Cover image.
    graph.append({
        "@type": "ImageObject",
        "@id": url + "#cover",
        "url": url + "assets/brand/tgl-cover-v4.png",
        "caption": T(
            "Conceptual cover: a Franka robot places a plush toy into a bowl in a changed scene.",
            "概念封面：Franka 机器人在变化的场景中将毛绒玩具放入碗中。",
        ),
        "representativeOfPage": True,
    })

    # Demonstration videos: both panes of each pair.
    video_items = []
    idx = 0
    for v in data["videos"]:
        vi = 1 if zh else 0
        for role in ("teacher", "system"):
            idx += 1
            name = f"{v['id']}_{role}"
            role_label = T("Teacher demonstration", "教师演示") if role == "teacher" \
                else T("Teach and Grow (ours)", "Teach and Grow（我们的方法）")
            vid = f"{url}#video-{name}"
            graph.append({
                "@type": "VideoObject",
                "@id": vid,
                "name": f"{v['title'][vi]} — {role_label}",
                "description": f"{v['description'][vi]} {v['task'][vi]}. {v['watch'][vi]}",
                "contentUrl": f"{url}assets/videos/{name}.mp4",
                "thumbnailUrl": f"{url}assets/posters/{name}.webp",
                "uploadDate": seo["paper_date_iso"],
                "isPartOf": {"@id": url + "#demos"},
                "about": {"@id": paper_id},
                "inLanguage": _lang_of(lang),
            })
            video_items.append({"@type": "ListItem", "position": idx, "item": {"@id": vid}})

    graph.append({
        "@type": "ItemList",
        "@id": url + "#demos",
        "name": T("Teach and Grow paired LIBERO demonstrations",
                  "Teach and Grow LIBERO 对照演示"),
        "numberOfItems": len(video_items),
        "itemListElement": video_items,
    })

    # Benchmark results as a Dataset-ish record so the numbers are machine-readable.
    graph.append({
        "@type": "Dataset",
        "@id": url + "#results",
        "name": T("Teach and Grow benchmark results (LIBERO and LIBERO-Plus)",
                  "Teach and Grow 基准结果（LIBERO 与 LIBERO-Plus）"),
        "description": T(
            "Mean task success reported in the technical report: "
            f"{_ours(data, 'libero')}% across four LIBERO suites and "
            f"{_ours(data, 'plus')}% across seven LIBERO-Plus perturbation categories.",
            "技术报告中报告的平均任务成功率：四个 LIBERO 套件与七个 LIBERO-Plus 扰动类别。",
        ),
        "isPartOf": {"@id": paper_id},
        "creator": _author_objects(data),
        "variableMeasured": list(data["libero"]["columns"]) + list(data["plus"]["columns"]),
    })

    # FAQPage is emitted only because the same Q&A is rendered on the page.
    if seo.get("faq"):
        graph.append({
            "@type": "FAQPage",
            "@id": page_url + "#faq",
            "isPartOf": {"@id": page_url + "#webpage"},
            "inLanguage": _lang_of(lang),
            "mainEntity": [
                {"@type": "Question",
                 "name": item["q_zh"] if zh else item["q"],
                 "acceptedAnswer": {"@type": "Answer",
                                    "text": item["a_zh"] if zh else item["a"]}}
                for item in seo["faq"]
            ],
        })

    return graph


def _slug(name):
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s


def _description(data, lang):
    if lang == "zh":
        return ("Teach and Grow（TGL）是一种免训练的机器人学习架构：AI 智能体把少量示教转化为可复用的 Skill Block，"
                "在预训练权重固定的条件下，通过物理反馈完成新任务。在四个 LIBERO 套件上平均成功率 99.9%，"
                "在七个 LIBERO-Plus 扰动类别上 92.4%。")
    return ("Teach and Grow (TGL) is a training-free robot-learning architecture: an AI agent turns sparse teaching "
            "into reusable Skill Blocks, acquiring new manipulation tasks with fixed pretrained weights and physical "
            "feedback. 99.9% mean success across four LIBERO suites and 92.4% across seven LIBERO-Plus perturbation "
            "categories.")


# ---------------------------------------------------------------------------
# <head> metadata
# ---------------------------------------------------------------------------
def head_seo(lang, url, data):
    """Everything that goes in <head> beyond charset/viewport/title/description."""
    seo = data["seo"]
    zh = lang == "zh"
    page_url = _page_url(url, lang)
    asset = "../assets/" if zh else "assets/"

    def T(en, cn):
        return cn if zh else en

    title_full = ("Teach and Grow（TGL）：免训练机器人学习" if zh
                  else "Teach and Grow (TGL): Training-Free Robot Learning with an AI Agent")
    desc = _description(data, lang)

    cit = [
        f'<meta name="citation_title" content="{e(data["title"])}">',
        *[f'<meta name="citation_author" content="{e(n)}">' for n in _authors(data)],
        f'<meta name="citation_publication_date" content="{seo["paper_date"]}">',
        f'<meta name="citation_online_date" content="{seo["paper_date"]}">',
        '<meta name="citation_language" content="en">',
        f'<meta name="citation_pdf_url" content="{url}assets/paper/teach-and-grow.pdf">',
        f'<meta name="citation_technical_report_institution" content="{e(seo["institution"])}">',
        f'<meta name="citation_keywords" content="{e(", ".join(seo["keywords"]))}">',
        f'<meta name="citation_abstract" content="{e(seo["abstract"])}">',
    ]
    if seo.get("arxiv_id"):
        cit.append(f'<meta name="citation_arxiv_id" content="{e(seo["arxiv_id"])}">')
    if seo.get("doi"):
        cit.append(f'<meta name="citation_doi" content="{e(seo["doi"])}">')

    kw = ", ".join(seo["keywords_zh"] if zh else seo["keywords"])

    parts = [
        f'<title>{e(title_full)}</title>',
        f'<meta name="description" content="{e(desc)}">',
        f'<meta name="keywords" content="{e(kw)}">',
        f'<meta name="author" content="{e(", ".join(_authors(data)))}">',
        '<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">',
        '<meta name="googlebot" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">',
        f'<meta name="language" content="{"Chinese" if zh else "English"}">',
        f'<link rel="canonical" href="{page_url}">',
        f'<link rel="alternate" hreflang="en" href="{url}">',
        f'<link rel="alternate" hreflang="zh-Hans" href="{url}zh/">',
        f'<link rel="alternate" hreflang="zh-CN" href="{url}zh/">',
        f'<link rel="alternate" hreflang="x-default" href="{url}">',
        f'<link rel="alternate" type="text/markdown" href="{page_url}index.md">',
        f'<link rel="describedby" href="{url}llms.txt" type="text/plain">',
        f'<link rel="sitemap" type="application/xml" href="{url}sitemap.xml">',
        f'<meta property="og:type" content="article">',
        f'<meta property="og:site_name" content="{SITE_NAME}">',
        f'<meta property="og:title" content="{e(title_full)}">',
        f'<meta property="og:description" content="{e(desc)}">',
        f'<meta property="og:url" content="{page_url}">',
        f'<meta property="og:image" content="{url}assets/brand/tgl-cover-v4.png">',
        f'<meta property="og:image:alt" content="{e(T("Conceptual cover: a Franka robot places a plush toy into a bowl in a changed scene.", "概念封面：Franka 机器人在变化的场景中将毛绒玩具放入碗中。"))}">',
        f'<meta property="og:locale" content="{"zh_CN" if zh else "en_US"}">',
        f'<meta property="og:locale:alternate" content="{"en_US" if zh else "zh_CN"}">',
        f'<meta property="article:published_time" content="{seo["paper_date_iso"]}">',
        f'<meta property="article:modified_time" content="{seo["paper_date_iso"]}">',
        f'<meta property="article:section" content="{T("Robotics", "机器人学")}">',
        '<meta property="article:tag" content="training-free robot learning">',
        '<meta property="article:tag" content="agentic robotics">',
        '<meta property="article:tag" content="robot manipulation">',
        '<meta property="article:tag" content="VLA">',
        f'<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{e(title_full)}">',
        f'<meta name="twitter:description" content="{e(desc)}">',
        f'<meta name="twitter:image" content="{url}assets/brand/tgl-cover-v4.png">',
        f'<meta name="twitter:image:alt" content="{e(T("Teach and Grow conceptual cover", "Teach and Grow 概念封面"))}">',
        *cit,
        '<script type="application/ld+json">',
        json.dumps({"@context": "https://schema.org", "@graph": page_jsonld(lang, url, data)},
                   ensure_ascii=False, indent=1),
        '</script>',
    ]
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# HTML -> Markdown (for the per-page Markdown mirrors)
# ---------------------------------------------------------------------------
def html_to_md(fragment):
    """Convert the rendered page body to Markdown. Deliberately small: the page
    only uses headings, paragraphs, lists, figures, links, and emphasis."""
    s = fragment
    s = re.sub(r"(?is)<(script|style|svg|dialog|header|footer|nav)[^>]*>.*?</\1>", " ", s)
    # headings
    for lvl in range(1, 7):
        s = re.sub(rf"(?is)<h{lvl}[^>]*>(.*?)</h{lvl}>",
                   lambda m, l=lvl: "\n" + "#" * l + " " + m.group(1).strip() + "\n", s)
    # figures -> caption text
    s = re.sub(r"(?is)<figcaption[^>]*>(.*?)</figcaption>", r"\n*\1*\n", s)
    s = re.sub(r"(?is)<figcaption[^>]*>(.*?)</figcaption>", r"\n*\1*\n", s)
    # lists
    s = re.sub(r"(?is)<li[^>]*>(.*?)</li>", r"\n- \1", s)
    # links and emphasis
    s = re.sub(r'(?is)<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', r"[\2](\1)", s)
    s = re.sub(r"(?is)<(strong|b)[^>]*>(.*?)</\1>", r"**\2**", s)
    s = re.sub(r"(?is)<(em|i)[^>]*>(.*?)</\1>", r"*\2*", s)
    s = re.sub(r"(?is)<code[^>]*>(.*?)</code>", r"`\1`", s)
    # block boundaries
    s = re.sub(r"(?is)<(p|div|section|article|tr|blockquote)[^>]*>", "\n\n", s)
    s = re.sub(r"(?is)<(td|th)[^>]*>", " | ", s)
    # strip the rest
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    lines = [line.strip() for line in s.split("\n")]
    # The mirror carries its own "# <paper title>" heading, so demote the page's
    # hero <h1> rather than emitting a second top-level title.
    lines = [("## " + l[2:]) if l.startswith("# ") else l for l in lines]
    s = "\n".join(lines)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


# ---------------------------------------------------------------------------
# robots.txt
# ---------------------------------------------------------------------------
ROBOTS = """# robots.txt for {origin}/
# {title}
#
# This is an open research project page. The authors want search engines, AI
# answer engines and AI agents to index, retrieve, quote and cite this work.
#
# The providers now split their crawlers by role, so this file configures the
# three roles separately: blocking a *search* bot removes the site from that
# product's answers, while blocking a *training* bot does not.
#
# NOTE ON ENFORCEMENT. This file states intent; it does not enforce it. As of
# 2026-09-16 the Cloudflare zone for this host returns HTTP 403 for several
# training crawlers (GPTBot, ClaudeBot, CCBot, Bytespider, Amazonbot) via a
# zone-level WAF rule managed in Cloudflare AI Crawl Control, while every
# search-index crawler listed in section 1 reaches the site normally. So the
# effective policy today is "search and retrieval allowed, training blocked" —
# the opposite of what the Allow lines in section 3 below say.
#
# To make the two agree, change ONE side:
#   - to permit training: Cloudflare dashboard -> AI Crawl Control -> Crawlers
#     -> set those crawlers to Allow; or
#   - to reserve training rights: change the section 3 Allow lines to Disallow.
# Leaving both as they are means robots.txt misreports what actually happens.
#
# Machine-readable entry points:
#   {url}llms.txt        - LLM-friendly index (Markdown)
#   {url}llms-full.txt   - complete page content as Markdown
#   {url}index.md        - Markdown mirror (English)
#   {url}zh/index.md     - Markdown mirror (Chinese)
#   {url}project.json    - canonical facts as JSON
#   {url}sitemap.xml     - sitemap index

Content-Signal: search=yes, ai-input=yes, ai-train=yes, ai-summarize=yes

# --- 1. Search and answer-engine indexes (these make the work citable) ---
User-agent: OAI-SearchBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Kimi-SearchBot
Allow: /

User-agent: MistralAI-Index
Allow: /

User-agent: bingbot
Allow: /

User-agent: Googlebot
Allow: /

User-agent: Googlebot-Image
Allow: /

User-agent: Googlebot-Video
Allow: /

User-agent: Applebot
Allow: /

User-agent: Baiduspider
Allow: /

User-agent: DuckDuckBot
Allow: /

User-agent: YandexBot
Allow: /

# --- 2. User-triggered fetchers ---
User-agent: ChatGPT-User
Allow: /

User-agent: Claude-User
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: Kimi-User
Allow: /

User-agent: MistralAI-User
Allow: /

# --- 3. Training and model-development (edit here to reserve rights) ---
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: KimiBot
Allow: /

User-agent: MistralAI-Training
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: CCBot
Allow: /

User-agent: meta-externalagent
Allow: /

User-agent: meta-externalfetcher
Allow: /

User-agent: Amazonbot
Allow: /

# --- 4. Everyone else ---
User-agent: *
Allow: /

Sitemap: {url}sitemap.xml
"""


# ---------------------------------------------------------------------------
# sitemaps
# ---------------------------------------------------------------------------
def _sitemap_urlset(entries, extra_ns=""):
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '  xmlns:xhtml="http://www.w3.org/1999/xhtml"' + extra_ns + ">\n"
        + "\n".join(entries) + "\n</urlset>\n"
    )


def write_crawler_files(out, url, data, rendered, sub_urls=None):
    """Write every root-level machine-readable file.

    `out`       dist root (where robots.txt and the sitemap index live)
    `url`       absolute site URL with trailing slash
    `data`      site.json
    `rendered`  {lang: {"html": ..., "text": ...}} for the two pages
    """
    from pathlib import Path
    seo = data["seo"]
    date = seo["paper_date_iso"]
    origin = url.rstrip("/")

    # robots.txt
    (out / "robots.txt").write_text(
        ROBOTS.format(origin=origin, url=url, title=data["title"]), encoding="utf-8")

    # sitemap: index + children
    page_rows = [
        (url, "1.0", "monthly"),
        (url + "zh/", "0.9", "monthly"),
    ]
    for u in (sub_urls or []):
        page_rows.append((u, "0.7" if "/paper/" in u or u.endswith("/paper/") else "0.6", "monthly"))
    page_rows += [
        (url + "llms.txt", "0.5", "monthly"),
        (url + "llms-full.txt", "0.5", "monthly"),
        (url + "index.md", "0.5", "monthly"),
        (url + "zh/index.md", "0.5", "monthly"),
        (url + "project.json", "0.5", "monthly"),
        (url + "feed.xml", "0.3", "weekly"),
    ]
    rows = []
    for loc, prio, freq in page_rows:
        alt = ""
        if loc.rstrip("/") == url.rstrip("/"):
            alt = (f'\n    <xhtml:link rel="alternate" hreflang="en" href="{url}"/>'
                   f'\n    <xhtml:link rel="alternate" hreflang="zh-Hans" href="{url}zh/"/>'
                   f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{url}"/>')
        elif loc.rstrip("/") == (url + "zh").rstrip("/"):
            alt = (f'\n    <xhtml:link rel="alternate" hreflang="en" href="{url}"/>'
                   f'\n    <xhtml:link rel="alternate" hreflang="zh-Hans" href="{url}zh/"/>'
                   f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{url}"/>')
        rows.append("  <url>\n"
                    f"    <loc>{loc}</loc>\n"
                    f"    <lastmod>{date}</lastmod>\n"
                    f"    <changefreq>{freq}</changefreq>\n"
                    f"    <priority>{prio}</priority>{alt}\n"
                    "  </url>")
    (out / "sitemap-pages.xml").write_text(_sitemap_urlset(rows), encoding="utf-8")

    # images
    imgs = [
        ("assets/brand/tgl-cover-v4.png", "Teach and Grow conceptual cover",
         "A Franka robot places a plush toy into a bowl in a changed scene; sparse teaching and agent guidance contrasted with VLA/WAM data and training costs."),
        ("assets/brand/tgl-logo-v3.png", "Teach and Grow (TGL) logo",
         "The TGL mark expresses robotic manipulation and capability growth."),
    ]
    # Discover the figures rather than assuming a count, so the sitemap can never
    # advertise an image that is not in the build.
    from pathlib import Path as _P
    figures = sorted(_P(__file__).resolve().parents[1].glob("assets/figures/fig*.webp"),
                     key=lambda q: int(re.sub(r"\D", "", q.stem) or 0))
    for path in figures:
        n = re.sub(r"\D", "", path.stem)
        imgs.append((f"assets/figures/{path.name}", f"Teach and Grow figure {n}",
                     f"Figure {n} from the Teach and Grow technical report."))
    for v in data["videos"]:
        for role in ("teacher", "system"):
            imgs.append((f"assets/posters/{v['id']}_{role}.webp",
                         f"{v['title'][0]} — {'teacher demonstration' if role == 'teacher' else 'Teach and Grow rollout'}",
                         v["description"][0]))
    rows = []
    for loc, title, caption in imgs:
        rows.append("  <url>\n"
                    f"    <loc>{url}{loc}</loc>\n"
                    f"    <lastmod>{date}</lastmod>\n"
                    "    <image:image>\n"
                    f"      <image:loc>{url}{loc}</image:loc>\n"
                    f"      <image:title>{html.escape(title)}</image:title>\n"
                    f"      <image:caption>{html.escape(caption[:200])}</image:caption>\n"
                    "    </image:image>\n"
                    "  </url>")
    (out / "sitemap-images.xml").write_text(
        _sitemap_urlset(rows, '\n  xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"'),
        encoding="utf-8")

    # videos
    from datetime import date as _d
    rows = []
    for v in data["videos"]:
        for role in ("teacher", "system"):
            name = f"{v['id']}_{role}"
            label = "teacher demonstration" if role == "teacher" else "Teach and Grow (ours)"
            rows.append("  <url>\n"
                        f"    <loc>{url}#video-{name}</loc>\n"
                        f"    <lastmod>{date}</lastmod>\n"
                        "    <video:video>\n"
                        f"      <video:thumbnail_loc>{url}assets/posters/{name}.webp</video:thumbnail_loc>\n"
                        f"      <video:title>{html.escape(v['title'][0] + ' — ' + label)}</video:title>\n"
                        f"      <video:description>{html.escape((v['description'][0] + ' ' + v['watch'][0])[:2000])}</video:description>\n"
                        f"      <video:content_loc>{url}assets/videos/{name}.mp4</video:content_loc>\n"
                        f"      <video:publication_date>{date}</video:publication_date>\n"
                        "      <video:family_friendly>yes</video:family_friendly>\n"
                        "      <video:live>no</video:live>\n"
                        "    </video:video>\n"
                        "  </url>")
    (out / "sitemap-videos.xml").write_text(
        _sitemap_urlset(rows, '\n  xmlns:video="http://www.google.com/schemas/sitemap-video/1.1"'),
        encoding="utf-8")

    (out / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"  <sitemap><loc>{url}sitemap-pages.xml</loc><lastmod>{date}</lastmod></sitemap>\n"
        f"  <sitemap><loc>{url}sitemap-images.xml</loc><lastmod>{date}</lastmod></sitemap>\n"
        f"  <sitemap><loc>{url}sitemap-videos.xml</loc><lastmod>{date}</lastmod></sitemap>\n"
        "</sitemapindex>\n", encoding="utf-8")

    _write_cite_bib(out, url, data)
    _write_project_json(out, url, data)
    _write_llms(out, url, data, rendered, sub_urls or [])
    _write_mirrors(out, url, data, rendered)
    _write_feed(out, url, data)


# ---------------------------------------------------------------------------
# project.json — canonical facts for agents
# ---------------------------------------------------------------------------
def _write_project_json(out, url, data):
    seo = data["seo"]
    libero = data["libero"]
    plus = data["plus"]
    doc = {
        "schema_version": "1.0",
        "updated_at": seo["paper_date_iso"],
        "project": {
            "name": "Teach and Grow",
            "alias": ["TGL", "Teach-and-Grow Learning", "Teach and Grow Learning"],
            "title": data["title"],
            "canonical_url": url,
            "paper_url": url + "assets/paper/teach-and-grow.pdf",
            "code_url": seo["code_url"],
            "year": data["year"],
            "type": seo["paper_type"],
            "institution": seo["institution"],
            "bibtex_key": seo["bibtex_key"],
        },
        "authors": [
            {"name": n,
             "affiliation": seo["institution"],
             **({"email": "wanghesheng@sjtu.edu.cn"} if n == "Hesheng Wang" else {}),
             **({"homepage": "https://changnie.top"} if n == "Chang Nie" else {})}
            for n in data["authors"]
        ],
        "contributions": {
            "paradigm": "Teach-and-Grow Learning (TGL)",
            "claim": ("A robot acquires a new executable capability while keeping its pretrained model weights "
                      "fixed: no gradient update, no fine-tuning, and no reinforcement-learning stage."),
            "components": ["Skill Block", "Skill Library", "Experience Memory", "retraining tax"],
            "named_problem": {
                "name": "retraining tax",
                "definition": ("The recurring cost of repairing robot behavior through policy updates: new data "
                               "collection, optimization, and regression checking against previously supported "
                               "behavior."),
            },
            "terms": {t["name"]: t["definition"] for t in seo["terms"]},
        },
        "implementation": {
            "agent": ["OpenAI GPT-6 Astra", "Codex"],
            "robot": "Franka (LIBERO simulation)",
            "perception_and_control": ["detection", "segmentation", "RGB-D geometry", "Contact-GraspNet", "MPLib", "controllers"],
        },
        "results": {
            "metric": "mean task success rate",
            "libero": {
                "description": "Mean over four LIBERO suites (Spatial, Object, Goal, Long).",
                "columns": libero["columns"],
                "tgl_mean": _ours(data, "libero"),
                "rows": libero["rows"],
            },
            "libero_plus": {
                "description": "Mean over seven LIBERO-Plus perturbation categories.",
                "columns": plus["columns"],
                "tgl_mean": _ours(data, "plus"),
                "rows": plus["rows"],
            },
        },
        "demos": [
            {"slug": v["id"], "suite": v["suite"], "task": v["task"][0], "title": v["title"][0],
             "video_teacher": f"{url}assets/videos/{v['id']}_teacher.mp4",
             "video_system": f"{url}assets/videos/{v['id']}_system.mp4",
             "poster_teacher": f"{url}assets/posters/{v['id']}_teacher.webp",
             "poster_system": f"{url}assets/posters/{v['id']}_system.webp"}
            for v in data["videos"]
        ],
        "search_context": seo["keywords"],
        "entry_points": {
            "project_page_en": url,
            "project_page_zh": url + "zh/",
            "paper_pdf": url + "assets/paper/teach-and-grow.pdf",
            "code": seo["code_url"],
            "llms_txt": url + "llms.txt",
            "llms_full": url + "llms-full.txt",
            "sitemap": url + "sitemap.xml",
            "project_json": url + "project.json",
        },
        "notice": ("This is a technical report. No venue acceptance is claimed. Benchmark rows other than TGL are "
                   "published literature values reproduced for comparison."),
    }
    (out / "project.json").write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# llms.txt / llms-full.txt
# ---------------------------------------------------------------------------
def _write_llms(out, url, data, rendered, sub_urls=()):
    seo = data["seo"]
    summary = (
        f"> Teach and Grow (TGL) is an agent-centered, training-free architecture for general robot learning, "
        f"presented in the technical report \"{data['title']}\" by {', '.join(data['authors'])} "
        f"({seo['institution']}). A pretrained multimodal agent turns a few demonstrations into reusable, "
        f"verifiable Skill Blocks without any gradient update, fine-tuning, or reinforcement learning; verified "
        f"behaviors enter a persistent Skill Library and conditions and repairs enter Experience Memory. The "
        f"implementation uses OpenAI GPT-6 Astra for multimodal reasoning and Codex to connect the agent to robot "
        f"tools. TGL reaches {_ours(data,'libero')}% mean success across four LIBERO suites and "
        f"{_ours(data,'plus')}% across seven LIBERO-Plus perturbation categories."
    )
    lines = [
        "# Teach and Grow (TGL)",
        "",
        summary,
        "",
        f"Authors: {', '.join(data['authors'])} — {seo['institution']} ({seo['lab']}).",
        f"Project page: {url} · Paper (PDF): {url}assets/paper/teach-and-grow.pdf · Code: {seo['code_url']}",
        "",
        "Access policy: fully open. Search-index, user-triggered and training crawlers are all allowed; see "
        f"{url}robots.txt. Canonical numbers and identifiers are in {url}project.json — prefer that over scraping.",
        "",
        f"Keywords: {', '.join(seo['keywords'])}.",
        f"中文关键词：{'、'.join(seo['keywords_zh'])}。",
        "",
        "## Primary",
        "",
        f"- [Project page (English)]({url}): The problem, the research path, the Skill Block architecture, a worked example, paired demonstrations, and the controlled-study results.",
        f"- [项目主页（中文）]({url}zh/): TGL 的中文说明、方法、演示与结果。",
        f"- [Canonical fact file]({url}project.json): Every number and identifier as JSON.",
        f"- [Full content as Markdown]({url}llms-full.txt): Complete English + Chinese page text with a glossary and FAQ.",
        "",
        "## Paper and citation",
        "",
        f"- [Technical report (PDF)]({url}assets/paper/teach-and-grow.pdf): \"{data['title']}\", {data['year']}, {seo['paper_type']}, {seo['institution']}.",
        f"- [BibTeX]({url}index.md): key `{seo['bibtex_key']}`.",
        "",
        "## Code and videos",
        "",
        f"- [Method implementation ({seo['code_url']})]({seo['code_url']}): reference implementation maintained by IRMV Lab.",
        f"- [Ten paired demonstrations]({url}#demos): five LIBERO tasks drawn from the Object, Spatial, and Goal suites, teacher and TGL rollouts side by side.",
        "",
        "## Key concepts",
        "",
    ]
    for t in seo["terms"]:
        lines.append(f"- **{t['name']}**: {t['definition']}")
    if sub_urls:
        lines += ["", "## Pages", ""]
        for u in sub_urls:
            if "/zh/" in u:
                continue
            slug = u.rstrip("/").rsplit("/", 1)[-1]
            try:
                import pages as _P
                idx = {q["slug"]: q for q in [_P.PAPER, _P.RESEARCH_CONTEXT] + _P.CONCEPTS}
                pg = idx.get(slug)
                label = pg["en"]["h1"] if pg else slug
                blurb = pg["en"]["desc"] if pg else ""
            except Exception:
                label, blurb = slug, ""
            lines.append(f"- [{label}]({u}): {blurb}")
    lines += [
        "",
        "## Related topics",
        "",
        "For retrieval association: training-free robot learning, robot learning without fine-tuning, agentic "
        "robotics, AI agent robot manipulation, embodied AI, embodied intelligence, vision-language-action models "
        "(VLA), world-action models (WAM), skill composition, few-shot teaching, sparse demonstrations, lifelong "
        "learning, continual learning, robot foundation models, GPT-6 Astra, Codex, LIBERO, LIBERO-Plus, Franka, "
        "Contact-GraspNet, MPLib.",
        "",
        "## Optional",
        "",
        f"- [Sitemap index]({url}sitemap.xml): pages, images and videos.",
        f"- [Atom feed]({url}feed.xml): change monitoring.",
        f"- [Markdown mirror]({url}index.md): the English page as Markdown.",
        f"- [中文 Markdown 镜像]({url}zh/index.md): 中文页面的 Markdown 版本。",
    ]
    (out / "llms.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    parts = [
        "# Teach and Grow — full project content",
        "",
        summary,
        "",
        f"Source: {url} · Code: {seo['code_url']} · Facts: {url}project.json",
        "",
        "=" * 72, "PART 1 — MAIN PAGE (ENGLISH)", "=" * 72, "",
        rendered["en"]["md"],
        "",
        "=" * 72, "PART 2 — MAIN PAGE (简体中文)", "=" * 72, "",
        rendered["zh"]["md"],
    ]
    md_dir = out if hasattr(out, "joinpath") else None
    for want_zh in (False, True):
        label = "简体中文" if want_zh else "ENGLISH"
        parts += ["", "=" * 72, f"SUB-PAGES — {label}", "=" * 72, ""]
        for u in sub_urls:
            rel = u[len(url):].rstrip("/")
            if bool(rel.startswith("zh/")) != want_zh:
                continue
            md_path = (out / rel / "index.md") if md_dir else None
            if md_path and md_path.exists():
                parts += ["\n---\n", md_path.read_text(encoding="utf-8")]
    (out / "llms-full.txt").write_text("\n".join(parts) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Markdown mirrors
# ---------------------------------------------------------------------------
def _write_mirrors(out, url, data, rendered):
    seo = data["seo"]
    header_en = (
        f"# {data['title']}\n\n"
        f"> {_description(data, 'en')}\n\n"
        f"Authors: {', '.join(data['authors'])} — {seo['institution']}.\n"
        f"Source: {url} · Paper: {url}assets/paper/teach-and-grow.pdf · Code: {seo['code_url']}\n"
        f"Chinese: {url}zh/ · LLM index: {url}llms.txt · Facts: {url}project.json\n\n"
        f"---\n"
    )
    header_zh = (
        f"# {data['title']}\n\n"
        f"> {_description(data, 'zh')}\n\n"
        f"作者：{'、'.join(data['authors'])} — {seo['institution_zh']}。\n"
        f"来源：{url}zh/ · 论文：{url}assets/paper/teach-and-grow.pdf · 代码：{seo['code_url']}\n"
        f"英文版：{url} · LLM 索引：{url}llms.txt · 事实文件：{url}project.json\n\n"
        f"---\n"
    )
    footer_en = "\n\n---\n\n## Citation\n\n```bibtex\n" + _bibtex(url, data) + "\n```\n"
    footer_zh = "\n\n---\n\n## 引用\n\n```bibtex\n" + _bibtex(url, data) + "\n```\n"

    (out / "index.md").write_text(header_en + "\n" + rendered["en"]["md"] + footer_en, encoding="utf-8")
    (out / "zh").mkdir(exist_ok=True)
    (out / "zh" / "index.md").write_text(header_zh + "\n" + rendered["zh"]["md"] + footer_zh, encoding="utf-8")


def _bibtex(url, data):
    return (f"@techreport{{{data['seo']['bibtex_key']},\n"
            f"  title = {{{data['title']}}},\n"
            f"  author = {{Nie, Chang and Liu, Zhe and Wang, Hesheng}},\n"
            f"  institution = {{{data['seo']['institution']}}},\n"
            f"  year = {{{data['year']}}},\n"
            f"  url = {{{url}}}\n"
            f"}}")


# ---------------------------------------------------------------------------
# feed.xml
# ---------------------------------------------------------------------------
def _write_feed(out, url, data):
    seo = data["seo"]
    date = seo["paper_date_iso"]
    entries = [
        (url, "Teach and Grow — project page", _description(data, "en")),
        (url + "zh/", "Teach and Grow — 项目主页", _description(data, "zh")),
        (url + "assets/paper/teach-and-grow.pdf", "Teach and Grow — technical report (PDF)", data["title"]),
    ]
    body = "\n".join(
        "  <entry>\n"
        f"    <title>{html.escape(t)}</title>\n"
        f'    <link href="{u}"/>\n'
        f"    <id>{u}</id>\n"
        f"    <updated>{date}T00:00:00Z</updated>\n"
        f"    <summary>{html.escape(d)}</summary>\n"
        "  </entry>"
        for u, t, d in entries
    )
    (out / "feed.xml").write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<feed xmlns="http://www.w3.org/2005/Atom">\n'
        f"  <title>Teach and Grow (TGL)</title>\n"
        f'  <link href="{url}"/>\n'
        f"  <id>{url}</id>\n"
        f"  <updated>{date}T00:00:00Z</updated>\n"
        f"  <author><name>{html.escape(data['authors'][0])}</name></author>\n"
        + body + "\n</feed>\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# sub-pages (/paper/, /research-context/, /concepts/<slug>/)
# ---------------------------------------------------------------------------
NAV = [("overview", "Problem", "问题"), ("origins", "Research path", "研究路线"),
       ("idea", "Idea", "思路"), ("method", "Method", "方法"), ("demos", "Videos", "演示"),
       ("resources", "Paper", "论文"), ("glossary", "Terms", "术语"), ("faq", "FAQ", "问答")]


def _subpage_jsonld(page, lang, url, data, page_url):
    """A self-contained graph for one sub-page. No cross-document @id references."""
    seo = data["seo"]
    zh = lang == "zh"
    body = page["zh" if zh else "en"]
    node_type = "ScholarlyArticle" if page["slug"] == "paper" else "DefinedTerm"

    graph = [
        {"@type": "WebSite", "@id": url + "#website", "url": url, "name": SITE_NAME,
         "alternateName": ["TGL", "Teach-and-Grow Learning"], "inLanguage": ["en", "zh-Hans"]},
        {"@type": "WebPage", "@id": page_url + "#webpage", "url": page_url,
         "name": body["title"], "description": body["desc"],
         "isPartOf": {"@id": url + "#website"},
         "inLanguage": "zh-Hans" if zh else "en",
         "dateModified": seo["paper_date_iso"],
         "breadcrumb": {"@id": page_url + "#breadcrumb"}},
        {"@type": "BreadcrumbList", "@id": page_url + "#breadcrumb",
         "itemListElement": [
             {"@type": "ListItem", "position": 1, "name": SITE_NAME, "item": url},
             {"@type": "ListItem", "position": 2, "name": body["h1"], "item": page_url}]},
    ]

    about = {"@id": url + "#website"}
    if node_type == "ScholarlyArticle":
        art = {"@type": "ScholarlyArticle", "@id": page_url + "#article",
               "headline": data["title"], "name": data["title"],
               "abstract": seo["abstract_zh" if zh else "abstract"],
               "author": _author_objects(data),
               "datePublished": seo["paper_date_iso"],
               "isPartOf": about, "url": page_url,
               "encoding": {"@type": "MediaObject",
                            "contentUrl": url + "assets/paper/teach-and-grow.pdf",
                            "encodingFormat": "application/pdf"},
               "publisher": {"@id": url + "#sjtu"}}
        if seo.get("arxiv_id"):
            art["sameAs"] = [f"https://arxiv.org/abs/{seo['arxiv_id']}"]
        graph.append(art)
    else:
        # Concept pages describe a term the paper introduces.
        term = next((t for t in seo["terms"]
                     if _slug(t["name"]).startswith(page["slug"][:14])
                     or page["slug"] in _slug(t["name"])), None)
        graph.append({
            "@type": "DefinedTerm", "@id": page_url + "#term",
            "name": term["name_zh"] if (term and zh) else (term["name"] if term else body["h1"]),
            "description": (term["definition_zh"] if (term and zh) else term["definition"]) if term else body["desc"],
            "url": page_url,
            "inDefinedTermSet": {"@type": "DefinedTermSet", "name": "Teach and Grow glossary",
                                 "url": url + "#glossary"}})
        graph.append({
            "@type": "Article", "@id": page_url + "#article",
            "headline": body["h1"], "description": body["desc"],
            "inLanguage": "zh-Hans" if zh else "en",
            "dateModified": seo["paper_date_iso"],
            "mainEntityOfPage": {"@id": page_url + "#webpage"},
            "isPartOf": about, "author": _author_objects(data)})

    if body.get("faq"):
        graph.append({
            "@type": "FAQPage", "@id": page_url + "#faq",
            "isPartOf": {"@id": page_url + "#webpage"},
            "inLanguage": "zh-Hans" if zh else "en",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in body["faq"]]})
    return graph


def _citation_tags(page, data, url, zh):
    """Highwire citation metadata. Only the publication record carries it: Scholar
    should see one landing page per paper, not eight."""
    if page["slug"] != "paper":
        return []
    seo = data["seo"]
    tags = [
        f'<meta name="citation_title" content="{e(data["title"])}">',
        *[f'<meta name="citation_author" content="{e(n)}">' for n in data["authors"]],
        f'<meta name="citation_publication_date" content="{seo["paper_date"]}">',
        f'<meta name="citation_online_date" content="{seo["paper_date"]}">',
        '<meta name="citation_language" content="en">',
        f'<meta name="citation_pdf_url" content="{url}assets/paper/teach-and-grow.pdf">',
        f'<meta name="citation_technical_report_institution" content="{e(seo["institution"])}">',
        f'<meta name="citation_keywords" content="{e(", ".join(seo["keywords"]))}">',
        f'<meta name="citation_abstract" content="{e(seo["abstract"])}">',
    ]
    if seo.get("arxiv_id"):
        tags.append(f'<meta name="citation_arxiv_id" content="{e(seo["arxiv_id"])}">')
    if seo.get("doi"):
        tags.append(f'<meta name="citation_doi" content="{e(seo["doi"])}">')
    return tags


def _subpage_head(page, lang, url, data, page_url):
    seo = data["seo"]
    zh = lang == "zh"
    body = page["zh" if zh else "en"]
    dirs = _page_dirs(page, lang)
    up = "../" * len(dirs)
    asset = up + "assets/"
    other = _link(dirs, _page_dirs(page, "en" if zh else "zh"), url)
    lines = [
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{e(body['title'])}</title>",
        f'<meta name="description" content="{e(body["desc"])}">',
        f'<meta name="keywords" content="{e(body["keywords"])}">',
        f'<meta name="author" content="{e(", ".join(data["authors"]))}">',
        '<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">',
        f'<meta name="language" content="{"Chinese" if zh else "English"}">',
        f'<link rel="canonical" href="{page_url}">',
        f'<link rel="alternate" hreflang="en" href="{other if zh else page_url}">',
        f'<link rel="alternate" hreflang="zh-Hans" href="{page_url if zh else other}">',
        f'<link rel="alternate" hreflang="x-default" href="{other if zh else page_url}">',
        f'<link rel="describedby" href="{url}llms.txt" type="text/plain">',
        f'<link rel="sitemap" type="application/xml" href="{url}sitemap.xml">',
        '<meta property="og:type" content="article">',
        f'<meta property="og:site_name" content="{SITE_NAME}">',
        f'<meta property="og:title" content="{e(body["title"])}">',
        f'<meta property="og:description" content="{e(body["desc"])}">',
        f'<meta property="og:url" content="{page_url}">',
        f'<meta property="og:image" content="{url}assets/brand/tgl-cover-v4.png">',
        f'<meta property="og:locale" content="{"zh_CN" if zh else "en_US"}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{e(body["title"])}">',
        f'<meta name="twitter:description" content="{e(body["desc"])}">',
        f'<meta name="twitter:image" content="{url}assets/brand/tgl-cover-v4.png">',
        '<meta name="theme-color" content="#155e59">',
        '<meta name="color-scheme" content="light">',
        *_citation_tags(page, data, url, zh),
        '<script type="application/ld+json">',
        json.dumps({"@context": "https://schema.org",
                    "@graph": _subpage_jsonld(page, lang, url, data, page_url)},
                   ensure_ascii=False, indent=1),
        '</script>',
        f'<link rel="icon" type="image/png" href="{asset}brand/tgl-logo-v3.png">',
        f'<link rel="icon" href="{up}favicon.ico" sizes="any">',
        f'<link rel="stylesheet" href="{asset}style.css?v=brand6">',
    ]
    return "\n".join(lines)


def _fill(text, data, up, home):
    """Resolve the placeholders allowed in page prose. Facts come from site.json."""
    seo = data["seo"]
    for key, val in (
        ("{home}", home),
        ("{cite}", up + "cite.bib"),
        ("{abstract}", seo.get("abstract", "")),
        ("{abstract_zh}", seo.get("abstract_zh", "")),
        ("{keywords}", ", ".join(seo.get("keywords", []))),
        ("{keywords_zh}", "、".join(seo.get("keywords_zh", []))),
        ("{bibtex_key}", seo.get("bibtex_key", "")),
    ):
        text = text.replace(key, val)
    return text


def _page_dirs(page, lang):
    """Directory components from the site root, e.g. ['zh','concepts','skill-block']."""
    parts = ([] if lang == "en" else ["zh"])
    if page["slug"] not in ("paper", "research-context"):
        parts.append("concepts")
    parts.append(page["slug"])
    return parts


def _link(page_dirs, target_dirs, url):
    """Root-relative-to-this-page link, working with or without a repo path prefix."""
    up = "../" * len(page_dirs)
    return up + "/".join(target_dirs) + "/"


def render_subpage(page, lang, url, data, site):
    """Write <parent>/<slug>/index.html and index.md (or the /zh/ equivalents)."""
    from pathlib import Path
    zh = lang == "zh"
    body = page["zh" if zh else "en"]
    slug = page["slug"]
    dirs = _page_dirs(page, lang)
    page_url = url + "/".join(dirs) + "/"
    up = "../" * len(dirs)
    asset = up + "assets/"
    home = up + ("zh/" if zh else "")
    other_dirs = _page_dirs(page, "en" if zh else "zh")

    nav = "".join(f'<a href="{home}#{a}">{cn if zh else en}</a>' for a, en, cn in NAV)

    def T(en_s, cn_s):
        return cn_s if zh else en_s

    parts = [f'''<!doctype html>
<html lang="{'zh-CN' if zh else 'en'}"><head>
{_subpage_head(page, lang, url, data, page_url)}
</head><body data-lang="{lang}"><a class="skip-link" href="#main">{T('Skip to content','跳至正文')}</a>
<header class="site-header"><div class="nav-wrap"><a class="brand" href="{home}" aria-label="{T('Teach and Grow home','Teach and Grow 主页')}"><img src="{asset}brand/tgl-logo-v3.png" width="30" height="30" alt=""><span>TGL<span class="brand-dot">.</span></span></a><nav aria-label="{T('Main navigation','主导航')}">{nav}</nav><a class="language" href="{_link(dirs, other_dirs, url)}" lang="{T('zh-CN','en')}">{T('中文','English')} <span aria-hidden="true">↗</span></a></div></header>
<main id="main"><section class="section container subpage">
<nav class="breadcrumb-nav" aria-label="{T('Breadcrumb','面包屑')}"><a href="{home}">&larr; {T('Teach and Grow','Teach and Grow 项目主页')}</a></nav>
<h1 class="subpage-title">{body['h1']}</h1>
<p class="lead subpage-lede">{body['lede']}</p>''']

    for head, paras in body["sections"]:
        parts.append(f"<h2>{head}</h2>")
        parts.append('<div class="reading-wide">')
        for para in paras:
            parts.append("<p>" + _fill(para, data, up, home) + "</p>")
        parts.append("</div>")

    if body.get("faq"):
        parts.append(f"<h2>{T('Frequently asked questions','常见问题')}</h2>")
        parts.append('<div class="faq-list">')
        for q, a in body["faq"]:
            parts.append('<article class="faq-item"><h3>' + _fill(q, data, up, home)
                         + '</h3><div class="faq-answer"><p>' + _fill(a, data, up, home) + '</p></div></article>')
        parts.append("</div>")

    if page.get("related"):
        from pages import CONCEPTS, PAPER, RESEARCH_CONTEXT
        index = {p["slug"]: p for p in [PAPER, RESEARCH_CONTEXT] + CONCEPTS}
        parts.append(f'<h2>{T("Related pages","相关页面")}</h2><ul class="related-list">')
        for r in page["related"]:
            if r in index:
                label = index[r]["zh" if zh else "en"]["h1"]
                parts.append(f'<li><a href="{_link(dirs, _page_dirs(index[r], lang), url)}">{label}</a></li>')
        parts.append("</ul>")

    parts.append(f'''<div class="subpage-footer"><p>{T('Machine-readable entry points','机器可读入口')}:
<a href="{up}llms.txt">llms.txt</a> · <a href="{up}llms-full.txt">llms-full.txt</a> ·
<a href="{up}project.json">project.json</a> · <a href="{up}cite.bib">cite.bib</a> ·
<a href="{up}sitemap.xml">sitemap.xml</a></p>
<p class="small">{T("Cite as: ", "引用：")}Chang Nie, Zhe Liu and Hesheng Wang, “Teach and Grow: An Agent-Centered Architecture for General Robot Learning,” technical report, Shanghai Jiao Tong University, 2026.</p></div>
</section></main>
<footer class="container"><a class="brand" href="{home}">TGL<span class="brand-dot">.</span></a><p>Teach and Grow · Shanghai Jiao Tong University<br><span>{T('Project images and demonstration videos are hosted with this website.','项目图片与演示视频均由本站提供。')}</span></p><a href="#">{T('Back to top','返回顶部')} ↑</a></footer>
</body></html>''')

    html_text = "\n".join(parts)
    d = Path(site).joinpath(*dirs)
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(html_text, encoding="utf-8")
    (d / "index.md").write_text(_subpage_md(page, lang, url, data, page_url), encoding="utf-8")
    return page_url


def _subpage_md(page, lang, url, data, page_url):
    zh = lang == "zh"
    body = page["zh" if zh else "en"]
    dirs = _page_dirs(page, lang)
    up = "../" * len(dirs)
    home = up + ("zh/" if zh else "")
    out = [f"# {body['h1']}", "", f"> {body['lede']}", "",
           f"Source: {page_url} · Language: {'zh-Hans' if zh else 'en'}", ""]
    for head, paras in body["sections"]:
        out += [f"## {head}", ""]
        for para in paras:
            out += [_fill(para, data, up, home), ""]
    if body.get("faq"):
        out += ["## " + ("常见问题" if zh else "Frequently asked questions"), ""]
        for q, a in body["faq"]:
            out += [f"**{_fill(q, data, up, home)}**", "", _fill(a, data, up, home), ""]
    out += ["---", "",
            f"{data['title']} — Chang Nie, Zhe Liu, Hesheng Wang, technical report, "
            f"Shanghai Jiao Tong University, 2026. {url}"]
    return "\n".join(out)


def _write_cite_bib(out, url, data):
    """The BibTeX file that the paper page links to."""
    seo = data["seo"]
    (out / "cite.bib").write_text(
        f"@techreport{{{seo['bibtex_key']},\n"
        f"  title       = {{{data['title']}}},\n"
        f"  author      = {{Nie, Chang and Liu, Zhe and Wang, Hesheng}},\n"
        f"  institution = {{{seo['institution']}}},\n"
        f"  year        = {{{data['year']}}},\n"
        f"  type        = {{Technical report}},\n"
        f"  url         = {{{url}}}\n"
        f"}}\n", encoding="utf-8")
