#!/usr/bin/env python3
"""Dependency-free static build for GitHub Pages and a future custom domain."""
import argparse
import html
import json
from pathlib import Path
import shutil
from research import sections
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
    narrative = sections(t, figure, paper)
    nav = [("overview",t("Problem","问题")),("origins",t("Research path","研究路线")),("idea",t("Idea","思路")),("method",t("Method","方法")),("demos",t("Videos","演示")),("resources",t("Paper","论文"))]
    nav_html = ''.join(f'<a href="#{a}">{b}</a>' for a,b in nav)
    description=t('Training-free robot learning from sparse teaching. Reusable Skill Blocks, agent-led execution, and physical feedback turn demonstrations into lasting capability.','通过少量示教学会新任务，无需微调模型。Teach and Grow 将演示转化为可复用技能，以智能体决策和物理反馈实现机器人能力积累。')
    return f'''<!doctype html>
<html lang="{t('en','zh-CN')}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Teach and Grow · {t('Training-free Robot Learning','无需训练的机器人学习')}</title>
<meta name="description" content="{description}"><meta name="theme-color" content="#155e59"><meta name="color-scheme" content="light">
<link rel="canonical" href="{page_url}"><link rel="alternate" hreflang="en" href="{url}"><link rel="alternate" hreflang="zh-CN" href="{url}zh/"><link rel="alternate" hreflang="x-default" href="{url}">
<meta property="og:type" content="article"><meta property="og:title" content="Teach and Grow"><meta property="og:description" content="{description}"><meta property="og:url" content="{page_url}"><meta property="og:image" content="{url}assets/figures/fig1.webp"><meta name="twitter:card" content="summary_large_image">
<meta name="citation_title" content="{e(DATA['title'])}"><meta name="citation_author" content="Nie, Chang"><meta name="citation_author" content="Liu, Zhe"><meta name="citation_author" content="Wang, Hesheng"><meta name="citation_publication_date" content="2026"><meta name="citation_pdf_url" content="{url}assets/paper/teach-and-grow.pdf">
<link rel="icon" href="{asset}favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{asset}style.css?v=research2"><script src="{asset}app.js?v=research2" defer></script>
</head><body data-lang="{lang}"><a class="skip-link" href="#main">{t('Skip to content','跳至正文')}</a>
<header class="site-header"><div class="nav-wrap"><a class="brand" href="#" aria-label="Teach and Grow home"><img src="{asset}favicon.svg" width="30" height="30" alt=""><span>TGL<span class="brand-dot">.</span></span></a><nav aria-label="{t('Main navigation','主导航')}">{nav_html}</nav><a class="language" href="{'../' if zh else 'zh/'}" lang="{t('zh-CN','en')}">{t('中文','English')} <span aria-hidden="true">↗</span></a></div></header>
<main id="main">
<section class="hero research-hero"><div class="container"><p class="eyebrow hero-kicker">{t('AGENT-CENTERED ROBOT LEARNING / SHANGHAI JIAO TONG UNIVERSITY','以智能体为中心的机器人学习 / 上海交通大学')}</p><div class="hero-caption"><span class="signal-dot"></span>{t('A study of learning with fixed model weights','探索模型权重固定时的机器人学习')}</div><h1>Teach <em>and</em> Grow<span class="title-period">.</span></h1><p class="paper-subtitle">An Agent-Centered Architecture<br class="desktop-break"> for General Robot Learning</p><p class="authors"><a href="mailto:changniep@gmail.com">Chang Nie</a><span>·</span>Zhe Liu<span>·</span><a href="mailto:wanghesheng@sjtu.edu.cn">Hesheng Wang</a></p><p class="affiliation">{t('School of Automation and Intelligent Sensing, Shanghai Jiao Tong University','上海交通大学 自动化与感知学院')}</p><p class="hero-summary">{t('How can a robot turn a few demonstrations into<br>capabilities it can adapt, verify, and use again?','机器人如何将少量演示，转化为<br>能够适应场景、接受验证并持续复用的能力？')}</p><div class="hero-links"><a class="button primary" href="#overview">{t('Explore the idea','了解研究思路')} ↓</a><a class="button" href="{paper}" target="_blank" rel="noopener">{t('Read the paper','阅读论文')} ↗</a><a class="button text-button" href="#demos">▷ {t('Watch demonstrations','观看演示')}</a></div><div class="hero-system" aria-label="{t('Teaching feeds agent-led Skill Blocks, whose verified outcomes grow the library and experience memory','示教形成智能体主导的技能块，经过验证的结果进入技能库与经验记忆')}"><div class="system-node"><span>01 / TEACH</span><b>{t('Sparse demonstrations','少量演示')}</b><small>{t('Subgoals & shared structure','子目标与共同结构')}</small></div><span class="system-arrow" aria-hidden="true">→</span><div class="system-node node-core"><span>02 / ACT + VERIFY</span><b>{t('Agent + Skill Blocks','Agent + Skill Blocks')}</b><small>{t('Grounded in physical feedback','以物理反馈形成闭环')}</small></div><span class="system-arrow" aria-hidden="true">→</span><div class="system-node"><span>03 / GROW</span><b>{t('Skills + experience','技能与经验')}</b><small>{t('Retained for the next task','用于下一个任务')}</small></div><div class="system-return"><span>↖</span> {t('Reusable knowledge returns to the next decision','可复用知识回到下一次决策')} <span>↵</span></div></div><div class="hero-bottom"><span>PRETRAINED WEIGHTS / FIXED</span><span>EXECUTABLE EXPERIENCE / EVOLVING</span></div></div></section>
{narrative['overview']}
{narrative['origins']}
{narrative['idea']}
{narrative['method']}
{narrative['memory']}
<section id="demos" class="section container"><div class="section-intro"><p class="eyebrow">06 / {t('BEHAVIOR IN CONTEXT','场景中的行为')}</p><h2>{t('Learn the task. Adapt the execution.','理解任务，灵活执行。')}</h2><p class="lead">{t('Five paired LIBERO demonstrations show the teacher’s example alongside Teach and Grow. Look for changes in grasping, scene grounding, and recovery.','五组 LIBERO 视频并排展示教师演示与 Teach and Grow 的执行，呈现抓取适应、场景落地与反馈纠错。')}</p></div><div class="demo-toolbar"><div class="filters" role="group" aria-label="{t('Filter demonstrations','筛选演示')}" hidden><button class="active" data-filter="All" aria-pressed="true">{t('All five','全部五组')}</button><button data-filter="Object" aria-pressed="false">Object</button><button data-filter="Spatial" aria-pressed="false">Spatial</button><button data-filter="Goal" aria-pressed="false">Goal</button></div><span class="small">{t('Teacher ← → TGL · videos play on request','左：教师 · 右：TGL · 点击播放')}</span></div><p class="small demo-note">{t('Qualitative simulation examples. Clips have different durations; joint playback starts them together without aligning individual actions. Playback speed refers to the supplied videos, not measured robot latency.','这些是仿真中的定性示例。视频时长不同，同时播放只统一起点，不对齐具体动作；播放倍速针对原视频，不代表实测机器人延迟。')}</p><div class="demo-grid">{videos}</div></section>
{narrative['investigation']}
{narrative['growth']}
<section id="resources" class="section resources soft"><div class="container"><div class="resource-top"><div><p class="eyebrow">09 / {t('PAPER & RESOURCES','论文与资源')}</p><h2>{t('Read the full paper.','阅读全文。')}</h2><p>{t('The technical report includes the formulation, Skill Block contract, evaluation, and extended discussion.','技术报告包含问题定义、Skill Block 契约、实验评估和扩展讨论。')}</p></div><a class="button primary" href="{paper}" target="_blank" rel="noopener">{t('Open paper · PDF','打开论文 · PDF')} ↗</a></div><div class="resource-links"><a href="#demos">{t('10 demonstration videos','10 段演示视频')} ↗</a><a href="https://github.com/biubiu3/tgl-web" target="_blank" rel="noopener">{t('Website source','网页源码')} ↗</a><a href="mailto:changniep@gmail.com">{t('Contact the authors','联系作者')} ↗</a></div><p class="small">{t('Robot implementation code is not linked in this release. The repository above contains this project website.','本次发布未提供机器人实现代码链接，上方仓库为本项目网页源码。')}</p><div class="citation" id="citation"><div><h3>BibTeX</h3><button id="copy-citation" type="button" hidden>{t('Copy citation','复制引用')}</button></div><pre><code id="bibtex">{e(bib)}</code></pre><span id="copy-status" role="status"></span></div></div></section>
</main><footer class="container"><a class="brand" href="#">TGL<span class="brand-dot">.</span></a><p>Teach and Grow · Shanghai Jiao Tong University<br><span>{t('Self-hosted images and videos. No analytics or third-party embeds.','图片与视频均由本站提供，无统计追踪或第三方嵌入。')}</span></p><a href="#">{t('Back to top','返回顶部')} ↑</a></footer><dialog id="image-dialog" aria-label="{t('Enlarged paper figure','放大的论文图片')}"><button class="dialog-close" aria-label="{t('Close image','关闭图片')}">×</button><img alt=""><p></p></dialog>
</body></html>'''

(site/'index.html').write_text(page('en'))
(site/'zh').mkdir()
(site/'zh/index.html').write_text(page('zh'))
# A project root redirects to the requested /tgl/ review route.
if site != out:
    target = '/'.join(segments) + '/'
    (out/'index.html').write_text(f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Teach and Grow</title><meta http-equiv="refresh" content="0;url={target}"><link rel="canonical" href="{url}"><p><a href="{target}">Continue to Teach and Grow →</a></p></html>')
(out/'404.html').write_text(f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found · TGL</title><style>body{{font:20px system-ui;max-width:640px;margin:15vh auto;padding:24px;color:#173d37}}a{{color:#155e59}}</style><h1>Page not found</h1><p>The page may have moved.</p><a href="{url}">Return to Teach and Grow →</a></html>')
(out/'.nojekyll').touch()
(out/'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{url}</loc></url><url><loc>{url}zh/</loc></url></urlset>')
(out/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {parts.scheme}://{parts.netloc}/' + ('/'.join([s for s in parts.path.split('/') if s][:1])+'/' if parts.hostname.endswith('.github.io') and parts.path.strip('/') else '') + 'sitemap.xml\n')
if args.custom_domain:
    if '/' in args.custom_domain or args.custom_domain != parts.hostname:
        raise SystemExit('Custom domain must match the hostname in --url')
    (out/'CNAME').write_text(args.custom_domain+'\n')
print(f'Built {site.relative_to(ROOT)} → {url} (English + Chinese)')
