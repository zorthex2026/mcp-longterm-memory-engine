#!/usr/bin/env python3
"""
MCP Long-Term Memory Engine
Core SQLite-backed Knowledge Graph implementation.

Author: Renato Santi
DOI: 10.5281/zenodo.20625302
License: MIT
"""

import json
import sqlite3
from datetime import datetime
from typing import Optional


class MemoryEngine:
    """
    Local SQLite-backed Knowledge Graph for persistent LLM context.
    
    Stores entities, relations, and observations in a structured
    graph that persists across LLM session boundaries.
    """

    def __init__(self, db_path: str = "./memory.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the SQLite schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS entities (
                    name TEXT PRIMARY KEY,
                    entity_type TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS observations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entity_name TEXT NOT NULL,
                    observation TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (entity_name) REFERENCES entities(name)
                );

                CREATE TABLE IF NOT EXISTS relations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    from_entity TEXT NOT NULL,
                    relation_type TEXT NOT NULL,
                    to_entity TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (from_entity) REFERENCES entities(name),
                    FOREIGN KEY (to_entity) REFERENCES entities(name)
                );
            """)

    def create_entity(self, name: str, entity_type: str,
                      observations: list[str] = None) -> dict:
        """Create a new entity in the knowledge graph."""
        now = datetime.utcnow().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR IGNORE INTO entities (name, entity_type, created_at) VALUES (?, ?, ?)",
                (name, entity_type, now)
            )
            if observations:
                for obs in observations:
                    conn.execute(
                        "INSERT INTO observations (entity_name, observation, created_at) VALUES (?, ?, ?)",
                        (name, obs, now)
                    )
        return {"name": name, "type": entity_type, "observations": observations or []}

    def add_observation(self, entity_name: str, observation: str) -> dict:
        """Add an observation to an existing entity."""
        now = datetime.utcnow().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO observations (entity_name, observation, created_at) VALUES (?, ?, ?)",
                (entity_name, observation, now)
            )
        return {"entity": entity_name, "observation": observation}

    def create_relation(self, from_entity: str, relation_type: str,
                        to_entity: str) -> dict:
        """Create a directed relation between two entities."""
        now = datetime.utcnow().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO relations (from_entity, relation_type, to_entity, created_at) VALUES (?, ?, ?, ?)",
                (from_entity, relation_type, to_entity, now)
            )
        return {"from": from_entity, "relation": relation_type, "to": to_entity}

    def search_nodes(self, query: str, limit: int = 10) -> list[dict]:
        """Search entities and observations by keyword."""
        with sqlite3.connect(self.db_path) as conn:
            results = conn.execute("""
                SELECT DISTINCT e.name, e.entity_type,
                    GROUP_CONCAT(o.observation, ' | ') as observations
                FROM entities e
                LEFT JOIN observations o ON e.name = o.entity_name
                WHERE e.name LIKE ? OR o.observation LIKE ?
                GROUP BY e.name
                LIMIT ?
            """, (f"%{query}%", f"%{query}%", limit)).fetchall()

        return [
            {"name": r[0], "type": r[1], "observations": r[2].split(" | ") if r[2] else []}
            for r in results
        ]

    def open_nodes(self, names: list[str]) -> list[dict]:
        """Retrieve specific entities by name."""
        results = []
        with sqlite3.connect(self.db_path) as conn:
            for name in names:
                entity = conn.execute(
                    "SELECT name, entity_type FROM entities WHERE name = ?", (name,)
                ).fetchone()
                if entity:
                    obs = conn.execute(
                        "SELECT observation FROM observations WHERE entity_name = ?", (name,)
                    ).fetchall()
                    rels = conn.execute(
                        "SELECT relation_type, to_entity FROM relations WHERE from_entity = ?", (name,)
                    ).fetchall()
                    results.append({
                        "name": entity[0],
                        "type": entity[1],
                        "observations": [o[0] for o in obs],
                        "relations": [{"type": r[0], "to": r[1]} for r in rels]
                    })
        return results

    def read_graph(self) -> dict:
        """Export the full knowledge graph."""
        with sqlite3.connect(self.db_path) as conn:
            entities = conn.execute(
                "SELECT name, entity_type FROM entities"
            ).fetchall()
            relations = conn.execute(
                "SELECT from_entity, relation_type, to_entity FROM relations"
            ).fetchall()

        return {
            "entities": [{"name": e[0], "type": e[1]} for e in entities],
            "relations": [{"from": r[0], "type": r[1], "to": r[2]} for r in relations],
            "total_entities": len(entities),
            "total_relations": len(relations)
        }

    def delete_entity(self, name: str) -> dict:
        """Delete an entity and all its observations and relations."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM observations WHERE entity_name = ?", (name,))
            conn.execute(
                "DELETE FROM relations WHERE from_entity = ? OR to_entity = ?", (name, name)
            )
            conn.execute("DELETE FROM entities WHERE name = ?", (name,))
        return {"deleted": name}
