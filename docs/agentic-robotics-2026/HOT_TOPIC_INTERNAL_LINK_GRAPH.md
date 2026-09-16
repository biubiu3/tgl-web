# Hot-topic internal link graph

Generated from `scripts/pages_hot.py` and the generated footers. Every edge was
verified against the built HTML by `scripts/check_site.py`.

## Hub to concept pages

- `/research/agentic-robotics-2026/` → `gpt-6-robotic-arm/`
- `/research/agentic-robotics-2026/` → `agent-as-policy/`
- `/research/agentic-robotics-2026/` → `physical-in-context-learning/`

## Concept pages to the hub

Every hot concept page links back to the research map, so the cluster is connected in both directions.

- `/concepts/gpt-6-robotic-arm/` → `/research/agentic-robotics-2026/`  (also → `agent-as-policy/`, `llm-robotics/`, `ai-agent-robotic-arm/`)
- `/concepts/agent-as-policy/` → `/research/agentic-robotics-2026/`  (also → `gpt-6-robotic-arm/`, `coding-agent-robotics/`, `general-purpose-agent-robot/`)
- `/concepts/coding-agent-robotics/` → `/research/agentic-robotics-2026/`  (also → `agent-as-policy/`, `tool-use-robotics/`, `gpt-6-robotic-arm/`)
- `/concepts/physical-in-context-learning/` → `/research/agentic-robotics-2026/`  (also → `no-retraining-robot-learning/`, `agent-as-policy/`, `robot-agent-memory/`)
- `/concepts/general-purpose-agent-robot/` → `/research/agentic-robotics-2026/`  (also → `agent-as-policy/`, `ai-agent-robotic-arm/`, `general-robot-learning/`)
- `/concepts/no-retraining-robot-learning/` → `/research/agentic-robotics-2026/`  (also → `training-free-robot-learning/`, `retraining-tax/`, `physical-in-context-learning/`)
- `/concepts/robot-agent-memory/` → `/research/agentic-robotics-2026/`  (also → `experience-memory/`, `skill-library/`, `general-purpose-agent-robot/`)
- `/concepts/runtime-reasoning-robotics/` → `/research/agentic-robotics-2026/`  (also → `agent-as-policy/`, `tool-use-robotics/`, `robot-agent-memory/`)
- `/concepts/tool-use-robotics/` → `/research/agentic-robotics-2026/`  (also → `agent-as-policy/`, `coding-agent-robotics/`, `runtime-reasoning-robotics/`)

## Homepage footer

The English and Chinese homepages link to the hub and to five hot concept pages:

`/` → `/research/agentic-robotics-2026/`, `/concepts/gpt-6-robotic-arm/`,
`/concepts/agent-as-policy/`, `/concepts/coding-agent-robotics/`,
`/concepts/physical-in-context-learning/`, `/concepts/robot-agent-memory/`

## Machine-file links

- `llms.txt` → every page in `## Pages`, plus `## Current agentic-robotics context`
- `llms-full.txt` → nine `# TGL and …` sections and `# 2026 Agentic Robotics Research Landscape`
- `project.json` → `research_context_2026.pages` and `topics`
- `related-work.json` → `categories`, each naming its page
- `page-index.json` → every generated page with its type
