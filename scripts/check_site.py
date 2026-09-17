#!/usr/bin/env python3
"""Check generated local links, page anchors, and benchmark arithmetic."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT/'dist'
errors = []
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.ids=[]; self.images=[]; self.videos=0
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        for k in ('src','href','poster'):
            if k in a: self.links.append(a[k])
        if tag=='img': self.images.append(a)
        if tag=='video': self.videos+=1
pages={}
for path in DIST.rglob('*.html'):
    parser=Page();parser.feed(path.read_text());pages[path.resolve()]=parser
for path,p in pages.items():
    if len(p.ids)!=len(set(p.ids)): errors.append(f'{path}: duplicate IDs')
    for img in p.images:
        if 'alt' not in img: errors.append(f'{path}: missing alt')
    for link in p.links:
        u=urlsplit(link)
        if u.scheme or u.netloc: continue
        target=(path.parent / unquote(u.path)).resolve() if u.path else path
        if target.is_dir(): target=target/'index.html'
        if not target.exists(): errors.append(f'{path}: missing {link}')
        if u.fragment and target.suffix=='.html' and target in pages and u.fragment not in pages[target].ids:
            errors.append(f'{path}: missing anchor {link}')
    if path.name=='index.html' and p.videos:
        if p.videos!=10: errors.append(f'{path}: expected 10 videos, got {p.videos}')
data=json.loads((ROOT/'content/site.json').read_text())
for key in ('libero','plus'):
    for row in data[key]['rows']:
        mean=sum(row[1:-1])/len(row[1:-1])
        if abs(mean-row[-1])>0.051: errors.append(f'{key}: inconsistent mean for {row[0]}')
# The positioning statement is machine-layer only: it must not enter rendered HTML.
for path in DIST.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    for token in ('positioning.json', 'positioning.md'):
        if token in text:
            errors.append(f'{path}: machine-layer statement leaked into HTML ({token})')
pos = data['seo'].get('positioning')
if pos:
    en, zh = pos.get('en', {}), pos.get('zh', {})
    if set(en) != set(zh):
        errors.append('seo.positioning: en/zh keys differ: ' + ', '.join(sorted(set(en) ^ set(zh))))
    for key, val in en.items():
        if isinstance(val, list) and len(val) != len(zh.get(key, [])):
            errors.append(f'seo.positioning.{key}: {len(val)} English items, {len(zh.get(key, []))} Chinese')
    terms = {t['name'] for t in data['seo']['terms']}
    for name in en.get('term_attribution', {}).get('introduced_here', []):
        if name not in terms:
            errors.append(f'seo.positioning: attributed term not defined in seo.terms: {name}')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} HTML pages, all local links and anchors, 10 videos per language, '
      'benchmark means, positioning statement structure.')
