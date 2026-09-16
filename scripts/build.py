#!/usr/bin/env python3
"""Dependency-free static build for GitHub Pages and a future custom domain."""
import argparse
import html
import json
from pathlib import Path
import shutil
from research import sections
from seo import head_seo, write_crawler_files, html_to_md, render_subpage
import pages as PAGES
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'content/site.json').read_text())
CONFIG = json.loads((ROOT / 'deployment.json').read_text())
IMAGE_SIZES = json.loads((ROOT / 'content/image-sizes.json').read_text())
parser = argparse.ArgumentParser()
parser.add_argument('--url', default=CONFIG['url'])
parser.add_argument('--custom-domain', default=CONFIG['custom_domain'])
parser.add_argument('--out', default='dist')
args = parser.parse_args()
url = args.url.rstrip('/') + '/'
parts = urlsplit(url)
if parts.scheme not in ('http', 'https') or not parts.netloc:
    raise SystemExit('--url must be an absolute HTTP(S) URL')
# On github.io, the first path component is the repository prefix, not an artifact directory.
segments = [s for s in parts.path.split('/') if s]
if parts.hostname.endswith('.github.io') and segments:
    segments = segments[1:]
if any(s in ('.', '..') for s in segments):
    raise SystemExit('Invalid site path')
out = ROOT / args.out
if out.resolve() == ROOT or ROOT not in out.resolve().parents:
    raise SystemExit('Output must be a child directory')
if out.exists():
    shutil.rmtree(out)
site = out.joinpath(*segments)
site.mkdir(parents=True)
shutil.copytree(ROOT / 'assets', site / 'assets')
e = html.escape

def page(lang):
    zh = lang == 'zh'
    def t(en, cn): return cn if zh else en
    asset = '../assets/' if zh else 'assets/'
    base = '../' if zh else ''
    page_url = url + ('zh/' if zh else '')
    paper = asset + 'paper/teach-and-grow.pdf'
    def figure(num, alt, caption, cls=''):
        width, height = IMAGE_SIZES[f'fig{num}']
        return f'''<figure class="paper-figure {cls}"><a class="zoom" href="{asset}figures/fig{num}.webp" aria-label="{t('Enlarge figure: ', '放大图片：')}{e(alt)}"><img src="{asset}figures/fig{num}.webp" alt="{e(alt)}" width="{width}" height="{height}" loading="lazy" decoding="async"><span class="zoom-label">↗ {t('Enlarge', '放大')}</span></a><figcaption>{caption}</figcaption></figure>'''
    videos = ''
    for i,v in enumerate(DATA['videos']):
        vi = int(zh)
        pair = ''
        for role in ('teacher','system'):
            name = v['id'] + '_' + role
            label = t('Teacher demonstration','教师演示') if role == 'teacher' else t('Teach and Grow · ours','Teach and Grow · 我们的方法')
            pair += f'''<div class="video-pane {role}"><div class="video-label"><span class="status-dot"></span>{label}</div><video controls playsinline muted preload="none" poster="{asset}posters/{name}.webp" aria-label="{e(v['task'][vi])} — {label}"><source src="{asset}videos/{name}.mp4" type="video/mp4">{t('Your browser does not support embedded video.', '你的浏览器不支持内嵌视频。')} <a href="{asset}videos/{name}.mp4">MP4</a></video></div>'''
        videos += f'''<article class="demo-card" data-suite="{v['suite']}" id="demo-{i+1}"><div class="demo-heading"><div><p class="eyebrow">{v['suite'].upper()} <span>/{i+1:02d}</span></p><h3>{v['title'][vi]}</h3><p class="task-name">{v['task'][vi]}</p></div><span class="tag">{v['tag'][vi]}</span></div><div class="video-pair">{pair}</div><div class="pair-controls" hidden><button class="pair-play" type="button">▶ {t('Play both','同时播放')}</button><button class="pair-restart" type="button">↺ {t('Restart','重新播放')}</button><label>{t('Speed','速度')} <select class="pair-speed" aria-label="{t('Playback speed','播放速度')}"><option value="0.5">0.5×</option><option value="1" selected>1×</option><option value="2">2×</option></select></label></div><p>{v['description'][vi]}</p><p class="watch-note"><strong>{t('Watch for:','观察重点：')}</strong> {v['watch'][vi]}</p><p class="play-status" role="status"></p></article>'''
    bib = f'''@techreport{{nie2026teachandgrow,
  title = {{{DATA['title']}}},
  author = {{Nie, Chang and Liu, Zhe and Wang, Hesheng}},
  institution = {{Shanghai Jiao Tong University}},
  year = {{2026}},
  url = {{{url}}}
}}'''
    narrative = sections(t, figure, paper, DATA)
    nav = [("overview",t("Problem","问题")),("origins",t("Research path","研究路线")),("idea",t("Idea","思路")),("method",t("Method","方法")),("demos",t("Videos","演示")),("resources",t("Paper","论文")),("glossary",t("Terms","术语")),("faq",t("FAQ","问答"))]
    nav_html = ''.join(f'<a href="#{a}">{b}</a>' for a,b in nav)
    return f'''<!doctype html>
<html lang="{t('en','zh-CN')}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
{head_seo(lang, url, DATA)}
<meta name="theme-color" content="#155e59"><meta name="color-scheme" content="light">
<link rel="icon" type="image/png" href="{asset}brand/tgl-logo-v3.png"><link rel="icon" href="{'../' if zh else ''}favicon.ico" sizes="any"><link rel="stylesheet" href="{asset}style.css?v=brand6"><script src="{asset}app.js?v=brand6" defer></script>
</head><body data-lang="{lang}"><a class="skip-link" href="#main">{t('Skip to content','跳至正文')}</a>
<header class="site-header"><div class="nav-wrap"><a class="brand" href="#" aria-label="Teach and Grow home"><img src="{asset}brand/tgl-logo-v3.png" width="30" height="30" alt=""><span>TGL<span class="brand-dot">.</span></span></a><nav aria-label="{t('Main navigation','主导航')}">{nav_html}</nav><a class="language" href="{'../' if zh else 'zh/'}" lang="{t('zh-CN','en')}">{t('中文','English')} <span aria-hidden="true">↗</span></a></div></header>
<main id="main">
<section class="hero research-hero"><div class="container"><p class="eyebrow hero-kicker">{t('AGENT-CENTERED ROBOT LEARNING / SHANGHAI JIAO TONG UNIVERSITY','以智能体为中心的机器人学习 / 上海交通大学')}</p><div class="hero-caption"><span class="signal-dot"></span>{t('AI-agent robot learning · GPT-6 Astra + Codex','基于 AI Agent 的机器人学习 · GPT-6 Astra + Codex')}</div><h1>Teach <em>and</em> Grow<span class="title-period">.</span></h1><p class="paper-subtitle">An Agent-Centered Architecture<br class="desktop-break"> for General Robot Learning</p><p class="authors"><a href="https://changnie.top" target="_blank" rel="noopener" aria-label="Chang Nie — personal homepage">Chang Nie ↗</a><span>·</span>Zhe Liu<span>·</span><a href="mailto:wanghesheng@sjtu.edu.cn">Hesheng Wang</a></p><p class="affiliation">{t('School of Automation and Intelligent Sensing, Shanghai Jiao Tong University','上海交通大学 自动化与感知学院')}</p><p class="hero-summary">{t('A few demonstrations become reusable robot skills,<br>with model weights that never change.','少量演示变成可复用的机器人技能，<br>而模型权重始终不变。')}</p><div class="hero-links"><a class="button primary" href="#overview">{t('Explore the idea','了解研究思路')} ↓</a><a class="button" href="{paper}" target="_blank" rel="noopener">{t('Read the paper','阅读论文')} ↗</a><a class="button" href="https://github.com/IRMVLab/TGL" target="_blank" rel="noopener">{t("Code · GitHub","代码 · GitHub")} ↗</a><a class="button text-button" href="#demos">▷ {t('Watch demonstrations','观看演示')}</a></div><div class="hero-system" aria-label="{t('Teaching feeds agent-led Skill Blocks, whose verified outcomes grow the library and experience memory','示教形成智能体主导的技能块，经过验证的结果进入技能库与经验记忆')}"><div class="system-node"><span>01 / TEACH</span><b>{t('Sparse demonstrations','少量演示')}</b><small>{t('Subgoals & shared structure','子目标与共同结构')}</small></div><span class="system-arrow" aria-hidden="true">→</span><div class="system-node node-core"><span>02 / ACT + VERIFY</span><b>{t('Agent + Skill Blocks','Agent + Skill Blocks')}</b><small>{t('Grounded in physical feedback','以物理反馈形成闭环')}</small></div><span class="system-arrow" aria-hidden="true">→</span><div class="system-node"><span>03 / GROW</span><b>{t('Skills + experience','技能与经验')}</b><small>{t('Retained for the next task','用于下一个任务')}</small></div><div class="system-return"><span>↖</span> {t('Reusable knowledge returns to the next decision','可复用知识回到下一次决策')} <span>↵</span></div></div><div class="hero-bottom"><span>PRETRAINED WEIGHTS / FIXED</span><span>EXECUTABLE EXPERIENCE / EVOLVING</span></div></div></section>
<figure class="project-cover container"><a class="zoom" href="{asset}brand/tgl-cover-v4.png" aria-label="{t('Enlarge project cover','放大项目封面')}"><img src="{asset}brand/tgl-cover-v4.png" width="1672" height="941" alt="{t('Conceptual cover: a Franka robot places a plush toy into a bowl in a changed scene; a few demonstrations and agent guidance contrast with VLA/WAM data and training costs','概念封面：Franka 机器人在变化的场景中将毛绒玩具放入碗中；少量示教与智能体指导，对照 VLA/WAM 的数据和训练成本')}" fetchpriority="high"><span class="zoom-label">↗ {t('Enlarge','放大')}</span></a><figcaption>{t('New scenes, reusable skills: sparse teaching and agent-guided execution with fixed model weights. Conceptual artwork.','场景变化，技能复用：通过少量示教与智能体指导，在模型权重固定的条件下适应任务。概念封面。')}</figcaption></figure>
{narrative['abstract']}
{narrative['overview']}
{narrative['origins']}
{narrative['idea']}
{narrative['method']}
{narrative['memory']}
<section id="demos" class="section container"><div class="section-intro"><p class="eyebrow">06 / {t('BEHAVIOR IN CONTEXT','场景中的行为')}</p><h2>{t('Learn the task. Adapt the execution.','理解任务，灵活执行。')}</h2><p class="lead">{t('Five paired LIBERO demonstrations put the teacher’s example next to Teach and Grow on the same task. Three suite families appear here: Object tasks (place a named object in a basket), Spatial tasks (place one object in relation to another), and Goal tasks (bring about a state, such as turning on the stove).','五组 LIBERO 视频把教师演示与 Teach and Grow 放在同一任务上对照，覆盖三类套件：Object（把指定物体放入篮子）、Spatial（把物体放到与另一物体的空间关系中）与 Goal（达成某个状态，例如打开炉灶）。')}</p></div><div class="demo-toolbar"><div class="filters" role="group" aria-label="{t('Filter demonstrations','筛选演示')}" hidden><button class="active" data-filter="All" aria-pressed="true">{t('All five','全部五组')}</button><button data-filter="Object" aria-pressed="false">Object</button><button data-filter="Spatial" aria-pressed="false">Spatial</button><button data-filter="Goal" aria-pressed="false">Goal</button></div><span class="small">{t('Teacher ← → TGL · videos play on request','左：教师 · 右：TGL · 点击播放')}</span></div><p class="small demo-note">{t('Qualitative simulation examples. Clips have different durations; joint playback starts them together without aligning individual actions. Playback speed refers to the supplied videos, not measured robot latency.','这些是仿真中的定性示例。视频时长不同，同时播放只统一起点，不对齐具体动作；播放倍速针对原视频，不代表实测机器人延迟。')}</p><div class="demo-grid">{videos}</div></section>
{narrative['investigation']}
{narrative['growth']}
<section id="resources" class="section resources soft"><div class="container"><div class="resource-top"><div><p class="eyebrow">09 / {t('PAPER & RESOURCES','论文与资源')}</p><h2>{t('Read the full paper.','阅读全文。')}</h2><p>{t('The technical report covers the formulation, the Skill Block contract, the LIBERO and LIBERO-Plus evaluations, the controlled studies, and the scaling hypothesis, with appendices on cost regimes and experimental details.','技术报告包含问题定义、Skill Block 契约、LIBERO 与 LIBERO-Plus 评测、受控研究以及缩放假设，并在附录中给出成本模型与实验细节。')}</p></div><a class="button primary" href="{paper}" target="_blank" rel="noopener">{t('Open paper · PDF','打开论文 · PDF')} ↗</a></div><div class="resource-links"><a href="https://github.com/IRMVLab/TGL" target="_blank" rel="noopener">{t("Method code · IRMVLab/TGL","方法代码 · IRMVLab/TGL")} ↗</a><a href="#demos">{t('10 demonstration videos','10 段演示视频')} ↗</a><a href="https://github.com/biubiu3/tgl-web" target="_blank" rel="noopener">{t('Website source','网页源码')} ↗</a><a href="https://changnie.top" target="_blank" rel="noopener">{t("Chang Nie · Personal homepage","聂畅 · 个人主页")} ↗</a><a href="mailto:changniep@gmail.com">{t('Contact the authors','联系作者')} ↗</a></div><p class="small">{t('The method implementation is maintained in IRMVLab/TGL. Installation and execution instructions are in its README.','方法实现在 IRMVLab/TGL 仓库维护，安装与运行说明请见该仓库 README。')}</p><div class="citation" id="citation"><div><h3>BibTeX</h3><button id="copy-citation" type="button" hidden>{t('Copy citation','复制引用')}</button></div><pre><code id="bibtex">{e(bib)}</code></pre><span id="copy-status" role="status"></span></div></div></section>
{narrative['glossary']}
{narrative['faq']}
</main><footer class="container"><a class="brand" href="#">TGL<span class="brand-dot">.</span></a><p>Teach and Grow · Shanghai Jiao Tong University<br><span>{t('Project images and demonstration videos are hosted with this website.','项目图片与演示视频均由本站提供。')}</span></p><a href="#">{t('Back to top','返回顶部')} ↑</a><nav class="footer-index footer-pages" aria-label="{t('Related pages','相关页面')}"><a href="{base}paper/">{t('Paper record','论文著录')}</a><a href="{base}research-context/">{t('Research context','技术定位')}</a><a href="{base}concepts/teach-and-grow-learning/">{t('Teach-and-Grow Learning','Teach-and-Grow Learning')}</a><a href="{base}concepts/training-free-robot-learning/">{t('Training-free robot learning','免训练机器人学习')}</a><a href="{base}concepts/skill-block/">{t('Skill Block','Skill Block')}</a><a href="{base}concepts/skill-library/">{t('Skill Library','Skill Library')}</a><a href="{base}concepts/experience-memory/">{t('Experience Memory','Experience Memory')}</a><a href="{base}concepts/retraining-tax/">{t('Retraining tax','再训练成本')}</a></nav><nav class="footer-index" aria-label="{t('Machine-readable entry points','机器可读入口')}"><a href="{base}llms.txt">llms.txt</a><a href="{base}llms-full.txt">llms-full.txt</a><a href="{base}project.json">project.json</a><a href="{base}sitemap.xml">sitemap.xml</a><a href="{base}robots.txt">robots.txt</a><a href="{base}{'' if zh else 'zh/'}" lang="{t('zh-CN','en')}">{t('中文版','English')}</a></nav></footer><dialog id="image-dialog" aria-label="{t('Enlarged research image','放大的研究图片')}"><button class="dialog-close" aria-label="{t('Close image','关闭图片')}">×</button><img alt=""><p></p></dialog>
</body></html>'''

EN_HTML = page('en')
(site/'index.html').write_text(EN_HTML)
(site/'zh').mkdir()
ZH_HTML = page('zh')
(site/'zh/index.html').write_text(ZH_HTML)
rendered = {
    'en': {'html': EN_HTML, 'md': html_to_md(EN_HTML)},
    'zh': {'html': ZH_HTML, 'md': html_to_md(ZH_HTML)},
}
# A project root redirects to the requested /tgl/ review route.
if site != out:
    target = '/'.join(segments) + '/'
    (out/'index.html').write_text(f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Teach and Grow</title><meta http-equiv="refresh" content="0;url={target}"><link rel="canonical" href="{url}"><p><a href="{target}">Continue to Teach and Grow →</a></p></html>')
(out/'404.html').write_text(f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found · TGL</title><style>body{{font:20px system-ui;max-width:640px;margin:15vh auto;padding:24px;color:#173d37}}a{{color:#155e59}}</style><h1>Page not found</h1><p>The page may have moved.</p><a href="{url}">Return to Teach and Grow →</a></html>')
(out/'.nojekyll').touch()
# Generated sub-pages: /paper/, /research-context/, /concepts/<slug>/, and /zh/ equivalents.
SUBPAGES = [PAGES.PAPER, PAGES.RESEARCH_CONTEXT] + PAGES.CONCEPTS
SUB_URLS = []
for _pg in SUBPAGES:
    for _lang in ("en", "zh"):
        SUB_URLS.append(render_subpage(_pg, _lang, url, DATA, site))
print(f'  wrote {len(SUB_URLS)} sub-pages')

write_crawler_files(out, url, DATA, rendered, SUB_URLS)
# Browsers and some crawlers probe /favicon.ico directly.
shutil.copy2(ROOT/'assets/favicon.ico', out/'favicon.ico')
if args.custom_domain:
    if '/' in args.custom_domain or args.custom_domain != parts.hostname:
        raise SystemExit('Custom domain must match the hostname in --url')
    (out/'CNAME').write_text(args.custom_domain+'\n')
print(f'Built {site.relative_to(ROOT)} → {url} (English + Chinese)')
