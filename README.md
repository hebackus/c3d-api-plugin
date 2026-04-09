# c3d-api — Civil 3D / AutoCAD .NET API Plugin

A Claude Code plugin providing a complete knowledge base for AutoCAD Civil 3D 2026 and AutoCAD 2026 .NET API development.

## Components

| Component | Count | Description |
|-----------|-------|-------------|
| **Skills** | 48 | API reference guides with code examples, gotchas, cross-references |
| **MCP Tools** | 6 | Structured API database queries (8,330 types, 31,254 members) |
| **Agents** | 4 | Specialized subagents for exploration, verification, and skill management |
| **Dev Guides** | 819 | Official Autodesk developer guide pages (Civil 3D + AutoCAD) |

## MCP Tools

| Tool | Purpose |
|------|---------|
| `lookup_type` | Get type metadata and all members (properties, methods, events, etc.) |
| `search_api` | Full-text search across all types and members |
| `get_parameters` | Method/constructor parameter details with overloads |
| `get_enum_values` | Enum value listings |
| `list_namespace` | All types in a namespace, grouped by kind |
| `search_devguide` | Keyword search across 819 developer guide pages |

## Agents

| Agent | Purpose |
|-------|---------|
| `api-explorer` | Finds types, methods, and patterns for a given development task |
| `code-verifier` | Reviews C# code for correct API usage against the database |
| `skill-writer` | Creates new SKILL.md files following format conventions |
| `skill-reviewer` | Audits SKILL.md files for quality and accuracy |

## Installation

```bash
claude /install-plugin hebackus/c3d-api-plugin
```

### Prerequisites

- Python 3.10+ with `mcp` package:
  ```bash
  pip install mcp
  ```

## Data Sources

- **SQLite Database** (`data/api_combined_2026.db`) — Parsed from decompiled Civil 3D and AutoCAD 2026 .NET assemblies. Contains types, members, parameters, enum values, interfaces, and attributes with FTS5 full-text search indexes.
- **Developer Guides** (`data/devguide/`) — Official Autodesk CloudHelp developer guides converted to markdown. 461 Civil 3D pages + 358 AutoCAD pages.
- **Skills** (`skills/`) — 25 AutoCAD skills + 23 Civil 3D skills with curated code examples, property/method references, gotchas, and cross-references.

## Updating Data

When the API database is regenerated, copy updated files into the plugin:

```bash
cp scripts/ApiParser/api_combined_2026.db CSharp/plugins/c3d-api/data/
cp -r ac3d_netapi2docs/docs/markdown/CIV3D_DevGuide CSharp/plugins/c3d-api/data/devguide/
cp -r ac3d_netapi2docs/docs/markdown/OARX_NET_DevGuide CSharp/plugins/c3d-api/data/devguide/
```
