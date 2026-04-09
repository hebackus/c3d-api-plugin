"""Civil 3D / AutoCAD .NET API MCP Server.

Exposes the api_combined_2026.db SQLite database and developer guide markdown
files as structured MCP tools for Claude Code.
"""

import os
import re
import sqlite3
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = os.environ.get(
    "C3D_API_DB_PATH",
    str(_ROOT / "data" / "api_combined_2026.db"),
)
DEVGUIDE_PATH = _ROOT / "data" / "devguide"

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
_conn: sqlite3.Connection | None = None


def _db() -> sqlite3.Connection:
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        _conn.row_factory = sqlite3.Row
        _conn.execute("PRAGMA query_only = ON")
    return _conn


# ---------------------------------------------------------------------------
# FTS helpers
# ---------------------------------------------------------------------------
_FTS_UNSAFE = re.compile(r"[^\w\s*]", re.UNICODE)


def _sanitize_fts(query: str) -> str:
    """Strip characters that break FTS5 MATCH and wrap tokens."""
    cleaned = _FTS_UNSAFE.sub(" ", query).strip()
    tokens = cleaned.split()
    if not tokens:
        return ""
    # Quote each token so multi-word queries use implicit AND
    return " ".join(f'"{t}"' for t in tokens)


# ---------------------------------------------------------------------------
# Dev-guide file cache
# ---------------------------------------------------------------------------
_devguide_files: list[Path] | None = None


def _get_devguide_files() -> list[Path]:
    global _devguide_files
    if _devguide_files is None:
        _devguide_files = sorted(DEVGUIDE_PATH.rglob("*.md")) if DEVGUIDE_PATH.is_dir() else []
    return _devguide_files


# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------
mcp = FastMCP(
    "c3d-api",
    instructions="Civil 3D / AutoCAD .NET API knowledge base — 8,330 types, 31,254 members, 819 developer guide pages",
)


# ---- Tool 1: lookup_type -------------------------------------------------
@mcp.tool()
def lookup_type(
    name: str,
    kind_filter: str | None = None,
    obsolete_only: bool = False,
) -> str:
    """Look up a Civil 3D or AutoCAD .NET API type by name.

    Returns the type's namespace, kind, base type, interfaces, and all members
    grouped by kind (properties, methods, events, fields, constructors).

    Args:
        name: Exact type name (e.g. "Alignment", "Point3d"). Falls back to
              fuzzy search if no exact match.
        kind_filter: Optional member kind filter — one of: property, method,
                     event, field, constructor, operator, indexer.
        obsolete_only: If True, return only obsolete members with their
                       deprecation messages.
    """
    db = _db()

    # Exact match first
    row = db.execute(
        """SELECT t.id, t.name, t.kind, t.modifiers, t.base_type,
                  t.is_obsolete, t.obsolete_message, t.assembly, n.name AS ns
           FROM types t JOIN namespaces n ON t.namespace_id = n.id
           WHERE t.name = ?""",
        (name,),
    ).fetchone()

    # Fuzzy fallback
    if row is None:
        candidates = db.execute(
            """SELECT t.name, t.kind, n.name AS ns
               FROM types t JOIN namespaces n ON t.namespace_id = n.id
               WHERE t.name LIKE ? ORDER BY t.name LIMIT 10""",
            (f"%{name}%",),
        ).fetchall()
        if not candidates:
            return f"No type found matching '{name}'."
        lines = [f"No exact match for '{name}'. Did you mean:\n"]
        for c in candidates:
            lines.append(f"- **{c['name']}** ({c['kind']}) — {c['ns']}")
        return "\n".join(lines)

    # Header
    out: list[str] = []
    obs = " [OBSOLETE]" if row["is_obsolete"] else ""
    out.append(f"## {row['name']} ({row['kind']}){obs}")
    out.append(f"**Namespace:** {row['ns']}")
    if row["base_type"]:
        out.append(f"**Base:** {row['base_type']}")
    if row["assembly"]:
        out.append(f"**Assembly:** {row['assembly']}")
    if row["is_obsolete"] and row["obsolete_message"]:
        out.append(f"**Obsolete:** {row['obsolete_message']}")

    # Interfaces
    ifaces = db.execute(
        "SELECT interface_name FROM type_interfaces WHERE type_id = ? ORDER BY interface_name",
        (row["id"],),
    ).fetchall()
    if ifaces:
        out.append(f"**Interfaces:** {', '.join(i['interface_name'] for i in ifaces)}")

    out.append("")

    # Members
    where_clauses = ["m.type_id = ?"]
    params: list = [row["id"]]

    if kind_filter:
        where_clauses.append("m.kind = ?")
        params.append(kind_filter.lower())
    if obsolete_only:
        where_clauses.append("m.is_obsolete = 1")

    members = db.execute(
        f"""SELECT m.kind, m.name, m.return_type, m.modifiers,
                   m.is_obsolete, m.obsolete_message
            FROM members m
            WHERE {' AND '.join(where_clauses)}
            ORDER BY m.kind, m.name""",
        params,
    ).fetchall()

    if not members:
        if kind_filter or obsolete_only:
            out.append("_No matching members._")
        else:
            out.append("_No members found._")
        return "\n".join(out)

    # Group by kind
    current_kind = ""
    for m in members:
        if m["kind"] != current_kind:
            current_kind = m["kind"]
            kind_count = sum(1 for x in members if x["kind"] == current_kind)
            out.append(f"### {current_kind.title()}s ({kind_count})")
        mods = f" [{m['modifiers']}]" if m["modifiers"] else ""
        ret = f" -> {m['return_type']}" if m["return_type"] else ""
        obs_mark = " **[OBSOLETE]**" if m["is_obsolete"] else ""
        obs_msg = f" _{m['obsolete_message']}_" if m["is_obsolete"] and m["obsolete_message"] else ""
        out.append(f"- `{m['name']}`{ret}{mods}{obs_mark}{obs_msg}")

    return "\n".join(out)


# ---- Tool 2: search_api --------------------------------------------------
@mcp.tool()
def search_api(query: str, limit: int = 20) -> str:
    """Full-text search across all API types and members.

    Searches type names, base types, member names, and return types.
    Returns a combined list of matching types and members.

    Args:
        query: Search terms (e.g. "Profile", "GetStation", "Surface Volume").
        limit: Maximum results to return (default 20).
    """
    db = _db()
    fts_query = _sanitize_fts(query)

    results: list[str] = []

    if fts_query:
        # Search types
        type_rows = db.execute(
            """SELECT t.name, t.kind, n.name AS ns
               FROM types_fts fts
               JOIN types t ON fts.rowid = t.id
               JOIN namespaces n ON t.namespace_id = n.id
               WHERE types_fts MATCH ?
               LIMIT ?""",
            (fts_query, limit),
        ).fetchall()

        for r in type_rows:
            results.append(f"- **[type]** {r['name']} ({r['kind']}) — {r['ns']}")

        # Search members
        remaining = max(0, limit - len(type_rows))
        if remaining > 0:
            member_rows = db.execute(
                """SELECT t.name AS type_name, m.name, m.kind, m.return_type
                   FROM members_fts fts
                   JOIN members m ON fts.rowid = m.id
                   JOIN types t ON m.type_id = t.id
                   WHERE members_fts MATCH ?
                   LIMIT ?""",
                (fts_query, remaining),
            ).fetchall()

            for r in member_rows:
                ret = f" -> {r['return_type']}" if r["return_type"] else ""
                results.append(f"- **[{r['kind']}]** {r['type_name']}.{r['name']}{ret}")

    # LIKE fallback if FTS returned nothing
    if not results:
        like_pattern = f"%{query}%"
        type_rows = db.execute(
            """SELECT t.name, t.kind, n.name AS ns
               FROM types t JOIN namespaces n ON t.namespace_id = n.id
               WHERE t.name LIKE ? ORDER BY t.name LIMIT ?""",
            (like_pattern, limit),
        ).fetchall()
        for r in type_rows:
            results.append(f"- **[type]** {r['name']} ({r['kind']}) — {r['ns']}")

        remaining = max(0, limit - len(type_rows))
        if remaining > 0:
            member_rows = db.execute(
                """SELECT t.name AS type_name, m.name, m.kind, m.return_type
                   FROM members m JOIN types t ON m.type_id = t.id
                   WHERE m.name LIKE ? ORDER BY m.name LIMIT ?""",
                (like_pattern, remaining),
            ).fetchall()
            for r in member_rows:
                ret = f" -> {r['return_type']}" if r["return_type"] else ""
                results.append(f"- **[{r['kind']}]** {r['type_name']}.{r['name']}{ret}")

    if not results:
        return f"No results for '{query}'."

    header = f"## Search results for '{query}' ({len(results)} matches)\n"
    return header + "\n".join(results)


# ---- Tool 3: get_parameters ----------------------------------------------
@mcp.tool()
def get_parameters(type_name: str, member_name: str) -> str:
    """Get parameter details for a method or constructor.

    Shows all overloads with parameter names, types, modifiers (ref/out/params),
    and default values.

    Args:
        type_name: The type that owns the member (e.g. "Alignment").
        member_name: The method or constructor name (e.g. "Create", ".ctor").
    """
    db = _db()

    rows = db.execute(
        """SELECT m.id, m.name, m.return_type, m.modifiers, m.kind
           FROM members m JOIN types t ON m.type_id = t.id
           WHERE t.name = ? AND m.name = ?
           ORDER BY m.id""",
        (type_name, member_name),
    ).fetchall()

    if not rows:
        # Try constructors if member_name matches type
        if member_name == type_name or member_name == ".ctor":
            rows = db.execute(
                """SELECT m.id, m.name, m.return_type, m.modifiers, m.kind
                   FROM members m JOIN types t ON m.type_id = t.id
                   WHERE t.name = ? AND m.kind = 'constructor'
                   ORDER BY m.id""",
                (type_name,),
            ).fetchall()

    if not rows:
        return f"No member '{member_name}' found on type '{type_name}'."

    out: list[str] = [f"## {type_name}.{member_name} — {len(rows)} overload(s)\n"]

    for i, m in enumerate(rows, 1):
        params = db.execute(
            """SELECT p.ordinal, p.name, p.type, p.modifier, p.default_value
               FROM parameters p WHERE p.member_id = ?
               ORDER BY p.ordinal""",
            (m["id"],),
        ).fetchall()

        mods = f" [{m['modifiers']}]" if m["modifiers"] else ""
        ret = f" -> {m['return_type']}" if m["return_type"] else ""
        out.append(f"### Overload {i}{mods}{ret}")

        if not params:
            out.append("_(no parameters)_\n")
            continue

        for p in params:
            mod = f"_{p['modifier']}_ " if p["modifier"] else ""
            default = f" = `{p['default_value']}`" if p["default_value"] else ""
            out.append(f"{p['ordinal']}. {mod}**{p['name']}** : `{p['type']}`{default}")
        out.append("")

    return "\n".join(out)


# ---- Tool 4: get_enum_values ---------------------------------------------
@mcp.tool()
def get_enum_values(enum_name: str) -> str:
    """Get all values of an enum type.

    Args:
        enum_name: The enum type name (e.g. "AlignmentType", "OpenMode").
    """
    db = _db()

    type_row = db.execute(
        """SELECT t.id, t.name, t.kind, n.name AS ns
           FROM types t JOIN namespaces n ON t.namespace_id = n.id
           WHERE t.name = ?""",
        (enum_name,),
    ).fetchone()

    if type_row is None:
        # Fuzzy search
        candidates = db.execute(
            """SELECT t.name, n.name AS ns FROM types t
               JOIN namespaces n ON t.namespace_id = n.id
               WHERE t.name LIKE ? AND t.kind = 'enum'
               ORDER BY t.name LIMIT 10""",
            (f"%{enum_name}%",),
        ).fetchall()
        if not candidates:
            return f"No enum found matching '{enum_name}'."
        lines = [f"No exact match for '{enum_name}'. Enum candidates:\n"]
        for c in candidates:
            lines.append(f"- **{c['name']}** — {c['ns']}")
        return "\n".join(lines)

    if type_row["kind"] != "enum":
        return f"'{enum_name}' is a {type_row['kind']}, not an enum."

    values = db.execute(
        """SELECT ev.name, ev.value FROM enum_values ev
           WHERE ev.type_id = ? ORDER BY ev.rowid""",
        (type_row["id"],),
    ).fetchall()

    out = [f"## {type_row['name']} (enum)", f"**Namespace:** {type_row['ns']}\n"]
    for v in values:
        val_str = f" = {v['value']}" if v["value"] is not None else ""
        out.append(f"- `{v['name']}`{val_str}")

    if not values:
        out.append("_(no values defined)_")

    return "\n".join(out)


# ---- Tool 5: list_namespace ----------------------------------------------
@mcp.tool()
def list_namespace(namespace: str) -> str:
    """List all types in a namespace, grouped by kind.

    Args:
        namespace: Full or partial namespace name
                   (e.g. "Autodesk.Civil.DatabaseServices").
    """
    db = _db()

    # Exact match first
    rows = db.execute(
        """SELECT t.name, t.kind, t.is_obsolete
           FROM types t JOIN namespaces n ON t.namespace_id = n.id
           WHERE n.name = ?
           ORDER BY t.kind, t.name""",
        (namespace,),
    ).fetchall()

    matched_ns = namespace

    # Partial match fallback
    if not rows:
        ns_matches = db.execute(
            "SELECT name FROM namespaces WHERE name LIKE ? ORDER BY name LIMIT 10",
            (f"%{namespace}%",),
        ).fetchall()

        if not ns_matches:
            return f"No namespace found matching '{namespace}'."

        if len(ns_matches) == 1:
            matched_ns = ns_matches[0]["name"]
            rows = db.execute(
                """SELECT t.name, t.kind, t.is_obsolete
                   FROM types t JOIN namespaces n ON t.namespace_id = n.id
                   WHERE n.name = ?
                   ORDER BY t.kind, t.name""",
                (matched_ns,),
            ).fetchall()
        else:
            lines = [f"Multiple namespaces match '{namespace}':\n"]
            for ns in ns_matches:
                count = db.execute(
                    """SELECT COUNT(*) AS c FROM types t
                       JOIN namespaces n ON t.namespace_id = n.id
                       WHERE n.name = ?""",
                    (ns["name"],),
                ).fetchone()["c"]
                lines.append(f"- **{ns['name']}** ({count} types)")
            return "\n".join(lines)

    out = [f"## {matched_ns} ({len(rows)} types)\n"]

    current_kind = ""
    for r in rows:
        if r["kind"] != current_kind:
            current_kind = r["kind"]
            kind_count = sum(1 for x in rows if x["kind"] == current_kind)
            out.append(f"### {current_kind.title()}s ({kind_count})")
        obs = " [OBSOLETE]" if r["is_obsolete"] else ""
        out.append(f"- {r['name']}{obs}")

    return "\n".join(out)


# ---- Tool 6: search_devguide ---------------------------------------------
@mcp.tool()
def search_devguide(query: str, limit: int = 10) -> str:
    """Search the Civil 3D and AutoCAD developer guide markdown files.

    Searches file content for keywords and returns matching pages with
    breadcrumb paths and context snippets.

    Args:
        query: Search terms (e.g. "corridor baseline", "transaction",
               "block reference").
        limit: Maximum results to return (default 10).
    """
    files = _get_devguide_files()
    if not files:
        return "Developer guide files not found."

    pattern = re.compile(re.escape(query), re.IGNORECASE)
    results: list[tuple[int, str, str, str]] = []  # (count, breadcrumb, title, snippet)

    for fpath in files:
        try:
            content = fpath.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        matches = pattern.findall(content)
        if not matches:
            continue

        # Extract breadcrumb from first HTML comment
        breadcrumb = ""
        bc_match = re.search(r"<!--\s*(.+?)\s*-->", content)
        if bc_match:
            bc_text = bc_match.group(1)
            if "Source:" not in bc_text:
                breadcrumb = bc_text.strip()

        # Extract H1 title
        title = ""
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()

        # Snippet around first match
        first = pattern.search(content)
        if first:
            start = max(0, first.start() - 100)
            end = min(len(content), first.end() + 100)
            snippet = content[start:end].replace("\n", " ").strip()
            if start > 0:
                snippet = "..." + snippet
            if end < len(content):
                snippet = snippet + "..."
        else:
            snippet = ""

        # Relative path for display
        rel_path = fpath.relative_to(DEVGUIDE_PATH)
        guide_type = "Civil 3D" if "CIV3D" in str(rel_path) else "AutoCAD"

        results.append((len(matches), breadcrumb, title, snippet, guide_type, str(rel_path)))

    # Sort by match count descending
    results.sort(key=lambda x: x[0], reverse=True)
    results = results[:limit]

    if not results:
        return f"No developer guide pages match '{query}'."

    out = [f"## Developer guide results for '{query}' ({len(results)} pages)\n"]
    for count, breadcrumb, title, snippet, guide_type, rel_path in results:
        out.append(f"### [{guide_type}] {title or rel_path}")
        if breadcrumb:
            out.append(f"_{breadcrumb}_")
        out.append(f"**Matches:** {count} | **File:** `{rel_path}`")
        if snippet:
            out.append(f"> {snippet}")
        out.append("")

    return "\n".join(out)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run(transport="stdio")
