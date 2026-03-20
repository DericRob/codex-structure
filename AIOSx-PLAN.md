# AIOSx Plan

## Purpose

AIOSx should be a separate GitHub repository that combines:

- the practical local developer experience from this repo (`AIOS`)
- the kernel/runtime architecture from `agiresearch/AIOS`
- the operating-system framing described in the AIOS paper

The goal is not to clone either project. The goal is to build a usable "AI operating layer" that is:

- local-first
- observable
- policy-aware
- agent-runtime capable
- simple enough for real developer workflows

## What Is Different Today

### This repo (`AIOS`)

This repo is a Codex-native setup and operations kit.

- It standardizes local setup for Codex.
- It injects startup context (`CODEX.md`), MCP config, memory files, and skills.
- It includes a watcher that reads local Codex session logs and exposes a dashboard plus alerts.
- It is focused on reproducibility, governance, and developer workflow support.

This is not a true agent kernel or agent execution platform. It is closer to:

- environment bootstrap
- prompt/runtime configuration
- memory packaging
- local observability
- operational guardrails

### `agiresearch/AIOS`

That project is trying to be an actual agent operating system kernel plus SDK.

- It separates application, kernel, and hardware layers.
- It treats LLM access, memory, storage, tools, scheduling, and access control as kernel-managed resources.
- It uses an SDK and system-call style interface for agents.
- It aims to run multiple agents/frameworks under a common runtime model.

That is a runtime platform, not just a setup repo.

## What The Video Is Talking About

Based on the transcript you provided, the video is explicitly describing AIOS as:

- "LLM as OS / agents as apps"
- a kernel that manages agent resources
- scheduling and context switching for LLM workloads
- memory, storage, tools, and access control as operating-system concerns
- a locally deployable system for running agents on a user's machine

This is conceptually different from your current repo. Your repo is focused on making Codex usable, observable, and reproducible on a real machine. Their AIOS is focused on building a general runtime substrate for many agents and frameworks.

## Updated Direct Comparison

### Your current `AIOS` repo

What it actually is:

- a Codex-native workstation bootstrap repo
- a local watcher and alerting system for Codex session activity
- a packaging format for memory, MCP config, startup prompts, and skills
- an operational control layer for a developer machine

What it is not:

- not a scheduler for multiple agents
- not a kernel that exposes syscall-style agent services
- not a general-purpose LLM runtime
- not an execution substrate for many agent frameworks

### The paper/repo/video AIOS

What it actually is trying to be:

- an LLM agent operating system
- an application layer plus kernel layer plus hardware layer model
- a runtime with modules such as scheduler, context manager, memory manager, storage manager, tool manager, and access manager
- a system where agents call into runtime services instead of manually wiring everything themselves

What it is not primarily focused on:

- not mainly about bootstrap scripts and local machine setup
- not mainly about Codex session observability
- not mainly about prompt injection wrappers or memory-file packaging

### Bottom line

Your repo is an operational shell around one AI developer environment.

The research/video AIOS is a kernel-oriented runtime for many AI agents.

AIOSx should bridge that gap.

## AIOSx Thesis

AIOSx should combine:

- your repo's strong local UX, watcher, memory packaging, and policy orientation
- their repo's kernel abstraction, scheduling model, and syscall-based resource management

AIOSx should avoid:

- becoming only a prompt/template repo
- becoming only a research-kernel demo that is hard to adopt

## AIOSx Repo Definition

### Repository name

`AIOSx`

### One-sentence pitch

AIOSx is a local-first agent operating platform that combines developer setup, policy enforcement, runtime observability, and kernel-style resource management for AI agents.

## Recommended Scope For V1

### Keep from this repo

- watcher dashboard and alert model
- Codex launcher pattern
- memory bootstrapping
- machine bootstrap templates
- local policy/config files
- Windows and Unix launcher support
- practical developer-workstation focus
- local-first auditability

### Keep from `agiresearch/AIOS`

- application/kernel split
- scheduler abstraction
- context manager idea
- memory/storage/tool manager separation
- syscall-style interfaces between agents and runtime services
- multi-agent and multi-framework orientation

### Do not copy directly into V1

- full research-style framework breadth
- every supported backend or model provider
- broad UI surface area
- heavyweight distributed kernel design
- video-style "brain of the OS" framing without clear operational boundaries

V1 should be narrower and operationally clean.

## Proposed Architecture

### Layer 1: Developer Experience Layer

- installer/bootstrap scripts
- local config generation
- launcher wrappers
- project memory and policy loading

### Layer 2: Control Plane

- watcher ingestion
- audit/event bus
- policy engine
- risk scoring and alerts
- dashboard/API
- session replay and runtime traces

### Layer 3: Agent Runtime Kernel

- agent scheduler
- model router / LLM core abstraction
- tool manager
- memory manager
- storage manager
- access manager
- syscall API

### Layer 4: Execution Adapters

- Codex adapter
- OpenAI Responses/API adapter
- MCP adapter
- shell/file adapter
- optional framework adapters for AutoGen/Open Interpreter style agents

## Suggested Repository Structure

```text
AIOSx/
├── README.md
├── docs/
│   ├── architecture.md
│   ├── policy-model.md
│   ├── watcher-model.md
│   └── adapters.md
├── bootstrap/
│   ├── install.ps1
│   ├── install.sh
│   └── templates/
├── kernel/
│   ├── scheduler/
│   ├── context/
│   ├── memory/
│   ├── storage/
│   ├── tools/
│   ├── access/
│   └── syscalls/
├── controlplane/
│   ├── watcher/
│   ├── alerts/
│   ├── api/
│   └── dashboard/
├── adapters/
│   ├── codex/
│   ├── mcp/
│   ├── openai/
│   └── shell/
├── sdk/
│   ├── python/
│   └── types/
├── examples/
│   ├── coding-agent/
│   ├── documentation-agent/
│   └── review-agent/
└── tests/
```

## Phase Plan

### Phase 1: Foundation

- Create the separate `AIOSx` repo.
- Move the current watcher, launcher, and template ideas into a clean bootstrap/control-plane layout.
- Define a normalized event schema for agent actions, tool calls, alerts, and policy decisions.
- Write a short architecture note that explicitly distinguishes "bootstrap/control plane" from "runtime kernel."

### Phase 2: Runtime Kernel

- Implement a minimal scheduler.
- Add a syscall-style internal interface for model, tool, memory, and storage requests.
- Build a simple policy engine around tool access and file/shell boundaries.
- Add context snapshot and restore support for long-running or interrupted agent tasks.

### Phase 3: Adapters

- Add a Codex adapter first.
- Add MCP integration second.
- Add an OpenAI-native adapter third for non-Codex runtime use.

### Phase 4: Operationalization

- Expand the watcher into a proper control-plane service.
- Add replay, audit export, and policy analytics.
- Add developer/team deployment profiles.

## Main Design Principles

- Local-first by default
- Clear separation between bootstrap, control plane, and runtime kernel
- Observability is a first-class feature, not an afterthought
- Policies and approvals must be runtime-native
- Adapters should be replaceable
- Start with one strong workflow before generalizing

## Best Initial Use Cases

- Coding-agent workstations with policy and audit requirements
- Regulated or security-sensitive engineering environments
- Teams that need reproducible AI-assisted developer environments
- Organizations that want both agent runtime capability and operator visibility
- Local AI assistant deployments where developers want the video's "AI in the OS" idea without losing control or traceability

## Immediate Next Steps

1. Create a new GitHub repo named `AIOSx`.
2. Seed it with `README.md`, `docs/architecture.md`, and the skeleton folders above.
3. Port the watcher into `controlplane/watcher/`.
4. Define the event schema and policy schema before adding more features.
5. Implement the first runtime kernel as a narrow local service, not a distributed system.
6. Add a Codex adapter as the first supported agent environment.

## Notes On Source Interpretation

- The comparison to `agiresearch/AIOS` is based on its public GitHub repo and the AIOS paper.
- The video interpretation is now based on the transcript text you supplied, not inference alone.
