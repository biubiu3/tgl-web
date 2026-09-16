"""Additional concept pages, covering the broader query space around TGL.

Same shape as pages.py: `en` and `zh` bodies side by side, prose only, facts from
site.json. These pages exist so that queries phrased in the vocabulary of the
wider field ("agentic robotics", "continual learning", "GPT robotic arm") reach a
page that answers them and routes the reader to TGL, rather than reaching nothing.
"""

CONCEPTS = [
    {
        "slug": "agentic-robotics",
        "parent": "concepts",
        "related": ["llm-robotics", "general-robot-learning", "teach-and-grow-learning"],
        "en": {
            "title": "Agentic Robotics: What It Means for a Robot to Be Agent-Centered",
            "desc": ("Agentic robotics puts a reasoning agent in charge of selecting subgoals and tools while "
                     "specialised components handle geometry and control. Teach and Grow is an agent-centered "
                     "architecture for general robot learning."),
            "h1": "Agentic Robotics",
            "lede": ("Agentic robotics means putting a reasoning agent — typically a large multimodal model — in "
                     "charge of what a robot should do next, while specialised components handle geometry and "
                     "continuous control. The agent reads the scene, chooses a subgoal and a tool, observes the "
                     "result, and revises the plan. Teach-and-Grow Learning (TGL) is an agent-centered "
                     "architecture built on exactly that loop."),
            "sections": [
                ("The loop", [
                    "An agentic system is defined less by its model than by its cycle: observe, decide, act, read "
                    "the outcome, revise. In a workspace that means camera observations standing in for state, "
                    "perception and motion tools performing physical operations, and executor reports describing "
                    "what happened. The agent's next choice depends on those reports rather than on a fixed script.",
                    "This is what made tool-using language agents useful in software, applied somewhere less "
                    "forgiving: a mistaken action changes the physical world, and the correction has to come from "
                    "what the robot actually observed.",
                ]),
                ("Why the division of labour matters", [
                    "A language model cannot emit joint torques, and a manipulation policy cannot reason about a "
                    "multi-minute task. The two have incompatible requirements — long context and slow deliberation "
                    "on one side, tens of hertz on the other. Agentic robotics splits them rather than trying to "
                    "make one model do both, which produces something either too slow to control or too shallow "
                    "to plan.",
                ]),
                ("Where the agent stops being able to help", [
                    "An agent reasons over the world it can see, and it sees only what its tools report. If the "
                    "low-level interface silently discards something — a brief event that fell between two "
                    "decisions, say — then that information is missing from the agent's model of the world too, "
                    "and its plan is built on an incomplete picture. This is why the low-level interface is an "
                    "agent-level concern rather than only a control detail.",
                ]),
                ("Where TGL fits", [
                    "TGL is agent-centered by design. The agent identifies subgoals shared across demonstrations, "
                    "expresses them as closed-loop Skill Blocks, grounds each block in the current scene, and "
                    "decides what to keep. The robot-side executors supply the geometry and control. In the "
                    "paper's implementation the reasoning comes from OpenAI GPT-6 Astra, with Codex connecting "
                    "the agent to the robot tools.",
                ]),
            ],
            "keywords": ("agentic robotics, agent-centered architecture, AI agent robot, robot agent, embodied "
                         "agent, LLM robot control, tool-using agent, physical agent, TGL, Teach-and-Grow "
                         "Learning"),
        },
        "zh": {
            "title": "智能体机器人学：以智能体为中心对机器人意味着什么",
            "desc": ("智能体机器人学让推理智能体负责选择子目标与工具，由专用组件处理几何与连续控制。"
                     "Teach and Grow 就是一套以智能体为中心的通用机器人学习架构。"),
            "h1": "智能体机器人学（Agentic Robotics）",
            "lede": ("智能体机器人学指让推理智能体——通常是一个大型多模态模型——决定机器人下一步该做什么，"
                     "而由专用组件负责几何与连续控制。智能体读取场景、选择子目标与工具、观察结果、修正计划。"
                     "Teach-and-Grow Learning（TGL）正是建立在这一循环之上的以智能体为中心的架构。"),
            "sections": [
                ("循环", [
                    "一个系统是否“智能体化”，与其说取决于模型，不如说取决于它的循环：观察、决策、行动、读取结果、修正。"
                    "在工作空间中，这意味着相机观测充当状态、感知与运动工具执行物理操作、执行器回执描述实际发生了什么。"
                    "智能体的下一次选择取决于这些回执，而不是一段固定脚本。",
                    "这正是让工具型语言智能体在软件中变得有用的模式，只是被放到了更不宽容的场合：一次错误动作会改变物理世界，"
                    "而纠正必须来自机器人实际观察到的东西。",
                ]),
                ("为什么分工重要", [
                    "语言模型无法输出关节力矩，操作策略也无法规划数分钟长的任务。两者的需求互不相容——"
                    "一边需要长上下文与缓慢深思，另一边需要数十赫兹。智能体机器人学选择把它们拆开，"
                    "而不是试图让一个模型同时胜任；后者得到的要么太慢无法控制，要么太浅无法规划。",
                ]),
                ("智能体帮不上忙的地方", [
                    "智能体对它能看到的世界进行推理，而它只能看到工具报告的内容。如果低层接口悄悄丢弃了什么——"
                    "比如掉在两次决策之间的一段短暂事件——那么这个信息在智能体的世界模型里同样缺失，"
                    "它的规划就建立在并不完整的图景上。这就是为什么低层接口属于智能体层面的问题，而不只是控制细节。",
                ]),
                ("TGL 的位置", [
                    "TGL 在设计上以智能体为中心。智能体识别演示之间共享的子目标，把它们表达为闭环的 Skill Block，"
                    "将每个块落实到当前场景，并决定保留什么。机器人侧执行器提供几何与控制。"
                    "在论文的实现中，推理由 OpenAI GPT-6 Astra 完成，Codex 负责把智能体与机器人工具连接起来。",
                ]),
            ],
            "keywords": ("智能体机器人学, 以智能体为中心的架构, AI 智能体机器人, 机器人智能体, 具身智能体, "
                         "大模型机器人控制, 工具型智能体, 物理智能体, TGL, Teach-and-Grow Learning"),
        },
    },
    {
        "slug": "general-robot-learning",
        "parent": "concepts",
        "related": ["teach-and-grow-learning", "agentic-robotics", "retraining-tax"],
        "en": {
            "title": "General Robot Learning: Two Routes to Generality, and What Each Costs",
            "desc": ("General robot learning aims for one system that handles many tasks and scenes. The dominant "
                     "route scales data and parameters; Teach-and-Grow Learning takes a complementary route "
                     "through explicit, reusable skills with fixed weights."),
            "h1": "General Robot Learning",
            "lede": ("General robot learning is the goal of one system that handles many tasks, objects and scenes "
                     "without being rebuilt for each. The dominant route pursues it by scaling data and "
                     "parameters. Teach-and-Grow Learning takes a complementary route: hold the pretrained stack "
                     "fixed and let explicit, reusable skills accumulate instead."),
            "sections": [
                ("Why generality is the hard part", [
                    "A robot that has learned one pick-and-place task has learned very little about the next "
                    "object. Physical interaction data is expensive in a way text and code are not: it has to be "
                    "created by operating a machine. Object pose, camera geometry, clutter, material and "
                    "embodiment all interact, and covering one factor does not cover their combinations. A "
                    "general system has to generalise over that product, not over a single axis.",
                ]),
                ("Route one: scale", [
                    "Train a large policy on a broad cross-embodiment corpus so that its representations transfer, "
                    "then fine-tune per task. This is the route behind modern vision-language-action models, and it "
                    "works. Its cost is structural: a new capability is absorbed into shared parameters, so "
                    "repairing one behaviour means re-checking the others, and the expense recurs with every "
                    "change of object, sensor or gripper.",
                ]),
                ("Route two: explicit capability", [
                    "The complementary route does not try to make one set of weights cover everything. It keeps "
                    "the pretrained prior and grows an explicit store of validated behaviours, each with a stated "
                    "scope and an outcome test, plus a memory of the conditions under which each was used. "
                    "Generality then comes from retrieval and composition rather than from parameter coverage.",
                    "The two routes are not exclusive. A learned policy can implement one of the explicit skills; "
                    "a geometric planner can bridge two of them. What changes is where new task knowledge is "
                    "written.",
                ]),
                ("What route two costs", [
                    "It moves the difficulty rather than removing it. Grounding, validation, compatibility "
                    "checking and retrieval all have to stay manageable, or the explicit store becomes as "
                    "expensive to grow as the parameters were to retrain. TGL analyses those cost regimes rather "
                    "than treating cheap growth as automatic.",
                ]),
            ],
            "keywords": ("general robot learning, general-purpose robot policy, generalist robot manipulation, "
                         "robot generalisation, cross-task robot learning, TGL, Teach-and-Grow Learning, "
                         "retraining tax"),
        },
        "zh": {
            "title": "通用机器人学习：通往通用性的两条路线与各自代价",
            "desc": ("通用机器人学习追求用一套系统处理多种任务与场景。主流路线靠扩大数据与参数；"
                     "Teach-and-Grow Learning 走互补路线：固定权重，让显式可复用技能持续积累。"),
            "h1": "通用机器人学习",
            "lede": ("通用机器人学习的目标是：用一套系统处理多种任务、物体与场景，而不必为每一个都重建。"
                     "主流路线通过扩大数据与参数来追求这一点。Teach-and-Grow Learning 走的是一条互补路线："
                     "保持预训练栈不变，让显式的可复用技能持续积累。"),
            "sections": [
                ("为什么通用性最难", [
                    "学会了把一个物体拿起来的机器人，对下一个物体几乎一无所知。物理交互数据的昂贵程度不同于文本和代码："
                    "它必须通过操作机器来产生。物体位姿、相机几何、杂乱程度、材质与本体形态彼此耦合，"
                    "覆盖一个因素并不等于覆盖它们的组合。通用系统必须在这个乘积上泛化，而不是在单个轴上。",
                ]),
                ("路线一：规模化", [
                    "在广泛的跨本体语料上训练大型策略，使其表示可迁移，再按任务微调。"
                    "这是现代视觉-语言-动作模型背后的路线，而且它有效。它的代价是结构性的："
                    "新能力被吸收进共享参数，因此修复一个行为意味着重新检查其它行为，"
                    "而这种开销会在每次更换物体、传感器或夹爪时反复出现。",
                ]),
                ("路线二：显式能力", [
                    "互补路线不去试图让一套权重覆盖一切。它保留预训练先验，转而增长一份显式的经验证行为存储——"
                    "每个行为都带有明确适用范围与结果检验——外加一份记录其使用条件的记忆。"
                    "通用性因此来自检索与组合，而不是来自参数的覆盖范围。",
                    "两条路线并不互斥。学习策略可以实现其中某个显式技能；几何规划器可以连接其中两个。"
                    "改变的是新任务知识被写在哪里。",
                ]),
                ("路线二的代价", [
                    "它转移了困难，而不是消除困难。场景落地、验证、兼容性检查与检索都必须保持可控，"
                    "否则显式存储的增长成本会和重训参数一样高。TGL 分析的是这些成本情形，"
                    "而不是把低成本增长视为自动成立。",
                ]),
            ],
            "keywords": ("通用机器人学习, 通用机器人策略, 通用操作, 机器人泛化能力, 跨任务机器人学习, "
                         "TGL, Teach-and-Grow Learning, 再训练成本"),
        },
    },
    {
        "slug": "lifelong-robot-learning",
        "parent": "concepts",
        "related": ["retraining-tax", "teach-and-grow-learning"],
        "en": {
            "title": "Lifelong Robot Learning Without Catastrophic Forgetting",
            "desc": ("Lifelong robot learning means a robot keeps acquiring tasks across its working life. "
                     "Parameter updates risk overwriting earlier competence; Teach-and-Grow Learning keeps new "
                     "capability in explicit stores that do not overwrite anything."),
            "h1": "Lifelong Robot Learning",
            "lede": ("Lifelong robot learning is the goal of a robot that keeps acquiring new tasks throughout its "
                     "working life rather than being trained once and frozen. The central difficulty is that "
                     "learning a new task must not erase an old one. Teach-and-Grow Learning addresses that by "
                     "keeping new capability in explicit stores instead of shared parameters."),
            "sections": [
                ("The forgetting problem", [
                    "When a policy absorbs a new behaviour by updating its parameters, the update touches weights "
                    "that also support everything learned before. The result can be degraded performance on "
                    "earlier tasks — the classic stability-plasticity trade-off — and the usual mitigation is "
                    "rehearsal or regularisation, both of which cost something.",
                    "In robotics the practical symptom is worse than a metric drop: a robot that was reliable on "
                    "one task becomes unreliable on it after being taught another, and the failure may only "
                    "surface in the field.",
                ]),
                ("An alternative mechanism", [
                    "If new knowledge is stored as an explicit object rather than written into weights, then "
                    "adding it does not overwrite anything. TGL's Skill Library holds validated behaviours with "
                    "their scopes, and Experience Memory holds the conditions and repairs. Acquiring a new task "
                    "adds to those stores.",
                    "This does not make forgetting impossible. Retrieval can still pick the wrong block, and "
                    "grounding can fail in a new scene. What it removes is the mechanism by which learning one "
                    "thing directly damages another.",
                ]),
                ("What has to be true for this to work", [
                    "Two conditions matter. Entries need stated scopes, so that an overgeneralised skill can be "
                    "narrowed rather than silently misapplied. And compatibility has to stay checkable: if every "
                    "new skill must be validated against every existing one, growth becomes quadratic and the "
                    "advantage disappears. The paper analyses these regimes explicitly.",
                ]),
                ("The scaling hypothesis", [
                    "The report proposes a hypothesis relating effective reusable experience to future-task error "
                    "and teaching demand, both falling toward irreducible floors. It is presented as a hypothesis "
                    "to be tested over sequential acquisition experiments, not as a fitted law.",
                ]),
            ],
            "keywords": ("lifelong robot learning, continual robot learning, catastrophic forgetting robot, "
                         "stability plasticity robot, robot skill accumulation, TGL, Teach-and-Grow Learning, "
                         "retraining tax"),
        },
        "zh": {
            "title": "终身机器人学习：如何避免灾难性遗忘",
            "desc": ("终身机器人学习指机器人在整个工作周期中持续获得新任务。参数更新有覆盖既有能力的风险；"
                     "Teach-and-Grow Learning 把新能力放在显式存储中，不覆盖任何东西。"),
            "h1": "终身机器人学习",
            "lede": ("终身机器人学习的目标是：机器人不是训练一次就被冻结，而是在整个工作周期中持续获得新任务。"
                     "核心困难在于学习新任务不能抹掉旧任务。Teach-and-Grow Learning 通过把新能力放进显式存储、"
                     "而不是共享参数，来应对这一点。"),
            "sections": [
                ("遗忘问题", [
                    "当策略通过更新参数来吸收新行为时，这次更新会触及同时也支撑着此前所学内容的权重。"
                    "结果可能是早期任务性能下降——经典稳定性-可塑性权衡——而常见的缓解手段是回放或正则化，两者都有代价。",
                    "在机器人上，实际症状比指标下降更糟：一个原本可靠的机器人，在被教了另一个任务之后，"
                    "在前一个任务上变得不可靠，而这种失效可能只在现场才暴露出来。",
                ]),
                ("一种替代机制", [
                    "如果新知识被存为显式对象而不是写进权重，那么新增它就不会覆盖任何东西。"
                    "TGL 的 Skill Library 保存带适用范围的经验证行为，Experience Memory 保存条件与修复。"
                    "获取一个新任务就是往这些存储里添加内容。",
                    "这并不意味着遗忘不可能发生。检索仍然可能选错技能块，落地也可能在新场景中失败。"
                    "被移除的是「学一件事直接损坏另一件事」这个机制。",
                ]),
                ("要做到这一点需要满足什么", [
                    "两个条件很重要。条目需要有明确的适用范围，这样过度泛化的技能才能被收窄，而不是被悄悄误用。"
                    "兼容性必须保持可检查：如果每个新技能都要与所有既有技能逐一验证，增长会变成平方级，优势就消失了。"
                    "论文对这些情形做了明确分析。",
                ]),
                ("缩放假设", [
                    "报告提出一个假设，把有效的可复用经验与未来任务误差、示教需求的下降联系起来，二者都趋向不可约的下限。"
                    "它是作为需要在顺序获取实验中检验的假设提出的，而不是拟合出的定律。",
                ]),
            ],
            "keywords": ("终身机器人学习, 持续机器人学习, 机器人灾难性遗忘, 稳定性可塑性, 机器人技能积累, "
                         "TGL, Teach-and-Grow Learning, 再训练成本"),
        },
    },
    {
        "slug": "vla-without-retraining",
        "parent": "concepts",
        "related": ["teach-and-grow-learning", "general-robot-learning", "retraining-tax"],
        "en": {
            "title": "Adapting a VLA Model Without Retraining It",
            "desc": ("Vision-language-action models normally absorb a new task by collecting more data and "
                     "updating the policy. Teach-and-Grow Learning asks what can be adapted while the VLA weights "
                     "stay frozen, and stores the answer as explicit Skill Blocks."),
            "h1": "Adapting a VLA Model Without Retraining",
            "lede": ("Vision-language-action (VLA) models normally absorb an unfamiliar task by collecting more "
                     "robot data and updating the policy. Teach-and-Grow Learning asks a narrower question: what "
                     "can still be adapted while the pretrained VLA weights stay frozen? Its answer is to store "
                     "the new capability as an explicit Skill Block and leave the model alone."),
            "sections": [
                ("What the pretrained model is still for", [
                    "Freezing the weights does not make the model passive. The VLA stack still supplies the "
                    "perception, language grounding and control priors that let the robot interpret a scene and "
                    "move through it. What it does not supply is a place to put a new task, because in the "
                    "end-to-end route the only such place is the parameters.",
                    "TGL adds a second place. The agent composes subgoals into Skill Blocks, each grounded in the "
                    "current observation and checked against an outcome test, and stores the ones that pass.",
                ]),
                ("Where the adaptation actually happens", [
                    "Three things change during acquisition, and none of them is a weight: the set of available "
                    "Skill Blocks, the retrieval that selects among them, and the Experience Memory that records "
                    "what happened. Adaptation is therefore a change in the explicit state the agent reasons over, "
                    "not a change in the model.",
                    "In a new scene the same block can produce a different physical realization, because object "
                    "bindings, grasp geometry and collision-free motion are recomputed from what the robot "
                    "currently observes.",
                ]),
                ("What this does and does not buy", [
                    "It buys locality: repairing one behaviour is an edit to one explicit object rather than a "
                    "parameter update with regression risk across everything else. It does not buy unlimited "
                    "capability — the frozen prior still bounds what the robot can perceive and do, and grounding "
                    "can still fail. It also does not remove the need for validated scope: an overgeneralised "
                    "block is a real failure mode, which is why candidates are tested beyond their teaching "
                    "demonstrations before admission.",
                ]),
                ("Relation to other adaptation routes", [
                    "Prompting, in-context adaptation and parameter-efficient fine-tuning also try to avoid full "
                    "retraining. They differ in where the adapted knowledge lives: in a context window, in a small "
                    "set of adapter weights, or — in TGL's case — in an inspectable store of behaviours that a "
                    "person can read, narrow or revert.",
                ]),
            ],
            "keywords": ("VLA without retraining, frozen VLA adaptation, adapting robot policy without "
                         "fine-tuning, vision-language-action adaptation, prompt adaptation robot, TGL, "
                         "Teach-and-Grow Learning, retraining tax"),
        },
        "zh": {
            "title": "在不重训的前提下适配 VLA 模型",
            "desc": ("视觉-语言-动作模型通常通过采集更多数据、更新策略来吸收新任务。"
                     "Teach-and-Grow Learning 提出的问题是：在 VLA 权重冻结时还能适配什么，并把答案存为显式的 Skill Block。"),
            "h1": "在不重训的前提下适配 VLA 模型",
            "lede": ("视觉-语言-动作（VLA）模型通常通过采集更多机器人数据、更新策略来吸收不熟悉的任务。"
                     "Teach-and-Grow Learning 问的是一个更窄的问题：当预训练 VLA 权重保持冻结时，还有什么可以被适配？"
                     "它的回答是把新能力存为显式的 Skill Block，让模型保持不动。"),
            "sections": [
                ("预训练模型仍然负责什么", [
                    "冻结权重并不会让模型变得无所作为。VLA 栈仍然提供感知、语言 grounding 与控制先验，"
                    "使机器人能够理解场景并在其中运动。它不提供的，是存放新任务的地方——"
                    "因为在端到端路线中，唯一这样的地方就是参数。",
                    "TGL 增加了第二个地方。智能体把子目标组合为 Skill Block，每个块都落实到当前观测并接受结果检验，"
                    "通过检验的会被保存下来。",
                ]),
                ("适配实际发生在哪里", [
                    "获取过程中有三样东西改变，而它们都不是权重：可用 Skill Block 的集合、在它们之间做选择的检索、"
                    "以及记录实际发生了什么的 Experience Memory。因此适配是智能体所推理的显式状态发生了变化，"
                    "而不是模型发生了变化。",
                    "在新场景中，同一个技能块可以产生不同的物理实现，因为物体绑定、抓取几何与无碰撞运动"
                    "都会根据机器人当前观测重新计算。",
                ]),
                ("这样做能换来什么，换不来什么", [
                    "它换来了局部性：修复一个行为是对单个显式对象的编辑，而不是一次带有全局回归风险的参数更新。"
                    "它换不来无限的能力——冻结的先验仍然限制着机器人能感知和能做到的范围，落地也仍然可能失败。"
                    "它也没有取消对适用范围的验证需求：过度泛化的技能块是真实的失效模式，"
                    "这正是候选必须在示教演示之外接受检验的原因。",
                ]),
                ("与其他适配路线的关系", [
                    "提示、上下文内适配与参数高效微调也在试图避免完整重训。它们的区别在于适配后的知识存放在哪里："
                    "在上下文窗口里、在一小部分适配器权重里，或者在 TGL 的情况下——"
                    "在一个可被人阅读、收窄或回退的行为存储里。",
                ]),
            ],
            "keywords": ("VLA 免重训适配, 冻结 VLA 适配, 无需微调适配机器人策略, 视觉语言动作模型适配, "
                         "提示适配机器人, TGL, Teach-and-Grow Learning, 再训练成本"),
        },
    },
    {
        "slug": "physical-ai",
        "parent": "concepts",
        "related": ["llm-robotics", "general-robot-learning"],
        "en": {
            "title": "Physical AI and Embodied AI: What the Terms Mean for Robot Manipulation",
            "desc": ("Physical AI and embodied AI describe systems that perceive and act in the physical world "
                     "through sensors and actuators. For manipulation the real questions are sensory interfaces, "
                     "timing under delayed control, and where training data comes from."),
            "h1": "Physical AI and Embodied AI",
            "lede": ("Physical AI and embodied AI are the terms now used for systems that perceive and act in the "
                     "physical world through sensors and actuators, rather than producing text or images. Behind "
                     "the labels is a set of concrete engineering problems: how a policy's sensory interface "
                     "should be shaped, how it behaves when decisions are delayed, and where its training data "
                     "comes from."),
            "sections": [
                ("The label and the substance", [
                    "Physical AI is the industry framing; embodied AI and embodied intelligence are the more "
                    "academic ones. All three point at the same shift. A language model predicts the next token; "
                    "a physical agent has to deal with the consequences of its own actions in a world that pushes "
                    "back. Mass, friction, inertia and contact are not in the training distribution of text, so "
                    "the representation a physical agent needs is not the one a chatbot needs.",
                ]),
                ("What is genuinely hard", [
                    "<b>Data.</b> Internet text and video are abundant and third-person. A robot needs "
                    "first-person evidence of what the world becomes after <i>it</i> acts, and that data is "
                    "expensive to create.",
                    "<b>Sensory interfaces.</b> Most work assumes vision suffices. It does not: contact, force "
                    "and hidden internal state are invisible to cameras, and the modalities that do report them "
                    "each carry their own temporal structure.",
                    "<b>Timing.</b> Physical agents run under latency and their most capable policies run slowly. "
                    "Anything that must be noticed between two decisions falls into the gap.",
                    "<b>Evaluation.</b> Reaching a goal is not the same as behaving correctly. A policy can look "
                    "successful on a geometric metric while being wrong in the way that matters.",
                ]),
                ("Where TGL fits", [
                    "Teach and Grow is a physical-AI system. Its subject is the agent's interface to the physical "
                    "world: a robot acquiring a new manipulation capability by acting, observing the outcome, and "
                    "keeping what validated. Its claim is that for agents under delayed control, preserving what "
                    "happened is a requirement rather than a refinement.",
                ]),
            ],
            "keywords": ("physical AI, embodied AI, embodied intelligence, embodied agent, physical agent, "
                         "robot manipulation, first-person robot data, robot learning, TGL, 物理AI, 具身智能"),
        },
        "zh": {
            "title": "物理AI 与具身智能：这些词对机器人操作意味着什么",
            "desc": ("物理AI 与具身智能指通过传感器与执行器在物理世界中感知和行动的系统。"
                     "对操作而言真正的问题是感官接口、延迟控制下的时序，以及训练数据从哪里来。"),
            "h1": "物理AI 与具身智能",
            "lede": ("物理AI 与具身智能是当下用来指代“通过传感器与执行器在物理世界中感知和行动、而非生成文本或图像的"
                     "系统“的术语。标签背后是一组具体的工程问题：策略的感官接口应当如何设计、"
                     "当决策被延迟时它会如何表现，以及训练数据从哪里来。"),
            "sections": [
                ("标签与实质", [
                    "物理AI 是产业界的说法，具身智能（embodied AI / embodied intelligence）更偏学术。三者指向同一个转变："
                    "语言模型预测下一个词元，而物理智能体必须应对自己行动在一个会「顶回来」的世界中造成的后果。"
                    "质量、摩擦、惯性与接触都不在文本的训练分布里，因此物理智能体需要的表示并不是聊天机器人需要的表示。",
                ]),
                ("真正困难的地方", [
                    "<b>数据。</b>互联网文本与视频丰富且是第三人称视角。机器人需要第一人称证据——"
                    "<i>它自己</i>行动之后世界变成了什么样——而这类数据的采集很昂贵。",
                    "<b>感官接口。</b>多数工作假定视觉已足够。但并非如此：接触、力与隐藏的内部状态对相机不可见，"
                    "而能够报告它们的模态各自带有独特的时间结构。",
                    "<b>时序。</b>物理智能体在延迟下运行，而它们最有能力的策略运行得很慢。"
                    "任何必须在两次决策之间被注意到的东西都会掉进这个空档。",
                    "<b>评测。</b>到达目标不等于行为正确。一个策略可以在几何指标上看起来成功，"
                    "却在真正重要的意义上出错。",
                ]),
                ("TGL 的位置", [
                    "Teach and Grow 是一个物理AI 系统。它的主题是智能体与物理世界的接口："
                    "机器人通过行动、观察结果、保留经验证的内容来获得新的操作能力。"
                    "它的主张是：对处于延迟控制下的智能体而言，把发生过的事情保留下来是一项要求，而不是可选的改进。",
                ]),
            ],
            "keywords": ("物理AI, 物理人工智能, 具身智能, 具身智能体, 物理智能体, 机器人操作, "
                         "第一人称机器人数据, 机器人学习, TGL"),
        },
    },
    {
        "slug": "llm-robotics",
        "parent": "concepts",
        "related": ["ai-agent-robotic-arm", "gpt-robotic-arm", "agentic-robotics"],
        "en": {
            "title": "LLM Robotics: What Large Language Models Add to a Robot",
            "desc": ("Large language models contribute task decomposition, tool selection and recovery to robotics, "
                     "but they cannot emit control signals. Teach-and-Grow Learning uses a multimodal LLM agent "
                     "for reasoning and leaves execution to robot-side components."),
            "h1": "LLM Robotics",
            "lede": ("LLM robotics is the use of large language models in a robot's control stack. What they "
                     "contribute is task decomposition, tool selection, state tracking and recovery — reasoning "
                     "over symbols and outcomes. What they cannot contribute is a control signal, because they do "
                     "not run at anything close to the frequency a robot needs."),
            "sections": [
                ("What an LLM is actually good for here", [
                    "Decomposing “make coffee” into ordered steps is largely a symbolic problem, and a language "
                    "model handles it well. So does choosing which tool to invoke next, noticing that an outcome "
                    "contradicts the plan, and proposing an alternative. These are the parts of a task that "
                    "benefit from a long context and slow deliberation.",
                    "Multimodal models extend this to reading the scene. An agent that can look at a camera frame "
                    "and see that the drawer did not open has something concrete to reason about, rather than "
                    "reasoning only over a text description of the state.",
                ]),
                ("What an LLM cannot do", [
                    "It cannot produce joint torques, and re-running a large model before every low-level command "
                    "is not feasible at control frequency. In practice the two layers are separated: the agent "
                    "decides what and the robot-side components handle how.",
                    "This also means the agent only knows what its tools tell it. A low-level interface that "
                    "discards information constrains the agent's reasoning, not just its control.",
                ]),
                ("How TGL uses one", [
                    "In Teach-and-Grow Learning the multimodal agent identifies subgoals shared across "
                    "demonstrations, expresses them as closed-loop Skill Blocks, and revises the remaining plan "
                    "from what the robot observed. The paper's implementation uses OpenAI GPT-6 Astra for that "
                    "reasoning, with Codex connecting the agent to the robot tools. Detection, segmentation, "
                    "RGB-D geometry, Contact-GraspNet, MPLib and controllers supply the physical grounding.",
                ]),
            ],
            "keywords": ("LLM robotics, large language model robot control, GPT robot, multimodal LLM agent "
                         "robot, tool-using LLM robot, codex robotics, TGL, Teach-and-Grow Learning, "
                         "agentic robotics"),
        },
        "zh": {
            "title": "大模型机器人学：大语言模型给机器人带来了什么",
            "desc": ("大语言模型为机器人带来任务分解、工具选择与恢复能力，但无法输出控制信号。"
                     "Teach-and-Grow Learning 用多模态大模型智能体负责推理，把执行交给机器人侧组件。"),
            "h1": "大模型机器人学（LLM Robotics）",
            "lede": ("大模型机器人学指把大语言模型用进机器人的控制栈。它们贡献的是任务分解、工具选择、状态跟踪与恢复——"
                     "也就是对符号与结果的推理。它们无法贡献的是控制信号，因为它们运行的频率远达不到机器人所需。"),
            "sections": [
                ("大模型在这里真正擅长什么", [
                    "把「煮咖啡」分解为有序步骤，基本上是符号化问题，语言模型处理得很好。"
                    "选择下一个调用哪个工具、注意到某个结果与计划矛盾、并提出替代方案，同样如此。"
                    "这些正是受益于长上下文与缓慢深思的环节。",
                    "多模态模型把这一点扩展到读取场景。一个能看着相机画面、看出抽屉没有打开的智能体，"
                    "就有了具体的对象可以推理，而不只是对一段文字状态描述做推理。",
                ]),
                ("大模型做不到什么", [
                    "它无法产生关节力矩，而在每条底层指令之前重新运行一次大模型，在控制频率下并不可行。"
                    "实践中两层被分开：智能体决定做什么，机器人侧组件处理怎么做。",
                    "这也意味着智能体只知道工具告诉它的内容。一个丢弃信息的低层接口，限制的不只是控制，"
                    "还有智能体的推理。",
                ]),
                ("TGL 如何使用大模型", [
                    "在 Teach-and-Grow Learning 中，多模态智能体识别演示之间共享的子目标，把它们表达为闭环的 Skill Block，"
                    "并根据机器人观察到的结果修正剩余计划。论文的实现使用 OpenAI GPT-6 Astra 完成这一推理，"
                    "并用 Codex 把智能体与机器人工具连接起来。检测、分割、RGB-D 几何、Contact-GraspNet、MPLib 与控制器"
                    "提供物理落地。",
                ]),
            ],
            "keywords": ("大模型机器人学, LLM 机器人控制, GPT 机器人, 多模态大模型智能体, 工具型大模型机器人, "
                         "Codex 机器人, TGL, Teach-and-Grow Learning, 智能体机器人学"),
        },
    },
    {
        "slug": "gpt-robotic-arm",
        "parent": "concepts",
        "related": ["llm-robotics", "ai-agent-robotic-arm", "agentic-robotics"],
        "en": {
            "title": "GPT and Robotic Arms: What a Large Model Can and Cannot Do for an Arm",
            "desc": ("A GPT-class model can plan and sequence a robotic arm's task in language, and a "
                     "vision-language-action model can drive it directly. Neither removes the need for physical "
                     "validation of what the arm actually did."),
            "h1": "GPT and Robotic Arms",
            "lede": ("“GPT robotic arm” describes a robot arm controlled with the help of a large pretrained "
                     "model. That happens at two levels: a language model can plan and sequence the task in "
                     "words, and a vision-language-action model can drive the arm directly. Both work. Neither "
                     "removes the need to check what the arm physically did."),
            "sections": [
                ("Level one: planning", [
                    "A language model can decompose a goal into steps, choose tools and recover from some "
                    "failures, because that reasoning is largely symbolic. It has no access to joint angles and "
                    "does not need them. This level is well established and mostly a software-integration "
                    "problem.",
                ]),
                ("Level two: direct action", [
                    "A vision-language-action model takes images, an instruction and proprioception as input and "
                    "outputs continuous actions. It works because the backbone's pretraining already produces "
                    "aligned representations of scenes and language, so comparatively little robot data suffices "
                    "to attach an action head.",
                ]),
                ("What neither level supplies", [
                    "A model can plan well and still be wrong about the world, because a plan is not evidence. "
                    "Something has to observe the physical outcome and decide whether the intended effect "
                    "actually occurred — a closed gripper is not proof that an object is held. That check is what "
                    "turns a sequence of commands into a behaviour with a defined scope.",
                    "It is also what makes repair local. When the outcome is checked against a stated effect, a "
                    "failure points at one behaviour rather than at an entire policy.",
                ]),
                ("How TGL puts this together", [
                    "Teach-and-Grow Learning uses a multimodal GPT-class agent for task-level reasoning and tool "
                    "interaction, and wraps each subgoal in a Skill Block with an outcome test. The agent decides "
                    "what should change; the robot-side executors decide how, and report back what happened.",
                ]),
            ],
            "keywords": ("GPT robotic arm, GPT robot arm, LLM robot arm, large model robotic arm, vision "
                         "language action robot arm, AI robot arm, TGL, Teach-and-Grow Learning, 大模型机械臂, "
                         "GPT 机械臂"),
        },
        "zh": {
            "title": "GPT 与机械臂：大模型能为机械臂做什么、不能做什么",
            "desc": ("GPT 级别的大模型可以用语言规划机械臂任务，视觉-语言-动作模型可以直接驱动它。"
                     "两者都不能免除对机械臂实际动作结果的物理验证。"),
            "h1": "GPT 与机械臂",
            "lede": ("「GPT 机械臂」指的是借助大型预训练模型控制的机械臂。这件事发生在两个层面："
                     "语言模型可以用文字规划并编排任务，视觉-语言-动作模型可以直接驱动机械臂。两者都可行。"
                     "但两者都不能免除对机械臂物理动作结果的检查。"),
            "sections": [
                ("层面一：规划", [
                    "语言模型可以把目标分解为步骤、选择工具、并从某些失败中恢复，因为这类推理基本上是符号化的。"
                    "它接触不到关节角，也不需要。这一层面已经相当成熟，主要是软件集成问题。",
                ]),
                ("层面二：直接动作", [
                    "视觉-语言-动作模型以图像、指令与本体感觉为输入，输出连续动作。它之所以可行，"
                    "是因为骨干的预训练已经产生了场景与语言对齐的表示，因此接上动作头所需的机器人数据相对较少。",
                ]),
                ("两个层面都不提供什么", [
                    "模型可以规划得很好，同时对世界判断错误——因为计划不是证据。"
                    "需要有东西观察物理结果，并判断意图中的效果是否真的发生：夹爪闭合并不证明物体被拿住了。"
                    "正是这一检查把一串指令变成了一个具有明确适用范围的「行为」。",
                    "它也正使修复变得局部。当结果与声明的效果对照检查时，一次失败指向的是某个行为，而不是整个策略。",
                ]),
                ("TGL 如何把它们组合起来", [
                    "Teach-and-Grow Learning 使用 GPT 级别的多模态智能体做任务级推理与工具交互，"
                    "并把每个子目标包装进带有结果检验的 Skill Block。智能体决定应该改变什么；"
                    "机器人侧执行器决定怎么做，并回报实际发生了什么。",
                ]),
            ],
            "keywords": ("GPT 机械臂, 大模型机械臂, 机械臂大模型, 大模型机器人控制, 视觉语言动作模型机械臂, "
                         "AI 机械臂, TGL, Teach-and-Grow Learning, GPT robotic arm"),
        },
    },
    {
        "slug": "ai-agent-robotic-arm",
        "parent": "concepts",
        "related": ["llm-robotics", "gpt-robotic-arm", "agentic-robotics"],
        "en": {
            "title": "AI Agent Robotic Arm: Combining an Agent Loop with a Physical Arm",
            "desc": ("An AI-agent robotic arm pairs a reasoning agent with the perception, grasping and motion "
                     "tools an arm needs. Teach-and-Grow Learning is an agent-centered design of that pairing, "
                     "with verification at every subgoal."),
            "h1": "AI Agent Robotic Arm",
            "lede": ("An AI-agent robotic arm combines a reasoning agent — which decides what to do next — with "
                     "the perception, grasping and motion components that let a physical arm do it. The design "
                     "question is where to draw the line between the two, and what evidence crosses it."),
            "sections": [
                ("The division of labour", [
                    "The agent handles what is expensive to do slowly: reading the situation, ordering subgoals, "
                    "choosing a tool, recognising that the outcome contradicts the plan. The arm-side components "
                    "handle what must be fast and physical: metric depth, collision-free motion, contact and "
                    "high-rate control. Neither side can do the other's job, and trying to merge them produces a "
                    "system that is either too slow to control or too shallow to plan.",
                ]),
                ("What crosses the boundary", [
                    "Evidence. The agent's picture of the world is exactly what its tools report, so the interface "
                    "determines what the agent can reason about. If an executor reports only “command sent”, the "
                    "agent cannot tell a successful grasp from a failed one. If it reports the intended physical "
                    "effect and whether that effect was observed, the agent has something it can act on.",
                    "This is why TGL attaches an outcome test to every Skill Block rather than treating execution "
                    "as assumed to succeed.",
                ]),
                ("Why verification makes repair local", [
                    "When each subgoal carries a test of its effect, a failure identifies a specific behaviour. "
                    "The agent can then re-observe, choose a different executor, or revise the remaining route — "
                    "without re-deriving the whole task. A demonstration that fails at one stage does not "
                    "invalidate the stages that were verified.",
                ]),
                ("From execution to accumulation", [
                    "The same structure is what makes a robotic arm accumulate capability rather than repeat "
                    "episodes. Validated behaviours enter the Skill Library with their scopes; the conditions, "
                    "outcomes, diagnoses and repairs enter Experience Memory. A later task retrieves both, so one "
                    "task can make the next easier rather than merely leaving a log behind.",
                ]),
            ],
            "keywords": ("AI agent robotic arm, agent robot arm, AI robot arm control, embodied agent robot arm, "
                         "robot agent manipulation, tool-using robot arm, TGL, Teach-and-Grow Learning, "
                         "AI 智能体机械臂"),
        },
        "zh": {
            "title": "AI 智能体机械臂：把智能体循环与物理机械臂结合起来",
            "desc": ("AI 智能体机械臂把推理智能体与机械臂所需的感知、抓取、运动工具配对。"
                     "Teach-and-Grow Learning 是这种配对的一种以智能体为中心的设计，每个子目标都带验证。"),
            "h1": "AI 智能体机械臂",
            "lede": ("AI 智能体机械臂把一个推理智能体——负责决定下一步做什么——与让物理机械臂能够执行它的感知、抓取、"
                     "运动组件结合起来。设计问题是：这条界线画在哪里，以及什么东西跨过它。"),
            "sections": [
                ("分工", [
                    "智能体负责那些可以慢慢做但代价高的部分：读取情境、排列子目标、选择工具、"
                    "识别出结果与计划矛盾。机械臂侧组件负责必须快速且物理的部分：度量深度、无碰撞运动、接触与高速控制。"
                    "任何一方都做不了另一方的活，强行合并得到的系统要么太慢无法控制，要么太浅无法规划。",
                ]),
                ("什么跨过这条界线", [
                    "证据。智能体对世界的认识恰好等于工具所报告的内容，因此接口决定了智能体能对什么进行推理。"
                    "如果执行器只报告「指令已发出」，智能体无法分辨抓取成功还是失败。"
                    "如果它报告意图中的物理效果以及该效果是否被观察到，智能体就有了可以据以行动的东西。",
                    "这正是 TGL 为每个 Skill Block 附加结果检验、而不是把执行默认为成功的原因。",
                ]),
                ("为什么验证让修复变成本地", [
                    "当每个子目标都带有对其效果的检验时，一次失败就指向一个具体的行为。"
                    "智能体可以随后重新观察、更换执行器，或修正剩余路线——而无需重新推导整个任务。"
                    "在某个阶段失败的演示，并不会使已经通过验证的阶段失效。",
                ]),
                ("从执行到积累", [
                    "正是同一套结构让机械臂积累能力而不是重复回合。经验证的行为带着适用范围进入 Skill Library；"
                    "条件、结果、诊断与修复进入 Experience Memory。后续任务会同时检索两者，"
                    "因此一个任务能让下一个更轻松，而不只是留下一份日志。",
                ]),
            ],
            "keywords": ("AI 智能体机械臂, 智能体机器人手臂, AI 机器人手臂控制, 具身智能体机械臂, "
                         "机器人智能体操作, 工具型机械臂, TGL, Teach-and-Grow Learning, agent robotic arm"),
        },
    },
]
