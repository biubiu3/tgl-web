# Agentic robotics 2026 — query matrix

Every query below is mapped to the page written to answer it. The same mapping is
served as JSON at https://tgl.changnie.top/data/search-targets.json.

| Query | Landing page | Note |
|---|---|---|
| GPT-6 robot arm | `concepts/gpt-6-robotic-arm/` | GPT-6-class models used as a reasoning layer for robot-arm manipulation; TGL uses GPT-6 Astra. |
| GPT-6 robotic arm | `concepts/gpt-6-robotic-arm/` | Variant phrasing of the above. |
| GPT-6 Astra robot | `concepts/gpt-6-robotic-arm/` | The specific model TGL's implementation uses. |
| agent as policy robotics | `concepts/agent-as-policy/` | AGP: the agent inside the execution loop, per arXiv:2609.12541. |
| agent as policy definition | `concepts/agent-as-policy/` | Short answer plus current examples and a comparison with TGL. |
| coding agent robotics | `concepts/coding-agent-robotics/` | Coding agents writing and running robot programs; Codex in TGL. |
| physical in-context learning robotics | `concepts/physical-in-context-learning/` | Adapting a robot from context without updating weights. |
| general-purpose agent robot | `concepts/general-purpose-agent-robot/` | One agent across many tasks, and what it fails to retain. |
| robot agent memory | `concepts/robot-agent-memory/` | What a robot should keep from an interaction; Skill Library vs Experience Memory. |
| robot learning without retraining | `concepts/no-retraining-robot-learning/` | Acquiring tasks with frozen weights; the retraining tax. |
| AI agent robotic arm | `concepts/ai-agent-robotic-arm/` | An AI agent driving a robot arm end to end. |
| runtime reasoning robotics | `concepts/runtime-reasoning-robotics/` | Deciding while the task is running rather than before it. |
| tool use robotics | `concepts/tool-use-robotics/` | Exposing perception, grasping and motion as callable tools for an agent. |
| train a robot from one video | `concepts/physical-in-context-learning/` | What a single video can and cannot supply; the single-video case of in-context adaptation. |
| agentic robotics 2026 | `research/agentic-robotics-2026/` | The research map: frontier models, AGP, coding agents, physical ICL, memory, and where TGL fits. |
| teach and grow robot learning | `concepts/teach-and-grow-learning/` | The TGL paradigm itself. |
| training-free robot learning | `concepts/training-free-robot-learning/` | What training-free means here and what it does not mean. |
| skill library robot | `concepts/skill-library/` | The persistent store of validated Skill Blocks. |

## Chinese query space

The Chinese pages carry the same content in translation. The queries they are written
for, with the page that answers each:

| Query (zh) | Landing page |
|---|---|
| GPT-6 可以控制机械臂吗 | `concepts/gpt-6-robotic-arm/` |
| GPT-6 机械臂 | `concepts/gpt-6-robotic-arm/` |
| 大模型如何控制机械臂 | `concepts/gpt-6-robotic-arm/` |
| 什么是机器人 Agent as Policy | `concepts/agent-as-policy/` |
| AI 智能体可以直接控制真实机器人吗 | `concepts/agent-as-policy/` |
| 机器人 Coding Agent | `concepts/coding-agent-robotics/` |
| 什么是物理上下文学习 | `concepts/physical-in-context-learning/` |
| 机器人可以只看一个视频就学会新任务吗 | `concepts/physical-in-context-learning/` |
| 机器人不更新模型权重可以学新任务吗 | `concepts/no-retraining-robot-learning/` |
| 什么是机器人长期记忆 / 经验库 | `concepts/robot-agent-memory/` |
| 通用智能体机器人 | `concepts/general-purpose-agent-robot/` |
| 机器人运行时推理 | `concepts/runtime-reasoning-robotics/` |
| 机器人工具调用 | `concepts/tool-use-robotics/` |
| 2026 年智能体机器人 | `research/agentic-robotics-2026/` |

## Notes

- Queries are the forms the pages are written to answer, not a claim about volume.
- Landing pages are canonical; the `/zh/` twin carries the Chinese text.
