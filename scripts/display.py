"""Reader-facing copy edits; leave metadata, URLs and formal paper titles intact."""
import re


def visible_faq(items):
    omitted = {'What results does TGL report?', 'Is the paper published?'}
    return [item for item in items if item['q'] not in omitted]


def display_html(document):
    head, separator, body = document.partition('</head>')
    if not separator:
        return document
    # Never rewrite attributes (URLs, IDs, CSS classes), scripts, or code examples.
    fragments = re.split(r'(<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>|<code\b[^>]*>.*?</code>|<[^>]+>)', body, flags=re.S | re.I)
    titles = (
        'An Agent-Centered Architecture for General Robot Learning',
        'An Agent-Centered Architecture',
        '面向通用机器人学习的以智能体为中心的架构',
        'Agent as Policy', 'Agent-as-Policy', 'agent-as-policy',
        'Agent-Guided Policy',
    )
    for i in range(0, len(fragments), 2):
        text = fragments[i]
        for j, title in enumerate(titles):
            text = text.replace(title, f'__FORMAL_TITLE_{j}__')
        for sentence in (
            'The rest of this page describes how the agent, the Skill Blocks, and the robot-side executors divide that work.',
            '本页其余部分说明智能体、Skill Block 与机器人侧执行器如何分工。',
            "The paper's own keywords are listed above.", '论文自身的关键词见上。',
            'Project images and demonstration videos are hosted with this website.',
            '项目图片与演示视频均由本站提供。',
        ):
            text = text.replace(sentence, '')
        text = re.sub(r'\bAI[- ]+[Aa]gents?\b', lambda m: 'AI Agents' if m[0].endswith('s') else 'AI Agent', text)
        text = re.sub(r'(?<!AI )\bagent(s)?\b', lambda m: 'AI Agents' if m[1] else 'AI Agent', text, flags=re.I)
        text = text.replace('AI Agent-CENTERED ROBOT LEARNING', 'AI AGENT-CENTERED ROBOT LEARNING')
        text = re.sub(r'(?<!AI )智能体', 'AI 智能体', text)
        text = text.replace('a AI Agent', 'an AI Agent')
        text = re.sub(r'(?<=[\u4e00-\u9fff])AI', ' AI', text)
        for j, title in enumerate(titles):
            text = text.replace(f'__FORMAL_TITLE_{j}__', title)
        fragments[i] = text
    return head + separator + ''.join(fragments)
