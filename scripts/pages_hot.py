"""Hot-topic pages: the 2026 agentic-robotics query space around TGL.

One hub page plus the concept pages that queries in this space land on. Same
shape as pages.py and pages_extra.py.

Framing rule for this module: these pages describe *patterns* that the 2026
literature and community discussion are converging on, and connect each to TGL.
Where a pattern has a named paper (Code as Policies, SayCan, ReKep) it is cited
with its arXiv identifier. "Agent as Policy" is a named method as of September
2026 — Jia et al., arXiv:2609.12541 — and is cited as such. Every identifier in
this module was checked against the arXiv API; none is invented.
"""

HUB = {
    "slug": "agentic-robotics-2026",
    "parent": "research",
    "schema": ["Article"],
    # The research map discusses every one of these, so it carries the whole set.
    "topics": ["Agentic robotics", "AI agent robotics", "Agent as Policy",
               "Coding agents for robotics", "Physical in-context learning",
               "General-purpose agent robots", "Robot agent memory",
               "Robot learning without retraining", "Runtime reasoning robotics",
               "Tool-using robot agents", "GPT-6 robotics", "Frontier model robotics",
               "Robotic manipulation", "Robot skill libraries", "Physical AI",
               "Vision-language-action models"],
    "related": ["gpt-6-robotic-arm", "agent-as-policy", "physical-in-context-learning"],
    "en": {
        "title": "Agentic Robotics in 2026: GPT-6 Robot Arms, Agent-as-Policy and Teach-and-Grow Learning",
        "desc": ("A research map of the 2026 agentic-robotics landscape: frontier models controlling robot arms, "
                 "agents inside the execution loop, coding agents for robots, physical in-context learning, robot "
                 "memory, and where Teach-and-Grow Learning (TGL) fits."),
        "h1": "Agentic Robotics in 2026: From GPT-6 Robot Arms to Persistent Robot Learning",
        "lede": ("Robot learning in 2026 is being reshaped by frontier multimodal models entering the control loop. "
                 "The recurring pattern is an agent that observes, reasons at runtime, invokes robot tools or "
                 "generated programs, inspects the physical result, and revises. Teach-and-Grow Learning (TGL) "
                 "addresses the complementary problem: what the robot keeps after each of those episodes."),
        "sections": [
            ("1. What changed in robot learning in 2026?", [
                "Two things. First, frontier multimodal models became usable as a reasoning layer for physical "
                "manipulation rather than only for language-level planning. Second, the question shifted from "
                "\"can a model produce an action?\" to \"what does the robot retain?\" — because an agent that "
                "can drive an arm still starts from zero on the next object unless something persists.",
            ]),
            ("2. GPT-6 and frontier models controlling robot arms", [
                "GPT-6-class systems are used as a reasoning layer that interprets visual observations and invokes "
                "robot-control tools or generated programs, rather than emitting joint commands directly. TGL's "
                "implementation uses OpenAI GPT-6 Astra for exactly that role, with Codex connecting the agent to "
                "the robot tools and specialist components handling geometry and control.",
            ]),
            ("3. Agent as Policy", [
                "Agent as Policy (AGP) names a design in which a general-purpose agent sits inside the execution "
                "loop instead of planning offline: it observes the robot and environment, reasons at runtime, "
                "invokes control tools or executable programs, inspects the physical result, and revises its next "
                "action. Jia et al. introduced the term and demonstrated it across real manipulation tasks in "
                "“Agent as Policy for Robotic Manipulation” (arXiv:2609.12541, September 2026). TGL is built "
                "on that loop and adds what the loop does not by itself provide: persistence.",
            ]),
            ("4. Coding agents for robotics", [
                "Coding agents are a good fit for the robot-tool boundary: they can inspect state, call tools, "
                "write and run a short program, and read the result. In TGL, Codex plays this role. The pattern "
                "also has a lineage in program-as-policy work, where a model writes a policy expressed as code "
                "that a robot then executes.",
            ]),
            ("5. Physical in-context learning", [
                "A robot adapts to a new task from context — demonstrations, a video, a written procedure — "
                "without updating model weights. TGL sits in this family, and adds a specific mechanism: the "
                "adapted behaviour is written into explicit stores rather than left in a context window, so it "
                "survives the episode.",
            ]),
            ("6. Single-video task acquisition", [
                "The minimal version of that idea: one video, no teleoperation, no policy training. What a single "
                "video can and cannot supply is the interesting part — it usually reveals the order of operations "
                "while leaving the grasp unresolved, which is exactly the distinction TGL preserves between "
                "semantic structure and robot-specific grounding.",
            ]),
            ("7. Agent memory and experience stores", [
                "Robot-agent memory preserves information from earlier physical interaction for future decisions. "
                "In TGL the split is explicit: the Skill Library holds reusable executable behaviour, while "
                "Experience Memory carries forward success, failure, diagnosis and repair.",
            ]),
            ("8. Skill libraries and reusable robot behaviour", [
                "A skill library is only useful if its entries are runnable and scoped. TGL's unit is the Skill "
                "Block — a goal, a reusable strategy, supported conditions, compatible executors and an outcome "
                "test — and admission to the library is gated on validation outside the teaching demonstrations.",
            ]),
            ("9. Physical feedback and runtime repair", [
                "Execution checks the required effect before allowing the next stage. A passed effect advances the "
                "plan; a failed or inconclusive one prompts another observation, a different executor, or a "
                "revised route. This is what makes a correction local rather than a policy-wide update.",
            ]),
            ("10. VLA, WAM and robot foundation models", [
                "Vision-language-action models and world-action models remain the source of pretrained priors. "
                "TGL does not replace them; it changes where a newly acquired capability is stored, so a repair "
                "does not require re-optimising a policy that also supports everything else.",
            ]),
            ("11. Where Teach-and-Grow Learning fits", [
                "TGL takes the agentic-robotics loop as given and asks what accumulates. Its claim is narrow: "
                "for a robot acquiring tasks over time, storing validated behaviour and the conditions of its use "
                "as explicit objects makes each acquisition local, provided grounding, validation, compatibility "
                "and retrieval stay manageable.",
            ]),
            ("12. Related work timeline", [
                "Language-model planning for robots, program-as-policy approaches, and code-writing agents form "
                "one line. Closed-loop manipulation with spatial or constraint-based reasoning forms another. "
                "Physical in-context adaptation and single-video task acquisition form a third. TGL's contribution "
                "is the persistence layer that sits under all three: an explicit Skill Library and an Experience "
                "Memory that survive the episode.",
            ]),
            ("13. Comparison", [
                "A common pattern across these directions is that the agent is capable but stateless, or the "
                "policy is persistent but not inspectable. TGL's design point is to keep the agent's generality "
                "while making what it learned explicit, versioned and editable by a person.",
            ]),
        ],
        "faq": [
            ("What is the agentic robotics shift in 2026?",
             "Frontier multimodal models moved from planning in language to participating in the robot's "
             "execution loop: observing, invoking tools or generated programs, inspecting physical results and "
             "revising. The open question moved with it — from whether a model can act, to what the robot retains "
             "afterward."),
            ("How is TGL related to GPT-6 robotic-arm systems?",
             "TGL is an instance of one: its implementation uses GPT-6 Astra for task-level reasoning. Its "
             "contribution is the persistence layer around that agent — validated Skill Blocks, a Skill Library "
             "and an Experience Memory."),
            ("Is Agent-as-Policy a specific model?",
             "No. It describes a design in which a general-purpose agent is placed inside the execution loop "
             "rather than restricted to offline planning. TGL follows that design."),
        ],
        "keywords": ("agentic robotics 2026, GPT-6 robotic arm, agent as policy, coding agent robotics, physical "
                     "in-context learning, robot agent memory, robot skill library, agentic robot manipulation, "
                     "physical AI 2026, TGL, Teach-and-Grow Learning"),
    },
    "zh": {
        "title": "2026 智能体机器人：GPT-6 机械臂、Agent as Policy 与 Teach-and-Grow Learning",
        "desc": ("2026 年智能体机器人版图：前沿模型控制机械臂、智能体进入执行回路、机器人 coding agent、"
                 "物理上下文学习、机器人记忆，以及 Teach-and-Grow Learning（TGL）所处的位置。"),
        "h1": "2026 智能体机器人：从 GPT-6 机械臂到可持续积累的机器人学习",
        "lede": ("2026 年的机器人学习正在被进入控制回路的前沿多模态模型重塑。反复出现的模式是："
                 "智能体观察、在运行时推理、调用机器人工具或生成的程序、检查物理结果、然后修正。"
                 "Teach-and-Grow Learning（TGL）处理的是互补的问题：每一次这样的回合之后，机器人到底留下了什么。"),
        "sections": [
            ("一、2026 年机器人学习发生了什么变化", [
                "两件事。第一，前沿多模态模型开始被用作物理操作的推理层，而不只是语言层面的规划。"
                "第二，问题从「模型能否产生一个动作」转向了「机器人留下了什么」——"
                "因为一个能驱动机械臂的智能体，面对下一个物体时仍然从零开始，除非有什么东西被持久保留下来。",
            ]),
            ("二、GPT-6 与前沿模型控制机械臂", [
                "GPT-6 级别的系统被用作推理层：解读视觉观测，并调用机器人控制工具或生成的程序，"
                "而不是直接输出关节指令。TGL 的实现正是用 OpenAI GPT-6 Astra 承担这一角色，"
                "由 Codex 把智能体与机器人工具连接起来，专用组件负责几何与控制。",
            ]),
            ("三、Agent as Policy", [
                "「Agent as Policy」更接近一种设计选择的描述，而不是已经定名的具体方法："
                "智能体位于执行回路之内，而不是只在离线规划。它观察机器人与环境、在运行时推理、"
                "调用控制工具或可执行程序、检查物理结果、修正下一步动作。TGL 建立在这一循环之上。",
            ]),
            ("四、面向机器人的 coding agent", [
                "coding agent 很适合机器人工具的边界：它能检查状态、调用工具、编写并运行一小段程序、读取结果。"
                "在 TGL 中这个角色由 Codex 承担。这一模式也有更早的传承——把策略写成由模型生成、"
                "再由机器人执行的程序。",
            ]),
            ("五、物理上下文学习（Physical In-Context Learning）", [
                "机器人从上下文中适配新任务——演示、一段视频、一份书面流程——而不更新模型权重。"
                "TGL 属于这一族，并增加了一个具体机制：适配后的行为被写入显式存储，"
                "而不是留在上下文窗口里，因此它能活过当前回合。",
            ]),
            ("六、单视频任务获取", [
                "这是同一思路的最小版本：一段视频，没有遥操作，不训练策略。"
                "真正有意思的是「一段视频能提供什么、不能提供什么」——它通常揭示了操作顺序，却没有解决抓取方式。"
                "而 TGL 保留的正是语义结构与机器人特定落地之间的这一区分。",
            ]),
            ("七、智能体记忆与经验存储", [
                "机器人智能体记忆保存早先物理交互中的信息，以供后续决策使用。TGL 把它明确拆成两份："
                "Skill Library 保存可复用的可执行行为，Experience Memory 延续成功、失败、诊断与修复。",
            ]),
            ("八、技能库与可复用机器人行为", [
                "技能库只有在条目可运行、有明确范围时才有用。TGL 的单元是 Skill Block——"
                "目标、可复用策略、支持条件、兼容执行器与结果检验——并且只有在示教演示之外通过验证才被收录。",
            ]),
            ("九、物理反馈与运行时修复", [
                "执行会先检查必要效果，通过后才允许进入下一阶段。效果失败或不确定时，"
                "会触发再一次观察、更换执行器，或修改后续路线。"
                "这正是让一次纠正变成本地编辑、而不是全策略更新的原因。",
            ]),
            ("十、VLA、WAM 与机器人基础模型", [
                "视觉-语言-动作模型与世界动作模型仍然是预训练先验的来源。TGL 不取代它们，"
                "而是改变新获得能力的存放位置，使一次修复不必重新优化一个同时支撑其它一切的策略。",
            ]),
            ("十一、Teach-and-Grow Learning 的位置", [
                "TGL 把智能体机器人循环当作既定前提，追问的是「什么在被积累」。它的主张很窄："
                "对长期获取任务的机器人而言，把经验证的行为及其使用条件存为显式对象，能让每次获取变成本地操作——"
                "前提是场景落地、验证、兼容性与检索保持可控。",
            ]),
            ("十二、相关工作脉络", [
                "面向机器人的语言模型规划、程序即策略、以及会写代码的智能体构成一条线；"
                "带空间或约束推理的闭环操作构成另一条；物理上下文适配与单视频任务获取构成第三条。"
                "TGL 的贡献是位于这三条之下的持久化层：一份显式 Skill Library 与一份 Experience Memory。",
            ]),
            ("十三、对比", [
                "这些方向的一个共同模式是：智能体很有能力但无状态，或者策略持久但不可检查。"
                "TGL 的设计点是同时保留智能体的通用性，并让它学到的东西显式、可版本化、可由人编辑。",
            ]),
        ],
        "faq": [
            ("2026 年智能体机器人的转变是什么？",
             "前沿多模态模型从用语言做规划，转为参与机器人的执行回路：观察、调用工具或生成的程序、"
             "检查物理结果、修正。随之转移的还有那个开放问题——从「模型能否行动」变成「机器人之后留下了什么」。"),
            ("TGL 与 GPT-6 机械臂系统是什么关系？",
             "TGL 就是其中一个实例：它的实现使用 GPT-6 Astra 做任务级推理。它的贡献是围绕该智能体的持久化层——"
             "经验证的 Skill Block、Skill Library 与 Experience Memory。"),
            ("Agent as Policy 是某个具体模型吗？",
             "不是。它描述的是一种设计：把通用智能体放进执行回路，而不是限制在离线规划。TGL 遵循这一设计。"),
        ],
        "keywords": ("2026 智能体机器人, GPT-6 机械臂, agent as policy, 机器人 coding agent, 物理上下文学习, "
                     "机器人智能体记忆, 机器人技能库, 智能体机器人操作, 物理AI 2026, TGL, Teach-and-Grow Learning, "
                     "具身智能 2026"),
    },
}

CONCEPTS = [
    {
        "slug": "gpt-6-robotic-arm",
        "parent": "concepts",
        "related": ["agent-as-policy", "llm-robotics", "ai-agent-robotic-arm", "agentic-robotics-2026"],
        "en": {
            "title": "GPT-6 Robotic Arm: Frontier Models as the Reasoning Layer for Manipulation",
            "desc": ("GPT-6-class robotic-arm systems use a frontier multimodal model as a reasoning layer that "
                     "interprets visual observations and invokes robot-control tools or generated programs. Recent "
                     "2026 demonstrations use GPT-6 Astra for real robot-arm manipulation."),
            "h1": "GPT-6 Robotic Arm",
            "lede": ("A GPT-6 robotic arm is a robot arm whose task-level reasoning comes from a frontier "
                     "multimodal model. The model does not emit joint commands; it interprets visual observations, "
                     "decides what should happen next, and invokes robot-control tools or generated programs. "
                     "Recent 2026 demonstrations use GPT-6 Astra for real robot-arm manipulation."),
            "sections": [
                ("Short answer", [
                    "GPT-6-class robotic-arm systems use a frontier multimodal model as a reasoning layer that "
                    "interprets visual observations and invokes robot-control tools or generated programs. Recent "
                    "2026 demonstrations use GPT-6 Astra for real robot-arm manipulation. TGL addresses a "
                    "complementary problem: retaining and reusing physical capabilities and experience across "
                    "tasks through Skill Blocks, a persistent Skill Library, and Experience Memory.",
                ]),
                ("Key idea", [
                    "The frontier model supplies generality — it can read a scene and a goal it has never seen — "
                    "while the robot-side stack supplies physical competence. Splitting the two is what makes "
                    "either usable: a language model cannot emit torques, and a control policy cannot reason "
                    "about a multi-minute task.",
                ]),
                ("How it works", [
                    "The agent receives camera observations, a goal and the state reported by its tools. It "
                    "chooses a subgoal and a tool, the tool executes, and the result comes back as evidence. The "
                    "agent's next choice depends on that evidence. Where the interface reports only “command "
                    "sent”, the agent cannot distinguish success from failure; where it reports the intended "
                    "physical effect, the agent has something to reason about.",
                ]),
                ("How TGL relates", [
                    "TGL's implementation uses OpenAI GPT-6 Astra for multimodal reasoning and Codex to connect "
                    "the agent to the robot tools, with detection, segmentation, RGB-depth geometry, "
                    "Contact-GraspNet, MPLib and controllers supplying the physical grounding. TGL's own "
                    "contribution is what persists: each subgoal is wrapped in a Skill Block with an outcome "
                    "test, and validated blocks accumulate.",
                ]),
                ("Related work", [
                    "The lineage runs from language-model task planning and program-as-policy approaches — where "
                    "a model writes code that the robot executes — to code-writing agents used as the bridge "
                    "between a frontier model and robot tools. TGL belongs to the branch that adds persistent, "
                    "inspectable stores underneath.",
                ]),
            ],
            "faq": [
                ("Can GPT-6 control a robotic arm?",
                 "Yes — as a reasoning layer rather than a controller. A GPT-6-class model interprets the visual "
                 "scene and decides what should happen, then invokes robot-control tools or writes a short program. "
                 "It does not emit joint commands at control rate; specialist components do that."),
                ("What is a GPT-6 robotic arm?",
                 "The phrase describes a robot arm driven by a GPT-6-class multimodal model: the model supplies "
                 "task-level reasoning and tool selection, while perception, grasping and motion come from robot-side "
                 "components. TGL's implementation uses OpenAI GPT-6 Astra in exactly this role (arXiv:2608.17209)."),
                ("How do frontier AI models control robot arms?",
                 "Three routes appear in the 2026 literature. As a planner, the model produces a sequence that lower "
                 "layers execute. As a policy, it emits actions directly — the vision-language-action route. As an "
                 "agent, it stays in the loop, invoking tools or writing programs and revising on physical outcomes. "
                 "TGL takes the third route."),
                ("How does TGL relate to GPT-6 robotic-arm demonstrations?",
                 "TGL is one such system, and its report is a worked study of the arrangement: GPT-6 Astra reasons, "
                 "Codex connects the agent to the robot tools, and the acquisition of new tasks happens outside the "
                 "weights. The site's paired LIBERO videos show teacher and TGL rollouts on the same tasks."),
                ("How is TGL different from direct frontier-model robot control?",
                 "Direct control asks the model to produce the action. TGL asks it to produce and check a reusable "
                 "procedure: each subgoal becomes a Skill Block with an outcome test, and what validates is stored. "
                 "The model's weights are the same either way; what differs is whether anything persists."),
                ("Can TGL work with stronger future multimodal agents?",
                 "That is the design intent. Nothing in the architecture depends on this particular model — a "
                 "stronger agent should ground subgoals better and diagnose failures better, while the Skill Library "
                 "and Experience Memory carry over unchanged."),
                ("Does GPT-6 directly control the arm?",
                 "No. It supplies task-level reasoning and tool selection. Joint-level geometry and continuous "
                 "control come from specialist components, with the model invoking them."),
                ("What does TGL add to a GPT-6 robotic arm?",
                 "Persistence. TGL wraps each subgoal in a Skill Block with an outcome test, keeps validated "
                 "blocks in a Skill Library, and records conditions, outcomes, diagnoses and repairs in "
                 "Experience Memory, so a later task starts from more than a log."),
            ],
            "keywords": ("GPT-6 robotic arm, GPT-6 robot arm, GPT-6 Astra robot, frontier model robot arm, "
                         "large model robotic arm manipulation, AI agent robot arm, TGL, Teach-and-Grow Learning, "
                         "GPT-6 机械臂"),
        },
        "zh": {
            "title": "GPT-6 机械臂：以前沿模型作为操作的推理层",
            "desc": ("GPT-6 级别的机械臂系统以前沿多模态模型作为推理层：解读视觉观测，并调用机器人控制工具或生成的程序。"
                     "2026 年的演示使用 GPT-6 Astra 完成真实机械臂操作。"),
            "h1": "GPT-6 机械臂",
            "lede": ("GPT-6 机械臂指的是任务级推理由前沿多模态模型承担的机械臂。模型并不输出关节指令，"
                     "而是解读视觉观测、决定下一步该做什么、并调用机器人控制工具或生成的程序。"
                     "2026 年的演示使用 GPT-6 Astra 完成真实机械臂操作。"),
            "sections": [
                ("简述", [
                    "GPT-6 级别的机械臂系统以前沿多模态模型作为推理层：解读视觉观测，调用机器人控制工具或生成的程序。"
                    "2026 年的演示使用 GPT-6 Astra 完成真实机械臂操作。TGL 处理的是互补问题："
                    "通过 Skill Block、持久化的 Skill Library 与 Experience Memory，把物理能力与经验跨任务保留并复用。",
                ]),
                ("核心思路", [
                    "前沿模型提供通用性——它能读懂从未见过的场景与目标；机器人侧栈提供物理能力。"
                    "把两者拆开，才使各自可用：语言模型无法输出力矩，控制策略也无法规划数分钟长的任务。",
                ]),
                ("如何工作", [
                    "智能体接收相机观测、目标，以及工具报告的状态。它选择子目标与工具，工具执行，"
                    "结果作为证据返回。智能体的下一次选择取决于这些证据。"
                    "如果接口只报告「指令已发出」，智能体无法分辨成功与失败；如果它报告意图中的物理效果，"
                    "智能体就有可推理的内容。",
                ]),
                ("TGL 的关系", [
                    "TGL 的实现使用 OpenAI GPT-6 Astra 做多模态推理，用 Codex 把智能体与机器人工具连接起来，"
                    "检测、分割、RGB-D 几何、Contact-GraspNet、MPLib 与控制器提供物理落地。"
                    "TGL 自身的贡献在于「什么被保留下来」：每个子目标被包进带结果检验的 Skill Block，"
                    "通过验证的块持续积累。",
                ]),
                ("相关工作", [
                    "这条脉络从语言模型任务规划、程序即策略（模型写出由机器人执行的代码），"
                    "延伸到把会写代码的智能体用作前沿模型与机器人工具之间的桥梁。"
                    "TGL 属于其中增加了持久、可检查存储的那一支。",
                ]),
            ],
            "faq": [
                ("GPT-6 可以控制机械臂吗？",
                 "可以——但它是作为推理层，而不是控制器。GPT-6 级模型解读视觉场景、决定应当发生什么，"
                 "然后调用机器人控制工具或编写一小段程序。它并不以控制频率输出关节指令，那是专用组件的职责。"),
                ("什么是 GPT-6 机械臂？",
                 "这个说法指的是由 GPT-6 级多模态模型驱动的机械臂：模型提供任务级推理与工具选择，"
                 "感知、抓取与运动由机器人侧组件完成。TGL 的实现正是用 OpenAI GPT-6 Astra 承担这一角色（arXiv:2608.17209）。"),
                ("大模型如何控制机械臂？",
                 "2026 年的文献里出现三条路线。作为规划器：模型产出一段由下层执行的序列。作为策略：直接输出动作，"
                 "即视觉-语言-动作路线。作为智能体：留在回路内，调用工具或编写程序，"
                 "并根据物理结果修正。TGL 走第三条路线。"),
                ("TGL 与 GPT-6 机械臂演示是什么关系？",
                 "TGL 就是这类系统中的一个，其报告是对这种安排的完整研究：GPT-6 Astra 负责推理，"
                 "Codex 把智能体与机器人工具连接起来，新任务的获取发生在权重之外。"
                 "站内的成对 LIBERO 视频展示了同一任务上教师与 TGL 的对照。"),
                ("TGL 与直接用前沿模型控制机器人有何不同？",
                 "直接控制要求模型产出动作；TGL 要求它产出并检查一段可复用的过程——每个子目标变成带结果检验的 Skill Block，"
                 "通过验证的被存下来。两种情况下模型权重相同，区别在于是否有东西被留存。"),
                ("TGL 能配合未来更强的多模态智能体吗？",
                 "这正是设计意图。架构中没有任何部分依赖某一个特定模型——更强的智能体应当能更好地落实子目标、"
                 "更好地诊断失败，而 Skill Library 与 Experience Memory 原样沿用。"),
                ("GPT-6 直接控制机械臂吗？",
                 "不是。它提供任务级推理与工具选择。关节级几何与连续控制由专用组件完成，由模型调用它们。"),
                ("TGL 为 GPT-6 机械臂增加了什么？",
                 "持久性。TGL 把每个子目标包进带结果检验的 Skill Block，把通过验证的块存入 Skill Library，"
                 "并把条件、结果、诊断与修复记入 Experience Memory，使后续任务不只是从一份日志开始。"),
            ],
            "keywords": ("GPT-6 机械臂, GPT-6 机器人, GPT-6 Astra 机器人, 前沿模型机械臂, 大模型机械臂操作, "
                         "AI 智能体机械臂, TGL, Teach-and-Grow Learning"),
        },
    },
    {
        "slug": "agent-as-policy",
        "parent": "concepts",
        "related": ["gpt-6-robotic-arm", "coding-agent-robotics", "general-purpose-agent-robot", "agentic-robotics-2026"],
        "en": {
            "title": "Agent as Policy (AGP): A General Agent Inside the Robot's Execution Loop",
            "desc": ("Agent as Policy (AGP) puts a general-purpose AI agent inside the robot's execution loop instead "
                     "of limiting it to offline planning. Named and demonstrated by Jia et al., arXiv:2609.12541, 2026."),
            "h1": "Agent as Policy (AGP)",
            "lede": ("Agent as Policy (AGP) places a general-purpose AI agent inside the execution loop rather than "
                     "limiting it to offline planning. The agent observes the robot and environment, reasons at "
                     "runtime, invokes control tools or executable programs, inspects the physical result, and "
                     "revises its next action. Jia et al. named the approach and demonstrated it on real "
                     "manipulation tasks in September 2026."),
            "sections": [
                ("Short answer", [
                    "Agent-as-Policy robotics places a general-purpose AI agent inside the execution loop rather than "
                    "limiting it to offline planning. The agent observes the robot and environment, reasons at "
                    "runtime, invokes control tools or executable programs, inspects the physical result, and "
                    "revises its next action.",
                ]),
                ("Where the name comes from", [
                    "“Agent as Policy for Robotic Manipulation” (Jia et al., <a href='https://arxiv.org/abs/2609.12541' "
                    "target='_blank' rel='noopener'>arXiv:2609.12541</a>, September 2026) introduces AGP and shows a "
                    "general-purpose agent driving a physical robot through task execution with no task-specific or "
                    "environment-specific training. Given a task and a robot interface, the agent interprets visual "
                    "evidence, writes executable programs, issues motion commands, and revises its actions in response "
                    "to physical outcomes — across precision manipulation, dynamic motions and deformable-object tasks.",
                    "The contrast is with the foundation-policy line, where a vision-language-action model maps "
                    "observations to actions directly. AGP keeps the agent running in the loop and gives it programs "
                    "and tools rather than joint targets.",
                ]),
                ("Key idea", [
                    "What distinguishes the placement is where the deciding component sits: outside the loop, producing "
                    "a plan that lower layers execute, or inside it, reacting to what the robot actually observed. "
                    "Physical execution produces evidence — a failed grasp, an object that moved, a drawer that stayed "
                    "shut — and only a component that is still running can act on it.",
                    "The cost is latency and cost per step. Reasoning on every action is far more expensive than "
                    "feed-forward inference, which is why the placement tends to be reserved for novelty: unfamiliar "
                    "objects, diagnosis and recovery.",
                ]),
                ("Current examples", [
                    "<b>Agent as Policy (AGP)</b> — Jia et al., <a href='https://arxiv.org/abs/2609.12541' target='_blank' "
                    "rel='noopener'>arXiv:2609.12541</a>, 2026: a general agent drives a real robot across manipulation "
                    "tasks with no task-specific training.",
                    "<b>Agentic Robot</b> — Yang et al., <a href='https://arxiv.org/abs/2505.23450' target='_blank' "
                    "rel='noopener'>arXiv:2505.23450</a>, 2025: a framework for vision-language-action models that adds "
                    "an action-coordination protocol and execution-time verification for long-horizon manipulation.",
                    "<b>Push-T with agentic robotics</b> — Xie, Chen and Goldberg, <a href='https://arxiv.org/abs/2608.18227' "
                    "target='_blank' rel='noopener'>arXiv:2608.18227</a>, 2026: an LLM coding agent writes a solution to "
                    "Push-T with no demonstration data, compared against a visuomotor imitation policy.",
                    "<b>Code as Policies</b> — Liang et al., <a href='https://arxiv.org/abs/2209.07753' target='_blank' "
                    "rel='noopener'>arXiv:2209.07753</a>, 2022: the program-as-policy predecessor, where a language model "
                    "writes policy code over perception primitives.",
                    "<b>SayCan</b> — Ahn et al., <a href='https://arxiv.org/abs/2204.01691' target='_blank' rel='noopener'>"
                    "arXiv:2204.01691</a>, 2022: grounding language-model plans in what the robot can actually do.",
                    "<b>ReKep</b> — Huang et al., <a href='https://arxiv.org/abs/2409.01652' target='_blank' rel='noopener'>"
                    "arXiv:2409.01652</a>, 2024: relational keypoint constraints for closed-loop manipulation — a "
                    "spatial-reasoning route to the same problem.",
                ]),
                ("Agent as Policy compared with Teach-and-Grow Learning", [
                    "The two share the control locus — an agent inside the loop — and differ on what persists. Across the "
                    "dimensions that matter for a robot acquiring tasks over time:",
                    "<b>Control locus</b>: identical. Both keep the agent inside the execution loop.",
                    "<b>Task acquisition</b>: AGP acquires from the task description and the robot interface; TGL "
                    "acquires from sparse demonstrations, which supply subgoal structure and the conditions worth checking.",
                    "<b>Runtime reasoning</b>: identical. Both reason while the task runs.",
                    "<b>Skill persistence</b>: AGP does not define a persistent store; in TGL, validated behaviour enters "
                    "a Skill Library as Skill Blocks.",
                    "<b>Memory</b>: AGP carries state within the task; TGL keeps a separate Experience Memory of outcome, "
                    "diagnosis and repair across tasks.",
                    "<b>Experience reuse</b>: AGP re-derives a solution on a repeat task; TGL retrieves the validated block.",
                    "<b>Demonstration use</b>: AGP requires none; TGL uses a few.",
                    "<b>Task-specific retraining</b>: neither updates the policy — this is the shared claim.",
                    "<b>Physical feedback</b>: both inspect the physical outcome; TGL makes the effect check part of each "
                    "Skill Block's contract.",
                    "<b>Future-task transfer</b>: TGL's explicit claim and the report's scaling hypothesis; not a claim AGP makes.",
                ]),
                ("How TGL relates", [
                    "TGL follows the Agent-as-Policy design and adds the persistence layer. The agent orders subgoals, "
                    "chooses tools and revises the route; validated behaviour accumulates in a Skill Library, and the "
                    "conditions, outcomes, diagnoses and repairs of each attempt accumulate in Experience Memory. The "
                    "report's slow-teacher/fast-student split lets a learned policy take over mature behaviours, "
                    "keeping agentic deliberation for novelty.",
                ]),
            ],
            "faq": [
                ("Is Agent as Policy the same as using an LLM for planning?",
                 "Not quite. Planning puts the model before execution and commits to a plan. Agent as Policy keeps it "
                 "running during execution, so it can inspect physical results and revise."),
                ("Does Agent as Policy require task-specific training?",
                 "No — that is its central claim. Jia et al. demonstrate a general-purpose agent driving a physical robot "
                 "through task execution with no task-specific or environment-specific training."),
                ("Can a general-purpose AI agent directly control a physical robot?",
                 "Yes, and this is the central demonstration of AGP: Jia et al. show a general-purpose agent driving "
                 "a physical robot through task execution with no task-specific or environment-specific training. What "
                 "it produces is executable programs and motion commands through a robot interface, not joint torques."),
                ("How does TGL relate to Agent as Policy?",
                 "TGL adopts the same loop and adds the persistence layer. The agent orders subgoals and revises on "
                 "physical feedback in both; in TGL, validated behaviour also enters a Skill Library and each attempt's "
                 "diagnosis enters Experience Memory, so a repeat task starts from what the first one established."),
                ("Does the agent produce actions or programs?",
                 "Typically programs or tool calls rather than joint targets. In a code-writing variant the agent produces "
                 "a program that a robot-side layer executes; in a tool-calling variant it selects subgoals and invokes "
                 "control primitives."),
            ],
            "keywords": ("agent as policy, AGP, agent as policy for robotic manipulation, agentic policy robotics, "
                         "AI agent execution loop, runtime reasoning robot, general agent robot control, embodied agent "
                         "policy, arXiv 2609.12541, TGL, Teach-and-Grow Learning, agent 即策略"),
        },
        "zh": {
            "title": "Agent as Policy（AGP）：把通用智能体放进机器人的执行回路",
            "desc": ("Agent as Policy（AGP）把通用 AI 智能体放进机器人的执行回路，而不是把它限制在离线规划。"
                     "该术语由 Jia 等人在 arXiv:2609.12541（2026）中提出并在真实操作任务上验证。"),
            "h1": "Agent as Policy（AGP，智能体即策略）",
            "lede": ("Agent as Policy（AGP）把通用 AI 智能体放在执行回路之内，而不是把它限制在离线规划。"
                     "智能体观察机器人与环境、在运行时推理、调用控制工具或可执行程序、检查物理结果、修正下一步动作。"
                     "Jia 等人在 2026 年 9 月为该方法命名，并在真实操作任务上做了验证。"),
            "sections": [
                ("简述", [
                    "Agent-as-Policy 机器人学把通用 AI 智能体放进执行回路，而不是把它限制在离线规划。"
                    "智能体观察机器人与环境、在运行时推理、调用控制工具或可执行程序、检查物理结果、修正下一步动作。",
                ]),
                ("这个名字从何而来", [
                    "《Agent as Policy for Robotic Manipulation》（Jia 等人，"
                    "<a href='https://arxiv.org/abs/2609.12541' target='_blank' rel='noopener'>arXiv:2609.12541</a>，"
                    "2026 年 9 月）提出 AGP，并展示了通用智能体在无需任务特定或环境特定训练的条件下驱动物理机器人完成任务："
                    "给定任务与机器人接口，智能体解读视觉证据、编写可执行程序、发出运动指令，"
                    "并根据物理结果修正动作——覆盖精细操作、动态运动与可变形物体任务。",
                    "与之对照的是基础策略（foundation policy）路线：视觉-语言-动作模型把观测直接映射为动作。"
                    "AGP 让智能体留在回路内，交给它的是程序与工具，而不是关节目标。",
                ]),
                ("核心思想", [
                    "区别在于做决定的组件所处的位置：在回路之外，产出一份由下层执行的计划；"
                    "或者在回路之内，对机器人实际观察到的内容作出反应。"
                    "物理执行会产生证据——一次失败的抓取、一个被移动的物体、一个没有打开的抽屉——"
                    "而只有仍在运行的组件才能对它采取行动。",
                    "代价是延迟与每步成本。对每个动作都推理，远比前馈推理昂贵，"
                    "这也是为什么这种安排通常留给陌生情形：不熟悉的物体、诊断与恢复。",
                ]),
                ("当前工作实例", [
                    "<b>Agent as Policy（AGP）</b>——Jia 等人，"
                    "<a href='https://arxiv.org/abs/2609.12541' target='_blank' rel='noopener'>arXiv:2609.12541</a>，"
                    "2026：通用智能体在无需任务特定训练的条件下驱动真实机器人完成操作任务。",
                    "<b>Agentic Robot</b>——Yang 等人，"
                    "<a href='https://arxiv.org/abs/2505.23450' target='_blank' rel='noopener'>arXiv:2505.23450</a>，"
                    "2025：面向视觉-语言-动作模型的框架，为长时程操作加入动作协调协议与执行期验证。",
                    "<b>Push-T 与智能体机器人</b>——Xie、Chen、Goldberg，"
                    "<a href='https://arxiv.org/abs/2608.18227' target='_blank' rel='noopener'>arXiv:2608.18227</a>，"
                    "2026：LLM coding agent 在没有任何演示数据的条件下写出 Push-T 的解法，并与视觉运动模仿策略对比。",
                    "<b>Code as Policies</b>——Liang 等人，"
                    "<a href='https://arxiv.org/abs/2209.07753' target='_blank' rel='noopener'>arXiv:2209.07753</a>，"
                    "2022：程序即策略的前身，语言模型在感知原语之上写出策略代码。",
                    "<b>SayCan</b>——Ahn 等人，"
                    "<a href='https://arxiv.org/abs/2204.01691' target='_blank' rel='noopener'>arXiv:2204.01691</a>，"
                    "2022：把语言模型的计划落到机器人真正做得到的事情上。",
                    "<b>ReKep</b>——Huang 等人，"
                    "<a href='https://arxiv.org/abs/2409.01652' target='_blank' rel='noopener'>arXiv:2409.01652</a>，"
                    "2024：面向闭环操作的关系关键点约束，是解决同一问题的空间推理路线。",
                ]),
                ("Agent as Policy 与 Teach-and-Grow 的对比", [
                    "两者共享同一控制位置——智能体在回路之内——差别在于什么被留存下来。"
                    "就一个需要长期获取任务的机器人而言，可以从这些维度比较：",
                    "<b>控制位置</b>：相同。两者都把智能体留在执行回路内。",
                    "<b>任务获取</b>：AGP 从任务描述与机器人接口获取；TGL 从少量演示获取，"
                    "演示提供子目标结构与值得检查的条件。",
                    "<b>运行时推理</b>：相同。两者都在任务运行期间推理。",
                    "<b>技能持久化</b>：AGP 未定义持久存储；在 TGL 中，经验证的行为以 Skill Block 的形式进入 Skill Library。",
                    "<b>记忆</b>：AGP 在任务内携带状态；TGL 另设 Experience Memory，跨任务保存结果、诊断与修复。",
                    "<b>经验复用</b>：AGP 在重复任务上重新推导解法；TGL 检索已验证的技能块。",
                    "<b>演示的使用</b>：AGP 不需要演示；TGL 使用少量演示。",
                    "<b>任务特定重训</b>：两者都不更新策略——这是共同的立场。",
                    "<b>物理反馈</b>：两者都会检查物理结果；TGL 把效果检验写进每个 Skill Block 的契约。",
                    "<b>向未来任务迁移</b>：这是 TGL 的明确主张与报告中的缩放假设；AGP 并未提出这一点。",
                ]),
                ("TGL 的关系", [
                    "TGL 遵循 Agent-as-Policy 的设计，并加上持久化层。智能体排列子目标、选择工具、修正路线；"
                    "经验证的行为积累在 Skill Library，每次尝试的条件、结果、诊断与修复积累在 Experience Memory。"
                    "报告提出的「慢教师–快学生」拆分，会随后让学习到的策略接手成熟行为，"
                    "把智能体式的深思留给陌生情形。",
                ]),
            ],
            "faq": [
                ("Agent as Policy 与用 LLM 做规划是一回事吗？",
                 "不完全是。规划把模型放在执行之前，并对一份计划作出承诺；"
                 "Agent as Policy 让它在执行期间持续运行，因此可以检查物理结果并修正。"),
                ("Agent as Policy 需要任务特定训练吗？",
                 "不需要，这正是它的核心主张。Jia 等人展示了通用智能体在无需任务特定或环境特定训练的条件下驱动物理机器人完成任务。"),
                ("AI 智能体可以直接控制真实机器人吗？",
                 "可以，这正是 AGP 的核心展示：Jia 等人表明通用智能体在无需任务特定或环境特定训练的条件下"
                 "驱动物理机器人完成任务。它产出的是可执行程序与通过机器人接口发出的运动指令，而不是关节力矩。"),
                ("TGL 与 Agent as Policy 是什么关系？",
                 "TGL 采用同一个回路，并加上持久化层。两者都由智能体排列子目标并根据物理反馈修正；"
                 "在 TGL 中，通过验证的行为还会进入 Skill Library，每次尝试的诊断进入 Experience Memory，"
                 "因此重复任务会从第一次已确立的东西开始。"),
                ("智能体产出的是动作还是程序？",
                 "通常是程序或工具调用，而不是关节目标。在写代码的变体中，智能体产出一段由机器人侧执行的程序；"
                 "在工具调用的变体中，它选择子目标并调用控制原语。"),
            ],
            "keywords": ("agent as policy, AGP, 智能体即策略, agent as policy for robotic manipulation, "
                         "智能体执行回路, 运行时推理机器人, 通用智能体机器人控制, 具身智能体策略, "
                         "arXiv 2609.12541, TGL, Teach-and-Grow Learning"),
        },
    },
    {
        "slug": "coding-agent-robotics",
        "parent": "concepts",
        "related": ["agent-as-policy", "tool-use-robotics", "gpt-6-robotic-arm", "agentic-robotics-2026"],
        "en": {
            "title": "Coding Agents for Robotics: Models That Write and Run Robot Programs",
            "desc": ("Coding agents inspect state, call tools, write and run short programs, and read the result. "
                     "That loop fits the boundary between a frontier model and a robot's control stack, and it is "
                     "the role Codex plays in Teach-and-Grow Learning."),
            "h1": "Coding Agents for Robotics",
            "lede": ("A coding agent inspects the current state, calls tools, writes and runs a short program, and "
                     "reads what came back. That loop maps unusually well onto the boundary between a frontier "
                     "model and a robot's control stack, because what a robot needs from a model is rarely a "
                     "single instruction and often a small procedure."),
            "sections": [
                ("Why the pattern fits robotics", [
                    "Robot tasks involve a sequence of geometric operations with checks between them: perceive, "
                    "verify held, move, verify placement. Expressing that as a short program the agent writes — "
                    "rather than as a stream of separate model calls — reduces round trips, makes the sequence "
                    "inspectable, and lets deterministic code run the parts that do not need reasoning.",
                    "It also gives the agent a natural way to handle state: a program can hold intermediate "
                    "results, and its output is something the agent can read back.",
                ]),
                ("The lineage", [
                    "This is not a new idea in robotics. Program-as-policy approaches had a model write a policy "
                    "expressed as code, with perception primitives supplied as callable functions. What changed is "
                    "the capability of the coding model and the quality of the tool interfaces it is given.",
                ]),
                ("Where it breaks", [
                    "Generated code assumes its preconditions hold. A program that assumes a successful grasp will "
                    "continue into a failed placement rather than stopping, unless the primitives it calls report "
                    "the effects it depends on. That is why the interface matters more than the code: a program is "
                    "only as correct as the evidence its tools return.",
                ]),
                ("How TGL relates", [
                    "In Teach-and-Grow Learning, Codex connects the agent to the robot tools, and each subgoal is "
                    "wrapped in a Skill Block with an outcome test rather than being assumed to succeed. Generic "
                    "verification — “did the gripper close?” — is not treated as proof that the intended physical "
                    "effect occurred.",
                ]),
            ],
            "faq": [
                ("What is a coding agent for robotics?",
                 "A model that inspects the robot's state, calls tools, writes and runs a short program, and reads "
                 "the result. It fits robotics because a robot usually needs a small procedure rather than a single "
                 "instruction, and because a program can hold intermediate results between steps."),
                ("Can Codex-style agents control robots?",
                 "They can drive one through tools, but they do not produce control-rate joint commands. In TGL, "
                 "Codex connects the agent to the robot tools, while detection, RGB-D geometry, Contact-GraspNet, "
                 "MPLib and controllers do the physical work."),
                ("How does TGL relate to coding agents?",
                 "Codex is the coding agent in TGL's implementation. What TGL adds is the contract around each call: "
                 "a subgoal is wrapped in a Skill Block with a stated effect and an outcome test, so running a "
                 "program is not the same as assuming it worked."),
            ],
            "keywords": ("coding agent robotics, code as policy, LLM writes robot code, Codex robotics, program "
                         "synthesis robot manipulation, code-writing agent robot, TGL, Teach-and-Grow Learning, "
                         "代码智能体机器人"),
        },
        "zh": {
            "title": "面向机器人的 coding agent：会写并运行机器人程序的模型",
            "desc": ("coding agent 检查状态、调用工具、编写并运行一小段程序、读取结果。这一循环与前沿模型和机器人控制栈之间的边界高度契合，"
                     "也正是 Codex 在 Teach-and-Grow Learning 中承担的角色。"),
            "h1": "面向机器人的 Coding Agent",
            "lede": ("coding agent 检查当前状态、调用工具、编写并运行一小段程序、读取返回的内容。"
                     "这一循环与「前沿模型 ↔ 机器人控制栈」之间的边界格外契合，"
                     "因为机器人从模型那里需要的很少是一条单指令，往往是一小段过程。"),
            "sections": [
                ("为什么这个模式适合机器人", [
                    "机器人任务包含一串几何操作，其间还有检查：感知、确认已拿住、移动、确认已放置。"
                    "把它表达为由智能体编写的一小段程序，而不是一串彼此独立的模型调用，"
                    "能减少往返、让序列可检查，并让确定性的代码去跑那些不需要推理的部分。",
                    "它还给智能体一个自然的处理状态的方式：程序可以保存中间结果，其输出是智能体可以读回的。",
                ]),
                ("脉络", [
                    "这在机器人领域不是新想法。程序即策略的工作让模型写出以代码表达的策略，"
                    "感知原语以可调用函数的形式提供。变化的是 coding agent 自身的能力，"
                    "以及提供给它的工具接口的质量。",
                ]),
                ("它在什么地方失效", [
                    "生成的代码假定自己的前置条件成立。一段假定抓取成功的程序，会继续走向失败的放置，"
                    "而不是停下来——除非它调用的原语报告了它所依赖的效果。"
                    "这就是为什么接口比代码更重要：程序只能和它工具返回的证据一样正确。",
                ]),
                ("TGL 的关系", [
                    "在 Teach-and-Grow Learning 中，Codex 把智能体与机器人工具连接起来，"
                    "每个子目标都被包进带结果检验的 Skill Block，而不是默认为成功。"
                    "通用式的验证——「夹爪闭合了吗？」——不被当作意图物理效果已发生的证明。",
                ]),
            ],
            "faq": [
                ("什么是面向机器人的 coding agent？",
                 "指会检查机器人状态、调用工具、编写并运行一小段程序、再读取结果的模型。"
                 "它适合机器人，是因为机器人需要的通常是一小段过程而不是一条指令，"
                 "也因为程序能在步骤之间保存中间结果。"),
                ("Codex 这类智能体能控制机器人吗？",
                 "它们能通过工具驱动机器人，但不会输出控制频率的关节指令。在 TGL 中，"
                 "Codex 把智能体与机器人工具连接起来，而检测、RGB-D 几何、Contact-GraspNet、"
                 "MPLib 与控制器负责物理执行。"),
                ("TGL 与 coding agent 是什么关系？",
                 "Codex 就是 TGL 实现中的 coding agent。TGL 增加的是每次调用周围的契约："
                 "子目标被包进带声明效果与结果检验的 Skill Block，"
                 "因此「运行了程序」与「假定它成功了」不是同一件事。"),
            ],
            "keywords": ("面向机器人的 coding agent, 代码即策略, 大模型写机器人代码, Codex 机器人, "
                         "程序合成机器人操作, 代码智能体机器人, TGL, Teach-and-Grow Learning"),
        },
    },
    {
        "slug": "physical-in-context-learning",
        "parent": "concepts",
        "related": ["no-retraining-robot-learning", "agent-as-policy", "robot-agent-memory", "agentic-robotics-2026"],
        "en": {
            "title": "Physical In-Context Learning: Adapting a Robot Without Updating Weights",
            "desc": ("Physical in-context learning lets a robot adapt to a new task from context — demonstrations, "
                     "video, a written procedure — without updating model weights. TGL stores the reusable "
                     "behaviour and experience persistently so learning accumulates across tasks."),
            "h1": "Physical In-Context Learning",
            "lede": ("Physical in-context learning lets a robot adapt to a new task from context such as "
                     "demonstrations or video, without updating the underlying model weights. The adaptation "
                     "happens in what the model is conditioned on rather than in what it stores."),
            "sections": [
                ("Short answer", [
                    "Physical in-context learning lets a robot adapt to a new task from context such as "
                    "demonstrations or video without updating the underlying model weights. TGL complements this "
                    "direction by storing reusable behavior and structured physical experience persistently so "
                    "that learning can accumulate across tasks.",
                ]),
                ("What the context can carry", [
                    "A few demonstrations can convey a subgoal sequence and the conditions worth checking. Video "
                    "can convey the order of operations. A written procedure can convey constraints and "
                    "affordances. None of them conveys the physical realization — the pose, grasp and motion the "
                    "current scene requires — which has to be recovered on the robot.",
                    "That gap is why in-context adaptation works better for some tasks than others. Where the "
                    "hard part is knowing what to do, context is enough. Where the hard part is doing it, context "
                    "is only a starting point.",
                ]),
                ("The durability question", [
                    "Context is scoped to a session. When it is gone, so is the adaptation, unless something "
                    "outside the context window recorded it. A robot that adapts well but retains nothing repeats "
                    "the same adaptation on the next object.",
                    "This is the point at which in-context learning meets the memory question: what should survive "
                    "the episode, and in what form.",
                ]),
                ("How TGL relates", [
                    "TGL treats context as the starting point and stores the outcome. The agent reads the "
                    "demonstrations for structure, grounds each subgoal in the current scene, checks the physical "
                    "effect, and keeps what validated — as a Skill Block in the Skill Library, with the conditions "
                    "and repairs of the attempt in Experience Memory. The adaptation therefore persists after the "
                    "context that produced it is gone.",
                ]),
            ],
            "faq": [
                ("Can a robot learn a task from one video without retraining?",
                 "It can acquire the structure of the task that way — the order of operations and the conditions "
                 "worth checking — and no weights need to change. What the video does not supply is the physical "
                 "realization: the pose, grasp and motion this scene requires. TGL's answer is to ground each "
                 "subgoal on the robot and keep what validated."),
                ("What is the difference between physical ICL and lifelong robot learning?",
                 "Lifelong learning asks how a system keeps acquiring tasks without forgetting; physical ICL asks "
                 "how a task is acquired without a weight update. They are different axes. TGL sits on both: the "
                 "acquisition is in-context and the retention is explicit."),
            ],
            "keywords": ("physical in-context learning, in-context robot adaptation, robot adaptation without "
                         "weights, few-shot robot adaptation, context-conditioned robot policy, robot imitation "
                         "context, TGL, Teach-and-Grow Learning, 物理上下文学习"),
        },
        "zh": {
            "title": "物理上下文学习：不更新权重地适配机器人",
            "desc": ("物理上下文学习让机器人从上下文——演示、视频、书面流程——适配新任务，而不更新模型权重。"
                     "TGL 通过持久保存可复用行为与结构化物理经验来补充这一方向，使学习能跨任务积累。"),
            "h1": "物理上下文学习（Physical In-Context Learning）",
            "lede": ("物理上下文学习让机器人从演示或视频这样的上下文中适配新任务，而不更新底层模型权重。"
                     "适配发生在模型被「条件化」的内容里，而不是它存储的内容里。"),
            "sections": [
                ("简述", [
                    "物理上下文学习让机器人从上下文——演示、视频、书面流程——适配新任务，而不更新底层模型权重。"
                    "TGL 通过持久保存可复用行为与结构化物理经验来补充这一方向，使学习能跨任务积累。",
                ]),
                ("上下文能承载什么", [
                    "少量演示可以传达子目标序列与值得检查的条件；视频可以传达操作顺序；"
                    "书面流程可以传达约束与可供性。它们都不传达物理实现——当前场景所需的位姿、抓取与运动——"
                    "而这必须在机器人上重新求取。",
                    "这一落差正是上下文适配对某些任务效果更好、对另一些更差的原因。"
                    "如果难的是「知道该做什么」，上下文就够了；如果难的是「做到它」，上下文只是起点。",
                ]),
                ("持久性问题", [
                    "上下文的作用域是一次会话。它消失时，适配也随之消失——除非上下文窗口之外的某个东西记录了它。"
                    "一个适配得很好但不保留任何东西的机器人，会在下一个物体上重复同样的适配。",
                    "这正是上下文学习遇到记忆问题的地方：什么应当活过这个回合，以什么形式。",
                ]),
                ("TGL 的关系", [
                    "TGL 把上下文当作起点，把结果存下来。智能体从演示中读取结构，把每个子目标落实到当前场景，"
                    "检查物理效果，并保留通过验证的部分——作为 Skill Library 中的 Skill Block，"
                    "同时把这次尝试的条件与修复记入 Experience Memory。"
                    "因此适配在产生它的上下文消失之后依然存在。",
                ]),
            ],
            "faq": [
                ("机器人可以只看一个视频就学会新任务吗？",
                 "可以借此获得任务的结构——操作顺序与值得检查的条件——并且无需改变任何权重。"
                 "视频提供不了的是物理实现：当前场景所需的位姿、抓取与运动。"
                 "TGL 的答案是：把每个子目标落到机器人上，并保留通过验证的部分。"),
                ("物理上下文学习与终身机器人学习有什么不同？",
                 "终身学习问的是系统如何在不遗忘的前提下持续获取任务；物理上下文学习问的是如何在不更新权重的前提下获取任务。"
                 "这是两个不同的轴。TGL 同时落在两者上：获取在上下文内完成，留存是显式的。"),
            ],
            "keywords": ("物理上下文学习, 上下文机器人适配, 不更新权重的机器人适配, 少样本机器人适配, "
                         "上下文条件化机器人策略, TGL, Teach-and-Grow Learning, physical in-context learning"),
        },
    },
    {
        "slug": "general-purpose-agent-robot",
        "parent": "concepts",
        "related": ["agent-as-policy", "ai-agent-robotic-arm", "general-robot-learning", "agentic-robotics-2026"],
        "en": {
            "title": "General-Purpose Agent Robots: One Agent, Many Tasks, and What It Retains",
            "desc": ("A general-purpose agent robot uses one reasoning agent across many tasks. Its openness is "
                     "the point, and its statelessness is the limit — Teach-and-Grow Learning gives such an agent "
                     "persistent, inspectable memory."),
            "h1": "General-Purpose Agent Robots",
            "lede": ("A general-purpose agent robot uses a single reasoning agent across many tasks rather than a "
                     "task-specific program. That generality is the appeal: the same agent can read a new goal and "
                     "a new scene. The limit is that a general agent is stateless by default, so what it learned "
                     "on one task does not carry to the next."),
            "sections": [
                ("What generality buys", [
                    "A general agent does not need to be rebuilt for a new task. It reads the scene and the goal, "
                    "decides on a subgoal and a tool, and acts. That removes the per-task engineering that "
                    "dominates classical automation, where each new object tends to mean a new program.",
                ]),
                ("What it does not buy", [
                    "Generality of reasoning is not retained capability. Ask the same agent to repeat yesterday's "
                    "task and it re-derives the same solution from scratch, at the same cost, with the same chance "
                    "of the same failure. Nothing about having solved it once makes it easier the second time.",
                    "That is a specific and fixable limitation, and it is distinct from the model's competence. "
                    "The agent is not worse at the task; it simply has nowhere to keep the answer.",
                ]),
                ("What would change it", [
                    "Somewhere to put validated behaviour, with enough structure that it can be retrieved and "
                    "checked rather than merely replayed; and somewhere to record why an attempt went the way it "
                    "did. Both need to be inspectable, because a general agent operating over time accumulates "
                    "conditions no single demonstration covered.",
                ]),
                ("How TGL relates", [
                    "TGL supplies exactly those two places. Validated behaviours enter the Skill Library with a "
                    "stated scope and an outcome test; conditions, outcomes, diagnoses and repairs enter "
                    "Experience Memory. The agent keeps its generality, and the second attempt at a task starts "
                    "from what the first one established.",
                ]),
            ],
            "keywords": ("general-purpose agent robot, generalist robot agent, AI agent robot, universal robot "
                         "agent, agent robot tasks, embodied general agent, TGL, Teach-and-Grow Learning, "
                         "通用智能体机器人"),
        },
        "zh": {
            "title": "通用智能体机器人：一个智能体、多种任务，以及它保留了什么",
            "desc": ("通用智能体机器人用同一个推理智能体处理多种任务。它的开放性是优点，无状态是局限——"
                     "Teach-and-Grow Learning 为这样的智能体提供持久、可检查的记忆。"),
            "h1": "通用智能体机器人",
            "lede": ("通用智能体机器人用单个推理智能体处理多种任务，而不是为每个任务写一段专用程序。"
                     "这种通用性正是吸引力所在：同一个智能体可以读懂新目标与新场景。"
                     "局限在于通用智能体默认是无状态的，它在一个任务上学到的东西不会带到下一个。"),
            "sections": [
                ("通用性换来了什么", [
                    "通用智能体不必为新任务重建。它读取场景与目标，决定子目标与工具，然后行动。"
                    "这消除了按任务逐个工程化的负担——在经典自动化中，每换一个物体往往就意味着换一段程序。",
                ]),
                ("它换不来什么", [
                    "推理的通用性不等于被保留的能力。让同一个智能体重复昨天的任务，它会从零重新推导同样的解法，"
                    "成本相同，同样的失败概率也相同。做过一次，并不会让第二次更容易。",
                    "这是一个具体且可修复的局限，且与模型能力无关。智能体并不是在这个任务上更差；"
                    "它只是没有地方存放答案。",
                ]),
                ("什么能改变它", [
                    "一个存放经验证行为的地方，并且结构足够清晰，使它能够被检索和检查，而不只是被重放；"
                    "以及一个记录一次尝试为何如此的地方。两者都需要可检查，"
                    "因为长期运行的通用智能体会积累没有任何单次演示覆盖过的条件。",
                ]),
                ("TGL 的关系", [
                    "TGL 提供的正是这两个地方。经验证的行为带着明确适用范围与结果检验进入 Skill Library；"
                    "条件、结果、诊断与修复进入 Experience Memory。智能体保持其通用性，"
                    "而第二次尝试从第一次已经确立的东西开始。",
                ]),
            ],
            "keywords": ("通用智能体机器人, 通用机器人智能体, AI 智能体机器人, 通用机器人任务, "
                         "具身通用智能体, TGL, Teach-and-Grow Learning, general-purpose agent robot"),
        },
    },
    {
        "slug": "no-retraining-robot-learning",
        "parent": "concepts",
        "related": ["training-free-robot-learning", "retraining-tax", "physical-in-context-learning", "agentic-robotics-2026"],
        "en": {
            "title": "Robot Learning Without Retraining: Acquiring Tasks with Frozen Weights",
            "desc": ("Robot learning without retraining means acquiring a new task without a policy update: no "
                     "gradient step, no task-specific fine-tuning, no reinforcement-learning stage. New capability "
                     "is stored explicitly instead of written into weights."),
            "h1": "Robot Learning Without Retraining",
            "lede": ("Robot learning without retraining means acquiring a new task without updating the policy: no "
                     "gradient step, no task-specific fine-tuning, and no reinforcement-learning stage. What the "
                     "robot learns is stored explicitly rather than written into the weights, so acquiring one "
                     "task does not disturb the others."),
            "sections": [
                ("What is being avoided, and why it matters", [
                    "The avoided step is the policy update. It is expensive in data because robot interaction data "
                    "has to be created by operating a machine. It is expensive in risk because a parameter update "
                    "touches weights that also support previously learned behaviour, so a local failure can demand "
                    "a broadly coupled repair and regression checking across everything else.",
                    "The report names that recurring cost the retraining tax. Avoiding it is not about saving "
                    "compute; it is about keeping a repair local.",
                ]),
                ("Where the capability goes instead", [
                    "Two explicit stores. A Skill Library of validated behaviours, each carrying a goal, a reusable "
                    "strategy, supported conditions, compatible executors and an outcome test. And an Experience "
                    "Memory of the task, the selected blocks, observations, outcome, diagnosis and repair.",
                ]),
                ("What this is not", [
                    "It is not “no learning” — behaviour is acquired and both stores grow. It is not “no "
                    "pretraining” — a strong pretrained stack is exactly what makes the route viable. And it does "
                    "not mean weights may never change: under the report's slow-teacher/fast-student path the "
                    "verified trajectories the system produces are the supervision a policy is trained from, which "
                    "is a separate step from the acquisition of the incoming task.",
                ]),
                ("How it relates to in-context adaptation", [
                    "Both avoid the parameter update. In-context adaptation scopes the change to a session; TGL "
                    "writes it into stores that survive the session. The two are complementary — context is a good "
                    "way to convey a task, and an explicit store is a good place to keep what came of it.",
                ]),
            ],
            "faq": [
                ("Is “without retraining” the same as zero-shot?",
                 "No. Zero-shot usually means no task-specific example at all. Learning without retraining still "
                 "uses a few demonstrations; what it avoids is the policy update, not the teaching."),
                ("What replaces the policy update?",
                 "An edit to explicit state: a new or narrowed Skill Block, a changed recovery rule, or a record "
                 "in Experience Memory that changes which block is retrieved next time."),
            ],
            "keywords": ("robot learning without retraining, no-retraining robot adaptation, frozen policy robot "
                         "learning, no fine-tuning robot manipulation, policy-free task acquisition, retraining "
                         "tax, TGL, Teach-and-Grow Learning, 免重训机器人学习"),
        },
        "zh": {
            "title": "免重训机器人学习：在权重冻结的前提下获得新任务",
            "desc": ("免重训机器人学习指在不更新策略的前提下获得新任务：没有梯度步、没有任务特定微调、没有强化学习阶段。"
                     "新能力被显式存放，而不是写进权重。"),
            "h1": "免重训机器人学习",
            "lede": ("免重训机器人学习指在不更新策略的前提下获得新任务：没有梯度步、没有任务特定微调、也没有强化学习阶段。"
                     "机器人学到的东西被显式存放，而不是写进权重，因此获取一个任务不会扰动其它任务。"),
            "sections": [
                ("被避免的是什么，为什么重要", [
                    "被避免的是策略更新。它在数据上昂贵，因为机器人交互数据必须通过操作机器来产生。"
                    "它在风险上也昂贵，因为参数更新会触及同时也支撑着此前所学行为的权重，"
                    "因此一次局部失败可能要求一次耦合面很广的修复，以及对其它一切的回归检查。",
                    "报告把这种反复出现的成本命名为再训练成本。避免它并不是为了省算力，而是为了让修复保持本地。",
                ]),
                ("能力去了哪里", [
                    "两份显式存储。一份是 Skill Library，保存经验证的行为，每条带有目标、可复用策略、"
                    "支持条件、兼容执行器与结果检验。另一份是 Experience Memory，"
                    "记录任务、所选技能块、观测、结果、诊断与修复。",
                ]),
                ("这不是什么", [
                    "它不是「不学习」——行为确实被获得，两份存储都在增长。它不是「不预训练」——"
                    "强大的预训练栈正是这条路线可行的原因。它也不意味着权重永不可变："
                    "报告提出的「慢教师–快学生」路线会随后用经验证的轨迹训练策略，"
                    "那是有意的扩展，不属于获取这一步。",
                ]),
                ("与上下文适配的关系", [
                    "两者都避免参数更新。上下文适配把改变限定在一次会话内；TGL 把它写进能活过会话的存储。"
                    "两者互补——上下文是传达任务的好方式，显式存储是保存其结果的好地方。",
                ]),
            ],
            "faq": [
                ("「免重训」等于零样本吗？",
                 "不等。零样本通常指完全没有任务特定示例。免重训学习仍然使用少量演示；"
                 "它避免的是策略更新，而不是示教。"),
                ("什么替代了策略更新？",
                 "对显式状态的编辑：新增或收窄一个 Skill Block、修改一条恢复规则，"
                 "或者在 Experience Memory 中留下一条记录，改变下次检索到哪个块。"),
            ],
            "keywords": ("免重训机器人学习, 无重训机器人适配, 冻结策略机器人学习, 无需微调的机器人操作, "
                         "无策略更新任务获取, 再训练成本, TGL, Teach-and-Grow Learning, no-retraining robot learning"),
        },
    },
    {
        "slug": "robot-agent-memory",
        "parent": "concepts",
        "related": ["experience-memory", "skill-library", "general-purpose-agent-robot", "agentic-robotics-2026"],
        "en": {
            "title": "Robot Agent Memory: What a Robot Should Keep from an Interaction",
            "desc": ("Robot-agent memory preserves information from earlier physical interaction for future "
                     "decisions. In TGL, a Skill Library stores reusable executable behaviour while Experience "
                     "Memory carries forward success, failure, diagnosis and repair."),
            "h1": "Robot Agent Memory",
            "lede": ("Robot-agent memory is the part of a robot system that preserves information from earlier "
                     "physical interaction so later decisions can use it. It is a different problem from language "
                     "memory: what has to be retained is not what was said but what physically happened, and why."),
            "sections": [
                ("Short answer", [
                    "Robot-agent memory preserves information from earlier physical interaction for future "
                    "decisions. In TGL, a Skill Library stores reusable executable behavior, while Experience "
                    "Memory carries forward success, failure, and repair.",
                ]),
                ("Two kinds of thing to remember", [
                    "A robot has two distinct memory needs and conflating them causes trouble. The first is "
                    "<b>what it can do</b>: behaviours that can be selected and executed, each with the conditions "
                    "under which it applies and a test of its effect. The second is <b>what happened when it "
                    "tried</b>: the task, the blocks chosen, the observations, the outcome, the diagnosis, and any "
                    "repair.",
                    "Keeping them apart matters because they grow differently. A behaviour is admitted once it "
                    "validates; an experience is recorded every time, whether or not anything new was learned.",
                ]),
                ("Why the diagnosis is the valuable part", [
                    "An outcome alone — success or failure — is weak evidence for the next decision. The useful "
                    "content is the explanation: an unsuitable grasp family, an ambiguous observation, a "
                    "calibration issue. That is what lets a later retrieval choose differently rather than simply "
                    "retrying.",
                ]),
                ("Where this connects to the wider field", [
                    "Memory has become an explicit concern in robot learning because policies that condition only "
                    "on the current frame fail on tasks that are not Markovian — where the same observation "
                    "implies different correct actions depending on history. TGL's split between executable "
                    "behaviour and contextual experience is one way to structure that history so that it stays "
                    "inspectable and editable.",
                ]),
            ],
            "faq": [
                ("How does robot memory help an AI agent?",
                 "It changes what the agent can do on the second attempt. A diagnosis recorded after one failure "
                 "lets a later retrieval choose a different grasp family or observation rather than re-running the "
                 "same plan. Outcome alone — success or failure — is weak evidence; the explanation is the useful part."),
                ("What is an experience store for a robot agent?",
                 "A record of what was tried and what came of it: the task, the blocks selected, the observations, "
                 "the outcome, the diagnosis and any repair. In TGL it is Experience Memory, kept separate from the "
                 "Skill Library so that validated behaviour and contextual history grow independently."),
            ],
            "keywords": ("robot agent memory, robot memory, robot experience memory, robot long-term memory, "
                         "memory for robot manipulation, non-Markovian robot policy, robot skill library, TGL, "
                         "Teach-and-Grow Learning, 机器人智能体记忆"),
        },
        "zh": {
            "title": "机器人智能体记忆：一次交互之后应当留下什么",
            "desc": ("机器人智能体记忆保存早先物理交互中的信息，以供后续决策使用。在 TGL 中，"
                     "Skill Library 保存可复用的可执行行为，而 Experience Memory 延续成功、失败、诊断与修复。"),
            "h1": "机器人智能体记忆（Robot Agent Memory）",
            "lede": ("机器人智能体记忆是机器人系统中保存早先物理交互信息、供后续决策使用的部分。"
                     "它与语言记忆是不同的问题：需要保留的不是说了什么，而是物理上发生了什么，以及为什么。"),
            "sections": [
                ("简述", [
                    "机器人智能体记忆保存早先物理交互中的信息，以供后续决策使用。在 TGL 中，"
                    "Skill Library 保存可复用的可执行行为，而 Experience Memory 延续成功、失败与修复。",
                ]),
                ("两类需要记住的东西", [
                    "机器人有两类不同的记忆需求，把它们混在一起会出问题。第一类是<b>它能做什么</b>："
                    "可被选择与执行的行为，每条带有适用条件与对效果的检验。第二类是<b>它尝试时发生了什么</b>："
                    "任务、所选的技能块、观测、结果、诊断以及任何修复。",
                    "把它们分开很重要，因为它们的增长方式不同。行为在通过验证时被收录一次；"
                    "经验则每次都被记录，无论是否学到了新东西。",
                ]),
                ("为什么诊断才是最有价值的部分", [
                    "仅有结果——成功或失败——对下一次决策来说是弱证据。有用的内容是解释："
                    "不合适的抓取方式、含糊的观测、标定问题。"
                    "正是它让后续检索能够做出不同的选择，而不只是简单地重试。",
                ]),
                ("与更广领域的连接", [
                    "记忆之所以成为机器人学习中的显式议题，是因为只以当前帧为条件的策略，"
                    "在非马尔可夫任务上会失败——同一观测依据历史不同而对应不同的正确动作。"
                    "TGL 把「可执行行为」与「上下文经验」分开，是组织这段历史的一种方式，"
                    "好处是它保持可检查、可编辑。",
                ]),
            ],
            "faq": [
                ("机器人记忆对 AI 智能体有什么用？",
                 "它改变了智能体在第二次尝试时能做什么。一次失败之后记录下来的诊断，"
                 "能让后续检索换用不同的抓取方式或观测，而不是把同一个计划再跑一遍。"
                 "仅有结果——成功或失败——是弱证据；解释才是有用的部分。"),
                ("什么是机器人智能体的经验库？",
                 "尝试过什么、结果如何的记录：任务、所选技能块、观测、结果、诊断与任何修复。"
                 "在 TGL 中它就是 Experience Memory，与 Skill Library 分开保存，"
                 "使「经验证的行为」与「上下文历史」各自独立增长。"),
            ],
            "keywords": ("机器人智能体记忆, 机器人记忆, 机器人经验记忆, 机器人长期记忆, 机器人操作记忆, "
                         "非马尔可夫机器人策略, 机器人技能库, TGL, Teach-and-Grow Learning"),
        },
    },
    {
        "slug": "runtime-reasoning-robotics",
        "parent": "concepts",
        "related": ["agent-as-policy", "tool-use-robotics", "robot-agent-memory", "agentic-robotics-2026"],
        "en": {
            "title": "Runtime Reasoning for Robots: Deciding While the Task Is Running",
            "desc": ("Runtime reasoning means the model that decides what to do next is still running while the "
                     "task executes, so it can act on what the robot observes. It is the opposite of committing "
                     "to an offline plan."),
            "h1": "Runtime Reasoning for Robots",
            "lede": ("Runtime reasoning means the component that decides what to do next is still running while "
                     "the task executes. It is the difference between a plan committed before execution and a "
                     "decision that can respond to what the robot actually observes mid-task."),
            "sections": [
                ("Why it is worth the cost", [
                    "Reasoning at runtime is far more expensive per step than feed-forward inference. What it buys "
                    "is the ability to act on evidence that only exists during execution: a grasp that did not "
                    "hold, a drawer that did not open, an object that moved. An offline planner cannot see any of "
                    "these, because it finished before they occurred.",
                ]),
                ("The usual compromise", [
                    "In practice the two are combined rather than chosen between. Deliberation is reserved for "
                    "novelty, diagnosis and recovery, while mature behaviour runs on a cheap learned policy. TGL's "
                    "report builds on exactly that split — a slow teacher for the frontier of knowledge, a fast "
                    "student for what is already established — and the verified trajectories the system produces "
                    "are what the fast student is trained from.",
                ]),
                ("What has to be true for it to help", [
                    "The reasoning component has to receive enough evidence to reason with. If the robot's "
                    "interface reports only that a command was issued, runtime reasoning has nothing to work on; "
                    "it will re-derive the same plan. This is why the interface — what a subgoal reports about "
                    "its own effect — matters as much as the reasoning.",
                ]),
                ("How TGL relates", [
                    "TGL keeps the agent running through the task and gives it something to reason over: each "
                    "Skill Block has an outcome test, and its result is what the agent reads. A passed effect "
                    "advances the plan; a failed or inconclusive one prompts another observation, a different "
                    "executor, or a revised route.",
                ]),
            ],
            "keywords": ("runtime reasoning robot, online reasoning robotics, test-time reasoning robot, "
                         "deliberation robot control, agent runtime decision, slow fast robot policy, TGL, "
                         "Teach-and-Grow Learning"),
        },
        "zh": {
            "title": "机器人运行时推理：在任务进行中做决定",
            "desc": ("运行时推理指决定下一步做什么的模型在任务执行期间仍在运行，因此能对机器人观察到的内容作出反应。"
                     "它与「在执行前就承诺一份计划」相反。"),
            "h1": "机器人运行时推理",
            "lede": ("运行时推理指决定下一步做什么的组件在任务执行期间仍在运行。"
                     "这正是「在执行前承诺的计划」与「能对机器人在任务中途实际观察到的内容作出反应的决策」之间的差别。"),
            "sections": [
                ("为什么值得这个代价", [
                    "运行时推理每步的成本远高于前馈推理。它换来的是对「只在执行期间才存在的证据」作出反应的能力："
                    "没有夹稳的抓取、没有打开的抽屉、被移动的物体。离线规划器看不到这些，"
                    "因为它在这些事情发生之前就已经结束了。",
                ]),
                ("通常的折中", [
                    "实践中两者是被组合使用的，而不是二选一。深思被留给陌生情形、诊断与恢复，"
                    "成熟行为则跑在廉价的学习策略上。TGL 的报告提出的正是这一拆分——"
                    "把慢教师留给知识的前沿，把快学生留给已经确立的部分——"
                    "并把从经验证轨迹蒸馏视为未来扩展，而不是当前系统的一部分。",
                ]),
                ("它要真正起作用需要什么", [
                    "推理组件必须收到足够推理用的证据。如果机器人接口只报告「指令已发出」，运行时推理就无从下手，"
                    "它会重新推导出同样的计划。这就是为什么接口——一个子目标对自身效果的汇报——"
                    "和推理本身同样重要。",
                ]),
                ("TGL 的关系", [
                    "TGL 让智能体在整个任务期间保持运行，并给它可推理的东西：每个 Skill Block 都带结果检验，"
                    "而它的结果正是智能体所读取的。效果通过就推进计划；"
                    "失败或不确定则触发再一次观察、更换执行器，或修改后续路线。",
                ]),
            ],
            "keywords": ("机器人运行时推理, 在线推理机器人, 测试时推理机器人, 机器人控制深思, "
                         "智能体运行时决策, 慢快机器人策略, TGL, Teach-and-Grow Learning"),
        },
    },
    {
        "slug": "tool-use-robotics",
        "parent": "concepts",
        "related": ["agent-as-policy", "coding-agent-robotics", "runtime-reasoning-robotics", "agentic-robotics-2026"],
        "en": {
            "title": "Tool Use in Robotics: Giving an Agent Capabilities It Can Call",
            "desc": ("Tool use in robotics means exposing perception, grasping and motion as callable capabilities "
                     "an agent selects and invokes. It is what lets a reasoning model act without emitting control "
                     "signals itself."),
            "h1": "Tool Use in Robotics",
            "lede": ("Tool use in robotics means exposing perception, grasping, motion and control as callable "
                     "capabilities that a reasoning agent selects and invokes. It is the mechanism that lets a "
                     "model act on the physical world without emitting control signals itself."),
            "sections": [
                ("Why tools rather than one model", [
                    "A robot needs capabilities that a language model does not have: metric depth, collision-free "
                    "motion, contact, and control at tens of hertz. Wrapping each as a tool keeps the agent's job "
                    "at the level it is good at — deciding what should happen — and keeps the geometry where it "
                    "belongs.",
                    "It also makes the system inspectable. A tool has a documented effect and a version; when a "
                    "behaviour stops working, the question of which component changed has an answer.",
                ]),
                ("What a good tool reports", [
                    "The return value matters more than the call. A tool that reports “command sent” gives the "
                    "agent nothing to reason with. A tool that reports the intended physical effect and whether it "
                    "was observed gives the agent something it can act on — and gives the whole system a place to "
                    "check causality rather than assume it.",
                    "This is the same argument as the outcome test on a Skill Block, seen from the tool side.",
                ]),
                ("Where tools and skills meet", [
                    "A skill is what the robot can do; a tool is how it does it. TGL's Skill Block is explicit "
                    "about the relationship: a block declares which executors can realize it and what evidence "
                    "counts as success. That declaration is what makes a block portable across tool versions "
                    "rather than bound to one implementation.",
                ]),
                ("How TGL relates", [
                    "The agent selects subgoals and invokes tools; detection, segmentation, RGB-depth geometry, "
                    "Contact-GraspNet, MPLib and controllers supply the physical operations, with Codex connecting "
                    "the agent to them. What TGL adds is the contract around each call — a stated effect and a "
                    "test — so that invoking a tool is not the same as assuming it worked.",
                ]),
            ],
            "keywords": ("tool use robotics, robot skills as tools, robot tool calling, agent tool interface "
                         "robot, MCP robotics, callable robot capabilities, TGL, Teach-and-Grow Learning, "
                         "机器人工具调用"),
        },
        "zh": {
            "title": "机器人中的工具调用：给智能体可以调用的能力",
            "desc": ("机器人中的工具调用指把感知、抓取与运动暴露为智能体可选择与调用的能力。"
                     "正是它让推理模型无需自己输出控制信号就能对物理世界采取行动。"),
            "h1": "机器人中的工具调用（Tool Use in Robotics）",
            "lede": ("机器人中的工具调用指把感知、抓取、运动与控制暴露为推理智能体可选择并调用的能力。"
                     "它是让模型无需自己输出控制信号就能对物理世界采取行动的机制。"),
            "sections": [
                ("为什么要工具而不是单一模型", [
                    "机器人需要一些语言模型并不具备的能力：度量深度、无碰撞运动、接触，以及数十赫兹的控制。"
                    "把每一项包装成工具，能让智能体的工作停留在它擅长的层面——决定应当发生什么——"
                    "并把几何留在它该在的地方。",
                    "它也让系统可检查。工具有文档化的效果与版本；当一个行为停止工作时，"
                    "「是哪个组件变了」这个问题有答案。",
                ]),
                ("一个好的工具应当汇报什么", [
                    "返回值比调用本身更重要。只报告「指令已发出」的工具，没给智能体任何可推理的东西。"
                    "报告意图物理效果、以及该效果是否被观察到的工具，才给了智能体可以据以行动的内容——"
                    "也给了整个系统一个检查因果关系、而不是假定它的地方。",
                    "这与 Skill Block 上的结果检验是同一个论证，只是从工具这一侧看。",
                ]),
                ("工具与技能在哪里相遇", [
                    "技能是机器人能做什么，工具是它怎么做。TGL 的 Skill Block 对二者关系有明确表述："
                    "一个块声明哪些执行器能实现它，以及什么证据算作成功。"
                    "正是这一声明，让块可以在不同工具版本间移植，而不是绑定在某一种实现上。",
                ]),
                ("TGL 的关系", [
                    "智能体选择子目标并调用工具；检测、分割、RGB-D 几何、Contact-GraspNet、MPLib 与控制器"
                    "提供物理操作，Codex 负责把智能体与它们连接起来。"
                    "TGL 增加的是每次调用周围的契约——声明的效果与检验——"
                    "使「调用了工具」与「假定它成功了」不再是同一件事。",
                ]),
            ],
            "keywords": ("机器人工具调用, 机器人技能即工具, 机器人 tool calling, 智能体工具接口, "
                         "MCP 机器人, 可调用机器人能力, TGL, Teach-and-Grow Learning, tool use robotics"),
        },
    },
]
