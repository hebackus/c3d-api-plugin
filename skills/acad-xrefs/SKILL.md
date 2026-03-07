---
name: acad-xrefs
description: external references, xref attach and overlay, xref path management, binding xrefs, detach unload reload, nested xrefs, xref notification and demand loading, BlockTableRecord xref properties, xref layer naming, XrefGraph dependency analysis
---

# AutoCAD External References (Xrefs)

Use this skill when working with external reference drawings — attaching, overlaying, binding, detaching, reloading, or analyzing xref dependencies in an AutoCAD drawing.

## Attachment vs Overlay

AutoCAD supports two xref modes:

- **Attachment** — the xref and all its nested xrefs propagate into any drawing that references the host. Use for shared base files (survey, utilities) that should always travel with the drawing.
- **Overlay** — the xref appears only in the immediate host drawing. Nested overlays are ignored by parent drawings. Use to avoid circular references or to keep coordination views local.

The mode is stored on the `BlockTableRecord` and can be changed after the fact by toggling `IsFromOverlayReference`.

## Attaching Xrefs

### Attach (Standard Attachment)

```csharp
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.Geometry;

public static ObjectId AttachXref(Database db, string xrefPath, string blockName)
{
    // AttachXref returns the ObjectId of the new BlockTableRecord
    ObjectId xrefBtrId = db.AttachXref(xrefPath, blockName);

    using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        BlockTableRecord modelSpace = (BlockTableRecord)tr.GetObject(
            SymbolUtilityServices.GetBlockModelSpaceId(db), OpenMode.ForWrite);

        // Insert a reference to the xref block
        using (BlockReference br = new BlockReference(Point3d.Origin, xrefBtrId))
        {
            modelSpace.AppendEntity(br);
            tr.AddNewlyCreatedDBObject(br, true);
        }

        tr.Commit();
    }

    return xrefBtrId;
}
```

### Overlay

```csharp
public static ObjectId OverlayXref(Database db, string xrefPath, string blockName)
{
    ObjectId xrefBtrId = db.OverlayXref(xrefPath, blockName);

    using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        BlockTableRecord modelSpace = (BlockTableRecord)tr.GetObject(
            SymbolUtilityServices.GetBlockModelSpaceId(db), OpenMode.ForWrite);

        using (BlockReference br = new BlockReference(Point3d.Origin, xrefBtrId))
        {
            modelSpace.AppendEntity(br);
            tr.AddNewlyCreatedDBObject(br, true);
        }

        tr.Commit();
    }

    return xrefBtrId;
}
```

### Key Points

- `db.AttachXref(path, name)` and `db.OverlayXref(path, name)` both return the `ObjectId` of the created `BlockTableRecord`.
- The block name must be unique in the block table. If a block with that name already exists, the call throws.
- The returned BTR has no insertion in model space yet — you must create a `BlockReference` yourself.
- The xref file does not need to exist at attach time, but will show as unresolved until found.

## Xref Path Management

### Path Types

- **Absolute path** — full path stored (e.g., `C:\Projects\Survey.dwg`). Breaks when files move.
- **Relative path** — path relative to the host drawing (e.g., `.\Xrefs\Survey.dwg`). Preferred for project portability. Requires the host drawing to be saved first.
- **No path (found path)** — AutoCAD searches its support file paths and project paths to locate the xref by filename alone.

### Reading and Setting Paths

```csharp
public static void ManageXrefPath(Database db, string blockName)
{
    using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        BlockTable bt = (BlockTable)tr.GetObject(db.BlockTableId, OpenMode.ForRead);

        if (!bt.Has(blockName))
            return;

        BlockTableRecord btr = (BlockTableRecord)tr.GetObject(bt[blockName], OpenMode.ForWrite);

        if (!btr.IsFromExternalReference)
            return;

        // Read current path
        string currentPath = btr.PathName;

        // Change to a new path (absolute or relative)
        btr.PathName = @".\Xrefs\Survey.dwg";

        // Read the resolved (found) path — where AutoCAD actually found the file
        string foundPath = btr.GetXrefDatabase(false)?.Filename;

        tr.Commit();
    }
}
```

### Properties

- `PathName` (string, get/set) — the stored reference path (absolute or relative)
- `GetXrefDatabase(bool)` — returns the `Database` of the resolved xref; pass `false` to avoid forcing a load

## Binding Xrefs

Binding converts xref-dependent objects into local objects, removing the external dependency.

### Bind vs Insert Mode

- **Bind mode** — renames xref-dependent symbols as `BlockName$0$LayerName`. Preserves the xref origin in the symbol name.
- **Insert mode** — merges xref-dependent symbols directly, renaming to just `LayerName` (stripping the block prefix). If a symbol already exists locally, the local version wins.

```csharp
public static void BindXrefs(Database db, ObjectIdCollection xrefBtrIds, bool insertMode)
{
    // insertMode: true = insert-style bind, false = traditional bind
    db.BindXrefs(xrefBtrIds, !insertMode);

    // The second parameter is "bInsertBind" — confusingly:
    //   true  = traditional bind  (BlockName$0$Symbol)
    //   false = insert-style bind (Symbol merged directly)
    // So we negate insertMode to match the API expectation.
}
```

### Binding a Single Xref

```csharp
public static void BindSingleXref(Database db, string blockName, bool insertMode)
{
    using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        BlockTable bt = (BlockTable)tr.GetObject(db.BlockTableId, OpenMode.ForRead);

        if (!bt.Has(blockName))
            return;

        ObjectIdCollection ids = new ObjectIdCollection();
        ids.Add(bt[blockName]);

        // No commit needed — BindXrefs operates outside the transaction
        tr.Commit();
    }

    db.BindXrefs(ids, !insertMode);
}
```

## Detaching, Unloading, and Reloading

### Detach

Permanently removes the xref definition and all its block references from the drawing.

```csharp
public static void DetachXref(Database db, string blockName)
{
    using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        BlockTable bt = (BlockTable)tr.GetObject(db.BlockTableId, OpenMode.ForRead);

        if (!bt.Has(blockName))
            return;

        ObjectId btrId = bt[blockName];
        db.DetachXref(btrId);

        tr.Commit();
    }
}
```

### Unload

Keeps the xref definition but suppresses its display and frees memory. Block references remain as placeholders.

```csharp
public static void UnloadXref(Database db, string blockName)
{
    using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        BlockTable bt = (BlockTable)tr.GetObject(db.BlockTableId, OpenMode.ForRead);

        if (!bt.Has(blockName))
            return;

        BlockTableRecord btr = (BlockTableRecord)tr.GetObject(bt[blockName], OpenMode.ForWrite);

        if (btr.IsFromExternalReference)
        {
            btr.IsUnloaded = true;
        }

        tr.Commit();
    }
}
```

### Reload

Forces AutoCAD to re-read the xref from disk.

```csharp
public static void ReloadXref(Database db, string blockName)
{
    using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        BlockTable bt = (BlockTable)tr.GetObject(db.BlockTableId, OpenMode.ForRead);

        if (!bt.Has(blockName))
            return;

        ObjectIdCollection ids = new ObjectIdCollection();
        ids.Add(bt[blockName]);

        // ReloadXrefs takes a collection
        db.ReloadXrefs(ids);

        tr.Commit();
    }
}
```

## Nested Xrefs

An xref can itself contain xrefs. Behavior depends on the mode:

- **Attached xrefs** propagate their nested attached xrefs into the host.
- **Overlaid xrefs** do NOT propagate their nested overlays (but do propagate nested attachments).
- A nested overlay in an attached xref is ignored by grandparent drawings.

### Resolving Nested References

Use `XrefGraph` (see below) to walk the full dependency tree including nested references. Nested xref BTRs appear in the host's block table with their own `IsFromExternalReference` flag.

## Xref Notification and Demand Loading

### Xref Notification

AutoCAD can notify users when an xref file changes on disk.

```csharp
// Enable/disable xref notification via system variable
Autodesk.AutoCAD.ApplicationServices.Application.SetSystemVariable("XNOTIFY", 1); // 0=off, 1=on
```

### Demand Loading

Controls how much of an xref is loaded into memory.

```csharp
// XLOADCTL system variable:
// 0 = load entire xref
// 1 = demand-load (load objects as needed, xref file locked)
// 2 = demand-load with copy (load from copy, original not locked)
Autodesk.AutoCAD.ApplicationServices.Application.SetSystemVariable("XLOADCTL", 2);
```

- `XLOADCTL = 2` is recommended for multi-user environments — allows others to edit the xref while it is referenced.

## BlockTableRecord Xref Properties

Key properties on `BlockTableRecord` for xref inspection:

- `IsFromExternalReference` (bool, get) — true if this BTR represents an xref (attachment or overlay)
- `IsFromOverlayReference` (bool, get/set) — true if overlay mode; false if attachment mode. Writable to change mode after attach.
- `IsUnloaded` (bool, get/set) — true if the xref is currently unloaded
- `IsResolved` (bool, get) — true if AutoCAD successfully found and loaded the xref file
- `XrefStatus` (XrefStatus, get) — current status enum value
- `PathName` (string, get/set) — stored file path for the xref
- `IsDependent` (bool, get) — true if this BTR came in through an xref (xref-dependent symbol)

### XrefStatus Enum Values

- `NotAnXref` — BTR is a regular block, not an xref
- `Resolved` — xref loaded successfully
- `FileNotFound` — xref file could not be located
- `Unloaded` — xref is intentionally unloaded
- `Unreferenced` — xref BTR exists but no block references point to it
- `Unresolved` — xref could not be resolved (general failure)

### Enumerating All Xrefs

```csharp
public static void ListAllXrefs(Database db)
{
    using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        BlockTable bt = (BlockTable)tr.GetObject(db.BlockTableId, OpenMode.ForRead);

        foreach (ObjectId btrId in bt)
        {
            BlockTableRecord btr = (BlockTableRecord)tr.GetObject(btrId, OpenMode.ForRead);

            if (!btr.IsFromExternalReference)
                continue;

            string mode = btr.IsFromOverlayReference ? "Overlay" : "Attach";
            string status = btr.XrefStatus.ToString();
            string path = btr.PathName;

            // btr.Name is the xref block name
            System.Diagnostics.Debug.WriteLine(
                $"Xref: {btr.Name}, Mode: {mode}, Status: {status}, Path: {path}");
        }

        tr.Commit();
    }
}
```

## Xref Layer Naming

Xref-dependent layers follow the naming convention `BlockName|LayerName`. The pipe character (`|`) separates the xref block name from the original layer name.

```csharp
public static void InspectXrefLayers(Database db)
{
    using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        LayerTable lt = (LayerTable)tr.GetObject(db.LayerTableId, OpenMode.ForRead);

        foreach (ObjectId layerId in lt)
        {
            LayerTableRecord ltr = (LayerTableRecord)tr.GetObject(layerId, OpenMode.ForRead);

            if (ltr.IsDependent)
            {
                // Layer came from an xref
                // Name format: "XrefBlockName|OriginalLayerName"
                string fullName = ltr.Name;
                int pipeIndex = fullName.IndexOf('|');
                string xrefName = fullName.Substring(0, pipeIndex);
                string originalLayer = fullName.Substring(pipeIndex + 1);

                System.Diagnostics.Debug.WriteLine(
                    $"Xref layer: {fullName} (from xref '{xrefName}', original: '{originalLayer}')");
            }
        }

        tr.Commit();
    }
}
```

After binding with **bind mode**, the pipe becomes `$0$` (e.g., `Survey$0$Contours`). After binding with **insert mode**, the prefix is stripped entirely and the layer merges with any existing local layer of the same name.

## XrefGraph for Dependency Analysis

The `XrefGraph` class provides a directed graph of all xref relationships in a database.

```csharp
using Autodesk.AutoCAD.DatabaseServices;

public static void AnalyzeXrefDependencies(Database db)
{
    XrefGraph graph = db.GetHostDwgXrefGraph(false);

    // Node 0 is always the host drawing
    XrefGraphNode hostNode = graph.HostDrawing;
    System.Diagnostics.Debug.WriteLine($"Host: {hostNode.Name}");

    // Iterate all nodes (index 0 = host, 1..N = xrefs)
    for (int i = 0; i < graph.NumNodes; i++)
    {
        XrefGraphNode node = graph.GetXrefNode(i);

        string name = node.Name;
        ObjectId btrId = node.BlockTableRecordId;
        bool isNested = node.IsNested;
        XrefStatus status = node.XrefStatus;

        System.Diagnostics.Debug.WriteLine(
            $"Node {i}: {name}, Nested: {isNested}, Status: {status}");

        // Walk outgoing edges (this node's children / nested xrefs)
        for (int j = 0; j < node.NumOut; j++)
        {
            XrefGraphNode child = node.Out(j) as XrefGraphNode;
            if (child != null)
            {
                System.Diagnostics.Debug.WriteLine($"  -> {child.Name}");
            }
        }
    }
}
```

### XrefGraphNode Properties

- `Name` (string, get) — block name of the xref
- `BlockTableRecordId` (ObjectId, get) — ObjectId of the corresponding BTR
- `IsNested` (bool, get) — true if this xref is nested inside another xref
- `XrefStatus` (XrefStatus, get) — resolution status of this node
- `NumIn` (int, get) — number of incoming edges (parents referencing this xref)
- `NumOut` (int, get) — number of outgoing edges (xrefs nested inside this one)
- `In(int)` — get parent node at index
- `Out(int)` — get child node at index

### Detecting Circular References

```csharp
public static bool HasCircularXrefs(Database db)
{
    XrefGraph graph = db.GetHostDwgXrefGraph(false);

    // A circular reference manifests as a node that is both
    // an ancestor and descendant of another node.
    // The XrefGraph handles this — circular xrefs show
    // XrefStatus.Unresolved and AutoCAD refuses to load them.

    for (int i = 1; i < graph.NumNodes; i++)
    {
        XrefGraphNode node = graph.GetXrefNode(i);
        if (node.XrefStatus == XrefStatus.Unresolved)
        {
            // Could be circular or simply missing — check PathName
            return true;
        }
    }

    return false;
}
```

## Gotchas

- `db.BindXrefs()` second parameter naming is counterintuitive: `true` = traditional bind (`$0$` renaming), `false` = insert-style bind (merge). Many codebases get this backwards.
- `db.DetachXref()` will fail if block references to the xref still exist in the drawing. Erase all references first, or use `db.ResolveXrefs()` after erasing.
- Xref paths are stored as-is. If you attach with a relative path, the host drawing must be saved to a location first, or the relative path has no anchor point.
- `btr.GetXrefDatabase(true)` forces a load and can throw if the file is missing. Use `false` to get the cached database without forcing resolution.
- Overlay xrefs do not propagate through nesting. If Drawing A overlays Drawing B, and Drawing C attaches Drawing A, Drawing C will NOT see Drawing B.
- After `BindXrefs()`, the BTR is converted to a regular block. `IsFromExternalReference` becomes `false`, and the original xref layer names transform according to the bind mode.
- `XrefGraph` node index 0 is always the host drawing, not an xref. Start iteration at index 1 to process only xrefs.
- Xref-dependent layers (`BlockName|LayerName`) are read-only. You cannot rename, freeze, or change properties of xref-dependent layers until the xref is bound.
- `ReloadXrefs()` does not update block references in layouts automatically. A `REGEN` or `Editor.Regen()` may be needed to refresh the display.
- Demand loading with `XLOADCTL = 1` locks the xref file on disk. Use `XLOADCTL = 2` in team environments to avoid file-locking conflicts.

## Related Skills

- `acad-blocks` — xref definitions live in the block table as specialized BlockTableRecords
- `acad-layers` — xref-dependent layers use `BlockName|LayerName` naming and become editable after binding
- `acad-database-operations` — wblock and insert operations interact with xref resolution and binding
- `acad-layouts-viewports` — xrefs display in viewports with per-viewport layer freeze/thaw control
