# MCP Long-Term Memory Engine

**Localized Knowledge Graph Architectures for Persistent LLM Context Mitigation via Model Context Protocol (MCP)**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20625302.svg)](https://doi.org/10.5281/zenodo.20625302)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## Overview

State-of-the-art Large Language Models (LLMs) are structurally constrained by fixed context windows and session-isolated statelessness. In long-cycle software engineering projects, these limitations induce "context drift" and token degradation due to repetitive codebase injections.

This repository implements a **decentralized, local persistence layer** utilizing the Model Context Protocol (MCP). By anchoring an arbitrary LLM agent to a local SQLite-backed Knowledge Graph, it provides a deterministic approach to cross-session memory preservation.

**Empirically validated on Project Zorthex™** — demonstrating near-zero context initialization latency and significant reduction in token consumption overhead.

---

## Quick Setup (3 steps)

**Step 1 — Clone the repository**
```bash
git clone https://github.com/zorthex2026/mcp-longterm-memory-engine.git
cd mcp-longterm-memory-engine
```

**Step 2 — Install the only dependency**
```bash
pip install fastmcp
```

> `fastmcp` is the only external library required. Everything else (SQLite, json, datetime) is included in Python's standard library.

**Step 3 — Start the MCP server**
```bash
python src/mcp_memory_server.py
```

The server is now running and ready to connect to your LLM agent.

---

## What is SQLite?

SQLite is a lightweight database that lives as a **single file** on your computer (`memory.db`). It requires no installation, no server, no password. Python includes it by default.

When you run the engine for the first time, it automatically creates `memory.db` in your working directory. You can copy, move, or back it up like any regular file.

---

## What is MCP?

The **Model Context Protocol (MCP)** is an open standard that allows LLM agents (Claude, GPT, etc.) to call external tools and retrieve structured data. This engine exposes the Knowledge Graph as a set of MCP tools that any compatible LLM can call directly.

---

## Key Features

- **Local-first**: All data stored in a local SQLite database — nothing leaves your infrastructure
- **MCP-native**: Built on the Model Context Protocol for seamless LLM integration
- **Knowledge Graph**: Structured entity-relationship storage, not flat key-value pairs
- **Cross-session persistence**: Memory survives session boundaries deterministically
- **Zero cloud dependency**: No external APIs required for memory operations
- **MIT licensed**: Free to use, modify, and distribute

---

## Why This Matters

Standard LLM deployments suffer from:

| Problem | Impact |
|---------|--------|
| Fixed context window | Long projects require constant re-injection of context |
| Session statelessness | Each session starts from zero |
| Token overhead | Repeated context injection wastes tokens and increases latency |
| Context drift | Critical decisions and methodology get lost over time |

This engine solves all four by maintaining a persistent, structured knowledge graph that the LLM can query instead of re-reading entire codebases or conversation histories.

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│                  LLM Agent                       │
│              (Claude, GPT, etc.)                 │
└──────────────────┬──────────────────────────────┘
                   │ MCP Protocol
┌──────────────────▼──────────────────────────────┐
│              MCP Memory Server                   │
│         (src/mcp_memory_server.py)               │
└──────────────────┬──────────────────────────────┘
                   │ SQLite queries
┌──────────────────▼──────────────────────────────┐
│           Local Knowledge Graph                  │
│              (memory.db — single file)           │
│                                                  │
│  Entities ──── Relations ──── Observations      │
└─────────────────────────────────────────────────┘
```

---

## Quick Start (Python)

```python
from src.memory_engine import MemoryEngine

# Initialize — creates memory.db automatically
engine = MemoryEngine(db_path="./memory.db")

# Store context
engine.create_entity("my_project", "project", [
    "This project does X",
    "Key decision: we chose approach Y because Z",
    "Current status: phase 2 complete"
])

# Link entities
engine.create_relation("my_project", "uses", "methodology_A")

# Retrieve context in a future session
results = engine.search_nodes("phase 2")
print(results)
# → [{"name": "my_project", "observations": ["Current status: phase 2 complete", ...]}]
```

---

## MCP Integration (Claude Desktop)

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "longterm-memory": {
      "command": "python",
      "args": ["/full/path/to/src/mcp_memory_server.py"],
      "env": {
        "MEMORY_DB_PATH": "/full/path/to/memory.db"
      }
    }
  }
}
```

Restart Claude Desktop. The memory tools will appear automatically.

---

## Available MCP Tools

| Tool | Description |
|------|-------------|
| `create_entities` | Add one or more entities to the graph |
| `create_relations` | Link two entities with a named relation |
| `add_observations` | Add facts to an existing entity |
| `search_nodes` | Search across all entities and observations |
| `open_nodes` | Retrieve specific entities by name |
| `read_graph` | Export the full knowledge graph |
| `delete_entities` | Remove entities and their relations |

---

## Cross-Session Persistence — Example

```
# Session 1 (Monday):
User: "Store our decision to use SHA-256 for document hashing"
Claude: [calls create_entities] → stored in memory.db

# Session 2 (Friday, fresh start):
User: "What hashing algorithm did we decide on?"
Claude: [calls search_nodes("hashing")] → retrieves exact decision from memory.db
```

No re-injection of hundreds of pages. No context drift. Deterministic retrieval.

---

## Research Context

This engine was developed as part of **Project Zorthex™** — an independent research framework measuring diffusion lag (L) in AI adoption across institutional contexts.

The persistent memory problem is structurally related to the "diffusion lag" concept at the core of Zorthex: just as institutions fail to adapt to new norms within measurable time windows, LLM agents fail to retain critical context across session boundaries. Both problems are solved by the same architectural principle: **explicit, verifiable, timestamped state**.

### Related Work

- Zorthex™ Diffusion Lag Framework: [DOI 10.5281/zenodo.20589503](https://doi.org/10.5281/zenodo.20589503)
- Didisheim, Kelly, Pourmohammadi & Tian (2026) — *The Inefficient Pricing of News*
- Anthropic Economic Index (2025) — diffusion patterns in AI adoption

---

## Citation

```bibtex
@software{santi2026mcp,
  author    = {Santi, Renato},
  title     = {MCP Long-Term Memory Engine: A Local Knowledge Graph for Persistent LLM Context via Model Context Protocol},
  year      = {2026},
  doi       = {10.5281/zenodo.20625302},
  url       = {https://github.com/zorthex2026/mcp-longterm-memory-engine},
  license   = {MIT}
}
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Author

**Renato Santi**  
Independent Researcher  
ORCID: [0009-0000-9936-1110](https://orcid.org/0009-0000-9936-1110)  
Zenodo: [zenodo.org/records/20625302](https://zenodo.org/records/20625302)

---

*Part of the Zorthex™ research ecosystem · Sassari, Italy · 2026*
