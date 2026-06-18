# Example Usage

## Basic Knowledge Graph Operations

```python
from src.memory_engine import MemoryEngine

engine = MemoryEngine(db_path="./my_project.db")

# Store project context
engine.create_entity("zorthex_project", "project", [
    "Framework measuring diffusion lag (L) in AI adoption",
    "Two metrics: L1 (public attention) and L2 (institutional adaptation)",
    "Dataset: 70 verified cases, 7 domains",
    "DOI: 10.5281/zenodo.20589503"
])

# Store a methodological decision
engine.create_entity("aba_opinion_512", "policy", [
    "ABA Formal Opinion 512, July 2024",
    "Establishes AI supervision obligations for lawyers",
    "Used as t_policy anchor for US L2 calculations"
])

# Link entities
engine.create_relation("zorthex_project", "references", "aba_opinion_512")

# Later — retrieve context
results = engine.search_nodes("L2 calibration")
for r in results:
    print(r["name"], ":", r["observations"])
```

## MCP Server Integration

Start the server:
```bash
MEMORY_DB_PATH=./project.db python src/mcp_memory_server.py
```

Configure in Claude Desktop (claude_desktop_config.json):
```json
{
  "mcpServers": {
    "longterm-memory": {
      "command": "python",
      "args": ["/path/to/src/mcp_memory_server.py"],
      "env": {
        "MEMORY_DB_PATH": "/path/to/project_memory.db"
      }
    }
  }
}
```

## Cross-Session Persistence

The key advantage: context survives session boundaries.

Session 1:
```
User: Store our calibration methodology
Claude: [calls create_entities with methodology details]
```

Session 2 (days later):
```
User: What was our calibration methodology?
Claude: [calls search_nodes("calibration")] → retrieves exact methodology
```

No re-injection of hundreds of pages of context required.
