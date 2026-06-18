# MCP Long-Term Memory Engine

**Localized Knowledge Graph Architectures for Persistent LLM Context Mitigation via Model Context Protocol (MCP)**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20625302.svg)](https://doi.org/10.5281/zenodo.20625302)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## Overview

State-of-the-art Large Language Models (LLMs) are structurally constrained by fixed context windows and session-isolated statelessness. In long-cycle software engineering projects, these limitations induce "context drift" and token degradation due to repetitive codebase injections.

This repository implements a **decentralized, local persistence layer** utilizing the Model Context Protocol (MCP). By anchoring an arbitrary LLM agent to a local SQLite-backed Knowledge Graph, it provides a deterministic approach to cross-session memory preservation.

**Empirically validated on Project Zorthex™** — demonstrating near-zero context initialization latency and significant reduction in token consumption overhead.

## Key Features

- **Local-first**: All data stored in a local SQLite database — nothing leaves your infrastructure
- **MCP-native**: Built on the Model Context Protocol for seamless LLM integration
- **Knowledge Graph**: Structured entity-relationship storage, not flat key-value pairs
- **Cross-session persistence**: Memory survives session boundaries deterministically
- **Zero cloud dependency**: No external APIs required for memory operations
- **MIT licensed**: Free to use, modify, and distribute

## Why This Matters

Standard LLM deployments suffer from:

| Problem | Impact |
|---------|--------|
| Fixed context window | Long projects require constant re-injection of context |
| Session statelessness | Each session starts from zero |
| Token overhead | Repeated context injection wastes tokens and increases latency |
| Context drift | Critical decisions and methodology get lost over time |

This engine solves all four by maintaining a persistent, structured knowledge graph that the LLM can query instead of re-reading entire codebases or conversation histories.

## Architecture

```
┌─────────────────────────────────────────────────┐
│                  LLM Agent                       │
│              (Claude, GPT, etc.)                 │
└──────────────────┬──────────────────────────────┘
                   │ MCP Protocol
┌──────────────────▼──────────────────────────────┐
│              MCP Memory Server                   │
│         (mcp_memory_server.py)                   │
└──────────────────┬──────────────────────────────┘
                   │ SQLite queries
┌──────────────────▼──────────────────────────────┐
│           Local Knowledge Graph                  │
│              (SQLite + JSON)                     │
│                                                  │
│  Entities ──── Relations ──── Observations      │
└─────────────────────────────────────────────────┘
```

## Installation

```bash
git clone https://github.com/zorthex2026/mcp-longterm-memory-engine.git
cd mcp-longterm-memory-engine
pip install -r requirements.txt
```

## Quick Start

```python
from src.memory_engine import MemoryEngine

# Initialize the engine
engine = MemoryEngine(db_path="./memory.db")

# Create entities
engine.create_entity("project_zorthex", "project", [
    "Dataset v2.0 with 70 verified cases",
    "Scanner accuracy: 90% on 10-case test set",
    "DOI: 10.5281/zenodo.20589503"
])

# Create relations
engine.create_relation("project_zorthex", "uses", "aba_opinion_512")

# Query context
context = engine.search("scanner calibration")
print(context)
```

## MCP Integration

Add to your MCP configuration:

```json
{
  "mcpServers": {
    "longterm-memory": {
      "command": "python",
      "args": ["path/to/mcp_memory_server.py"],
      "env": {
        "MEMORY_DB_PATH": "./project_memory.db"
      }
    }
  }
}
```

## API Reference

### Core Operations

| Method | Description |
|--------|-------------|
| `create_entity(name, type, observations)` | Add a new entity to the graph |
| `create_relation(from, relation, to)` | Link two entities |
| `add_observation(entity, observation)` | Add a fact to an existing entity |
| `search_nodes(query)` | Semantic search across the graph |
| `open_nodes(names)` | Retrieve specific entities by name |
| `read_graph()` | Export the full knowledge graph |
| `delete_entity(name)` | Remove an entity and its relations |

## Research Context

This engine was developed as part of **Project Zorthex™** — an independent research framework measuring diffusion lag (L) in AI adoption across institutional contexts.

The persistent memory problem is structurally related to the "diffusion lag" concept at the core of Zorthex: just as institutions fail to adapt to new norms within measurable time windows, LLM agents fail to retain critical context across session boundaries. Both problems are solved by the same architectural principle: **explicit, verifiable, timestamped state**.

### Related Work

- Zorthex™ Diffusion Lag Framework: [DOI 10.5281/zenodo.20589503](https://doi.org/10.5281/zenodo.20589503)
- Didisheim, Kelly, Pourmohammadi & Tian (2026) — *The Inefficient Pricing of News*
- Anthropic Economic Index (2025) — diffusion patterns in AI adoption

## Citation

```bibtex
@software{santi2026mcp,
  author    = {Santi, Renato},
  title     = {Localized Knowledge Graph Architectures for Persistent LLM Context Mitigation via Model Context Protocol (MCP)},
  year      = {2026},
  doi       = {10.5281/zenodo.20625302},
  url       = {https://github.com/zorthex2026/mcp-longterm-memory-engine},
  license   = {MIT}
}
```

## License

MIT License — see [LICENSE](LICENSE) for details.

## Author

**Renato Santi**  
Independent Researcher  
ORCID: [0009-0000-9936-1110](https://orcid.org/0009-0000-9936-1110)  
Zenodo: [zenodo.org/records/20625302](https://zenodo.org/records/20625302)

---

*Part of the Zorthex™ research ecosystem · Sassari, Italy · 2026*
