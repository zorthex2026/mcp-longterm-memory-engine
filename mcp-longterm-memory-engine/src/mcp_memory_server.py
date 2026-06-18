#!/usr/bin/env python3
"""
MCP Memory Server
Exposes the Knowledge Graph via Model Context Protocol.

Author: Renato Santi
DOI: 10.5281/zenodo.20625302
License: MIT
"""

import os
import json
from fastmcp import FastMCP
from memory_engine import MemoryEngine

DB_PATH = os.environ.get("MEMORY_DB_PATH", "./project_memory.db")
engine = MemoryEngine(db_path=DB_PATH)
mcp = FastMCP("longterm-memory")


@mcp.tool()
def create_entities(entities: list[dict]) -> str:
    """
    Create multiple entities in the knowledge graph.
    Each entity: {"name": str, "entityType": str, "observations": [str]}
    """
    results = []
    for e in entities:
        result = engine.create_entity(
            name=e["name"],
            entity_type=e.get("entityType", "general"),
            observations=e.get("observations", [])
        )
        results.append(result)
    return json.dumps(results, ensure_ascii=False)


@mcp.tool()
def create_relations(relations: list[dict]) -> str:
    """
    Create relations between entities.
    Each relation: {"from": str, "to": str, "relationType": str}
    """
    results = []
    for r in relations:
        result = engine.create_relation(
            from_entity=r["from"],
            relation_type=r["relationType"],
            to_entity=r["to"]
        )
        results.append(result)
    return json.dumps(results, ensure_ascii=False)


@mcp.tool()
def add_observations(observations: list[dict]) -> str:
    """
    Add observations to existing entities.
    Each item: {"entityName": str, "contents": [str]}
    """
    results = []
    for item in observations:
        for obs in item.get("contents", []):
            result = engine.add_observation(
                entity_name=item["entityName"],
                observation=obs
            )
            results.append(result)
    return json.dumps(results, ensure_ascii=False)


@mcp.tool()
def search_nodes(query: str) -> str:
    """Search entities and observations by keyword."""
    results = engine.search_nodes(query)
    return json.dumps(results, ensure_ascii=False)


@mcp.tool()
def open_nodes(names: list[str]) -> str:
    """Retrieve specific entities by name."""
    results = engine.open_nodes(names)
    return json.dumps(results, ensure_ascii=False)


@mcp.tool()
def read_graph() -> str:
    """Export the full knowledge graph summary."""
    result = engine.read_graph()
    return json.dumps(result, ensure_ascii=False)


@mcp.tool()
def delete_entities(names: list[str]) -> str:
    """Delete entities and their relations."""
    results = [engine.delete_entity(name) for name in names]
    return json.dumps(results, ensure_ascii=False)


if __name__ == "__main__":
    mcp.run()
