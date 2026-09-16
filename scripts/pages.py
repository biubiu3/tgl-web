"""Content for the generated sub-pages.

One dict per page, with `en` and `zh` bodies side by side so the two language
versions cannot drift structurally — they share a slug, a `related` list and a
`schema` list, and each supplies its own title/desc/h1/lede/sections/faq.

Prose only. Every number, identifier and definition that also appears in
metadata is read from content/site.json at build time (see seo.py), so this file
cannot contradict the canonical facts. `{...}` placeholders are filled from
site.json.

Page shape:
    slug      URL path segment; pages land at /<slug>/ and /zh/<slug>/
    en / zh   {"title", "desc", "h1", "lede", "sections": [(h, [p, ...])],
               "faq": [(q, a)], "keywords"}
"""

PAPER = {
    "slug": "paper",
    "parent": "",
    "schema": ["ScholarlyArticle"],
    "related": ["research-context", "teach-and-grow-learning"],
    "en": {
        "title": "Teach and Grow (TGL) — Paper, Abstract and Citation",
        "desc": ("Publication record for \"Teach and Grow: An Agent-Centered Architecture for General Robot "
                 "Learning\" by Chang Nie, Zhe Liu and Hesheng Wang: abstract, authors, keywords, BibTeX and "
                 "links to the PDF, code and demonstrations."),
        "h1": "Teach and Grow: An Agent-Centered Architecture for General Robot Learning",
        "lede": ("This is the publication record for the Teach and Grow technical report. TGL is a training-free "
                 "architecture for general robot learning: a pretrained multimodal agent turns a few "
                 "demonstrations into reusable, verifiable Skill Blocks while the model weights stay fixed."),
        "sections": [
            ("Authors and affiliation", [
                "Chang Nie, Zhe Liu and Hesheng Wang are with the School of Automation and Intelligent Sensing at "
                "Shanghai Jiao Tong University and the Shanghai Key Laboratory of Navigation and Location Based "
                "Services, Shanghai 200240, China. The corresponding author is Hesheng Wang.",
            ]),
            ("Publication status", [
                "This is a <b>technical report</b>. No venue acceptance is claimed. A public preprint is "
                "available: the paper is on arXiv as <code>arXiv:2608.17209</code>, first posted 17 August 2026, "
                "with DOI <code>10.48550/arXiv.2608.17209</code>. The current manuscript PDF is also served from "
                "this site, and the method implementation is maintained in the IRMVLab/TGL repository. This "
                "record will be updated if the manuscript is submitted to or accepted by a venue.",
            ]),
            ("Abstract", ["{abstract}"]),
            ("Keywords", ["{keywords}"]),
            ("Identifiers", [
                "arXiv: <a href=\"{arxiv_url}\">2608.17209</a> · DOI: "
                "<a href=\"{doi_url}\">10.48550/arXiv.2608.17209</a> · "
                "PDF: <a href=\"{pdf}\">manuscript (this site)</a> and "
                "<a href=\"{arxiv_pdf}\">arXiv:2608.17209</a> · "
                "Code: <a href=\"{code}\">IRMVLab/TGL</a>",
            ]),
            ("How to cite", [
                "BibTeX is available at <a href=\"{cite}\">/cite.bib</a> under the key "
                "<code>{bibtex_key}</code>, and as <code>CITATION.cff</code> for reference managers. A plain-text "
                "citation is: Chang Nie, Zhe Liu and Hesheng Wang, “Teach and Grow: An Agent-Centered "
                "Architecture for General Robot Learning,” arXiv:2608.17209, 2026. "
                "DOI: 10.48550/arXiv.2608.17209.",
            ]),
            ("Companion artifacts", [
                "The report is released together with a reference implementation and ten paired demonstration "
                "videos. The <a href=\"{home}\">project page</a> covers the problem framing, the Skill Block "
                "architecture, a worked example, the controlled studies and the demonstrations.",
            ]),
        ],
        "keywords": ("Teach and Grow paper, TGL technical report, training-free robot learning, agent-centered "
                     "robot learning, Skill Blocks, abstract, BibTeX, Chang Nie, Zhe Liu, Hesheng Wang, Shanghai "
                     "Jiao Tong University"),
    },
    "zh": {
        "title": "Teach and Grow（TGL）— 论文、摘要与引用",
        "desc": ("《Teach and Grow: An Agent-Centered Architecture for General Robot Learning》的著录页面，"
                 "作者为 Chang Nie、Zhe Liu、Hesheng Wang。含摘要、作者、关键词、BibTeX，以及 PDF、代码与演示链接。"),
        "h1": "Teach and Grow：面向通用机器人学习的以智能体为中心的架构",
        "lede": ("本页是 Teach and Grow 技术报告的正式著录页。TGL 是一种免训练的通用机器人学习架构："
                 "预训练的多模态智能体把少量演示转化为可复用、可验证的 Skill Block，而模型权重始终保持不变。"),
        "sections": [
            ("作者与单位", [
                "Chang Nie、Zhe Liu、Hesheng Wang 来自上海交通大学自动化与感知学院，以及上海市导航与定位服务重点实验室"
                "（上海 200240）。通讯作者为王贺升。",
            ]),
            ("发表状态", [
                "这是一份<b>技术报告</b>，不主张已被任何会议或期刊接收。公开预印本已发布："
                "论文在 arXiv 的编号为 <code>arXiv:2608.17209</code>，首次发布于 2026 年 8 月 17 日，"
                "DOI 为 <code>10.48550/arXiv.2608.17209</code>。当前稿件 PDF 同时由本站提供，"
                "方法实现维护在 IRMVLab/TGL 仓库中。若稿件后续投稿或获得接收，本页面会同步更新。",
            ]),
            ("摘要", ["{abstract_zh}"]),
            ("关键词", ["{keywords_zh}"]),
            ("标识符", [
                "arXiv：<a href=\"{arxiv_url}\">2608.17209</a> · DOI："
                "<a href=\"{doi_url}\">10.48550/arXiv.2608.17209</a> · "
                "PDF：<a href=\"{pdf}\">本站稿件</a> 与 <a href=\"{arxiv_pdf}\">arXiv:2608.17209</a> · "
                "代码：<a href=\"{code}\">IRMVLab/TGL</a>",
            ]),
            ("如何引用", [
                "BibTeX 位于 <a href=\"{cite}\">/cite.bib</a>，键为 <code>{bibtex_key}</code>；"
                "另有 <code>CITATION.cff</code> 供引用管理器使用。"
                "纯文本引用格式：Chang Nie, Zhe Liu and Hesheng Wang, “Teach and Grow: An Agent-Centered "
                "Architecture for General Robot Learning,” arXiv:2608.17209, 2026. "
                "DOI: 10.48550/arXiv.2608.17209。",
            ]),
            ("配套产出", [
                "本报告同时发布参考实现与十段成对演示视频。<a href=\"{home}\">项目主页</a>涵盖问题定义、"
                "Skill Block 架构、工作示例、受控研究与演示视频。",
            ]),
        ],
        "keywords": ("Teach and Grow 论文, TGL 技术报告, 免训练机器人学习, 以智能体为中心的机器人学习, "
                     "Skill Block, 摘要, BibTeX, 上海交通大学, 机器人操作, 具身智能"),
    },
}

RESEARCH_CONTEXT = {
    "slug": "research-context",
    "parent": "",
    "related": ["teach-and-grow-learning", "retraining-tax"],
    "en": {
        "title": "Research Context: Where Teach and Grow Sits Among VLA, WAM and Embodied AI",
        "desc": ("How the Teach and Grow (TGL) training-free robot learning architecture relates to "
                 "vision-language-action models, world-action models, robot foundation models, agentic robotics, "
                 "skill composition and lifelong learning."),
        "h1": "Research Context: Where Teach and Grow Sits",
        "lede": ("Teach and Grow is a training-free architecture for general robot learning. It sits inside "
                 "embodied-intelligence and agentic-robotics research, next to vision-language-action (VLA) "
                 "models and world-action models (WAM). The difference it proposes is not in how strong the "
                 "underlying models are, but in where a newly acquired capability is stored."),
        "sections": [
            ("Vision-language-action (VLA) models", [
                "VLA models map camera images, a language instruction and robot state directly to control, and "
                "they are the dominant architecture for general-purpose manipulation. They work because large "
                "multimodal pretraining produces representations that transfer. In their end-to-end route a new "
                "behaviour is absorbed into the model parameters through training: collect more robot data, "
                "optimise, re-check what the policy already supported. TGL keeps those models as the source of "
                "priors and moves new task knowledge somewhere else.",
            ]),
            ("World-action models and learned dynamics", [
                "World-action models add learned physical dynamics, so the system reasons about how a scene will "
                "evolve rather than only reacting to its current state. This improves generalisation, at the cost "
                "of a heavier training cycle and a larger data requirement. The retraining burden TGL names "
                "applies to these models as much as to VLA policies: the repair path runs through the parameters.",
            ]),
            ("Robot foundation models as the prior", [
                "TGL assumes a strong pretrained stack — a multimodal agent for reasoning, plus specialist "
                "perception, grasping and motion tools. Robot foundation models supply exactly that prior. In the "
                "paper's framing they are held fixed while the explicit, inspectable stores grow: the Skill "
                "Library of validated behaviours and the Experience Memory of conditions and repairs.",
            ]),
            ("Agentic robotics", [
                "The architecture is agent-centered: the reasoning agent reads the scene, chooses a subgoal and a "
                "tool, observes the result, and revises the remaining plan. This is the pattern that made "
                "tool-using language agents useful, applied where a mistaken action changes the physical world. "
                "The agent carries task-level reasoning; the robot-side executors carry geometry and continuous "
                "control.",
            ]),
            ("Skill composition and lifelong learning", [
                "TGL's neighbours also include work on skill composition, skill libraries and lifelong or "
                "continual learning. The shared question is what a robot retains across tasks and how it is "
                "retrieved later. TGL's contribution is to make the retained objects explicit — a validated "
                "behaviour with a stated scope and outcome test — so that a person can narrow an overgeneralised "
                "skill, revise a recovery rule, or mark an executor version as incompatible.",
            ]),
            ("Few-shot and sparse teaching", [
                "Teaching supplies the structure the agent starts from: the subgoal sequence, the ordering, and "
                "the conditions worth checking. It does not supply the physical realization, which is recomputed "
                "for the current scene. That is why TGL can preserve the intended effect while the actual grasp, "
                "path and contact point differ from the teacher's.",
            ]),
            ("What TGL keeps from these directions", [
                "A learned policy can still implement a Skill Block, execute a familiar composition, or become a "
                "future student under the proposed slow-teacher/fast-student split. A geometric planner can "
                "bridge two skills; a visual servo can close a local loop. TGL supplies the semantic contract and "
                "the feedback structure through which those components contribute to a task, rather than "
                "replacing them.",
            ]),
        ],
        "faq": [
            ("Is TGL a replacement for VLA models?",
             "No. TGL relies on pretrained models for perception, reasoning and control. What it changes is where "
             "a newly acquired task capability is stored: in explicit Skill Blocks and memory rather than in the "
             "weights, so acquiring one task does not require re-optimising the policy."),
            ("Is TGL a world model?",
             "No. TGL does not learn scene dynamics. It stores the semantic effect of a behaviour and recomputes "
             "the physical realization from the current observation, which is a different mechanism from "
             "predicting a future state."),
            ("Does TGL work without an AI agent?",
             "The architecture is agent-centered by design: the agent selects subgoals, invokes tools, and "
             "revises the remaining plan from physical feedback. Specialised robot components still perform the "
             "geometry and control, so the method is a division of labour rather than a single model."),
        ],
        "keywords": ("TGL research context, training-free robot learning vs VLA, world-action model WAM, robot "
                     "foundation models, agentic robotics, embodied intelligence, skill composition, lifelong "
                     "learning, continual learning, few-shot teaching, sparse demonstrations, robot manipulation"),
    },
    "zh": {
        "title": "技术定位：Teach and Grow 在 VLA、WAM 与具身智能中的位置",
        "desc": ("Teach and Grow（TGL）免训练机器人学习架构与视觉-语言-动作模型、世界动作模型、机器人基础模型、"
                 "智能体机器人学、技能组合与终身学习之间的关系。"),
        "h1": "技术定位：Teach and Grow 处在什么位置",
        "lede": ("Teach and Grow 是一种免训练的通用机器人学习架构，属于具身智能与智能体机器人学（agentic robotics）"
                 "的研究脉络，与视觉-语言-动作（VLA）模型和世界动作模型（WAM）相邻。"
                 "它提出的差别不在于底层模型有多强，而在于新获得的能力被存放在哪里。"),
        "sections": [
            ("视觉-语言-动作（VLA）模型", [
                "VLA 模型把相机图像、语言指令与机器人状态直接映射为控制，是通用操作任务的主流架构。"
                "它们之所以有效，是因为大规模多模态预训练产生了可迁移的表示。在端到端路线中，新行为通过训练被吸收进"
                "模型参数：采集更多机器人数据、做优化、再回归检查策略此前已支持的能力。"
                "TGL 把这些模型保留为先验来源，而把新任务知识放到别处。",
            ]),
            ("世界动作模型与学习到的动态", [
                "世界动作模型进一步引入学习到的物理动态，使系统能够推理场景将如何演变，而不只是对当前状态作出反应。"
                "这提升了泛化能力，代价是更重的训练周期与更大的数据需求。"
                "TGL 所指出的再训练负担同样适用于这类模型：修复路径仍然要穿过参数。",
            ]),
            ("机器人基础模型作为先验", [
                "TGL 假定存在一个强大的预训练栈——用于推理的多模态智能体，加上专用的感知、抓取与运动工具。"
                "机器人基础模型提供的正是这种先验。在论文的表述中，它们保持不变，而显式、可检查的存储持续增长："
                "存放经验证行为的 Skill Library，以及记录条件与修复的 Experience Memory。",
            ]),
            ("智能体机器人学", [
                "该架构以智能体为中心：推理智能体读取场景、选择子目标与工具、观察结果，并修正剩余计划。"
                "这正是让工具型语言智能体变得有用的模式，只是被应用到了“一次错误动作会改变物理世界”的场合。"
                "智能体承担任务级推理，机器人侧的执行器承担几何与连续控制。",
            ]),
            ("技能组合与终身学习", [
                "TGL 的邻近工作还包括技能组合、技能库以及终身学习或持续学习。共同的问题是：机器人在跨任务时保留了什么，"
                "以及之后如何检索。TGL 的贡献是把被保留的对象显式化——一个带有明确适用范围与结果检验的经验证行为——"
                "从而让人可以收窄过度泛化的技能、修改恢复规则，或标记某个执行器版本不兼容。",
            ]),
            ("少样本与稀疏示教", [
                "示教提供智能体起步所需的结构：子目标序列、顺序，以及值得检查的条件。它并不提供物理实现，"
                "后者会根据当前场景重新计算。这正是 TGL 能够保留意图效果、而实际抓取、路径与接触点与教师不同的原因。",
            ]),
            ("TGL 从这些方向保留了什么", [
                "学习策略仍然可以实现某个 Skill Block、执行熟悉的技能组合，或在拟议的“慢教师–快学生”路线中成为未来的学生。"
                "几何规划器可以连接两个技能，视觉伺服可以完成局部闭环。"
                "TGL 提供语义契约与反馈结构，让这些组件共同服务于任务，而不是取代它们。",
            ]),
        ],
        "faq": [
            ("TGL 会取代 VLA 模型吗？",
             "不会。TGL 依赖预训练模型完成感知、推理与控制。它改变的是新获得任务能力的存放位置："
             "存放在显式的 Skill Block 与记忆中，而不是写进权重，因此获取一个任务不需要重新优化策略。"),
            ("TGL 是世界模型吗？",
             "不是。TGL 不学习场景动态。它保存行为的语义效果，并根据当前观测重新计算物理实现，"
             "这与“预测未来状态”是不同机制。"),
            ("TGL 可以脱离 AI 智能体运行吗？",
             "该架构在设计上以智能体为中心：由智能体选择子目标、调用工具，并根据物理反馈修正剩余计划。"
             "专用机器人组件仍然负责几何与控制，因此这是一套分工，而不是单一模型。"),
        ],
        "keywords": ("TGL 技术定位, 免训练机器人学习与 VLA, 世界动作模型 WAM, 机器人基础模型, 智能体机器人学, "
                     "具身智能, 技能组合, 终身学习, 持续学习, 少样本示教, 稀疏示教, 机器人操作"),
    },
}

CONCEPTS = [
    {
        "slug": "teach-and-grow-learning",
        "parent": "concepts",
        "related": ["training-free-robot-learning", "retraining-tax", "research-context"],
        "en": {
            "title": "Teach-and-Grow Learning (TGL): Training-Free Robot Learning from Demonstrations",
            "desc": ("Teach-and-Grow Learning (TGL) is a training-free architecture in which a pretrained AI agent "
                     "turns a few demonstrations into reusable, verifiable Skill Blocks while model weights stay "
                     "fixed. New task knowledge lives in the Skill Library and Experience Memory."),
            "h1": "Teach-and-Grow Learning (TGL)",
            "lede": ("Teach-and-Grow Learning (TGL) is a training-free architecture for general robot learning. A "
                     "pretrained multimodal agent reads a few successful demonstrations, expresses their shared "
                     "structure as closed-loop Skill Blocks, grounds each block in the current scene, and keeps "
                     "the behaviours that pass validation. The pretrained model weights do not change."),
            "sections": [
                ("The name in two halves", [
                    "<b>Teach</b> is the input: a small number of demonstrations that reveal the subgoal sequence "
                    "and the conditions worth checking. Teaching supplies structure, not the physical "
                    "realization — the teacher's exact trajectory and pixel coordinates are deliberately not what "
                    "gets retained.",
                    "<b>Grow</b> is the output: each task adds validated behaviour to an explicit Skill Library "
                    "and the context of the attempt to Experience Memory. The next task starts from a larger base "
                    "of inspectable capability, so the resource grows after deployment rather than only at "
                    "training time.",
                ]),
                ("What makes it training-free", [
                    "Acquiring the incoming task invokes no gradient update, no fine-tuning, and no "
                    "reinforcement-learning stage. The agent and its specialist models may already be pretrained "
                    "— that is assumed. What changes during task acquisition is the explicit skill and memory "
                    "state, not the weights. This is the precise sense in which the term is used here, and it is "
                    "narrower than “a model that was not trained at all”.",
                ]),
                ("Why the separation matters", [
                    "In an end-to-end policy, repairing one failure means changing parameters that also support "
                    "everything else, followed by regression checks. There is no separately addressable fix for "
                    "one object or one contact condition. TGL makes the repair a local edit to an explicit "
                    "object: a Skill Block can be narrowed, its recovery rule changed, or an incompatible "
                    "executor version flagged, without reopening the rest of the system.",
                ]),
                ("What it does not claim", [
                    "TGL does not claim that stored files guarantee retained behaviour: the right block must "
                    "still be retrieved, grounded with current sensing, and executed successfully. It does not "
                    "claim that low-cost growth is automatic, because unrestricted pairwise compatibility checks "
                    "between skills can make a library expensive to grow. And the scaling hypothesis relating "
                    "reusable experience to falling future-task error is presented as a hypothesis, not as a "
                    "fitted law.",
                ]),
            ],
            "faq": [
                ("What does TGL stand for?",
                 "Teach-and-Grow Learning. The technical report is “Teach and Grow: An Agent-Centered "
                 "Architecture for General Robot Learning”."),
                ("How is TGL different from fine-tuning a robot policy?",
                 "Fine-tuning changes model parameters to absorb a new behaviour, which can affect previously "
                 "supported behaviour and requires regression checking. TGL leaves parameters fixed and stores "
                 "the new capability as an explicit, inspectable Skill Block."),
                ("What does a TGL run actually produce?",
                 "Two persistent stores: a Skill Library of validated executable behaviours with their scopes and "
                 "contracts, and an Experience Memory recording the task, the selected blocks, observations, the "
                 "outcome, the diagnosis and any repair."),
            ],
            "keywords": ("Teach-and-Grow Learning, TGL, training-free robot learning, robot learning from "
                         "demonstrations, agent-centered robot learning, Skill Blocks, Skill Library, Experience "
                         "Memory, retraining tax, GPT-6 Astra, Codex, LIBERO"),
        },
        "zh": {
            "title": "Teach-and-Grow Learning（TGL）：从演示中免训练学习机器人技能",
            "desc": ("Teach-and-Grow Learning（TGL）是一种免训练架构：预训练的 AI 智能体把少量演示转化为可复用、"
                     "可验证的 Skill Block，而模型权重保持不变。新任务知识存放在 Skill Library 与 Experience Memory 中。"),
            "h1": "Teach-and-Grow Learning（TGL）",
            "lede": ("Teach-and-Grow Learning（TGL）是一种面向通用机器人学习的免训练架构。预训练的多模态智能体读取少量"
                     "成功演示，把它们的共同结构表达为闭环的 Skill Block，将每个块落实到当前场景，并保留通过验证的行为。"
                     "预训练模型权重不发生改变。"),
            "sections": [
                ("名字的两半", [
                    "<b>Teach（教）</b>是输入：少量演示揭示子目标序列与值得检查的条件。示教提供的是结构，而不是物理实现——"
                    "教师的确切轨迹与像素坐标恰恰是刻意不被保留的部分。",
                    "<b>Grow（长）</b>是输出：每个任务都把经验证的行为加入显式的 Skill Library，并把这次尝试的上下文"
                    "写入 Experience Memory。下一个任务从更大的可检查能力基础上开始，因此这份资源在部署之后仍在增长，"
                    "而不只在训练阶段增长。",
                ]),
                ("“免训练”的含义", [
                    "获取当前任务的过程中不进行梯度更新、不做微调、也不包含强化学习阶段。智能体及其专用模型本身可以是"
                    "预训练好的——这是被假定的前提。任务获取期间改变的是显式的技能与记忆状态，而不是权重。"
                    "这里是该术语的精确含义，它比“完全没有训练过的模型”要窄得多。",
                ]),
                ("为什么这种分离重要", [
                    "在端到端策略中，修复一次失败意味着改动同时也支撑其它能力的参数，随后还要做回归检查。"
                    "针对某个物体或某种接触条件，不存在可单独定位的修复。TGL 把修复变成对显式对象的局部编辑："
                    "可以收窄一个 Skill Block、修改其恢复规则，或标记某个执行器版本不兼容，而不必重新打开系统的其余部分。",
                ]),
                ("它不主张什么", [
                    "TGL 不主张“保存了文件就等于保留了行为”：正确的块仍必须被检索到、结合当前传感落地，并成功执行。"
                    "它也不主张低成本增长是自动成立的——技能之间不受限制的两两兼容性检查同样可能让技能库变得昂贵。"
                    "而把可复用经验与未来任务误差下降联系起来的缩放假设，是作为假设提出的，不是拟合出的定律。",
                ]),
            ],
            "faq": [
                ("TGL 是什么的缩写？",
                 "Teach-and-Grow Learning（教与长学习）。技术报告标题为 “Teach and Grow: An Agent-Centered "
                 "Architecture for General Robot Learning”。"),
                ("TGL 与微调机器人策略有什么不同？",
                 "微调通过改变模型参数来吸收新行为，可能影响此前已支持的行为，并且需要回归检查。"
                 "TGL 保持参数不变，把新能力存为显式、可检查的 Skill Block。"),
                ("一次 TGL 运行实际产出什么？",
                 "两份持久化存储：一份是 Skill Library，保存经验证的可执行行为及其适用范围与契约；"
                 "另一份是 Experience Memory，记录任务、所选技能块、观测、结果、诊断与修复。"),
            ],
            "keywords": ("Teach-and-Grow Learning, TGL, 免训练机器人学习, 从演示学习机器人技能, "
                         "以智能体为中心的机器人学习, Skill Block, 技能库, 经验记忆, 再训练成本, "
                         "GPT-6 Astra, Codex, LIBERO"),
        },
    },
    {
        "slug": "training-free-robot-learning",
        "parent": "concepts",
        "related": ["teach-and-grow-learning", "skill-block", "retraining-tax"],
        "en": {
            "title": "Training-Free Robot Learning: What It Means and What It Does Not Mean",
            "desc": ("Training-free robot learning means acquiring a new capability without gradient updates, "
                     "fine-tuning or reinforcement learning. Pretrained weights stay fixed; new task knowledge "
                     "lives in explicit skill and memory stores instead."),
            "h1": "Training-Free Robot Learning",
            "lede": ("Training-free robot learning means acquiring a new robot capability without gradient "
                     "updates, fine-tuning, or reinforcement learning. The pretrained model weights stay fixed, "
                     "and whatever is learned about the new task is stored explicitly rather than written into "
                     "the parameters. Teach-and-Grow Learning (TGL) is an architecture built on that constraint."),
            "sections": [
                ("The precise definition", [
                    "The term is narrower than it may sound. “Training-free” here describes the <i>acquisition "
                    "path</i>, not the models: the pretrained agent, perception and control components were "
                    "trained by someone, and TGL assumes they are strong. What the term rules out is a gradient "
                    "update, a task-specific fine-tuning run, or a reinforcement-learning stage when the robot "
                    "meets a new task.",
                ]),
                ("Where the new knowledge goes instead", [
                    "If a capability is not written into weights, it has to live somewhere a person can inspect. "
                    "TGL uses two explicit stores. The <b>Skill Library</b> holds validated behaviours — the "
                    "goal, the reusable strategy, the supported conditions, compatible executors and an outcome "
                    "test. The <b>Experience Memory</b> holds the context of use: which task, which blocks, what "
                    "was observed, what happened, what the diagnosis was, and what repair was applied.",
                ]),
                ("Why the constraint is interesting", [
                    "Physical interaction data is expensive in a way text and code are not: it has to be created "
                    "by operating a robot or a simulator. Because an end-to-end policy absorbs new behaviour into "
                    "shared parameters, a local failure can demand a broadly coupled repair. Removing the "
                    "parameter update from the acquisition path makes the update local — provided grounding, "
                    "validation, compatibility and retrieval stay manageable, which is a condition the paper "
                    "analyses rather than assumes.",
                ]),
                ("What it is not", [
                    "It is not “no learning”: behaviour is acquired, and the library and memory grow. It is not "
                    "“no pretraining” — a strong prior is exactly what makes the route viable. And it is not a "
                    "claim that parameters should never be touched: the paper's proposed slow-teacher/fast-student "
                    "path would later train a policy from verified trajectories, which is a deliberate extension "
                    "rather than part of the training-free acquisition step.",
                ]),
            ],
            "keywords": ("training-free robot learning, robot learning without fine-tuning, no-gradient robot "
                         "learning, zero-shot robot manipulation, few-shot robot learning, agent-centered robot "
                         "learning, TGL, Teach-and-Grow Learning, skill library, experience memory"),
        },
        "zh": {
            "title": "免训练机器人学习：指的是什么，不指什么",
            "desc": ("免训练机器人学习指在没有梯度更新、微调或强化学习的情况下获得新的机器人能力。预训练权重保持固定，"
                     "新任务知识存放在显式的技能与记忆存储中。"),
            "h1": "免训练机器人学习",
            "lede": ("免训练机器人学习指在没有梯度更新、微调或强化学习的情况下获得新的机器人能力。预训练模型权重保持固定，"
                     "关于新任务学到的东西被显式存放，而不是写进参数。Teach-and-Grow Learning（TGL）就是建立在这一约束上的架构。"),
            "sections": [
                ("精确含义", [
                    "这个术语比字面上听起来要窄。这里的“免训练”描述的是<i>获取路径</i>，而不是模型："
                    "预训练智能体、感知组件与控制组件都是由别人训练出来的，TGL 假定它们足够强。"
                    "该术语排除的是：当机器人遇到新任务时进行梯度更新、做任务特定微调，或进入强化学习阶段。",
                ]),
                ("新知识去了哪里", [
                    "如果能力不写进权重，它就必须存在一个可被人检查的地方。TGL 使用两份显式存储。"
                    "<b>Skill Library</b> 保存经验证的行为——目标、可复用策略、支持条件、兼容执行器与结果检验。"
                    "<b>Experience Memory</b> 保存使用情境：哪个任务、选了哪些技能块、观察到什么、发生了什么、"
                    "诊断是什么、应用了什么修复。",
                ]),
                ("为什么这个约束有意思", [
                    "物理交互数据的昂贵程度不同于文本和代码：它必须通过操作机器人或仿真器来产生。"
                    "由于端到端策略把新行为吸收进共享参数，一个局部失败可能要求一次耦合面很广的修复。"
                    "把参数更新从获取路径中移除，能让更新变成本地的——前提是场景落地、验证、兼容性与检索保持可控，"
                    "而这是论文分析的条件，不是假定的条件。",
                ]),
                ("它不是什么", [
                    "它不是“不学习”：行为确实被获得了，技能库与记忆也在增长。它不是“不预训练”——"
                    "强大的先验正是这条路线可行的原因。它也不主张参数永远不应被改动：论文提出的“慢教师–快学生”路线"
                    "会用经验证的轨迹去训练策略，这是有意的扩展，而不属于免训练获取这一步。",
                ]),
            ],
            "keywords": ("免训练机器人学习, 无需微调的机器人学习, 无梯度机器人学习, 少样本机器人学习, "
                         "以智能体为中心的机器人学习, TGL, Teach-and-Grow Learning, 技能库, 经验记忆"),
        },
    },
    {
        "slug": "skill-block",
        "parent": "concepts",
        "related": ["skill-library", "experience-memory", "teach-and-grow-learning"],
        "en": {
            "title": "Skill Block: The Unit of Reusable Robot Behaviour in TGL",
            "desc": ("A Skill Block is the unit of reusable robot behaviour in Teach-and-Grow Learning: a goal, a "
                     "reusable strategy, supported conditions, compatible executors and an outcome test. The "
                     "semantic effect is retained; the physical realization is recomputed."),
            "h1": "Skill Block",
            "lede": ("A Skill Block is the unit of reusable robot behaviour in Teach-and-Grow Learning. It "
                     "carries a goal, a reusable strategy, the conditions under which it applies, the executors "
                     "that can realize it, and a test of its effect. What is retained is the semantic effect; the "
                     "physical realization — object bindings, grasp geometry, collision-free motion — is "
                     "recomputed from the current scene each time the block runs."),
            "sections": [
                ("What a demonstration contains, and what is worth keeping", [
                    "A demonstration holds two different things at once: a strategy worth keeping, and physical "
                    "details that belong to one scene. Consider placing a bowl on a plate. Across demonstrations "
                    "the hand may approach from different directions along different paths. The stable part is "
                    "the structure — acquire the requested bowl, establish that it is held, move toward the "
                    "target relation, release it onto the plate. TGL separates that structure from the motion.",
                ]),
                ("The contract", [
                    "A block answers practical questions: what effect is intended, when does it apply, what "
                    "evidence is needed, which executors can realize it, how is success observed, and what "
                    "recovery is allowed? Verification has to refer to the intended physical effect. For an "
                    "acquisition block, a closed gripper alone does not establish that the object is held; the "
                    "test must check the effect the block claims.",
                ]),
                ("Validation before reuse", [
                    "A candidate is evaluated beyond its teaching demonstrations before it is admitted to the "
                    "library. Its supported scope, executor compatibility, outcome test and recovery are checked. "
                    "A weak candidate is narrowed or repaired. This makes library growth an explicit decision "
                    "about a behaviour and the conditions under which it works, rather than a side effect of "
                    "running more episodes.",
                ]),
                ("Where it sits in the loop", [
                    "At execution time the working plan is an ordered composition of blocks, and its remainder "
                    "can change. A passed effect permits the next stage. A failed or inconclusive effect can "
                    "prompt another observation, a different executor, or a revised route. This is the point "
                    "where the agent's reasoning meets physical feedback: what happens next depends on what "
                    "actually happened.",
                ]),
            ],
            "faq": [
                ("Is a Skill Block just a scripted motion?",
                 "No. A scripted motion fixes the trajectory. A Skill Block fixes the intended effect and the "
                 "conditions, and delegates the motion to a compatible executor, so the same block can run in a "
                 "different scene with different geometry."),
                ("How is a Skill Block different from a function call?",
                 "A function call assumes its preconditions hold. A Skill Block states its supported conditions "
                 "and an outcome test, and the execution loop checks the effect before allowing the next stage."),
            ],
            "keywords": ("Skill Block, reusable robot skill, skill contract, robot skill verification, outcome "
                         "test robot, grounded execution, TGL, Teach-and-Grow Learning, agent-centered robot "
                         "learning"),
        },
        "zh": {
            "title": "Skill Block：TGL 中可复用机器人行为的单元",
            "desc": ("Skill Block 是 Teach-and-Grow Learning 中可复用机器人行为的单元：包含目标、可复用策略、"
                     "支持条件、兼容执行器与结果检验。被保留的是语义效果，物理实现则重新计算。"),
            "h1": "Skill Block（技能块）",
            "lede": ("Skill Block 是 Teach-and-Grow Learning 中可复用机器人行为的单元。它携带目标、可复用策略、"
                     "适用条件、能够实现它的执行器，以及对效果的检验。被保留的是语义效果；"
                     "物理实现——物体绑定、抓取几何、无碰撞运动——在每次执行时根据当前场景重新计算。"),
            "sections": [
                ("一次演示里有什么，值得留下什么", [
                    "一次演示同时包含两样不同的东西：值得保留的策略，以及只属于某一个场景的物理细节。"
                    "以把碗放到盘子上为例。在不同演示中，手可能从不同方向沿不同路径接近。稳定的部分是结构——"
                    "获取指定的碗、确认已经拿住、移动到目标关系、把它放到盘子上。TGL 把这一结构与具体动作分开。",
                ]),
                ("契约", [
                    "一个技能块要回答实际问题：意图产生什么效果、何时适用、需要什么证据、哪些执行器能实现它、"
                    "如何观察成功、允许什么恢复？验证必须指向意图中的物理效果。"
                    "对于获取类技能块，仅仅夹爪闭合并不足以说明已经拿住物体；检验必须检查该块所声明的效果。",
                ]),
                ("复用前的验证", [
                    "候选技能块在被纳入技能库之前，要在示教演示之外的情形上评估：检查其支持范围、执行器兼容性、"
                    "结果检验与恢复策略。较弱的候选会被收窄或修复。"
                    "这使技能库的增长成为关于「一个行为及其适用条件」的显式决策，而不是多跑几个回合的副作用。",
                ]),
                ("它在循环中的位置", [
                    "执行时，工作计划是技能块的有序组合，而其余部分可以改变。效果通过就进入下一阶段；"
                    "效果失败或不确定时，可以触发再一次观察、更换执行器，或修改后续路线。"
                    "这正是智能体的推理与物理反馈相遇的地方：接下来做什么，取决于实际发生了什么。",
                ]),
            ],
            "faq": [
                ("Skill Block 只是一段固定动作脚本吗？",
                 "不是。固定脚本规定了轨迹；Skill Block 规定的是意图效果与适用条件，"
                 "并把动作委托给兼容的执行器，因此同一个块可以在几何不同的场景中运行。"),
                ("Skill Block 与函数调用有什么不同？",
                 "函数调用假定前置条件成立。Skill Block 会声明其支持条件与结果检验，"
                 "执行循环在允许进入下一阶段之前会检查效果。"),
            ],
            "keywords": ("Skill Block, 技能块, 可复用机器人技能, 技能契约, 机器人技能验证, 结果检验, "
                         "场景落地执行, TGL, Teach-and-Grow Learning, 以智能体为中心的机器人学习"),
        },
    },
    {
        "slug": "skill-library",
        "parent": "concepts",
        "related": ["skill-block", "experience-memory", "teach-and-grow-learning"],
        "en": {
            "title": "Skill Library: Persistent, Validated Robot Behaviours",
            "desc": ("The Skill Library in Teach-and-Grow Learning is the persistent store of validated Skill "
                     "Blocks: their goals, reusable strategies, supported conditions, compatible executors and "
                     "outcome tests. It grows by validation, not by every episode."),
            "h1": "Skill Library",
            "lede": ("The Skill Library is the persistent store of validated behaviours in Teach-and-Grow "
                     "Learning. It holds Skill Blocks that can be selected and run — their subgoals, supported "
                     "conditions, grounding rules, compatible tools and verification logic — and it grows when a "
                     "candidate passes validation, not every time the robot runs an episode."),
            "sections": [
                ("What the library holds", [
                    "A text description of “how to grasp” is not enough. Each entry has to connect an intent to "
                    "an executor and to a test of its effect, together with the conditions under which the "
                    "behaviour is claimed to work. That combination is what makes an entry selectable and "
                    "runnable rather than merely descriptive, and it is what makes the scope of the claim "
                    "inspectable.",
                ]),
                ("How it grows", [
                    "A candidate block is tested on cases kept separate from the teaching demonstrations. The "
                    "test asks whether it produces the intended effect from the current scene, whether it "
                    "preserves matched old behaviour, and whether it stays within its claimed scope. A weak "
                    "block is narrowed or repaired; a validated one enters a new library version. Library growth "
                    "is therefore a sequence of explicit decisions rather than an accumulation of episodes.",
                ]),
                ("Why growth has a cost", [
                    "Adding a skill locally can avoid reopening the whole learning system — but only if "
                    "grounding, validation, compatibility and retrieval remain manageable. Unrestricted pairwise "
                    "compatibility checks between skills can themselves make the library expensive to grow. The "
                    "paper analyses these different cost regimes instead of treating cheap growth as automatic.",
                ]),
                ("Inspectability", [
                    "Because entries are explicit, a person can narrow an overgeneralised scope, change a "
                    "recovery rule, or mark an executor version as incompatible with a block. Two things are "
                    "deliberately kept apart: storing a behaviour, and that behaviour actually working later. "
                    "The second still depends on retrieval, grounding with current sensing, and successful "
                    "execution.",
                ]),
            ],
            "keywords": ("Skill Library, robot skill library, validated robot behaviours, skill admission, "
                         "versioned robot skills, robot capability library, TGL, Teach-and-Grow Learning, skill "
                         "composition, robot lifelong learning"),
        },
        "zh": {
            "title": "Skill Library：持久化的、经验证的机器人行为库",
            "desc": ("Teach-and-Grow Learning 中的 Skill Library 是经验证 Skill Block 的持久化存储："
                     "包含目标、可复用策略、支持条件、兼容执行器与结果检验。它靠验证增长，而不是靠每个回合增长。"),
            "h1": "Skill Library（技能库）",
            "lede": ("Skill Library 是 Teach-and-Grow Learning 中经验证行为的持久化存储。它保存可被选择与执行的 "
                     "Skill Block——其子目标、支持条件、落地规则、兼容工具与验证逻辑——并且只在候选项通过验证时增长，"
                     "而不是机器人每跑一个回合就增长。"),
            "sections": [
                ("技能库保存什么", [
                    "仅有一段「如何抓取」的文字描述并不够。每一条目都必须把意图连接到执行器，以及对该效果的检验，"
                    "并附上该行为被声明可用的条件。正是这一组合使条目可被选择、可被执行，而不只是描述性的，"
                    "也正是它让声明的适用范围变得可检查。",
                ]),
                ("它如何增长", [
                    "候选技能块会在与示教演示分开保留的情形上接受检验。检验会问：它能否从当前场景产生意图中的效果？"
                    "是否保持了匹配的旧行为？是否停留在所声明的范围内？较弱的块会被收窄或修复；"
                    "通过验证的块进入新的技能库版本。因此技能库的增长是一系列显式决策，而不是回合的堆积。",
                ]),
                ("为什么增长有成本", [
                    "本地新增一个技能可以避免重新打开整个学习系统——但前提是场景落地、验证、兼容性与检索保持可控。"
                    "技能之间不受限制的两两兼容性检查，本身就可能让技能库变得昂贵。"
                    "论文分析的是这些不同的成本情形，而不是把低成本增长视为自动成立。",
                ]),
                ("可检查性", [
                    "由于条目是显式的，人可以收窄过度泛化的范围、修改恢复规则，或标记某个执行器版本与某个块不兼容。"
                    "有两件事被刻意分开：保存了一个行为，与这个行为之后是否真的能跑通。"
                    "后者仍然取决于能否检索到、能否结合当前传感落地，以及能否成功执行。",
                ]),
            ],
            "keywords": ("Skill Library, 技能库, 可复用机器人技能, 经验证机器人行为, 技能入库, "
                         "版本化机器人技能, 机器人能力库, TGL, Teach-and-Grow Learning, 技能组合, 机器人终身学习"),
        },
    },
    {
        "slug": "experience-memory",
        "parent": "concepts",
        "related": ["skill-library", "skill-block", "retraining-tax"],
        "en": {
            "title": "Experience Memory: Recording Why a Robot Attempt Worked or Failed",
            "desc": ("Experience Memory in Teach-and-Grow Learning records the context of an attempt — task, "
                     "selected blocks, observations, outcome, diagnosis and repair — so later decisions can reuse "
                     "the conditions, not only the behaviour."),
            "h1": "Experience Memory",
            "lede": ("Experience Memory records the context of use in Teach-and-Grow Learning: the task, the "
                     "blocks that were selected, the observations, the outcome, the diagnosis, and the repair. It "
                     "is what lets a later decision reuse the conditions surrounding a behaviour, not only the "
                     "behaviour itself."),
            "sections": [
                ("Why behaviour and context are stored separately", [
                    "Solving an episode and acquiring a lasting capability are different events. The Skill "
                    "Library holds what can be executed; Experience Memory holds why it was chosen and what "
                    "happened. A failed attempt may reveal an unsuitable grasp family, an ambiguous observation, "
                    "or a calibration problem — an explanation that guides the next selection without turning "
                    "every episode into a new executable block.",
                ]),
                ("What it changes", [
                    "Memory changes the next decision rather than the next action directly. When a similar "
                    "situation recurs, the recorded outcome and diagnosis inform which block is retrieved and "
                    "which recovery is prepared. This is the mechanism by which a trial becomes useful beyond "
                    "the episode in which it occurred.",
                ]),
                ("Keeping it inspectable", [
                    "The records are searchable, versioned and human-editable. That matters because a robot "
                    "operating over time accumulates conditions that no single demonstration covers — unusual "
                    "contact, an ambiguous view, a gripper that behaves differently after a change. Keeping the "
                    "explanation alongside the outcome makes those cases addressable instead of merely repeated.",
                ]),
                ("Bounded claim", [
                    "Recording an explanation does not guarantee better behaviour. The paper treats memory as an "
                    "input to selection and recovery, and reports studies on how feedback changes decisions; it "
                    "does not claim that retained context alone produces improvement.",
                ]),
            ],
            "keywords": ("Experience Memory, 经验记忆, robot experience memory, robot failure diagnosis, robot "
                         "recovery learning, contextual memory robot, robot long-term memory, TGL, "
                         "Teach-and-Grow Learning, agent-centered robot learning"),
        },
        "zh": {
            "title": "Experience Memory：记录机器人一次尝试为何成功或失败",
            "desc": ("Teach-and-Grow Learning 中的 Experience Memory 记录一次尝试的上下文——任务、所选技能块、"
                     "观测、结果、诊断与修复——使后续决策能够复用条件，而不只是行为。"),
            "h1": "Experience Memory（经验记忆）",
            "lede": ("Experience Memory 记录 Teach-and-Grow Learning 中的使用情境：任务、被选中的技能块、观测、"
                     "结果、诊断与修复。正是它让后续决策能够复用行为周围的条件，而不只是行为本身。"),
            "sections": [
                ("为什么行为与上下文分开存放", [
                    "完成一个回合与获得持久能力是两件不同的事。Skill Library 保存的是可被执行的东西；"
                    "Experience Memory 保存的是它为何被选中、以及实际发生了什么。"
                    "一次失败可能揭示出不合适的抓取方式、含糊的观测，或标定问题——"
                    "这类解释能指导下一次选择，而不必把每个回合都变成新的可执行技能块。",
                ]),
                ("它改变什么", [
                    "记忆直接改变的是下一次决策，而不是下一个动作。当类似情形再次出现时，"
                    "已记录的结果与诊断会影响检索到哪个技能块、准备哪种恢复。"
                    "这就是一次尝试能够在其发生的回合之外继续产生作用的机制。",
                ]),
                ("保持可检查", [
                    "记录是可检索、可版本化、可由人编辑的。这很重要，因为长期运行的机器人会积累没有任何单次演示覆盖过的条件——"
                    "异常接触、含糊的视野、更换之后表现不同的夹爪。"
                    "把解释与结果一起保留下来，能让这些情形变得可处理，而不只是被反复遇到。",
                ]),
                ("有边界的声明", [
                    "记录了解释并不保证行为会变好。论文把记忆作为选择与恢复的输入，并报告了反馈如何改变决策的研究；"
                    "它并不主张仅凭保留的上下文就能带来改进。",
                ]),
            ],
            "keywords": ("Experience Memory, 经验记忆, 机器人经验记忆, 机器人失败诊断, 机器人恢复学习, "
                         "机器人上下文记忆, 机器人长期记忆, TGL, Teach-and-Grow Learning, 以智能体为中心的机器人学习"),
        },
    },
    {
        "slug": "retraining-tax",
        "parent": "concepts",
        "related": ["teach-and-grow-learning", "training-free-robot-learning", "research-context"],
        "en": {
            "title": "The Retraining Tax: The Recurring Cost of Repairing a Robot Policy",
            "desc": ("The retraining tax is the recurring cost of repairing robot behaviour through policy "
                     "updates: new data collection, optimisation, and regression checking against everything the "
                     "policy previously supported. Teach-and-Grow Learning names it and proposes an alternative."),
            "h1": "The Retraining Tax",
            "lede": ("The retraining tax is the recurring cost of repairing robot behaviour through a policy "
                     "update. It includes new data collection, optimisation, and regression checking against "
                     "everything the policy already supported. The term is introduced in the Teach and Grow "
                     "technical report, which uses it to frame an alternative: store the new capability "
                     "explicitly and leave the weights alone."),
            "sections": [
                ("Why the cost recurs", [
                    "End-to-end policies absorb a new behaviour into shared parameters. That is what makes them "
                    "general, and it is also why a local failure rarely has a local fix: adding corrective data "
                    "and changing the parameters does not produce a separately addressable repair for one object "
                    "or one contact condition. Previously supported behaviour may need to be checked again. The "
                    "same applies when a sensor is added or a gripper changed, which introduces observation "
                    "interfaces, calibration and action compatibility to validate.",
                ]),
                ("Why the long tail exposes it", [
                    "The cost is tolerable while changes are broad and infrequent. It becomes visible in the "
                    "long tail, where a rare contact condition or an unusual object needs a specific lesson "
                    "rather than another wide round of experience. The cheaper an individual correction should "
                    "be, the more the shared-parameter route costs relative to it.",
                ]),
                ("What TGL does instead", [
                    "TGL keeps the pretrained stack fixed and stores new capability in explicit objects: Skill "
                    "Blocks with stated scopes and outcome tests, and Experience Memory of the conditions and "
                    "repairs. A correction becomes an edit to one of those objects. The paper analyses when this "
                    "is genuinely cheaper — grounding, validation, compatibility checking and retrieval all have "
                    "to stay manageable — rather than assuming it always is.",
                ]),
                ("How the term should be used", [
                    "The retraining tax is a framing device for a cost structure, not a measured quantity in the "
                    "paper. It is useful for asking, of any robot-learning system, what has to be redone when one "
                    "behaviour is repaired. It should not be quoted as an empirical measurement.",
                ]),
            ],
            "keywords": ("retraining tax, 再训练成本, robot policy retraining cost, cost of updating robot "
                         "policy, robot regression testing, catastrophic forgetting robot, training-free "
                         "alternative, TGL, Teach-and-Grow Learning, robot skill repair"),
        },
        "zh": {
            "title": "再训练成本（Retraining Tax）：修复机器人策略的反复代价",
            "desc": ("再训练成本指通过策略更新修复机器人行为所带来的反复代价：新增数据采集、优化，"
                     "以及对策略此前已支持能力的回归验证。Teach-and-Grow Learning 命名了它，并提出了替代方案。"),
            "h1": "再训练成本（Retraining Tax）",
            "lede": ("再训练成本指通过一次策略更新来修复机器人行为所付出的反复代价，包括新增数据采集、优化，"
                     "以及对策略此前已支持的全部能力做回归验证。该术语由 Teach and Grow 技术报告提出，"
                     "用来引出一种替代方案：把新能力显式存起来，让权重保持不动。"),
            "sections": [
                ("为什么这个代价会反复出现", [
                    "端到端策略把新行为吸收进共享参数。这正是它们具备通用性的原因，也正是局部失败很少有局部修复方案的原因："
                    "追加纠正数据并改动参数，并不会产生一个针对某个物体或某种接触条件的、可单独定位的修复。"
                    "此前已支持的行为可能需要重新检查。新增传感器或更换夹爪时同样如此——"
                    "这会引入需要验证的观测接口、标定与动作兼容性。",
                ]),
                ("为什么长尾会暴露它", [
                    "当改动幅度大且不频繁时，这个代价是可以承受的。它会在长尾中显现："
                    "某种罕见接触条件或某个不寻常的物体，需要的是一条具体的经验，而不是又一轮宽泛的经验积累。"
                    "单次纠正本应越便宜，共享参数路线的相对成本就越高。",
                ]),
                ("TGL 的做法", [
                    "TGL 保持预训练栈不变，把新能力存放在显式对象中：带明确适用范围与结果检验的 Skill Block，"
                    "以及记录条件与修复的 Experience Memory。一次纠正变成对其中某个对象的编辑。"
                    "论文分析的是这种路线在什么条件下才真正更便宜——场景落地、验证、兼容性检查与检索都必须保持可控——"
                    "而不是假定它总是更便宜。",
                ]),
                ("这个术语该怎么用", [
                    "再训练成本是对一种成本结构的框定方式，不是论文中的实测量。"
                    "它适合用来追问：对任何机器人学习系统而言，修复一个行为时需要重做哪些事情。"
                    "不应当把它当作实证测量值引用。",
                ]),
            ],
            "keywords": ("再训练成本, retraining tax, 机器人策略重训成本, 机器人回归测试, 灾难性遗忘, "
                         "免训练替代方案, TGL, Teach-and-Grow Learning, 机器人技能修复, 机器人操作"),
        },
    },
]
