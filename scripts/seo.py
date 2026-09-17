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

# The 2026 agentic-robotics topics this site addresses, with the page that treats
# each one. `menus` are used as JSON-LD `mentions` on pages where the topic is
# named or linked, so the association is always backed by something visible.
TOPIC_PAGES = [
    ("Agentic robotics", "research/agentic-robotics-2026/"),
    ("AI agent robotics", "concepts/ai-agent-robotic-arm/"),
    ("Agent as Policy", "concepts/agent-as-policy/"),
    ("Coding agents for robotics", "concepts/coding-agent-robotics/"),
    ("Physical in-context learning", "concepts/physical-in-context-learning/"),
    ("General-purpose agent robots", "concepts/general-purpose-agent-robot/"),
    ("Robot agent memory", "concepts/robot-agent-memory/"),
    ("Robot learning without retraining", "concepts/no-retraining-robot-learning/"),
    ("Runtime reasoning robotics", "concepts/runtime-reasoning-robotics/"),
    ("Tool-using robot agents", "concepts/tool-use-robotics/"),
    ("GPT-6 robotics", "concepts/gpt-6-robotic-arm/"),
    ("Frontier model robotics", "concepts/gpt-6-robotic-arm/"),
    ("Robotic manipulation", "concepts/general-robot-learning/"),
    ("Robot skill libraries", "concepts/skill-library/"),
    ("Physical AI", "concepts/physical-ai/"),
    ("Vision-language-action models", "concepts/vla-without-retraining/"),
]


def _topic_mentions(url, exclude=()):
    return [{"@type": "Thing", "name": name, "url": url + path}
            for name, path in TOPIC_PAGES if name not in exclude]
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
        "dateModified": seo.get("updated_iso", seo["paper_date_iso"]),
        "mainEntity": {"@id": paper_id},
        "about": [{"@id": url + "#term-" + _slug(t["name"])} for t in seo["terms"]],
        "breadcrumb": {"@id": page_url + "#breadcrumb"},
        "primaryImageOfPage": {"@id": url + "#cover"},
        # The topics the homepage names in its research-context bridge or links in its footer.
        "mentions": _topic_mentions(url),
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
    ids = []
    same = []
    if seo.get("arxiv_id"):
        ids.append({"@type": "PropertyValue", "propertyID": "arXiv", "value": seo["arxiv_id"]})
        same.append(seo["arxiv_url"])
    if seo.get("doi"):
        ids.append({"@type": "PropertyValue", "propertyID": "DOI", "value": seo["doi"]})
        same.append(seo["doi_url"])
    if ids:
        paper["identifier"] = ids
    paper["sameAs"] = same + [seo["code_url"]]
    if seo.get("arxiv_pdf_url"):
        paper["sameAs"].append(seo["arxiv_pdf_url"])
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
            "Mean task success reported in the paper: "
            f"{_ours(data, 'libero')}% across four LIBERO suites and "
            f"{_ours(data, 'plus')}% across seven LIBERO-Plus perturbation categories.",
            "论文中报告的平均任务成功率：四个 LIBERO 套件与七个 LIBERO-Plus 扰动类别。",
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

def _citation_tags_values(seo, data, url, pdf_url=None, abstract_html_url=None):
    """The Highwire citation set. One definition, used by every page that carries it."""
    tags = [
        f'<meta name="citation_title" content="{e(data["title"])}">',
        *[f'<meta name="citation_author" content="{e(n)}">' for n in data["authors"]],
        f'<meta name="citation_publication_date" content="{seo["paper_date"]}">',
        f'<meta name="citation_online_date" content="{seo["paper_date_iso"]}">',
        '<meta name="citation_language" content="en">',
        f'<meta name="citation_pdf_url" content="{pdf_url or seo.get("arxiv_pdf_url", "")}">',
    ]
    if abstract_html_url:
        tags.append(f'<meta name="citation_abstract_html_url" content="{abstract_html_url}">')
    if seo.get("arxiv_id"):
        tags.append(f'<meta name="citation_arxiv_id" content="{e(seo["arxiv_id"])}">')
    if seo.get("doi"):
        tags.append(f'<meta name="citation_doi" content="{e(seo["doi"])}">')
    tags += [
        f'<meta name="citation_author_institution" content="{e(seo["institution"])}">',
        f'<meta name="citation_keywords" content="{e(", ".join(seo["keywords"]))}">',
        f'<meta name="citation_abstract" content="{e(seo["abstract"])}">',
    ]
    return tags


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

    cit = _citation_tags_values(seo, data, url,
                                pdf_url=url + "assets/paper/teach-and-grow.pdf",
                                abstract_html_url=url + "paper/")

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


def write_crawler_files(out, url, data, rendered, sub_urls=None, all_pages=None):
    """Write every root-level machine-readable file.

    `out`       dist root (where robots.txt and the sitemap index live)
    `url`       absolute site URL with trailing slash
    `data`      site.json
    `rendered`  {lang: {"html": ..., "text": ...}} for the two pages
    """
    from pathlib import Path
    seo = data["seo"]
    date = seo["paper_date_iso"]
    updated = seo.get("updated_iso", date)
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
        (url + "results.json", "0.5", "monthly"),
        (url + "results.csv", "0.4", "monthly"),
        (url + "page-index.json", "0.4", "monthly"),
        (url + "related-work.json", "0.4", "monthly"),
        (url + "data/agentic-robotics-2026.json", "0.4", "monthly"),
        (url + "data/search-targets.json", "0.4", "monthly"),
        (url + "CITATION.cff", "0.4", "yearly"),
        (url + "codemeta.json", "0.4", "yearly"),
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
                    f"    <lastmod>{updated}</lastmod>\n"
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
                     f"Figure {n} from the Teach and Grow paper."))
    for v in data["videos"]:
        for role in ("teacher", "system"):
            imgs.append((f"assets/posters/{v['id']}_{role}.webp",
                         f"{v['title'][0]} — {'teacher demonstration' if role == 'teacher' else 'Teach and Grow rollout'}",
                         v["description"][0]))
    rows = []
    for loc, title, caption in imgs:
        rows.append("  <url>\n"
                    f"    <loc>{url}{loc}</loc>\n"
                    f"    <lastmod>{updated}</lastmod>\n"
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
                        f"    <lastmod>{updated}</lastmod>\n"
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
    _write_data_endpoints(out, url, data, sub_urls or [])
    _write_citation_cff(out, url, data)
    _write_codemeta(out, url, data)
    _write_project_json(out, url, data)
    _write_llms(out, url, data, rendered, sub_urls or [], all_pages or [])
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
            "published": seo["paper_date_iso"],
            "arxiv_id": seo.get("arxiv_id"),
            "arxiv_url": seo.get("arxiv_url"),
            "doi": seo.get("doi"),
            "doi_url": seo.get("doi_url"),
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
        "topics": [
            "agentic robotics",
            "AI agent robotics",
            "agent as policy",
            "general-purpose agent robotics",
            "GPT-6 robotics",
            "GPT robotic arm",
            "frontier model robotics",
            "coding agent robotics",
            "physical in-context learning",
            "robot experience memory",
            "robot skill library",
            "runtime reasoning robotics",
            "tool-using robot agents",
            "robot learning without task-specific retraining",
        ],
        "research_context_2026": {
            "hub": url + "research/agentic-robotics-2026/",
            "pages": {
                "GPT-6 robotic arm": url + "concepts/gpt-6-robotic-arm/",
                "Agent as Policy": url + "concepts/agent-as-policy/",
                "Coding agents for robotics": url + "concepts/coding-agent-robotics/",
                "Physical in-context learning": url + "concepts/physical-in-context-learning/",
                "General-purpose agent robot": url + "concepts/general-purpose-agent-robot/",
                "Robot learning without retraining": url + "concepts/no-retraining-robot-learning/",
                "Robot agent memory": url + "concepts/robot-agent-memory/",
                "Runtime reasoning": url + "concepts/runtime-reasoning-robotics/",
                "Tool use in robotics": url + "concepts/tool-use-robotics/",
            },
        },
        "entry_points": {
            "project_page_en": url,
            "project_page_zh": url + "zh/",
            "paper_pdf": url + "assets/paper/teach-and-grow.pdf",
            "code": seo["code_url"],
            "llms_txt": url + "llms.txt",
            "llms_full": url + "llms-full.txt",
            "sitemap": url + "sitemap.xml",
            "project_json": url + "project.json",
            "agentic_robotics_2026": url + "data/agentic-robotics-2026.json",
            "search_targets": url + "data/search-targets.json",
        },
        "notice": ("This paper is available as an arXiv preprint. Benchmark rows other than TGL are "
                   "published literature values reproduced for comparison."),
    }
    (out / "project.json").write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# llms.txt / llms-full.txt
# ---------------------------------------------------------------------------
def _write_llms(out, url, data, rendered, sub_urls=(), all_pages=None):
    seo = data["seo"]
    summary = (
        f"> Teach and Grow (TGL) is an agent-centered, training-free architecture for general robot learning, "
        f"presented in the paper \"{data['title']}\" by {', '.join(data['authors'])} "
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
        f"- [arXiv preprint (PDF)]({url}assets/paper/teach-and-grow.pdf): \"{data['title']}\", {data['year']}, {seo['paper_type']}, {seo['institution']}.",
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
            idx = {q["slug"]: q for q in (all_pages or [])}
            pg = idx.get(slug)
            if pg:
                label = pg["en"]["h1"]
                blurb = pg["en"]["desc"]
            else:
                # derived index pages carry their own copy
                fallback = {
                    "concepts": ("Concept index", "Every concept page for Teach-and-Grow Learning in one place."),
                    "glossary": ("Glossary", "Definitions of the terms this work introduces."),
                    "faq": ("FAQ", "Direct answers about Teach-and-Grow Learning."),
                }
                label, blurb = fallback.get(slug, (slug, ""))
            lines.append(f"- [{label}]({u}): {blurb}")
    lines += [
        "",
        "## Current agentic-robotics context",
        "",
        f"- [Agentic robotics in 2026]({url}research/agentic-robotics-2026/): the research map — frontier models driving robot arms, agents inside the execution loop, coding agents, physical in-context learning, robot memory, and where TGL fits.",
        f"- [GPT-6 robotic arms]({url}concepts/gpt-6-robotic-arm/): GPT-6-class models as a reasoning layer for manipulation; the role GPT-6 Astra plays in TGL.",
        f"- [Agent as Policy (AGP)]({url}concepts/agent-as-policy/): the agent inside the execution loop, with current examples and a comparison against TGL.",
        f"- [Coding agents for robotics]({url}concepts/coding-agent-robotics/): models that write and run robot programs; Codex's role in TGL.",
        f"- [Physical in-context learning]({url}concepts/physical-in-context-learning/): adapting a robot from context without updating weights.",
        f"- [General-purpose agent robot]({url}concepts/general-purpose-agent-robot/): one agent across many tasks, and what it does not retain.",
        f"- [Robot agent memory]({url}concepts/robot-agent-memory/): what a robot should keep from an interaction.",
        f"- [Robot learning without retraining]({url}concepts/no-retraining-robot-learning/): acquiring tasks with frozen weights.",
        f"- [Runtime reasoning]({url}concepts/runtime-reasoning-robotics/): deciding while the task is running.",
        f"- [Tool use in robotics]({url}concepts/tool-use-robotics/): perception, grasping and motion as callable tools.",
        f"- [2026 reading list]({url}data/agentic-robotics-2026.json): neighbouring work with arXiv identifiers, verified.",
        f"- [Query to page map]({url}data/search-targets.json): the queries each page is written to answer.",
        "",
        "## Related topics",
        "",
        "For retrieval association: training-free robot learning, robot learning without fine-tuning, agentic "
        "robotics, AI agent robot manipulation, embodied AI, embodied intelligence, vision-language-action models "
        "(VLA), world-action models (WAM), skill composition, few-shot teaching, sparse demonstrations, lifelong "
        "learning, continual learning, robot foundation models, GPT-6 Astra, Codex, LIBERO, LIBERO-Plus, Franka, "
        "Contact-GraspNet, MPLib. "
        "2026 agentic-robotics context: agent as policy (AGP), coding agent robotics, physical in-context "
        "learning, single-video robot learning, robot experience memory, robot skill library, runtime reasoning "
        "robotics, tool-using robot agents, frontier-model robot control, general-purpose agent robots, "
        "robot learning without task-specific retraining.",
        "",
        "## Optional",
        "",
        f"- [Sitemap index]({url}sitemap.xml): pages, images and videos.",
        f"- [Atom feed]({url}feed.xml): change monitoring.",
        f"- [Markdown mirror]({url}index.md): the English page as Markdown.",
        f"- [中文 Markdown 镜像]({url}zh/index.md): 中文页面的 Markdown 版本。",
    ]
    (out / "llms.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    parts = ["# Teach and Grow — full project content", "", summary, ""]
    parts += _knowledge_base(url, data)
    md_dir = out if hasattr(out, "joinpath") else None
    for want_zh, label in ((False, "ENGLISH"), (True, "简体中文")):
        parts += ["", "=" * 72, f"FULL PAGES — {label}", "=" * 72, ""]
        mains = (["index.md"] if not want_zh else ["zh/index.md"])
        for m in mains:
            mp = (out / m) if md_dir else None
            if mp and mp.exists():
                parts += ["\n---\n", mp.read_text(encoding="utf-8")]
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
def _frontmatter(data, url, page_url, lang):
    """YAML frontmatter for the Markdown mirrors, so a plain-text reader gets the
    canonical identity before any prose."""
    seo = data["seo"]
    zh = lang == "zh"
    lines = ["---",
             f'title: "{data["title"]}"',
             'short_name: "TGL"',
             f'expanded_name: "Teach-and-Grow Learning"',
             f'canonical: "{page_url}"',
             f'project: "{url}"',
             f'paper_page: "{url}paper/"']
    if seo.get("arxiv_id"):
        lines.append(f'arxiv: "{seo["arxiv_id"]}"')
        lines.append(f'arxiv_url: "{seo["arxiv_url"]}"')
    if seo.get("doi"):
        lines.append(f'doi: "{seo["doi"]}"')
    lines += [f'published: "{seo["paper_date_iso"]}"',
              f'updated: "{seo.get("updated_iso", seo["paper_date_iso"])}"',
              f'type: "{seo["paper_type"]}"',
              f'status: "no venue acceptance claimed"',
              "authors:"]
    lines += [f'  - {n}' for n in data["authors"]]
    lines += [f'institution: "{seo["institution"]}"',
              "language: " + ("zh-Hans" if zh else "en"),
              "topics:"]
    topics = (seo["keywords_zh"][:10] if zh else seo["keywords"][:10])
    lines += [f'  - {t}' for t in topics]
    lines += [f'code: "{seo["code_url"]}"',
              f'llms_txt: "{url}llms.txt"',
              f'citation: "{url}cite.bib"',
              "---", ""]
    return "\n".join(lines)


def _write_mirrors(out, url, data, rendered):
    seo = data["seo"]
    urls = {lang: url + ("zh/" if lang == "zh" else "") for lang in ("en", "zh")}
    for lang in ("en", "zh"):
        page_url = urls[lang]
        head = _frontmatter(data, url, page_url, lang)
        head += f"# {data['title']}\n\n> {_description(data, lang)}\n\n"
        head += (f"Authors: {', '.join(data['authors'])} — {seo['institution']}.\n"
                 f"Source: {page_url} · Paper: {url}paper/ · Code: {seo['code_url']}\n"
                 f"Facts: {url}project.json · LLM index: {url}llms.txt\n\n---\n")
        foot = "\n\n---\n\n## " + ("引用" if lang == "zh" else "Citation") + "\n\n```bibtex\n" \
               + _bibtex(url, data) + "\n```\n"
        path = (out / "zh" / "index.md") if lang == "zh" else (out / "index.md")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(head + "\n" + rendered[lang]["md"] + foot, encoding="utf-8")


def _bibtex(url, data):
    seo = data['seo']
    return (f"@misc{{{seo['bibtex_key']},\n"
            f"  title = {{{data['title']}}},\n"
            f"  author = {{Nie, Chang and Liu, Zhe and Wang, Hesheng}},\n"
            f"  year = {{{data['year']}}},\n"
            f"  eprint = {{{seo['arxiv_id']}}},\n"
            f"  archivePrefix = {{arXiv}},\n"
            f"  primaryClass = {{cs.RO}},\n"
            f"  doi = {{{seo['doi']}}},\n"
            f"  url = {{{seo['arxiv_url']}}}\n"
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
        (url + "assets/paper/teach-and-grow.pdf", "Teach and Grow — paper (PDF)", data["title"]),
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


def _page_registry():
    """Every sub-page by slug, so `related` resolves across all three page modules."""
    import pages as PAGES
    import pages_extra as PAGES_EXTRA
    import pages_hot as PAGES_HOT
    everything = [PAGES.PAPER, PAGES.RESEARCH_CONTEXT, PAGES_HOT.HUB]
    everything += PAGES.CONCEPTS + PAGES_EXTRA.CONCEPTS + PAGES_HOT.CONCEPTS
    return {p["slug"]: p for p in everything}


def _subpage_jsonld(page, lang, url, data, page_url):
    """A self-contained graph for one sub-page. No cross-document @id references."""
    seo = data["seo"]
    zh = lang == "zh"
    body = page["zh" if zh else "en"]
    # A page that declares its own @type is not a glossary entry: the 2026 research
    # map is an Article, and tagging it DefinedTerm would invent a term.
    declared = page.get("schema")
    if page["slug"] == "paper":
        node_type = "ScholarlyArticle"
    elif declared and "DefinedTerm" not in declared:
        node_type = declared[0]
    else:
        node_type = "DefinedTerm"

    graph = [
        {"@type": "WebSite", "@id": url + "#website", "url": url, "name": SITE_NAME,
         "alternateName": ["TGL", "Teach-and-Grow Learning"], "inLanguage": ["en", "zh-Hans"]},
        {"@type": "WebPage", "@id": page_url + "#webpage", "url": page_url,
         "name": body["title"], "description": body["desc"],
         "isPartOf": {"@id": url + "#website"},
         "inLanguage": "zh-Hans" if zh else "en",
         "dateModified": seo.get("updated_iso", seo["paper_date_iso"]),
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
        ids, same = [], []
        if seo.get("arxiv_id"):
            ids.append({"@type": "PropertyValue", "propertyID": "arXiv", "value": seo["arxiv_id"]})
            same.append(seo["arxiv_url"])
        if seo.get("doi"):
            ids.append({"@type": "PropertyValue", "propertyID": "DOI", "value": seo["doi"]})
            same.append(seo["doi_url"])
        if ids:
            art["identifier"] = ids
        if same:
            art["sameAs"] = same
        graph.append(art)
        # The article names its publisher, so the node has to exist in this document:
        # the graph is self-contained and nothing may point outside it.
        graph.append({
            "@type": "CollegeOrUniversity", "@id": url + "#sjtu",
            "name": "Shanghai Jiao Tong University",
            "alternateName": seo["institution_zh"],
            "url": "https://en.sjtu.edu.cn/",
            "department": {"@type": "Organization",
                           "name": "School of Automation and Intelligent Sensing"},
        })
    else:
        if node_type == "DefinedTerm":
            # Concept pages describe a term the paper introduces.
            term = next((t for t in seo["terms"]
                         if _slug(t["name"]).startswith(page["slug"][:14])
                         or page["slug"] in _slug(t["name"])), None)
            node = {
                "@type": "DefinedTerm", "@id": page_url + "#term",
                "name": term["name_zh"] if (term and zh) else (term["name"] if term else body["h1"]),
                "description": (term["definition_zh"] if (term and zh) else term["definition"]) if term else body["desc"],
                "url": page_url}
            # Only the six glossary terms claim membership of the term set; the wider
            # 2026 pages define their own term on their own page and are not listed there.
            if term:
                node["inDefinedTermSet"] = {"@type": "DefinedTermSet",
                                            "name": "Teach and Grow glossary",
                                            "url": url + "#glossary"}
            graph.append(node)
        graph.append({
            "@type": "Article", "@id": page_url + "#article",
            "headline": body["h1"], "description": body["desc"],
            "inLanguage": "zh-Hans" if zh else "en",
            "dateModified": seo.get("updated_iso", seo["paper_date_iso"]),
            "mainEntityOfPage": {"@id": page_url + "#webpage"},
            "isPartOf": about, "author": _author_objects(data)})

    if page.get("topics"):
        graph.append({
            "@type": "ItemList", "@id": page_url + "#topics",
            "name": "Topics covered",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1,
                 "item": {"@type": "Thing", "name": name, "url": url + path}}
                for i, (name, path) in enumerate(
                    (n, p) for n, p in TOPIC_PAGES if n in page["topics"])],
        })

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
    return _citation_tags_values(data["seo"], data, url,
                                 pdf_url=url + "assets/paper/teach-and-grow.pdf",
                                 abstract_html_url=url + "paper/")


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
        f'<link rel="stylesheet" href="{asset}style.css?v=readability1">',
    ]
    return "\n".join(lines)


def _fill(text, data, up, home, url):
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
        ("{arxiv_url}", seo.get("arxiv_url", "")),
        ("{arxiv_pdf}", seo.get("arxiv_pdf_url", "")),
        ("{doi_url}", seo.get("doi_url", "")),
        ("{code}", seo.get("code_url", "")),
        ("{pdf}", url + "assets/paper/teach-and-grow.pdf"),
    ):
        text = text.replace(key, val)
    return text


def _page_dirs(page, lang):
    """Directory components from the site root, e.g. ['zh','concepts','skill-block'].

    The parent folder is explicit on the page dict; never inferred from the slug,
    because that put /faq/ and /glossary/ one level too deep.
    """
    parts = ([] if lang == "en" else ["zh"])
    parent = page.get("parent", "")
    if parent:
        parts.append(parent)
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
            parts.append("<p>" + _fill(para, data, up, home, url) + "</p>")
        parts.append("</div>")

    if body.get("faq"):
        parts.append(f"<h2>{T('Frequently asked questions','常见问题')}</h2>")
        parts.append('<div class="faq-list">')
        for q, a in body["faq"]:
            parts.append('<article class="faq-item"><h3>' + _fill(q, data, up, home, url)
                         + '</h3><div class="faq-answer"><p>' + _fill(a, data, up, home, url) + '</p></div></article>')
        parts.append("</div>")

    if page.get("related"):
        index = _page_registry()
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
<p class="small">{T("Cite as: ", "引用：")}Chang Nie, Zhe Liu and Hesheng Wang, “Teach and Grow: An Agent-Centered Architecture for General Robot Learning,” arXiv:2608.17209, 2026.</p></div>
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
            out += [_fill(para, data, up, home, url), ""]
    if body.get("faq"):
        out += ["## " + ("常见问题" if zh else "Frequently asked questions"), ""]
        for q, a in body["faq"]:
            out += [f"**{_fill(q, data, up, home, url)}**", "", _fill(a, data, up, home, url), ""]
    out += ["---", "",
            f"{data['title']} — Chang Nie, Zhe Liu, Hesheng Wang, arXiv preprint, "
            f"Shanghai Jiao Tong University, 2026. {url}"]
    return "\n".join(out)


def _write_cite_bib(out, url, data):
    """Export the same arXiv citation displayed on the project page."""
    (out / "cite.bib").write_text(_bibtex(url, data) + "\n", encoding="utf-8")


def _write_citation_cff(out, url, data):
    """CITATION.cff — Citation File Format 1.2.0, for GitHub and reference managers."""
    seo = data["seo"]
    lines = [
        "cff-version: 1.2.0",
        'message: "If you use Teach and Grow (TGL) in your work, please cite the paper."',
        f'title: "{data["title"]}"',
        "type: software",
        "authors:",
    ]
    for name in data["authors"]:
        fam, _, given = name.rpartition(" ")
        lines += [f"  - family-names: {fam}", f"    given-names: {given}",
                  f'    affiliation: "{seo["institution"]}"']
    lines += [
        f'url: "{url}"',
        f'repository-code: "{seo["code_url"]}"',
        "license: Apache-2.0",
        f'date-released: "{seo["paper_date_iso"]}"',
        "preferred-citation:",
        "  type: article",
        f'  title: "{data["title"]}"',
        "  authors:",
    ]
    for name in data["authors"]:
        fam, _, given = name.rpartition(" ")
        lines += [f"    - family-names: {fam}", f'      given-names: {given}']
    lines += [f'  year: {data["year"]}',
              f'  month: {int(seo["paper_date_iso"][5:7])}',
              "  journal: arXiv"]
    if seo.get("doi"):
        lines.append(f'  doi: "{seo["doi"]}"')
    if seo.get("arxiv_id"):
        lines.append(f'  url: "{seo["arxiv_url"]}"')
    (out / "CITATION.cff").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_codemeta(out, url, data):
    """CodeMeta 2.0 software metadata."""
    seo = data["seo"]
    doc = {
        "@context": "https://doi.org/10.5063/schema/codemeta-2.0",
        "@type": "SoftwareSourceCode",
        "name": "Teach and Grow (TGL)",
        "description": ("Reference implementation of Teach-and-Grow Learning, a training-free architecture for "
                        "general robot learning in which a pretrained multimodal agent turns sparse "
                        "demonstrations into reusable Skill Blocks."),
        "codeRepository": seo["code_url"],
        "url": url,
        "license": seo["code_url"],
        "programmingLanguage": ["Python"],
        "datePublished": seo["paper_date_iso"],
        "dateModified": seo.get("updated_iso", seo["paper_date_iso"]),
        "author": [
            {"@type": "Person",
             "givenName": n.rpartition(" ")[2],
             "familyName": n.rpartition(" ")[0],
             "affiliation": {"@type": "Organization", "name": seo["institution"]}}
            for n in data["authors"]
        ],
        "referencePublication": {
            "@type": "ScholarlyArticle",
            "name": data["title"],
            "url": seo.get("arxiv_url", url + "paper/"),
            "sameAs": [u for u in (seo.get("arxiv_url"), seo.get("doi_url")) if u],
            "datePublished": seo["paper_date_iso"],
        },
        "keywords": seo["keywords"],
        "developmentStatus": "active",
    }
    (out / "codemeta.json").write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n",
                                       encoding="utf-8")


# ---------------------------------------------------------------------------
# Derived index pages: /concepts/, /glossary/, /faq/
# ---------------------------------------------------------------------------
def _concept_index(all_pages):
    """Pages that live under /concepts/. The 2026 research map is an article under
    /research/, so it stays out of the concept index and off the glossary path."""
    return [p for p in all_pages if p.get("parent") == "concepts"]


def render_index_pages(url, data, site, all_pages):
    """Build the three pages that aggregate what is already in site.json and pages*.py."""
    from pathlib import Path
    seo = data["seo"]
    concepts = _concept_index(all_pages)
    urls = []

    for lang in ("en", "zh"):
        zh = lang == "zh"
        up = "../" if not zh else "../"

        def T(en_s, cn_s):
            return cn_s if zh else en_s

        # ---- /concepts/ hub ----
        dirs = (["zh"] if zh else []) + ["concepts"]
        items = []
        for c in concepts:
            b = c["zh" if zh else "en"]
            href = _link(dirs, _page_dirs(c, lang), url)
            items.append(f'<li><a href="{href}">{b["h1"]}</a><p>{b["desc"]}</p></li>')
        _write_index_page(
            site, url, data, lang, "concepts",
            T("Concepts — Teach and Grow (TGL)", "概念 — Teach and Grow（TGL）"),
            T("Every concept page for Teach-and-Grow Learning in one place: the paradigm, training-free robot "
              "learning, Skill Blocks, the Skill Library, Experience Memory, the retraining tax, and the wider "
              "research vocabulary around them.",
              "Teach-and-Grow Learning 的全部概念页：范式本身、免训练机器人学习、Skill Block、Skill Library、"
              "Experience Memory、再训练成本，以及围绕它们的研究词汇。"),
            T("Concept index", "概念索引"),
            T("Each page defines one term so it can be quoted or checked on its own, and links to the pages it "
              "relates to.", "每页定义一个术语，便于单独引用或核对，并链接到相关页面。"),
            f'<ul class="concept-index">{"".join(items)}</ul>')
        if zh:
            urls.append(url + "zh/concepts/")
        else:
            urls.append(url + "concepts/")

        # ---- /glossary/ ----
        terms = seo["terms"]
        faq = seo.get("faq", [])
        gl = []
        for t in terms:
            name = t["name_zh"] if zh else t["name"]
            definition = t["definition_zh"] if zh else t["definition"]
            gl.append(f'<div class="glossary-item"><dt>{name}</dt><dd>{definition}</dd></div>')
        for item in faq:
            q = item["q_zh"] if zh else item["q"]
            a = item["a_zh"] if zh else item["a"]
            gl.append(f'<div class="glossary-item"><dt>{q}</dt><dd>{a}</dd></div>')
        _write_index_page(
            site, url, data, lang, "glossary",
            T("Glossary — Teach and Grow (TGL) terminology", "术语表 — Teach and Grow（TGL）术语"),
            T("Definitions of the terms Teach-and-Grow Learning introduces — training-free robot learning, Skill "
              "Block, Skill Library, Experience Memory, retraining tax — each written to stand alone.",
              "Teach-and-Grow Learning 提出术语的定义——免训练机器人学习、Skill Block、Skill Library、"
              "Experience Memory、再训练成本——每条都可独立引用。"),
            "Glossary" if not zh else "术语表",
            T("Definitions are self-contained so they can be quoted, checked or reused without the surrounding "
              "page.", "每条定义都保持自包含，便于单独引用、核对或复用。"),
            f'<dl class="glossary-grid">{"".join(gl)}</dl>')
        urls.append(url + ("zh/" if zh else "") + "glossary/")

        # ---- /faq/ ----
        faqs = list(faq)
        for c in concepts:
            b = c["zh" if zh else "en"]
            for q, a in b.get("faq", []):
                faqs.append({"q": q, "a": a})
        blocks = "".join(
            f'<article class="faq-item"><h3>{f["q_zh"] if zh and "q_zh" in f else f["q"]}</h3>'
            f'<div class="faq-answer"><p>{f["a_zh"] if zh and "a_zh" in f else f["a"]}</p></div></article>'
            for f in faqs)
        _write_index_page(
            site, url, data, lang, "faq",
            T("FAQ — Teach and Grow (TGL)", "常见问题 — Teach and Grow（TGL）"),
            T("Direct answers about Teach-and-Grow Learning: what it is, what training-free means, how it "
              "differs from training a VLA model, what the results are, and how to cite it.",
              "关于 Teach-and-Grow Learning 的直接回答：它是什么、免训练指什么、与训练 VLA 模型有何不同、"
              "结果如何、以及如何引用。"),
            "FAQ" if not zh else "常见问题",
            T("Written to be self-contained so a reader or an AI assistant can quote an answer without the rest "
              "of the site.", "刻意写成自包含的，读者或 AI 助手可以直接引用某条回答，而无需依赖网站其余部分。"),
            f'<div class="faq-list">{blocks}</div>')
        urls.append(url + ("zh/" if zh else "") + "faq/")

    return urls


def _write_index_page(site, url, data, lang, slug, title, desc, h1, lede, body_html):
    """Write one derived index page plus its Markdown mirror."""
    from pathlib import Path
    zh = lang == "zh"
    dirs = (["zh"] if zh else []) + [slug]
    page_url = url + "/".join(dirs) + "/"
    page = {"slug": slug, "parent": "", "en": {"title": title, "desc": desc, "h1": h1, "lede": lede,
                                 "keywords": title, "sections": []},
            "zh": {"title": title, "desc": desc, "h1": h1, "lede": lede,
                   "keywords": title, "sections": []}}
    up = "../" * len(dirs)
    asset = up + "assets/"
    home = up + ("zh/" if zh else "")
    NAVH = "".join(f'<a href="{home}#{a}">{cn if zh else en}</a>' for a, en, cn in NAV)
    other = _link(dirs, ["zh"] + [slug] if not zh else [slug], url)
    html_text = f'''<!doctype html>
<html lang="{'zh-CN' if zh else 'en'}"><head>
{_subpage_head(page, lang, url, data, page_url)}
</head><body data-lang="{lang}">
<header class="site-header"><div class="nav-wrap"><a class="brand" href="{home}" aria-label="Teach and Grow home"><img src="{asset}brand/tgl-logo-v3.png" width="30" height="30" alt=""><span>TGL<span class="brand-dot">.</span></span></a><nav aria-label="Main navigation">{NAVH}</nav><a class="language" href="{other}" lang="{'zh-CN' if not zh else 'en'}">{'中文' if not zh else 'English'} <span aria-hidden="true">↗</span></a></div></header>
<main id="main"><section class="section container subpage">
<nav class="breadcrumb-nav" aria-label="Breadcrumb"><a href="{home}">&larr; {'Teach and Grow' if not zh else 'Teach and Grow 项目主页'}</a></nav>
<h1 class="subpage-title">{h1}</h1>
<p class="lead subpage-lede">{lede}</p>
{body_html}
<div class="subpage-footer"><p>{'机器可读入口' if zh else 'Machine-readable entry points'}:
<a href="{up}llms.txt">llms.txt</a> · <a href="{up}llms-full.txt">llms-full.txt</a> ·
<a href="{up}project.json">project.json</a> · <a href="{up}cite.bib">cite.bib</a> ·
<a href="{up}sitemap.xml">sitemap.xml</a></p></div>
</section></main>
<footer class="container"><a class="brand" href="{home}">TGL<span class="brand-dot">.</span></a><p>Teach and Grow · Shanghai Jiao Tong University</p><a href="#">{'返回顶部' if zh else 'Back to top'} ↑</a></footer>
</body></html>'''
    d = Path(site).joinpath(*dirs)
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(html_text, encoding="utf-8")
    (d / "index.md").write_text(f"# {h1}\n\n> {lede}\n\nSource: {page_url}\n\n{html_to_md(body_html)}\n",
                                encoding="utf-8")


# ---------------------------------------------------------------------------
# Data endpoints: results, page index, related work
# ---------------------------------------------------------------------------
def _write_data_endpoints(out, url, data, sub_urls):
    """JSON/CSV mirrors of the numbers and the page inventory."""
    seo = data["seo"]
    import csv
    import io

    # results.json — the benchmark tables, so a reader never has to scrape HTML
    results = {
        "schema_version": "1.0",
        "updated_at": seo.get("updated_iso", seo["paper_date_iso"]),
        "paper": {"title": data["title"], "arxiv": seo.get("arxiv_id"), "doi": seo.get("doi")},
        "metric": "mean task success rate (%)",
        "benchmarks": {},
    }
    for key, label in (("libero", "LIBERO"), ("plus", "LIBERO-Plus")):
        t = data[key]
        results["benchmarks"][key] = {
            "name": label,
            "columns": t["columns"],
            "rows": [{"method": r[0], **{c: v for c, v in zip(t["columns"], r[1:])}} for r in t["rows"]],
            "tgl_mean": _ours(data, key),
        }
    results["notes"] = (
        "Rows other than TGL are published literature values reproduced for comparison in the paper. Full protocols and per-task tables are in the paper.")
    (out / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # results.csv — one flat table, both benchmarks
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["benchmark", "method"] + list(data["libero"]["columns"]))
    for key, label in (("libero", "LIBERO"), ("plus", "LIBERO-Plus")):
        for row in data[key]["rows"]:
            w.writerow([label, row[0]] + list(row[1:]))
    (out / "results.csv").write_text(buf.getvalue(), encoding="utf-8")

    # page-index.json — what exists and what it is for
    entries = [
        {"url": url, "lang": "en", "title": data["title"], "role": "project page"},
        {"url": url + "zh/", "lang": "zh", "title": data["title"], "role": "project page"},
    ]
    for u in sub_urls:
        rel = u[len(url):].rstrip("/")
        lang = "zh" if rel.startswith("zh/") else "en"
        entries.append({"url": u, "lang": lang, "slug": rel, "role": "generated page"})
    (out / "page-index.json").write_text(json.dumps(
        {"schema_version": "1.0", "updated_at": seo.get("updated_iso", seo["paper_date_iso"]),
         "count": len(entries), "pages": entries}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # related-work.json — neighbouring directions, for entity association
    related = {
        "schema_version": "1.0",
        "updated_at": seo.get("updated_iso", seo["paper_date_iso"]),
        "note": ("Neighbouring research directions, listed so that retrieval systems can associate this work "
                 "correctly. Listing is association, not a priority claim."),
        "paradigm": {"name": "Teach-and-Grow Learning", "abbreviation": "TGL"},
        "directions": [
            {"name": "Vision-language-action models", "abbreviation": "VLA",
             "page": url + "concepts/vla-without-retraining/", "relation": "TGL keeps these frozen"},
            {"name": "World-action models", "abbreviation": "WAM",
             "page": url + "research-context/", "relation": "learned-dynamics alternative"},
            {"name": "Agentic robotics", "page": url + "concepts/agentic-robotics/",
             "relation": "TGL is agent-centered"},
            {"name": "Physical AI / embodied AI", "page": url + "concepts/physical-ai/",
             "relation": "application setting"},
            {"name": "Lifelong / continual robot learning",
             "page": url + "concepts/lifelong-robot-learning/", "relation": "shared goal, different mechanism"},
            {"name": "Few-shot and sparse teaching", "page": url + "concepts/training-free-robot-learning/",
             "relation": "input regime"},
            {"name": "Skill composition and skill libraries",
             "page": url + "concepts/skill-library/", "relation": "shared object of study"},
            {"name": "LLM robotics / GPT robotic arms", "page": url + "concepts/llm-robotics/",
             "relation": "reasoning layer"},
            {"name": "Robot foundation models", "page": url + "concepts/general-robot-learning/",
             "relation": "source of pretrained priors"},
            {"name": "LIBERO / LIBERO-Plus", "abbreviation": "benchmark",
             "page": url + "#results", "relation": "evaluation suite"},
        ],
    }
    # The 2026 query categories: each names the direction and the page that treats it.
    related["categories"] = [
        {"id": "frontier-model-robot-control", "name": "Frontier-model robot control",
         "page": url + "concepts/gpt-6-robotic-arm/",
         "relation_to_tgl": "the reasoning layer TGL leaves frozen"},
        {"id": "agent-as-policy", "name": "Agent as Policy (AGP)",
         "page": url + "concepts/agent-as-policy/",
         "relation_to_tgl": "shared control locus; TGL adds persistence",
         "reference": "Jia et al., arXiv:2609.12541 (2026)"},
        {"id": "coding-agent-robotics", "name": "Coding agents for robotics",
         "page": url + "concepts/coding-agent-robotics/",
         "relation_to_tgl": "the role Codex plays in TGL"},
        {"id": "physical-in-context-learning", "name": "Physical in-context learning",
         "page": url + "concepts/physical-in-context-learning/",
         "relation_to_tgl": "TGL writes the adaptation into stores that outlive the context"},
        {"id": "robot-agent-memory", "name": "Robot agent memory",
         "page": url + "concepts/robot-agent-memory/",
         "relation_to_tgl": "Skill Library plus Experience Memory"},
        {"id": "single-video-robot-learning", "name": "Single-video task acquisition",
         "page": url + "concepts/physical-in-context-learning/",
         "relation_to_tgl": "context supplies structure; TGL supplies the grounded realization"},
        {"id": "agentic-vla", "name": "Agentic VLA",
         "page": url + "concepts/vla-without-retraining/",
         "relation_to_tgl": "TGL keeps the VLA fixed and stores new capability outside it"},
        {"id": "physical-ai-agent", "name": "Physical AI agent",
         "page": url + "concepts/physical-ai/",
         "relation_to_tgl": "application framing"},
    ]
    for d in related["directions"]:
        d.setdefault("categories", [c["id"] for c in related["categories"]
                                    if c["page"] == d.get("page")])
    (out / "related-work.json").write_text(json.dumps(related, ensure_ascii=False, indent=2) + "\n",
                                            encoding="utf-8")

    # /data/ — the 2026 agentic-robotics reading list and the query map.
    _write_agentic_data(out, url)


def _write_agentic_data(out, url):
    """Two JSON files under /data/.

    agentic-robotics-2026.json — the neighbouring work the 2026 pages cite. Every
    arXiv identifier here was resolved against the arXiv API before it was written;
    nothing is inferred from a search snippet or from a document's summary of it.

    search-targets.json — query to landing page, so an assistant that has the query
    can find the page without a site crawl.
    """
    from pathlib import Path
    d = Path(out) / "data"
    d.mkdir(parents=True, exist_ok=True)

    landscape = {
        "schema_version": "1.0",
        "topic": "Agentic robotics, 2026",
        "note": ("Neighbouring directions to this work, with identifiers verified against the arXiv API on "
                 "2026-09-16. Listing is association, not a priority claim, and not a claim that this list is "
                 "complete. Each entry links to the page that discusses it."),
        "hub": url + "research/agentic-robotics-2026/",
        "works": [
            {"name": "Agent as Policy for Robotic Manipulation",
             "abbreviation": "AGP",
             "authors": "Mengzhao Jia, Yang Lin, Xixin Zhang, Zhihan Zhang, Xiaobai Liu, Meng Jiang",
             "date": "2026-09-11",
             "category": ["agent-as-policy", "frontier-model-robot-control", "robot manipulation"],
             "identifier": {"scheme": "arXiv", "value": "2609.12541"},
             "url": "https://arxiv.org/abs/2609.12541",
             "contribution": ("Introduces Agent as Policy: a general-purpose agent drives a physical robot "
                              "through task execution with no task-specific or environment-specific training, "
                              "writing executable programs and revising on physical outcomes."),
             "relation_to_tgl": ("Same control locus — an agent inside the execution loop. TGL adds the "
                                 "persistence layer AGP does not define: a Skill Library and Experience Memory."),
             "page": url + "concepts/agent-as-policy/"},
            {"name": "Revisiting the \"Push-T\" Robot Manipulation Task with Agentic Robotics",
             "authors": "Shuangyu Xie, Kaiyuan Chen, Ken Goldberg",
             "date": "2026-08-18",
             "category": ["coding-agent-robotics", "agent-as-policy"],
             "identifier": {"scheme": "arXiv", "value": "2608.18227"},
             "url": "https://arxiv.org/abs/2608.18227",
             "contribution": ("An LLM coding agent is prompted to write a solution to Push-T with no "
                              "demonstration data; the resulting code-as-policy is compared with a visuomotor "
                              "imitation-learning policy."),
             "relation_to_tgl": ("Evidence for the coding-agent-for-robots pattern TGL uses via Codex, and a "
                                 "direct comparison between a written program and a learned policy."),
             "page": url + "concepts/coding-agent-robotics/"},
            {"name": "Agentic Robot: A Brain-Inspired Framework for Vision-Language-Action Models in Embodied Agents",
             "authors": "Zhejian Yang, Yongchao Chen, Xueyang Zhou, Jiangyue Yan, Dingjie Song, Yinuo Liu, Yuting Li, Yu Zhang, Pan Zhou",
             "date": "2025-05-29",
             "category": ["agentic-vla", "agent-as-policy"],
             "identifier": {"scheme": "arXiv", "value": "2505.23450"},
             "url": "https://arxiv.org/abs/2505.23450",
             "contribution": ("A coordination protocol (Standardized Action Procedure) for vision-language-action "
                              "components, aimed at error accumulation and missing verification in long-horizon "
                              "manipulation."),
             "relation_to_tgl": ("Shares the diagnosis that execution needs verification. TGL makes the effect "
                                 "check part of each Skill Block's contract rather than a layer around the policy."),
             "page": url + "concepts/agent-as-policy/"},
            {"name": "Code as Policies: Language Model Programs for Embodied Control",
             "authors": "Jacky Liang, Wenlong Huang, Fei Xia, Peng Xu, Karol Hausman, Brian Ichter, Pete Florence, Andy Zeng",
             "date": "2022-09-16",
             "category": ["coding-agent-robotics", "frontier-model-robot-control"],
             "identifier": {"scheme": "arXiv", "value": "2209.07753"},
             "url": "https://arxiv.org/abs/2209.07753",
             "project_url": "https://code-as-policies.github.io/",
             "contribution": "The program-as-policy predecessor: a language model writes policy code over supplied perception primitives.",
             "relation_to_tgl": "The lineage TGL's Codex role descends from; TGL adds validation and persistence around the written program.",
             "page": url + "concepts/coding-agent-robotics/"},
            {"name": "Do As I Can, Not As I Say: Grounding Language in Robotic Affordances",
             "authors": "Michael Ahn et al.",
             "date": "2022-04-04",
             "category": ["frontier-model-robot-control"],
             "identifier": {"scheme": "arXiv", "value": "2204.01691"},
             "url": "https://arxiv.org/abs/2204.01691",
             "project_url": "https://say-can.github.io/",
             "contribution": "Grounds language-model plans in the affordances of the robot that will execute them.",
             "relation_to_tgl": "The planning-side predecessor; TGL's grounding happens per subgoal against the current scene.",
             "page": url + "concepts/agent-as-policy/"},
            {"name": "ReKep: Spatio-Temporal Reasoning of Relational Keypoint Constraints for Robotic Manipulation",
             "authors": "Wenlong Huang, Chen Wang, Yunzhu Li, Ruohan Zhang, Li Fei-Fei",
             "date": "2024-09-03",
             "category": ["frontier-model-robot-control", "agent-as-policy"],
             "identifier": {"scheme": "arXiv", "value": "2409.01652"},
             "url": "https://arxiv.org/abs/2409.01652",
             "contribution": "Represents manipulation as relational keypoint constraints and solves them in a closed loop.",
             "relation_to_tgl": "A different route to closed-loop reliability: constraints rather than validated reusable blocks.",
             "page": url + "concepts/agent-as-policy/"},
        ],
        "excluded": ("Several widely-circulated 2026 items are omitted because they could not be resolved to a "
                     "verifiable primary source at the time of writing. They are not listed speculatively."),
    }
    (d / "agentic-robotics-2026.json").write_text(
        json.dumps(landscape, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def target(query, slug, note):
        return {"query": query, "url": url + slug, "note": note}

    targets = {
        "schema_version": "1.0",
        "updated_at": "2026-09-16",
        "note": ("Search queries this site is written to answer, mapped to the page that answers them. "
                 "Intended for assistants that receive a query and want the right page directly."),
        "targets": [
            target("GPT-6 robot arm", "concepts/gpt-6-robotic-arm/",
                   "GPT-6-class models used as a reasoning layer for robot-arm manipulation; TGL uses GPT-6 Astra."),
            target("GPT-6 robotic arm", "concepts/gpt-6-robotic-arm/", "Variant phrasing of the above."),
            target("GPT-6 Astra robot", "concepts/gpt-6-robotic-arm/",
                   "The specific model TGL's implementation uses."),
            target("agent as policy robotics", "concepts/agent-as-policy/",
                   "AGP: the agent inside the execution loop, per arXiv:2609.12541."),
            target("agent as policy definition", "concepts/agent-as-policy/",
                   "Short answer plus current examples and a comparison with TGL."),
            target("coding agent robotics", "concepts/coding-agent-robotics/",
                   "Coding agents writing and running robot programs; Codex in TGL."),
            target("physical in-context learning robotics", "concepts/physical-in-context-learning/",
                   "Adapting a robot from context without updating weights."),
            target("general-purpose agent robot", "concepts/general-purpose-agent-robot/",
                   "One agent across many tasks, and what it fails to retain."),
            target("robot agent memory", "concepts/robot-agent-memory/",
                   "What a robot should keep from an interaction; Skill Library vs Experience Memory."),
            target("robot learning without retraining", "concepts/no-retraining-robot-learning/",
                   "Acquiring tasks with frozen weights; the retraining tax."),
            target("AI agent robotic arm", "concepts/ai-agent-robotic-arm/",
                   "An AI agent driving a robot arm end to end."),
            target("runtime reasoning robotics", "concepts/runtime-reasoning-robotics/",
                   "Deciding while the task is running rather than before it."),
            target("tool use robotics", "concepts/tool-use-robotics/",
                   "Exposing perception, grasping and motion as callable tools for an agent."),
            target("train a robot from one video", "concepts/physical-in-context-learning/",
                   "What a single video can and cannot supply; the single-video case of in-context adaptation."),
            target("agentic robotics 2026", "research/agentic-robotics-2026/",
                   "The research map: frontier models, AGP, coding agents, physical ICL, memory, and where TGL fits."),
            target("teach and grow robot learning", "concepts/teach-and-grow-learning/",
                   "The TGL paradigm itself."),
            target("training-free robot learning", "concepts/training-free-robot-learning/",
                   "What training-free means here and what it does not mean."),
            target("skill library robot", "concepts/skill-library/",
                   "The persistent store of validated Skill Blocks."),
        ],
    }
    (d / "search-targets.json").write_text(
        json.dumps(targets, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"  wrote data/agentic-robotics-2026.json ({len(landscape['works'])} works) "
          f"and data/search-targets.json ({len(targets['targets'])} queries)")


def _knowledge_base(url, data):
    """A structured knowledge base, then the full page text follows."""
    seo = data["seo"]
    out = []
    A = out.append

    def sec(h, body):
        A(f"\n{h}\n")
        if body:
            A(body.strip() + "\n")

    sec("# Canonical Identity", f'''Title: {data["title"]}
Short name: TGL
Expanded name: Teach-and-Grow Learning
Authors: {", ".join(data["authors"])}
Institution: {seo["institution"]} ({seo["lab"]})
Project: {url}
Paper page: {url}paper/
Code: {seo["code_url"]}''')

    meta = [f"arXiv: {seo['arxiv_id']}" if seo.get("arxiv_id") else None,
            f"arXiv URL: {seo['arxiv_url']}" if seo.get("arxiv_url") else None,
            f"DOI: {seo['doi']}" if seo.get("doi") else None,
            f"Published: {seo['paper_date_iso']}",
            f"Type: {seo['paper_type']}",
            "Status: no venue acceptance claimed"]
    sec("# Paper Metadata", "\n".join(m for m in meta if m))

    sec("# Abstract", seo["abstract"])
    sec("# 摘要", seo.get("abstract_zh", ""))

    problem = data["libero"]
    sec("# Research Problem", f'''General robot learning aims for one system that handles many tasks and scenes. End-to-end
vision-language-action and world-action models pursue it by absorbing each new capability into policy parameters, which
requires new robot data, optimisation, and regression checking against everything already supported. The paper names
this recurring cost the retraining tax. Physical interaction data is expensive in a way text and code are not: it has to
be created by operating a machine.''')
    sec("## The Retraining Tax",
        "The recurring cost of repairing robot behaviour through a policy update: new data collection, optimisation, and "
        "regression checking against previously supported behaviour. It becomes most visible in the long tail, where a "
        "specific lesson is needed rather than another broad round of experience.")

    sec("# Architecture", """TGL holds the pretrained stack fixed and stores new capability in two explicit, inspectable
places. The agent reads the scene, chooses a subgoal and a tool, observes the physical outcome, and revises the
remaining plan.""")
    sec("## Multimodal Agent",
        "Task-level reasoning and tool interaction. The paper's implementation uses OpenAI GPT-6 Astra, with Codex "
        "connecting the agent to the robot tools.")
    sec("## Skill Blocks",
        "The unit of reusable behaviour: a goal, a reusable strategy, supported conditions, compatible executors, and an "
        "outcome test. The semantic effect is retained; object bindings, grasp geometry and collision-free motion are "
        "recomputed from the current scene.")
    sec("## Skill Library",
        "The persistent store of validated Skill Blocks with their scopes and contracts. It grows when a candidate "
        "passes validation on cases kept separate from the teaching demonstrations, not every episode.")
    sec("## Experience Memory",
        "The contextual store: task, selected blocks, observations, outcome, diagnosis and repair. It informs the next "
        "retrieval and recovery without turning every episode into a new executable block.")
    sec("## Physical Feedback Loop",
        "Execution checks the required effect before allowing the next stage. A passed effect advances the plan; a "
        "failed or inconclusive one prompts another observation, a different executor, or a revised route.")
    sec("## Teaching and Growing",
        "Teaching supplies the subgoal structure and the conditions worth checking. Growing is what gathers into the "
        "library and memory, so a later task starts from a larger base of inspectable capability.")

    sec("# Evaluation", f'''Benchmark suites: LIBERO (four suites) and LIBERO-Plus (seven perturbation categories).
Simulation only; the page presents five qualitative paired demonstrations.''')
    sec("## Main Results", f'''TGL mean success: {_ours(data, "libero")}% on LIBERO (columns: {", ".join(data["libero"]["columns"])}).
TGL mean success: {_ours(data, "plus")}% on LIBERO-Plus (columns: {", ".join(data["plus"]["columns"])}).
Machine-readable: {url}results.json and {url}results.csv. Full tables are in the paper.''')
    sec("## Controlled Studies",
        "The paper describes studies on skill induction, persistence across episodes, agent-directed adaptation under "
        "physical feedback, and library growth affecting related-task execution with the same weights and executors.")

    sec("# Scaling Law Hypothesis",
        "The paper proposes — as a hypothesis to be tested over sequential acquisition experiments, not as a fitted "
        "law — that effective reusable experience X relates to falling future-task error and falling teaching demand, "
        "both approaching irreducible floors as power laws in X.")

    sec("# 2026 Agentic Robotics Research Landscape",
        "In 2026 frontier multimodal models became usable as a reasoning layer for physical manipulation, and "
        "attention moved from \"can a model produce an action?\" to \"what does the robot retain?\". The pages "
        "below map that landscape and place TGL in it. The research map is at "
        f"{url}research/agentic-robotics-2026/; a machine-readable reading list with verified arXiv identifiers "
        f"is at {url}data/agentic-robotics-2026.json.")

    sec("# TGL and GPT-6-Class Robot Agents",
        "GPT-6-class systems are used as a reasoning layer that interprets visual observations and invokes "
        "robot-control tools or generated programs, rather than emitting joint commands. TGL's implementation "
        f"uses OpenAI GPT-6 Astra in that role. See {url}concepts/gpt-6-robotic-arm/.")
    sec("# TGL and Agent-as-Policy Robotics",
        "Agent as Policy (AGP) places a general-purpose agent inside the execution loop rather than limiting it "
        "to offline planning. Jia et al., arXiv:2609.12541 (2026), named and demonstrated it. TGL shares the "
        "control locus and adds persistence: validated behaviour enters a Skill Library, and outcome, diagnosis "
        f"and repair enter Experience Memory. See {url}concepts/agent-as-policy/.")
    sec("# TGL and Coding Agents for Robots",
        "Coding agents inspect state, call tools, write and run short programs, and read the result — a good fit "
        "for the boundary between a frontier model and a robot's control stack. Codex plays this role in TGL. The "
        "lineage runs through Code as Policies (Liang et al., arXiv:2209.07753); a 2026 example is Xie, Chen and "
        f"Goldberg, arXiv:2608.18227. See {url}concepts/coding-agent-robotics/.")
    sec("# TGL and Physical In-Context Learning",
        "Physical in-context learning lets a robot adapt to a new task from context such as demonstrations or "
        "video without updating model weights. TGL complements it by storing reusable behaviour and structured "
        f"physical experience persistently, so learning accumulates across tasks. See {url}concepts/physical-in-context-learning/.")
    sec("# TGL and Single-Video Robot Learning",
        "The minimal case: one video, no teleoperation, no policy training. A video usually reveals the order of "
        "operations while leaving the grasp unresolved — the same distinction TGL preserves between semantic "
        f"structure and robot-specific grounding. See {url}concepts/physical-in-context-learning/.")
    sec("# TGL and Robot Agent Memory",
        "Robot-agent memory preserves information from earlier physical interaction for future decisions. In TGL "
        "the split is explicit: the Skill Library holds reusable executable behaviour, while Experience Memory "
        f"carries forward success, failure, diagnosis and repair. See {url}concepts/robot-agent-memory/.")
    sec("# TGL and Runtime Physical Reasoning",
        "The deciding component stays running while the task executes, so it can act on evidence that only exists "
        "during execution. TGL gives it something to reason over: each Skill Block has an outcome test, and its "
        f"result is what the agent reads. See {url}concepts/runtime-reasoning-robotics/.")
    sec("# TGL and Tool-Using Robot Agents",
        "Perception, grasping, motion and control are exposed as callable tools with documented effects, so the "
        "agent decides what should happen while geometry and control stay in specialist components. A Skill Block "
        f"declares which executors can realize it and what evidence counts as success. See {url}concepts/tool-use-robotics/.")
    sec("# TGL and Frontier-Model Robotic Manipulation",
        "Frontier models supply the reasoning; TGL changes where a newly acquired capability is stored, so a "
        "repair is local rather than a policy-wide update. Robot learning without task-specific retraining is "
        f"the claim: see {url}concepts/no-retraining-robot-learning/.")

    sec("# Research Context", seo.get("context", ""))
    for label, slug in (("## TGL and Agentic Robotics", "agentic-robotics"),
                        ("## TGL and General Robot Learning", "general-robot-learning"),
                        ("## TGL and Vision-Language-Action Models", "vla-without-retraining"),
                        ("## TGL and Lifelong Robot Learning", "lifelong-robot-learning"),
                        ("## TGL and Physical AI / Embodied AI", "physical-ai"),
                        ("## TGL and LLM / GPT Robotics", "llm-robotics")):
        sec(label, f"See {url}concepts/{slug}/ for the full treatment.")

    A("\n# Glossary\n")
    for t in seo["terms"]:
        A(f"- **{t['name']}** ({t['name_zh']}): {t['definition']}")
    A("\n# FAQ\n")
    for item in seo.get("faq", []):
        A(f"**{item['q']}**\n\n{item['a']}\n")

    sec("# Canonical URLs", "\n".join([
        f"Project (en): {url}", f"Project (zh): {url}zh/",
        f"Paper: {url}paper/", f"Research context: {url}research-context/",
        f"Concepts hub: {url}concepts/", f"Glossary: {url}glossary/", f"FAQ: {url}faq/",
        f"Agentic robotics 2026: {url}research/agentic-robotics-2026/",
        f"Reading list: {url}data/agentic-robotics-2026.json", f"Query map: {url}data/search-targets.json",
        f"Machines: {url}llms.txt · {url}llms-full.txt · {url}project.json · {url}results.json · "
        f"{url}page-index.json · {url}related-work.json · {url}sitemap.xml · {url}cite.bib · "
        f"{url}CITATION.cff · {url}codemeta.json · {url}robots.txt",
    ]))
    sec("# Citation", f'''Chang Nie, Zhe Liu and Hesheng Wang, “Teach and Grow: An Agent-Centered Architecture for
General Robot Learning,” arXiv:{seo.get("arxiv_id", "")}, {data["year"]}. DOI: {seo.get("doi", "")}.
BibTeX: {url}cite.bib (key {seo["bibtex_key"]}).''')
    return out
