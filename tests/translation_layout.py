"""Browser layout stress test; simulates extension DOM, not a live translation service.
Run after build: python3 tests/translation_layout.py [base URL]
"""
import json
import sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8879'
INJECT = r'''(kind) => {
 const selector = 'main p,main h1,main h2,main h3,main h4,main dt,main dd,main figcaption,main small,.nav-wrap nav a,.hero-links a,.system-node b,.system-node>span,.state-row b,.state-label,.video-label,.tag,.pair-controls button,.walk-tabs button,.filters button';
 const targets = [...document.querySelectorAll(selector)].filter(e => !e.querySelector(selector) && !e.closest('pre,code,[translate="no"]') && e.textContent.trim());
 for (const e of targets) {
   const original = document.createElement('span');
   original.dataset.testOriginal = '';
   while (e.firstChild) original.append(e.firstChild);
   e.append(original);
   const wrapper = document.createElement(kind === 'generic' ? 'font' : 'span');
   wrapper.dataset.testTranslation = '';
   if (kind !== 'generic') wrapper.className = 'immersive-translate-target-wrapper';
   wrapper.lang = document.body.dataset.lang === 'en' ? 'zh' : 'en';
   wrapper.style.display = 'block';
   wrapper.textContent = wrapper.lang === 'zh' ? '双语布局测试：机器人根据当前观察选择可复用的技能，并在执行之后验证实际结果。' : 'Bilingual layout sample: the robot selects reusable skills from current observations and verifies the physical outcome after execution.';
   if (kind === 'immersive' && e.matches('.demo-card>p,.reading-wide>p,.article-copy>p')) e.after(wrapper);
   else e.append(wrapper);
 }
 return targets.length;
}'''
CHECK = r'''() => {
 const problems = [];
 if (document.documentElement.scrollWidth > innerWidth + 1) problems.push('document overflow');
 for (const e of document.querySelectorAll('main p,main h1,main h2,main h3,main dd,.system-node b,.system-node small,.state-row,.video-label,.button,.walk-tabs button,.pair-controls button')) {
   if (!e.getBoundingClientRect().height || e.closest('[hidden]')) continue;
   if (e.scrollWidth > e.clientWidth + 2) problems.push('clipped width: '+e.className);
   if (e.scrollHeight > e.clientHeight + 2) problems.push('clipped height: '+e.className);
 }
 for (const pane of document.querySelectorAll('.video-pane')) {
   if (!pane.getBoundingClientRect().height) continue;
   if(pane.querySelector('.video-label').getBoundingClientRect().bottom > pane.querySelector('video').getBoundingClientRect().top + 1) problems.push('video label overlap');
 }
 const header=document.querySelector('.site-header').getBoundingClientRect().height;
 const offset=parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop);
 if(offset<header+15) problems.push('stale header offset');
 if(header>innerHeight*.4) problems.push('header occupies too much of the viewport');
 return problems;
}'''
results=[]
with sync_playwright() as p:
    browser=p.chromium.launch()
    for route in ('/','/zh/','/paper/','/zh/glossary/'):
        for width in (360,390,768,1024,1440):
            for kind in ('immersive','generic'):
                page=browser.new_page(viewport={'width':width,'height':1000},reduced_motion='reduce')
                errors=[]
                page.on('pageerror',lambda e:errors.append(str(e)))
                page.goto(BASE+route,wait_until='networkidle')
                page.wait_for_timeout(80)
                assert not page.evaluate(CHECK),(route,width,'original',page.evaluate(CHECK))
                n=page.evaluate(INJECT,kind)
                page.wait_for_timeout(80)
                assert not page.evaluate(CHECK),(route,width,kind,page.evaluate(CHECK))
                if route=='/' and width==390 and kind=='immersive':
                    page.locator('.walk-tabs button').nth(1).click()
                    assert page.locator('.walk-tabs button').nth(1).get_attribute('aria-pressed')=='true'
                    page.locator('.filters button').nth(1).click()
                    page.locator('.filters button').first.click()
                    page.locator('.project-cover .zoom').click()
                    assert page.locator('dialog').is_visible()
                    page.keyboard.press('Escape')
                    page.evaluate("document.querySelector('.hero-system').scrollIntoView({behavior:'instant',block:'start'})")
                    page.screenshot(path='/tmp/tgl-translation-mobile.png')
                # Translation-only and toggle back must also reflow.
                page.evaluate("document.querySelectorAll('[data-test-original]').forEach(e=>e.hidden=true)")
                page.wait_for_timeout(80)
                assert not page.evaluate(CHECK),(route,width,'translation only',page.evaluate(CHECK))
                page.evaluate("document.querySelectorAll('[data-test-translation]').forEach(e=>e.remove());document.querySelectorAll('[data-test-original]').forEach(e=>e.replaceWith(...e.childNodes))")
                page.wait_for_timeout(80)
                assert not page.evaluate(CHECK),(route,width,'restored',page.evaluate(CHECK))
                assert not errors,errors
                results.append({'route':route,'width':width,'markup':kind,'translated_blocks':n})
                page.close()
    browser.close()
print(f'PASS: {len(results)} cases; original, bilingual, translation-only, restored; wrapping, video labels, header offset and controls.')
