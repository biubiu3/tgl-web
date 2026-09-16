# Agentic robotics 2026 — related work

Served as JSON at https://tgl.changnie.top/data/agentic-robotics-2026.json.

**Every arXiv identifier below was resolved against the arXiv API on 2026-09-16 before it was
written.** Identifiers that could not be resolved are not listed — several 2026 items that
circulate in discussion could not be traced to a primary source and are deliberately absent.

| Work | Date | Identifier | Relation to TGL |
|---|---|---|---|
| Agent as Policy for Robotic Manipulation | 2026-09-11 | [2609.12541](https://arxiv.org/abs/2609.12541) | Same control locus — an agent inside the execution loop. TGL adds the persistence layer AGP does not define: a Skill Library and Experience Memory. |
| Revisiting the "Push-T" Robot Manipulation Task with Agentic Robotics | 2026-08-18 | [2608.18227](https://arxiv.org/abs/2608.18227) | Evidence for the coding-agent-for-robots pattern TGL uses via Codex, and a direct comparison between a written program and a learned policy. |
| Agentic Robot: A Brain-Inspired Framework for Vision-Language-Action Models in Embodied Agents | 2025-05-29 | [2505.23450](https://arxiv.org/abs/2505.23450) | Shares the diagnosis that execution needs verification. TGL makes the effect check part of each Skill Block's contract rather than a layer around the policy. |
| Code as Policies: Language Model Programs for Embodied Control | 2022-09-16 | [2209.07753](https://arxiv.org/abs/2209.07753) | The lineage TGL's Codex role descends from; TGL adds validation and persistence around the written program. |
| Do As I Can, Not As I Say: Grounding Language in Robotic Affordances | 2022-04-04 | [2204.01691](https://arxiv.org/abs/2204.01691) | The planning-side predecessor; TGL's grounding happens per subgoal against the current scene. |
| ReKep: Spatio-Temporal Reasoning of Relational Keypoint Constraints for Robotic Manipulation | 2024-09-03 | [2409.01652](https://arxiv.org/abs/2409.01652) | A different route to closed-loop reliability: constraints rather than validated reusable blocks. |

## Categories

`related-work.json` groups the neighbouring directions under eight categories:

- **frontier-model-robot-control** — Frontier-model robot control; page `concepts/gpt-6-robotic-arm/`; the reasoning layer TGL leaves frozen
- **agent-as-policy** — Agent as Policy (AGP); page `concepts/agent-as-policy/`; shared control locus; TGL adds persistence (Jia et al., arXiv:2609.12541 (2026))
- **coding-agent-robotics** — Coding agents for robotics; page `concepts/coding-agent-robotics/`; the role Codex plays in TGL
- **physical-in-context-learning** — Physical in-context learning; page `concepts/physical-in-context-learning/`; TGL writes the adaptation into stores that outlive the context
- **robot-agent-memory** — Robot agent memory; page `concepts/robot-agent-memory/`; Skill Library plus Experience Memory
- **single-video-robot-learning** — Single-video task acquisition; page `concepts/physical-in-context-learning/`; context supplies structure; TGL supplies the grounded realization
- **agentic-vla** — Agentic VLA; page `concepts/vla-without-retraining/`; TGL keeps the VLA fixed and stores new capability outside it
- **physical-ai-agent** — Physical AI agent; page `concepts/physical-ai/`; application framing

## What TGL claims relative to these

TGL shares the control locus of the agentic line — an agent inside the execution loop — and
differs on persistence. The report's claim is narrow: for a robot acquiring tasks over time,
storing validated behaviour and the conditions of its use as explicit objects makes each
acquisition local, provided grounding, validation, compatibility and retrieval stay manageable.
