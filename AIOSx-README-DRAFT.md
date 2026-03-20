# AIOSx

AIOSx is a local-first agent operating platform that combines developer setup, policy enforcement, runtime observability, and kernel-style resource management for AI agents.

## Why AIOSx

There are two useful but incomplete patterns in the current AI tooling landscape:

- practical local developer environments that are easy to run but weak on runtime architecture
- ambitious agent operating system designs that are strong on architecture but harder to operationalize

AIOSx is intended to bridge that gap.

It combines:

- the workstation bootstrap, watcher, policy, and observability strengths of this `AIOS` repo
- the kernel-style scheduler, memory, tool, access, and syscall ideas described in the AIOS paper and `agiresearch/AIOS`

The goal is not to build a metaphorical "AI brain for the OS." The goal is to build a usable operating layer for real agent workflows with clear controls, visibility, and practical developer adoption.

## What AIOSx Is

AIOSx is designed to be:

- local-first
- observable
- policy-aware
- agent-runtime capable
- adapter-driven
- usable on real developer workstations

AIOSx should provide:

- a bootstrap layer for developer setup
- a control plane for audit, policy, and alerting
- a runtime kernel for agent scheduling and resource access
- adapters for concrete execution environments such as Codex, MCP, and OpenAI-native agents

## What AIOSx Is Not

AIOSx is not intended to be:

- just a prompt/template repo
- just a research demo
- a broad distributed systems platform in V1
- a replacement for the host operating system

The first version should be narrow, local, and operationally disciplined.

## Problem Statement

Teams increasingly want to run AI agents locally for coding, review, documentation, analysis, and operational automation. Today, that usually means:

- inconsistent local setup
- weak observability into what agents are doing
- ad hoc policy controls
- poor traceability for risky tool use
- no clean separation between agent applications and runtime services

AIOSx addresses those issues by treating agent execution as a platform concern rather than a pile of scripts.

## Core Design

AIOSx has four layers.

### 1. Developer Experience Layer

- installer/bootstrap scripts
- launcher wrappers
- project memory and policy loading
- local config generation

### 2. Control Plane

- watcher ingestion
- audit/event bus
- alerting and risk scoring
- dashboard/API
- replay and runtime traces

### 3. Agent Runtime Kernel

- agent scheduler
- context manager
- memory manager
- storage manager
- tool manager
- access manager
- syscall-style runtime interface

### 4. Execution Adapters

- Codex adapter
- MCP adapter
- OpenAI Responses/API adapter
- shell/file adapter

## How It Differs From The Current `AIOS` Repo

This repo is a Codex-native workstation operations kit. It standardizes setup, loads project memory, and adds watcher-based observability.

AIOSx goes further.

It adds:

- a runtime kernel rather than just bootstrap/configuration
- scheduler and context management
- managed access to tools, memory, and storage
- policy-native execution boundaries
- a platform model that can support more than one agent environment

## Example Use Cases

- coding-agent workstations with auditable tool use
- policy-aware local AI assistants for regulated environments
- internal developer platforms that need reproducible AI setup
- local review/documentation/debugging agents with runtime controls
- multi-agent development workflows where operators need visibility

## V1 Scope

V1 should focus on a strong local implementation, not maximal breadth.

### Include in V1

- bootstrap/install flow
- event schema and watcher ingestion
- audit dashboard and alerts
- minimal agent scheduler
- tool, memory, and access management interfaces
- Codex adapter
- MCP integration

### Exclude from V1

- broad framework coverage
- distributed orchestration
- many model backends
- enterprise multi-tenant complexity
- excessive UI scope

## Proposed Repository Layout

```text
AIOSx/
├── README.md
├── docs/
│   ├── architecture.md
│   ├── leadership-brief.md
│   ├── policy-model.md
│   ├── watcher-model.md
│   └── adapters.md
├── bootstrap/
│   ├── install.ps1
│   ├── install.sh
│   └── templates/
├── controlplane/
│   ├── watcher/
│   ├── alerts/
│   ├── api/
│   └── dashboard/
├── kernel/
│   ├── scheduler/
│   ├── context/
│   ├── memory/
│   ├── storage/
│   ├── tools/
│   ├── access/
│   └── syscalls/
├── adapters/
│   ├── codex/
│   ├── mcp/
│   ├── openai/
│   └── shell/
├── sdk/
│   ├── python/
│   └── types/
├── examples/
└── tests/
```

## Initial Roadmap

### Phase 1

- create the separate `AIOSx` repository
- define the normalized event schema
- port watcher/control-plane concepts into the new layout
- document the architecture and policy model

### Phase 2

- implement a minimal scheduler
- add runtime interfaces for tools, memory, storage, and access
- add context snapshot and restore support

### Phase 3

- add the Codex adapter
- add MCP support
- add OpenAI-native adapter support

### Phase 4

- expand replay, analytics, and deployment profiles
- refine policy enforcement and audit workflows

## Design Principles

- local-first by default
- observability first
- explicit policy boundaries
- clear separation between bootstrap, control plane, and runtime kernel
- adapters should be replaceable
- practical workflows before architectural breadth

## Current Status

AIOSx is currently a defined target architecture and repo plan, not yet a standalone implementation.

The immediate next step is to create a separate repository and seed it with:

- `README.md`
- `docs/architecture.md`
- `docs/leadership-brief.md`
- base folder structure
- first control-plane/event schema definitions

## Source Basis

This draft is based on:

- the current `AIOS` repo in this workspace
- the `agiresearch/AIOS` public repository
- the AIOS research paper
- the provided video transcript describing AIOS as an LLM agent operating system with scheduler, context, memory, storage, tool, and access modules
